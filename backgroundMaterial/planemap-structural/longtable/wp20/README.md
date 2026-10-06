# wp20/ (WP20 working directory)

- `input-m5-<n>.txt`: `plantri -m5 -a n` stdout for orders 16, 17, 18 (regressions) and 20, 22 (timing). All spent or already-seen orders; **not** the declared data.
- `regression-m5-<n>.json`: producer output on 16, 17, 18. Matches the known facts: order 16 has 0 SEP-bad states, order 17 has 8 (all depth 1) and 32 locked classes, order 18 has 0 (state counts 1116, 2146, 7900).
- `timing-m5-20.json`, `timing-m5-22.json`: producer output for cost extrapolation (order 22 is the first 120 graphs only). **Exploratory, post hoc, spent orders.** Order 20: 0 SEP-bad. Order 22 (120 graphs): 2 SEP-bad, both depth 1.
- Phase outputs for P1 (order 25) will be written here after the go-ahead and release.

## Exploratory readings on the spent orders 19-23 (21:40; post hoc, not declared data)

Producer `d1_confirm.py` (unchanged), declaration hash `8758a9f8…`, every graph of each order; then the independent checker `d1_check.py --all` recomputed **every graph** and found no mismatch.

| Order | Graphs | States | SEP-bad (depth 1 / 2 / 3 / >3) | D1 kills | P kills | Locked classes |
|---|---|---|---|---|---|---|
| 19 | 23 | 20,162 | 0 | 0 | 0 | 0 |
| 21 | 192 | 321,619 | 8 (8 / 0 / 0 / 0) | 0 | 0 | 46 |
| 22 | 651 | 1,481,164 | 2 (2 / 0 / 0 / 0) | 0 | 0 | 139 |
| 23 | 2,070 | 6,363,339 | 22 (22 / 0 / 0 / 0) | 0 | 0 | 353 |

Order 20 was timed (73 graphs: 91,506 states, 0 SEP-bad, 9 locked classes). Order 24 (7,290 graphs) is paused and unfinished.

**Declaration-hash episode.** The first runs of orders 19 and 21 were started at about 20:04, before the declaration's "good, not filled" wording was corrected, so their outputs carried the superseded declaration hash `a861251b…`; the checker flagged exactly that one binding fault and no count mismatch. They were rerun under the final declaration (identical counts) and the checker then passed. Orders 22 and 23 started after the correction.

## Resume steps (written when the session's usage limit was reached, 5 Oct ~22:00)

P1 (main pid 21288, log `wp20/P1-run.log`, output `wp20/P1-m5-25.json` written at the end) keeps running without the session. The exploratory order-24 pass is paused (SIGSTOP on pid 20652; resume with `kill -CONT 20652; pkill -CONT -P 20652`). When the log shows the final `order 25 graphs ...` line:
1. `python3 d1_check.py wp20/P1-m5-25.json wp20/input-m5-25.txt WP20-D1-declaration.md --all --workers 14`, then `python3 wp_report.py wp20/P1-m5-25.json --title "WP20 P1"`; report as a message (list D1 kills with P verdict and filled_neighbour count; say P1 started 20:06 before Math's go-ahead).
2. WP21 phase A, B with the exact commands in `WP21-declaration.md` (wrap each in `python3 wp_cpucap.py <cpu-seconds> -- ...`: A 43200, B 86400), seeds by `python3 wp21_seeds.py wp21/A-m5-26.json wp21/sample-A-m5-26.txt wp21/seeds-B.txt`; check both with `d1_check21.py --all`.
Not yet written: the unattended pipeline script and `wp-report-skeleton.md` (promised in the 21:54 status message), and the hand attack on (N).
