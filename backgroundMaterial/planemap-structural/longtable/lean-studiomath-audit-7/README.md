# J11: the audit's §2 check including MinimalFrame.lean, Mac Studio

This is the procedure of J10 (../lean-studiomath-audit-6/) plus MinimalFrame. The audit writes the verdict.

- Run 2026-10-06 15:21:01-15:22:06 MDT (`times.txt`), at nice -n 10, on Kyles-Mac-Studio.local (Apple M4 Max).
- Files: worktree ~/studio-scratch/main-wt2 at origin/main dcb7818. SHA256SUMS lists six files: EulerSharp, MinimalFrame (08cf33da...), RStar, RStarCore, SideTriangle and VacancyIcosahedral. The folder's check.sh compiles all six into a copy-on-write clone of B, as in J9 and J10.
- Prints added to J10's (MinimalFrame copy): `#print` RStarNoSepTri; `#check` and `#print axioms` four_color_of_RStar_noSepTri and rStarNoSepTri_of_core.
- A first J11 attempt at 15:18:59 compiled every file, but a script slip dropped the MinimalFrame prints. It was discarded and rerun; only the rerun's outputs are here.
- Negative control: the planted `sorry` theorem in a second EulerSharp copy.
- Outputs, verbatim: `check-sh.txt`, `shasum-c.txt`, `grep.txt`, `audit_*.out`, and the compiled /tmp copies.
