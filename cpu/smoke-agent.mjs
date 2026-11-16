#!/usr/bin/env node
// cpu/smoke-agent.mjs — stdlib-only CPU agent loop (node 20). No deps, no secrets.
// Tools: LS/GREP/READ/SIDECAR/EDIT/EDITLINE(single-line)/WRITE(new files)/DONE.
// Batch-9 (registry: gAbort+gShape+gSchema+gFinish+gPre, F21/D17, F20, P12/P14/P15/P17, E13):
//  - T1-forcing REMOVED (F20 prune: 30/30 rejects, zero compliance — shapes replace forcing).
//  - multi-action parse: all ACTION lines scanned; prompt-example duplicates, lastSig
//    repeats and non-tree paths skipped; first survivor executes (fallback: first line).
//  - signature-level repeat ban (Mingbird-M4 flavor): READ=path, GREP/SIDECAR=normalized
//    query, EDIT/EDITLINE=path+normalized-old; file change resets (re-read allowed once).
//  - git add -N on WRITE (F19 fix: WRITE visible to L1, no perverse gradient).
//  - echo-masking on ERR (P12/P14: failed-action text never re-fed; repeat 0.06->0.54).
//  - no-progress abort k=3 (F21: 14/14 dead runs caught t2-5, 0/10 winners killed).
//  - changes-critic pre-DONE (P14) + finish gate (P17: summary must name touched file)
//    + post-green cap +2 calls (P15; submit-anything-that-applies).
//  - pre-execution routing (EffGen flavor): repo-size route logged, one line, no model call.
//  - structured spec-feeding (P16/BRA): KEY LINES shaped from issue, never echoed raw.
import fs from "node:fs";
import path from "node:path";
import { execFileSync } from "node:child_process";

const arg = (k, d) => { const i = process.argv.indexOf(k); return i >= 0 ? process.argv[i + 1] : d; };
const WS = arg("--ws", "/tmp/ws");
const TASK = JSON.parse(fs.readFileSync(arg("--task", "cpu/tasks-smoke.jsonl"), "utf8"));
const PROMPT = fs.readFileSync(arg("--prompt", "cpu/prompt-mini.md"), "utf8");
const URL = arg("--url", "http://localhost:8000/v1/chat/completions");
const MAX_CALLS = parseInt(arg("--max-calls", "10"), 10);
const TEST_FILES = arg("--test-files", "").split(/\s+/).filter(Boolean);
const OUT = arg("--out", "results");
const ARM = arg("--arm", "nosidecar-10");
const SCIDX = arg("--sidecar-index", "");
let SC = null;
if (SCIDX) { try { SC = JSON.parse(fs.readFileSync(SCIDX, "utf8")).symbols || []; } catch (e) { SC = "ERR:" + String(e).slice(0, 100); } }
fs.mkdirSync(OUT, { recursive: true });
const log = (o) => fs.appendFileSync(path.join(OUT, "transcript.jsonl"), JSON.stringify(o) + "\n");

// ---- repo tree (also the placeholder detector's ground truth) ----
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
const TREE = tree(WS, 0, []);
const TOP = new Set(TREE.map(p => p.split("/")[0].toLowerCase()));
function pathInTree(p) {
  const first = (p || "").split("/")[0].toLowerCase();
  return TOP.has(first);
}
// prompt example ACTION lines (exact strings) — burst copies of these are skipped, not executed
const EXAMPLES = new Set(
  PROMPT.split("\n").map(l => l.trim()).filter(l => /^ACTION:\s*\w+/i.test(l))
);

