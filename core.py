"""core.py - shared helpers + the local test engine. Pure Python 3.9+, no dependencies.

Solution files do `from core import *`, so List, Optional, ListNode, TreeNode,
heapq, deque, Counter, defaultdict, bisect, math ... are all available.
"""

import bisect
import collections
import copy
import functools
import heapq
import itertools
import math
import random
import signal
import time
import traceback
from collections import Counter, OrderedDict, defaultdict, deque
from functools import lru_cache
from typing import Dict, List, Optional, Set, Tuple

SKIP = Ellipsis  # in design-problem ops: "call this method, don't check the result"

__all__ = [
    "bisect",
    "collections",
    "copy",
    "functools",
    "heapq",
    "itertools",
    "math",
    "random",
    "Counter",
    "OrderedDict",
    "defaultdict",
    "deque",
    "lru_cache",
    "Dict",
    "List",
    "Optional",
    "Set",
    "Tuple",
    "ListNode",
    "TreeNode",
    "Node",
    "list_to_ll",
    "ll_to_list",
    "list_to_tree",
    "tree_to_list",
    "find_node",
    "SKIP",
]


# ----------------------------------------------------------------- data structures
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Node:
    """Graph node for Clone Graph: a value and a list of neighbour nodes."""

    def __init__(self, val=0, neighbors=None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def list_to_ll(values):
    dummy = tail = ListNode()
    for v in values:
        tail.next = ListNode(v)
        tail = tail.next
    return dummy.next


def ll_to_list(head):
    out = []
    while head:
        out.append(head.val)
        head = head.next
    return out


def list_to_tree(vals):
    """Level-order list with None for missing children -> tree (LeetCode style)."""
    if not vals or vals[0] is None:
        return None
    root = TreeNode(vals[0])
    q = deque([root])
    i = 1
    while q and i < len(vals):
        node = q.popleft()
        if i < len(vals) and vals[i] is not None:
            node.left = TreeNode(vals[i])
            q.append(node.left)
        i += 1
        if i < len(vals) and vals[i] is not None:
            node.right = TreeNode(vals[i])
            q.append(node.right)
        i += 1
    return root


def tree_to_list(root):
    if not root:
        return []
    out, q = [], deque([root])
    while q:
        n = q.popleft()
        if n is None:
            out.append(None)
            continue
        out.append(n.val)
        q.append(n.left)
        q.append(n.right)
    while out and out[-1] is None:
        out.pop()
    return out


def find_node(root, val):
    stack = [root]
    while stack:
        n = stack.pop()
        if n is None:
            continue
        if n.val == val:
            return n
        stack += [n.left, n.right]
    return None


# ----------------------------------------------------------------- test engine
class Timeout(Exception):
    pass


def _arm(seconds):
    if hasattr(signal, "SIGALRM"):  # not available on Windows -> no timeout there

        def handler(*_):
            raise Timeout()

        signal.signal(signal.SIGALRM, handler)
        signal.setitimer(signal.ITIMER_REAL, seconds)


def _disarm():
    if hasattr(signal, "SIGALRM"):
        signal.setitimer(signal.ITIMER_REAL, 0)


def base_namespace():
    ns = {name: globals()[name] for name in __all__}
    ns["__name__"] = "solution"  # so a stub's `if __name__ == "__main__"` block is skipped
    ns["__file__"] = __file__
    return ns


def compile_solution(source):
    ns = base_namespace()
    exec(compile(source, "<solution>", "exec"), ns)
    return ns


def _normalize(x, mode):
    if mode == "unordered":  # outer order free, inner order matters
        return sorted(x, key=repr)
    if mode == "nested_unordered":  # both outer and inner order free
        return sorted((sorted(i, key=repr) for i in x), key=repr)
    return x


def equal(got, exp, mode="exact"):
    if mode == "float":
        return abs(got - exp) <= 1e-5
    try:
        return _normalize(got, mode) == _normalize(exp, mode)
    except Exception:
        return False


def _short(x, n=110):
    s = repr(x)
    return s if len(s) <= n else s[: n - 3] + "..."


def run_problem(p, source, verbose=True, timeout=2.0, stats=None):
    """Run every test of problem `p` against `source`. Returns (passed, total).
    stats (dict, optional) receives {"timeouts": n} so callers can tell 'too slow' from 'wrong'."""
    out = print if verbose else (lambda *a, **k: None)
    if stats is not None:
        stats["timeouts"] = 0
    sys_limit = __import__("sys").getrecursionlimit()
    __import__("sys").setrecursionlimit(max(sys_limit, 10000))
    try:
        ns = compile_solution(source)
    except Exception:
        out("  x could not load your file:\n   ", traceback.format_exc(limit=1).strip().splitlines()[-1])
        return 0, len(p["tests"])
    passed = 0
    for i, (args, exp) in enumerate(p["tests"], 1):
        t0 = time.perf_counter()
        got, ok, err = None, False, None
        try:
            if p.get("kind") == "design":
                obj = ns[p["cls"]](*args)
                ok = True
                for method, margs, mexp in exp:
                    _arm(timeout)
                    got = getattr(obj, method)(*copy.deepcopy(margs))
                    _disarm()
                    if mexp is not SKIP and not equal(got, mexp, p.get("compare", "exact")):
                        ok = False
                        err = f"{method}{tuple(margs)} -> {_short(got)}, expected {_short(mexp)}"
                        break
            else:
                a = copy.deepcopy(args)
                if "adapt_in" in p:
                    a = p["adapt_in"](a)
                _arm(timeout)
                got = ns[p["fn"]](*a)
                _disarm()
                if "inplace" in p:  # function mutates argument #inplace instead of returning
                    got = a[p["inplace"]]
                if "adapt_out" in p:
                    got = p["adapt_out"](got)
                if "check" in p:  # several answers are valid -> custom validator
                    ok = bool(p["check"](args, got))
                else:
                    ok = equal(got, exp, p.get("compare", "exact"))
        except Timeout:
            err = f"TIMEOUT (> {timeout}s) - too slow, look for a better complexity"
            if stats is not None:
                stats["timeouts"] += 1
        except Exception:
            err = traceback.format_exc(limit=2).strip().splitlines()[-1]
        finally:
            _disarm()
        ms = (time.perf_counter() - t0) * 1000
        if ok:
            passed += 1
            out(f"  ok  test {i}  ({ms:.1f} ms)")
        else:
            out(f"  FAIL test {i}")
            if p.get("kind") == "design":
                out(f"       {err}")
            else:
                out(f"       input   : {_short(args)}")
                out(f"       expected: {_short(exp)}")
                out(f"       got     : {err or _short(got)}")
    return passed, len(p["tests"])
