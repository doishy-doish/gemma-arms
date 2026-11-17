#!/usr/bin/env node
// cpu/spectrum.js — partial-credit gauge (spectrum 0..5 + test pass-rate), stdlib only.
// Reads results/ (transcript.jsonl, metrics.json, ladder.json, ladder-suites.json),
// writes results/spectrum.json. Never throws: on any problem writes {error} instead.
// Milestones (CPU-adapted, documented next to GPU spectrum.js):
//   M1 LOCATED: first grounding action (LS/GREP/SIDECAR/READ) before first edit action.
//   M2 VERIFIED: agent ran a mid-run suite check (midcheck present in transcript).
//   M3 EDITED: patch_chars > 0.
//   M4 FINISHED: DONE accepted or auto-DONE (metrics.done non-null, not aborted).
//   M5 EFFICIENT: calls <= 20 (same bar as GPU scorer; wall excluded — CPU is slower).
// test_rate: graded pass fraction from ladder-suites.json, or null.
// binary: ladder.json L3 (the gate), or null when grading never ran.
import fs from "node:fs";
import path from "node:path";

const arg = (k, d) => { const i = process.argv.indexOf(k); return i >= 0 ? process.argv[i + 1] : d; };
const RES = arg("--res", "results");

function read(p) { try { return fs.readFileSync(p, "utf8"); } catch (e) { return null; } }
const out = { error: null };
try {
  const tRaw = read(path.join(RES, "transcript.jsonl")) || "";
  const turns = tRaw.split("\n").filter(Boolean).map((l) => { try { return JSON.parse(l); } catch (e) { return null; } }).filter(Boolean);
  const GROUND = new Set(["LS", "GREP", "SIDECAR", "READ"]);
  const EDITC = new Set(["EDIT", "EDITLINE", "WRITE"]);
  let firstG = Infinity, firstE = Infinity, mid = false;
  for (const t of turns) {
    if (t.midcheck) mid = true;
    const a = t.action;
    if (typeof a !== "string") continue;
    if (GROUND.has(a) && t.turn < firstG) firstG = t.turn;
    if (EDITC.has(a) && t.turn < firstE) firstE = t.turn;
  }
  const metRaw = read(path.join(RES, "metrics.json"));
  const met = metRaw ? JSON.parse(metRaw) : {};
  const M1 = firstG < firstE ? 1 : 0;
  const M2 = mid ? 1 : 0;
  const M3 = (met.patch_chars || 0) > 0 ? 1 : 0;
  const M4 = met.done ? 1 : 0;
  const M5 = (met.calls || 99) <= 20 ? 1 : 0;
  let testRate = null;
  try {
    const s = JSON.parse(read(path.join(RES, "ladder-suites.json")) || "null");
    const g = s && s.graded;
    if (g && g.collected > 0) testRate = (g.collected - g.failed - g.errors) / g.collected;
  } catch (e) { /* stays null */ }
  let binary = null;
  try {
    const l = JSON.parse(read(path.join(RES, "ladder.json")) || "null");
    if (l && typeof l.L3 === "boolean") binary = l.L3;
  } catch (e) { /* stays null */ }
  Object.assign(out, {
    task: met.task || null, arm: met.arm || null,
    resolved_binary: binary, spectrum: M1 + M2 + M3 + M4 + M5,
    M1, M2, M3, M4, M5, test_rate: testRate,
    tool_calls: met.calls ?? null, patch_chars: met.patch_chars ?? null,
  });
} catch (e) { out.error = String(e).slice(0, 200); }
fs.mkdirSync(RES, { recursive: true });
fs.writeFileSync(path.join(RES, "spectrum.json"), JSON.stringify(out, null, 1));
console.log("spectrum=" + (out.spectrum !== undefined ? out.spectrum : "ERR") + " binary=" + out.resolved_binary + " test_rate=" + out.test_rate);
