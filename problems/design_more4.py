"""more Design problems (batch 6) - part of the problem bank for the "design" topic.

Each entry in PROBLEMS is ONE problem, written so you can read it top to bottom:
  title / lc / slug  name and LeetCode number (the official statement lives on LeetCode)
  prompt             the task in plain words          sig / fn   the function signature students implement
  tests              (arguments, expected result)     hints      three nudges, smallest first
  pattern / explain  the idea, and WHY it works       cx         complexity of the optimised solution
  brute / brute_cx   a simple correct solution and its cost (may be slow - that is the point)
  solution           the optimised solution, tested by `python dsa.py selftest`
Design problems are classes: tests are (constructor args, [(method, args, expected)]); S means "do not check
this return value" (for methods that return nothing or something random).
"""

from core import SKIP

S = SKIP

PROBLEMS = [
    # ---- Design a Text Editor (LeetCode 2296) ----
    dict(
        title="Design a Text Editor",
        diff="H",
        lc=2296,
        slug="design-a-text-editor",
        prompt=(
            "Implement TextEditor, an editor with a cursor that starts empty. addText(text) inserts text at the "
            "cursor (the cursor ends after it). deleteText(k) deletes up to k characters to the LEFT of the cursor "
            "and returns how many were deleted. cursorLeft(k) and cursorRight(k) move the cursor by up to k "
            "characters (staying inside the text) and return the last min(10, len) characters to the left of the "
            "cursor afterwards."
        ),
        sig=(
            "class TextEditor:\n    def __init__(self):\n        pass\n    def addText(self, text: str) -> "
            "None:\n        pass\n    def deleteText(self, k: int) -> int:\n        pass\n    def cursorLeft(self, "
            "k: int) -> str:\n        pass\n    def cursorRight(self, k: int) -> str:\n        pass"
        ),
        kind="design",
        cls="TextEditor",
        tests=[
            (
                (),
                [
                    ("addText", ["leetcode"], S),
                    ("deleteText", [4], 4),
                    ("addText", ["practice"], S),
                    ("cursorRight", [3], "etpractice"),
                    ("cursorLeft", [8], "leet"),
                    ("deleteText", [10], 4),
                    ("cursorLeft", [2], ""),
                    ("cursorRight", [6], "practi"),
                ],
            ),
            (
                (),
                [
                    ("addText", ["ab"], S),
                    ("cursorLeft", [1], "a"),
                    ("deleteText", [5], 1),
                    ("addText", ["xy"], S),
                    ("cursorRight", [10], "xyb"),
                ],
            ),
            (
                (),
                [
                    ("deleteText", [3], 0),
                    ("cursorLeft", [2], ""),
                    ("cursorRight", [2], ""),
                ],
            ),
        ],
        hints=[
            "Everything happens at the cursor, so split the text into 'left of the cursor' and 'right of the cursor'.",
            (
                "Keep the left part and the right part as two stacks (lists of characters): the end of 'left' and "
                "the end of 'right' are both next to the cursor."
            ),
            (
                "Moving the cursor pops characters from one stack and pushes them on the other; deleting pops from "
                "'left'; adding pushes onto 'left'. Return the last up-to-10 characters of 'left'."
            ),
        ],
        pattern="Two stacks around a cursor",
        explain=(
            "The cursor is a boundary between two pieces of text, and every operation touches only the characters "
            "right next to it. Storing the left piece as a stack (top = nearest the cursor) and the right piece as "
            "a stack (top = nearest the cursor, so it holds the text reversed) makes each character move, insertion "
            "or deletion O(1). The brute force keeps one string and rebuilds it on every operation."
        ),
        cx="O(k) per call (k = characters moved, added or deleted)",
        brute_cx="O(n) per call - rebuild the whole string each time",
        brute=r"""
# BRUTE FORCE: O(n) per call - rebuild the whole string each time
class TextEditor:
    def __init__(self):
        self.text = ""
        self.cursor = 0

    def addText(self, text):
        self.text = self.text[: self.cursor] + text + self.text[self.cursor :]
        self.cursor += len(text)

    def deleteText(self, k):
        removed = min(k, self.cursor)
        self.text = self.text[: self.cursor - removed] + self.text[self.cursor :]
        self.cursor -= removed
        return removed

    def cursorLeft(self, k):
        self.cursor = max(0, self.cursor - k)
        return self.text[max(0, self.cursor - 10) : self.cursor]

    def cursorRight(self, k):
        self.cursor = min(len(self.text), self.cursor + k)
        return self.text[max(0, self.cursor - 10) : self.cursor]
""",
        solution=r"""
# OPTIMISED: O(k) per call (k = characters moved, added or deleted)
# Idea: Two stacks around a cursor
class TextEditor:
    def __init__(self):
        self.left = []
        self.right = []

    def addText(self, text):
        self.left.extend(text)

    def deleteText(self, k):
        removed = min(k, len(self.left))
        del self.left[len(self.left) - removed :]
        return removed

    def cursorLeft(self, k):
        for _ in range(min(k, len(self.left))):
            self.right.append(self.left.pop())
        return "".join(self.left[-10:])

    def cursorRight(self, k):
        for _ in range(min(k, len(self.right))):
            self.left.append(self.right.pop())
        return "".join(self.left[-10:])
""",
    ),
]
