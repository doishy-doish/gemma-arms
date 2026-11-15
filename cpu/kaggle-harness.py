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
        lines = open(os.path.join(ws, p), encoding='utf-8', errors='replace').read().split('\n')
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
        lines = open(f, encoding='utf-8', errors='replace').read().split('\n')
        hits = [i for i, l in enumerate(lines) if l == oldL]
        if len(hits) != 1: return 'ERR: old line matches %d lines (need exactly 1)' % len(hits)
        lines[hits[0]] = newL
        open(f, 'w', encoding='utf-8').write('\n'.join(lines))
        return 'OK edited %s:%d' % (p, hits[0]+1)
    if name == 'WRITE':
        sp = rest.find(' ')
        p, body = rest[:sp].strip(), rest[sp+1:]
        f = os.path.join(ws, p)
        if os.path.exists(f): return 'ERR: WRITE is new-files-only'
        open(f, 'w', encoding='utf-8').write(body)
        return 'OK wrote ' + p
    return 'ERR: unknown tool ' + name
def run_agent(ws, task_id, problem, prompt, max_calls, arm, sc, outdir, wall_s=1200):
    os.makedirs(outdir, exist_ok=True)
    def log(o):
        open(os.path.join(outdir, 'transcript.jsonl'), 'a').write(json.dumps(o) + '\n')
    system = prompt + '\n\nRepo tree (top 2 levels):\n' + tree(ws)
    log({'system': system[:500], 'problem': problem[:500]})
    messages = [{'role': 'system', 'content': system}, {'role': 'user', 'content': problem}]
    calls, done, t0 = 0, None, time.time()
    while calls < max_calls and time.time() - t0 < wall_s:
        try: text = chat(messages)
        except Exception as e:
            log({'turn': calls, 'error': str(e)[:300]}); break
        m = re.search(r'^\\s*action:\\s*([A-Za-z]+)\\s*([^\\n]*)', text, re.I | re.M)
        if not m:
            calls += 1
            result = 'ERR: no ACTION line; reply with ACTION: <tool> <args>'
            echo = 'ACTION: (none parsed)'
            log({'turn': calls, 'raw': text[:2000], 'action': None})
        else:
            name, rest = m.group(1).upper(), (m.group(2) or '').strip()
            echo = 'ACTION: ' + name.strip() + ' ' + rest[:300]
            if name == 'DONE':
                calls += 1
                log({'turn': calls, 'raw': text[:2000], 'action': 'DONE'})
                done = rest[:300]; break
            calls += 1
            try: result = tool(name.strip(), rest, ws, sc)
            except Exception as e: result = 'ERR: ' + str(e)[:300]
            log({'turn': calls, 'raw': text[:2000], 'action': name.strip()})
        log({'turn': calls, 'result': str(result)[:2000]})
        # batch 4: never re-feed the full model echo (runaway text killed GH pilots
        # at 4944>4096). ACTION line only + sliding window under ~20k chars.
        messages.append({'role': 'assistant', 'content': echo})
        messages.append({'role': 'user', 'content': 'TOOL RESULT:\n' + str(result)[:3000] + '\nReply with EXACTLY one ACTION line.'})
        chars = sum(len(mm.get('content', '')) for mm in messages)
        while len(messages) > 4 and chars > 20000:
            for dd in messages[2:4]: chars -= len(dd.get('content', ''))
            del messages[2:4]
    diff = ''
    try:
        diff = subprocess.run(['git', '-C', ws, 'diff', '--', '.:!*.orig'], capture_output=True, text=True, timeout=60).stdout
    except Exception as e:
        diff = 'ERR git diff: ' + str(e)[:200]
    open(os.path.join(outdir, 'agent.patch'), 'w').write(diff)
    open(os.path.join(outdir, 'metrics.json'), 'w').write(json.dumps({'task': task_id, 'arm': arm, 'calls': calls, 'done': done, 'wall_s': round(time.time()-t0), 'patch_chars': len(diff)}))
    return calls, done, diff
print('harness loaded')