#!/usr/bin/env python3
"""Re-lays-out every problems/*.py file so each problem reads the same way.

For each problem it writes
  * a banner comment with the problem name,
  * one key per line in a fixed order, one test per line, one hint per line,
  * a plain-English header comment on top of every brute-force / optimised solution
    ("# OPTIMISED: O(n) time ... / Idea: ..."), so a reader knows what the code is for,
  * lint-friendly names inside the embedded solutions (the ambiguous one-letter `l` becomes `left`).

Run it after adding problems:  python tools/format_problems.py
It is idempotent and never changes what a solution does.
"""

import ast
import io
import json
import pathlib
import re
import shutil
import subprocess
import textwrap
import tokenize

# The order in which keys are written inside every problem.
ORDER = [
    "title",
    "diff",
    "lc",
    "slug",
    "prompt",
    "sig",
    "fn",
    "kind",
    "cls",
    "compare",
    "adapt_in",
    "adapt_out",
    "inplace",
    "check",
    "tests",
    "hints",
    "pattern",
    "explain",
    "cx",
    "brute_cx",
    "brute",
    "solution",
]
LIST_KEYS = {"tests", "hints"}  # lists that get one element per line
I1, I2, I3 = " " * 4, " " * 8, " " * 12  # indentation levels
RAWS = ("r'''", 'r"""')  # openings of the raw triple-quoted strings that hold embedded code


def seg(src, node):
    """The exact source text of an AST node."""
    return ast.get_source_segment(src, node, padded=False)


def one_line(src, node):
    """Source text of a value. A prose string that was split over several lines is joined back into one
    literal first, so `wrap_long_strings` can re-split it cleanly and the layout is the same on every run."""
    if isinstance(node, ast.Constant) and isinstance(node.value, str) and node.lineno != node.end_lineno:
        text = seg(src, node)
        if not text.startswith(RAWS):
            return json.dumps(node.value, ensure_ascii=False)
    return seg(src, node)


def rename_ambiguous(code):
    """Rename the lint-ambiguous variable `l` (E741: looks like 1 or I) to `left`.

    When `r` is used as its right-hand partner it becomes `right`. Strings and comments are never touched,
    and snippets that already use the new names are left alone to avoid a clash.
    """
    toks = list(tokenize.generate_tokens(io.StringIO(code).readline))
    names = {
        t.string for i, t in enumerate(toks) if t.type == tokenize.NAME and not (i and toks[i - 1].string == ".")
    }  # attribute names do not clash
    if "l" not in names or "left" in names:
        return code
    rename = {"l": "left"}
    if "r" in names and "right" not in names and "c" not in names:  # `r, c` means row/column, not a pair
        rename["r"] = "right"
    lines = code.split("\n")
    for i, tok in reversed(list(enumerate(toks))):
        is_attribute = i > 0 and toks[i - 1].string == "."
        if tok.type == tokenize.NAME and tok.string in rename and not is_attribute:
            row, col = tok.start
            line = lines[row - 1]
            lines[row - 1] = line[:col] + rename[tok.string] + line[col + len(tok.string) :]
    return "\n".join(lines)


LONG = 120  # the repo's line-length limit (ruff.toml)
STRING_LINE = re.compile(r"^(\s*)((?:[A-Za-z_]+=)?)(\"(?:[^\"\\]|\\.)*\"|'(?:[^'\\]|\\.)*')(,?)$")


def wrap_long_strings(text):
    """Split any over-long one-line string (a prompt, hint or explanation) into several adjacent literals.

    Python joins adjacent string literals, so the value does not change - only the layout does:
        prompt=("first part of the sentence "
                "second part"),
    """
    out, in_raw = [], False
    for line in text.split("\n"):
        if sum(line.count(q) for q in ("'''", '"""')) == 1:  # entering/leaving an embedded code block
            in_raw = not in_raw
        m = None if in_raw or len(line) <= LONG else STRING_LINE.match(line)
        if not m:
            out.append(line)
            continue
        indent, key, literal, comma = m.groups()
        value = ast.literal_eval(literal)
        quote = literal[0]
        pad = indent + "    "
        room = LONG - len(pad) - 3  # quotes + safety
        pieces, current = [], ""
        for word in re.findall(r"\S+\s*", value):
            if current and len(repr(current + word)) > room:
                pieces.append(current)
                current = ""
            current += word
        pieces.append(current)
        out.append(f"{indent}{key}(")
        out += [f"{pad}{json_quote(piece, quote)}" for piece in pieces]
        out.append(f"{indent}){comma}")
    return "\n".join(out)


