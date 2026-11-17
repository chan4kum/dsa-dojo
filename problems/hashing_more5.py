"""extra batch of Hashing problems - the problem bank for the "hashing" topic (batch 5).

Each entry in PROBLEMS is ONE problem, written so you can read it top to bottom:
  title / lc / slug  name and LeetCode number (the official statement lives on LeetCode)
  prompt             the task in plain words          sig / fn   the function signature students implement
  tests              (arguments, expected result)     hints      three nudges, smallest first
  pattern / explain  the idea, and WHY it works       cx         complexity of the optimised solution
  brute / brute_cx   a simple correct solution and its cost (may be slow - that is the point)
  solution           the optimised solution, tested by `python dsa.py selftest`
Optional keys: compare (how to compare answers), adapt_in/adapt_out (convert lists <-> linked lists / trees),
check (validate any correct answer), inplace (which argument is mutated).
"""


def _restore_ok(args, got):
    """True if `got` is an array whose adjacent pairs are exactly the given pairs (in either direction)."""
    pairs = args[0]
    if not isinstance(got, list) or len(got) != len(pairs) + 1:
        return False
    wanted = sorted(sorted(p) for p in pairs)
    return sorted(sorted(got[i : i + 2]) for i in range(len(got) - 1)) == wanted


PROBLEMS = [
    # ---- Longest Absolute File Path (LeetCode 388) ----
    dict(
        title="Longest Absolute File Path",
        diff="M",
        lc=388,
        slug="longest-absolute-file-path",
        prompt=(
            "A file system is written as one string: entries are separated by '\\n' and an entry's depth is the "
            "number of leading '\\t'. An entry containing a '.' is a file, otherwise a directory (which contains "
            "the deeper entries that follow it). Return the length of the longest absolute path to a file "
            "(directories and the file joined with '/'), or 0 if there is no file."
        ),
        sig="def length_longest_path(input: str) -> int:",
        fn="length_longest_path",
        tests=[
            (("dir\n\tsubdir1\n\tsubdir2\n\t\tfile.ext",), 20),
            (("dir\n\tsubdir1\n\t\tfile1.ext\n\t\tsubsubdir1\n\tsubdir2\n\t\tsubsubdir2\n\t\t\tfile2.ext",), 32),
            (("a",), 0),
            (("file1.txt\nfile2.txt\nlongfile.txt",), 12),
        ],
        hints=[
            (
                "The path to an entry is the path of its parent plus '/' plus its own name; the parent is the "
                "nearest earlier entry with a smaller depth."
            ),
            (
                "You only need LENGTHS, so store for each depth the length of the path ending at the latest entry "
                "of that depth."
            ),
            (
                "For an entry at depth d: length = lengths[d - 1] + 1 + len(name) (or just len(name) at depth 0). "
                "Record it at lengths[d]; if it is a file, update the answer."
            ),
        ],
        pattern="Hash map / array from depth to the current path length",
        explain=(
            "Entries are listed in depth-first order, so when an entry at depth d appears, the last seen entry at "
            "depth d - 1 is its parent, and everything deeper is already finished. Keeping the running path length "
            "for each depth lets every entry compute its own path length in O(1) without building strings."
        ),
        cx="O(n) time, O(depth) space",
        brute_cx="O(n * L) time - build the full path string for every file",
        brute=r"""
# BRUTE FORCE: O(n * L) time - build the full path string for every file
def length_longest_path(input):
    path = []
    best = 0

    for line in input.split("\n"):
        depth = len(line) - len(line.lstrip("\t"))
        name = line.lstrip("\t")
        del path[depth:]
        path.append(name)
        if "." in name:
            best = max(best, len("/".join(path)))

    return best
""",
        solution=r"""
# OPTIMISED: O(n) time, O(depth) space
# Idea: Hash map / array from depth to the current path length
def length_longest_path(input):
    lengths = {-1: -1}
    best = 0

    for line in input.split("\n"):
        name = line.lstrip("\t")
        depth = len(line) - len(name)
        lengths[depth] = lengths[depth - 1] + 1 + len(name)
        if "." in name:
            best = max(best, lengths[depth])

    return best
""",
    ),
    # ---- Set Mismatch (LeetCode 645) ----
    dict(
        title="Set Mismatch",
        diff="E",
        lc=645,
        slug="set-mismatch",
        prompt=(
            "nums should contain each of 1..n once, but one number was duplicated and thereby another number is "
            "missing. Return [duplicate, missing]."
        ),
        sig="def find_error_nums(nums: List[int]) -> List[int]:",
        fn="find_error_nums",
        tests=[
            (([1, 2, 2, 4],), [2, 3]),
            (([1, 1],), [1, 2]),
            (([2, 2],), [2, 1]),
            (([3, 2, 3, 4, 6, 5],), [3, 1]),
        ],
        hints=[
            "Count how often each number appears.",
            "The duplicate is the one with count 2; the missing one is the number in 1..n with count 0.",
            (
                "No counting table needed: sum(nums) - sum(set(nums)) is the duplicate, and n(n+1)/2 - "
                "sum(set(nums)) is the missing number."
            ),
        ],
        pattern="Set difference / sum arithmetic",
        explain=(
            "The distinct values are 1..n without the missing number, so their sum is n(n+1)/2 - missing. The plain "
            "sum counts the duplicate one extra time. Two subtractions therefore give both answers in one pass with "
            "O(n) memory for the set."
        ),
        cx="O(n) time, O(n) space",
        brute_cx="O(n^2) time - count every number 1..n by scanning the list",
        brute=r"""
# BRUTE FORCE: O(n^2) time - count every number 1..n by scanning the list
def find_error_nums(nums):
    duplicate = missing = 0

    for v in range(1, len(nums) + 1):
        count = nums.count(v)
        if count == 2:
            duplicate = v
        elif count == 0:
            missing = v

    return [duplicate, missing]
""",
        solution=r"""
# OPTIMISED: O(n) time, O(n) space
# Idea: Set difference / sum arithmetic
def find_error_nums(nums):
    distinct = sum(set(nums))
    n = len(nums)
    return [sum(nums) - distinct, n * (n + 1) // 2 - distinct]
""",
    ),
    # ---- Find and Replace Pattern (LeetCode 890) ----
    dict(
        title="Find and Replace Pattern",
        diff="M",
        lc=890,
        slug="find-and-replace-pattern",
        prompt=(
            "A word matches a pattern if some bijection of letters (each letter maps to one letter and no two "
            "letters map to the same one) turns the pattern into the word. Return the words that match pattern, in "
            "the original order."
        ),
        sig="def find_and_replace_pattern(words: List[str], pattern: str) -> List[str]:",
        fn="find_and_replace_pattern",
        tests=[
            ((["abc", "deq", "mee", "aqq", "dkd", "ccc"], "abb"), ["mee", "aqq"]),
            ((["a", "b", "c"], "a"), ["a", "b", "c"]),
            ((["xyz", "xxy"], "abc"), ["xyz"]),
            (([], "a"), []),
        ],
        hints=[
            "Two strings are 'the same shape' when equal letters sit at equal positions in both.",
            "Replace each string by its canonical form: the index of each letter's FIRST occurrence (abb -> 0,1,1).",
            "A word matches iff its canonical form equals the pattern's canonical form.",
        ],
        pattern="Canonical form / normalisation with a first-seen index map",
        explain=(
            "Writing each letter as the order in which it first appeared erases the actual letters but keeps the "
            "equality structure. A bijection exists iff the structures are identical, so comparing canonical forms "
            "replaces the two-way dictionary bookkeeping."
        ),
        cx="O(total length) time, O(word length) space",
        brute_cx=(
            "O(total length) time - count the distinct (word letter, pattern letter) pairs against the distinct "
            "letters on each side"
        ),
        brute=r"""
# BRUTE FORCE: O(total length) time - compare the number of distinct letter pairs with the distinct letters
def find_and_replace_pattern(words, pattern):
    matches = []
    for word in words:
        pairs = set(zip(word, pattern))
        if len(pairs) == len(set(word)) == len(set(pattern)):
            matches.append(word)
    return matches
""",
        solution=r"""
# OPTIMISED: O(total length) time, O(word length) space
# Idea: Canonical form / normalisation with a first-seen index map
def find_and_replace_pattern(words, pattern):
    def shape(text):
        first = {}
        return [first.setdefault(ch, len(first)) for ch in text]

    target = shape(pattern)
    return [word for word in words if shape(word) == target]
""",
    ),
    # ---- Array of Doubled Pairs (LeetCode 954) ----
    dict(
        title="Array of Doubled Pairs",
        diff="M",
        lc=954,
        slug="array-of-doubled-pairs",
        prompt=(
            "arr has even length. Return True if it can be reordered so that arr[2i + 1] == 2 * arr[2i] for every "
            "i, i.e. if the elements can be paired up as (x, 2x)."
        ),
        sig="def can_reorder_doubled(arr: List[int]) -> bool:",
        fn="can_reorder_doubled",
        tests=[
            (([3, 1, 3, 6],), False),
            (([2, 1, 2, 6],), False),
            (([4, -2, 2, -4],), True),
            (([0, 0],), True),
            (([1, 2, 4, 16, 8, 4],), False),
        ],
        hints=[
            (
                "The element closest to zero in absolute value can only be the SMALLER half of its pair - nothing "
                "else could double into it."
            ),
            "Process the values in order of increasing absolute value, using counts.",
            (
                "For each value x with count c > 0 you need c copies of 2x; if cnt[2x] < c fail, otherwise "
                "subtract. Zero pairs with itself, so it needs an even count."
            ),
        ],
        pattern="Greedy matching on a frequency map, smallest magnitude first",
        explain=(
            "The element with the smallest absolute value has exactly one possible partner (twice itself), because "
            "halving it would give something of even smaller magnitude. Forcing that pairing and moving to the next "
            "magnitude is therefore safe. Sorting by abs makes the order explicit; negative numbers work because -4 "
            "needs -8, and zero is its own double."
        ),
        cx="O(n log n) time, O(n) space",
        brute_cx="exponential - try every possible partner of the first remaining element",
        brute=r"""
# BRUTE FORCE: exponential - try every possible partner of the first remaining element
def can_reorder_doubled(arr):
    def match(rest):
        if not rest:
            return True

        x = rest[0]
        others = rest[1:]

        for target in {2 * x, x / 2}:
            if target in others:
                trial = list(others)
                trial.remove(target)
                if match(trial):
                    return True

        return False

    return match(list(arr))
""",
        solution=r"""
# OPTIMISED: O(n log n) time, O(n) space
# Idea: Greedy matching on a frequency map, smallest magnitude first
def can_reorder_doubled(arr):
    count = Counter(arr)

    for x in sorted(count, key=abs):
        if count[x] > count[2 * x]:
            return False
        if x == 0 and count[0] % 2:
            return False
        count[2 * x] -= count[x]

    return True
""",
    ),
    # ---- Divide Array in Sets of K Consecutive Numbers (LeetCode 1296) ----
    dict(
        title="Divide Array in Sets of K Consecutive Numbers",
        diff="M",
        lc=1296,
        slug="divide-array-in-sets-of-k-consecutive-numbers",
        prompt=(
            "Return True if nums can be divided into groups of exactly k consecutive integers (x, x+1, ..., x+k-1), "
            "using every element once."
        ),
        sig="def is_possible_divide(nums: List[int], k: int) -> bool:",
        fn="is_possible_divide",
        tests=[
            (([1, 2, 3, 3, 4, 4, 5, 6], 4), True),
            (([3, 2, 1, 2, 3, 4, 3, 4, 5, 9, 10, 11], 3), True),
            (([1, 2, 3, 4], 3), False),
            (([1, 2, 3, 4], 2), True),
            (([1, 1, 2, 2], 2), True),
        ],
        hints=[
            "The smallest remaining number can only be the START of a group (nothing smaller is left to precede it).",
            "So repeatedly take the smallest remaining number x and remove x, x+1, ..., x+k-1.",
            (
                "Keep a Counter; walk the distinct values in sorted order and for each value with count c > 0 "
                "subtract c from each of the next k-1 values (fail if any is too small)."
            ),
        ],
        pattern="Greedy from the smallest value with a frequency map",
        explain=(
            "The smallest remaining value cannot be inside a run that begins lower, so it must start a run. Taking "
            "all c copies at once starts c runs, which consume c copies of each of the next k - 1 values. If any is "
            "short, no valid grouping exists. The length must also be divisible by k."
        ),
        cx="O(n log n) time (sort the distinct values), O(n) space",
        brute_cx="O(n^2) time - repeatedly find the minimum and remove its run from the list",
        brute=r"""
# BRUTE FORCE: O(n^2) time - repeatedly find the minimum and remove its run from the list
def is_possible_divide(nums, k):
    rest = sorted(nums)

    while rest:
        start = rest[0]
        for x in range(start, start + k):
            if x not in rest:
                return False
            rest.remove(x)

    return True
""",
        solution=r"""
# OPTIMISED: O(n log n) time (sort the distinct values), O(n) space
# Idea: Greedy from the smallest value with a frequency map
def is_possible_divide(nums, k):
    if len(nums) % k:
        return False

    count = Counter(nums)

    for x in sorted(count):
        c = count[x]
        if c:
            for y in range(x, x + k):
                if count[y] < c:
                    return False
                count[y] -= c

    return True
""",
    ),
    # ---- Display Table of Food Orders in a Restaurant (LeetCode 1418) ----
    dict(
        title="Display Table of Food Orders in a Restaurant",
        diff="M",
        lc=1418,
        slug="display-table-of-food-orders-in-a-restaurant",
        prompt=(
            "orders[i] = [customerName, tableNumber, foodItem]. Build the 'display table': the header row ['Table', "
            "food1, food2, ...] with food names in alphabetical order, then one row per table in increasing numeric "
            "table order giving the table number and how many of each food that table ordered (all as strings)."
        ),
        sig="def display_table(orders: List[List[str]]) -> List[List[str]]:",
        fn="display_table",
        tests=[
            (
                (
                    [
                        ["David", "3", "Ceviche"],
                        ["Corina", "10", "Beef Burrito"],
                        ["David", "3", "Fried Chicken"],
                        ["Carla", "5", "Water"],
                        ["Carla", "5", "Ceviche"],
                        ["Rous", "3", "Ceviche"],
                    ],
                ),
                [
                    ["Table", "Beef Burrito", "Ceviche", "Fried Chicken", "Water"],
                    ["3", "0", "2", "1", "0"],
                    ["5", "0", "1", "0", "1"],
                    ["10", "1", "0", "0", "0"],
                ],
            ),
            (
                (
                    [
                        ["James", "12", "Fried Chicken"],
                        ["Ratesh", "12", "Fried Chicken"],
                        ["Amadeus", "12", "Fried Chicken"],
                        ["Adam", "1", "Canadian Waffles"],
                        ["Brianna", "1", "Canadian Waffles"],
                    ],
                ),
                [["Table", "Canadian Waffles", "Fried Chicken"], ["1", "2", "0"], ["12", "0", "3"]],
            ),
            (([["Laura", "2", "Bean Burrito"]],), [["Table", "Bean Burrito"], ["2", "1"]]),
        ],
        hints=[
            "Sort the table numbers numerically (as integers, not as strings) and the food names alphabetically.",
            "Count orders per (table, food) in a dictionary of dictionaries.",
            "Build the header from the sorted food names, then one row per table reading counts with .get(food, 0).",
        ],
        pattern="Nested dictionary (table -> food -> count) + sorted keys",
        explain=(
            "A dictionary keyed by table whose values are Counters of foods collects all counts in one pass. The "
            "output needs deterministic ordering, so the distinct foods are sorted alphabetically and the tables "
            "numerically (int, because '10' < '3' as strings)."
        ),
        cx="O(n + T * F) time for T tables and F foods, O(T * F) space",
        brute_cx="O(T * F * n) time - rescan all orders for every table and food cell",
        brute=r"""
# BRUTE FORCE: O(T * F * n) time - rescan all orders for every table and food cell
def display_table(orders):
    foods = sorted({food for _, _, food in orders})
    tables = sorted({int(table) for _, table, _ in orders})
    rows = [["Table"] + foods]

    for table in tables:
        row = [str(table)]
        for food in foods:
            row.append(str(sum(1 for _, t, f in orders if int(t) == table and f == food)))
        rows.append(row)

    return rows
""",
        solution=r"""
# OPTIMISED: O(n + T * F) time for T tables and F foods, O(T * F) space
# Idea: Nested dictionary (table -> food -> count) + sorted keys
def display_table(orders):
    per_table = defaultdict(Counter)
    foods = set()

    for _, table, food in orders:
        per_table[int(table)][food] += 1
        foods.add(food)

    foods = sorted(foods)
    rows = [["Table"] + foods]

    for table in sorted(per_table):
        rows.append([str(table)] + [str(per_table[table][food]) for food in foods])

    return rows
""",
    ),
    # ---- Making File Names Unique (LeetCode 1487) ----
    dict(
        title="Making File Names Unique",
        diff="M",
        lc=1487,
        slug="making-file-names-unique",
        prompt=(
            "Create folders one by one from names. If a name is already used, append the smallest suffix '(k)' with "
            "k >= 1 that makes it unused (the suffixed name then counts as used). Return the actual names that were "
            "created."
        ),
        sig="def get_folder_names(names: List[str]) -> List[str]:",
        fn="get_folder_names",
        tests=[
            ((["pes", "fifa", "gta", "pes(2019)"],), ["pes", "fifa", "gta", "pes(2019)"]),
            ((["gta", "gta(1)", "gta", "avalon"],), ["gta", "gta(1)", "gta(2)", "avalon"]),
            (
                (["onepiece", "onepiece(1)", "onepiece(2)", "onepiece(3)", "onepiece"],),
                ["onepiece", "onepiece(1)", "onepiece(2)", "onepiece(3)", "onepiece(4)"],
            ),
            ((["wano", "wano", "wano", "wano"],), ["wano", "wano(1)", "wano(2)", "wano(3)"]),
            ((["kaido", "kaido(1)", "kaido", "kaido(1)"],), ["kaido", "kaido(1)", "kaido(2)", "kaido(1)(1)"]),
        ],
        hints=[
            "Keep a set of all names created so far.",
            "Retrying k = 1, 2, 3, ... from scratch each time is correct but slow for many duplicates.",
            (
                "Remember, per base name, the next suffix to try (a dictionary name -> k). Resume from there and "
                "still check the set, because the suffixed name might already exist."
            ),
        ],
        pattern="Set of used names + per-name 'next suffix' memo",
        explain=(
            "A name's suffixes are tried in increasing order, and a suffix that was rejected once stays rejected "
            "(names are never freed), so the search can resume where it stopped last time. The memo only skips "
            "suffixes known to be taken; the set check still guards against a freshly created name that collides "
            "with a suffix form such as 'a(1)'."
        ),
        cx="O(n) amortised time, O(n) space",
        brute_cx="O(n * k) time - restart the suffix search at 1 for every duplicate",
        brute=r"""
# BRUTE FORCE: O(n * k) time - restart the suffix search at 1 for every duplicate
def get_folder_names(names):
    used = set()
    out = []

    for name in names:
        candidate = name
        k = 0
        while candidate in used:
            k += 1
            candidate = f"{name}({k})"
        used.add(candidate)
        out.append(candidate)

    return out
""",
        solution=r"""
# OPTIMISED: O(n) amortised time, O(n) space
# Idea: Set of used names + per-name 'next suffix' memo
def get_folder_names(names):
    used = set()
    next_suffix = defaultdict(int)
    out = []

    for name in names:
        candidate = name
        k = next_suffix[name]

        while candidate in used:
            k += 1
            candidate = f"{name}({k})"

        next_suffix[name] = k
        used.add(candidate)
        out.append(candidate)

    return out
""",
    ),
    # ---- Restore the Array From Adjacent Pairs (LeetCode 1743) ----
    dict(
        title="Restore the Array From Adjacent Pairs",
        diff="M",
        lc=1743,
        slug="restore-the-array-from-adjacent-pairs",
        prompt=(
            "An array of n distinct integers was lost; you are given every pair of ADJACENT elements "
            "adjacentPairs[i] = [u, v] in arbitrary order and either orientation. Return the original array (either "
            "the array or its reverse is accepted)."
        ),
        sig="def restore_array(adjacent_pairs: List[List[int]]) -> List[int]:",
        fn="restore_array",
        check=_restore_ok,
        tests=[
            (([[2, 1], [3, 4], [3, 2]],), [1, 2, 3, 4]),
            (([[4, -2], [1, 4], [-3, 1]],), [-2, 4, 1, -3]),
            (([[100000, -100000]],), [100000, -100000]),
        ],
        hints=[
            "The array is a path; each interior element has two neighbours and the two end elements have one.",
            "Build an adjacency map value -> list of neighbours.",
            (
                "Start from a value with exactly one neighbour (an end) and walk: at each step move to the "
                "neighbour that is not the previous element."
            ),
        ],
        pattern="Adjacency map; walk a path from an endpoint",
        explain=(
            "The pairs are the edges of a simple path over distinct values. Its endpoints are the only values of "
            "degree 1, so starting there and repeatedly stepping to the unvisited neighbour reproduces the sequence "
            "in O(n). The reverse walk from the other endpoint is equally valid."
        ),
        cx="O(n) time, O(n) space",
        brute_cx="O(n! * n) time - try every ordering of the values and test all adjacent pairs",
        brute=r"""
# BRUTE FORCE: O(n! * n) time - try every ordering of the values and test all adjacent pairs
def restore_array(adjacent_pairs):
    values = sorted({x for pair in adjacent_pairs for x in pair})
    wanted = sorted(sorted(p) for p in adjacent_pairs)
    for perm in itertools.permutations(values):
        if sorted(sorted(perm[i : i + 2]) for i in range(len(perm) - 1)) == wanted:
            return list(perm)
""",
        solution=r"""
# OPTIMISED: O(n) time, O(n) space
# Idea: Adjacency map; walk a path from an endpoint
def restore_array(adjacent_pairs):
    neighbours = defaultdict(list)

    for u, v in adjacent_pairs:
        neighbours[u].append(v)
        neighbours[v].append(u)

    start = next(x for x, nb in neighbours.items() if len(nb) == 1)
    out = [start]
    previous = None
    current = start

    while len(out) < len(adjacent_pairs) + 1:
        step = [x for x in neighbours[current] if x != previous][0]
        out.append(step)
        previous, current = current, step

    return out
""",
    ),
    # ---- Evaluate the Bracket Pairs of a String (LeetCode 1807) ----
    dict(
        title="Evaluate the Bracket Pairs of a String",
        diff="M",
        lc=1807,
        slug="evaluate-the-bracket-pairs-of-a-string",
        prompt=(
            "s contains lowercase letters and bracket pairs '(key)'. knowledge is a list of [key, value] pairs. "
            "Replace every '(key)' by its value, or by '?' if the key is unknown. (Brackets never nest.) Return the "
            "resulting string."
        ),
        sig="def evaluate(s: str, knowledge: List[List[str]]) -> str:",
        fn="evaluate",
        tests=[
            (("(name)is(age)yearsold", [["name", "bob"], ["age", "two"]]), "bobistwoyearsold"),
            (("hi(name)", [["a", "b"]]), "hi?"),
            (("(a)(a)(a)aaa", [["a", "yes"]]), "yesyesyesaaa"),
            (("abc", []), "abc"),
        ],
        hints=[
            (
                "Replacing with repeated str.replace for each pair is slow when there are many keys, and it cannot "
                "produce '?' for unknown keys."
            ),
            "Put the knowledge in a dictionary first.",
            (
                "Scan s once: outside brackets copy characters; on '(' collect characters up to ')' as the key and "
                "append dict.get(key, '?')."
            ),
        ],
        pattern="Dictionary lookup during a single parse",
        explain=(
            "A dictionary turns each key lookup into O(1). A single left-to-right pass either copies a literal "
            "character or consumes one bracket pair, so the total work is linear in the length of s regardless of "
            "how many knowledge entries there are."
        ),
        cx="O(len(s) + len(knowledge)) time, O(len(knowledge)) space",
        brute_cx="O(len(s) * len(knowledge)) time - for each pair rewrite the whole string, then mark leftovers",
        brute=r"""
# BRUTE FORCE: O(len(s) * len(knowledge)) time - for each pair rewrite the whole string, then mark leftovers
def evaluate(s, knowledge):
    for key, value in knowledge:
        s = s.replace(f"({key})", value)

    parts = s.split("(")
    out = parts[0]

    for part in parts[1:]:
        _, _, rest = part.partition(")")
        out += "?" + rest

    return out
""",
        solution=r"""
# OPTIMISED: O(len(s) + len(knowledge)) time, O(len(knowledge)) space
# Idea: Dictionary lookup during a single parse
def evaluate(s, knowledge):
    mapping = dict(knowledge)
    out = []
    i = 0

    while i < len(s):
        if s[i] == "(":
            j = s.index(")", i)
            out.append(mapping.get(s[i + 1 : j], "?"))
            i = j + 1
        else:
            out.append(s[i])
            i += 1

    return "".join(out)
""",
    ),
    # ---- Count Nice Pairs in an Array (LeetCode 1814) ----
    dict(
        title="Count Nice Pairs in an Array",
        diff="M",
        lc=1814,
        slug="count-nice-pairs-in-an-array",
        prompt=(
            "rev(x) is x with its decimal digits reversed. Count the pairs i < j with nums[i] + rev(nums[j]) == "
            "nums[j] + rev(nums[i]), modulo 1_000_000_007."
        ),
        sig="def count_nice_pairs(nums: List[int]) -> int:",
        fn="count_nice_pairs",
        tests=[
            (([42, 11, 1, 97],), 2),
            (([13, 10, 35, 24, 76],), 4),
            (([5],), 0),
            (([1, 1, 1],), 3),
        ],
        hints=[
            "Rearrange the equation so that i and j are on different sides.",
            "nums[i] - rev(nums[i]) == nums[j] - rev(nums[j]).",
            (
                "Compute key = x - rev(x) for each element; the answer is the number of pairs with equal keys: add "
                "the running count of each key as you go."
            ),
        ],
        pattern="Move variables to one side -> count equal keys with a hash map",
        explain=(
            "The condition is symmetric after moving terms: it says both elements have the same value of x - "
            "rev(x). So the problem becomes counting pairs with equal keys, which a Counter does in one pass "
            "(adding the number of earlier equal keys for each element)."
        ),
        cx="O(n * digits) time, O(n) space",
        brute_cx="O(n^2) time - test every pair against the original equation",
        brute=r"""
# BRUTE FORCE: O(n^2) time - test every pair against the original equation
def count_nice_pairs(nums):
    def rev(x):
        return int(str(x)[::-1])

    count = 0

    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + rev(nums[j]) == nums[j] + rev(nums[i]):
                count += 1

    return count % (10**9 + 7)
""",
        solution=r"""
# OPTIMISED: O(n * digits) time, O(n) space
# Idea: Move variables to one side -> count equal keys with a hash map
def count_nice_pairs(nums):
    seen = Counter()
    total = 0
    for x in nums:
        key = x - int(str(x)[::-1])
        total += seen[key]
        seen[key] += 1
    return total % (10**9 + 7)
""",
    ),
    # ---- Number of Pairs of Interchangeable Rectangles (LeetCode 2001) ----
    dict(
        title="Number of Pairs of Interchangeable Rectangles",
        diff="M",
        lc=2001,
        slug="number-of-pairs-of-interchangeable-rectangles",
        prompt=(
            "rectangles[i] = [width, height]. Two rectangles are interchangeable if they have the same width / "
            "height ratio. Count the pairs i < j of interchangeable rectangles."
        ),
        sig="def interchangeable_rectangles(rectangles: List[List[int]]) -> int:",
        fn="interchangeable_rectangles",
        tests=[
            (([[4, 8], [3, 6], [10, 20], [15, 30]],), 6),
            (([[4, 5], [7, 8]],), 0),
            (([[1, 1]],), 0),
            (([[2, 3], [4, 6], [6, 9]],), 3),
        ],
        hints=[
            "Comparing ratios with floating-point division can mis-compare equal fractions.",
            "Reduce each ratio to lowest terms with gcd: (w / g, h / g) is an exact, hashable key.",
            (
                "For each rectangle add the number of earlier rectangles with the same key, then increment that "
                "key's count."
            ),
        ],
        pattern="Exact normalised key (reduced fraction) + hash counting",
        explain=(
            "Two rectangles have the same ratio iff their reduced fractions are identical, and the reduced pair is "
            "an exact integer key. Counting equal keys as you scan counts each unordered pair exactly once. "
            "Cross-multiplying is the alternative for the brute-force check."
        ),
        cx="O(n log M) time (gcd), O(n) space",
        brute_cx="O(n^2) time - cross-multiply every pair",
        brute=r"""
# BRUTE FORCE: O(n^2) time - cross-multiply every pair
def interchangeable_rectangles(rectangles):
    count = 0
    for i in range(len(rectangles)):
        for j in range(i + 1, len(rectangles)):
            if rectangles[i][0] * rectangles[j][1] == rectangles[j][0] * rectangles[i][1]:
                count += 1
    return count
""",
        solution=r"""
# OPTIMISED: O(n log M) time (gcd), O(n) space
# Idea: Exact normalised key (reduced fraction) + hash counting
def interchangeable_rectangles(rectangles):
    seen = Counter()
    total = 0

    for w, h in rectangles:
        g = math.gcd(w, h)
        key = (w // g, h // g)
        total += seen[key]
        seen[key] += 1

    return total
""",
    ),
    # ---- Longest Palindrome by Concatenating Two Letter Words (LeetCode 2131) ----
    dict(
        title="Longest Palindrome by Concatenating Two Letter Words",
        diff="M",
        lc=2131,
        slug="longest-palindrome-by-concatenating-two-letter-words",
        prompt=(
            "words are strings of exactly two lowercase letters. Choose some of them (each at most once) and "
            "concatenate them in any order to form the longest possible palindrome. Return its length (0 if none)."
        ),
        sig="def longest_palindrome(words: List[str]) -> int:",
        fn="longest_palindrome",
        tests=[
            ((["lc", "cl", "gg"],), 6),
            ((["ab", "ty", "yt", "lc", "cl", "ab"],), 8),
            ((["cc", "ll", "xx"],), 2),
            ((["ab"],), 0),
            ((["aa", "aa", "aa"],), 6),
        ],
        hints=[
            (
                "A word 'xy' (x != y) is useful only together with its mirror 'yx': one goes on the left half, the "
                "other on the right half."
            ),
            "A word like 'aa' can pair with another 'aa', and ONE leftover 'aa' may sit in the exact middle.",
            (
                "Count the words; add 4 per mirror pair (min of the two counts), 4 per pair of identical-letter "
                "words, and +2 at the end if any identical-letter word is left over."
            ),
        ],
        pattern="Counting mirror pairs with a hash map",
        explain=(
            "A palindrome of two-letter blocks pairs every block with its reverse on the opposite side. "
            "Different-letter words 'xy' and 'yx' pair min(count) times; same-letter words pair with themselves "
            "floor(count / 2) times, and at most one single same-letter word can occupy the centre. Each pair "
            "contributes 4 letters, the centre 2."
        ),
        cx="O(n) time, O(n) space",
        brute_cx="O(n! * n) time - try every ordered selection of words and test for a palindrome",
        brute=r"""
# BRUTE FORCE: O(n! * n) time - try every ordered selection of words and test for a palindrome
def longest_palindrome(words):
    best = 0
    for size in range(1, len(words) + 1):
        for chosen in itertools.permutations(words, size):
            text = "".join(chosen)
            if text == text[::-1]:
                best = max(best, len(text))
    return best
""",
        solution=r"""
# OPTIMISED: O(n) time, O(n) space
# Idea: Counting mirror pairs with a hash map
def longest_palindrome(words):
    count = Counter(words)
    total = 0
    centre = False

    for word, c in count.items():
        mirror = word[::-1]
        if word == mirror:
            total += c // 2 * 4
            if c % 2:
                centre = True
        elif word < mirror:
            total += min(c, count[mirror]) * 4

    return total + (2 if centre else 0)
""",
    ),
    # ---- Find All Lonely Numbers in the Array (LeetCode 2150) ----
    dict(
        title="Find All Lonely Numbers in the Array",
        diff="M",
        lc=2150,
        slug="find-all-lonely-numbers-in-the-array",
        prompt=(
            "A number x is lonely if it appears exactly once in nums and neither x - 1 nor x + 1 appears in nums. "
            "Return all lonely numbers in any order."
        ),
        sig="def find_lonely(nums: List[int]) -> List[int]:",
        fn="find_lonely",
        compare="unordered",
        tests=[
            (([10, 6, 5, 8],), [10, 8]),
            (([1, 3, 5, 3],), [1, 5]),
            (([7],), [7]),
            (([2, 2],), []),
            (([1, 2],), []),
        ],
        hints=[
            "You need two facts about each value: how many times it occurs, and whether its neighbours exist.",
            "A Counter gives O(1) answers to both questions.",
            "Keep x when count[x] == 1 and count[x - 1] == 0 and count[x + 1] == 0.",
        ],
        pattern="Frequency map with neighbour lookups",
        explain=(
            "Loneliness is a local property: it depends only on the multiplicity of x and the presence of x - 1 and "
            "x + 1. A Counter provides these in O(1); Counter returns 0 for missing keys, so no existence check is "
            "needed. (Sorting and comparing neighbours is the alternative.)"
        ),
        cx="O(n) time, O(n) space",
        brute_cx="O(n^2) time - scan the array for every value's count and neighbours",
        brute=r"""
# BRUTE FORCE: O(n^2) time - scan the array for every value's count and neighbours
def find_lonely(nums):
    return [x for x in nums if nums.count(x) == 1 and (x - 1) not in nums and (x + 1) not in nums]
""",
        solution=r"""
# OPTIMISED: O(n) time, O(n) space
# Idea: Frequency map with neighbour lookups
def find_lonely(nums):
    count = Counter(nums)
    return [x for x in nums if count[x] == 1 and count[x - 1] == 0 and count[x + 1] == 0]
""",
    ),
    # ---- Minimum Consecutive Cards to Pick Up (LeetCode 2260) ----
    dict(
        title="Minimum Consecutive Cards to Pick Up",
        diff="M",
        lc=2260,
        slug="minimum-consecutive-cards-to-pick-up",
        prompt=(
            "Pick up a block of consecutive cards that contains two cards with the same value. Return the minimum "
            "number of cards in such a block, or -1 if no two cards match."
        ),
        sig="def minimum_card_pickup(cards: List[int]) -> int:",
        fn="minimum_card_pickup",
        tests=[
            (([3, 4, 2, 3, 4, 7],), 4),
            (([1, 0, 5, 3],), -1),
            (([1, 1],), 2),
            (([5, 5, 5],), 2),
        ],
        hints=[
            (
                "The best block for a repeated value ends with two occurrences that are NEXT to each other in that "
                "value's occurrence list."
            ),
            "Remember the last index where each value was seen.",
            (
                "At index j with value v seen before at index i, the block length is j - i + 1; keep the minimum "
                "and update last[v] = j."
            ),
        ],
        pattern="Last-seen index map; distance between consecutive occurrences",
        explain=(
            "For a fixed value, a block containing two of its cards must contain two occurrences; the shortest such "
            "block uses two consecutive occurrences. A dictionary of last-seen positions produces exactly those "
            "pairs while scanning once."
        ),
        cx="O(n) time, O(n) space",
        brute_cx="O(n^2) time - for each card search forward for its next copy",
        brute=r"""
# BRUTE FORCE: O(n^2) time - for each card search forward for its next copy
def minimum_card_pickup(cards):
    best = None

    for i in range(len(cards)):
        for j in range(i + 1, len(cards)):
            if cards[i] == cards[j]:
                length = j - i + 1
                best = length if best is None else min(best, length)
                break

    return -1 if best is None else best
""",
        solution=r"""
# OPTIMISED: O(n) time, O(n) space
# Idea: Last-seen index map; distance between consecutive occurrences
def minimum_card_pickup(cards):
    last = {}
    best = float("inf")
    for j, v in enumerate(cards):
        if v in last:
            best = min(best, j - last[v] + 1)
        last[v] = j
    return -1 if best == float("inf") else best
""",
    ),
    # ---- Node With Highest Edge Score (LeetCode 2374) ----
    dict(
        title="Node With Highest Edge Score",
        diff="M",
        lc=2374,
        slug="node-with-highest-edge-score",
        prompt=(
            "A directed graph has n nodes 0..n-1 and each node i has exactly one outgoing edge to edges[i]. The "
            "edge score of a node is the sum of the indices of all nodes that point to it. Return the node with the "
            "highest edge score (the smallest index if tied)."
        ),
        sig="def edge_score(edges: List[int]) -> int:",
        fn="edge_score",
        tests=[
            (([1, 0, 0, 0, 0, 7, 7, 5],), 7),
            (([2, 0, 0, 2],), 0),
            (([1, 0],), 0),
            (([1, 2, 0],), 0),
        ],
        hints=[
            "Each node contributes its own index to exactly one target.",
            "Accumulate score[edges[i]] += i in one pass.",
            (
                "Return the index with the maximum score, preferring the smaller index on ties (max over scores "
                "with a stable scan, or compare with > only)."
            ),
        ],
        pattern="Accumulate into a hash map / array by target",
        explain=(
            "The score is a sum over incoming edges, so one pass that adds each source index to its target's total "
            "computes all scores. Scores can exceed 32 bits for large n, which Python handles natively. Scanning "
            "indices in increasing order and replacing the best only on a strictly larger score keeps the smallest "
            "index on ties."
        ),
        cx="O(n) time, O(n) space",
        brute_cx="O(n^2) time - for every node sum the indices of all nodes pointing to it",
        brute=r"""
# BRUTE FORCE: O(n^2) time - for every node sum the indices of all nodes pointing to it
def edge_score(edges):
    best_node, best_score = 0, -1
    for node in range(len(edges)):
        score = sum(i for i, target in enumerate(edges) if target == node)
        if score > best_score:
            best_node, best_score = node, score
    return best_node
""",
        solution=r"""
# OPTIMISED: O(n) time, O(n) space
# Idea: Accumulate into a hash map / array by target
def edge_score(edges):
    score = [0] * len(edges)

    for i, target in enumerate(edges):
        score[target] += i

    best = 0

    for node in range(1, len(edges)):
        if score[node] > score[best]:
            best = node

    return best
""",
    ),
    # ---- Most Popular Video Creator (LeetCode 2456) ----
    dict(
        title="Most Popular Video Creator",
        diff="M",
        lc=2456,
        slug="most-popular-video-creator",
        prompt=(
            "creators[i], ids[i], views[i] describe video i. A creator's popularity is the total views of all their "
            "videos. For every creator with the highest popularity return [creator, id] where id is their most "
            "viewed video (the lexicographically smallest id if tied). Answers may be in any order."
        ),
        sig="def most_popular_creator(creators: List[str], ids: List[str], views: List[int]) -> List[List[str]]:",
        fn="most_popular_creator",
        compare="unordered",
        tests=[
            (
                (["alice", "bob", "alice", "chris"], ["one", "two", "three", "four"], [5, 10, 5, 4]),
                [["alice", "one"], ["bob", "two"]],
            ),
            ((["alice", "alice", "alice"], ["a", "b", "c"], [1, 2, 2]), [["alice", "b"]]),
            ((["x"], ["v"], [0]), [["x", "v"]]),
        ],
        hints=[
            "Group by creator: you need a running total and the current best video.",
            "A creator's best video is the one with the largest views; break ties with the smaller id.",
            (
                "Keep a dict creator -> [total, best_views, best_id], update per video, then output every creator "
                "whose total equals the maximum total."
            ),
        ],
        pattern="Group-by with a running aggregate and a tie-breaking best",
        explain=(
            "One dictionary entry per creator holds the sum of views and the best (views, id) pair, compared as "
            "(-views, id) so a higher view count wins and ties fall to the smaller id. After the pass, the maximum "
            "total identifies the most popular creators."
        ),
        cx="O(n) time, O(n) space",
        brute_cx="O(n * c) time - for every creator rescan all videos for the total and the best video",
        brute=r"""
# BRUTE FORCE: O(n * c) time - for every creator rescan all videos for the total and the best video
def most_popular_creator(creators, ids, views):
    totals = {c: sum(v for cc, v in zip(creators, views) if cc == c) for c in set(creators)}
    top = max(totals.values())
    out = []

    for creator, total in totals.items():
        if total == top:
            videos = [(-v, i) for c, i, v in zip(creators, ids, views) if c == creator]
            out.append([creator, min(videos)[1]])

    return out
""",
        solution=r"""
# OPTIMISED: O(n) time, O(n) space
# Idea: Group-by with a running aggregate and a tie-breaking best
def most_popular_creator(creators, ids, views):
    total = defaultdict(int)
    best = {}

    for creator, video, count in zip(creators, ids, views):
        total[creator] += count
        key = (-count, video)
        if creator not in best or key < best[creator]:
            best[creator] = key

    top = max(total.values())

    return [[creator, best[creator][1]] for creator in total if total[creator] == top]
""",
    ),
    # ---- Subdomain Visit Count (LeetCode 811) ----
    dict(
        title="Subdomain Visit Count",
        diff="M",
        lc=811,
        slug="subdomain-visit-count",
        prompt=(
            "Each entry of cpdomains is 'count domain', e.g. '9001 discuss.leetcode.com', meaning that domain was "
            "visited count times. A visit to a domain also counts for each of its parent domains ('leetcode.com', "
            "'com'). Return the total visits of every (sub)domain as 'count domain' strings, in any order."
        ),
        sig="def subdomain_visits(cpdomains: List[str]) -> List[str]:",
        fn="subdomain_visits",
        compare="unordered",
        tests=[
            ((["9001 discuss.leetcode.com"],), ["9001 leetcode.com", "9001 discuss.leetcode.com", "9001 com"]),
            (
                (["900 google.mail.com", "50 yahoo.com", "1 intel.mail.com", "5 wiki.org"],),
                [
                    "901 mail.com",
                    "50 yahoo.com",
                    "900 google.mail.com",
                    "5 wiki.org",
                    "5 org",
                    "1 intel.mail.com",
                    "951 com",
                ],
            ),
            ((["5 a.com"],), ["5 a.com", "5 com"]),
        ],
        hints=[
            "Split each entry into the count and the domain.",
            "The suffixes of a domain split at dots are exactly its parent domains: a.b.c -> a.b.c, b.c, c.",
            (
                "Add the count to a dictionary entry for every suffix, then format the dictionary as 'count domain' "
                "strings."
            ),
        ],
        pattern="Accumulate counts for every dot-suffix in a hash map",
        explain=(
            "A visit to a.b.c is a visit to every suffix obtained by removing leading labels, so each entry adds "
            "its count to each suffix key. A Counter holds the totals; the answer is the Counter formatted as "
            "strings."
        ),
        cx="O(total length of domains) time, O(distinct subdomains) space",
        brute_cx="O(D^2 * L) time - for every distinct subdomain scan all entries that end with it",
        brute=r"""
# BRUTE FORCE: O(D^2 * L) time - for every distinct subdomain scan all entries that end with it
def subdomain_visits(cpdomains):
    entries = [(int(c), d) for c, d in (item.split() for item in cpdomains)]
    subdomains = set()

    for _, domain in entries:
        labels = domain.split(".")
        for i in range(len(labels)):
            subdomains.add(".".join(labels[i:]))

    out = []

    for sub in subdomains:
        total = sum(c for c, d in entries if d == sub or d.endswith("." + sub))
        out.append(f"{total} {sub}")

    return out
""",
        solution=r"""
# OPTIMISED: O(total length of domains) time, O(distinct subdomains) space
# Idea: Accumulate counts for every dot-suffix in a hash map
def subdomain_visits(cpdomains):
    total = Counter()
    for item in cpdomains:
        count, domain = item.split()
        labels = domain.split(".")
        for i in range(len(labels)):
            total[".".join(labels[i:])] += int(count)
    return [f"{count} {domain}" for domain, count in total.items()]
""",
    ),
]
