# J5: the audit's §2 check of Studio Math's Lean files, run on the Mac Studio

Instructions: SolvingFrameworkPlan/messages/2026-10-06/2026-10-06_1520_audit_to_coordination+studiomath+navigator+severn_Euler-and-H-Lean-statements-and-studio-check.md, §2. The audit writes the verdict; this README only records what was run.

- Machine: Kyles-Mac-Studio.local, Apple M4 Max, macOS 15.5. The run was 2026-10-06 14:25:04-14:25:35 MDT (`times.txt`), at nice -n 10.
- Commits:
  - Instructions and files: detached worktree ~/studio-scratch/main-wt2 at origin/main 2effe65, which contains the audit commit 0ab1cb1. `SolvingFrameworkPlan/docs/working/StudioMathLean` is unchanged between 536ffbc and 2effe65, so the files are as at 536ffbc.
  - Built checkout B=$HOME/mathlib4-planemap-build: PlaneMap 8299419 over Mathlib 300d0e535721bc098547106fc297d8ba2a63f6bb, Lean v4.35.0-rc3. Its build is recorded in ../lean-8299419/.
- Script: `run_j5.sh`, which runs the audit's commands. Two layout choices are mine:
  - the statement prints (`#check`/`#print` lines) were appended to the EulerSharp and VacancyIcosahedral copies before the sweep;
  - the negative-control line `theorem auditPlanted : (1:ℕ) = 2 := sorry` was appended to a second EulerCounting copy before the sweep.
  The /tmp copies that were compiled are included (`audit_*.lean`).
- Outputs, verbatim:
  - `shasum-c.txt`: three files OK, exit 0.
  - `grep.txt`: no output (grep exit 1).
  - `audit_EulerCounting.out`
  - `audit_EulerSharp.out`
  - `audit_VacancyIcosahedral.out`
  - `audit_EulerCounting_negcontrol.out`
