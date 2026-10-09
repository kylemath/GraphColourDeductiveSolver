# Referee report: "Kempe chains around a degree-five vertex: a mod-4 chain count and a parity law"

Draft of 8 Oct 2026 (`main.tex`). Report of 9 Oct 2026, by an AI referee session that did not write the note, the Lean code or any of the cited scripts. I read `main.tex`, `README.md`, the five Lean modules (`QuarterLockParity`, `ChainCount`, `ChainMod4`, `TutteSides`, `ChainF`), the definitions in `QuarterFloor`/`QuarterPi`, the audit J14 README and `NonVacuity.lean`, and the source files for every quoted number. I wrote my own checking code (described in §5). It imports nothing from the project.

## 1. Verdict

**Minor revision.** One proof has a real gap: the converse direction of Proposition 2 (Kempe duality). The statement is true, compiled in Lean, and passed 97,707/97,707 of my checks, and the gap has a standard repair. One wording error in the abstract and title needs fixing: the formula determines N only mod 2, not mod 4. Several sharpness claims are stated more broadly than the data shows. I checked the other new hand proofs line by line and found them correct:
- Lemma W via the filled map;
- the last sentence of Lemma F0;
- the primal Euler proof of Tutte's identity;
- the fill argument for Theorem F;
- the law and its corollaries.

Every quoted number matches its source.

## 2. Errors and gaps (by severity)

### E1. Error (wording): "a formula for N(c) mod 4" (abstract; title "a mod-4 chain count")
Theorem F says 2N ≡ RHS (mod 4). That determines **N mod 2 only**, and it also forces RHS to be even. The mod-4 content is that cw enters mod 4. The abstract's "We give a formula for N(c) mod 4" is false as written.
**Fix:** "a formula for the parity of N(c), in terms of the number of clockwise faces mod 4, …". Retitle to something like "a mod-4 identity for the chain count" or "a chain-count parity formula". The same applies to "a mod-4 form of Tutte's parity theorem", which is acceptable if it is read as "an identity mod 4".

### G1. Gap: Proposition 2, converse direction (contraction argument), §4.1
The proof says that after contracting a spanning tree of U = Q ∪ {v}, "two consecutive edges ua, ub at u bound a face coming from a face of T, so a = b or a ∼ b", and so the neighbours of u form a closed walk.
- This is false whenever T[U] contains a cycle, which is the usual case for a βδ-chain.
- Each non-tree edge of T[U] becomes a **loop** at u.
- Between the two ends of a loop, the rotation at u lists the neighbours that lie inside the disc the loop bounds.
- If loops are deleted, consecutive outside neighbours need not be equal or adjacent.
- If loops are kept, the "walk" passes through u, that is, through βδ-coloured vertices, and the conclusion "an αγ-walk in T−v" fails.
- The issue is loops, not parallel edges. README item 5 asks about "multigraph contractions"; the answer is that loops break the argument.

**Data:** I traced the Euler tour around the tree and took the cyclic sequence of outside neighbours with loops deleted:
- When T[U] has a cycle, the claim fails in **6,913 of 6,913** L2-false sphere states.
- When T[U] is a tree, it fails in **0 of 39,482**.
- (A second run gave 1,797/1,797 and 0/11,920.)

**Fix (standard):** let R be the face of the plane graph T[U] that contains x4. T[U] is connected, so ∂R is one closed walk. The T-faces in R incident to ∂R give a closed walk of outside neighbours, and consecutive ones are equal or adjacent.
- v has only one U-neighbour, x1, so v is a leaf of T[U] and its corner in R reads x2, x3, x4, x0.
- All other vertices of the walk are α/γ-coloured neighbours of Q, and x4 occurs only at v.

Alternatively, contract only the closed disc complement. With this fix the rest of the paragraph stands as written.

### G2. Gap / overclaim: "Each result fails on the torus" (abstract) and "Each result fails on other surfaces" (§5)
- **(∗)** holds on every surface; the note itself says so. The **link-free part of Lemma W** is stated to hold on every surface. Both are counterexamples to "each result fails".
- **Proposition 4 (N ≥ 8)** and **Theorem 8 (Remark 7)** get no off-sphere data in the note. I supply some:
  - N < 8 at **1,607 of 6,381** doubly locked (DL) torus states (another run: 1,955/10,333);
  - N < 8 at 288/1,429 genus-2 DL states;
  - Theorem 8 fails at **903 of 2,090** link-free torus exchanges (another run: 1,498/4,321);
  - Theorem 8 fails at 371/752 genus-2 link-free exchanges.
- **Lemma W at π** fails on the torus only in the degenerate case x0 ∈ K_αγ(x2), which Proposition 2 excludes on the sphere:
  - 3,064 failures of 6,381 π-steps; every failure has x0 ∈ K;
  - it holds at **3,317/3,317** steps with x0 ∉ K.

