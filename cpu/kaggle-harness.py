import json, os, re, subprocess, sys, time, urllib.request
URL = 'http://localhost:8000/v1/chat/completions'
def chat(messages, timeout=600, tries=5):
    import time as _t, urllib.error as _e
    body = json.dumps({'messages': messages, 'temperature': 0.2, 'max_tokens': 512}).encode()
    last = 'no tries'
    for _ in range(tries):
        try:
            req = urllib.request.Request(URL, data=body, headers={'Content-Type': 'application/json'})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                j = json.load(r)
            return j['choices'][0]['message']['content']
        except Exception as ex:
            last = str(ex)[:200]; _t.sleep(30)
    raise RuntimeError(last)
def tree(ws):
    out = []
    def walk(d, depth):
        if depth > 2 or len(out) > 200: return
        try: ents = sorted(os.listdir(d))
        except Exception: return
        for e in ents:
            if e in ('.git', '__pycache__'): continue
            p = os.path.join(d, e)
            out.append(os.path.relpath(p, ws) + ('/' if os.path.isdir(p) else ''))
            if os.path.isdir(p): walk(p, depth + 1)
            if len(out) > 200: break
    walk(ws, 0)
    return '\n'.join(out)
def build_index(ws):
    syms = []
    pat = re.compile(r'^(\s*)(def|class)\s+([A-Za-z_][A-Za-z0-9_]*)')
    for root, dirs, files in os.walk(ws):
        dirs[:] = [d for d in dirs if d not in ('.git', '__pycache__', '.hg', 'node_modules')]
        for f in files:
            if not f.endswith('.py'): continue
            p = os.path.join(root, f)
            try: fh = open(p, encoding='utf-8', errors='replace')
            except Exception: continue
            with fh:
                for i, line in enumerate(fh):
                    m = pat.match(line)
                    if m: syms.append({'n': m.group(3), 'f': os.path.relpath(p, ws), 'l': i + 1, 'k': m.group(2)})
                    if len(syms) >= 200000: break
    return syms
