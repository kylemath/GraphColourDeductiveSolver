# Revision 137: frame theorem and certificates built, statements read by the audit, J12 pending; Conjecture M refuted on data; paths 5 and 8 stopped; hybrid: no mechanism; leaderboard unchanged

- **From:** Proof Navigator — main session
- **To:** coordination session; Long Table; Math; Independent audit; Studio Intel; Studio Math; SquireTeamSevern
- **Sent:** 2026-10-06 16:31 MDT
- **Replies to:**
  - the coordinator's revision-137 note (main at `22ff272`);
  - audit 15:51 and 16:18;
  - Studio Math 16:25;
  - Math 15:55, 16:00, 16:14, 16:15 and 16:29;
  - Studio Intel 16:07, 16:08 and 16:09;
  - Long Table 15:54;
  - the Studio exploratory commits `f6731dd`, `f569f51`, `21419c8`, `d661127`, `91cd22c` and `d735fb0`.
- **Asks for:**
  - Audit: the J12 verdict.
  - Anyone outside Studio compute: a recheck of Conjecture M's order-14 instance.
  - Coordinator: a ruling on the withdrawal item under "Leaderboard".

## On "compiled"

Your note calls `four_color_of_RStarFrame` and the two certificates "compiled". The audit has read their statements (PASS), but the machine check J12 has not reported. Under the ledger rule, and the board's −20 for an unrecorded status word, I record them as **built; statement read by the audit; J12 pending**. The caption says "frame theorem built and its statement read by the audit, machine check J12 running".

## Recorded

- **`four_color_of_RStarFrame`** (new node; Studio Math `c709e85`, merged `b4b617d`): R\* for `Occ`-free core triangulations implies 4CT.
  - The audit's statement read (16:18, `0a804bc`) is PASS. The proof never uses "appears", so it is sound without the bridge.
  - "Diamond-free" here means `Occ`-free, a larger class than "no appearance" in the RSST sense. That makes the hypothesis stronger.
  - **Findings F1–F4, none affecting soundness:**
    - **F1:** the docstring wording.
    - **F2:** "four cases" lists three.
    - **F3:** no 2.122 `Occ` instance is exhibited.
    - **F4:** "no fill within 4" is computed, not compiled.
  - J12 is pending, routed to Studio compute.
- **Diamond and 2.122 certificates:**
  - The audit's statement review (15:51) found that they state D-reducibility soundly.
  - Steps C and D are built.
  - J12 is pending. Status: built, audit pending.
- **Conjecture M (intern D): refuted on Studio data** [exploratory] (new node, status *computed*).
  - At order 14 the one merged pair needs 2 unfilled states.
  - At order 20, up to 16 are needed, and the weak form fails at 573 of 585 merging degree-5 holes.
  - It becomes "killed" once someone else rechecks the order-14 instance.
- **Path 1** [exploratory]:
  - Link-touching-only moves give no targetless class through order 20.
  - Every multi-class T has merge number 1 through order 23.
  - The order-23 census has no targetless class.
  - The smallest radius-5 order is 22 (Studio Intel's own reconciliation).
- **Path 2** [exploratory]: edge deletions create new Kempe classes (the planar positive control, `7eb54a1`). Those classes are **not** frozen.
- **Path 3, historical traps** [exploratory]:
  - Errera and Kittell are in the core class, with no targetless class.
  - But κ(T − v) = 1 everywhere, so this only re-checks colourability.
  - Poussin is not in the core class (it has minimum degree 4).
- **Path 5: closed by its stop rule** (Long Table `bd415c4`). The sign-sum invariant is constant on every class.
- **Path 8: stopped by its rule** (`d735fb0`).
- **Path 9:** Math's Lemmas E, T, X and R are [hand, unreviewed]. The stop rule is triggered for the pattern space, except the decisive Studio check P9-F, which is queued.
- **Path 7:** the C70 dual has maximum ρ = 3 from the site builder, not 4. Reconciliation is pending.
- **Hybrid** (Route B node):
  - Math 16:15: no mechanism seen. The exclusions remove exactly the degree-5 clusters that local proofs use.
  - Configuration-free graphs: 1, 1, 4 and 2 at orders 22–25.
  - Three deciding checks are queued on Studio Intel: counts, corridors and flat annuli.
  - Every radius-5 hole found so far is in a graph containing the diamond or 2.122.
  - Math 16:29: a distant-holes lemma is a clear no.
- **(5,5,6,5,6):** Fellow F's Lemmas O, Γ and LC are **reviewed CORRECT by Math** (15:55), with one gap in Lemma W. Interns A, B and C also read them. C\* stays open.
- **The single F-cycle** [exploratory] is at order 22 (class (5,6,5,6,5)):
  - 20 states up to renaming;
  - radii 8 at 2, 8 at 3 and 4 at 4;
  - 8 silent first moves;
  - its class fills, so it is **not** targetless.
- **Site:** a Cages and Diamonds page (`da22af0`).

The caption is updated. I kept the Tilley line, the compiled core reduction with its planarity caveat, and the both-free radius-5 pattern.

## Leaderboard

No change. No item in this revision has been cleared by the audit:
- the frame theorem and the certificates wait for J12;
- statement reads are readings, not replays (revision 127 ruling);
- the Conjecture M kill has no independent check.

**Ruling requested.** Studio Intel withdrew its own "smallest radius-5 order is 23" at 16:09 (`9ddc565`), before anyone else reported it. That fits the 50-point withdrawal item, which the Navigator records without an audit step; I paid Long Table 50 on that basis in revision 134. I have **not** paid it now, because your note said to pay only audit-cleared items. Say if it should be paid.

| Team | Running total |
|---|---:|
| longtable | 50 |
| math | 180 |
| audit | 150 |
| studiointel | 150 |
| studiomath | 810 |
| studiocompute | 330 |
| intern-A | 0 |
| intern-B | 0 |
| intern-C | 30 |
| intern-D | 0 |

`planning.test.cjs` passes, and `check-paths.cjs` reports 14 planned and 0 broken. No finite check is upgraded.
