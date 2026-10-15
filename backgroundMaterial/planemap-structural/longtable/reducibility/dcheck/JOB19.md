# Job 19 (Studio): DCheckSound R2, project-level glue [exploratory]

Pre-registration, written 2026-10-15 00:26 MDT before any proof work.

**Target.** In a file that imports `RingReduce` (StudioMathLean PlaneMap) and `DCheckS1`/`DCheckS3`/`DCheckR1`:
```
theorem ConfigOcc.colorable_of_dReducible (cf : DCheck.Conf) (hD : DCheck.dReducible cf = true)
    (hr2 : 2 ≤ cf.r) (hr : cf.r ≤ 15)
    (hsym : ∀ a b, intAdjOf cf a b = true → intAdjOf cf b a = true)
    (O : ConfigOcc T G cf.r cf.m ρ ι (intAdjOf cf) (ringAdjOf cf))
    {c : Fin n → Fin 4} (hc : ProperOff G.graph O.hole c) : T.graph.Colorable 4
```
(`cf.r ≤ 15` because DCheck's `matchTable` stops at p = 7; Job 23 lifts it.)

**Pieces.**
- (A) `extendsQ` soundness: a true backtracking result gives an interior colouring (`hint`, `hring`).
- (B) ring code of a colouring, `col (code c) t = c (ρ t)`, `code c < 4^r`.
- (C) realised codes are proper on the ring (`ring_proper`, `ring_proper_wrap`).
- (D) `canon r (code c) = code (σ ∘ c)` for some colour permutation σ (from `S1.cinv`).
- (E) **R2 proper:** `KempeMatching cf P` for P = codes of proper colourings of G off the hole. Arc chains satisfy
  `NCLabel` (from `chains_noncrossing(_same)`) and `ParityLabel`. With `nc_matching` and `matchTable_complete`, the
  flip of the selected chains is proper and has ring code `k ^^^ flipMask r k θ lab s`.
- (F) Assemble with `dReducible_sound` and `ConfigOcc.colorable_of_ext`.

**Hypothesis H19.** (A)–(F) go through using only the existing lemmas, with no new geometric input. The only
geometry is in `chains_noncrossing(_same)`.
**Kill.** A step that needs a geometric fact not already in the repo, for example that a Kempe chain meeting the ring
in two arcs of the same class must pass through the outside (it can't use the hole), or that `ProperOff` is too weak for
the flip. Report the missing statement exactly.
**Axiom budget.** propext, Classical.choice, Quot.sound, plus the existing native_decide axioms of R1 (`check4..8`).

## Result (15 Oct 2026): H19 survives. R2 and the full glue are proved, with no `sorry`.

`./build_r2.sh` does a clean build in about 2 min at nice 10: the StudioMathLean PlaneMap modules up to `RingReduce`, then the
DCheck core and `DCheckR2A`–`D`.

```
theorem SimpleGraph.SphericalMap.ConfigOcc.colorable_of_dReducible (cf : DCheck.Conf)
    (hD : dReducible cf = true) (hr2 : 2 ≤ cf.r) (hr15 : cf.r ≤ 15)
    (hsym : ∀ a b, intAdjOf cf a b = true → intAdjOf cf b a = true)
    (hloop : ∀ a, intAdjOf cf a a = false)
    (O : ConfigOcc T G cf.r cf.m ρ ι (intAdjOf cf) (ringAdjOf cf))
    {c : Fin n → Fin 4} (hc : ProperOff G.graph O.hole c) : T.graph.Colorable 4
```
Axioms: propext, Classical.choice, Quot.sound, and `DCheck.R1.check4..8` (the existing native_decide per-p table checks).

| file | content |
|---|---|
| `DCheckR2A` | (A) `extendsQ_sound`: a true backtracking run gives an interior colouring (propext, Quot.sound) |
| `DCheckR2B` | (B) `code`, `col_code`, `code_lt`, `code_ext`; (D) `canon_rename`: `canon` is an injective colour renaming |
| `DCheckR2C` | (E, abstract) transitions as a sorted list, class parity, an even number of transitions, arc representatives `rep j = T[(j+1) mod 2p]`, connectivity of each arc to its representative (including the wrap arc), chain labels with `NCLabel`/`ParityLabel`, then `nc_matching` + `matchTable_complete` → `abstract_matching`; `flip_code`: the ring code of the flip is `k ^^^ flipMask r k θ lab s` |
| `DCheckR2D` | (E, geometric) the θ-edge graph, `theta_cls`, θ-chain ↔ two-colour chain, `ConfigOcc.theta_nc` from `chains_noncrossing(_same)` (the only planar input), `ConfigOcc.kempeMatching`; (F) `colorable_of_dReducible` |

- **One hypothesis not in the original target:** `hloop` (no self-loops in `intAdj`). `extAux` only checks earlier neighbours, so a listed self-loop would make the interior constraint impossible to satisfy. It is decidable per `Conf`.
- **Sabotage checks, all rejected:**
  - ring bound changed to 16 (fails at `matchTable_complete`, p ≤ 7);
  - `hloop` dropped;
  - the non-crossing hypothesis of `abstract_matching` replaced by `True`.
- **Scope:**
  - This covers `DCheck.run` certificates with ring ≤ 15. The DCheck16/DCheck18 runs (rings 16–19, including studio14c/14d) are not covered yet; that is Job 23.
  - Not checked yet: an end-to-end use on a concrete `Conf` together with a project `ConfigOcc` (for example the diamond).

### End-to-end check on a real configuration (`DCheckR2Diamond.lean`)
`DCheck.R2.DiamondE2E.colorable_of_occ`: a triangulation with a Birkhoff-diamond occurrence (`DiamondM.Occ`, orientation −1) is 4-colourable when every smaller spherical map is. The proof goes `DiamondM.configOcc` → `ConfigOcc.colorable_of_dReducible` with the DCheck `Conf` `cfD` (ring 6, interior 4); the generated certificate is not used.
- `dReducible cfD = true` is proved by `native_decide`. `run`'s `while` loop is opaque to the kernel.
- `intAdjOf cfD = DiamondM.intAdj` and `ringAdjOf cfD = DiamondM.ringAdj` are proved by `fin_cases`/`simp`; `hsym` and `hloop` by `decide`.
- Axioms: as for the glue, plus `cfD_dReducible`'s native_decide axiom.
