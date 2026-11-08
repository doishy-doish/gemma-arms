// fire_audit.js — durable pre-fire auditor for GEMMA ARM fire notebooks.
// Encodes EVERY past failure mode (H1 v1..v6, ARM2 v1..v3) as a check against
// the FIRED artifact (the notebook JSON actually pushed), never just sources.
// Runs anywhere: pure logic, no imports. In execute_js:
//   const code = await fs.readTextFile('scratch/gemma/tools/fire_audit.js');
//   const audit = new Function(code + '\nreturn auditFireNotebook;')();
//   return audit(await fs.readTextFile('scratch/gemma/fire-arm2-v3.ipynb'));
// Returns {pass, failures:[], checks:[{id, ok, detail}]} — fail loud on parse.
function auditFireNotebook(nbText, opts) {
  opts = opts || {};
  const checks = [];
  const ok = (id, cond, detail) => checks.push({ id, ok: !!cond, detail: detail || '' });
  let nb;
  try { nb = JSON.parse(nbText); }
  catch (e) { return { pass: false, failures: ['parse'], checks: [{ id: 'parse', ok: false, detail: String(e) }] }; }
  const cells = nb.cells.map(c => Array.isArray(c.source) ? c.source.join('') : String(c.source || ''));
  const all = cells.join('\n---CELL---\n');

  // A0. shape
  ok('cells-11', nb.cells.length === 11, 'got ' + nb.cells.length);

  // A1. H1 v1 class: import header (load_tasks + decoding support).
  // NOTE: imports may be comma-joined (`import re, hashlib, json, base64`),
  // so match tokens, not exact `import X` lines.
  ok('import-load_tasks', /from\s+swegemma\.models\s+import\s+[^\n]*load_tasks/.test(all), 'swegemma load_tasks');
  ok('import-base64', /\bbase64\b/.test(all) && /import[^\n]*\bbase64\b/.test(all), 'base64 imported');
  ok('uses-load_tasks', /load_tasks\s*\(\s*TASKS_PATH\s*\)/.test(all), 'MAIN tasks built via load_tasks');

  // A2. H1 v1: model swap + adapter strip on EVERY declared yaml + post-check.
  ok('swap-loop', /MODEL_NAME\s*=\s*'gemma-4-e4b-it-qat-w4a16-ct'/.test(all) && /model:\\s*/.test(all), 'E4B swap loop');
  ok('adapter-strip', /shutil\.rmtree\(AGENT_DIR\s*\/\s*'adapters'/.test(all), 'adapters/ stripped');
  ok('swap-postcheck', /model swap clean/.test(all) && /leftover/.test(all), 'post-swap grep assert');

  // A3. H1 v2: no backup/temp files inside submission dir (validator rejects).
  ok('backup-outside', /agent\.yaml\.pre-fc\.bak/.test(all) && /WORKING_DIR\s*\/\s*'agent\.yaml\.pre-fc\.bak'/.test(all), 'backup outside submission');
  ok('purge-gate', /\.orig/.test(all) && /leftovers/.test(all), 'orig/bak purge + assert');
  ok('no-orig-inside', !/AGENT_DIR\s*\/\s*'agent\.yaml\.orig'/.test(all), 'no .orig written into submission');

  // A4. H1 v3: skill mechanism does not exist in this harness.
  ok('skills-removed', /shutil\.rmtree\(AGENT_DIR\s*\/\s*'skills'/.test(all), 'skills/ removed');
  ok('tool-allowlist', /KNOWN_TOOLS/.test(all), '9-tool registry assert');
  ok('no-skills-stanza', !/^skills:\s*$/m.test(all), 'no skills: stanza');
  const loadSkillHits = [];
  { let p = 0; while (true) { const i = all.indexOf('load_skill', p); if (i < 0) break; loadSkillHits.push(all.slice(Math.max(0, i - 40), i + 40)); p = i + 1; if (loadSkillHits.length > 10) break; } }
  ok('load_skill-only-in-guard', loadSkillHits.length > 0 && loadSkillHits.every(s => /assert|do NOT exist|registry/.test(s)),
    loadSkillHits.length + ' mention(s), all in guard/comment');

  // A5. H1 v5: braces in prompt become ADK session placeholders.
  let sys = null;
  try {
    const m = cells.map(c => c.match(/"prompts\/system\.md":\s*"([^"]+)"/)).find(Boolean);
    if (m) {
      const bin = atob(m[1]);
      sys = { len: bin.length, braces: bin.includes('{') || bin.includes('}'), needles: ['HARD LIMITS', 'CALL PLAN', 'by call 12', 'CONFIDENCE', 'never rewrite a whole file', 'STEP 1'].filter(n => bin.includes(n)) };
    }
  } catch (e) { sys = { err: String(e) }; }
  ok('systemmd-decodes', !!(sys && !sys.err), sys && sys.err ? sys.err : (sys ? sys.len + ' chars' : 'no payload'));
  ok('systemmd-zero-braces', !!(sys && !sys.braces), sys ? 'braces=' + sys.braces : '');
  ok('systemmd-needles', !!(sys && sys.needles && sys.needles.length === 6), sys ? sys.needles.join('|') : '');

  // A6. ARM2 v2: sampling.yaml must NEVER ship thinking keys.
  const fkeys = [];
  { const m4 = cells[4] || ''; const re = /"([^"]+)":\s*"/g; let m; while ((m = re.exec(m4))) fkeys.push(m[1]); }
  ok('F-keys-exact-3', JSON.stringify(fkeys.slice(0, 3)) === JSON.stringify(['prompts/system.md', 'agent.yaml', 'eval_config.yaml']), fkeys.slice(0, 5).join(','));
  ok('no-sampling-ship', !fkeys.some(k => /sampling/i.test(k)), 'sampling.yaml not in F');
  ok('no-thinking-pin', !all.includes('thinking->4096'), 'no 4096 pin');
  ok('thinking-strip', /_kept\s*=\s*\[l for l in _lines/.test(all), 'line-filter strip present');
  ok('no-doublebs-strip', !/r\('\^\\\\s/.test(all), 'no double-escaped strip regex');
  ok('thinking-guard', /assert 'thinking_budget' not in samp/.test(all), 'fail-loud assert present');
  ok('safe-pins', ['temperature', 'top_p', 'top_k', 'max_output_tokens'].every(k => all.includes("'" + k + "'")), 'temp/top_p/top_k/max_tokens');

  // A7. Envelope: tasks, run tag, manifest, sidecar, validator, brace scan.
  const taskIds = [...new Set([...all.matchAll(/"(fastapi_\d+|rich_\d+|requests_\d+|httpx_\d+)"/g)].map(m => m[1]))];
  ok('tasks-10-no14356', taskIds.length === 10 && !all.includes('14356'), taskIds.join(','));
  ok('run-tag', /arm2-winner/.test(all), 'RUN_TAG arm2-winner');
  ok('manifest', /ARM2_MANIFEST/.test(all), 'manifest');
  ok('sidecar', /OUR-TRANSCRIPTS/.test(all), 'PKG-SIDECAR');
  ok('validator-gate', /validate_directory/.test(all), 'real validator gate');
  ok('brace-scan', /brace scan/.test(all), 'brace scan cell');
  ok('no-arm1', !/arm1_|ARM1_MANIFEST/.test(all), 'no arm1 leftovers');
  ok('no-case-swap-bug', !/Never rewrite a whole file/.test(all) || /never rewrite a whole file/.test(all), 'needle case matches prompt');

  const failures = checks.filter(c => !c.ok).map(c => c.id);
  return { pass: failures.length === 0, failures, checks };
}

// Fire-body auditor: SaveKernel params that live OUTSIDE the notebook
// (H1 v4 pin typo + title rules). Pass the exact body about to be POSTed.
function auditFireBody(body, opts) {
  opts = opts || {};
  const checks = [];
  const ok = (id, cond, detail) => checks.push({ id, ok: !!cond, detail: detail || '' });
  ok('pin-exact', body.dockerImage === 'gcr.io/kaggle-private-byod/python@sha256:37c64f7dd9c54116ecd1bcc88817c5469b88387388fade02bfa8bf3fc647d461', String(body.dockerImage || '').slice(0, 60));
  ok('title-len', typeof body.new_title === 'string' && body.new_title.length >= 1 && body.new_title.length <= 50, (body.new_title || '') + ' (' + (body.new_title || '').length + ' chars)');
  ok('title-fresh', !opts.usedTitles || !opts.usedTitles.includes(body.new_title), 'must differ from every pushed title (Kaggle 409s repeats)');
  ok('gpu-l4', body.enableGpu === true && body.machineShape === 'NvidiaL4', body.machineShape);
  ok('no-internet', body.enableInternet === false, 'harness is offline');
  ok('sources', (body.competitionDataSources || []).includes('gemma-4-developer-agent') && (body.modelDataSources || []).some(s => s.includes('e4b')), JSON.stringify(body.modelDataSources || []));
  ok('save-and-run', body.kernelExecutionType === 'SAVE_AND_RUN_ALL', body.kernelExecutionType);
  const failures = checks.filter(c => !c.ok).map(c => c.id);
  return { pass: failures.length === 0, failures, checks };
}
