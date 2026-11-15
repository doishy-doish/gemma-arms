#!/usr/bin/env node
// cpu/smoke-agent.mjs — stdlib-only CPU agent loop (node 20). No deps, no secrets.
// Tools: READ/LS/GREP/EDIT(single-line)/WRITE(new files)/DONE. Caps: 10 calls, 20 min.
// Burns nothing but runner minutes. Transcript + patch + metrics are the artifacts.
import fs from "node:fs";
import path from "node:path";
import { execFileSync } from "node:child_process";

const arg = (k, d) => { const i = process.argv.indexOf(k); return i >= 0 ? process.argv[i + 1] : d; };
const WS = arg("--ws", "/tmp/ws");
const TASK = JSON.parse(fs.readFileSync(arg("--task", "cpu/tasks-smoke.jsonl"), "utf8"));
const PROMPT = fs.readFileSync(arg("--prompt", "cpu/prompt-mini.md"), "utf8");
const URL = arg("--url", "http://localhost:8000/v1/chat/completions");
const MAX_CALLS = parseInt(arg("--max-calls", "10"), 10);
const OUT = arg("--out", "results");
const ARM = arg("--arm", "nosidecar-10");
const SCIDX = arg("--sidecar-index", "");
let SC = null;
if (SCIDX) { try { SC = JSON.parse(fs.readFileSync(SCIDX, "utf8")).symbols || []; } catch (e) { SC = "ERR:" + String(e).slice(0, 100); } }
fs.mkdirSync(OUT, { recursive: true });
const log = (o) => fs.appendFileSync(path.join(OUT, "transcript.jsonl"), JSON.stringify(o) + "\n");

