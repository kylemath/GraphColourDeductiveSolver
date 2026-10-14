# dcheck: Lake package for the D-reducibility checker [exploratory]

The main description of this package (the checker, the data, the `native_decide` theorems and the
soundness plan) is in `../README.md`, sections "dcheck" and "Soundness". This file holds only the
run log of item B3 (checker soundness), kept inside `dcheck/` by that run's rules.

## Run B3 (checker soundness, Long Table Lean agent, exploratory/draft)

**Pre-registration (written 2026-10-14 15:12 MDT, before any proof work).**
- **H:** (S1) of `DCheckSound.lean` closes with the invariant stated in that file's header,
  parts (a)–(c): (a) `good[i] = true → Good cf ks[i]`; (b) the progress pointer `prog[3i+θ-1] = p`
  means every matching with index `< p` has a flip into `Good`; (c) `ringColourings r` lists exactly
  the canonical proper codes and the `HashMap` index is a bijection onto them.
- **Kill:** a concrete counterexample to the invariant as stated. Then report the corrected invariant.
- **Scope:** (S1) in full in this package (replace both `sorry`s `run_sound` and `canon_mem`). Then
  (S3)(i), the non-crossing-partition lemma, and (S3)(ii), simultaneous swaps, both at an abstract
  level. The project-level glue of (S3) stays a stated remaining step.
- **Rules:** `DCheck.lean` is not edited. Facts are proved about it, or about a separate
  reference implementation proved equal to it.

**Milestones.**
1. 2026-10-14 15:20 MDT. **Invariant stated formally** (`DCheckS1.lean`): `OuterInv` (good bits ⇒
   `Good`, `reached ≤ countTrue good`, `good.size = N`), `ProgOK` (pointer `p ≠ dead` for `(i, θ)`
   ⇒ every matching `q < p` of the table has a flip `s > 0` with `Good (canon (k ⊕ flipMask … s))`),
   the index fact `index[x]? = some j → ks[j]! = x`, and the mask fact `xorSel … = k ^^^ flipMask …`.
   The loop is reasoned about through `DCheckRef.lean`: `runRef`, `run` with each inner loop moved
   into a named definition, bodies copied verbatim; `run_eq_runRef : run cf = runRef cf` is `rfl`.
2. 2026-10-14 15:20 MDT. **(S1) `run_sound` proved, no `sorry`** (axioms: propext,
   Classical.choice, Quot.sound; `Classical.choice` comes from core's `while`-loop unfolding
   `Loop.forIn_eq_of_monadTail` and from the choice of the witness `w` in `Good.step`). H stands
   so far: no counterexample. Two precisions to the header's wording: (b) is needed only for
   `p ≠ dead` and only for `q < matchTable[…].size`; (c) only the direction "lookup ⇒ `ks[j] = x`"
   of the index bijection is used. `canon_mem` (completeness of `ringColourings`) still `sorry`.
   The theorems `run_sound`, `canon_mem` and `dReducible_sound` moved from `DCheckSound.lean` to
   `DCheckS1.lean` (same names), because `DCheckS1` imports `DCheckSound`.
2b. 2026-10-14 15:27 MDT. **`canon_mem` proved**, so **(S1) is closed with no `sorry`**:
   `DCheck.run_sound`, `DCheck.canon_mem` and `DCheck.dReducible_sound` (S1 + S2, relative to the
   hypothesis `KempeMatching`) all depend only on propext, Classical.choice, Quot.sound. The
   completeness proof models `canon`'s loop state `(mp, nxt, out)` as `cst k i` with invariant
   `CInv` (labels injective on seen colours, `nxt + #unseen = 4`, `col out t = mp[col k t]`, no
   bits at or above `2i`), and shows the pair `(out_i, nxt_i)` survives each round of
   `ringColourings`. **H confirmed: no counterexample; the invariant needed only the precisions in
   item 2.**
