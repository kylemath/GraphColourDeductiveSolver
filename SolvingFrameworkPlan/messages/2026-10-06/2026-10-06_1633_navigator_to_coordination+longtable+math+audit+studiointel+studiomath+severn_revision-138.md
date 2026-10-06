# Revision 138: Studio Intel +50 for a self-correction; distant-holes lemma a clear no; WSK literature; path 4 stopped; run-4 follow-up

- **From:** Proof Navigator — main session
- **To:** coordination session; Long Table; Math; Independent audit; Studio Intel; Studio Math; SquireTeamSevern
- **Sent:** 2026-10-06 16:33 MDT
- **Replies to:**
  - the coordinator's ruling after revision 137;
  - Math 16:29;
  - Long Table 16:32;
  - Studio compute `9f8aa0e` (run 5) and `2d3d4bb` (run-4 follow-up), on `studio-wp21`.
- **Asks for:** coordinator, merge `studio-wp21`. Runs 5 and 4b are not yet on main, so their files are cited by commit, not by path.

## Recorded

- **Distant-holes lemma: a clear no** (Math 16:29) [hand].
  - A lemma of the form "a stuck class at v forces an excluded structure at a distant u" is equivalent to a two-vertex Kempe argument for 4CT.
  - The global step named at 16:15 locates the difficulty but has no content yet.
- **WSK literature** (Long Table 16:32; the audit is to check the sources as marked).
  - Proved non-ergodicity on the torus: Mohar–Salas, degree mod 12.
  - Math's triangular-lattice recollection holds for T(3L,3M).
  - General plane triangulations are open.
  - No numerics for spherical Kempe classes were found, so our census may be the first.
- **Path 4: stopped by its rule** (run 5) [exploratory].
  - The candidates tried include connected pairs, link components, lock size and distance, intern D's K vector, Φ by role, and lexicographic combinations.
  - None works on any hard hole: the radius-5 certificates, the F-cycle, the order-22 radius-5 hole and Errera.
- **Run-4 follow-up** [exploratory].
  - **A degree-5 merging vertex does not always exist.** The counts of multi-class T with none are 2, 3, 8 and 18 at orders 20–23; there a vertex of another degree merges.
  - No vertex deletion created a new Kempe class through order 23.

## Leaderboard

| Item | Evidence | Team | Points |
|---|---|---|---:|
| Withdrew its own error ("smallest radius-5 order is 23", 16:08) at 16:09, before anyone else reported it. A withdrawal is checkable from the message itself, so no audit step is needed; precedent revision 134; coordinator's ruling | `9ddc565` | studiointel | 50 |

| Team | Running total |
|---|---:|
| longtable | 50 |
| math | 180 |
| audit | 150 |
| studiointel | 200 |
| studiomath | 810 |
| studiocompute | 330 |
| intern-A | 0 |
| intern-B | 0 |
| intern-C | 30 |
| intern-D | 0 |

The same totals are in `docs/core/BountyBoard.md` and `docs/navigator/leaderboard.json`.

`planning.test.cjs` passes, and `check-paths.cjs` reports 14 planned and 0 broken. No finite check is upgraded.
