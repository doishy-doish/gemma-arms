"""Exact local re-synthesis of targets.

For every target-producing instruction, take its exclusive dependency cone (instructions used only to
build that target and covering no other target first). If the target can be built in fewer instructions
(depth <= 3) from the values that are in the registers at that point, splice the shorter sequence in,
using only dead registers as scratch, and accept it only if the full program replays correctly.
"""
import json, sys
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from verify import check

OPS = '+-*/'

def apply(op, a, b, L):
    if op == '+': v = a + b
    elif op == '-':
        if a <= b: return None
        v = a - b
    elif op == '*': v = a * b
    else:
        if a % b: return None
        v = a // b
    return v if v <= L else None

def simulate(p, prog):
    R = [None] * 48; prod = [None] * 48
    for k, v in enumerate(p['start']): R[k] = v; prod[k] = -1 - k
    snaps = []; srcs = []; vals = []
    for n, (op, i, j, d) in enumerate(prog):
        snaps.append((R[:], prod[:]))
        srcs.append((prod[i], prod[j]))
        v = apply(op, R[i], R[j], p['limit']); vals.append(v)
        R[d] = v; prod[d] = n
    return snaps, srcs, vals

def inverse_needed(t, a, L):
    """Yield (op, order, c) such that t = a op c (order 0) or t = c op a (order 1)."""
    if t > a: yield ('+', 0, t - a)
    if a > t: yield ('-', 0, a - t)
    if t + a <= L: yield ('-', 1, t + a)
    if t % a == 0: yield ('*', 0, t // a)
    if a % t == 0: yield ('/', 0, a // t)
    if t * a <= L: yield ('/', 1, t * a)

def search(t, pool, L, maxcost):
    """pool: dict value -> register. Returns list of (op, x, y) expression trees or None.
    Expression nodes: ('r', reg) leaf or (op, left, right)."""
    vals = list(pool)
    leaf = lambda v: ('r', pool[v])
    # cost 1
    for a in vals:
        for op, order, c in inverse_needed(t, a, L):
            if c in pool:
                return (op, leaf(a), leaf(c)) if order == 0 else (op, leaf(c), leaf(a))
    if maxcost < 2: return None
    S1 = {}
    for x in vals:
        for y in vals:
            for op in OPS:
                v = apply(op, x, y, L)
                if v is not None and v not in pool and v not in S1: S1[v] = (op, leaf(x), leaf(y))
    if t in S1: return S1[t]
    for a in vals:
        for op, order, c in inverse_needed(t, a, L):
            if c in S1:
                return (op, leaf(a), S1[c]) if order == 0 else (op, S1[c], leaf(a))
    if maxcost < 3: return None
    # cost 3a: t = c1 op c2, c1,c2 in S1
    for c1, e1 in S1.items():
        for op, order, c2 in inverse_needed(t, c1, L):
            if c2 in S1:
                return (op, e1, S1[c2]) if order == 0 else (op, S1[c2], e1)
    # cost 3b: t = a op (b op c'), c' in S1
    for a in vals:
        for op, order, c in inverse_needed(t, a, L):
            for b in vals:
                for op2, order2, c2 in inverse_needed(c, b, L):
                    if c2 in S1:
                        inner = (op2, leaf(b), S1[c2]) if order2 == 0 else (op2, S1[c2], leaf(b))
                        return (op, leaf(a), inner) if order == 0 else (op, inner, leaf(a))
    return None

def size(e):
    return 0 if e[0] == 'r' else 1 + size(e[1]) + size(e[2])

def emit(e, scratch, dest, out):
    """Emit instructions; returns register holding the value. Shared subtrees are recomputed (counted by size)."""
    if e[0] == 'r': return e[1]
    a = emit(e[1], scratch, None, out); b = emit(e[2], scratch, None, out)
    d = dest if dest is not None else scratch.pop()
    out.append([e[0], a, b, d])
    return d

def improve_once(p, prog, maxcost=3):
    snaps, srcs, vals = simulate(p, prog)
    N = len(prog)
    users = [[] for _ in range(N)]
    for n, (s1, s2) in enumerate(srcs):
        for s in (s1, s2):
            if s >= 0: users[s].append(n)
    T = set(p['targets']); seen = set(p['start']); firstcover = set(); covers_of = {}
    for n, v in enumerate(vals):
        if v in T and v not in seen: firstcover.add(n)
        seen.add(v)
    # liveness: is the value held in register r just before instruction n read later?
    # live_after[n] = set of producers read at or after n
    last_read = {}
    for n in range(N):
        for s in srcs[n]: last_read[s] = n
    L = p['limit']
    cands = sorted(firstcover, key=lambda n: -n)
    for n in cands:
        cone = {n}; changed = True
        while changed:
            changed = False
            for m in list(cone):
                for s in srcs[m]:
                    if s >= 0 and s not in cone and s not in firstcover and all(u in cone for u in users[s]):
                        cone.add(s); changed = True
        k = len(cone)
        if k < 2: continue
        R, prod = snaps[n]
        cone_regs = {prog[m][3] for m in cone if m != n}
        # pool: registers before n whose producer is not in the cone
        pool = {}
        for r in range(48):
            if R[r] is not None and prod[r] not in cone and R[r] not in pool: pool[R[r]] = r
        t = vals[n]
        e = search(t, pool, L, min(maxcost, k - 1))
        if e is None: continue
        c = size(e)
        if c >= k: continue
        dest = prog[n][3]
        # scratch: registers whose current value (producer prod[r]) is never read at/after n, or cone-held
        scratch = [r for r in range(48) if r != dest and
                   (R[r] is None or prod[r] in cone or last_read.get(prod[r], -1) < n)
                   and r not in {x[1] for x in leaves(e)}]
        if len(scratch) < c - 1: continue
        out = []
        emit(e, scratch, dest, out)
        new = [ins for m, ins in enumerate(prog[:n]) if m not in cone] + out + prog[n + 1:]
        ok, _ = check(p, new)
        if ok and len(new) < len(prog):
            return new
    return None

def leaves(e):
    if e[0] == 'r': return [e]
    return leaves(e[1]) + leaves(e[2])

def improve(p, prog, maxcost=3):
    while True:
        new = improve_once(p, prog, maxcost)
        if new is None: return prog
        prog = new


def improve_move_once(p, prog, maxcost=3):
    """Leaf targets (value never read again): delete the exclusive cone and rebuild the target at the
    position (0..N) where it is cheapest. Accept only a strictly shorter program that replays."""
    snaps, srcs, vals = simulate(p, prog)
    N = len(prog)
    R = [None] * 48; prod = [None] * 48
    for k, v in enumerate(p['start']): R[k] = v; prod[k] = -1 - k
    for n, (op, i, j, d) in enumerate(prog): R[d] = vals[n]; prod[d] = n
    snaps = snaps + [(R, prod)]
    users = [[] for _ in range(N)]
    for n, (s1, s2) in enumerate(srcs):
        for s in (s1, s2):
            if s >= 0: users[s].append(n)
    T = set(p['targets']); seen = set(p['start']); firstcover = set()
    for n, v in enumerate(vals):
        if v in T and v not in seen: firstcover.add(n)
        seen.add(v)
    last_read = {}
    for n in range(N):
        for s in srcs[n]: last_read[s] = n
    L = p['limit']
    for n in sorted(firstcover):
        if users[n]: continue
        cone = {n}; changed = True
        while changed:
            changed = False
            for m in list(cone):
                for s in srcs[m]:
                    if s >= 0 and s not in cone and s not in firstcover and all(u in cone for u in users[s]):
                        cone.add(s); changed = True
        k = len(cone)
        t = vals[n]
        best = None
        for m in range(N + 1):
            Rm, pm = snaps[m]
            pool = {}
            for r in range(48):
                if Rm[r] is not None and pm[r] not in cone and Rm[r] not in pool: pool[Rm[r]] = r
            if t in pool: continue  # cannot happen for a first cover unless duplicate; skip
            lim = min(maxcost, k - 1) if best is None else min(maxcost, best[0] - 1)
            if lim < 1: break
            e = search(t, pool, L, lim)
            if e is None: continue
            c = size(e)
            if c >= k or (best and c >= best[0]): continue
            lv = {x[1] for x in leaves(e)}
            scratch = [r for r in range(48) if r not in lv and
                       (Rm[r] is None or pm[r] in cone or last_read.get(pm[r], -1) < m)]
            if len(scratch) < c: continue
            out = []
            dest = scratch.pop(0)
            emit(e, scratch, dest, out)
            new = [ins for q, ins in enumerate(prog[:m]) if q not in cone] + out + \
                  [ins for q, ins in enumerate(prog[m:], start=m) if q not in cone]
            ok, _ = check(p, new)
            if ok and len(new) < len(prog):
                best = (c, new)
        if best: return best[1]
    return None


def improve_all(p, prog, maxcost=3):
    while True:
        new = improve_once(p, prog, maxcost) or improve_move_once(p, prog, maxcost)
        if new is None: return prog
        prog = new


def improve_deep_once(p, prog, mincone=5):
    """Like improve_once but tries the exact 4-op search for cones of size >= mincone."""
    from deep4 import search4
    snaps, srcs, vals = simulate(p, prog)
    N = len(prog)
    users = [[] for _ in range(N)]
    for n, (s1, s2) in enumerate(srcs):
        for s in (s1, s2):
            if s >= 0: users[s].append(n)
    T = set(p['targets']); seen = set(p['start']); firstcover = set()
    for n, v in enumerate(vals):
        if v in T and v not in seen: firstcover.add(n)
        seen.add(v)
    last_read = {}
    for n in range(N):
        for s in srcs[n]: last_read[s] = n
    L = p['limit']
    for n in sorted(firstcover, key=lambda n: -n):
        cone = {n}; changed = True
        while changed:
            changed = False
            for m in list(cone):
                for s in srcs[m]:
                    if s >= 0 and s not in cone and s not in firstcover and all(u in cone for u in users[s]):
                        cone.add(s); changed = True
        k = len(cone)
        if k < mincone: continue
        R, prod = snaps[n]
        pool = {}
        for r in range(48):
            if R[r] is not None and prod[r] not in cone and R[r] not in pool: pool[R[r]] = r
        t = vals[n]
        e = search(t, pool, L, min(3, k - 1)) or search4(t, pool, L)
        if e is None or size(e) >= k: continue
        c = size(e); dest = prog[n][3]
        lv = {x[1] for x in leaves(e)}
        scratch = [r for r in range(48) if r != dest and r not in lv and
                   (R[r] is None or prod[r] in cone or last_read.get(prod[r], -1) < n)]
        if len(scratch) < c - 1: continue
        out = []; emit(e, scratch, dest, out)
        new = [ins for m, ins in enumerate(prog[:n]) if m not in cone] + out + prog[n + 1:]
        ok, _ = check(p, new)
        if ok and len(new) < len(prog): return new
    return None


def improve_deep(p, prog, _mc=4):
    while True:
        new = improve_deep_once(p, prog)
        if new is None: return prog
        prog = new