**Fix:** write "each of the main results (Prop. 2, Thm 3, Prop. 4, Thm 5, Thm 6, Cor. 7, Thm 8) fails on the torus; (∗) and the link-free part of Lemma W do not", and add a line of data for Prop. 4 and Thm 8.

### G3. Unclear: the population behind "the law failed at 282 of 544 π-steps"
`TrackC/scripts/tc_mod4.py` uses `pi_move` from `TrackI-review/ri_core.py`, which returns `None` when x0 ∈ K_αγ(x2). The 544 torus π-steps are therefore only the DL states with x0 ∉ K. With the note's own definition (π = swap of K_αγ(x2) at every DL state), π-steps with x0 ∈ K exist on the torus. There the frame moves, and Lemma W and L1(πc) = 1 also fail.
- My data, law failures: x0 ∉ K **1,497/3,317 (45%)**; x0 ∈ K 2,757/3,064.
- TrackC's 52% on its own sample is consistent with this.

**Fix:** say "at π-steps with x0 ∉ K_αγ(x2)".

### G4. Unclear: π used beyond its definition (§1)
The note defines π only at DL states (Definition 1). The introduction says "on the sphere π permutes each Kempe class". That needs the extension of π to all states (Lean `piMove`, defined on filled and singly locked states too). **Fix:** "π extends to a permutation of each Kempe class [vhe2026]".

### M1. Minor: Example (n = 22), "none was found at order 20"
This comes from 261,093 greedy reductions of order-22 violators (TrackU), not from an exhaustive search. Say so.

### M2. Minor: stale census claim (§5, Open problems)
"the longest near-rigid run … grows with the order and reaches 8 at order 33". Census34, which is committed (5e9f5299), shows the maximum NR **stays at 8** at order 34 (5 holes at the maximum). **Fix:** "orders 22–34 … reaches 8 at order 33 and stays 8 at order 34".

### M3. Minor: abstract, "a colouring with the minimum number of chains (eight)"
Eight is the minimum among **DL** states only. Unfilled non-DL states can have N as low as 6. Say "a rigid colouring (eight chains, the minimum for doubly locked colourings)".

### M4. Minor: abstract, "the law alone does not exclude near-rigid π-cycles"
The evidence is an abstract, non-planar matching-form example, not a surface. The §5 wording is accurate: "the parity law, together with the local matching structure, does not exclude …". Use that wording in the abstract too.

### M5. Minor: notation and labels
- p(p,q) uses p both as the chain-count function and as a colour.
- cw is redefined in §4.2 to count all faces. Use cw_T or cw_{T°} explicitly. The proofs of Thm F and Lemma W already mix cw(c) (faces of T avoiding v) and cw_{T°}.
- Lemma 10 carries three labels; this conflicts with the stated one-label policy.
- Lemma F0 says "every closed oriented triangulated surface". It should say loopless, with faces on three distinct vertices, as in Lemma 12.
- Lemma W's second sentence is surface-general, but it sits in a section headed "Throughout this section T is a triangulation of the sphere". In Lean, `lemmaW_linkFree` also needs `StarHyp`; it is automatic for a genuine surface hole.

### M6. Minor: once the fixes are applied, mark the new proofs reviewed
The bracket "new in this note and unreviewed" on Lemma W, and "last sentence new here and unreviewed" on Lemma F0, can be updated once this report is accepted. Lemma 10's primal proof can say it is reviewed. Proposition 2's converse should be updated only after G1 is fixed.

## 3. Line-by-line check of the three new proofs

**(1) Lemma W via T° (§4.3). Correct.**
- Under DL, Proposition 2 gives x0 ∉ K, so c′ has link (α,β,γ,α,δ).
- The diagonals are βγ and βδ, so K stays a whole αγ-chain of T°, and c′ is proper on T°.
- Lemma F0's last sentence gives cw_{T°}(c′) ≡ cw_{T°}(c) (mod 4).
- Fill faces under c′, by my table check over all 24 colour assignments:
  - Tait triples (e,g,a), (a,e,g), (e,a,g);
  - clockwise iff η = 0, 0, 1;
  - so cw_{T°}(c′) = cw(c′) + 2 − η.
- Combined with cw_{T°}(c) = cw(c) + 3η, this gives cw(c′) ≡ cw(c) + 4η − 2 ≡ cw(c) + 2.
- Link-free case: K is a chain of T°, and the fill faces are unchanged.
- Data: 24,907/24,907 π-steps and 27,878/27,878 link-free exchanges on spheres. The link-free part also held 4,321 + 2,090 times on the torus and 752 times in genus 2.