def json_quote(piece, quote):
    """Write `piece` as a string literal using the same quote character as the original."""
    body = repr(piece)
    if body[0] != quote:  # repr picked the other quote style
        body = quote + body[1:-1].replace(quote, "\\" + quote) + quote
    return body


def ruff_format(code):
    """Lay the code out the way the rest of the repo is laid out (one statement per line, consistent quotes).
    Skipped silently when ruff is not installed."""
    if not shutil.which("ruff"):
        return code
    run = subprocess.run(
        ["ruff", "format", "--line-length", "100", "--stdin-filename", "snippet.py", "-"],
        input=code,
        capture_output=True,
        text=True,
    )
    return run.stdout if run.returncode == 0 else code


def annotate(code, label, cost, idea=None):
    """Put a header comment on top of a solution: what it is, what it costs and (optionally) the key idea."""
    body = code.lstrip("\n")
    if body.startswith(("# BRUTE FORCE", "# OPTIMISED")):
        return code  # already annotated
    head = [f"# {label}: {cost}" if cost else f"# {label}"]
    if idea:
        head += textwrap.wrap(f"Idea: {idea}", 96, initial_indent="# ", subsequent_indent="#       ")
    return "\n" + "\n".join(head) + "\n" + body


def code_value(src, node, label, cost, idea=None):
    """Re-emit a brute/solution raw string with its header comment and lint-friendly names."""
    text = seg(src, node)
    opening = next((q for q in RAWS if text.startswith(q)), None)
    if opening is None:
        return text
    code = ast.literal_eval(node)
    code = ruff_format(rename_ambiguous(code).strip("\n") + "\n")
    return opening + annotate("\n" + code, label, cost, idea) + opening[1:]


def render_problem(src, call):
    """Return the canonical source text of one problem (a `dict(...)` call)."""
    kws = {k.arg: k.value for k in call.keywords}
    title = ast.literal_eval(kws["title"])
    lc = ast.literal_eval(kws["lc"])
    out = [f"{I1}# {'-' * 4} {title} (LeetCode {lc}) {'-' * 4}", f"{I1}dict("]
    keys = [k for k in ORDER if k in kws] + [k for k in kws if k not in ORDER]
    for k in keys:
        v = kws[k]
        if k in LIST_KEYS and isinstance(v, ast.List) and v.elts:
            out.append(f"{I2}{k}=[")
            out += [f"{I3}{one_line(src, e)}," for e in v.elts]
            out.append(f"{I2}],")
        elif k == "brute":
            cost = ast.literal_eval(kws["brute_cx"]) if "brute_cx" in kws else None
            out.append(f"{I2}brute={code_value(src, v, 'BRUTE FORCE', cost)},")
        elif k == "solution":
            cost = ast.literal_eval(kws["cx"]) if "cx" in kws else None
            idea = ast.literal_eval(kws["pattern"]) if "pattern" in kws else None
            out.append(f"{I2}solution={code_value(src, v, 'OPTIMISED', cost, idea)},")
        else:
            out.append(f"{I2}{k}={one_line(src, v)},")
    out.append(f"{I1}),")
    return "\n".join(out)


def format_file(path):
    """Rewrite the PROBLEMS list of one file; everything else in the file is kept as it is."""
    src = path.read_text()
    tree = ast.parse(src)
    node = next(
        (n for n in tree.body if isinstance(n, ast.Assign) and getattr(n.targets[0], "id", "") == "PROBLEMS"), None
    )
    if node is None:
        return False
    body = "\n\n".join(render_problem(src, c) for c in node.value.elts)
    lines = src.split("\n")
    new = lines[: node.lineno - 1] + ["PROBLEMS = [", body, "]"] + lines[node.end_lineno :]
    path.write_text(wrap_long_strings("\n".join(new).rstrip("\n") + "\n"))
    return True


if __name__ == "__main__":
    root = pathlib.Path(__file__).resolve().parent.parent / "problems"
    count = sum(format_file(p) for p in sorted(root.glob("*.py")) if p.name != "__init__.py")
    if shutil.which("ruff"):  # final pass: ruff's own layout, same line length
        subprocess.run(["ruff", "format", "--line-length", "120", "-q", str(root)], check=False)
    print(f"formatted {count} problem files")
