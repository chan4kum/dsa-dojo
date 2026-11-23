"""Run a bounded D01 lab and check its observed result."""

import argparse
from math import isqrt


def decode_byte(broken):
    number = 0xFF
    if not broken and number >= 0x80:
        number -= 0x100
    return number


def matrix_vector(broken):
    matrix = ((1, 2), (3, 4))
    vector = (2,) if broken else (2, 1)
    if any(len(row) != len(vector) for row in matrix):
        return "incompatible dimensions"
    return [sum(left * right for left, right in zip(row, vector)) for row in matrix]


def trial_division(value: int, *, bounded: bool) -> tuple[bool, int]:
    """Return whether value is prime and how many divisibility checks ran."""
    if value < 2:
        return False, 0
    stop = isqrt(value) + 1 if bounded else value
    checks = 0
    for divisor in range(2, stop):
        checks += 1
        if value % divisor == 0:
            return False, checks
    return True, checks


def divisor_counts(broken):
    return [trial_division(value, bounded=not broken)[1] for value in (17, 97, 257)]


def attention_budget(broken):
    tokens = 32_768 if broken else 1_024
    score_bytes = tokens * tokens * 4
    limit = 64 * 2**20
    return score_bytes, score_bytes <= limit


LABS = {
    "L1": (decode_byte, -1, 255),
    "L2": (matrix_vector, [4, 10], "incompatible dimensions"),
    "L3": (divisor_counts, [3, 8, 15], [15, 95, 255]),
    "L4": (attention_budget, (4_194_304, True), (4_294_967_296, False)),
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
