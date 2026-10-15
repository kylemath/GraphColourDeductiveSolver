# Job 24 (Studio): occurrence modules and per-key reducibility lemmas for the 47+3 deferred K=1 keys [exploratory]

Pre-registration, written 2026-10-15 01:03 MDT before the work.

**Per key** (the 50 lines of `discharge/studio14b/k1_r17_19.txt`; centre-66666 keys included):
- `gen_occ_key.py`: computes the free-completion rotation of the 2-ball from `ball.build`. The rotation is the link cycle of
  each interior vertex, oriented consistently by the rule "`(a,b)` consecutive at `v` ⇒ `(v,a)` consecutive at `b`".
- It emits a plain Lean file: `Occ` and `configOcc` (the generator logic of `StudioMathReview-scripts/gen_occ.py`, orientation −1,
  ring positions as in the dfast line, with no Kempe certificate), the `DCheck18.Conf` of the key, the adjacency equalities
  `intAdjOf = intAdj` and `ringAdjOf = ringAdj`, `hsym` and `hloop`, and
  `colorable_of_occ (hD : DCheck18.dReducible cf = true) … : T.graph.Colorable 4` via `colorable_of_dReducible18`.

**H24.** For every key the generated file compiles with no `sorry`, and the only open premise is `hD` (filled when studio14c/14d finish).
**Kill.** A key whose 2-ball rotation is not a consistent disc triangulation, or whose `configOcc` fails to compile
(for example a ring chord or a repeated ring vertex breaking `RingFace`). Report the key and the failing step.
**Scope notes.** One orientation per key. The mirror image needs either its own `hD` or a mirror-invariance lemma; that is a
follow-up. Ring ≤ 15 K=1 keys (about 19k): measure the cost per key first, and run them only if cheap.
**Priority.** One compile at a time at nice 15, so the studio14c workers aren't slowed.

## Result (15 Oct 2026): H24 survives. All 49 key modules compile with no `sorry`.

`occ24/run24.sh` generates and compiles one module per line of `discharge/studio14b/k1_r17_19.txt` (49 lines: the 47 deferred keys and the 2 keys centred on 66666). Each module takes 11–13 s at nice 15; the log is in `occ24/results.txt` (49 × `errors=0 sorry=0`).

Each module `K<ii>.lean` (namespace `SimpleGraph.SphericalMap.K<ii>`) contains:
- `ringList`, `intList`, `ringAdj`, `intAdj`, the `Occ` structure (rotation-based occurrence of the free-completion 2-ball), and `configOcc` (proved: deleting the interior gives a `ConfigOcc` and a strictly smaller support);
- `cf : DCheck18.Conf` (the wheelcheck18 input line), `intAdjOf_eq` and `ringAdjOf_eq` (`fin_cases`/`simp`), and `cf_sym`/`cf_loop` (`decide`);
- `colorable_of_occ_dred (hD : DCheck18.dReducible cf = true) … (h : Occ T ring int) (IH …) : T.graph.Colorable 4`.
  Axioms: propext, Classical.choice, Quot.sound, `check4..9`.

**Open premises.**
- `hD`: one per key. It is discharged when studio14c/14d report D=true. A `native_decide` proof of it would re-run the 5–165 h evaluation.
- Mirror orientation: each module covers the orientation that matches the dfast line. Mirror images need their own `hD` or a mirror-invariance lemma.
- Building the build `Occ` from the discharging argument's "2-ball appears" (an `Appears → Occ` bridge, as `AppearsOcc` does for the diamond) is not done here.

**Ring ≤ 15 K=1 keys: not run.**
- About 8–12 s per key. For the roughly 2.9k Studio-D keys (Job 14) that is about 8 core-h; for all roughly 19k K=1 keys in R, about 50 core-h. Generated files are about 2 MB per 50 keys, so they would be checked and logged rather than committed.
- Their `hD` facts are dfast18 results, not Lean runs, so each key would also need a checker run (`DCheck16/18`, fast at ring ≤ 15).
