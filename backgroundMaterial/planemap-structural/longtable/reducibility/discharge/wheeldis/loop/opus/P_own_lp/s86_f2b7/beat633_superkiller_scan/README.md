# beat_633 stage-1 leaf profile: super-killer candidate scan (Opus, 11 Nov 2026 05:30Z)

Read-only scan, no solve and none of the outside binaries run. Input is k's outside team data on
origin/main 6eca7e244 under `.../wheeldis/out/job_OUTSIDE2/beat_633/data/`:
`stage1_ext_profile.jsonl` (167,990 leaves), `pool_configs.json` (4,095 configs, first 633 = RSST),
`synth_active.txt` (598 ids kept after Pass 1). The copies on main are byte-identical to
`/mnt/project-files/swarm/outside/` (MD5SUMS 362443df beat_633, 67cd081d fullstack_t0).

## What the profile is

`solve_hitting_set.py` calls `fast_compress --mode profile --k-thin 1 --cap-per-cfg 400` on the 71 RSST
parts with all 633 configs active. Each line is one positive leaf killed by exactly ONE RSST config
(`kS`, a "forced leaf" of that config) plus every pool config that kills it (`kU`).
The cap stops at about 400 leaves per config, in enumeration order.

## Findings (all on the capped sample, [P], one reader)

- 310 of 633 configs are at the cap, so the set "more than 600 forced leaves" cannot be read from this
  file. An at-cap sample covers a median of 3 link words (often 1), so it is not a fair sample.
- None of the 35 Pass 1 drops was at the cap (their sampled counts are 2..281).
- 463 of 633 configs have every sampled forced leaf also killed by one single non-RSST pool config
  (a 1-for-1 swap, no gain; consistent with the note's "0 k-for-1 swaps" under the 71 parts).
- 16 pool configs kill 90% or more of the sampled forced leaves of two or three RSST configs:
  `superkiller_candidates.tsv`. All 16 are D, ring 11 to 13 (nl51 family). Taken disjointly over configs
  still active after Pass 1 that is 11 merges and 13 configs saved at most. Best: nl1583_r11 for
  7322.122 + 7566.123 + 7386.126, and nl6326_r13 for 39782.1023 + 11780.363 + 7322.3682920.
- 14 configs (13 of ring 14) have every sampled forced leaf killed by nothing else in the pool; 50 have
  at least half such. For those only new rules or new configs can help. 10,205 of the 167,990 sampled
  leaves have no other pool killer.

## What it does not show

A merge of a and b also needs the leaves that only a and b kill together (not in a k-thin 1 profile) and
the uncapped forced leaves. Sizing the residual that "1-2 surgical rules" must cover needs an uncapped
profile with the pair removed, on the final beat_633 rule file (Pass 2+), from an engine that expresses
those parts (not eng_p8 or eng_v2).

## Files

- `per_config.tsv`: 633 rows: sampled forced leaves, at-cap flag, sampled words, leaves with no other
  pool killer, best external config and its cover, Pass 1 status.
- `superkiller_candidates.tsv`: the 16 candidates with the RSST configs each covers.
- `code/cover2.py`: `python3 -I cover2.py DATA_DIR OUT_DIR`.