**Lemma F0, last sentence. Correct.** A swap of p, q fixes the class of each colour A ∉ {p,q}. Lemma 12 (Fisk, mod 4) then fixes cw mod 4. This argument needs only that the result is a proper colouring of a closed oriented loopless triangulated surface. Data:
- Fisk mod 4 held at 390,828 (T°, sphere), 89,536 (torus) and 12,152 (genus 2) colour checks;
- it held at 298,616 checks on T with full colourings;
- my 24-case table confirms σ = sign of (d,a,b,e);
- the edge-pair rule "equal σ iff z ≠ w" holds in 48/48 cases.

**(2) Proposition 2, converse.** See G1. The forward direction (Jordan) is correct for L2, and for L1 with γ ↔ δ: the rotation x0,…,x4 separates {x2} from {x4, x0} by vx1, vx3.

**(3) Lemma 10, primal Euler proof. Correct.**
- Euler for a plane multigraph with k components, V − E + F = 1 + k, gives the face count.
- Every face of G contains a T-face, and that T-face has a Z/W corner because its corners carry three distinct colours.
- The Z/W corners of one T-face are adjacent.
- R minus finitely many vertices is connected, so the T-faces of R are linked through edges outside G, and these have a Z/W end.
- Each Z/W vertex in R is a corner of a T-face in R.
- So every face holds exactly one chain. Parallel edges cause no trouble, since e(X,Y) counts multiplicity in both places.
- Data: 447,924 identities on simple T with full colourings; 586,242 on the multigraph T°. 17,555 of 28,183 sampled states had a parallel diagonal, so the multigraph case was well exercised.

**Theorem F via T°. Correct.**
- Orientation of the fill: (x1,x2,x3) traverses x1→x2 as (v,x1,x2) did, so the fan is oriented consistently.
- N = N_{T°} + (1−L1) + (1−L2) held 97,707/97,707.
- cw_{T°} = cw + 3η held 97,707/97,707.
- The arithmetic 3η ≡ −η and −2L ≡ 2L (mod 4) is right.
- I also checked that global orientation reversal leaves F invariant when cw and η are reversed together, using the evenness of RHS. So the convention is exactly "η read in the same orientation as cw", matching Lean's `handS`.

**Theorem 6 and its corollaries. Correct.**
- Frame of πc: (α′,β′,γ′,δ′) = (α,δ,β,γ) from x3, so η is unchanged.
- L1(πc) = L2(c) because βδ-chains are untouched.
- Theorem 8 follows the same way.
- Data, all 0 failures: law 24,907; L1(πc) = 1 24,907; η(πc) = η(c) 24,907; frame starts at x3 24,907; Theorem 8 27,878; rigid isolation 3,962 rigid states; N ≥ 8 and rigid ⇔ N = 8 24,907.

**Lock parity proof (∗). Correct.** I redid all six link evaluations:
- 3+0 / 5+1;
- 2+1 / 5+1;
- 4+1.

(∗) held at 97,707 sphere states, 35,241 torus states and 3,038 genus-2 states (0 failures), consistent with "no topology".

## 4. Statement-vs-Lean fidelity

- Locks, frame, π, chain counts and RigidAt match: Lock1/Lock2 use `pairGraph` of G − h, and π = `rot3` at a DL state (`piMove_of_dl`). The order of the six RigidAt counts is (αβ, γδ, αγ, βδ, αδ, βγ), as in the note.
- `cwCount` reads the Tait triple along `faceNext`. `handS` flips η when `P` is labelled against `faceNext`. This matches the note's convention.
- `ChainFormulaF` uses (n : ZMod 4) − 1 with n the size of `Fin n`. With no isolated vertices and no connectivity assumption, a disjoint union of spheres is allowed. That is harmless because F is additive over components.
- `ChainParityLaw` uses `DLState (πc)` (DL in some frame). Frames of unfilled states are unique, so this is the note's "πc is DL".
- "No isolated vertex" appears only on F, the law, rigid isolation and Theorem 8, as the note says.
- `lemmaW` (surface-general) carries `LinkBalanced` and `StarHyp`, and `cw_piMove` is sphere-only. The note's table is accurate.
- `tutte_sides` contains γ (number of components) and is for simple graphs. The note's "compiled in a sides form" is fair. The hand proof applies Lemma 10 to the multigraph T°, which has no Lean counterpart. That is acceptable, since Lean takes a different route.
- Audit metadata matches `Audit-2026-10-08/README.md`: commit ad0fd00b, Mathlib 300d0e5, Lean v4.35.0-rc3, 91 modules, planted sorry. All five hash prefixes match `shasum` of the current files. `SHA256SUMS` checks 40/40.
- The NonVacuity instances include F, the law, eight, lock parity and `cw_piMove`, as stated. N = 12 for both c and πc is audit row 9.

## 5. Sharpness section

