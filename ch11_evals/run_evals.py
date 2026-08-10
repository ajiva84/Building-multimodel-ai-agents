"""Chapter 11 — golden-set runner. Wire this into deploy.sh as a gate."""
import json, glob, sys, argparse

def load_cases(folder):
    return [json.load(open(p)) for p in sorted(glob.glob(f"{folder}/*.json"))]

def run_case(case: dict) -> bool:
    """STUB: run your agent on case['input'], compare to case['expect']
    with code checks (exact fields, thresholds, must_flag...)."""
    raise NotImplementedError

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--set", default="golden")
    ap.add_argument("--runs", type=int, default=3)   # agents are dice
    ap.add_argument("--min-pass", type=float, default=0.85)
    a = ap.parse_args()

    cases = load_cases(a.set)
    total, passed = 0, 0
    for case in cases:
        for _ in range(a.runs):
            total += 1
            if run_case(case):
                passed += 1
    rate = passed / total if total else 0
    print(f"pass rate: {rate:.0%} ({passed}/{total})")
    sys.exit(0 if rate >= a.min_pass else 1)

if __name__ == "__main__":
    main()
