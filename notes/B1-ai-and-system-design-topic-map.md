# B1 - Topic map: System Design & AI engineering (concepts first, no timeline)

> DSA is the *vocabulary*; system design and AI engineering are the *sentences*. This page lists the concepts to learn, why each matters, the DSA idea underneath it, and a **local mini-lab** you can run on your laptop with plain Python.
> Status: concept map (not yet full hand-notes). Stable concepts (CAP, quorums, BM25, HNSW, LoRA) are textbook; fast-moving items (agent protocols, security lists, interview formats) carry an **as-of date** and a source in the Sources list at the bottom. Last reviewed: **2026-11-15**.

## Part 1 - System design

### 1.1 How to approach any design question (the paper method again)
1. **Requirements:** functional (what) vs non-functional (scale, latency, availability, consistency, cost). Ask, do not assume.
2. **Estimate:** users -> requests/second -> storage/day -> bandwidth. (Powers of two, "1 day ~ 10^5 s", read:write ratio.)
3. **API & data model:** the 3-5 core endpoints and entities.
4. **High-level design:** client -> LB -> services -> cache -> DB / queue / object store.
5. **Deep dive** on the 1-2 hardest parts (the bottleneck): partitioning, hot keys, consistency, failure.
6. **Trade-offs & failure modes:** what breaks, how you detect it, how you recover.

### 1.2 Concept blocks
| Block | Core ideas to learn | DSA underneath | Local mini-lab |
|---|---|---|---|
| Estimation & latency | QPS, peak factor, storage maths, latency numbers (memory vs SSD vs network) | arithmetic, log scales | write a `capacity(users, rps, size)` calculator |
| Load balancing | L4 vs L7, round-robin / least-connections / consistent hashing, health checks | modulo, hashing, sorted ring + binary search | **consistent-hash ring** with virtual nodes; measure key movement when a node is added |
| Caching | cache-aside / write-through / write-back, TTL, eviction (LRU/LFU), stampede, hot keys, CDN | hash map + doubly linked list, heap for TTL | LRU+TTL cache; simulate a stampede and fix it with request coalescing |
| Databases | SQL vs NoSQL, indexes (B-tree vs LSM), replication, sharding, ACID vs BASE, isolation levels | B-tree = balanced search tree, LSM = merge of sorted runs | tiny KV store with a write-ahead log + compaction (k-way merge) |
| Partitioning | range vs hash sharding, rebalancing, hot partitions, geo-sharding | hashing, binary search, quadtree / geohash (trie) | shard router + rebalancer |
| Consistency & CAP | CAP/PACELC, strong vs eventual, quorum (R+W>N), vector clocks, idempotency | sets, partial orders | quorum read/write simulator with failures |
| Queues & streams | queue vs log, partitions, consumer groups, at-least/at-most/exactly-once, ordering, backpressure | queue/deque, heap for delayed jobs | in-memory pub/sub with consumer groups and offsets |
| Rate limiting | token bucket, leaky bucket, fixed/sliding window | deque (sliding window), counters | implement all three; compare burst behaviour |
| Search | inverted index, tokenisation, TF-IDF/BM25, autocomplete | hash map of postings lists, trie, heap for top-k | mini search engine over a folder of text files |
| Unique IDs & short links | snowflake IDs, base62, collisions, sequence generators | bit manipulation, base conversion | base62 URL shortener + collision handling |
| Reliability | timeouts, retries with exponential backoff + jitter, circuit breaker, bulkheads, idempotent writes | state machines | circuit-breaker class with a fake flaky service |
| Observability | metrics/logs/traces, SLI/SLO/error budget, p50/p95/p99 | heaps / sketches for percentiles | latency histogram + percentile calculator |
| Security basics | authn vs authz, OAuth2/OIDC, JWT, secrets, multi-tenancy isolation | hashing, signatures | sign and verify a JWT by hand with `hmac` |

### 1.3 Classic designs to be able to draw end to end
URL shortener - rate limiter - key-value store - distributed cache - unique ID generator - news feed - chat / messaging - notification system - web crawler - typeahead / autocomplete - file storage (Dropbox-style) - video streaming - ride-hailing (geo index) - payment system (idempotency!) - search engine - metrics/monitoring system.
For each, be able to answer: *what is the bottleneck, what is the partition key, what is the consistency requirement, how does it fail?*

## Part 2 - AI / LLM engineering

