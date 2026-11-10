# k19 relaunch (prepared by Studio 10 Nov 2026 after the ~20:28Z reboot; NOT run, awaiting k / coordinator)

The third k19 run (wheelcheck18, ring-19 K≤1 key) started on 2 Nov 13:42 local and died in the 10 Nov ~20:28Z reboot after about 7 d 20 h
at nice 19. `k19.out` and `k19.time` are 0 bytes, so there is no result. wheelcheck18 cannot checkpoint, so a relaunch starts from scratch.

Reconstruction:
- From the pre-reboot `ps` line: `caffeinate -i zsh -c nice -n 19 /usr/bin/time -l <reverent-cartwright>/…`.
- From the files: the input is `k19` in this folder (studio14d, inspiring-lamport worktree); the outputs are this folder's
  `k19.out` / `k19.time`, last written 2 Nov 13:42.
- Matches RESTART.md (17 Oct), except at nice 19 instead of 10.

**One-step relaunch** (from this folder; detached, survives a session restart but NOT a reboot):

    cd /Users/kylemathewson/GraphColourDeductiveSolver/.claude/worktrees/inspiring-lamport-831744/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/studio14d
    mkdir -p k19_attempt3 && mv k19.out k19.time k19_attempt3/ 2>/dev/null
    nohup caffeinate -i zsh -c 'nice -n 19 /usr/bin/time -l /Users/kylemathewson/GraphColourDeductiveSolver/.claude/worktrees/reverent-cartwright-aa34d5/backgroundMaterial/planemap-structural/longtable/reducibility/dcheck/.lake/build/bin/wheelcheck18 k19 > k19.out 2> k19.time' < /dev/null > /dev/null 2>&1 &

- Binary: `wheelcheck18`, md5 4cbc2897, built 14 Oct, in the reverent-cartwright worktree.
- Input: `k19` (this folder).
- Expected run time ≈ 165 CPU-h at full speed (RESTART.md); the last run had 7 d 20 h at nice 19 and did not finish.
- Caveats:
  - The exact redirections inside the zsh -c are inferred: the ps line was truncated. The output file names match the
    0-byte files.
  - At nice 19 with the current Lean queues it will run below a full core.
