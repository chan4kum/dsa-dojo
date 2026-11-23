"""Check a learner-provided D03 mini-library with the Dojo test engine."""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from core import run_problem  # noqa: E402

PROBLEMS = (
    {
        "fn": "first_unique_index",
        "tests": [
            (("",), -1),
            (("swiss",), 1),
            (("aabb",), -1),
            (("éaé",), 1),
        ],
    },
    {
        "fn": "count_subarrays",
        "tests": [
            (([], 0), 0),
            (([1, -1, 0], 0), 3),
            (([0, 0, 0], 0), 6),
            (([2, 1, 2], 3), 2),
            (([2**60, 1, -(2**60)], 1), 2),
        ],
    },
    {
        "fn": "lru_misses",
        "tests": [
            (([], 2), 0),
            ((["a", "a"], 0), 2),
            ((["a", "b", "a", "c", "b"], 2), 4),
            ((["a", "b", "a", "b"], 2), 2),
            ((["a", "b", "a"], 1), 3),
        ],
    },
)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("submission", type=Path)
    args = parser.parse_args()
    source = args.submission.read_text(encoding="utf-8")
    passed = total = 0
    for problem in PROBLEMS:
        print(problem["fn"])
        correct, count = run_problem(problem, source)
        passed += correct
        total += count
    print(f"D03: {passed}/{total} independent project cases passed")
    if passed != total:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
