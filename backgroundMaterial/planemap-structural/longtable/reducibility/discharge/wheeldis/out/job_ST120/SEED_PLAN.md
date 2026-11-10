# ST-120 SEED_PLAN: Lean for the RSST-seeded t = 0 certificate (main line from 10 Nov 15:50Z)

Studio, 10 Nov. The goal is a Lean theorem `Unavoidable R_K633` with no LP in the trusted base, plus Lean reducibility for every
configuration it uses.
- [read] = taken from a file; [inf] = estimate. pd = person-days, one agent-day of focused Lean.
- CPU is Studio CPU-h.

**Already done [read]:**
- **B1** (charge + Euler): `RSSTCharge.lean` f7f3f13e, 0 sorry.
- **B3** (induced window): `RSSTWindow*.lean`, 748 lines, 0 sorry, standard axioms. Commit 9e76a5a70.

## Pieces

| # | piece | pd | CPU-h | depends on | notes |
|---|---|---|---|---|---|
| B2 | rules as data: the 71 parts (spec §3.2) as a Lean table + fit semantics (§3.3–3.5, hats, §6 9+ handling) | 5–8 | ~0 | spec only | generated from the spec by a script, semantics by hand; cross-checked against RSST-1SHOT's fit counts (test vectors) |
| B6a | read what `OccursW` / `OccursC` need of K's ring image (ring 3), the cut/pendant gap counts, and mirrors | 0.5–1 | 0 | — | reading only; it decides B6's shape before B4 commits to a word format |
| B4 | locality: (1) orientation coherence (B3 §9 note 1); (2) a decidable locality lemma over the 71 parts (every constrained position in the window, no ring-3 or 9+ middle constrained, hubs deg ≤ 8); (3) `finalCharge T u = evalWord (wordOf T u)` | 8–14 | <1 | B2, B3 | (2) is a `decide` over B2's table. (1) extends B3 with arc-order fields (2–4 pd) |
| B5 | Lean check of the fixed point d = 5..14 (full world, K633) and d ≥ 15 by 60 − 4d | 10–16 | 10–60 (native runs) | B2, B4 statement | see "B5: how it becomes Lean-checkable" |
| B6 | containment ⇒ `OccursW` / `OccursC`: a generic lemma from "K embeds in the drawn window" to an occurrence in T, through B3's iso | 6–10 | 0 | B3, B6a, the K633 config data | replaces 0.6 M lines of per-entry glue for the 582 |
| R | reducibility Lean for the remaining 403 of the 582: 198 hD + 205 hC (`rsst582_lean_coverage.tsv` d2f91ec5) | 1–2 (driving) | ~61 (13 hD + 48 hC) + ~3 for the own-engine re-check | — | 2 slots: about 30 h wall |
| S | substitutes: HDST111 (34 hD), then HDST119 (108 hD) + HCST119 (11 hC) | <1 | ~5 + ~37 | — | 1 slot: about 40 h wall |
| A | assembly: B1 + B3 + B4 + B5 + B6 + R + S ⇒ `Unavoidable`, then into `ClaimGlue.four_color_of_unavoidable` | 3–5 | 0 | everything | |

- **Total person-days:** about 33–55 pd. Of this, B4 + B5 + B6 = 24–40 pd are the bulk.
- **Total CPU:** about 110–160 CPU-h. It runs in the background on 3 slots and finishes well before the pd work does.
- **Held (not in this plan):**
  - route (i) for 2.126 / 128.1324802, about 10 pd (Addendum C), waiting on W6b RSST-RULE1;
  - P21.
  - The 426 leaves that need those two configs stay open until route (i) or a substitute lands.

## B5: how the full-world check becomes Lean-checkable (this changes how we describe the proof)

| route | what Lean trusts | cost | how we would describe it |
|---|---|---|---|
| (a) kernel `decide` | the kernel only | **infeasible**: d7 / d8 alone have 140 k states left after K582, from a far larger raw space, each needing a containment test against up to 633 configs; kernel reduction is many orders too slow | "fully kernel-checked" |
| (b) one big `native_decide` running the search itself | the compiler (`Lean.ofReduceBool`), as for every hD / hC today | low pd (port rcore.py, 351 lines); CPU = one compiled run per degree, est. 10–60 h; the Lean statement is just "for all words …" | "checked by a decision procedure compiled from Lean" |
| (c) a verified checker plus certificate files | the compiler for running the checker (`native_decide`); the checker's soundness is a Lean proof | more pd (completeness lemma over §8.1 grouping, witness format); CPU is lower and linear (verify a given killer per group, no search); certificates inspectable, tens of MB | "a Lean-verified checker replays an exported certificate" |

- **No feasible route avoids `native_decide`.** The seed proof will have the same trust class as our reducibility side: kernel
  plus `Lean.ofReduceBool`. Its description should say so plainly.
- **Recommendation: (c), with (b) as a fallback.**
  - Reason: the certificate (per positive group, a K633 config id plus its embedding) is the object reviewers and other engines
    (W6r, W6b) can check independently.
  - The Lean checker then does no search, so its correctness argument is short. Completeness ("every word is in some
    group") is a structural lemma over the grouping, which B5 has to prove in both (b) and (c) anyway.
- **d = 9..14** replays the max-plus / Karp potentials (spec §13) as a small DP certificate under `native_decide`.
- **d ≥ 15:** a plain lemma (60 − 4d ≤ 0).

## Order

1. **Now, at the same time:**
   - CPU starts at once on 3 slots: R and S.
   - Work: B2 (the data generator and table), with B6a done alongside as reading.
2. B4 (2), the decidable locality lemma over B2's table. Then B4 (1), orientation coherence. Then B4 (3).
3. B5: certificate exporter (Python, from RSST-1SHOT's code) → Lean checker → soundness → native runs per degree.
4. B6, shaped by B6a.
5. A.

**Critical path:** B2 → B4 → B5 soundness. B6 can run beside B5 once B6a and B2 are done.

## CPU split (coordinator 15:50Z)

- HCK5P21 / 22 finish as they are.
- Then 3 Lean slots:
  - **2 on R:** first an own-engine re-check of all 403 (kc -C + dfast18 for D2; kc -C -x X + cfast --fixed X for C2cons;
    about 3 CPU-h), then hD/hC largest ring first.
  - **1 on S:** HDST111 → HDST119 / HCST119.
- The LP lanes (MK12 / MK13, the v move) and the autocheck daemon keep running. If CPU is short, they drop to 1 process each
  before any Lean slot is touched.
- The 20 GB memory floor holds: hC modules peak at about 3 GB RSS, hD at about 0.5 GB.
