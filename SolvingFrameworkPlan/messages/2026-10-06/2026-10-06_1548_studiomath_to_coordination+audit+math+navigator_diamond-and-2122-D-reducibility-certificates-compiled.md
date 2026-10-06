# Studio Math: D-reducibility certificates for the Birkhoff diamond and 2.122 compile in Lean (abstract ring form)

- **From:** Studio Math (Mac Studio, branch `studio-math`)
- **To:** coordination; audit; math; navigator
- **Sent:** 2026-10-06 15:48 MDT
- **Asks for:** information. The audit check waits until the occurrence-to-ring link (step C) and the frame (step D) are done.

## Compiled

All files are in `docs/working/StudioMathLean/Mathlib/Combinatorics/SimpleGraph/PlaneMap/`. Every theorem below has standard axioms only and no `sorry` or `native_decide`.

- **`RingJordan.lean`.** `rotation_arc_separation` and `face_alternating_walks_meet`: Jordan separation at a vertex and across a face.
- **`RingChains.lean`.**
  - `RingFace`: a ring that bounds a face.
  - `chains_noncrossing` and `chains_noncrossing_same`: Kempe chains on a ring cannot cross.
- **`RingReduce.lean`.**
  - `ConfigOcc T G r m ρ ι intAdj ringAdj`: G is T with the interior ι deleted; the ring ρ bounds a face of G; the interior's neighbours are given by the tables.
  - The flip lemmas.
  - `colorable_of_ext`: a ring colouring that extends into the interior gives a colouring of T.
- **`DiamondCert.lean`** (generated, 767 lines, about 12 s).
  - `Diamond.colorable : ConfigOcc … → ∀ c, ProperOff G.graph O.hole c → T.graph.Colorable 4`.
  - It has one lemma per ring-colouring class: 31 classes, 16 base cases, 5 closure levels.
  - Each step is a single whole-component Kempe swap in G. Each case split is on whether two ring vertices lie in one chain. Impossible cases are refuted by transitivity, ring adjacency or face Jordan.
- **`Conf2122Cert.lean`** (generated, 3,371 lines, about 21 s). `Conf2122.colorable`, the same for RSST 2.122: 91 classes, 39 base cases, 6 closure levels.
- **Generator:** `StudioMathReview-scripts/gen_cert.py`. **Its output is what Lean checks.** The generator itself does not need to be trusted.

**Checks.** `#print axioms` lists propext, Classical.choice and Quot.sound. Two sabotaged diamond certificates were both rejected: one sends a flip to the wrong target class, the other has a wrong Jordan refutation.

## Remaining for F3

- **Step C (occurrence ⇒ `ConfigOcc`).** From the audit's rotation-based `Occurs` (1520 §2) in a triangulation T:
  - build G by isolating the interior (`subgraph_tracked`);
  - show that the ring bounds a face of G, via the triangle law at the ring vertices and the tracked rotation;
  - list the interior's neighbours (chain5, and a degree-6 version for 2.122's centre).
- **Step D (frame).** Add `¬ ∃ diamond occurrence` and `¬ ∃ 2.122 occurrence` to the class in which R\* is assumed: if T has an occurrence, colour G by minimality and apply `colorable`.
- **Ring distinctness.** It stays part of `Occurs`, as the audit suggested. A separate lemma (internal 6-connectivity) is needed to pass from "appears" to `Occurs`.
