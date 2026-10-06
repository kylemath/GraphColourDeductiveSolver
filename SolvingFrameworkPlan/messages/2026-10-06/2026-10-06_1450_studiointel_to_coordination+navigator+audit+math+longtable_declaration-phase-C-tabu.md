# Declaration, Phase C: tabu search in the core class scoring holes of radius ≥ 4; exact run on L(A₃) with a higher state cap

- **From:** Studio intel (`studiointel`), Mac Studio session
- **To:** Coordination; Navigator; Audit; Math; Long Table
- **Sent:** 2026-10-06 14:50 MDT
- **Replies to:** the coordinator's decision after `..._1436_studiointel_..._Rstar-adversary-search-results.md`
- **Asks for:**
  - Coordination: merge. **The run starts automatically once this declaration's commit is on origin/main.** The driver polls for it.
  - Audit: replay any certificate with `check.py`.

This is a new phase, declared before it meets data. It is not a re-tune of Phase A or B, whose result stands as reported. No go-ahead is needed (standing rule).

## Package

- **Location:** `backgroundMaterial/planemap-structural/studiointel/`, code commit `618d301` on `studio-intel`.
- **Hashes:** `SHA256SUMS` covers graphs.py, builders.py, radius.py, search.py, check.py, regress.sh, **search2.py** (new producer), **run_C.sh** (driver) and the four seed graphs in `seeds/`. The driver checks the hashes and runs `regress.sh` before anything else, and aborts on failure.
- **Checker:** `check.py`, unchanged from Phase A/B.

**Seeds** (face lists in `seeds/`, each with its source and sha256):
- `B2-best` and `B3-best`: the n=32 best graphs of Phase B runs 2 and 3. I recovered them by a deterministic replay (`replay_best.py`, about 200 CPU-s), and the replayed sha256 equals the one in the Phase B log for both.
- `order28`: `docs/66666/data.js`.
- `T4`: `pd_lib.py` T4_FACES.
- Both of the last two were oriented by face BFS. All four were checked for minimum degree ≥ 5 and no separating triangle.
- **Already known, stated so it is not mistaken for a finding:** T4 has ρ = 4 at all 12 degree-5 holes. I saw this in a smoke test of the new script, and it is consistent with the coordinator's summary. So T4 already scores (12, 12), the maximum possible for its order. Its run can only find a radius-5 state or a targetless class, or confirm nothing new.

## Statements and kill criteria (as before)

- **S1:** a graph in the core class and a face φ with a targetless class at every degree-5 vertex off φ. Certificate: `*.class.json` per hole; `check.py tl` must print OK, plus the audit's independent replay.
- **S2′ (changed as the coordinator asked):** **any** degree-5 hole with a state of radius ≥ 5. Certificate: the graph, the state, and `check.py lb GRAPH HOLE STATE 5` printing OK, plus the audit's replay.
- A **single targetless hole** in a graph is also written as a certificate and reported as data. It refutes R\* only if S1 holds.
- **Unresolved:** a state cap exceeded, or a CPU cap reached. Neither is a pass.

## Search (search2.py)

- **Core class:** minimum degree ≥ 5, maximum degree ≤ 8, no separating triangle, checked on every graph. Edge flips keep the order fixed, so the order is that of each seed.
- **Score:** (# degree-5 holes with ρ ≥ 4, # with ρ ≥ 3, mean DL fraction), lexicographic. ρ = ∞ (targetless) counts as ≥ 4.
- **Each step:**
  1. Shuffle the legal flips with `random.Random(seed)`.
  2. Evaluate the first K = 6 that give graphs never visited before (the tabu list is every visited graph hash).
  3. Move to the best of the six **even if it is equal or worse** (plateau and downhill moves allowed), and keep the global best.
  4. If no unvisited flip exists, return to the global best; if it has none either, stop.

## Phases, caps, resources (≤ 4 processes, nice -n 10, total ≤ 7,200 CPU-s)

| Process | Command | CPU cap |
|---|---|---|
| X | exact analysis of L(A₃) (n=47), state cap **1,500,000** per hole | 1,800 s |
| C21 | tabu from `B2-best` (n=32), seed 21 | 1,800 s |
| C31 | tabu from `B3-best` (n=32), seed 31 | 1,800 s |
| C41 then C51 | tabu from `order28` (n=28), seed 41, 1,200 s; then from `T4` (n=17), seed 51, 600 s | 1,800 s |

- **L(A₃) feasibility:** a count-only measurement before this declaration found 867,940 states at one hole, enumerated in 12.7 s with 0.4 GB resident. The analysis may still exceed 1,800 s over 12 holes. Holes not finished are reported as capped.
- **Orders up to ~60 are not feasible with this engine.** The pure-Python engine keeps every state of a hole in memory, and the state count grows by about ×1.4 per vertex (868k at n=47, so about 10⁷ to 10⁸ near n=60). Phase C therefore stays at orders ≤ 47. A faster engine (C, or symmetry reduction) would be a separate declaration.
- Each run is one pass with no tuning between runs. Results are reported per statement, with the scope stated.
