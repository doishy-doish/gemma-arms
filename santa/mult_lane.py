"""Multiplier-lane rewrite: pay for one multiplier m once, rebuild many targets through it.
For each candidate m (program values + small ints + powers of two):
  cost(m) = search(m, pool0) or None (skip if m already in pool0 with cost 0)
  for each target t: cost(t | pool0+{m}) via resynth.search (<=3)
  total = cost(m) + sum(costs); accept iff total < current total for those targets
        AND full program replays (check arbiter).
Splice: build m once at best position, rebuild each target cone through m.
This is a Python port of the Atakan multiplier-lanes idea (paid multiplier, shared).
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from verify import check
from resynth import apply, search, size, emit, leaves, simulate

def pool_from_reg(R, prod, cone):
    pool = {}
    for r in range(48):
        if R[r] is not None and prod[r] not in cone and R[r] not in pool:
            pool[R[r]] = r
    return pool

def try_multiplier(p, prog, m_val):
    L = p['limit']
    # find cheapest way to build m from starts (pool0 = starts)
    pool0 = {}
    for k, v in enumerate(p['start']):
        if v not in pool0:
            pool0[v] = k
    if m_val in pool0:
        m_cost_e = None
        m_cost = 0
    else:
        m_cost_e = search(m_val, pool0, L, 3)
        if m_cost_e is None:
            return None
        m_cost = size(m_cost_e)
        if m_cost == 0:
            m_cost_e = None
            m_cost = 0
    # for each firstcover target, cost with and without m
    snaps, srcs, vals = simulate(p, prog)
    N = len(prog)
    from collections import defaultdict
    users = [[] for _ in range(N)]
    for n, (s1, s2) in enumerate(srcs):
        for s in (s1, s2):
            if s >= 0:
                users[s].append(n)
    T = set(p['targets'])
    seen = set(p['start'])
    firstcover = []
    for n, v in enumerate(vals):
        if v in T and v not in seen:
            firstcover.append((n, v))
        if v is not None:
            seen.add(v)
    # baseline: current cone sizes for each firstcover (exclusive cone)
    total_save = 0
    plans = []
    # pool at each n includes m (assume m built before all targets; approximate with starts+m+early targets)
    # simple: pool_m = pool0 + {m: reg} + {t for earlier targets}
    # iterate in order, growing pool
    pool_m_base = dict(pool0)
    if m_val not in pool_m_base:
        pool_m_base[m_val] = 48  # placeholder reg
    for n, t in firstcover:
        R, prod = snaps[n]
        # current exclusive cone size
        cone = {n}
        ch = True
        fcset = {nn for nn, _ in firstcover}
        while ch:
            ch = False
            for mm in list(cone):
                for s in srcs[mm]:
                    if s >= 0 and s not in cone and s not in fcset and all(u in cone for u in users[s]):
                        cone.add(s)
                        ch = True
        k = len(cone)
        # cost without m (from live pool)
        pool_live = {}
        for r in range(48):
            if R[r] is not None and prod[r] not in cone and R[r] not in pool_live:
                pool_live[R[r]] = r
        # cost with m: pool_live + m
        pool_with = dict(pool_live)
        if m_val not in pool_with:
            pool_with[m_val] = -99
        e_with = search(t, pool_with, L, 3)
        c_with = size(e_with) if e_with is not None else 99
        if c_with < k:
            total_save += (k - c_with)
            plans.append((n, t, cone, e_with, c_with, k))
    if total_save <= m_cost or not plans:
        return None
    # splice: build m at start (after starts), then rebuild each planned target in order
    # simplest correct splice: rebuild whole program greedily is complex; instead do sequential single-target splices
    # using improve_once logic with pool forced to contain m. Do one target at a time, best saving first.
    plans.sort(key=lambda x: (x[5] - x[4]), reverse=True)
    cur = prog
    # ensure m exists in program: if not in starts, prepend its construction (via search from starts)
    if m_val not in p['start']:
        if m_cost_e is None:
            return None
        # emit m construction at beginning (regs: use high regs, then check)
        # find free regs: use 40..47 (assume free early; check() will catch collisions via overwrite semantics?
        # overwriting early regs is safe if they are dead after? To stay safe, build m, then rebuild targets.
        # We do: new = emit(m) + cur, with dest reg 47, scratch 40..46. Then run single-target splices.
        # If m construction overwrites a live start reg, check() still passes? Overwriting starts is allowed
        # (regs can be reused), but later reads of that start would break. Use highest regs to minimize risk,
        # then verify with check(); if invalid, abort this m.
        out = []
        scratch = [40, 41, 42, 43, 44, 45, 6-6+46]  # 40..46
        # emit needs scratch stack + dest; dest 47
        # leaves of m_cost_e reference pool0 regs (starts) — safe
        tmp = []
        # copy emit logic (avoid importing emit with reg assumptions)
        def _emit(e, scr, dest, o):
            if e[0] == 'r':
                return e[1]
            a = _emit(e[1], scr, None, o)
            b = _emit(e[2], scr, None, o)
            d = dest if dest is not None else scr.pop()
            o.append([e[0], a, b, d])
            return d
        _emit(m_cost_e, scratch[:], 47, tmp)
        cur = tmp + cur
        ok, _ = check(p, cur)
        if not ok:
            return None
    # now for each plan (recompute indices as program grew — instead re-run resynth improve with m pinned?
    # simplest: run standard improve_once loop; m is now in program so search will use it naturally.
    import resynth as Rmod
    for _ in range(5):
        nxt = Rmod.improve_once(p, cur, 3)
        if nxt is None or len(nxt) >= len(cur):
            break
        cur = nxt
    if len(cur) < len(prog):
        ok, _ = check(p, cur)
        if ok:
            return cur
    return None

def improve_mult(p, prog):
    best = prog
    # candidates: program values (first 40) + small ints + powers of two within limit
    cands = set()
    snaps, _, vals = simulate(p, prog)
    for v in vals[:200]:
        if v is not None and 2 <= v <= p['limit']:
            cands.add(v)
    for v in list(range(2, 64)) + [100, 128, 256, 1000, 1024]:
        if v <= p['limit']:
            cands.add(v)
    # prefer candidates dividing many targets
    T = [t for t in p['targets'] if t not in p['start']]
    def score(m):
        s = 0
        for t in T:
            if t % m == 0:
                s += 2
            elif (t - 1) % m == 0 or (t + 1) % m == 0:
                s += 1
        return s
    ranked = sorted(cands, key=lambda m: (-score(m), m))[:40]
    for m in ranked:
        try:
            nxt = try_multiplier(p, best, m)
        except Exception:
            continue
        if nxt is not None and len(nxt) < len(best):
            best = nxt
    return best