// ---- tools (unchanged semantics except WRITE add -N) ----
function tool(name, rest) {
  if (name === "READ") {
    const clean = rest.replace(/[\[\]"]/g, "").replace(/start-line=|end-line=/g, "");
    const [p, a, b] = clean.split(/\s+/);
    let lines;
    try { lines = fs.readFileSync(path.join(WS, p), "utf8").split("\n"); }
    catch (e) { return "ERR: no such file: " + (p || "(empty)") + ". Use a path from this repo tree:\n" + TREE.join("\n").slice(0, 2000); }
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
    catch (e) { return "ERR: no such file: " + p.trim() + ". Use a path from this repo tree:\n" + TREE.join("\n").slice(0, 2000); }
    let ehits = elines.reduce((ac, l, i) => (l === oldL ? ac.concat(i) : ac), []);
    let how = "exact";
    if (ehits.length !== 1) { const want = oldL.trim(); ehits = elines.reduce((ac, l, i) => (l.trim() === want ? ac.concat(i) : ac), []); how = "flex"; }
    if (ehits.length !== 1) {
      const toks = oldL.split(/\s+/).map((w) => w.replace(/[^A-Za-z0-9_]/g, "")).filter((w) => w.length >= 4).sort((x, y) => y.length - x.length);
      const tok = toks.length ? toks[0] : "";
      const near = [];
      if (tok) elines.forEach((l, i) => { if (near.length < 3 && l.includes(tok)) near.push((i + 1) + ":" + l.slice(0, 160)); });
      return "ERR: old line matches " + ehits.length + " lines (need exactly 1)" + (near.length ? ". Closest lines with '" + tok + "':\n" + near.join("\n") : ". No close lines.");
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
    catch (e) { return "ERR: no such file: " + p.trim() + ". Use a path from this repo tree:\n" + TREE.join("\n").slice(0, 2000); }
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
    fs.writeFileSync(f, body);
    try { execFileSync("git", ["-C", WS, "add", "-N", p.trim()], { encoding: "utf8" }); } catch (e) { /* best-effort */ }
    return "OK wrote " + p;
  }
  return "ERR: unknown tool " + name;
}

// ---- batch-9 deterministic machinery ----
// signature-level repeat ban: same shape twice in a row is banned even with varied args
function sigOf(name, rest) {
  const norm = (s) => (s || "").toLowerCase().replace(/[^a-z0-9_]+/g, "");
  if (name === "READ") return "READ " + (rest.split(/\s+/)[0] || "").toLowerCase();
  if (name === "LS") return "LS " + (rest.trim() || ".").toLowerCase();
  if (name === "GREP" || name === "SIDECAR") return name + " " + norm(rest);
  if (name === "EDIT") { const ps = rest.split(" ||| "); return "EDIT " + (ps[0] || "").trim().toLowerCase() + " :: " + norm(ps[1] || ""); }
  if (name === "EDITLINE") { const ps = rest.split(" ||| "); return "EDITLINE " + (ps[0] || "").trim().toLowerCase() + " :: " + (ps[1] || "").trim(); }
  if (name === "WRITE") return "WRITE " + (rest.split(/\s+/)[0] || "").toLowerCase();
  return name + " " + rest.trim();
}
const EDIT_CLASS = new Set(["EDIT", "EDITLINE", "WRITE"]);
const GROUND_CLASS = new Set(["LS", "SIDECAR", "GREP", "READ"]);
function pathArg(name, rest) {
  if (name === "READ" || name === "LS" || name === "WRITE") return (rest.split(/\s+/)[0] || "").trim();
  if (name === "EDIT" || name === "EDITLINE") return ((rest.split(" ||| ")[0]) || "").trim();
  return "";
}
function gitDiff() { try { return execFileSync("git", ["-C", WS, "diff", "--", ".:!*.orig"], { encoding: "utf8", maxBuffer: 1 << 20 }); } catch (e) { return "ERR"; } }
function diffFiles() {
  try {
    const s = execFileSync("git", ["-C", WS, "diff", "--name-status", "--", ".:!*.orig"], { encoding: "utf8" });
    return s.split("\n").filter(Boolean).map(l => { const [st, ...rp] = l.split("\t"); return { st: (st || "").trim(), p: rp.join("\t") }; });
  } catch (e) { return []; }
}
// changes-critic (P14) + finish gate (P17): deterministic pre-DONE review
function critic(summary) {
  const d = gitDiff();
  if (!d.trim() || d.startsWith("ERR")) return "ERR: DONE rejected. Working tree has no patch (0 chars). Make at least one EDIT that changes repo source, then DONE.";
  const files = diffFiles();
  const bad = files.filter(f => /(^|\/)tests?\//.test(f.p) || /(^|\/)(test_.*|conftest\.py)$/.test(f.p) || /\.(cfg|toml|ini|yaml|yml)$/.test(f.p) || f.p === "setup.py");
  if (bad.length) return "ERR: DONE rejected. Patch touches test/config paths (" + bad.map(f => f.p).join(", ") + "). EDIT repo source only, then DONE.";
  if (files.length && files.every(f => f.st === "A")) return "ERR: DONE rejected. Patch adds files but modifies no existing source. EDIT the buggy file, then DONE.";
  const names = files.map(f => (f.p.split("/").pop() || "").toLowerCase()).filter(Boolean);
  const s = (summary || "").toLowerCase();
  if (!names.some(n => n && s.includes(n))) return "ERR: DONE rejected. Summary must name a file your patch touches (" + names.slice(0, 5).join(", ") + "). Re-read your diff, then DONE.";
  return null;
}
// KEY LINES: structured spec-feeding (P16/BRA) — shaped signal, never raw echo
function keyLines(problem) {
  const out = [];
  for (const l of String(problem || "").split("\n")) {
    if (out.length >= 12) break;
    const t = l.trim();
    if (t.length < 4 || t.length > 220) continue;
    if (/error|assert|expected|raise|traceback|denied|fail|def |class |return|import /i.test(t)) out.push(t.slice(0, 160));
  }
  return out;
}
// pre-execution routing (EffGen flavor): one deterministic line, no model call
const ROUTE = TREE.length < 60
  ? "small-repo: open with GREP or SIDECAR on issue symbols, LS only if lost"
  : "standard: open with LS or GREP, then READ +-40 around hits";
function midGreen() {
  if (!TEST_FILES.length) return "unknown";
  try {
    const o = execFileSync("python", ["-m", "pytest", ...TEST_FILES, "-q", "--tb=no", "-W", "ignore::DeprecationWarning"], { cwd: WS, encoding: "utf8", timeout: 240000, maxBuffer: 1 << 20 });
    const tail = o.split("\n").filter(Boolean).slice(-3).join(" ");
    if (/failed|error/i.test(tail)) return "red";
    return /passed/.test(tail) ? "green" : "unknown";
  } catch (e) { return "unknown"; }
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

const KL = keyLines(TASK.problem_statement);
const problem = "ISSUE (" + TASK.id + " in " + TASK.repo + "):\n" + TASK.problem_statement +
  (KL.length ? "\nKEY LINES (shaped spec — GREP these symbols):\n" + KL.join("\n") : "");
const system = PROMPT + "\nROUTER: " + ROUTE + ".\n\nRepo tree (top 2 levels):\n" + TREE.join("\n");
const t0 = Date.now();
let messages = [{ role: "system", content: system }, { role: "user", content: problem }];
let calls = 0, done = null;
let lastSig = "", seenSigs = new Set(), streak = 0, aborted = false;
let greenAt = 0, greenCheckedPatch = -1;
let criticRejects = 0, maskedErrs = 0, skippedBurst = 0, sigRepeats = 0;
log({ system: system.slice(0, 500), problem: problem.slice(0, 500), route: ROUTE });
while (calls < MAX_CALLS && Date.now() - t0 < 20 * 60 * 1000) {
  const { text, ms } = await chat(messages);
  // multi-action parse (F20): scan ALL action lines; skip example-copies, repeats, non-tree paths
  const acts = [...text.matchAll(/^\s*action:\s*([A-Za-z]+)\s*([^\n]*)/gim)].map(m => ({ name: m[1].toUpperCase().trim(), rest: (m[2] || "").trim(), line: m[0].trim() }));
  let result, echo, acted = null, progress = false;
  if (!acts.length) {
    calls++; result = "ERR: no ACTION line; reply with ACTION: <tool> <args>"; echo = "ACTION: (none parsed)";
    log({ turn: calls, raw: text.slice(0, 2000), action: null, progress: false, streak: streak + 1 });
    streak++;
    if (streak >= 3) { aborted = true; log({ turn: calls, result: String(result).slice(0, 2000), abort: "mute streak=3, run capped (F21)" }); break; }
  } else {
    let pick = null; const skipped = [];
    for (const a of acts) {
      if (EXAMPLES.has(a.line)) { skipped.push("example-copy:" + a.line.slice(0, 60)); continue; }
      const s = sigOf(a.name, a.rest);
      if (a.name !== "DONE" && s === lastSig) { skipped.push("repeat:" + s.slice(0, 60)); continue; }
      const pa = pathArg(a.name, a.rest);
      if (pa && !pathInTree(pa)) { skipped.push("non-tree:" + pa.slice(0, 60)); continue; }
      pick = a; break;
    }
    if (!pick) pick = acts[0];
    skippedBurst += skipped.length;
    const { name, rest } = pick;
    echo = "ACTION: " + name + " " + rest.slice(0, 300);
    calls++;
    const sig = sigOf(name, rest);
    if (name === "DONE") {
      log({ turn: calls, raw: text.slice(0, 2000), action: "DONE", skipped });
      const rej = critic(rest);
      if (rej) { result = rej; criticRejects++; }
      else { done = rest.slice(0, 300); log({ turn: calls, result: "DONE accepted" }); break; }
    } else if (sig === lastSig) {
      sigRepeats++;
      result = "ERR: repeated action shape — same " + name + " shape twice in a row is banned, switch tools (READ once, then GREP or EDIT).";
    } else {
      lastSig = sig;
      if (EDIT_CLASS.has(name)) { try { result = tool(name, rest); } catch (e) { result = "ERR: " + String(e).slice(0, 300); } lastSig = ""; progress = true; }
      else if (GROUND_CLASS.has(name)) { try { result = tool(name, rest); } catch (e) { result = "ERR: " + String(e).slice(0, 300); } if (!seenSigs.has(sig)) { seenSigs.add(sig); progress = true; } }
      else { try { result = tool(name, rest); } catch (e) { result = "ERR: " + String(e).slice(0, 300); } }
      acted = name;
      log({ turn: calls, raw: text.slice(0, 2000), action: name, sig: sig.slice(0, 80), progress, streak, skipped });
    }
    // no-progress abort k=3 (F21/D17): deterministic, executor untouched otherwise
    if (!progress && name !== "DONE") streak++; else if (name !== "DONE") streak = 0;
    if (streak >= 3 && !done) {
      aborted = true;
      log({ turn: calls, result: String(result).slice(0, 2000), abort: "no-progress streak=3, run capped (F21)" });
      break;
    }
  }
  // echo-masking on ERR (P12/P14): failed-action text never re-fed
  const isErr = String(result).startsWith("ERR");
  if (isErr) maskedErrs++;
  messages.push({ role: "assistant", content: isErr ? "ACTION failed (masked). Switch tools, never repeat." : echo });
  messages.push({ role: "user", content: "TOOL RESULT:\n" + String(result).slice(0, 3000) + "\nReply with EXACTLY one ACTION line." });
  let histChars = 0;
  for (const mm of messages) histChars += (mm.content || "").length;
  while (messages.length > 4 && histChars > 20000) {
    for (const dd of messages.splice(2, 2)) histChars -= (dd.content || "").length;
  }
  // post-green cap (P15): first non-empty patch + suite green -> +2 calls then auto-DONE
  if (!greenAt && acted && EDIT_CLASS.has(acted) && String(result).startsWith("OK")) {
    const now = gitDiff();
    if (now.trim() && !now.startsWith("ERR") && now.length !== greenCheckedPatch) {
      greenCheckedPatch = now.length;
      const g = midGreen();
      log({ turn: calls, midcheck: g, patch_chars: now.length });
      if (g === "green") { greenAt = calls; }
    }
  }
  if (greenAt && calls >= greenAt + 2 && !done) {
    const files = diffFiles().map(f => f.p.split("/").pop());
    done = "auto: post-green cap (+2), touches " + files.slice(0, 3).join(", ");
    log({ turn: calls, result: "post-green cap fired, auto-DONE" });
    break;
  }
}
let diff = gitDiff();
fs.writeFileSync(path.join(OUT, "agent.patch"), diff.startsWith("ERR") ? "" : diff);
fs.writeFileSync(path.join(OUT, "metrics.json"), JSON.stringify({ task: TASK.id, arm: ARM, calls, done, wall_s: Math.round((Date.now() - t0) / 1000), patch_chars: (diff.startsWith("ERR") ? 0 : diff.length), abort: aborted, green_at: greenAt, critic_rejects: criticRejects, masked_errs: maskedErrs, skipped_burst: skippedBurst, sig_repeats: sigRepeats, route: ROUTE }, null, 1));
console.log("calls=" + calls + " patch_chars=" + (diff.startsWith("ERR") ? 0 : diff.length) + " done=" + (done || (aborted ? "ABORTED" : "no-DONE")));
