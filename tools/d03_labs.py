"""Run bounded D03 hashing controls."""

import argparse
import sys
from collections import OrderedDict
from itertools import product
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from core import compile_solution  # noqa: E402
from dsa import get  # noqa: E402


def references():
    _, _, problem = get("hashing/1")
    name = problem["fn"]
    return tuple(compile_solution(problem[key])[name] for key in ("brute", "solution"))


def duplicate_pair(broken):
    brute, _ = references()
    return brute([3] if broken else [3, 3], 6), brute([], 6)


def collisions(broken):
    buckets = [[], [], [], []]
    for key in (1, 5, 9):
        buckets[key % len(buckets)].append(key)

    def lookup(key):
        bucket = buckets[key % len(buckets)]
        return next((entry for entry in bucket if broken or entry == key), None)

    return lookup(9), lookup(13)


def properties(broken):
    brute, optimized = references()
    checked = errors = 0
    for size in range(4):
        for values in product(range(-1, 2), repeat=size):
            for target in range(-2, 3):
                checked += 1
                expected = brute(values, target)
                actual = optimized(values, target)
                if broken and size == 1 and 2 * values[0] == target:
                    actual = [0, 0]
                if actual:
                    left, right = actual
                    valid = 0 <= left < right < size and values[left] + values[right] == target
                else:
                    valid = not expected
                errors += not valid
    return checked, errors


def lru_trace(broken):
    keys = "ABACDA" if broken else "ABAA"
    cache = OrderedDict()
    hits = 0
    for key in keys:
        if key in cache:
            hits += 1
            cache.move_to_end(key)
        else:
            cache[key] = None
            if len(cache) > 2:
                cache.popitem(last=False)
    return hits, len(cache)


LABS = {
    "L1": (duplicate_pair, ([0, 1], []), ([], [])),
    "L2": (collisions, (9, None), (1, 1)),
    "L3": (properties, (200, 0), (200, 3)),
    "L4": (lru_trace, (2, 2), (1, 2)),
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
