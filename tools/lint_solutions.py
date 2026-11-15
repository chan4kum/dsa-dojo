#!/usr/bin/env python3
"""Lint the Python code that lives INSIDE the problem files (the brute-force and optimised solutions).

`ruff check .` cannot see them because they are stored as strings. This script writes each one to a temporary
file and runs ruff on the lot, with the helper names the engine provides (List, TreeNode, Counter ...) declared
as builtins. Same rules as the rest of the repo (see ruff.toml).

    python tools/lint_solutions.py          # exits 1 if any solution breaks the lint rules
"""

import subprocess
import sys
import tempfile
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from core import __all__ as HELPER_NAMES  # noqa: E402
from dsa import TOPICS, load  # noqa: E402


def main():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        origin = {}  # temp file name -> "topic/n title (brute|optimised)"
        for topic in TOPICS:
            for n, problem in enumerate(load(topic), 1):
                for kind, key in (("brute", "brute"), ("optimised", "solution")):
                    name = f"{topic}_{n:02d}_{kind}.py"
                    (tmp / name).write_text(textwrap.dedent(problem[key]).lstrip("\n"))
                    origin[name] = f"{topic}/{n} {problem['title']} ({kind})"
        config = tmp / "ruff.toml"
        names = ", ".join(f'"{n}"' for n in HELPER_NAMES)
        config.write_text(
            f'line-length = 120\ntarget-version = "py39"\nbuiltins = [{names}]\n[lint]\nselect = ["E", "W", "F", "B"]\n'
        )
        run = subprocess.run(
            ["ruff", "check", "--config", str(config), "--output-format", "concise", str(tmp)],
            capture_output=True,
            text=True,
        )
        lines = [ln for ln in run.stdout.splitlines() if ".py:" in ln]
        for ln in lines:
            file_name = Path(ln.split(":")[0]).name
            print(f"{origin.get(file_name, file_name)}: {ln.split(':', 1)[1].strip()}")
    print(f"lint_solutions: {len(origin)} embedded solutions checked, {len(lines)} problems")
    sys.exit(1 if lines else 0)


main()
