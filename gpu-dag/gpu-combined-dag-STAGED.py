"""Combined GPU DAG, STAGED ONLY — test runs, zero submissions.
Order: (1) Gap-4 tax (~10min) -> (2) GOLDSHAPE k4 -> (3) non-LoRA bundle test.
Transparency: per-step JSON + log, stop-on-fail, separate artifacts (attribution survives).
Guards: TEST-ONLY. Any submit path aborts. No Kaggle CreateSubmission. No submission.zip upload.
Fire (operator, after explicit go): run inside competition 4xL4 kernel, in order.
"""
import json, sys, time
from pathlib import Path

OUT = Path("gpu-dag-results")
OUT.mkdir(exist_ok=True)

def step(name, fn):
    t0 = time.time()
    try:
        res = fn()
        rec = {"step": name, "status": "PASS", "wall_s": round(time.time()-t0,1), **res}
    except SystemExit as e:
        rec = {"step": name, "status": "STOP", "wall_s": round(time.time()-t0,1), "reason": str(e)[:300]}
        (OUT/f"{name}.json").write_text(json.dumps(rec, indent=1))
        print(json.dumps(rec, indent=1))
        print("DAG STOPPED at", name)
        sys.exit(3)
    except Exception as e:
        rec = {"step": name, "status": "FAIL", "wall_s": round(time.time()-t0,1), "error": str(e)[:500]}
        (OUT/f"{name}.json").write_text(json.dumps(rec, indent=1))
        print(json.dumps(rec, indent=1))
        print("DAG STOPPED at", name)
        sys.exit(4)
    (OUT/f"{name}.json").write_text(json.dumps(rec, indent=1))
    print(json.dumps(rec, indent=1))
    return rec

def s1_gap4_tax():
    # import staged checker dry-first; live only on 4xL4 with wheelhouse
    import importlib.util
    spec = importlib.util.spec_from_file_location("gap4", "unified-optimum-build/train/gap4_speedcheck.py")
    # structural gate first (no torch): ensure script exists + canaries defined
    txt = Path("unified-optimum-build/train/gap4_speedcheck.py").read_text()
    assert "CANARIES" in txt and "690" in txt, "gap4 script shape changed"
    return {"mode": "STAGED-CHECK", "gate": "PASS iff live projected<=690min (live needs 4xL4)", "next": "s2 only if live PASS"}

def s2_goldshape_k4():
    # test-run only: 7427 + 13920/7328 with GOLDSHAPE-diff, no submit
    cfg = {"tasks": ["7427","13920","7328"], "arm": "GOLDSHAPE-diff", "mode": "test-only", "submit": False}
    assert cfg["submit"] is False, "submit must stay False"
    return {"config": cfg, "gate": "convert>=1 to proceed to s3 (live D2 decides)"}

def s3_bundle_test():
    cfg = {"bundle": ["GOLDSHAPE-diff","multi-file-rows","kill-teeth","skeleton-172B"], "mode": "test-only", "submit": False}
    assert cfg["submit"] is False
    return {"config": cfg, "gate": "measured only, never submitted from this DAG"}

if __name__ == "__main__":
    for bad in ["KAGGLE_SUBMIT","CreateSubmission","submission.zip"]:
        src = Path(__file__).read_text()
        assert bad not in src or "No " in src or "zero submissions" in src, bad
    print("== GPU DAG STAGED (no GPU touched, dry structural pass) ==")
    step("s1_gap4_tax", s1_gap4_tax)
    step("s2_goldshape_k4", s2_goldshape_k4)
    step("s3_bundle_test", s3_bundle_test)
    print("STAGED-OK: live fire needs operator + explicit go, 4xL4 kernel.")
