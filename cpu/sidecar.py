#!/usr/bin/env python3
"""cpu/sidecar.py - repo symbol index (stdlib only, offline, no secrets)."""
import argparse, json, os, re
SYM = re.compile(r'^(\s*)(def|class)\s+([A-Za-z_][A-Za-z0-9_]*)')
ap = argparse.ArgumentParser()
ap.add_argument('--ws', default='/tmp/ws')
ap.add_argument('--out', default='sidecar/index.json')
ap.add_argument('--cap', type=int, default=200000)
ap.add_argument('--issue-file', default='')
ap.add_argument('--topk', type=int, default=3)
ap.add_argument('--emit-candidates', action='store_true')
a = ap.parse_args()
syms = []
stop = False
for root, dirs, files in os.walk(a.ws):
    dirs[:] = [d for d in dirs if d not in ('.git', '__pycache__', '.hg', 'node_modules')]
    for f in files:
        if not f.endswith('.py'):
            continue
        p = os.path.join(root, f)
        rel = os.path.relpath(p, a.ws)
        try:
            fh = open(p, 'r', encoding='utf-8', errors='replace')
        except Exception:
            continue
        with fh:
            for i, line in enumerate(fh):
                m = SYM.match(line)
                if m:
                    syms.append({'n': m.group(3), 'f': rel, 'l': i + 1, 'k': m.group(2)})
                    if len(syms) >= a.cap:
                        stop = True
                        break
        if stop:
            break
os.makedirs(os.path.dirname(a.out) or '.', exist_ok=True)
json.dump({'symbols': syms}, open(a.out, 'w'))
print('symbols=' + str(len(syms)))
if a.emit_candidates and a.issue_file:
    # inject arm (P16, own decision set): rank symbols by token overlap with the
    # issue, emit top-k with source line content as UNVERIFIED candidates.
    import string as _s
    issue = open(a.issue_file, encoding='utf-8', errors='replace').read().lower()
    itoks = set(t for t in issue.translate(str.maketrans(_s.punctuation, ' ' * len(_s.punctuation))).split() if len(t) > 3)
    scored = []
    for sm in syms:
        ntoks = set(sm['n'].lower().split('_'))
        ov = len(ntoks & itoks)
        if ov: scored.append((ov, sm))
    scored.sort(key=lambda x: -x[0])
    for ov, sm in scored[:a.topk]:
        try:
            fl = open(os.path.join(a.ws, sm['f']), encoding='utf-8', errors='replace').read().split('\n')
            ctx = fl[sm['l'] - 1][:160] if 1 <= sm['l'] <= len(fl) else ''
        except Exception:
            ctx = ''
        print('CANDIDATE: %s:%d [%s] %s :: %s' % (sm['f'], sm['l'], sm['k'], sm['n'], ctx))