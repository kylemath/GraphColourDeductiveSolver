# The audit's radius-5 replay, run on the Mac Studio

- Instructions: SolvingFrameworkPlan/messages/2026-10-06/2026-10-06_1501_audit_to_coordination+studiomath+studiointel_radius-5-replay-single-command.md.
- Command, from the root of a detached worktree of origin/main at 01fa26a (contains the audit commit c8ff230):
  `bash backgroundMaterial/planemap-structural/longtable/audit/radius5-replay/run_replay.sh ~/studio-scratch/r5`
- Machine: Kyles-Mac-Studio.local, Apple M4 Max, Python 3.9.6. 2026-10-06 15:03:13 MDT; the whole script took under a second of wall time.
- This folder holds all of `<outdir>`, verbatim: commit.txt, shasums.txt, times.txt, and a .json and .err file for each step. All .err files are empty. The audit writes the verdict.
