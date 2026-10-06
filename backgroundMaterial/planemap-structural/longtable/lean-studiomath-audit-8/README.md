# J12: the audit's extended check (section 3 of the 1618 audit message), run by Studio compute on the Mac Studio

- Instructions: SolvingFrameworkPlan/messages/2026-10-06/2026-10-06_1618_audit_to_coordination+studiomath+navigator_RStarFrame-statement-PASS-and-J12-extended.md, section 3.
- Clean detached checkout of main at 22ff2722a958cd4ca28cbb585a244b03c07a3514 (`commit.txt`; contains 0a804bc). Run 2026-10-06 16:32:01-16:42:04 MDT on Kyles-Mac-Studio.local (Apple M4 Max).
- Base: B = ~/mathlib4-planemap-build (PlaneMap 8299419 over Mathlib 300d0e5, Lean v4.35.0-rc3).
- Procedure (as J11, `run_j12.sh`):
  1. the folder's `check.sh` compiles all 23 modules, in order, into a copy-on-write clone of B; output in `check-sh.txt`, exit 0;
  2. `shasum -c SHA256SUMS`: 23 OK, exit 0;
  3. the escape-hatch grep over every .lean file in the folder printed nothing (`grep.txt`);
  4. per-module audit copies (the prints of section 3, then the audit's axiom sweep) compiled against the clone;
  5. a negative control: a planted `sorry` in a second FrameF3 copy.
- Cap: `ulimit -t 1800` (30 CPU-min) per Lean process. No module came near it; the longest audit copy took 18 s wall.
- Outputs are verbatim: `audit_*.out`, and the compiled copies `audit_*.lean`.

## Per-module result
See `PASS-table.md`: all 17 modules PASS (exit 0, no error, no sorry, nonstandard 0 with a nonzero count), and the control is caught (`(auditPlanted, sorryAx)`).

## Prints (raw, for the audit's comparison with section 1)
- `RStarFrame`: for all m, T, given 0 < m, Connected, Triangulated, min degree >= 5, NoSep, DiamondFree and Conf2122Free, there exists v of degree 5 with PureClean T v.
- `DiamondFree`: no DiamondM.Occ and no DiamondP.Occ.
- `Conf2122Free`: no C2122M.Occ and no C2122P.Occ.
- `four_color_of_RStarFrame`, `rStarFrame_of_noSepTri`, `DiamondM.colorable_of_occ` and `C2122M.colorable_of_occ` all depend on [propext, Classical.choice, Quot.sound].
- RStarSanity: `occ_DiamondM` and `occ_DiamondP` hold in the icosahedron's sphericalMap, `not_diamondFree`, and `conf2122Free`.
- RadiusFive: `R80.pureFill` (hole 23) and `R91.pureFill` (hole 22).
