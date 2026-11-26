"""Joint cut: remove a shared helper value together with ALL its consumers and rebuild every consumer without
it (exact DAG search <= 4, depth 5 for big cones), each at its original position and into its original register.
Accept only a strictly shorter program that replays (check is the arbiter)."""
import sys
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from verify import check
from resynth import simulate
from dag4 import dag_search
from dag5 import dag5
from dagpass import emit_steps

def analyse(p, prog):
    snaps, srcs, vals = simulate(p, prog)
    N = len(prog); users = [[] for _ in range(N)]
    for n, (a, b) in enumerate(srcs):
        for s in {a, b}:
            if s >= 0: users[s].append(n)
    T = set(p['targets']); seen = set(p['start']); fc = set()
    for n, v in enumerate(vals):
        if v in T and v not in seen: fc.add(n)
        seen.add(v)
    last_read = {}
    for n in range(N):
        for s in srcs[n]: last_read[s] = n
    return snaps, srcs, vals, users, fc, last_read

def closure(roots, srcs, users, fc):
    cone = set(roots); ch = True
    while ch:
        ch = False
        for m in list(cone):
            for s in srcs[m]:
                if s >= 0 and s not in cone and s not in fc and all(u in cone for u in users[s]):
                    cone.add(s); ch = True
    return cone

def try_joint(p, prog, A, h, maxcost=5):
    snaps, srcs, vals, users, fc, last_read = A
    roots = sorted(set(users[h]))
    if len(roots) < 2 or h in fc: return None
    # every root must be "terminal enough": we rebuild roots, everything only they use goes too
    cone = closure(roots + [h], srcs, users, fc)
    if h not in cone: return None
    # roots that are read by instructions outside the cone must keep their register/value: fine (dest = orig)
    L = p['limit']; plan = {}; total_new = 0
    built = set()
    for n in roots:
        R, prod = snaps[n]
        pool = {}
        for r in range(48):
            if R[r] is not None and (prod[r] not in cone or prod[r] in built) and R[r] not in pool: pool[R[r]] = r
        own = closure([n], srcs, users, fc) - {h}
        cap = min(maxcost, 6)
        st = dag_search(vals[n], pool, L, min(4, cap))
        if st is None and cap >= 5: st = dag5(vals[n], pool, L)
        if st is None: return None
        plan[n] = (st, R, prod); total_new += len(st); built.add(n)
    if total_new >= len(cone): return None
    # splice
    cone_regs_dead = cone
    new = []
    for q, ins in enumerate(prog):
        if q in plan:
            st, R, prod = plan[q]; dest = ins[3]
            used = {x[1] for s in st for x in s[1:] if x[0] == 'r'}
            scratch = [r for r in range(48) if r != dest and r not in used and
                       (R[r] is None or (prod[r] in cone and prod[r] not in plan) or last_read.get(prod[r], -1) < q)]
            if len(scratch) < len(st) - 1: return None
            new += emit_steps(st, scratch, dest)
        elif q not in cone:
            new.append(ins)
    if len(new) < len(prog) and check(p, new)[0]: return new
    return None

def improve_joint(p, prog, _mc=5):
    while True:
        A = analyse(p, prog); hit = None
        for h in range(len(prog)):
            if len(set(A[3][h])) >= 2:
                hit = try_joint(p, prog, A, h)
                if hit: break
        if not hit: return prog
        prog = hit
