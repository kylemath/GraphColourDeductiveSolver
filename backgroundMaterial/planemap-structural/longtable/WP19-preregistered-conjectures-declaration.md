# WP19 declaration: pre-registered fill-length and unlocking conjectures, order 23

Long Table, 5 October 2026. **A declaration for review. Nothing has run.** The producer, the independent checker and the regressions will be committed before any phase. **No phase runs until the math team posts a written go-ahead in `SolvingFrameworkPlan/messages/` that names this file and its commit, and the user releases it.** The user has told Long Table that math agreed WP19 should be drafted. No written math message exists yet, so drafting is the only thing done.

## Why

Every statement below was written after seeing data on orders 12–22 (WP18, `wp18/mechanism.md`, `wp18/analysis-17-1.md`) or orders 12–20 (`swarm/vh-exists.md`). Data a statement was fitted on cannot test it. WP19 tests each statement exactly as worded here, on graphs none of them has seen. The statements are fixed now and will not be adjusted between phases.

## Objects

These are as in `WP18-fan-selection-length-declaration.md`:
- **Graphs:** plantri 5.8 `-m5 -a n`, checked by `mass_core.parse_ascii`.
- **Legal fans:** \(\tau_i=\{i(i+2),i(i+3)\}\) at a degree-5 vertex \(v\), legal when neither chord is an edge of \(T\).
- **Starts \(S(v,\tau)\):** proper 4-colourings of \(T-v\) whose two chords are bichromatic, taken up to renaming of colours. These are exactly the restrictions of colourings of \(T^\ast_\tau\).
- **Moves:** a Kempe swap of one whole bichromatic component of the current deletion (hole fixed), or a singleton slide.
- **Filled:** the current hole's link uses at most three colours.

Quantities:
- **ℓ(s):** the fewest mixed moves to a filled state.
- **κ(s):** the fewest Kempe swaps to a filled state, with the hole fixed at \(v\) and no slides.
- **\(L(v,\tau)\)** is \(\max_s ℓ(s)\) over \(S(v,\tau)\), and **\(m(T)\)** is \(\min_{(v,\tau)} L(v,\tau)\).
- **Locked:** a start \(c\) is locked when \((v,c)\) is not filled and no single Kempe swap of \(T-v\) fills it. By `fan-link.md` and Lemma A of `wp18/mechanism.md`, this is the gap case.
- **Kempe classes of \(T^\ast_\tau\):** the classes of \(S(v,\tau)\) under Kempe swaps performed in \(T^\ast_\tau\), so components include the chords. They are taken up to renaming of colours.
- **U\((v,\tau)\)** holds when every Kempe class of \(T^\ast_\tau\) contains a start that is not locked.

## Pre-registered statements and what kills each

All seven statements are **post hoc candidates**: each was formulated after seeing orders ≤ 22 (or ≤ 20 for U∃). **M3 is included on purpose.** Long Table's message of 5 October listed the WP19 statements in §6 and omitted M3 by mistake. M3 is part of Conjecture M in `wp18/mechanism.md`, and it is tested here as written there.

The search caps are: mixed breadth-first search to depth 6, and Kempe-only breadth-first search to depth 7. Every kill needs a certificate that the independent checker verifies.

| Id | Statement | Source | Killed by (certificate) |
|---|---|---|---|
| M1 | Every start has ℓ ≤ 4 | mechanism.md | A start whose breadth-first layers at depths 0–4 contain no filled state (complete layer enumeration). Capped starts (ℓ > 6) kill it too. |
| M2 | Every start has κ ≤ ℓ + 1 | mechanism.md | A start with a recorded ℓ-path, and Kempe-only layers at depths 0–(ℓ+1) containing no fill. A start whose Kempe class at \(v\) contains no fill at all also kills M2; that is a separate, notable finding. |
| M3 | ℓ = 2 implies κ = 2 | mechanism.md | A start with a 2-move mixed path, and Kempe-only layers at depths 0–2 containing no fill |
| C1 | m(T) ≤ 2 for every T of order ≥ 18 | analysis-17-1.md | For every legal pair, a start with no fill in mixed layers 0–2 |
| C2 | m(T) ≤ 3 for every T | analysis-17-1.md | For every legal pair, a start with no fill in mixed layers 0–3 |
| C3 | m(T) ≥ 3 implies every vertex has degree 5 or 6 | analysis-17-1.md | A C1-type certificate on a graph that has a vertex of degree ≥ 7 |
| U∃ | Every T has a pair (v,τ) with U(v,τ) | vh-exists.md | For every legal pair, one whole Kempe class of \(T^\ast_\tau\) in which every member is locked. The checker re-enumerates that class and checks its closure under \(T^\ast\) swaps. |

**Also recorded, not tested as a statement:**
- Any start with no fill within the mixed cap is reported as **inconclusive**, not as evidence against VH∃.
- Lemma A (`wp18/mechanism.md`) is a hand-proved lemma. Its prediction (locked exactly when ℓ ≥ 2) is checked at every start as a consistency assertion. A mismatch stops the phase as an implementation fault.

