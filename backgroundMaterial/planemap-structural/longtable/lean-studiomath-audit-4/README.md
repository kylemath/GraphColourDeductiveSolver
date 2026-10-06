# J8: rerun of the audit's §2 check on Studio Math's Lean files with Theorem HP (Mac Studio)

This is the same procedure as ../lean-studiomath-audit-3/ (J7), from the 1520 audit message, §2. The audit writes the verdict; this README only records what was run.

- Machine: Kyles-Mac-Studio.local, Apple M4 Max. Run 2026-10-06 14:39:15-14:39:27 MDT (`times.txt`), at nice -n 10.
- Commits:
  - Files: detached worktree ~/studio-scratch/main-wt2 at origin/main 24563a3 (contains studio-math 51f222b). SHA256SUMS lists EulerSharp.lean (7aa2015a..., unchanged since J7) and VacancyIcosahedral.lean (bfa9f7a1...).
  - B=$HOME/mathlib4-planemap-build: PlaneMap 8299419 over Mathlib 300d0e5, Lean v4.35.0-rc3.
- Script: `run_j8.sh`.
  - The grep list (which already includes native_decide) is unchanged from the audit's command.
  - It has the J7 prints plus `#check` and `#print axioms` for SphericalMap.theorem_HP, Icosahedron.theorem_HP_icosahedron and VacancyIcosahedral.hp_cases, appended to the VacancyIcosahedral copy before the sweep.
- Negative control: the planted `sorry` theorem, in a second EulerSharp copy, before the sweep.
- Outputs, verbatim:
  - `shasum-c.txt`: two files OK, exit 0.
  - `grep.txt`: no output (grep exit 1).
  - `audit_EulerSharp.out`
  - `audit_VacancyIcosahedral.out`
  - `audit_EulerSharp_negcontrol.out`
  - the compiled /tmp copies (`audit_*.lean`).
