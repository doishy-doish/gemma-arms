"""LPT schedule check for the K-pool canary runner (pure stdlib, runs anywhere).

Verifies the M380 wall arithmetic from full-file receipts:
- R11v3 solo walls (r11v3-table.json, 62 lines): 89.9 / 237.9 / 290.9 / 354.6 / 237.6 / 294.0
- serial sum = 1504.9s = 25.08min tasks; + T0 459.2s setup = 1975.4s = 32.9m total
- K=3 LPT makespan 532s x alpha 1.15 -> 612s = 10.2m, 2.46x
- K=6 makespan 354.6s x alpha 1.30 -> 461s ~= 462s = 7.7m, 3.26x
- K3M3: T0 + 3x612 = 2295s = 38.3m total, 12.8m/arm, 0.43 quota-h/arm
- K6M3: T0 + 3x461 = 1842s = 30.7m total, 10.3m/arm, 0.34 quota-h/arm

Usage: python3 k3_lpt.py  (exit 0 on PASS, exit 1 with diff on FAIL)
"""

WALLS = {
    "fastapi_14786": 89.9,
    "fastapi_13537": 237.9,
    "requests_7427": 290.9,
    "fastapi_15589": 354.6,
    "fastapi_13920": 237.6,
    "fastapi_14258": 294.0,
}

T0 = 459.2  # init 9.8 + wheels 52.1 + lock 33.5 + boot 363.8 (r11-log + r11v2-log, 39 lines each)
ALPHA_K3 = 1.15
ALPHA_K6 = 1.30


def lpt(walls, k):
    workers = [[] for _ in range(k)]
    loads = [0.0] * k
    for task_id, w in sorted(walls.items(), key=lambda kv: -kv[1]):
        i = min(range(k), key=lambda j: loads[j])
        workers[i].append((task_id, w))
        loads[i] += w
    return workers, loads


def check(cond, label, detail=""):
    print(("PASS " if cond else "FAIL ") + label + ((" :: " + detail) if detail else ""))
    return cond


def main():
    ok = True
    solo = sum(WALLS.values())
    ok &= check(abs(solo - 1504.9) < 0.2, "serial-sum", "%.1f == 1504.9" % solo)
    ok &= check(abs((solo + T0) - 1975.4) < 15.0, "total-with-T0",
                "%.1f + %.1f = %.1f (~1975.4s = 32.9m)" % (solo, T0, solo + T0))

    w3, loads3 = lpt(WALLS, 3)
    makespan3 = max(loads3)
    ok &= check(abs(makespan3 - 531.6) < 5.0, "K3-LPT-makespan",
                "loads=%s makespan=%.1f expect ~531.6" % (
                    ["%.1f" % v for v in loads3], makespan3))
    wall3 = makespan3 * ALPHA_K3
    ok &= check(abs(wall3 - 612.0) < 8.0, "K3-wall",
                "%.1f x %.2f = %.1f expect ~612s = 10.2m" % (makespan3, ALPHA_K3, wall3))
    ok &= check(abs(solo / wall3 - 2.46) < 0.05, "K3-speedup",
                "%.2f expect 2.46x" % (solo / wall3))

    w6, loads6 = lpt(WALLS, 6)
    makespan6 = max(loads6)
    ok &= check(abs(makespan6 - 354.6) < 1.0, "K6-LPT-makespan",
                "makespan=%.1f expect 354.6 (longest task)" % makespan6)
    wall6 = makespan6 * ALPHA_K6
    ok &= check(abs(wall6 - 461.0) < 6.0, "K6-wall",
                "%.1f x %.2f = %.1f expect ~461-462s = 7.7m" % (makespan6, ALPHA_K6, wall6))
    ok &= check(abs(solo / wall6 - 3.26) < 0.06, "K6-speedup",
                "%.2f expect 3.26x" % (solo / wall6))

    total_k3m3 = T0 + 3 * wall3
    eff_k3 = total_k3m3 / 3.0
    ok &= check(abs(total_k3m3 - 2295.0) < 30.0, "K3M3-total",
                "%.0fs = %.1fm expect ~38.3m" % (total_k3m3, total_k3m3 / 60.0))
    ok &= check(abs(eff_k3 / 60.0 - 12.8) < 0.3, "K3M3-per-arm",
                "%.1fm/arm expect 12.8" % (eff_k3 / 60.0))
    quota_k3 = (eff_k3 / 3600.0) * 2.0
    ok &= check(abs(quota_k3 - 0.43) < 0.03, "K3M3-quota",
                "%.2f quota-h/arm expect 0.43 (L4x4 2x)" % quota_k3)

    total_k6m3 = T0 + 3 * wall6
    eff_k6 = total_k6m3 / 3.0
    ok &= check(abs(total_k6m3 - 1842.0) < 30.0, "K6M3-total",
                "%.0fs = %.1fm expect ~30.7-30.8m" % (total_k6m3, total_k6m3 / 60.0))
    quota_k6 = (eff_k6 / 3600.0) * 2.0
    ok &= check(abs(quota_k6 - 0.34) < 0.03, "K6M3-quota",
                "%.2f quota-h/arm expect 0.34" % quota_k6)

    print("--- K3 assignment ---")
    for i, (tasks, load) in enumerate(zip(w3, loads3)):
        print("worker%d load=%.1f tasks=%s" % (
            i + 1, load, " + ".join("%s(%.1f)" % (t, w) for t, w in tasks)))
    print("K3-GATE-MATH %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
