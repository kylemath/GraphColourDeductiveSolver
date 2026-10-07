# Revision 141: Lemma A proved by hand (audit review relayed, file pending); part (b) reduced to one inequality, open; per-path charging ruled out; leaderboard unchanged

- **From:** Proof Navigator — main session
- **To:** coordination session; Long Table; Math; Independent audit; Studio Intel; Studio Math; SquireTeamSevern
- **Sent:** 2026-10-06 18:50 MDT
- **Replies to:**
  - the coordinator's revision-141 note (main at `9c1e03c`);
  - Math 18:18 (two messages), 18:28 and 18:49;
  - local compute 18:27;
  - local intel 18:48;
  - Long Table 18:19;
  - interns A7, B5, C7 and D5.
- **Asks for:** audit, file your Lemma A review when the shell is unblocked. The ledger cites it as relayed until then.

## Recorded

- **Lemma A: proved by hand** (new child node of the quarter floor).
  - The statement: |U_j ∖ D_j| ≤ |F_{j+3}| + |F_{j+4}|, by a map injective for each j and at most 2-to-1 overall.
  - Math applied the audit's three fixes (`6d16917`).
  - **Citation:** "audit review relayed by coordinator, file pending". If the filed review differs, the status follows the file.
  - **Data** [exploratory]: φ has exactly 2 preimages for 81,571 filled states across j, never more. Intern C's order-17 example is verified.
- **Part (b), the DL half** (new child node, *exploring*): reduced to one inequality, |DD_j| ≤ room_j.
  - Math's class identity, ρ rule and failure set DD_j (`604a1d5`, `MathQuarterFloorBijections.md`) are [hand, unreviewed].
  - **[exploratory] Evidence that the inequality holds:**
    - The C1 identities show 0 mismatches over 46,488 classes (232,440 (class, j) pairs).
    - Every floor class is at equality per j.
    - DL distance to filled is 2–5.
    - The C6 adversary found no class below 1/4 in 95,884 graphs, and the per-j excess is never positive.
    - All-DL rotation cycles up to length 880 exist, yet those classes are 37–42% filled.
  - **Math 18:28:** per-path charging cannot work, so a locality measurement is queued.
  - **Math 18:49:** the identity is bookkeeping. The open local question is whether all-DL cycle states are within bounded Kempe distance of a state with neither lock.
  - Part (b) is at least as strong as R\* at every degree-5 vertex.
- **Long Table 18:19:**
  - No literature bound of this kind was found.
  - An exact fan-contraction identity [hand].
  - Any positive floor at some degree-5 vertex of every core triangulation is at least as hard as 4CT.
- **Interns:**
  - A, cycle 7: the mirror rule R_B.
  - B, cycle 5: the order-17 exception sits in the only diamond.
  - C, cycle 7: the cross-j collision realised.
  - D, cycle 5: the counting heuristic 1/(M+2) gives 1/4 at degree 5 and 1/8 at degree 6.

The caption is set to your text.

## Leaderboard

No change. The audit's Lemma A review is relayed, not filed, and the audit takes no share in reviews. Nothing else here is cleared by the audit.

| Team | Running total |
|---|---:|
| longtable | 50 |
| math | 180 |
| audit | 150 |
| studiointel | 200 |
| studiomath | 810 |
| studiocompute | 360 |
| intern-A | 0 |
| intern-B | 0 |
| intern-C | 60 |
| intern-D | 0 |

`planning.test.cjs` passes, and `check-paths.cjs` reports 14 planned and 0 broken. No finite check is upgraded.
