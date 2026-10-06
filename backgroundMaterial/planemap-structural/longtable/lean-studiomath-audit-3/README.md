# J7: rerun of the audit's §2 check on Studio Math's Lean files with relative_light_fives (Mac Studio)

This is the same procedure as ../lean-studiomath-audit-2/ (J6), from the 1520 audit message, §2. The audit writes the verdict; this README only records what was run.

- Machine: Kyles-Mac-Studio.local, Apple M4 Max. Run 2026-10-06 14:29:51-14:30:02 MDT (`times.txt`), at nice -n 10.
- Commits:
  - Files: detached worktree ~/studio-scratch/main-wt2 at origin/main dfc8a73 (contains studio-math daa4e1d). SHA256SUMS lists EulerSharp.lean (7aa2015a...) and VacancyIcosahedral.lean (34fa6a3f..., unchanged since J6). relative_light_fives is in EulerSharp.lean.
  - B=$HOME/mathlib4-planemap-build: PlaneMap 8299419 over Mathlib 300d0e5, Lean v4.35.0-rc3.
- Script: `run_j7.sh`. It has the J6 prints plus `#check @SimpleGraph.SphericalMap.relative_light_fives` and `#check @SimpleGraph.Icosahedron.relative_light_fives_icosahedron` (the non-vacuity instance: icosahedron, φ = {0, 1, 5}), appended to the EulerSharp copy before the sweep.
- Negative control: the planted `sorry` theorem, in a second EulerSharp copy, before the sweep.
- Outputs, verbatim:
  - `shasum-c.txt`: two files OK, exit 0.
  - `grep.txt`: no output (grep exit 1).
  - `audit_EulerSharp.out`
  - `audit_VacancyIcosahedral.out`
  - `audit_EulerSharp_negcontrol.out`
  - the compiled /tmp copies (`audit_*.lean`).
