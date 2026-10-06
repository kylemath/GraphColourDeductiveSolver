# Three answers: 2.122 is D-reducible per RSST's data; a proposed `Occurs` definition (orientation, ring chords); Theorem R5³ final verdict

- **From:** Independent audit, main session
- **To:** coordination session; Studio Math; Math; Proof Navigator
- **Sent:** 2026-10-06 15:20 MDT
- **Replies to:**
  - the coordinator's two questions on Studio Math's D-reducibility interface (`StudioMathLean/PLAN.md`, `d522640`);
  - the R5³ kill test (studio-intel `c5d0954`)
- **Asks for:**
  - Studio Math: adopt or amend §2.
  - Navigator: record §3.

## 1. Is RSST 2.122 D-reducible? Yes, according to RSST's own data file

- **Source.** `routeb/rsst/unavoidable.conf` (SHA-256 `1c92fc28…`, RSST's published file), read with RSST's format description (thomas.math.gatech.edu/FC/ftpinfo.html).
- **The format.** Each entry's second line is `n r a b`, where a = |C| and b = |C′| ("as in the discussion before (3.2)" of the paper). The third line is `k` followed by 2k integers: **the edges of the contraction X**.
- **The two entries.**
  - 2.122: second line `11 7 39 0`, third line `0`.
  - The diamond `0.7322`: second line `10 6 16 0`, third line `0`.
  - Both have **X = ∅** and **|C′| = 0**.
- **The field discriminates.** Across all 633 entries, **384 have a nonempty contraction** (k > 0). So k = 0 marks the configurations RSST reduce without a contraction: **D-reducible**.
- **Caveat.** This is inferred from the data format. The audit did not read RSST's §3 definitions of C, C′ and D-reducibility. An independent D-reducibility check of 2.122 (ring 7) on the Studio would settle it directly, and is cheap.

## 2. Proposed occurrence definition `Occurs T K ρ ι`

`K` is a configuration given by its **free completion**, exactly as in the file:
- ring vertices `1..r` in cyclic order;
- interior vertices `r+1..n`;
- for each interior vertex, its neighbour list in rotation order.

`ρ : Fin r → V(T)` (ring) and `ι : Interior → V(T)` (interior).

**Definition.** `Occurs T K ρ ι ε`, with an orientation flag ε ∈ {+1, −1}, holds iff:
1. **ι is injective**, and **ρ is injective** (r distinct ring vertices), with `range ι ∩ range ρ = ∅`.
2. **Rotation (this fixes the embedding).** For every interior u, the rotation of T at ι u, as a cyclic sequence, equals the image of K's rotation at u under (ι ∪ ρ). It is read forwards if ε = +1, backwards if ε = −1, with **one ε for all u**.

**Consequences, not extra axioms.** Condition 2 forces:
- the exact neighbour set and **degree** of every interior vertex (= its degree in the free completion = γ);
- **inducedness** of the interior;
- every free-completion face is a face of T (each such face contains an interior vertex);
- the ring edges ρ(i)ρ(i+1) are edges of T.

So RSST's "appears" (induced, faces, degrees) is implied, and the embedding of the interior is fixed up to the global mirror ε.

**Orientation.** Allow both ε. Configurations are occurrences up to reflection, and the D-reducibility argument is orientation-free. Both the diamond and 2.122 are mirror-symmetric (swap the tips).

**Ring chords: allow them.** The definition says nothing about edges of T between ring vertices, other than the ring edges.
- D-reducibility works in T − ι(Interior). Any chord is an edge of T − K, so it only restricts which ring colourings occur, which can only help.
- The Kempe moves happen in T − K, and the extension test uses only K's interior and the ring colours.
- The **planar chain-matching lemma** needs the ring to bound a disc containing K with the rest of T outside. That follows from injective ρ plus condition 2, and does not need chord-freeness.

**What F3 must still prove separately.** "A minimal counterexample in which K *appears* (RSST sense) has an `Occurs` with injective ρ." Distinct ring vertices are where internal 6-connectivity is used: a repeated ring vertex closes a short separating cycle with interior vertices on both sides. **Keep that as its own lemma**, so that `Occurs` itself stays purely combinatorial.

## 3. Theorem R5³: final verdict

- **Hand.** Math (11 → 15:11). Math's own review: correct (15:16). **The audit re-derived it independently: correct** (`2026-10-06_1514`).
- **Machine (kill test, exploratory).** Studio intel `r55566_test.py` (`c5d0954`) ran over every degree-5 hole with three consecutive degree-5 neighbours, in every frame and both rotation senses: **0 violations on 6,256 holes**. It checks against the gen_tri lists for orders 12–22 and the certificate graphs. Its radius formula, 1 + d(s, non-DL), is exact, because a DL state cannot fill in one swap.
  - Independence note: it uses Studio intel's own `radius.py`. That is acceptable for a kill test, but the status rests on the two hand derivations.
- **Suggested status:** "**Theorem R5³: proved [hand]**, two independent hand derivations (Math, audit), machine kill test passed". The scope and coverage limits of the audit's 15:14 message stay (`09a1074`):
  - it does not cover (5,5,6,5,6), (5,5,6,6,6) or the three audited radius-5 certificates;
  - it is not enough for R\*.
- **Bounty.** The 300-point item is still half met.

## 4. New item the audit has not yet checked

`PLAN.md` (update 15:11) reports **link D compiled**: `SphericalMap.four_color_of_core_Rstar : RStarCore → …Colorable 4`. That closes the core-class chain in Lean. It needs the same check as J5–J9 before any status word is used. The audit will specify the J10 commands on request (reusing `run_j9.sh` plus `RStarCore.lean`), and will read `RStarCore`'s statement against the hand Lemma R\*.

— Independent audit
