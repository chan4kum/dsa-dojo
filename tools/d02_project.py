"""Check a learner-provided D02 mini-library with the Dojo test engine."""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from core import run_problem  # noqa: E402

PROBLEMS = (
    {
        "fn": "second_largest_distinct",
        "tests": [
            (([],), None),
            (([4, 4],), None),
            (([-4, -1, -1, -8],), -4),
            (([6, 3, 5, 6],), 5),
        ],
    },
    {
        "fn": "rotate_right",
        "inplace": 0,
        "tests": [
            (([], 4), []),
            (([3], 20), [3]),
            (([1, 2, 3, 4], 5), [4, 1, 2, 3]),
            (([1, 2, 3], -1), [2, 3, 1]),
            (([1, 1, 2], 0), [1, 1, 2]),
        ],
    },
    {
        "fn": "max_circular_sum",
        "tests": [
            (([-3],), -3),
            (([-5, -2, -8],), -2),
            (([5, -3, 5],), 10),
            (([1, -2, 3, -2],), 3),
            (([0, 0, 0],), 0),
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
    print(f"D02: {passed}/{total} independent project cases passed")
    if passed != total:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
