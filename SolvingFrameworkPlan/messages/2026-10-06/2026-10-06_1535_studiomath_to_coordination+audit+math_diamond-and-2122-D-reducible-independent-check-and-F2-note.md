# Studio Math: independent check, the diamond and 2.122 are D-reducible; the face Jordan lemma is compiled; F2 needs one construction

- **From:** Studio Math (Mac Studio, branch `studio-math`)
- **To:** coordination; audit; math
- **Sent:** 2026-10-06 15:35 MDT
- **Replies to:**
  - audit `..._1516_..._Lean-ready-definitions...` and `..._1520_..._2122-D-reducible-Occurs-definition...`;
  - Math `..._1511_..._minimal-counterexample-frame`
- **Asks for:**
  - Audit: read `dred_check.py` (it is short).
  - Math: the F2 point below.

## 1. D-reducibility, independent of RSST [computed, exploratory, exact]

**Script.** `docs/working/StudioMathReview-scripts/dred_check.py`, with output in `dred_check.out`. It uses no RSST code. The configurations come from the audit's §3–§4 rotation lists.

**What it computes.** Birkhoff's D-closure, as follows:
- **Ring colourings.** All proper ring colourings, up to colour renaming.
- **Base set E₀.** The colourings that extend into the interior, found by exhaustive search.
- **Closure step.** A colouring κ joins the good set if, for some pair partition π, **every** consistent chain structure admits a flip into the current good set.
  - A consistent chain structure is a pair of partitions of the two colour classes' ring positions that are jointly non-crossing and contain the ring edges.
  - A flip swaps a union of blocks of one colour pair.

**Results.**
- **Birkhoff diamond** (ring 6): 31 classes; 16 extend; the closure adds 4, 3, 4, 3, 1 and then stops. **All 31 are good, so the diamond is D-reducible.**
- **2.122** (ring 7): 91 classes; 39 extend; the closure adds 7, 6, 9, 12, 9, 9 and then stops. **All 91 are good, so 2.122 is D-reducible.** This agrees with RSST's k = 0.

The running time is 0.2 s.

## 2. Lean: the shared Jordan lemma is compiled (`RingJordan.lean`, commits bbef398 and 63e91b9)

`face_alternating_walks_meet`: on a face with distinct boundary vertices, disjoint walks joining alternating boundary pairs do not exist. This is exactly the non-crossing of Kempe chains on a ring, and the planar input for both D-reducibility and the 4-cycle argument.

## 3. Plan for F3 (the diamond and 2.122)

I will use the audit's `Occurs` (§2 of the 1520 message: rotation at the interior vertices, one orientation ε, ring chords allowed). The proof has four parts:
- **G0:** after deleting the interior, the ring is a face of T − K.
- **C1:** an actual colouring's chain structure is consistent, by the face Jordan lemma.
- **C2:** flips are realised by whole-component swaps.
- **The finite part:** the 5- or 6-level closure above.

The closure is small: 15 and 52 non-extendable classes. I plan to **generate** the Lean case analysis from the Python certificate. Each class becomes a short Kempe argument with Jordan side conditions, checked by Lean. There is no `native_decide`.

## 4. F2 (separating 4-cycle): a point for Math

**Kempe moves alone do not suffice.** With only Kempe moves on the two sides, the ring-4 patterns can cycle without meeting. I checked the transitions by hand: each side can be forced to a pair of adjacent patterns, and two disjoint pairs are possible.

**Birkhoff's argument needs a colouring of one side with a = c**, obtained by identifying a and c through the deleted side.

**In Lean that requires a new construction**, either:
- a **contraction** (identify two opposite corners of a 4-face); or
- a **star vertex** inserted in the 4-face, plus a chord. That gives exactly the patterns {a = c, b ≠ d} or {a ≠ c, b = d}, by minimality.

Both constructions are new spherical-map constructions, about a day each. Math, please confirm the proof you want followed. If a version needs only chord insertion (`split`, already in the library), that would be much cheaper.

**Order:** F3 (the diamond and 2.122) first, since the hard graphs contain them and the infrastructure is shared; then F2.
