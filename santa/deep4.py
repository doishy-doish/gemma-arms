"""Exact 4-instruction synthesis of a target from a register pool (numpy meet-in-the-middle)."""
import numpy as np

OPS = '+-*/'

def _combine(A, B, L):
    """All a op b for a in A, b in B (int64 arrays, values <= L <= 1e18). Returns (vals, ia, ib, op)."""
    ia, ib = np.meshgrid(np.arange(len(A)), np.arange(len(B)), indexing='ij')
    ia = ia.ravel(); ib = ib.ravel(); a = A[ia]; b = B[ib]
    out_v, out_a, out_b, out_o = [], [], [], []
    m = a <= L - b                                      # +
    out_v.append(a[m] + b[m]); out_a.append(ia[m]); out_b.append(ib[m]); out_o.append(np.full(m.sum(), 0, np.int8))
    m = a > b                                           # -
    out_v.append(a[m] - b[m]); out_a.append(ia[m]); out_b.append(ib[m]); out_o.append(np.full(m.sum(), 1, np.int8))
    m = a <= L // b                                     # *
    out_v.append(a[m] * b[m]); out_a.append(ia[m]); out_b.append(ib[m]); out_o.append(np.full(m.sum(), 2, np.int8))
    m = (a % b) == 0                                    # /
    out_v.append(a[m] // b[m]); out_a.append(ia[m]); out_b.append(ib[m]); out_o.append(np.full(m.sum(), 3, np.int8))
    return np.concatenate(out_v), np.concatenate(out_a), np.concatenate(out_b), np.concatenate(out_o)

def _needed(t, X, L):
    """For each x in X: values y with t = x op y (order 0) or t = y op x (order 1).
    Returns (y, ix, op, order)."""
    res = []
    ix = np.arange(len(X))
    def add(mask, y, op, order):
        res.append((y[mask], ix[mask], np.full(mask.sum(), op, np.int8), np.full(mask.sum(), order, np.int8)))
    add(X < t, t - X, 0, 0)                 # t = x + y
    add(X > t, X - t, 1, 0)                 # t = x - y
    add(X <= L - t, X + t, 1, 1)            # t = y - x
    add(t % X == 0, t // X, 2, 0)           # t = x * y
    add(X % t == 0, X // t, 3, 0)           # t = x / y
    add(X <= L // t, X * t, 3, 1)           # t = y / x
    return tuple(np.concatenate([r[k] for r in res]) for k in range(4))

def _lookup(sorted_vals, q):
    pos = np.searchsorted(sorted_vals, q)
    pos[pos >= len(sorted_vals)] = len(sorted_vals) - 1
    return np.nonzero(sorted_vals[pos] == q)[0], pos

def search4(t, pool, L):
    """pool: dict value->reg. Returns an expression tree with exactly <=4 ops, or None. Assumes cheaper
    (<=3) synthesis was already excluded by the caller."""
    pv = list(pool); V = np.array(pv, dtype=np.int64)
    leaf = lambda k: ('r', pool[pv[k]])
    s1v, s1a, s1b, s1o = _combine(V, V, L)
    def e1(k): return (OPS[s1o[k]], leaf(s1a[k]), leaf(s1b[k]))
    # S2 = S1 op V and V op S1
    x2v, x2a, x2b, x2o = _combine(s1v, V, L)
    y2v, y2a, y2b, y2o = _combine(V, s1v, L)
    s2v = np.concatenate([x2v, y2v]); n1 = len(x2v)
    def e2(k):
        if k < n1: return (OPS[x2o[k]], e1(x2a[k]), leaf(x2b[k]))
        k -= n1; return (OPS[y2o[k]], leaf(y2a[k]), e1(y2b[k]))
    o2 = np.argsort(s2v, kind='stable'); s2s = s2v[o2]
    def mk(op, order, x, y):
        return (OPS[op], x, y) if order == 0 else (OPS[op], y, x)
    # (a) t = x op y, x in S1, y in S2
    y, ix, op, od = _needed(t, s1v, L)
    hit, pos = _lookup(s2s, y)
    if len(hit):
        h = hit[0]; return mk(op[h], od[h], e1(ix[h]), e2(o2[pos[h]]))
    # (b) t = v op z, z = w op y, y in S2
    z, iv, opz, odz = _needed(t, V, L)
    for zi in range(len(z)):
        zz = int(z[zi])
        if zz < 1: continue
        y, iw, op2, od2 = _needed(zz, V, L)
        hit, pos = _lookup(s2s, y)
        if len(hit):
            h = hit[0]
            inner = mk(op2[h], od2[h], leaf(iw[h]), e2(o2[pos[h]]))
            return mk(opz[zi], odz[zi], leaf(iv[zi]), inner)
    # (c) t = v op z, z = y1 op y2, y1, y2 in S1
    o1 = np.argsort(s1v, kind='stable'); s1s = s1v[o1]
    for zi in range(len(z)):
        zz = int(z[zi])
        if zz < 1: continue
        y, i1, op2, od2 = _needed(zz, s1v, L)
        hit, pos = _lookup(s1s, y)
        if len(hit):
            h = hit[0]
            inner = mk(op2[h], od2[h], e1(i1[h]), e1(o1[pos[h]]))
            return mk(opz[zi], odz[zi], leaf(iv[zi]), inner)
    return None
