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
import http from "node:http";
import https from "node:https";
// 14B-CPU: llama.cpp prefill+generate can exceed undici's 300s headers timeout;
// raw http.request has no default headers timeout, so use it with an explicit 55-min cap.
function postJSON(url, payload, timeoutMs = 3300000) {
  return new Promise((resolve, reject) => {
    const u = new globalThis.URL(url);
    const lib = u.protocol === "https:" ? https : http;
    const data = JSON.stringify(payload);
    const req = lib.request({ hostname: u.hostname, port: u.port, path: u.pathname + u.search, method: "POST", headers: { "Content-Type": "application/json", "Content-Length": Buffer.byteLength(data) } }, (res) => {
      let body = "";
      res.on("data", (c) => { body += c; });
      res.on("end", () => resolve({ ok: res.statusCode >= 200 && res.statusCode < 300, status: res.statusCode, json: async () => JSON.parse(body) }));
    });
    req.on("error", reject);
    req.setTimeout(timeoutMs, () => req.destroy(new Error("postJSON timeout " + timeoutMs)));
    req.write(data);
    req.end();
  });
}

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
// ---- qsubmit arm (verbatim QSTACK submission prompt over rail-31B): JSON tool-call protocol ----
const QSUB = ARM.startsWith("qsubmit");
const QSUB_TOOLS = new Set(["run_command","read_file","write_file","edit_file","get_status","submit_patch"]);
function qsubExtract(text) {
  const cands = [];
  const fence = [...text.matchAll(/```(?:json)?\s*([\s\S]*?)```/gi)].map(m=>m[1]);
  for (const src of [text, ...fence]) {
    for (let i=0;i<src.length;i++) {
      if (src[i] !== '{') continue;
      let d=0, instr=false, esc=false;
      for (let j=i;j<src.length && j<i+4000;j++) {
        const c=src[j];
        if (instr) { if (esc) esc=false; else if (c==='\\') esc=true; else if (c==='"') instr=false; }
        else { if (c==='"') instr=true; else if (c==='{') d++; else if (c==='}') { d--; if(!d){ cands.push(src.slice(i,j+1)); i=j; break; } } }
      }
    }
  }
  for (const c of cands) {
    let o; try { o = JSON.parse(c); } catch(e){ continue; }
    if (!o || typeof o!=='object') continue;
    const nm = String(o.tool||o.function_name||o.name||'').toLowerCase();
    if (!QSUB_TOOLS.has(nm)) continue;
    let args = o.arguments||o.args||o.params||o.parameters||null;
    if (!args) { args = {...o}; delete args.tool; delete args.function_name; delete args.name; }
    return { name: nm, args: args||{} };
  }
  return null;
}
function qsubRun(name, a) {
  a = a||{};
  const rel = (p) => String(p||'').trim().replace(/^\.\//,'').replace(/^\/workspace\//,'');
  if (name==='run_command') {
    const cmd = String(a.command||'');
    if (!cmd) return 'ERR: run_command needs a command string';
    try {
      const o = execFileSync('bash',['-c',cmd],{cwd:WS,encoding:'utf8',timeout:110000,maxBuffer:1<<20});
      return 'exit=0\n'+String(o).slice(-3000);
    } catch(e) {
      return 'exit='+((e.status??'?'))+'\n'+String((e.stdout||'')+''+(e.stderr||'')).slice(-3000);
    }
  }
  if (name==='read_file') {
    const p = rel(a.filepath||a.path); if(!p) return 'ERR: read_file needs filepath';
    if (!pathInTree(p)) return 'ERR: path outside repo tree: '+p;
    let lines; try { lines = fs.readFileSync(path.join(WS,p),'utf8').split('\n'); } catch(e){ return 'ERR: no such file: '+p; }
    const s = Math.max(1, parseInt(a.start_line||a.start||'1',10)||1);
    const e = Math.min(lines.length, parseInt(a.end_line||a.end||String(s+120),10)||(s+120));
    if (!(s<=e)) return 'ERR: bad line range';
    return 'OK '+p+' lines '+s+'-'+e+'/'+lines.length+'\n'+lines.slice(s-1,e).map((l,i)=>'  '+(s+i)+': '+l).join('\n').slice(0,3000);
  }
  if (name==='write_file') {
    const p = rel(a.filepath||a.path); if(!p) return 'ERR: write_file needs filepath';
    if (!pathInTree(p)) return 'ERR: path outside repo tree: '+p;
    fs.writeFileSync(path.join(WS,p), String(a.content??''));
    try { execFileSync('git',['-C',WS,'add','-N',p],{encoding:'utf8'}); } catch(e){}
    return 'OK wrote '+p+' ('+String(a.content??'').length+' chars)';
  }
  if (name==='edit_file') {
    const p = rel(a.filepath||a.path); if(!p) return 'ERR: edit_file needs filepath';
    if (!pathInTree(p)) return 'ERR: path outside repo tree: '+p;
    let src; try { src = fs.readFileSync(path.join(WS,p),'utf8'); } catch(e){ return 'ERR: no such file: '+p; }
    const oldS = String(a.old_string??a.oldString??''), newS = String(a.new_string??a.newString??'');
    if (!oldS) return 'ERR: edit_file needs old_string';
    const ix = src.indexOf(oldS);
    if (ix<0) return 'ERR: old_string matches 0 occurrences in '+p+' (exact match required)';
    fs.writeFileSync(path.join(WS,p), src.slice(0,ix)+newS+src.slice(ix+oldS.length));
    return 'OK edited '+p+' (first of '+(src.split(oldS).length-1)+' occurrence(s) replaced)';
  }
  if (name==='get_status') {
    try {
      const st = execFileSync('git',['-C',WS,'status','--porcelain=v1'],{encoding:'utf8'});
      const df = execFileSync('git',['-C',WS,'diff','--stat','--','.:!*.orig'],{encoding:'utf8'});
      return 'OK status:\n'+String(st).slice(0,1500)+'\ndiffstat:\n'+String(df).slice(0,1500);
    } catch(e){ return 'ERR: git failed'; }
  }
  return 'ERR: unknown tool '+name;
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
    const r = await postJSON(URL, { messages, temperature: 0.2, top_p: 0.95, max_tokens: 512 });
    if (r.ok) { const j = await r.json(); return { text: j.choices[0].message.content, ms: Date.now() - t0 }; }
    last = "model HTTP " + r.status + " " + (await r.text().catch(() => "")).slice(0, 200);
    await new Promise((r2) => setTimeout(r2, 30000));
  }
  throw new Error(last);
}