**What a pass means.** Every statement is universal, so passes are never evidence of truth beyond the graphs tested. Phase reports state kills, certificates and counts only.

## Phases

1. **P1, holdout: order 23, every graph.** Plantri 5.8 output must hash to `d233b4efafdd3510f133760d9d918beab70e7496759aef512fb302cbd594bafa`. That is the night swarm's recorded order-23 output, made with plantri built from source tarball `e78a9441…29b8`. **Disclosure:** the graphs of order 23 already appeared in the night swarm's overnight q/lin/WP11-survivor rank sweeps (`wp12-scale/sweep-23-all.json`). Nobody has computed ℓ, κ, m, the diagonal sets or U on them, so order 23 is new **for these statistics**, but not new as a set of graphs.
2. **P2, optional: U∃ only, on orders 21 and 22.** These orders are fresh for U∃, which was seen only through order 20. They are not fresh for M1–M3 or C1–C3, which were seen through order 22.
3. **P3, optional: order 24, every graph** (7,290 graphs). Run only after P1's cost has been reported to math and math agrees.

Each phase is one pass with no tuning between phases. A kill in an earlier phase does not stop the later phases. A killed statement is still reported in later phases, labelled as already killed.

## Resource limits (fixing the WP18 findings)

- **Time:** at most 30 minutes per graph and 12 hours per phase. Deadlines are checked **inside** enumeration and breadth-first search, not only between starts.
- **Interruptions:** an interrupted graph keeps every completed pair and its partial counts, and is marked interrupted. That is inconclusive, never a pass.
- **Empty start families:** a pair with no starts is recorded as `empty`, never as L = −1.
- **Output:** at most 1 GB per phase, enforced. Past the limit, witnesses are dropped and the phase is marked `truncated`, but counts continue.
- **Memory:** at most 8 GB per worker, **enforced** *[revised 5 October, following `CreativeIntelCoordinationPlan.md`]*. The same in-loop hook that checks deadlines reads the worker's peak resident memory (`resource.getrusage`). Past 8 GB the graph stops and is recorded as interrupted with reason `memory`, keeping its partial counts. Peak memory is reported for every graph.
- **Accounting for every pair:** every legal pair of every graph appears in the output with its start count (or `empty`), its histograms, and either an exact L or a lower bound `L_at_least` with the reason (`capped` or `interrupted`). m(T) is reported as exact only when every pair is resolved. Otherwise it is reported as `m_at_least`, with the unresolved pairs listed. A statement is never counted as passed on a graph with unresolved pairs.
  - An interrupted graph still lists every legal pair. Pairs not reached carry `unresolved_reason: interrupted` and null counts.
  - Empty start families (`empty: true`) are excluded from the minimum that defines m(T).
  - `graph_index` is 0-based in input order.
  - `input_sha256` is the SHA-256 of the raw input bytes: plantri stdout, or the file.
- **Binding by hash:** each phase output records the SHA-256 of this declaration, of every producer source file, and of the plantri input. The checker refuses an output whose declaration hash differs from this file's committed version. The math team's go-ahead must name the commit that contains this file, the producer and the checker.

## Output and certificates

**Per graph:** the plantri index, the ASCII string and its hash, and the degree sequence. Per legal pair:
- the start count (or `empty`);
- the histograms of ℓ and κ;
- L and the U verdict;
- the number of Kempe classes of \(T^\ast_\tau\), and how many of them are all locked.

**Per graph summary:** m(T), the U∃ verdict, and any kill.

**Witnesses:**
- for every pair with L ≥ 3, the worst start and its path;
- for every start that violates M1, M2 or M3, the certificate data;
- for every pair where U fails, one all-locked class, listed in full.

**Independent checker** (`wp19/wp19_check.py`): it imports neither the producer nor `wp18_core`, `wp18_check` or `mass_core`. It does the following:
- re-parses each graph and validates it;
- enumerates the legal pairs independently;
- replays every path;
- enumerates the required breadth-first layers for every kill certificate;
- verifies every U-failure class: closure under \(T^\ast_\tau\) swaps, every member locked, and every member proper on \(T^\ast_\tau\).

The audit chat is invited to replay the full phase independently. The digests of the results, the witnesses and the source go in `wp19/SHA256SUMS-*`.

## Regressions, committed before any phase

1. The icosahedron gives ℓ ≤ 1 and κ ≤ 1 everywhere, L = 1 at all 60 pairs, and U holds at every pair.
2. The order-14 dipyramid start (`order14_fan_check.py`) has ℓ = 2 and is locked.
3. For 17:1, m = 3 is reproduced, and 38 of its 60 pairs satisfy U (`vh-exists-check.txt`).
4. The start at 22:93, v = 17 has ℓ = 4 and κ = 5 (`wp18/mechanism.md`). The phase does not re-read the order-22 file.
5. Malformed certificates must be rejected:
   - an improper start;
   - a non-closed "class";
   - a class containing an unlocked member;
   - a short path claimed as a kill.
6. Colour-renaming invariance is checked on one random start per regression graph.

## Not tested

The vacancy hypothesis, VH∃, the belt theorem, and the Four Colour Theorem.
