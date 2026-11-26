"""Pass: for each target, rebuild its exclusive cone with the DAG-aware exact search (<= 4 steps)."""
import sys
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from verify import check
from resynth import simulate
from dag4 import dag_search

def cones(p, prog):
    snaps, srcs, vals = simulate(p, prog)
    N = len(prog)
    users = [[] for _ in range(N)]
    for n, (s1, s2) in enumerate(srcs):
        for s in (s1, s2):
            if s >= 0: users[s].append(n)
    T = set(p['targets']); seen = set(p['start']); fc = set()
    for n, v in enumerate(vals):
        if v in T and v not in seen: fc.add(n)
        seen.add(v)
    last_read = {}
    for n in range(N):
        for s in srcs[n]: last_read[s] = n
    out = []
    for n in sorted(fc, key=lambda n: -n):
        cone = {n}; ch = True
        while ch:
            ch = False
            for m in list(cone):
                for s in srcs[m]:
                    if s >= 0 and s not in cone and s not in fc and all(u in cone for u in users[s]):
                        cone.add(s); ch = True
        out.append((n, cone))
    return snaps, vals, last_read, out

def emit_steps(steps, scratch, dest):
    regs = []; out = []
    for k, (op, x, y) in enumerate(steps):
        rx = x[1] if x[0] == 'r' else regs[x[1]]
        ry = y[1] if y[0] == 'r' else regs[y[1]]
        d = dest if k == len(steps) - 1 else scratch.pop()
        out.append([op, rx, ry, d]); regs.append(d)
    return out

def improve_dag_once(p, prog, maxcost=4):
    snaps, vals, last_read, cl = cones(p, prog)
    L = p['limit']
    for n, cone in cl:
        k = len(cone)
        if k < 2: continue
        R, prod = snaps[n]
        pool = {}
        for r in range(48):
            if R[r] is not None and prod[r] not in cone and R[r] not in pool: pool[R[r]] = r
        steps = dag_search(vals[n], pool, L, min(maxcost, k - 1))
        if steps is None or len(steps) >= k: continue
        dest = prog[n][3]
        used = {x[1] for st in steps for x in st[1:] if x[0] == 'r'}
        scratch = [r for r in range(48) if r != dest and r not in used and
                   (R[r] is None or prod[r] in cone or last_read.get(prod[r], -1) < n)]
        if len(scratch) < len(steps) - 1: continue
        seg = emit_steps(steps, scratch, dest)
        new = [ins for m, ins in enumerate(prog[:n]) if m not in cone] + seg + prog[n + 1:]
        if check(p, new)[0] and len(new) < len(prog): return new
    return None

def improve_dag(p, prog, _mc=4):
    while True:
        new = improve_dag_once(p, prog)
        if new is None: return prog
        prog = new


def improve_dag5_once(p, prog, mincone=6):
    from dag5 import dag5
    snaps, vals, last_read, cl = cones(p, prog)
    L = p['limit']
    for n, cone in cl:
        k = len(cone)
        if k < mincone: continue
        R, prod = snaps[n]
        pool = {}
        for r in range(48):
            if R[r] is not None and prod[r] not in cone and R[r] not in pool: pool[R[r]] = r
        steps = dag_search(vals[n], pool, L, 4) or dag5(vals[n], pool, L)
        if steps is None or len(steps) >= k: continue
        dest = prog[n][3]
        used = {x[1] for st in steps for x in st[1:] if x[0] == 'r'}
        scratch = [r for r in range(48) if r != dest and r not in used and
                   (R[r] is None or prod[r] in cone or last_read.get(prod[r], -1) < n)]
        if len(scratch) < len(steps) - 1: continue
        seg = emit_steps(steps, scratch, dest)
        new = [ins for m, ins in enumerate(prog[:n]) if m not in cone] + seg + prog[n + 1:]
        if check(p, new)[0] and len(new) < len(prog): return new
    return None

def improve_dag5(p, prog, _mc=5):
    while True:
        new = improve_dag5_once(p, prog)
        if new is None: return prog
        prog = new


def improve_pos_once(p, prog, maxcost=5, use5=True):
    """For each target cone, try every insertion position m in [first cone instr, n]: pool = registers at m
    (excluding cone values), scratch = registers dead at m, dest = original destination. The full replay
    (check) is the acceptance test."""
    from dag5 import dag5
    snaps, vals, last_read, cl = cones(p, prog)
    L = p['limit']
    for n, cone in cl:
        k = len(cone)
        if k < 2: continue
        m0 = min(cone); dest = prog[n][3]
        for m in range(n, m0 - 1, -1):
            R, prod = snaps[m]
            pool = {}
            for r in range(48):
                if R[r] is not None and prod[r] not in cone and R[r] not in pool: pool[R[r]] = r
            steps = dag_search(vals[n], pool, L, min(4, k - 1))
            if steps is None and use5 and k >= 6: steps = dag5(vals[n], pool, L)
            if steps is None or len(steps) >= k: continue
            used = {x[1] for st in steps for x in st[1:] if x[0] == 'r'}
            scratch = [r for r in range(48) if r != dest and r not in used and
                       (R[r] is None or prod[r] in cone or last_read.get(prod[r], -1) < m)]
            if len(scratch) < len(steps) - 1: continue
            seg = emit_steps(steps, scratch, dest)
            new = [ins for q, ins in enumerate(prog[:m]) if q not in cone] + seg + \
                  [ins for q, ins in enumerate(prog[m:], start=m) if q not in cone]
            if check(p, new)[0] and len(new) < len(prog): return new
    return None

def improve_pos(p, prog, _mc=5):
    while True:
        new = improve_pos_once(p, prog)
        if new is None: return prog
        prog = new
