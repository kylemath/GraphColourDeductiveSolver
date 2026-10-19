# CGlue Lean draft (Long Table, 19 Oct 2026)

File: `backgroundMaterial/planemap-structural/longtable/reducibility/dcheck/CGlue.lean` (imports `ClaimGlue`, `C66666`).
Scope: `CGLUE-SCOPE.md`. Status: first draft, see "Build" below.

## Statement

```lean
structure CEntry where            -- SimpleGraph.SphericalMap.CGlue.CEntry
  cf : DCheck18.Conf
  eqR : List (ℕ × ℕ)              -- contracted ring–interior edges (t, a)
  eqI : List (ℕ × ℕ)              -- contracted interior edges (b, a)
  lbl : List ℕ                    -- admissibility certificate (labels of interior vertices, then ring positions)
  hC   : cReducible18 cf eqR eqI = true                    -- native_decide per key
  hadm : admissibleX (Conf.of18 cf) eqR eqI lbl = true     -- decide
  hr2 : 2 ≤ cf.r;  hr : cf.r ≤ 19;  hsym;  hloop;  hrr      -- decide

theorem CEntry.colorable (e : CEntry) (h : OccursCX e T) (IH : SmallerColorable T) : T.graph.Colorable 4
theorem four_color_of_unavoidableC (R : Registry) (hU : Unavoidable R) (M : SphericalMap n) : M.graph.Colorable 4
```

The theorems are in `SimpleGraph.SphericalMap.CGlue`; it holds its own `Registry`/`Unavoidable`, with D entries
of `ClaimGlue.DEntry`. `cGlueX : CGlueX Cs` is ClaimGlue's hypothesis `CGlue`, restated for these entries and proved.

TODO: fill in the rest of this note once the build check has run.
