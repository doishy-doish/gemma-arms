"""Suffix re-planning: keep the program prefix, rebuild the remaining targets greedily
(cheapest-first, exact search of depth <= 4 from the live registers). Accept only if shorter and valid."""
import sys
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from verify import check
from resynth import apply, search, size, leaves, emit
from deep4 import search4

def run_prefix(p, prog):
    R = [None] * 48
    for k, v in enumerate(p['start']): R[k] = v
    seen = set(p['start'])
    for op, i, j, d in prog:
        R[d] = apply(op, R[i], R[j], p['limit']); seen.add(R[d])
    return R, seen

def cost_of(t, pool, L, cap):
    e = search(t, pool, L, min(3, cap))
    if e is None and cap >= 4: e = search4(t, pool, L)
    return e

def replan(p, prog, m, budget):
    L = p['limit']; T = set(p['targets'])
    R, seen = run_prefix(p, prog[:m])
    rem = sorted(T - seen)
    out = []; last_use = [0 if v is not None else -1 for v in R]; clock = 1
    tgt_reg = set(r for r in range(48) if R[r] in T)
    while rem:
        pool = {}
        for r in range(48):
            if R[r] is not None and R[r] not in pool: pool[R[r]] = r
        best = None
        for t in rem:
            e = cost_of(t, pool, L, 4 if best is None else min(4, size(best[1]) - 1))
            if e is not None and (best is None or size(e) < size(best[1])): best = (t, e)
            if best and size(best[1]) == 1: break
        if best is None: return None
        t, e = best
        c = size(e); lv = {x[1] for x in leaves(e)}
        free = [r for r in range(48) if R[r] is None]
        evict = sorted((r for r in range(48) if R[r] is not None and r not in lv and r not in free),
                       key=lambda r: (r in tgt_reg, last_use[r]))
        regs = (free + evict)[:c]
        if len(regs) < c: return None
        dest = regs[0]; scratch = list(reversed(regs[1:]))
        seg = []; emit(e, scratch, dest, seg)
        for op, i, j, d in seg:
            last_use[i] = last_use[j] = clock
            R[d] = apply(op, R[i], R[j], L); last_use[d] = clock; clock += 1
            if R[d] in T: tgt_reg.add(d)
            else: tgt_reg.discard(d)
            if R[d] in rem: rem.remove(R[d])
        out += seg
        if m + len(out) >= budget: return None
    new = prog[:m] + out
    return new if check(p, new)[0] else None

def improve_suffix(p, prog, ks=(2, 3, 4, 6, 8, 10, 14)):
    T = set(p['targets']); seen = set(p['start']); firsts = []
    R = [None] * 48
    for k, v in enumerate(p['start']): R[k] = v
    for n, (op, i, j, d) in enumerate(prog):
        R[d] = apply(op, R[i], R[j], p['limit'])
        if R[d] in T and R[d] not in seen: firsts.append(n)
        seen.add(R[d])
    best = prog
    for k in ks:
        if k > len(firsts): break
        # cut right after the instruction that covered the (k+1)-th last target
        m = firsts[-k - 1] + 1 if k < len(firsts) else 0
        new = replan(p, best[:m] if best is prog else prog[:m], m, len(best))
        if new is not None and len(new) < len(best): best = new
    return best
