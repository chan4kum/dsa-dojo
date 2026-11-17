"""more Two Pointers problems (batch 4) - part of the problem bank for the "two_pointers" topic.

Each entry in PROBLEMS is ONE problem, written so you can read it top to bottom:
  title / lc / slug  name and LeetCode number (the official statement lives on LeetCode)
  prompt             the task in plain words          sig / fn   the function signature students implement
  tests              (arguments, expected result)     hints      three nudges, smallest first
  pattern / explain  the idea, and WHY it works       cx         complexity of the optimised solution
  brute / brute_cx   a simple correct solution and its cost (may be slow - that is the point)
  solution           the optimised solution, tested by `python dsa.py selftest`
"""

PROBLEMS = [
    # ---- Backspace String Compare (LeetCode 844) ----
    dict(
        title="Backspace String Compare",
        diff="E",
        lc=844,
        slug="backspace-string-compare",
        prompt=(
            "'#' is a backspace in a typed string. Return True if s and t are equal after typing (an empty text "
            "stays empty on backspace)."
        ),
        sig="def backspace_compare(s: str, t: str) -> bool:",
        fn="backspace_compare",
        tests=[
            (("ab#c", "ad#c"), True),
            (("ab##", "c#d#"), True),
            (("a#c", "b"), False),
            (("y#fo##f", "y#f#o##f"), True),
        ],
        hints=[
            "Building both final strings with a stack works in O(n) space.",
            "Scanning from the END, a '#' means 'skip the next real character'.",
            (
                "Use two pointers from the back; advance each to its next surviving character and compare, tracking "
                "skip counters."
            ),
        ],
        pattern="Two pointers from the end (O(1) space)",
        explain=(
            "Going backwards you meet the backspace BEFORE the character it deletes, so a simple skip counter "
            "suffices and no stack is needed."
        ),
        cx="O(n + m) time, O(1) space",
        brute_cx="O(n + m) time, O(n + m) space - build both strings with a stack",
        brute=r"""
# BRUTE FORCE: O(n + m) time, O(n + m) space - build both strings with a stack
def backspace_compare(s, t):
    def typed(text):
        out = []
        for ch in text:
            if ch != "#":
                out.append(ch)
            elif out:
                out.pop()
        return out

    return typed(s) == typed(t)
""",
        solution=r"""
# OPTIMISED: O(n + m) time, O(1) space
# Idea: Two pointers from the end (O(1) space)
def backspace_compare(s, t):
    def next_valid(text, i):  # index of the next surviving character at or before i (or -1)
        skip = 0

        while i >= 0:
            if text[i] == "#":
                skip += 1
            elif skip:
                skip -= 1
            else:
                return i
            i -= 1

        return -1

    i, j = len(s) - 1, len(t) - 1

    while True:
        i, j = next_valid(s, i), next_valid(t, j)
        if i < 0 or j < 0:
            return i < 0 and j < 0  # both exhausted at the same time
        if s[i] != t[j]:
            return False
        i -= 1
        j -= 1
""",
    ),
    # ---- Long Pressed Name (LeetCode 925) ----
    dict(
        title="Long Pressed Name",
        diff="E",
        lc=925,
        slug="long-pressed-name",
        prompt=(
            "While typing name, some keys may be long-pressed (a character repeated extra times). Return True if "
            "typed could be the result of typing name."
        ),
        sig="def is_long_pressed_name(name: str, typed: str) -> bool:",
        fn="is_long_pressed_name",
        tests=[
            (("alex", "aaleex"), True),
            (("saeed", "ssaaedd"), False),
            (("leelee", "lleeelee"), True),
            (("laiden", "laiden"), True),
        ],
        hints=[
            "Compare the two strings in runs of equal characters.",
            "Each run in `name` must correspond to a run of the same letter in `typed` that is AT LEAST as long.",
            (
                "Two pointers: match name[i] with typed[j]; if typed[j] differs, it is allowed only when it repeats "
                "the previous typed character."
            ),
        ],
        pattern="Two pointers with run-length reasoning",
        explain=(
            "Run lengths in typed can only be longer, never shorter, and the letters must appear in the same order."
        ),
        cx="O(n + m) time, O(1) space",
        brute_cx="O(n + m) time, O(n + m) space - compare run-length encodings",
        brute=r"""
# BRUTE FORCE: O(n + m) time, O(n + m) space - compare run-length encodings
def is_long_pressed_name(name, typed):
    runs_name = [(k, len(list(g))) for k, g in itertools.groupby(name)]
    runs_typed = [(k, len(list(g))) for k, g in itertools.groupby(typed)]
    if len(runs_name) != len(runs_typed):
        return False
    return all(a == b and na <= nb for (a, na), (b, nb) in zip(runs_name, runs_typed))
""",
        solution=r"""
# OPTIMISED: O(n + m) time, O(1) space
# Idea: Two pointers with run-length reasoning
def is_long_pressed_name(name, typed):
    i = 0
    for j, ch in enumerate(typed):
        if i < len(name) and ch == name[i]:
            i += 1  # a character of the name was typed
        elif j == 0 or ch != typed[j - 1]:
            return False  # an unexpected new character (not just a long-press)
    return i == len(name)
""",
    ),
]
