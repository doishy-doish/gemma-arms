"""stats.py — frozen paper statistics (pre-registered 2026-11-08).

Wilson 95% interval (z=1.96) and same-task paired McNemar exact
(conditional binomial, standard one-sided + doubled two-sided).
Only the decision-line comparisons in PRE-REG.md may cite these.
"""
import math

Z = 1.96


def wilson(k, n, z=Z):
    """Return (lo, hi) Wilson score interval for k successes in n trials."""
    if n == 0:
        return (0.0, 1.0)
    p = k / n
    denom = 1.0 + z * z / n
    center = (p + z * z / (2.0 * n)) / denom
    half = z * math.sqrt(p * (1.0 - p) / n + z * z / (4.0 * n * n)) / denom
    return (max(0.0, center - half), min(1.0, center + half))


def mcnemar_exact(b, c):
    """Discordant pairs: b = arm-only solves, c = rival-only solves.

    Returns (p_standard_one_sided, p_doubled_two_sided). Doubling capped at 1.
    n=0 (no discordants) -> (1.0, 1.0): arms identical, nothing to claim.
    """
    n = b + c
    if n == 0:
        return (1.0, 1.0)
    k = min(b, c)
    tail = sum(math.comb(n, i) for i in range(k + 1)) / 2.0 ** n
    return (tail, min(1.0, 2.0 * tail))


FAILURE_PRECEDENCE = [
    "resolved",
    "context_overflow",
    "budget_truncation",
    "session_timeout",
    "patch_failed_tests",
    "abandoned_no_patch",
]


def classify(resolved, overflow=False, truncated=False, timed_out=False,
             patch_nonempty=False):
    if resolved:
        return "resolved"
    if overflow:
        return "context_overflow"
    if truncated:
        return "budget_truncation"
    if timed_out:
        return "session_timeout"
    if patch_nonempty:
        return "patch_failed_tests"
    return "abandoned_no_patch"


if __name__ == "__main__":
    # Self-test vectors (must print exact values; notebook asserts them).
    print("wilson(0,10) =", wilson(0, 10))
    print("wilson(2,10) =", wilson(2, 10))
    print("mcnemar(1,1) =", mcnemar_exact(1, 1))
    print("mcnemar(7,0) =", mcnemar_exact(7, 0))
    print("mcnemar(0,0) =", mcnemar_exact(0, 0))