function tree(dir, depth, out) {
  if (depth > 2 || out.length > 200) return out;
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    if (e.name === ".git" || e.name === "__pycache__") continue;
    out.push(path.relative(WS, path.join(dir, e.name)) + (e.isDirectory() ? "/" : ""));
    if (e.isDirectory()) tree(path.join(dir, e.name), depth + 1, out);
    if (out.length > 200) break;
  }
  return out;
}
function tool(name, rest) {
  if (name === "READ") {
    const clean = rest.replace(/[\[\]"]/g, "").replace(/start-line=|end-line=/g, "");
    const [p, a, b] = clean.split(/\s+/);
    let lines;
    try { lines = fs.readFileSync(path.join(WS, p), "utf8").split("\n"); }
    catch (e) { return "ERR: no such file: " + (p || "(empty)") + ". Use a path from this repo tree:\n" + tree(WS, 0, []).join("\n").slice(0, 2000); }
    const s = Math.max(0, (parseInt(a || "1", 10) - 1)), e = Math.min(lines.length, parseInt(b || String(s + 150), 10));
    return lines.slice(s, e).map((l, i) => (s + i + 1) + ":" + l).join("\n").slice(0, 10000);
  }
  if (name === "LS") {
    const ents = fs.readdirSync(path.join(WS, rest.trim() || "."), { withFileTypes: true });
    return ents.slice(0, 100).map(e => (e.isDirectory() ? e.name + "/" : e.name)).join("\n");
  }
  if (name === "GREP") {
    const out = [];
    const walk = (d) => {
      for (const e of fs.readdirSync(d, { withFileTypes: true })) {
        if (out.length > 30) return;
        const f = path.join(d, e.name);
        if (e.name === ".git" || e.name === "__pycache__") continue;
        if (e.isDirectory()) { walk(f); continue; }
        if (!/\.(py|md|txt|cfg|toml)$/.test(e.name)) continue;
        const lines = fs.readFileSync(f, "utf8").split("\n");
        lines.forEach((l, i) => { if (out.length <= 30 && l.includes(rest.trim())) out.push(path.relative(WS, f) + ":" + (i + 1) + ":" + l.slice(0, 200)); });
      }
    };
    walk(WS); return out.join("\n") || "(no hits)";
  }
  if (name === "SIDECAR") {
    if (!SCIDX) return "ERR: no sidecar index (nosidecar arm) - use GREP";
    if (typeof SC === "string") return SC;
    const q = rest.trim().toLowerCase();
    if (!q) return "ERR: SIDECAR needs a symbol substring";
    const hits = SC.filter(s => (s.n || "").toLowerCase().includes(q)).slice(0, 20).map(s => s.f + ":" + s.l + " [" + s.k + "] " + s.n);
    return hits.join("\n") || "(no symbols match)";
  }
  if (name === "EDIT") {
    const parts = rest.split(" ||| ");
    if (parts.length !== 3) return "ERR: EDIT needs <path> ||| <old line> ||| <new line>";
    const [p, oldRaw, newRaw] = parts;
    const unq = (s) => (typeof s !== "string" ? s : ((s.length >= 2 && s.startsWith('"') && s.endsWith('"')) ? s.slice(1, -1) : s));
    const oldL = unq(oldRaw), newL = unq(newRaw);
    const f = path.join(WS, p.trim());
    let elines;
    try { elines = fs.readFileSync(f, "utf8").split("\n"); }
    catch (e) { return "ERR: no such file: " + p.trim() + ". Use a path from this repo tree:\n" + tree(WS, 0, []).join("\n").slice(0, 2000); }
    let ehits = elines.reduce((ac, l, i) => (l === oldL ? ac.concat(i) : ac), []);
    let how = "exact";
    if (ehits.length !== 1) { const want = oldL.trim(); ehits = elines.reduce((ac, l, i) => (l.trim() === want ? ac.concat(i) : ac), []); how = "flex"; }
    if (ehits.length !== 1) {
      const toks = oldL.split(/\s+/).map((w) => w.replace(/[^A-Za-z0-9_]/g, "")).filter((w) => w.length >= 4).sort((x, y) => y.length - x.length);
      const tok = toks.length ? toks[0] : "";
      const near = [];
      if (tok) elines.forEach((l, i) => { if (near.length < 3 && l.includes(tok)) near.push((i + 1) + ":" + l.slice(0, 160)); });
      return "ERR: old line matches " + ehits.length + " lines (need exactly 1)" + (near.length ? ". Closest lines with \u0027" + tok + "\u0027:\n" + near.join("\n") : ". No close lines.");
    }
    elines[ehits[0]] = newL;
    fs.writeFileSync(f, elines.join("\n"));
    return "OK edited " + p.trim() + ":" + (ehits[0] + 1) + " (" + how + ")";
  }
  if (name === "EDITLINE") {
    const parts = rest.split(" ||| ");
    if (parts.length !== 3) return "ERR: EDITLINE needs <path> ||| <line number> ||| <new line>";
    const [p, nRaw, newL] = parts;
    const f = path.join(WS, p.trim());
    let lines;
    try { lines = fs.readFileSync(f, "utf8").split("\n"); }
    catch (e) { return "ERR: no such file: " + p.trim() + ". Use a path from this repo tree:\n" + tree(WS, 0, []).join("\n").slice(0, 2000); }
    const n = parseInt(nRaw.trim(), 10);
    if (!(n >= 1 && n <= lines.length)) return "ERR: line number out of range 1.." + lines.length;
    const was = lines[n - 1];
    lines[n - 1] = newL;
    fs.writeFileSync(f, lines.join("\n"));
    return "OK edited " + p.trim() + ":" + n + " (line) was: " + was.slice(0, 160);
  }
  if (name === "WRITE") {
    const sp = rest.indexOf(" ");
    const p = rest.slice(0, sp).trim(), body = rest.slice(sp + 1);
    const f = path.join(WS, p);
    if (fs.existsSync(f)) return "ERR: WRITE is new-files-only";
    fs.writeFileSync(f, body); return "OK wrote " + p;
  }
  return "ERR: unknown tool " + name;
}
async function chat(messages, tries = 5) {
  const t0 = Date.now();
  let last;
  for (let i = 0; i < tries; i++) {
    const r = await fetch(URL, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ messages, temperature: 0.2, max_tokens: 512 }) });
    if (r.ok) { const j = await r.json(); return { text: j.choices[0].message.content, ms: Date.now() - t0 }; }
    last = "model HTTP " + r.status + " " + (await r.text().catch(() => "")).slice(0, 200);
    await new Promise((r2) => setTimeout(r2, 30000));
  }
  throw new Error(last);
}
const problem = "ISSUE (" + TASK.id + " in " + TASK.repo + "):\n" + TASK.problem_statement;
const repoTree = tree(WS, 0, []).join("\n");
const system = PROMPT + "\n\nRepo tree (top 2 levels):\n" + repoTree;
const t0 = Date.now();
let messages = [{ role: "system", content: system }, { role: "user", content: problem }];
let calls = 0, done = null, lastKey = "", navigated = false;
log({ system: system.slice(0, 500), problem: problem.slice(0, 500) });
while (calls < MAX_CALLS && Date.now() - t0 < 20 * 60 * 1000) {
  const { text, ms } = await chat(messages);
  const m = text.match(/^\s*action:\s*([A-Za-z]+)\s*([^\n]*)/im);
  let result, echo;
  if (!m) { calls++; result = "ERR: no ACTION line; reply with ACTION: <tool> <args>"; echo = "ACTION: (none parsed)"; log({ turn: calls, raw: text.slice(0, 2000), action: null }); }
  else {
    const [, rawName, rest] = m;
    const name = rawName.toUpperCase();
    echo = "ACTION: " + name.trim() + " " + (rest || "").trim().slice(0, 300);
    calls++;
    const akey = name.trim() + " " + (rest || "").trim();
    if (akey === lastKey && name.trim() !== "DONE") { result = "ERR: repeated action — same ACTION+args twice in a row is banned, switch tools (READ→GREP→EDIT, never re-read the same range)"; }
    else if (!navigated && ["LS", "SIDECAR", "GREP"].indexOf(name.trim()) < 0) { result = "ERR: first action must navigate (LS, SIDECAR, or GREP) — example paths are placeholders, never use them blind"; }
    else { if (["LS", "SIDECAR", "GREP"].indexOf(name.trim()) >= 0) navigated = true; lastKey = akey; try { result = name === "DONE" ? "DONE" : tool(name.trim(), (rest || "").trim()); } catch (e) { result = "ERR: " + String(e).slice(0, 300); } }
    log({ turn: calls, raw: text.slice(0, 2000), action: name.trim(), ms });
    // batch 6: DONE with an empty working-tree patch is REJECTED (no free exits).
    if (name.trim() === "DONE") {
      let now = "";
      try { now = execFileSync("git", ["-C", WS, "diff", "--", ".:!*.orig"], { encoding: "utf8", maxBuffer: 1 << 20 }); } catch (e) { now = "ERR"; }
      if (!now.trim() || now.startsWith("ERR")) { result = "ERR: DONE rejected. Working tree has no patch (0 chars). Make at least one EDIT that changes repo source, then DONE."; }
      else { done = rest.trim().slice(0, 300); break; }
    }
  }
  log({ turn: calls, result: String(result).slice(0, 2000) });
  // batch 4: never re-feed the full model echo (runaway text amplified context to
  // 4944>4096 and killed two pilots). Send back only the parsed ACTION line, and
  // sliding-window the history under ~20k chars (system + problem always kept).
  messages.push({ role: "assistant", content: echo });
  messages.push({ role: "user", content: "TOOL RESULT:\n" + String(result).slice(0, 3000) + "\nReply with EXACTLY one ACTION line." });
  let histChars = 0;
  for (const mm of messages) histChars += (mm.content || "").length;
  while (messages.length > 4 && histChars > 20000) {
    for (const dd of messages.splice(2, 2)) histChars -= (dd.content || "").length;
  }
}
let diff = "";
try { diff = execFileSync("git", ["-C", WS, "diff", "--", ".:!*.orig"], { encoding: "utf8", maxBuffer: 1 << 20 }); } catch (e) { diff = "ERR git diff: " + String(e).slice(0, 200); }
fs.writeFileSync(path.join(OUT, "agent.patch"), diff);
fs.writeFileSync(path.join(OUT, "metrics.json"), JSON.stringify({ task: TASK.id, arm: ARM, calls, done, wall_s: Math.round((Date.now() - t0) / 1000), patch_chars: diff.length }, null, 1));
console.log("calls=" + calls + " patch_chars=" + diff.length + " done=" + (done || "no-DONE"));
