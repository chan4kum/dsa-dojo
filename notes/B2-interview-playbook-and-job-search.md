# B2 - Interview playbook & job-search system

> Knowing algorithms gets you to the interview; **communicating a method under pressure** gets you the offer. This note is the part of the craft that is not in any problem list.

## 1. The six-step protocol for any coding problem (about 35-40 minutes)
| step | what you do | what you say (out loud) |
|---|---|---|
| **U**nderstand | restate, ask about input size, duplicates, negatives, empty, sorted?, return what? | "So given X I return Y. Can the array be empty? How large can n be?" |
| **M**atch | name the pattern from the signals (see `00-pattern-finder.md`) | "This looks like a sliding window because we want a contiguous range with a monotone condition." |
| **P**lan | brute force first (state its cost), then the improvement | "Brute force is O(n^2). The wasted work is X, so I can use Y to get O(n)." |
| **I**mplement | write clean code with meaningful names; narrate invariants, not syntax | "`left` always marks the start of a valid window." |
| **R**eview | dry-run a small example and one edge case BY HAND | "Let me trace [2,3,1] ... the window grows to ... " |
| **E**valuate | time and space, trade-offs, follow-ups | "O(n) time, O(k) space. If the stream were unbounded I'd ..." |

Why brute force first: it proves you understand the problem, gives you a correct fallback, and shows the interviewer the *reason* for your optimisation. Every problem in this repo shows brute force and optimised side by side for exactly this habit.

## 2. If you are stuck (the 6-move protocol)
1. Re-read the prompt - which constraint have I not used? (sorted? positive? k small? values bounded?)
2. Solve a tiny example by hand and watch what YOU do.
3. Say the brute force and ask "what work is repeated?"
4. Run down the pattern finder's signals aloud.
5. Simplify: drop a constraint, solve the easier version, then add it back.
6. Ask for a hint *specifically*: "I'm considering a hash map vs sorting - is the order important here?" Interviewers reward direction, not silence.

## 3. Edge-case checklist (say two of these before coding)
empty / single element / all equal / already sorted / reverse sorted / negatives / zeros / duplicates / maximum size / overflow (mention it, even in Python) / cycles in a graph / disconnected graph / single-node tree / skewed tree.

## 4. Templates for stating complexity
- "Each element is pushed and popped at most once, so O(n) time; the stack can hold n items so O(n) space."
- "The loop inside the loop is amortised: the inner pointer only moves forward, total 2n steps."
- "Sorting dominates: O(n log n); the rest is linear."
- Recursion: "depth equals the tree height h, so O(h) stack space - O(n) in the worst case for a skewed tree."