const KL = keyLines(TASK.problem_statement);
// batch-9 amend-3 priming (P16/P17): blank page + example block = copy-loop.
// Harness executes ONE real grounding observation pre-T1 (zero model calls);
// the model replies to real repo content, not to the examples.
function topSymbol(problem) {
  const kw = new Set(["import", "from", "def", "class", "return", "raise", "assert", "for", "while", "with", "none", "true", "false", "null", "self", "issue", "error", "expected", "actual", "should", "when", "that", "this", "test", "tests"]);
  const toks = String(problem || "").split(/[^A-Za-z0-9_]+/).filter(t => t.length >= 4 && !kw.has(t.toLowerCase()));
  return toks.find(t => /_/.test(t) || /[a-z][A-Z]/.test(t)) || toks[0] || "";
}
const PRIME_SYM = topSymbol(TASK.problem_statement);
let PRIME_RES = "";
try { PRIME_RES = tool(SCIDX ? "SIDECAR" : "GREP", PRIME_SYM || "def").slice(0, 1500); }
catch (e) { PRIME_RES = "ERR: " + String(e).slice(0, 120); }
// batch-10 grounding enforcement (sweep-4 Agentless flavor: localize-then-repair,
// harness-enforced): EDIT/EDITLINE may only touch OBSERVED files (seen via READ/LS/
// GREP/SIDECAR hits or priming). Unobserved target -> redirect ERR naming observed
// files. Calls 1-3 are localize-only (edit window opens call 4, per E13 4-6).
const observed = new Set();
function noteObserved(name, rest, result) {
  if (!result || result.startsWith("ERR") || result === "(no hits)" || result === "(no symbols match)") return;
  if (name === "READ") { observed.add(pathArg(name, rest).toLowerCase()); }
  else if (name === "LS") {
    const d = (rest.trim() || ".").replace(/\/$/, "");
    for (const l of String(result).split("\n").slice(0, 100)) {
      const e = l.trim(); if (!e || e.endsWith("/")) continue;
      observed.add((d === "." ? e : d + "/" + e).toLowerCase());
    }
  } else if (name === "GREP") {
    for (const l of String(result).split("\n").slice(0, 30)) {
      const p = l.split(":")[0]; if (p && p.includes(".")) observed.add(p.trim().toLowerCase());
    }
  } else if (name === "SIDECAR") {
    for (const l of String(result).split("\n").slice(0, 20)) {
      const p = l.split(":")[0]; if (p && p.includes("/")) observed.add(p.trim().toLowerCase());
    }
  }
}
noteObserved(SCIDX ? "SIDECAR" : "GREP", PRIME_SYM || "def", PRIME_RES);
const problem = "ISSUE (" + TASK.id + " in " + TASK.repo + "):\n" + TASK.problem_statement +
  (KL.length ? "\nKEY LINES (shaped spec — GREP these symbols):\n" + KL.join("\n") : "") +
  "\nPRIMED OBSERVATION (real repo content — act on this, not the examples):\n" + (PRIME_RES || "(no hits — LS the tree)");
