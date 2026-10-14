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
2b. 2026-10-14 15:26 MDT. **`canon_mem` proved**, so **(S1) is closed with no `sorry`**:
   `DCheck.run_sound`, `DCheck.canon_mem` and `DCheck.dReducible_sound` (S1 + S2, relative to the
   hypothesis `KempeMatching`) all depend only on propext, Classical.choice, Quot.sound. The
   completeness proof models `canon`'s loop state `(mp, nxt, out)` as `cst k i` with invariant
   `CInv` (labels injective on seen colours, `nxt + #unseen = 4`, `col out t = mp[col k t]`, no
   bits at or above `2i`), and shows the pair `(out_i, nxt_i)` survives each round of
   `ringColourings`. **H confirmed: no counterexample; the invariant needed only the precisions in
   item 2.**
3. 2026-10-14 15:31 MDT. **(S3)(i) non-crossing-partition lemma proved** (`DCheckS3.lean`,
   `DCheck.S3.nc_matching`; axioms propext, Classical.choice, Quot.sound). Statement: for chain
   labels `c` of the `2p` ring arcs that do not cross (`NCLabel`) and have one parity per chain
   (`ParityLabel`, i.e. one θ-class per chain), the map `mu` (transition `e` of an even arc ↦ right
   end of the cyclically previous even arc of its chain, `e+1` ↦ left end of the next one) is a
   non-crossing perfect matching (`IsNCPM`), and no chord of it separates two arcs of one chain
   (`sameFace`). Non-crossing of `mu` is derived from `sameFace` itself. Note: `ParityLabel` is
   needed (without it a chain could contain an odd arc outside the chord of its even arcs).
4. 2026-10-14 15:32 MDT. **(S3)(ii) simultaneous-swap lemma proved** (`DCheckS3.lean`,
   `DCheck.S3.flip_proper`, `chainUnion_closed`, `flip_chains_proper`; axioms propext,
   Quot.sound). For a proper colouring `col : V → Nat`, XOR-ing `θ` on any θ-closed set (closed
   under edges with `col u ^^^ col v = θ`) is proper, and any union of θ-Kempe chains (`Reach`
   classes) is θ-closed.

**Status at stop (milestone 4).** No `sorry` remains in `DCheckSound.lean`, `DCheckS1.lean`,
`DCheckS3.lean`. `DCheck.dReducible_sound` (checker soundness relative to `KempeMatching`) uses
propext, Classical.choice, Quot.sound only. Still open for (S3): (R1) `matchTable[p]` covers every
non-crossing perfect matching with faces = `arcRegions` classes (checker level, this package);
(R2) the project-level glue (chains of a `ConfigOcc` colouring satisfy `NCLabel`/`ParityLabel`,
and the ring trace of the swap is `k ^^^ flipMask …`). Both are stated in the header of
`DCheckS3.lean`. Build: `nice -n 10 lake build DCheckS1 DCheckS3` (about 3 s after `DCheck`).
