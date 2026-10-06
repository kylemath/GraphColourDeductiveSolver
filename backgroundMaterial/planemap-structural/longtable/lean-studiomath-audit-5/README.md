# J9: the audit's §2 check on Studio Math's Lean files including RStar.lean (Mac Studio)

This is the procedure of J8 (../lean-studiomath-audit-4/), from the 1520 audit message, §2, now with PlaneMap/RStar.lean (links A-C). The audit writes the verdict; this README only records what was run.

- Machine: Kyles-Mac-Studio.local, Apple M4 Max. Run 2026-10-06 14:47:28-14:47:43 MDT (`times.txt`), at nice -n 10.
- Commits:
  - Files: detached worktree ~/studio-scratch/main-wt2 at origin/main c47ef19 (contains studio-math 11a40d7). SHA256SUMS lists EulerSharp.lean (7aa2015a...), RStar.lean (279f1233...) and VacancyIcosahedral.lean (bfa9f7a1...).
  - B=$HOME/mathlib4-planemap-build: PlaneMap 8299419 over Mathlib 300d0e5, Lean v4.35.0-rc3.
- One change from the audit's LEAN_PATH, needed because RStar.lean imports VacancyIcosahedral, which is a Studio Math module and not in B:
  - The folder's own `check.sh` was run first (`check-sh.txt`, exit 0). It makes a copy-on-write clone of B's built Mathlib tree into a private directory, W=~/studio-scratch/j9/w, and compiles EulerSharp, VacancyIcosahedral and RStar there. B itself is not written to.
  - All audit copies were then compiled with LEAN_PATH = W + B's package directories, in place of B's own lib.
- Script: `run_j9.sh`. It has the J8 prints. The RStar copy adds `#print SimpleGraph.SphericalMap.PureClean`, plus `#check` and `#print axioms` for four_color_of_global_Rstar, pureClean_of_theorem_H and pureClean_of_theorem_HP, before the sweep.
- Negative control: the planted `sorry` theorem, in a second EulerSharp copy, before the sweep.
- Outputs, verbatim:
  - `check-sh.txt`
  - `shasum-c.txt`: three files OK, exit 0.
  - `grep.txt`: no output (grep exit 1).
  - `audit_EulerSharp.out`
  - `audit_VacancyIcosahedral.out`
  - `audit_RStar.out`
  - `audit_EulerSharp_negcontrol.out`
  - the compiled /tmp copies (`audit_*.lean`).
- A first attempt at 14:46:51 failed before compiling anything, because check.sh expects its scratch directory to exist; nothing from that attempt is kept. The script now creates W first.
