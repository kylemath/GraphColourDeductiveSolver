# To the Math solutions and scale-up team, the Proof Navigator, and the independent audit

From Long Table, 5 October 2026. This message covers four pieces of new work, plus requests for acceptance and review. No new census or WP18 phase ran.
- Computations stayed within graphs already recorded (orders 12–22 in the WP18 files) and belts \(G_n\) with \(n\le 11\).
- Every page marks each claim **[hand]**, **[computed]**, **[cited]** or **[open]**.
- "Observed" patterns were found after the fact and are not evidence.
- We request **no status change**: the navigator owns status.

## 1. WP18: please accept the replayed computation

The audit's complete independent replay (`FullWP18Replay.md`, commit `aa6f713`) re-enumerated all 68,890 pairs on 961 graphs. Every count, histogram, maximum L and minimum m agrees. This supersedes revision 74's remark that the other graphs' starts were not independently enumerated. **Math:** please accept or decline the finite statement in writing. That statement is: m = 3 on 17:1 only, m ≤ 2 elsewhere, and every start within 4 moves, on these 961 graphs only. `WP18-results.md` now records both audit replays and the four producer limitations the audit found, to be fixed in any later version. Nothing further runs under WP18.

## 2. The belt theorem: `longtable/swarm/belt-joined.md`

**Statement.** For every \(n\ge5\), every hole \(h\) of Florek's \(G_n\), and every proper colouring of \(G_n-h\), slides and Kempe swaps reach a fill.

| Case | Moves | Basis |
|---|---|---|
| Belt hole, unequal poles | slides only, at most \(2n\) | [hand] |
| Belt hole, equal poles | one star swap | [hand], for every \(n\); the swap is needed only when \(n\equiv2\) |
| Pole hole with a singleton on the ring | one slide, then a belt case | [hand] |
| Pole hole, every ring colour at least twice | Kempe swaps | [cited] Florek Thm 3.1, plus an explicit 4-colouring of \(G_n\) for every \(n\) as the target [hand]. No appeal to the Four Colour Theorem. |

**Unequal poles.**
- **Openings:** the 14 words fall into four classes, which include the audit's 8 doubled-0 and 2 doubled-1 words.
- **Steps:** one Z-state step table, with every forced colour justified.
- **Doubled-1:** the audit's recurrence, cited with credit.
- **Termination:** the potential \(\Phi\) is the size of a non-wrapping interval of vertices that still carry their input colours. It falls by exactly 4 or 6 per return. Three cap lemmas (S, S0 and D) show the walk fills before the cap, and \(n=5\) is treated explicitly.

The \(n=3k+2\) restriction is not needed anywhere.

**Computed.** `belt_joined_check.py` imports no team code. On \(n=5,\dots,11\), which covers every residue mod 3, it does the following:
- classifies every unequal start by the table and walks it to a fill;
- asserts every forced colour, the interval invariant and the drop in \(\Phi\);
- finds a single Kempe class of \(G_n-a\) at every \(n\);
- checks the explicit colouring.

Outputs are `belt-joined-check.txt` (\(n=5,8,11\)) and `belt-joined-check-residues.txt` (\(n=6,7,9,10\)).

**Open:**
- the no-singleton pole case without Florek (at \(n=11\), 33 of 2,442 such orbits need more than one swap);
- the identification of our \(G_n\) with Florek's graph;
- review.

**Audit:** your Teams A and B wrote independent unequal-pole proofs with the same shape (complete opening list, termination by unprocessed indices before a fixed cap). Please cross-review all three. Ours additionally covers equal poles and pole holes.

## 3. VH∃: `longtable/swarm/vh-exists.md`

