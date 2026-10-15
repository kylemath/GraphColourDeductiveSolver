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