def tool(name, rest, ws, sc):
    if name == 'SIDECAR':
        if sc is None: return 'ERR: no sidecar index (nosidecar arm) - use GREP'
        q = rest.strip().lower()
        if not q: return 'ERR: SIDECAR needs a symbol substring'
        hits = [s for s in sc if q in (s['n'] or '').lower()][:20]
        return '\n'.join('%s:%d [%s] %s' % (s['f'], s['l'], s['k'], s['n']) for s in hits) or '(no symbols match)'
    if name == 'READ':
        rest = re.sub(r'[\[\]"]', '', rest)
        rest = rest.replace('start-line=', '').replace('end-line=', '')
        parts = rest.split()
        p = parts[0]; a = parts[1] if len(parts) > 1 else '1'; b = parts[2] if len(parts) > 2 else None
        try:
            lines = open(os.path.join(ws, p), encoding='utf-8', errors='replace').read().split('\n')
        except Exception:
            return 'ERR: no such file: %s. Use a path from this repo tree:\n%s' % (p, tree(ws)[:2000])
        s = max(0, int(a) - 1); e = min(len(lines), int(b) if b else s + 150)
        return '\n'.join('%d:%s' % (s+i+1, l) for i, l in enumerate(lines[s:e]))[:10000]
    if name == 'LS':
        d = os.path.join(ws, rest.strip() or '.')
        es = sorted(os.listdir(d))
        return '\n'.join(e + ('/' if os.path.isdir(os.path.join(d, e)) else '') for e in es[:100])
    if name == 'GREP':
        q = rest.strip(); out = []
        for root, dirs, files in os.walk(ws):
            dirs[:] = [d for d in dirs if d not in ('.git', '__pycache__')]
            for f in files:
                if len(out) > 30: break
                if not re.search(r'\.(py|md|txt|cfg|toml)$', f): continue
                p = os.path.join(root, f)
                try: lines = open(p, encoding='utf-8', errors='replace').read().split('\n')
                except Exception: continue
                for i, l in enumerate(lines):
                    if len(out) > 30: break
                    if q in l: out.append('%s:%d:%s' % (os.path.relpath(p, ws), i+1, l[:200]))
        return '\n'.join(out) or '(no hits)'
    if name == 'EDIT':
        parts = rest.split(' ||| ')
        if len(parts) != 3: return 'ERR: EDIT needs <path> ||| <old line> ||| <new line>'
        p, oldRaw, newRaw = parts[0].strip(), parts[1], parts[2]
        q = lambda s: s[1:-1] if len(s) >= 2 and s.startswith('"') and s.endswith('"') else s
        oldL, newL = q(oldRaw), q(newRaw)
        f = os.path.join(ws, p)
        try:
            lines = open(f, encoding='utf-8', errors='replace').read().split('\n')
        except Exception:
            return 'ERR: no such file: %s. Use a path from this repo tree:\n%s' % (p, tree(ws)[:2000])
        hits = [i for i, l in enumerate(lines) if l == oldL]
        how = 'exact'
        if len(hits) != 1:
            want = oldL.strip()
            hits = [i for i, l in enumerate(lines) if l.strip() == want]
            how = 'flex'
        if len(hits) != 1:
            toks = sorted([re.sub(r'[^A-Za-z0-9_]', '', w) for w in oldL.split()], key=len, reverse=True)
            tok = next((w for w in toks if len(w) >= 4), '')
            near = []
            if tok:
                for i, l in enumerate(lines):
                    if len(near) >= 3: break
                    if tok in l: near.append('%d:%s' % (i+1, l[:160]))
            hint = ('. Closest lines with %r:\n%s' % (tok, '\n'.join(near))) if near else '. No close lines.'
            return 'ERR: old line matches %d lines (need exactly 1)' % len(hits) + hint
        lines[hits[0]] = newL
        open(f, 'w', encoding='utf-8').write('\n'.join(lines))
        return 'OK edited %s:%d (%s)' % (p, hits[0]+1, how)
    if name == 'EDITLINE':
        parts = rest.split(' ||| ')
        if len(parts) != 3: return 'ERR: EDITLINE needs <path> ||| <line number> ||| <new line>'
        p, nRaw, newL = parts[0].strip(), parts[1].strip(), parts[2]
        f = os.path.join(ws, p)
        try:
            lines = open(f, encoding='utf-8', errors='replace').read().split('\n')
        except Exception:
            return 'ERR: no such file: %s. Use a path from this repo tree:\n%s' % (p, tree(ws)[:2000])
        try: n = int(nRaw)
        except Exception: return 'ERR: line number must be an integer, got %r' % nRaw[:40]
        if not (1 <= n <= len(lines)): return 'ERR: line number out of range 1..%d' % len(lines)
        was = lines[n-1]
        lines[n-1] = newL
        open(f, 'w', encoding='utf-8').write('\n'.join(lines))
        return 'OK edited %s:%d (line) was: %s' % (p, n, was[:160])
    if name == 'WRITE':
        sp = rest.find(' ')
        p, body = rest[:sp].strip(), rest[sp+1:]
        f = os.path.join(ws, p)
        if os.path.exists(f): return 'ERR: WRITE is new-files-only'
        open(f, 'w', encoding='utf-8').write(body)
        try: subprocess.run(['git', '-C', ws, 'add', '-N', p.strip()], capture_output=True, timeout=60)
        except Exception: pass
        return 'OK wrote ' + p
    return 'ERR: unknown tool ' + name
# ---- batch-9 deterministic machinery (mirrors smoke-agent.mjs) ----
def sig_of(name, rest):
    norm = lambda s: re.sub(r'[^a-z0-9_]+', '', (s or '').lower())
    if name == 'READ': return 'READ ' + (rest.split()[0] if rest.split() else '').lower()
    if name == 'LS': return 'LS ' + (rest.strip() or '.').lower()
    if name in ('GREP', 'SIDECAR'): return name + ' ' + norm(rest)
    if name == 'EDIT':
        ps = rest.split(' ||| ')
        return 'EDIT ' + (ps[0] if ps else '').strip().lower() + ' :: ' + norm(ps[1] if len(ps) > 1 else '')
    if name == 'EDITLINE':
        ps = rest.split(' ||| ')
        return 'EDITLINE ' + (ps[0] if ps else '').strip().lower() + ' :: ' + (ps[1] if len(ps) > 1 else '').strip()
    if name == 'WRITE': return 'WRITE ' + (rest.split()[0] if rest.split() else '').lower()
    return name + ' ' + rest.strip()
