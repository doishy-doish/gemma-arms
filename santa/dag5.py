"""Depth-5 exact check: t = A op B with A, B two independent 2-step DAG values from the pool
(F2 = {v1 op x : v1 in S1, x in pool or v1}).  Returns steps or None."""
import numpy as np
from deep4 import _combine
OPS = '+-*/'

def forward2(V, L):
    s1v, s1a, s1b, s1o = _combine(V, V, L)
    fa_v, fa_p, fa_a, fa_o = _combine(s1v, V, L)      # v1 op a
    fb_v, fb_a, fb_p, fb_o = _combine(V, s1v, L)      # a op v1
    m2 = s1v <= L // 2; msq = s1v <= np.int64(10**9)
    fc_v = np.concatenate([s1v[m2] * 2, s1v[msq] ** 2])
    fc_p = np.concatenate([np.nonzero(m2)[0], np.nonzero(msq)[0]])
    fc_o = np.concatenate([np.zeros(m2.sum(), np.int8), np.full(msq.sum(), 2, np.int8)])
    ok = fc_v <= L; fc_v, fc_p, fc_o = fc_v[ok], fc_p[ok], fc_o[ok]
    F = np.concatenate([fa_v, fb_v, fc_v])
    na, nb = len(fa_v), len(fb_v)
    def steps(k, base):
        """steps computing F[k], step indices offset by base; returns list."""
        def s1(p): return (OPS[s1o[p]], ('r', int(s1a[p])), ('r', int(s1b[p])))
        if k < na:
            p = fa_p[k]; return [s1(p), (OPS[fa_o[k]], ('s', base), ('r', int(fa_a[k])))]
        k -= na
        if k < nb:
            p = fb_p[k]; return [s1(p), (OPS[fb_o[k]], ('r', int(fb_a[k])), ('s', base))]
        k -= nb
        p = fc_p[k]; return [s1(p), (OPS[fc_o[k]], ('s', base), ('s', base))]
    return F, steps

def dag5(t, pool, L):
    pv = list(pool); V = np.array(pv, dtype=np.int64)
    F, steps = forward2(V, L)
    # dedupe values for lookup
    uv, ui = np.unique(F, return_index=True)
    A = uv
    with np.errstate(all='ignore'):
        cands = [
            (t - A, '+', 0, A < t),
            (A - t, '-', 0, A > t),
            (A + t, '-', 1, A <= L - t),
            (t // np.maximum(A, 1), '*', 0, (t % np.maximum(A, 1)) == 0),
            (A // t, '/', 0, (A % t) == 0),
            (A * t, '/', 1, A <= L // t),
        ]
    for q, op, order, ok in cands:
        qi = np.nonzero(ok)[0]
        if not len(qi): continue
        qq = q[qi]
        pos = np.searchsorted(uv, qq); pos[pos >= len(uv)] = len(uv) - 1
        hit = np.nonzero(uv[pos] == qq)[0]
        if len(hit):
            ka = int(ui[qi[hit[0]]]); kb = int(ui[pos[hit[0]]])
            sa = steps(ka, 0); sb = steps(kb, 2)
            # remap register refs to pool registers
            def remap(st):
                return [(o, ('r', pool[pv[x[1]]]) if x[0] == 'r' else x, ('r', pool[pv[y[1]]]) if y[0] == 'r' else y)
                        for o, x, y in st]
            sa, sb = remap(sa), remap(sb)
            last = (op, ('s', 1), ('s', 3)) if order == 0 else (op, ('s', 3), ('s', 1))
            return sa + sb + [last]
    return None
