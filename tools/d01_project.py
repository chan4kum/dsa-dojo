"""Check a learner-provided D01 mini-library against public cases."""

import argparse
from pathlib import Path
from runpy import run_path

CASES = {
    "gcd": (
        ((0, 0), 0),
        ((-45, 30), 15),
        ((0, -32), 32),
        ((832_040, 514_229), 1),
    ),
    "integer_sqrt": (
        ((0,), 0),
        ((48,), 6),
        ((49,), 7),
        (((2**60) ** 2 - 1,), 2**60 - 1),
        ((-1,), None),
    ),
    "modular_power": (
        ((-2, 5, 7), 3),
        ((0, 0, 3), 1),
        ((10, 0, 1), 0),
        ((3, 100_001, 97), pow(3, 100_001, 97)),
        ((3, -1, 7), None),
        ((3, 0, 0), None),
    ),
}


def check(submission):
    functions = run_path(str(submission))
    passed = 0
    for name, cases in CASES.items():
        solve = functions.get(name)
        if not callable(solve):
            raise SystemExit(f"Define {name} in your solution file.")
        for args, expected in cases:
            try:
                actual = solve(*args)
            except ValueError:
                if expected is not None:
                    raise SystemExit(f"{name}{args}: unexpected ValueError") from None
            else:
                if expected is None:
                    raise SystemExit(f"{name}{args}: expected ValueError, observed {actual!r}")
                if type(actual) is not int or actual != expected:
                    raise SystemExit(f"{name}{args}: expected {expected!r}, observed {actual!r}")
            passed += 1
    return passed


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("submission", type=Path)
    args = parser.parse_args()
    print(f"D01: {check(args.submission)} independent project cases passed")


if __name__ == "__main__":
    main()