EDIT_CLASS = ('EDIT', 'EDITLINE', 'WRITE')
GROUND_CLASS = ('LS', 'SIDECAR', 'GREP', 'READ')
def path_arg(name, rest):
    if name in ('READ', 'LS', 'WRITE'): return (rest.split()[0] if rest.split() else '').strip()
    if name in ('EDIT', 'EDITLINE'): return (rest.split(' ||| ')[0] if rest else '').strip()
    return ''
def git_diff(ws):
    try:
        return subprocess.run(['git', '-C', ws, 'diff', '--', '.:!*.orig'], capture_output=True, text=True, timeout=60).stdout
    except Exception: return 'ERR'
def diff_files(ws):
    try:
        s = subprocess.run(['git', '-C', ws, 'diff', '--name-status', '--', '.:!*.orig'], capture_output=True, text=True, timeout=60).stdout
        out = []
        for l in s.split('\n'):
            if not l.strip(): continue
            st, _, p = l.partition('\t')
            out.append({'st': st.strip(), 'p': p})
        return out
    except Exception: return []
def critic(ws, summary):
    d = git_diff(ws)
    if not d.strip() or d.startswith('ERR'): return 'ERR: DONE rejected. Working tree has no patch (0 chars). Make at least one EDIT that changes repo source, then DONE.'
    files = diff_files(ws)
    bad = [f['p'] for f in files if re.search(r'(^|/)tests?/', f['p']) or re.search(r'(^|/)(test_.*|conftest\.py)$', f['p']) or re.search(r'\.(cfg|toml|ini|yaml|yml)$', f['p']) or f['p'] == 'setup.py']
    if bad: return 'ERR: DONE rejected. Patch touches test/config paths (%s). EDIT repo source only, then DONE.' % ', '.join(bad)
    if files and all(f['st'] == 'A' for f in files): return 'ERR: DONE rejected. Patch adds files but modifies no existing source. EDIT the buggy file, then DONE.'
    names = [f['p'].split('/')[-1].lower() for f in files if f['p']]
    if not any(n and n in (summary or '').lower() for n in names):
        return 'ERR: DONE rejected. Summary must name a file your patch touches (%s). Re-read your diff, then DONE.' % ', '.join(names[:5])
    return None
def key_lines(problem):
    out = []
    for l in str(problem or '').split('\n'):
        if len(out) >= 12: break
        t = l.strip()
        if len(t) < 4 or len(t) > 220: continue
        if re.search(r'error|assert|expected|raise|traceback|denied|fail|def |class |return|import ', t, re.I): out.append(t[:160])
    return out
def mid_green(ws, test_files):
    if not test_files: return 'unknown'
    try:
        p = subprocess.run(['python', '-m', 'pytest'] + list(test_files) + ['-q', '--tb=no', '-W', 'ignore::DeprecationWarning'],
            cwd=ws, capture_output=True, text=True, timeout=240)
        tail = ' '.join(((p.stdout or '') + '\n' + (p.stderr or '')).split('\n')[-3:])
        if re.search(r'failed|error', tail, re.I): return 'red'
        return 'green' if 'passed' in tail else 'unknown'
    except Exception: return 'unknown'
def top_symbol(problem):
    kw = set(['import', 'from', 'def', 'class', 'return', 'raise', 'assert', 'for', 'while', 'with', 'none', 'true', 'false', 'null', 'self', 'issue', 'error', 'expected', 'actual', 'should', 'when', 'that', 'this', 'test', 'tests'])
    toks = [t for t in re.split(r'[^A-Za-z0-9_]+', str(problem or '')) if len(t) >= 4 and t.lower() not in kw]
    return next((t for t in toks if '_' in t or re.search('[a-z][A-Z]', t)), toks[0] if toks else '')
