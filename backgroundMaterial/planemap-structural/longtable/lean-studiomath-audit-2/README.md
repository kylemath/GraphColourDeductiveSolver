# J6: rerun of the audit's §2 check on Studio Math's updated Lean files (Mac Studio)

This uses the procedure of the 1520 audit message, §2 (as in ../lean-studiomath-audit/), on the updated files. The audit writes the verdict; this README only records what was run.

- Machine: Kyles-Mac-Studio.local, Apple M4 Max. Run 2026-10-06 14:28:10-14:28:20 MDT (`times.txt`), at nice -n 10.
- Commits:
  - Files: detached worktree ~/studio-scratch/main-wt2 at origin/main 8e131b3 (contains the studio-math merge 849a228). The folder SolvingFrameworkPlan/docs/working/StudioMathLean holds EulerSharp.lean and VacancyIcosahedral.lean; EulerCounting.lean is deleted, and SHA256SUMS lists only these two.
  - Built checkout B=$HOME/mathlib4-planemap-build: PlaneMap 8299419 over Mathlib 300d0e5, Lean v4.35.0-rc3 (../lean-8299419/).
- Script: `run_j6.sh`. The statement prints were appended before the sweep:
  - VacancyIcosahedral copy: SphericalMap.theorem_H, icoBall_of_triangulated, Icosahedron.theorem_H_icosahedron, SphericalMap.NoSeparatingTriangleAt (#print), SphericalMap.ico_fill, VacancyIcosahedral.IcoBall (#print).
  - EulerSharp copy: SphericalMap.twelve_light_fives, edge_card_bound_sharp, Icosahedron.twelve_light_fives_icosahedron, StudioMath.goodSet and highSet (#print).
- Negative control: `theorem auditPlanted : (1:ℕ) = 2 := sorry` appended before the sweep in a second EulerSharp copy, because EulerCounting no longer exists.
- Outputs, verbatim:
  - `shasum-c.txt`: two files OK, exit 0.
  - `grep.txt`: no output (grep exit 1).
  - `audit_EulerSharp.out`
  - `audit_VacancyIcosahedral.out`
  - `audit_EulerSharp_negcontrol.out`
  - the compiled /tmp copies (`audit_*.lean`).