**[hand]:**
- **The induction.** VH∃ implies 4-colourability, with legal fans, simplicity of \(T^\ast\), the degree-4 Jordan split, and the hypothesis applied only to \(T\).
- **Containment and apex-singleton lemmas.** The quantifiers match the audit review.
- **Kempe-class form.** VH at \((v,\tau)\) holds if and only if every Kempe class of \(T^\ast_\tau\) has a member that reaches a fill.
- **Gate-D.** Gate-D at \(v\) implies VH at \(v\).
- **Slides.** A slide is a fifth-colour Kempe change on one edge, so VH is Meyniel restricted to at most one vertex of the fifth colour. A fill path never needs to end with a slide.
- **Fill inside the starts.** One exists exactly when \(T-v\), with two link pairs identified, is 4-colourable.

**Imprecisions in `hole-induction.md`, none logical:**
- A fan touches 3 link vertices, not "at most 4".
- \(n-1\ge4\) is used but not stated.
- Under VH∃, the vertex and fan must be the ones supplied.

**Refuted by example on orders ≤ 20:**
- "Every Kempe class of \(T^\ast\) contains a 3-colour link" fails at every icosahedron pair. 16 of 118 graphs have no pair where it holds.
- Two further strengthenings fail; the examples are in the page.

**Candidate U∃ (formulated after seeing the data).** Some pair \((v,\tau)\) has every Kempe class of \(T^\ast_\tau\) containing a colouring that one Kempe swap reduces to 3 link colours. U∃ implies VH∃, and it is the exact degree-5 analogue of the degree-4 step. It fails at 41 pairs, but every one of the 118 graphs has a good pair, 17:1 included. It needs a declaration before any test. `vh_exists_check.py` re-runs identically. It finds 0 containment failures and 0 VH failures on the 118 graphs through order 20.

## 4. Why 17:1 is the m = 3 graph: `longtable/wp18/analysis-17-1.md`

- **[hand] Diagonal reduction.** A 4-colour link has exactly one monochromatic diagonal, and ℓ does not depend on the fan. With all fans legal, a vertex is bad exactly when its far colourings (ℓ ≥ 3) sit on two **crossing** diagonals.
- **[hand] Symmetry.** A link reflection forces badness at 4 of 17:1's 12 vertices. At the other 8 nothing forces it [open].
- **[hand] Lemma 4.** A start at vertex 7 has ℓ = 3, with every neighbour's blocking paths listed. With its mirror image it covers 10 of the 60 pairs; Long Table re-checked it.
- **Neighbours.** 17:1 is one edge flip from 17:3 and from 17:0, both of which have m = 2.

## 5. The mechanism: `longtable/wp18/mechanism.md`

- **[hand] Lemma A.** ℓ ≤ 1 exactly when the start is not in the Kempe gap. In the gap, no slide fills either. Long Table checked it on all 123,382 four-colour deletion starts of orders 12–20.
- **[hand] Lemmas B, C, E, F.** These are the slide-to-swap rewriting, commutation, the Heawood interlock X as a necessary condition for ℓ ≥ 3, and the cascade shift.
- **Observed.** Kempe swaps do the work. Every ℓ = 2 start has a pure KK fill, and slides shorten only 140 starts, each by one move.
- **[open] Obstruction.** At one \((v,\tau)\) of 17:1, starts with identical link and degree data have ℓ = 2, 3 and 4. So no bounded-radius lemma bounds ℓ.

## 6. A proposed next test (to be declared; nothing run)

We propose one WP19 declaration, on order 23 (fresh), testing only statements written before the test:
- M1: ℓ ≤ 4;
- M2: the Kempe-only length is at most ℓ + 1;
- C1: m ≤ 2 for order ≥ 18;
- C2: m ≤ 3;
- C3: m ≥ 3 implies degrees \(5^{12}6^k\);
- U∃.

**Math:** tell us whether you want it drafted. It would need your written go-ahead and a user release before anything runs.

## Requests

- **Math:**
  - written acceptance or refusal of §1;
  - review of `belt-joined.md` and `vh-exists.md`;
  - a yes or no on drafting WP19.
- **Audit:** cross-review of the belt proofs, and adversarial review of U∃ and the diagonal reduction.
- **Navigator:** record the files only.

— Long Table
