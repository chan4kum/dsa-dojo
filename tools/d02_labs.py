"""Run bounded D02 lab controls with the Dojo's existing stock references."""

import argparse
import sys
from itertools import product
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from core import compile_solution  # noqa: E402
from dsa import get  # noqa: E402


def references():
    _, _, problem = get("sliding_window/5")
    name = problem["fn"]
    return tuple(compile_solution(problem[key])[name] for key in ("brute", "solution"))


def baseline(broken):
    brute, _ = references()
    prices = [4, 4, 4, 4] if broken else [7, 1, 5, 3, 6, 4]
    count = len(prices)
    return count * (count - 1) // 2, brute(prices), brute([])


def adversarial_order(broken):
    _, optimized = references()
    prices = [7, 6, 4, 1]
    return max(prices) - min(prices) if broken else optimized(prices)


def properties(broken):
    brute, optimized = references()
    cases = [list(values) for size in range(5) for values in product(range(3), repeat=size)]
    cases.append([2**53, 2**53 + 1])
    disagreements = 0
    for prices in cases:
        candidate = [float(price) for price in prices] if broken else prices
        disagreements += brute(prices) != optimized(candidate)
    return len(cases), disagreements


def work_budget(broken):
    count = 4096 if broken else 64
    pairs = count * (count - 1) // 2
    return pairs, pairs <= 100_000, count <= 100_000


LABS = {
    "L1": (baseline, (15, 5, 0), (6, 0, 0)),
    "L2": (adversarial_order, 0, 6),
    "L3": (properties, (122, 0), (122, 1)),
    "L4": (work_budget, (2016, True, True), (8386560, False, True)),
}


def verify(lab, broken):
    experiment, normal, changed = LABS[lab]
    observed = experiment(broken)
    expected = changed if broken else normal
    if observed != expected:
        raise SystemExit(f"{lab}: expected {expected!r}, observed {observed!r}")
    return observed


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("lab", choices=LABS)
    parser.add_argument("--break", dest="broken", action="store_true")
    args = parser.parse_args()
    label = "failure control" if args.broken else "normal control"
    print(f"{args.lab} {label}: {verify(args.lab, args.broken)!r}")


if __name__ == "__main__":
    main()
