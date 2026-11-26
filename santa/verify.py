"""Exact verifier for Santa 2026 Elf Calculator programs (rules from the Data/Evaluation pages)."""
import csv, json, sys
csv.field_size_limit(10**9)

def load_puzzles(path):
    P = {}
    with open(path) as f:
        for r in csv.DictReader(f):
            P[r['id']] = dict(start=json.loads(r['starting_values']), targets=json.loads(r['targets']),
                              limit=int(r['value_limit']), regs=int(r['registers']))
    return P

def check(p, prog):
    """Return (ok, msg). prog = list of [op,i,j,d]."""
    if not isinstance(prog, list) or len(prog) > 4096:
        return False, 'bad/too long'
    R = [None] * p['regs']
    for k, v in enumerate(p['start']):
        R[k] = v
    need = set(p['targets']) - set(p['start'])
    L = p['limit']
    for n, ins in enumerate(prog):
        if not (isinstance(ins, list) and len(ins) == 4): return False, f'{n}: shape'
        op, i, j, d = ins
        if op not in '+-*/' or len(op) != 1: return False, f'{n}: op'
        for x in (i, j, d):
            if type(x) is not int or not 0 <= x < p['regs']: return False, f'{n}: reg'
        a, b = R[i], R[j]
        if a is None or b is None: return False, f'{n}: undefined'
        if op == '+': v = a + b
        elif op == '-':
            if a <= b: return False, f'{n}: sub nonpos'
            v = a - b
        elif op == '*': v = a * b
        else:
            if a % b: return False, f'{n}: inexact div'
            v = a // b
        if v > L: return False, f'{n}: over limit'
        R[d] = v
        need.discard(v)
    if need: return False, f'missing {len(need)} targets'
    return True, 'ok'

def load_sub(path):
    with open(path, encoding='utf-8') as f:
        return {r['id']: r['program'] for r in csv.DictReader(f)}

if __name__ == '__main__':
    P = load_puzzles(sys.argv[1])
    for sp in sys.argv[2:]:
        S = load_sub(sp); tot = 0; bad = 0
        for pid in P:
            if pid not in S: bad += 1; continue
            prog = json.loads(S[pid]); ok, m = check(P[pid], prog)
            if not ok: bad += 1
            tot += len(prog)
        print(f'{tot:8d} invalid={bad:4d} rows={len(S)} {sp}')
