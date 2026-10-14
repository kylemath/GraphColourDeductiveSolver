# Curvature near vs far from the hole, against locked-run length (exploratory, 14 Oct 2026)

**Prompted by** Kyle's look at the Gears skin: the densely packed centre looks like friction, and the hole sits
next to a freer region.

**Graph-intrinsic version.** Use curvature, i.e. degree-5 vertices (6 − deg > 0), counted at each distance from
the hole.

**Data.** Order-33 frame census, 979,741 holes. Script: `curv.py`; output: `curv-out.txt`.
- Difficulty measures: R, the longest interior π-run (locked run); NR; and mf, the minimum class F/N.
- All taken from `Census33/out/eval-33.jsonl.gz`.

**Findings (correlations only):**
- **More curvature within distance 2 means shorter locked runs.** Mean R falls from 0.81 to 0.60 as the number
  of degree-5 vertices within distance 2 rises from 2 to 14. P(R ≥ 4) falls from 0.47% to 0.
- **More curvature at distance ≥ 3 means longer locked runs.** Mean R rises from 0.80 to 0.93 as that count goes
  from 5 to 14, and P(R ≥ 4) from 0.09% to 0.24%.
- **Floor-tight classes** (mf = 1/4) peak at intermediate curvature (5–6 within distance 2).
- **Consistency:** this matches the wheel results. Degree-5 neighbours make small wheels D-reducible, and the
  flat 66666 hole is the hard case.

**Caveats.**
- Near and far counts are tied together by Euler's fixed total, so they cannot vary independently.
- The effects are moderate.
- Drawing density (Gears tile size) is partly a layout artefact. Curvature is the intrinsic quantity.
