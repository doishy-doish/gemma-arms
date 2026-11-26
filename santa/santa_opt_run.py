"""Santa optimizer — runs asterios exact passes on our_base.
Loads santa/puzzles.csv + santa/our_base.csv, runs:
  DCE -> resynth improve (maxcost 3) -> suffix -> dagpass (maxcost 4) -> jointcut
Each pass keeps iff valid AND strictly shorter (check() arbiter).
Writes santa/best_new.csv + prints TOTAL + gain. Uploaded as artifact.
"""
import sys, os, csv, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
from verify import load_puzzles, check
import resynth
import suffix as suffix_mod
import dagpass
import jointcut

def load_sub(path):
    S = {}
    with open(path, newline='', encoding='utf-8') as f:
        for r in csv.DictReader(f):
            S[r['id']] = json.loads(r['program'])
    return S

def write_sub(path, P, S):
    with open(path, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['id', 'program'])
        for pid in sorted(P.keys()):
            cell = json.dumps(S[pid], separators=(',', ':'))
            assert len(cell.encode()) <= 131072, pid
            w.writerow([pid, cell])

def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('--puzzles', default='santa/puzzles.csv')
    ap.add_argument('--base', default='santa/our_base.csv')
    ap.add_argument('--out', default='/tmp/santa_best_new.csv')
    ap.add_argument('--only', default='', help='comma-separated puzzle ids (default all)')
    ap.add_argument('--passes', default='resynth,suffix,dag,joint', help='comma list')
    args = ap.parse_args()

    P = load_puzzles(args.puzzles)
    S = load_sub(args.base)
    ids = [x.strip() for x in args.only.split(',') if x.strip()] if args.only else sorted(P.keys())
    passes = [x.strip() for x in args.passes.split(',') if x.strip()]

    base_total = sum(len(S[pid]) for pid in P)
    print(f'BASE total={base_total} puzzles={len(P)} focus={len(ids)} passes={passes}', flush=True)

    cur = {pid: S[pid] for pid in P}
    for pid in ids:
        p = {'start': P[pid]['start'], 'targets': P[pid]['targets'], 'limit': P[pid]['limit'], 'regs': P[pid]['regs']}
        prog = cur[pid]
        # DCE first (via resynth simulate? use dagpass cones? simple: run resynth improve which includes cone logic)
        try:
            if 'resynth' in passes:
                prog = resynth.improve(p, prog, 3)
            if 'suffix' in passes:
                prog = suffix_mod.improve_suffix(p, prog)
            if 'dag' in passes:
                prog = dagpass.improve_dag(p, prog)
                prog = dagpass.improve_dag5(p, prog)
            if 'joint' in passes:
                prog = jointcut.improve_joint(p, prog)
            # final resynth polish
            if 'resynth' in passes:
                prog = resynth.improve(p, prog, 3)
        except Exception as e:
            print(f'{pid} ERROR {type(e).__name__}: {e}', flush=True)
            prog = cur[pid]
        ok, msg = check(p, prog)
        if not ok:
            print(f'{pid} INVALID after opt ({msg}) — keeping base', flush=True)
            prog = cur[pid]
        if len(prog) < len(cur[pid]):
            print(f'{pid} WIN {len(cur[pid])}->{len(prog)} (-{len(cur[pid])-len(prog)})', flush=True)
            cur[pid] = prog

    new_total = sum(len(cur[pid]) for pid in P)
    print(f'NEW total={new_total} gain={base_total-new_total}', flush=True)
    write_sub(args.out, P, cur)
    # verify written file
    S2 = load_sub(args.out)
    tot2, bad = 0, 0
    for pid in P:
        ok, _ = check({'start': P[pid]['start'], 'targets': P[pid]['targets'], 'limit': P[pid]['limit'], 'regs': P[pid]['regs']}, S2[pid])
        if not ok:
            bad += 1
        tot2 += len(S2[pid])
    print(f'VERIFY out={args.out} total={tot2} bad={bad}', flush=True)
    assert bad == 0, f'{bad} invalid programs in output'
    # write total to step summary location if present
    gh_out = os.environ.get('GITHUB_OUTPUT')
    if gh_out:
        with open(gh_out, 'a') as f:
            f.write(f'new_total={new_total}\n')
            f.write(f'gain={base_total-new_total}\n')

if __name__ == '__main__':
    main()
