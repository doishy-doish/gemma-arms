#!/usr/bin/env python3
"""cpu/sidecar.py - repo symbol index (stdlib only, offline, no secrets)."""
import argparse, json, os, re
SYM = re.compile(r'^(\s*)(def|class)\s+([A-Za-z_][A-Za-z0-9_]*)')
ap = argparse.ArgumentParser()
ap.add_argument('--ws', default='/tmp/ws')
ap.add_argument('--out', default='sidecar/index.json')
ap.add_argument('--cap', type=int, default=200000)
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