const system = PROMPT + "\nROUTER: " + ROUTE + ".\n\nRepo tree (top 2 levels):\n" + TREE.join("\n");
const t0 = Date.now();
let messages = [{ role: "system", content: system }, { role: "user", content: problem }];
let calls = 0, done = null;
let lastSig = "", seenSigs = new Set(), streak = 0, aborted = false;
let greenAt = 0, greenCheckedPatch = -1;
let criticRejects = 0, maskedErrs = 0, skippedBurst = 0, sigRepeats = 0, gatedRejects = 0;
log({ system: system.slice(0, 500), problem: problem.slice(0, 500), route: ROUTE, primed: PRIME_SYM });
while (calls < MAX_CALLS && Date.now() - t0 < (QSUB ? 100 : 20) * 60 * 1000) {
  const { text, ms } = await chat(messages);
  // multi-action parse (F20): scan ALL action lines; skip example-copies, repeats, non-tree paths
  const acts = [...text.matchAll(/^\s*action:\s*([A-Za-z]+)\s*([^\n]*)/gim)].map(m => ({ name: m[1].toUpperCase().trim(), rest: (m[2] || "").trim(), line: m[0].trim() }));
  let result, echo, acted = null, progress = false;
  if (QSUB) {
    // thin mode: verbatim submission prompt, JSON tool protocol, no behavioral gates
    // (S2 forbids early-stop; edit-window/grounding/repeat rules are prompt-managed)
    const tc = qsubExtract(text);
    calls++;
    if (!tc) {
      result = "ERR: no tool call parsed; reply with ONE JSON tool call (run_command/read_file/write_file/edit_file/get_status/submit_patch).";
      echo = "(none parsed)";
      log({ turn: calls, raw: text.slice(0, 2000), action: null, progress: false, streak: streak + 1 });
      streak++;
      if (streak >= 8) { aborted = true; log({ turn: calls, result: String(result).slice(0,2000), abort: "qsubmit mute streak=8" }); break; }
    } else if (tc.name === "submit_patch") {
      log({ turn: calls, raw: text.slice(0, 2000), action: "DONE", skipped: [] });
      const rej = critic("submit_patch " + diffFiles().map(x=>x.p).join(" "));
      if (rej) { result = rej; criticRejects++; }
      else { done = "submit_patch accepted"; log({ turn: calls, result: "DONE accepted" }); break; }
    } else {
      streak = 0;
      try { result = qsubRun(tc.name, tc.args); } catch (e) { result = "ERR: " + String(e).slice(0, 300); }
      if (String(result).startsWith("ERR")) maskedErrs++;
      acted = tc.name; progress = !String(result).startsWith("ERR");
      log({ turn: calls, raw: text.slice(0, 2000), action: tc.name, progress, streak, skipped: [] });
    }
  } else {
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
    if (!pick) pick = { name: "__FILTERED__", rest: "", line: "" };
    skippedBurst += skipped.length;
    const { name, rest } = pick;
    echo = "ACTION: " + name + " " + rest.slice(0, 300);
    calls++;
    const sig = sigOf(name, rest);
    if (name === "__FILTERED__") {
      // fallback hole closed (floor32 pilot-2 lesson): never execute a known
      // example-copy / repeat / non-tree line. Redirect with ERR instead.
      result = "ERR: every ACTION line was a format example, a repeat, or a path outside the repo tree. Use REAL paths from the tree above and REAL symbols from KEY LINES. Reply with EXACTLY one ACTION line.";
    } else if (name === "DONE") {
      log({ turn: calls, raw: text.slice(0, 2000), action: "DONE", skipped });
      const rej = critic(rest);
      if (rej) { result = rej; criticRejects++; }
      else { done = rest.slice(0, 300); log({ turn: calls, result: "DONE accepted" }); break; }
    } else if (sig === lastSig) {
      sigRepeats++;
      result = "ERR: repeated action shape — same " + name + " shape twice in a row is banned, switch tools (READ once, then GREP or EDIT).";
    } else if ((name === "EDIT" || name === "EDITLINE") && calls <= 3) {
      gatedRejects++;
      result = "ERR: localize first — calls 1-3 are LS/GREP/SIDECAR/READ only (edit window opens call 4). Ground the bug location first.";
    } else if ((name === "EDIT" || name === "EDITLINE") && !observed.has(pathArg(name, rest).toLowerCase())) {
      gatedRejects++;
      const seen = [...observed].slice(0, 5);
      result = "ERR: grounding gate — " + (pathArg(name, rest) || "(no path)") + " is not a file you have looked at. " + (seen.length ? "You HAVE seen: " + seen.join(", ") + ". READ one first (READ <file> 1 40), then EDIT it." : "LS the tree or GREP a symbol first.") + " Example paths (acme/...) are never real.";
    } else {
      lastSig = sig;
      if (EDIT_CLASS.has(name)) { try { result = tool(name, rest); } catch (e) { result = "ERR: " + String(e).slice(0, 300); } lastSig = ""; progress = true; }
      else if (GROUND_CLASS.has(name)) { try { result = tool(name, rest); } catch (e) { result = "ERR: " + String(e).slice(0, 300); } if (!seenSigs.has(sig)) { seenSigs.add(sig); progress = true; } }
      else { try { result = tool(name, rest); } catch (e) { result = "ERR: " + String(e).slice(0, 300); } }
      acted = name;
      noteObserved(name, rest, result);
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
  } // close non-QSUB else
  // echo-masking on ERR (P12/P14): failed-action text never re-fed
  const isErr = String(result).startsWith("ERR");
  if (isErr) maskedErrs++;
  messages.push({ role: "assistant", content: QSUB ? (isErr ? "Tool call failed (masked). Send a different tool call, never repeat the same one." : echo) : (isErr ? "ACTION failed (masked). Switch tools, never repeat." : echo) });
  messages.push({ role: "user", content: QSUB ? ("TOOL RESULT:\n" + String(result).slice(0, 3000) + "\nReply with your next single tool call (first valid call per turn executes; extras ignored).") : ("TOOL RESULT:\n" + String(result).slice(0, 3000) + "\nReply with EXACTLY one ACTION line.") });
  let histChars = 0;
  for (const mm of messages) histChars += (mm.content || "").length;
  while (messages.length > 4 && histChars > 20000) {
    for (const dd of messages.splice(2, 2)) histChars -= (dd.content || "").length;
  }
  if (!QSUB) {
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
  } // close post-green !QSUB gate
}
let diff = gitDiff();
fs.writeFileSync(path.join(OUT, "agent.patch"), diff.startsWith("ERR") ? "" : diff);
fs.writeFileSync(path.join(OUT, "metrics.json"), JSON.stringify({ task: TASK.id, arm: ARM, calls, done, wall_s: Math.round((Date.now() - t0) / 1000), patch_chars: (diff.startsWith("ERR") ? 0 : diff.length), abort: aborted, green_at: greenAt, critic_rejects: criticRejects, masked_errs: maskedErrs, skipped_burst: skippedBurst, sig_repeats: sigRepeats, gated_rejects: gatedRejects, route: ROUTE, primed: PRIME_SYM, observed_n: observed.size }, null, 1));
console.log("calls=" + calls + " patch_chars=" + (diff.startsWith("ERR") ? 0 : diff.length) + " done=" + (done || (aborted ? "ABORTED" : "no-DONE")));
