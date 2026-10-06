# J10: the audit's §2 check on Studio Math's Lean files including link D (SideTriangle, RStarCore), Mac Studio

This is the procedure of J9 (../lean-studiomath-audit-5/), from the 1520 audit message, §2. The audit writes the verdict.

- Run 2026-10-06 15:17:13-15:17:42 MDT (`times.txt`), at nice -n 10, on Kyles-Mac-Studio.local (Apple M4 Max).
- Files: detached worktree ~/studio-scratch/main-wt2 at origin/main 2ae01b9 (contains studio-math 7a3cf9e). SHA256SUMS lists EulerSharp, RStar, RStarCore, SideTriangle and VacancyIcosahedral.
- As in J9, the folder's own `check.sh` first compiles the five modules into a copy-on-write clone of B (~/studio-scratch/j10/w; B=$HOME/mathlib4-planemap-build at 8299419 is not written). The audit copies then compile with LEAN_PATH = clone + B's packages.
- Prints added to J9's:
  - SideTriangle copy: `#print` RStarSupport and PureClean; `#check` and `#print axioms` four_color_of_RStarSupport.
  - RStarCore copy: `#print` RStarCore; `#check` and `#print axioms` four_color_of_core_Rstar and four_color_of_core_Rstar_planeMap.
- Negative control: the planted `sorry` theorem in a second EulerSharp copy.
- Outputs, verbatim: `check-sh.txt`, `shasum-c.txt`, `grep.txt`, `audit_*.out`, and the compiled /tmp copies (`audit_*.lean`).