def run_agent(ws, task_id, problem, prompt, max_calls, arm, sc, outdir, wall_s=1200, test_files=None):
    os.makedirs(outdir, exist_ok=True)
    def log(o):
        open(os.path.join(outdir, 'transcript.jsonl'), 'a').write(json.dumps(o) + '\n')
    examples = set(l.strip() for l in prompt.split('\n') if re.match(r'^ACTION:\s*\w+', l.strip(), re.I))
    treetxt = tree(ws)
    top = set(p.split('/')[0].lower() for p in treetxt.split('\n') if p)
    route = 'small-repo: open with GREP or SIDECAR on issue symbols, LS only if lost' if len(treetxt.split('\n')) < 60 else 'standard: open with LS or GREP, then READ +-40 around hits'
    kl = key_lines(problem)
    if kl: problem = problem + '\nKEY LINES (shaped spec \u2014 GREP these symbols):\n' + '\n'.join(kl)
    system = prompt + '\nROUTER: ' + route + '.\n\nRepo tree (top 2 levels):\n' + treetxt
    prime_sym = top_symbol(problem)
    try: prime_res = tool('SIDECAR' if sc is not None else 'GREP', prime_sym or 'def', ws, sc)[:1500]
    except Exception as ex: prime_res = 'ERR: ' + str(ex)[:120]
    problem = problem + chr(10) + 'PRIMED OBSERVATION (real repo content -- act on this, not the examples):' + chr(10) + (prime_res or '(no hits -- LS the tree)')
    observed = set()
    def note_observed(name, rest, result):
        if not result or result.startswith('ERR') or result in ('(no hits)', '(no symbols match)'): return
        if name == 'READ': observed.add(path_arg(name, rest).lower())
        elif name == 'LS':
            d = (rest.strip() or '.').rstrip('/')
            for l in str(result).split(chr(10))[:100]:
                e = l.strip()
                if not e or e.endswith('/'): continue
                observed.add((e if d == '.' else d + '/' + e).lower())
        elif name == 'GREP':
            for l in str(result).split(chr(10))[:30]:
                p = l.split(':')[0]
                if p and '.' in p: observed.add(p.strip().lower())
        elif name == 'SIDECAR':
            for l in str(result).split(chr(10))[:20]:
                p = l.split(':')[0]
                if p and '/' in p: observed.add(p.strip().lower())
    note_observed('SIDECAR' if sc is not None else 'GREP', prime_sym or 'def', prime_res)
    log({'system': system[:500], 'problem': problem[:500], 'route': route, 'primed': prime_sym})
    messages = [{'role': 'system', 'content': system}, {'role': 'user', 'content': problem}]
    calls, done, t0 = 0, None, time.time()
    lastSig, seenSigs, streak, aborted = '', set(), 0, False
    greenAt, greenCheckedPatch = 0, -1
    criticRejects, maskedErrs, skippedBurst, sigRepeats, gatedRejects = 0, 0, 0, 0, 0
    while calls < max_calls and time.time() - t0 < wall_s:
        try: text = chat(messages)
        except Exception as e:
            log({'turn': calls, 'error': str(e)[:300]}); break
        acts = [{'name': m.group(1).upper().strip(), 'rest': (m.group(2) or '').strip(), 'line': m.group(0).strip()}
                for m in re.finditer(r'^\s*action:\s*([A-Za-z]+)\s*([^\n]*)', text, re.I | re.M)]
        if not acts:
            calls += 1
            streak += 1
            result = 'ERR: no ACTION line; reply with ACTION: <tool> <args>'
            echo = 'ACTION: (none parsed)'
            log({'turn': calls, 'raw': text[:2000], 'action': None, 'progress': False, 'streak': streak})
            if streak >= 3:
                aborted = True
                log({'turn': calls, 'result': result, 'abort': 'mute streak=3, run capped (F21)'})
                break
        else:
            pick, skipped = None, []
            for ac in acts:
                s = sig_of(ac['name'], ac['rest'])
                if ac['line'] in examples: skipped.append('example-copy:' + ac['line'][:60]); continue
                if ac['name'] != 'DONE' and s == lastSig: skipped.append('repeat:' + s[:60]); continue
                pa = path_arg(ac['name'], ac['rest'])
                if pa and pa.split('/')[0].lower() not in top: skipped.append('non-tree:' + pa[:60]); continue
                pick = ac; break
            if pick is None: pick = acts[0]
            skippedBurst += len(skipped)
            name, rest = pick['name'], pick['rest']
            echo = 'ACTION: ' + name.strip() + ' ' + rest[:300]
            progress, acted = False, None
            if name == 'DONE':
                calls += 1
                log({'turn': calls, 'raw': text[:2000], 'action': 'DONE', 'skipped': skipped})
                rej = critic(ws, rest)
                if rej: result = rej; criticRejects += 1
                else: done = rest[:300]; log({'turn': calls, 'result': 'DONE accepted'}); break
            else:
                calls += 1
                s = sig_of(name.strip(), rest)
                if s == lastSig:
                    sigRepeats += 1
                    result = 'ERR: repeated action shape \u2014 same ' + name.strip() + ' shape twice in a row is banned, switch tools (READ once, then GREP or EDIT).'
                elif name.strip() in ('EDIT', 'EDITLINE') and calls <= 3:
                    gatedRejects += 1
                    result = 'ERR: localize first -- calls 1-3 are LS/GREP/SIDECAR/READ only (edit window opens call 4). Ground the bug location first.'
                elif name.strip() in ('EDIT', 'EDITLINE') and path_arg(name.strip(), rest).lower() not in observed:
                    gatedRejects += 1
                    seen = sorted(observed)[:5]
                    result = 'ERR: grounding gate -- ' + (path_arg(name.strip(), rest) or '(no path)') + ' is not a file you have looked at. ' + ('You HAVE seen: ' + ', '.join(seen) + '. READ one first, then EDIT it.' if seen else 'LS the tree or GREP a symbol first.') + ' Example paths (acme/...) are never real.'
                else:
                    lastSig = s
                    if name.strip() in EDIT_CLASS:
                        try: result = tool(name.strip(), rest, ws, sc)
                        except Exception as e: result = 'ERR: ' + str(e)[:300]
                        lastSig = ''; progress = True
                    elif name.strip() in GROUND_CLASS:
                        try: result = tool(name.strip(), rest, ws, sc)
                        except Exception as e: result = 'ERR: ' + str(e)[:300]
                        if s not in seenSigs: seenSigs.add(s); progress = True
                    else:
                        try: result = tool(name.strip(), rest, ws, sc)
                        except Exception as e: result = 'ERR: ' + str(e)[:300]
                    acted = name.strip()
                    note_observed(name.strip(), rest, result)
                    log({'turn': calls, 'raw': text[:2000], 'action': name.strip(), 'sig': s[:80], 'progress': progress, 'streak': streak, 'skipped': skipped})
                if not progress: streak += 1
                else: streak = 0
                if streak >= 3 and not done:
                    aborted = True
                    log({'turn': calls, 'result': str(result)[:2000], 'abort': 'no-progress streak=3, run capped (F21)'})
                    break
            log({'turn': calls, 'action': name.strip() if acts else None})
        isErr = str(result).startswith('ERR')
        if isErr: maskedErrs += 1
        messages.append({'role': 'assistant', 'content': 'ACTION failed (masked). Switch tools, never repeat.' if isErr else echo})
        messages.append({'role': 'user', 'content': 'TOOL RESULT:\n' + str(result)[:3000] + '\nReply with EXACTLY one ACTION line.'})
        chars = sum(len(mm.get('content', '')) for mm in messages)
        while len(messages) > 4 and chars > 20000:
            for dd in messages[2:4]: chars -= len(dd.get('content', ''))
            del messages[2:4]
        if not greenAt and acted and acted in EDIT_CLASS and str(result).startswith('OK'):
            now = git_diff(ws)
            if now.strip() and not now.startswith('ERR') and len(now) != greenCheckedPatch:
                greenCheckedPatch = len(now)
                g = mid_green(ws, test_files)
                log({'turn': calls, 'midcheck': g, 'patch_chars': len(now)})
                if g == 'green': greenAt = calls
        if greenAt and calls >= greenAt + 2 and not done:
            files = [f['p'].split('/')[-1] for f in diff_files(ws)]
            done = 'auto: post-green cap (+2), touches ' + ', '.join(files[:3])
            log({'turn': calls, 'result': 'post-green cap fired, auto-DONE'})
            break
    diff = git_diff(ws)
    if diff.startswith('ERR'): diff = ''
    open(os.path.join(outdir, 'agent.patch'), 'w').write(diff)
    open(os.path.join(outdir, 'metrics.json'), 'w').write(json.dumps({'task': task_id, 'arm': arm, 'calls': calls, 'done': done, 'wall_s': round(time.time()-t0), 'patch_chars': len(diff), 'abort': aborted, 'green_at': greenAt, 'critic_rejects': criticRejects, 'masked_errs': maskedErrs, 'skipped_burst': skippedBurst, 'sig_repeats': sigRepeats, 'gated_rejects': gatedRejects, 'route': route, 'primed': prime_sym, 'observed_n': len(observed)}))
    return calls, done, diff
print('harness loaded')