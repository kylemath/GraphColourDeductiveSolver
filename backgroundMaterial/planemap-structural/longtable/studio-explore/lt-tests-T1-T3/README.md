# [exploratory] Long Table's Studio tests T1-T3, run on the Mac Studio

- Spec: SolvingFrameworkPlan/messages/2026-10-06/2026-10-06_1514_longtable_to_coordination+math+audit+navigator_selection-sketches-and-Studio-tests.md, section 3.
- Script: Long Table's `explore-vhphi/pathways/sel_selection.py` (commit 25243be), run from a detached worktree of origin/main at edeebac.
- Runner: `run.sh`. Each test is capped at 600 CPU-s (`ulimit -t`), at nice -n 10. Run 2026-10-06 15:22:49-15:23:16 MDT on Kyles-Mac-Studio.local (M4 Max).
- Tests:
  - T1: stack 6 3, stack 7/8/9 3 one, stack 7 4 one.
  - T2: pair pentakis, pair sixring28 all, pair T4 all, pair S6_3.
  - T3: certmin.
  - Also `census`.
- Outputs, verbatim: `<test>.out`, `<test>.err` (all empty) and `times.txt`. Every test exited 0, well under its cap.
- Not run here: Long Table's T4 (for Math's vdred), and the Tilley order-12 and Birkhoff-diamond-string tests, which need the graphs built first.