- **Genus residue 2G (hand, unreviewed).** I computed the total region genus independently on T°:
  - per region, χ = V − E_in (multigraph count) and b = number of 2-factor cycle sides;
  - I checked that g = (2 − b − χ)/2 is a nonnegative integer at 202,518 + 28,736 regions;
  - I checked that each cycle's two sides lie in single regions at 3.4M + 0.7M crossings.

  Results:
  - residue ≡ 2G (mod 4) at **22,384 + 12,857 torus states** and at **3,038 genus-2 states**, 0 failures (README item 7 said genus ≥ 2 was unchecked);
  - G_i ≤ 1 always on the torus, which is also trivially true because genus is additive over disjoint subsurfaces;
  - G_i ≤ 2 in genus 2.

  Note that G = 3 is common in my torus sample (4,591/22,384, with every G_i = 1), while FProof's sample had only G ∈ {0,1,2}. The note quotes FProof's counts and does not claim G ≤ 2, so nothing is wrong. Still, consider saying "G = 0, …, 3 can occur".
- **Matching form.** On spheres:
  - N = 5 + k(H) + k(F12) + k(F13) held 97,707/97,707;
  - L1 ⇔ F12 pairs (e0e3)(e1e2), and L2 ⇔ F13 pairs (e1e3)(e0e4), each held 97,707/97,707;
  - N(πc) = 7 + k(M_{t−1} ∪ M_t) held 838/838, at DL→DL steps where F12 and F13 are connected at πc.

  The claim that a near-rigid cycle gives F12 and F13 connected cannot be proved state by state:
  - at general DL states with N = 9, the extra component falls in H, F12 or F13 roughly equally (11,779 / 8,113 / 7,851);
  - at the 650 in-shape states (N = 9 with both π-neighbours rigid) it was always H.

  So the claim really rests on the in-shape (J5/σ-type) lemma, as the note indicates. I did not test "a state is determined by M_t".
- **n = 22 example.** I checked it independently with networkx, using the edge list in `TrackU/out/t1_n22_first.txt`, which is identical to `TrackU/README.md` §0:
  - simple, 22 vertices, one vertex of degree 5 (vertex 0), all others cubic;
  - non-planar, vertex connectivity 3;
  - all 10 M_t perfect;
  - E − M_t connected, with v-pairing (f_{k−1}f_{k+1})(f_{k+2}f_{k−2}) and inner-vertex parities even/odd;
  - M_{t+1} ⊆ E − M_t contains f_{k−2}, and M_{t+1} △ M_{t−1} is exactly the odd loop;
  - word k(M_{t−1} ∪ M_t) = 1,2,1,2,1,2,1,2,1,2.

  All confirmed.

## 6. Numbers checked against sources (all match)

| figure | source | status |
|---|---|---|
| 111,912 / 281,230 | TrackI/RigidIsolation.md l.206–208 | ✓ |
| 21,968,170; 1,664,226 / 3,862,132 | TrackF/LockParity.md l.131–132 | ✓ |
| 2,192; 340 / 1,137 / 715; F fails at 1,137 | TrackK/FProof.md §4 table, §5 | ✓ |
| 282 / 544 | TrackC/README.md §6.4 table | ✓ (see G3 for the population) |
| 23/2,467, 1/1,401, 29/5,205; 53 rechecked | TrackH-review/README.md | ✓ |
| 611/1,261; 0/256 | TrackT/README.md l.38, l.177–179 | ✓ |
| n = 22, length 10, 1212121212, 2 engines; order 28; none at 20 | TrackU/README.md | ✓ (M1) |
| NR 8 at order 33; census 22–33 | Census33/README.md; VHE main.tex | ✓ but stale (M2) |
| N(c) = N(πc) = 12 | Audit J14 row 9 | ✓ |
| audit commit, versions, 91 modules, hashes | Audit README; shasum | ✓ |

Literature: Kempe, Heawood, Appel–Haken, RSST, Gonthier, Fisk (1977) and Tutte (1969) look right as given. I could not confirm the journal status of Mohar–Singer by web search. It stays a TODO, together with README items 11 and 12 (Tilley).

## 7. The referee's code

Scratchpad, not in the repository. The scripts are listed below; "every check" means all of the checks named in this report.
- `reflib.py`: the scripts below share it. It provides:
  - oriented triangulations and random edge flips;
  - generators for spheres (stacked, then flipped; n = 9–34), tori (flipped 4–6 × 4–6 grids) and genus 2 (connected sum of two flipped tori);
  - backtracking colouring;
  - chains.
- `check.py` (every check above). Two runs, 0 failures over about 1.03M checks:
  - spheres: 400 graphs, 97,707 unfilled states, 24,907 DL, 3,962 rigid; plus 120 graphs, 28,183 states;
  - tori: 116 + 64 graphs, 35,241 states;
  - genus 2: 16 graphs, 3,038 states.
- `fisk_table.py`, `n22.py`, `matchform.py`, `inshape.py`.

All runs used at most 2 processes, under `nice -n 10`.