### 2.1 Concept blocks
| Block | Core ideas to learn | DSA / maths underneath | Local mini-lab |
|---|---|---|---|
| ML basics | features/labels, loss, gradient descent, bias-variance, train/val/test, precision/recall/F1 | arithmetic, calculus intuition | gradient descent for linear regression in 30 lines of numpy |
| Embeddings & similarity | vectors, dot product, cosine similarity, normalisation, curse of dimensionality | linear algebra, heap for top-k | brute-force kNN over sentence vectors; measure latency vs size |
| Tokenisation & LLM basics | tokens, BPE, context window, attention (concept), sampling (temperature, top-p), logprobs | priority merges (heap), hashing, tries | toy BPE tokenizer; temperature-sampling demo |
| Prompting & structured output | roles, few-shot, chain-of-thought, JSON schema output, prompt versioning | - | prompt test-suite with expected outputs |
| **RAG** | chunking (size/overlap), embeddings, vector index (flat / IVF / HNSW), **hybrid search (BM25 + dense, fused with reciprocal rank fusion: score = sum of 1/(k + rank), k = 60 by convention)**, reranking, query rewriting, citations | sliding window (chunk overlap), inverted index, graph (HNSW), heap | BM25 from scratch + dense kNN + reciprocal-rank-fusion; measure **recall@k** on a golden set |
| Agents | tool calling, ReAct loop, planning, memory (short/long), guardrails, multi-agent orchestration, MCP (Model Context Protocol: an open JSON-RPC standard for connecting agents to tools and data; **as of 2026-11-15** stewarded by the Linux Foundation's Agentic AI Foundation, and its newest spec revision moves to a stateless design - check the current spec version before building) | DAG / topological order for workflows, state machines, queues | a ReAct loop with a stubbed model and two tools; add a step limit + loop detection |
| Evaluation | golden datasets, offline vs online eval, LLM-as-judge (and its biases), regression suites, groundedness/faithfulness | sets, statistics | eval harness: run cases, score, diff vs the previous run |
| Fine-tuning | SFT, LoRA/QLoRA (low-rank adapters), preference tuning (idea), when *not* to fine-tune | low-rank matrices | count trainable parameters for full vs LoRA on a given layer shape |
| Serving & cost | batching, KV cache, quantisation, streaming, latency/throughput, caching (exact + semantic), routing to cheaper models | hash map (cache), LRU, heap (scheduler), binary search (threshold tuning) | semantic-cache prototype + hit-rate/cost report |
| Data pipelines & MLOps | ingestion, dedup (hashing / MinHash), versioning, orchestration (DAGs), monitoring drift | hashing, topological sort | DAG runner with retries and a dependency graph |
| Safety & security | prompt injection, data exfiltration, PII handling, least-privilege tools, tenant isolation; use the **OWASP Top 10 for LLM Applications (2025 edition)** as the checklist (LLM01 Prompt Injection, LLM02 Sensitive Information Disclosure, LLM03 Supply Chain, LLM07 System Prompt Leakage, LLM08 Vector and Embedding Weaknesses, LLM10 Unbounded Consumption, ...) | access-control sets | red-team list: 10 injection prompts against your own RAG app |

### 2.2 The bridge: where DSA shows up in AI systems
- **Top-k retrieval** -> heap. **Approximate nearest neighbour (HNSW)** -> layered graphs + greedy search.
- **Beam search / Viterbi** -> DP. **Edit distance** -> spell-correction and fuzzy matching.
- **Chunking with overlap** -> sliding window. **Deduplication** -> hashing / MinHash + union-find.
- **Agent workflows** -> DAGs: topological sort, cycle detection, parallel stages.
- **Caches / rate limits for model APIs** -> LRU, token bucket, sliding-window counters.

## Sources (checked 2026-11-15)
- HNSW: Malkov & Yashunin, *Efficient and robust approximate nearest neighbor search using Hierarchical Navigable Small World graphs*, IEEE TPAMI 2020 - https://arxiv.org/abs/1603.09320
- Reciprocal rank fusion with k = 60: Cormack & Clarke (2009), as cited in implementation docs such as https://docs.rs/crate/nodedb-vector/0.3.0/source/src/hybrid/rrf.rs (secondary source; read the original paper before quoting it).
- MCP governance and spec: donated to the Linux Foundation's Agentic AI Foundation on 2025-12-09 (https://mcp.directory/blog/mcp-foundation-linux-foundation-aaif-2026-explained); stable spec 2025-11-25 and a newer stateless revision (2026-07-28) reported at https://www.theregister.com/a/5280027 and https://aaif.io/blog/mcp-graduates-to-enterprise-infrastructure-stateless-architecture-formal-governance-and-security
- OWASP Top 10 for LLM Applications 2025: https://www.invicti.com/blog/web-security/owasp-top-10-risks-llm-security-2025 (one vendor page mentions a later 2026 edition; confirm on the OWASP GenAI Security Project site, which I could not verify here).
- Not re-verified in this pass because they are textbook and stable: CAP/PACELC, quorum R+W>N, token/leaky bucket, BM25, LoRA/QLoRA, KV cache.

## How to use this map
Pick a block, read its concepts, then do the **mini-lab on paper first** (data structures + invariants), then in code with tests - same loop as `notes/00-foundations.md`. Blocks marked with a DSA idea you have not met yet tell you which DSA topic to study first.
