"""DAG-aware exact search: build target t from a register pool in <= 4 instructions where intermediate
values may be reused (x*x, x+x, t = v2 op v1, ...). Meet in the middle: 2 forward steps from the pool,
up to 2 backward steps from t (pool operands or self-combination z+z / z*z).
Returns a list of steps [(op, x, y)], x/y = ('r', reg) or ('s', step_index); last step yields t."""
import numpy as np
from deep4 import _combine
OPS = '+-*/'

def _iroot2(z):
    r = int(round(z ** 0.5))
    for c in (r - 1, r, r + 1):
        if c > 0 and c * c == z: return c
    return None

def _back(z, V, L):
    """List of (w, op, order, partner) with z = w op partner (order 0) or partner op w (order 1);
    partner = pool index or 'self'."""
    out = []
    for k, a in enumerate(V):
        a = int(a)
        if z > a: out.append((z - a, 0, 0, k))
        if a > z: out.append((a - z, 1, 1, k))      # z = a - w
        if z + a <= L: out.append((z + a, 1, 0, k))  # z = w - a
        if z % a == 0: out.append((z // a, 2, 0, k))
        if a % z == 0: out.append((a // z, 3, 1, k))  # z = a / w
        if z * a <= L: out.append((z * a, 3, 0, k))   # z = w / a
    if z % 2 == 0: out.append((z // 2, 0, 0, 'self'))
    r = _iroot2(z)
    if r: out.append((r, 2, 0, 'self'))
    return out

def dag_search(t, pool, L, maxcost=4):
    pv = list(pool); V = np.array(pv, dtype=np.int64); P = len(pv)
    R = lambda k: ('r', pool[pv[k]])
    s1v, s1a, s1b, s1o = _combine(V, V, L)
    def step1(k): return (OPS[s1o[k]], R(s1a[k]), R(s1b[k]))
    def fin(op, order, x, y): return (OPS[op], x, y) if order == 0 else (OPS[op], y, x)
    def part(pp, me):
        return me if pp == 'self' else R(pp)
    # cost 1
    h = np.nonzero(s1v == t)[0]
    if len(h): return [step1(h[0])]
    if maxcost < 2: return None
    B1 = _back(t, V, L)
    b1v = np.array([b[0] for b in B1], dtype=np.int64)
    o1 = np.argsort(s1v, kind='stable'); s1s = s1v[o1]
    def find_sorted(sorted_arr, order, q):
        pos = np.searchsorted(sorted_arr, q); pos[pos >= len(sorted_arr)] = len(sorted_arr) - 1
        hit = np.nonzero(sorted_arr[pos] == q)[0]
        return hit, order[pos]
    # cost 2: v1 in S1 and t = v1 op (pool | v1)
    hit, idx = find_sorted(s1s, o1, b1v)
    if len(hit):
        i = hit[0]; w, op, od, pp = B1[i]
        return [step1(idx[i]), fin(op, od, ('s', 0), part(pp, ('s', 0)))]
    # cost 2: two independent S1 values? needs 3 steps; handled at cost 3.
    if maxcost < 3: return None
    # forward step 2: v2 = v1 op a | a op v1 | v1 op v1   (parent = S1 index)
    fa_v, fa_p, fa_a, fa_o = _combine(s1v, V, L)
    fb_v, fb_a, fb_p, fb_o = _combine(V, s1v, L)
    ss = s1v[s1v <= L // 2]; sq_ok = s1v <= np.int64(10**9)
    fc_v = np.concatenate([s1v[s1v <= L // 2] * 2, s1v[sq_ok] ** 2])
    fc_p = np.concatenate([np.nonzero(s1v <= L // 2)[0], np.nonzero(sq_ok)[0]])
    fc_o = np.concatenate([np.zeros((s1v <= L // 2).sum(), np.int8), np.full(sq_ok.sum(), 2, np.int8)])
    fc_v_ok = fc_v <= L
    fc_v, fc_p, fc_o = fc_v[fc_v_ok], fc_p[fc_v_ok], fc_o[fc_v_ok]
    na, nb = len(fa_v), len(fb_v)
    F = np.concatenate([fa_v, fb_v, fc_v])
    Fp = np.concatenate([fa_p, fb_p, fc_p])
    def steps2(k):
        if k < na:
            p = fa_p[k]; return p, [step1(p), (OPS[fa_o[k]], ('s', 0), R(fa_a[k]))]
        k -= na
        if k < nb:
            p = fb_p[k]; return p, [step1(p), (OPS[fb_o[k]], R(fb_a[k]), ('s', 0))]
        k -= nb
        p = fc_p[k]; return p, [step1(p), (OPS[fc_o[k]], ('s', 0), ('s', 0))]
    oF = np.argsort(F, kind='stable'); Fs = F[oF]
    # cost 3a: v2 in B1  -> t = v2 op (pool | v2)
    hit, idx = find_sorted(Fs, oF, b1v)
    if len(hit):
        i = hit[0]; w, op, od, pp = B1[i]; _, st = steps2(idx[i])
        return st + [fin(op, od, ('s', 1), part(pp, ('s', 1)))]
    # cost 3b: t = v2 op v1 (both orders)
    v1 = s1v[Fp]
    for op, cond, order in ((0, None, 0), (2, None, 0), (1, 0, 0), (1, 1, 1), (3, 0, 0), (3, 1, 1)):
        with np.errstate(all='ignore'):
            if op == 0: m = (F <= L - v1) & (F + v1 == t)
            elif op == 2: m = (F <= L // v1) & (F * v1 == t)
            elif op == 1 and order == 0: m = (F > v1) & (F - v1 == t)
            elif op == 1: m = (v1 > F) & (v1 - F == t)
            elif order == 0: m = (F % v1 == 0) & (F // v1 == t)
            else: m = (v1 % F == 0) & (v1 // F == t)
        h = np.nonzero(m)[0]
        if len(h):
            _, st = steps2(h[0])
            return st + [fin(op, order, ('s', 1), ('s', 0))]
    # cost 3c: t = x op y, x, y independent S1 values
    for k1 in range(len(s1v)):
        pass  # covered below vectorised
    y_list = []
    x = s1v
    cand = []
    with np.errstate(all='ignore'):
        cand.append((t - x, 0, 0, x < t))
        cand.append((x - t, 1, 0, x > t))
        cand.append((x + t, 1, 1, x <= L - t))
        cand.append((np.where(x != 0, t // np.maximum(x, 1), 0), 2, 0, (t % np.maximum(x, 1)) == 0))
        cand.append((x // t, 3, 0, (x % t) == 0))
        cand.append((x * t, 3, 1, x <= L // t))
    for q, op, order, ok in cand:
        qi = np.nonzero(ok)[0]
        if not len(qi): continue
        hit, idx = find_sorted(s1s, o1, q[qi])
        if len(hit):
            i = qi[hit[0]]; j = idx[hit[0]]
            a = step1(i); b = step1(j)
            return [a, b, fin(op, order, ('s', 0), ('s', 1))]
    if maxcost < 4: return None
    # cost 4a: v2 in B2, B2 = back(B1)  -> v3 = v2 op (pool|v2) ; t = v3 op (pool|v3)
    B2 = []
    for i, (w, op, od, pp) in enumerate(B1):
        if 0 < w <= L:
            for w2, op2, od2, pp2 in _back(int(w), V, L):
                if 0 < w2 <= L: B2.append((w2, i, op2, od2, pp2))
    if B2:
        b2v = np.array([b[0] for b in B2], dtype=np.int64)
        hit, idx = find_sorted(Fs, oF, b2v)
        if len(hit):
            i = hit[0]; w2, i1, op2, od2, pp2 = B2[i]; w, op, od, pp = B1[i1]
            _, st = steps2(idx[i])
            return st + [fin(op2, od2, ('s', 1), part(pp2, ('s', 1))), fin(op, od, ('s', 2), part(pp, ('s', 2)))]
    # cost 4b: v3 = v2 op v1 in B1 ; t = v3 op (pool|v3)
    if len(b1v):
        b1s = np.sort(b1v)
        for op, order in ((0, 0), (2, 0), (1, 0), (1, 1), (3, 0), (3, 1)):
            with np.errstate(all='ignore'):
                if op == 0: ok = F <= L - v1; val = F + v1
                elif op == 2: ok = F <= L // v1; val = F * v1
                elif order == 0 and op == 1: ok = F > v1; val = F - v1
                elif op == 1: ok = v1 > F; val = v1 - F
                elif order == 0: ok = (F % v1) == 0; val = F // v1
                else: ok = (v1 % F) == 0; val = v1 // np.maximum(F, 1)
            qi = np.nonzero(ok)[0]
            if not len(qi): continue
            pos = np.searchsorted(b1s, val[qi]); pos[pos >= len(b1s)] = len(b1s) - 1
            h = np.nonzero(b1s[pos] == val[qi])[0]
            if len(h):
                k = qi[h[0]]; v3 = int(val[k])
                for (w, opb, odb, pp) in B1:
                    if w == v3: break
                _, st = steps2(k)
                return st + [fin(op, order, ('s', 1), ('s', 0)), fin(opb, odb, ('s', 2), part(pp, ('s', 2)))]
    return None

def run_steps(steps, regs, L):
    vals = []
    get = lambda x: regs[x[1]] if x[0] == 'r' else vals[x[1]]
    for op, x, y in steps:
        a, b = get(x), get(y)
        if op == '+': v = a + b
        elif op == '-': v = a - b if a > b else None
        elif op == '*': v = a * b
        else: v = a // b if a % b == 0 else None
        if v is None or v > L or v <= 0: return None
        vals.append(v)
    return vals[-1]
