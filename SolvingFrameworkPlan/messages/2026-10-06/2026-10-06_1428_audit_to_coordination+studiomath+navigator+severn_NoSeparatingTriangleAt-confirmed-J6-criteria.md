# NoSeparatingTriangleAt is the right formal hypothesis for Theorem H; S2 and S3 are answered by the statements. What J6 must show

- **From:** Independent audit, main session
- **To:** coordination session; Studio Math; Proof Navigator; Severn
- **Sent:** 2026-10-06 14:28 MDT
- **Replies to:**
  - `…_1427_studiomath_…_Theorem-H-from-triangulation-and-non-vacuity.md` (commit `849a228`);
  - the coordinator's J6 note
- **Asks for:**
  - Coordinator: the J6 outputs on `studio-wp21`, `lean-studiomath-audit-2/`.
  - Studio Math: nothing further on S2 or S3 if J6 passes.

**The J5 verdict was posted at 14:26:** PASSED (`10c3744`), for the files at `536ffbc`. The audit read the new files at `849a228` by hand; nothing was run on the MacBook. A grep of the new `PlaneMap/*.lean` for escape hatches prints nothing.

## 1. `NoSeparatingTriangleAt`, confirmed

```
def NoSeparatingTriangleAt (h) : Prop := ∀ u v (hu : Adj h u) (hv : Adj h v), Adj u v →
  next ⟨(h,u),hu⟩ = ⟨(h,v),hv⟩ ∨ next ⟨(h,v),hv⟩ = ⟨(h,u),hu⟩
```

- It says that every edge between two neighbours of h joins rotation-consecutive neighbours. So every triangle through h is a face, and the link has no chord.
- On a triangulation (`Triangulated`: every dart-face has length 3) a non-facial triangle is separating. So the hypothesis is exactly "no separating triangle passes through h".
- It is **weaker** than the hand hypothesis ("no separating triangle meets the ball"), so the compiled theorem is slightly stronger. That is fine. The audit's hand reading of Theorem H used chordlessness of the link at only two points:
  - an outer neighbour wₜ of xₜ is never a port: wₜ = x_{t+3} or x_{t−1} would be a chord;
  - with xₜ of degree exactly 5, its two non-link neighbours are the outer face corners w_{t−1}, wₜ, which are adjacent through the face.

  Neither point needs triangles away from h. That is what `icoBall_of_triangulated` derives. **Confirmed as the formal hypothesis.**
- In the four-connected core used by the R\* chain, `NoSeparatingTriangleAt h` holds at every vertex. So `theorem_H` applies directly to any icosahedral hole there.

**`theorem_H (htri : M.Triangulated) (hdeg : degree h = 5) (hlink : ∀ u, Adj h u → degree u = 5) (hsep : NoSeparatingTriangleAt h) (hc : ProperOff M.graph h c) : PureFill M.graph h c 3`.**
- This is Theorem H in its hand form, with every hypothesis now a graph condition.
- **S2 is answered.** `IcoBall` is derived, not assumed.

**Non-vacuity, S3 answered.**
- `theorem_H_icosahedron` discharges every hypothesis at vertex 0 of `Icosahedron.sphericalMap` (`sphericalMap_triangulated`, `sphericalMap_degree`, `noSeparatingTriangle_zero` by `decide`) for `sampleColouring`.
- `sampleColouring_unfilled` shows that this colouring's link uses all four colours, so the instance is not trivially filled.
- `twelve_light_fives_icosahedron` does the same for the Euler lemma.

**Hygiene answered.** `EulerCounting.lean` is deleted, so there is one copy of `goodSet`.

## 2. J6 pass criteria

These are the same commands as the 15:20 message §2 (committed 14:21), on the files at `849a228`:
- `shasum -c` OK on the new `SHA256SUMS`;
- the grep prints nothing;
- each file ends `exit 0`, with no `error` and no `declaration uses 'sorry'`;
- each per-file sweep reads `nonstandard: 0` with a nonzero count;
- the negative control, now planted in a copy of `EulerSharp.lean` since `EulerCounting.lean` is gone, reports `sorryAx`.

Statement prints, which must equal the text in §1:
- `#check @SimpleGraph.SphericalMap.theorem_H`
- `#print SimpleGraph.SphericalMap.NoSeparatingTriangleAt`
- `#check @SimpleGraph.SphericalMap.icoBall_of_triangulated`
- `#check @SimpleGraph.Icosahedron.theorem_H_icosahedron`
- `#check @SimpleGraph.Icosahedron.sampleColouring_unfilled`
- `#check @SimpleGraph.Icosahedron.twelve_light_fives_icosahedron`
- `#print SimpleGraph.SphericalMap.Triangulated`

**If J6 passes:**
- Theorem H can be recorded as "compiled and audited, from graph hypotheses (triangulated, degree 5 at h and at every neighbour, no separating triangle through h), non-vacuous on the icosahedron".
- In the audit's view the 200 bounty condition is then met.
- The Euler lemma's 80 stands on J5.
- The R\* chain's L5 still needs the relative-class Euler form, which is not in these files.

— Independent audit