## 5. Python pitfalls that cost people offers
- Mutable default arguments (`def f(a, seen=[])`).
- `grid = [[0]*C]*R` shares rows - use a comprehension.
- `list.pop(0)` / `insert(0, x)` are O(n): use `deque`.
- `a = b` aliases lists; copy with `b[:]` or `list(b)`; record results with `path[:]` in backtracking.
- Floor division and modulo with negatives (`-7 // 2 == -4`); to truncate toward zero use `int(a / b)` only for small values (float division loses precision beyond about 2^53) - for big integers use `-(-a // b)` or compare signs.
- Recursion limit (default 1000): deep DFS needs an explicit stack or `sys.setrecursionlimit`.
- `s = piece + s` / `s += piece` in a loop can be O(n^2) (each step may copy the string; CPython's in-place shortcut for `+=` is not guaranteed): collect pieces, `''.join`.
- `heapq` is a MIN-heap: negate for max-heap; add a tie-breaker so payloads are never compared.

## 6. "You are ready when..." (a checklist, not a calendar)
- You can name the pattern for a new problem within two minutes **before** coding (`python dsa.py quiz 10` - aim for 8/10).
- For every topic you can explain in one minute why its template is correct (the "teach it back" box at the end of each note).
- You solve a medium in about 25 minutes including a hand-traced test, and state both the brute-force and optimal complexity.
- You have redone, from a blank file, every problem in `python dsa.py review`.
- You have practised speaking while coding at least a few times with another person or a recorder.

## 7. Behavioural rounds (every large company has them)
Prepare **six stories** from real work; each should be usable for several questions. Use STAR: Situation (1 sentence), Task (your responsibility), Action (what *you* did - 60% of the time), Result (a number if you have one) + what you learned.
Story bank: a hard technical decision, a conflict with a colleague, a failure and what changed, leading without authority, a deadline or ambiguity, something you built that you are proud of, and a time you influenced a product or architecture decision.
Many companies publish their values or leadership principles on their careers sites - read them and map your stories to them.

## 8. The job-search system (treat it like a pipeline, not a lottery)
1. **Target list**: 30-50 companies in 3 tiers (dream / good / practice). Practise on tier 3 first.
2. **Resume**: one page per ~10 years, every bullet = *action + scope + measurable result* ("Cut batch-inference cost 38% by ... serving 4M requests/day"). Put keywords from the target job descriptions in naturally.
3. **Referrals beat cold applications.** Short message: who you are (1 line), why this role/team (1 line), one relevant proof (1 line), a specific small ask ("would you be open to referring me or pointing me to the right recruiter?"). Follow up once after about a week.
4. **Track everything** in a sheet: company, role, link, date applied, referral?, stage, next action + date, contact, notes. Review weekly; the pipeline shows where you leak (no replies = resume/targeting; screens fail = coding/communication; onsites fail = depth/system design).
5. **Prepare per stage**: recruiter screen (story + salary range research), phone screen (1-2 problems), onsite (coding x2-3, system design, behavioural, sometimes domain deep-dive).
6. **Offers**: always ask for time; compare total compensation (base, bonus, equity vesting, joining bonus), growth, team, and manager; negotiate respectfully with evidence (other offers, market data). Never lie about competing offers.
7. **After every interview write 5 lines**: what was asked, what went well, what slipped, one thing to drill, follow-up email sent.

## 8b. AI-assisted coding rounds (reported, as of 2026-11-15 - formats are pilots and vary by team)
- **Meta**: an AI-enabled coding round has been reported since October 2025, replacing one of the two onsite coding rounds (about 60 minutes, one staged problem, approved assistant inside the editor). The other round stays a classic no-AI algorithm interview.
- **Google**: reported in 2026 as a pilot of a "human-led, AI-assisted" **code comprehension** round (read, debug and improve an existing codebase with Gemini available); classic algorithm rounds remain.
- Other companies differ (some forbid AI in live coding unless the interview is explicitly AI-assisted and announced in advance). **Ask your recruiter which format you will get.**
- What is scored (as reported): breaking the problem down before prompting, directing the assistant precisely, **verifying and testing its output**, and spotting its bugs. You are still graded on your own judgement, so the habits in this repo (state brute force, hand-trace, test edge cases, state complexity) are exactly what carries over.
- Sources are mostly secondary (news and prep sites quoting internal documents), so treat details as indicative, not contractual: https://www.greatfrontend.com/blog/frontend-interview-process-at-google-amazon-and-meta-what-to-expect , https://www.byteherald.com/2026/10/google-changed-coding-interview-ai-is.html , https://medium.com/@fahimulhaq/meta-just-transformed-their-coding-interviews-with-ai-heres-what-developers-must-know-363b50dceda4

## 9. AI / LLM engineer track (what is asked besides coding)
- Coding rounds are the same patterns (see the pattern finder) - often plus data-manipulation in Python/SQL and a small ML or retrieval implementation.
- **ML system design**: problem framing, data & labels, features/embeddings, model choice, serving and latency, evaluation (offline and online), monitoring and drift, cost. Walk the lifecycle out loud.
- **LLM/RAG design**: chunking & indexing, retrieval (dense + sparse hybrid), re-ranking, prompt/context assembly, caching, guardrails, evaluation of retrieval and of answers, observability, cost and latency budgets, safety.
- **LLMOps**: versioned prompts/models, CI for evals, canary releases, rollback, secrets, rate limits.
- Practise with `notes/B1-ai-and-system-design-topic-map.md` and prepare one deep project story (problem -> design -> trade-offs -> measured impact -> what you would change).

## 10. Day-before checklist
Sleep. Re-read your six stories. Re-do two problems you already know (confidence, not learning). Test your audio/video/IDE setup. Prepare 3 questions to ask the interviewer (team, how success is measured, what the first project would be).
