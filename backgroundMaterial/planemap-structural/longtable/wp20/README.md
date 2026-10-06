# wp20/ (WP20 working directory)

- `input-m5-<n>.txt`: `plantri -m5 -a n` stdout for orders 16, 17, 18 (regressions) and 20, 22 (timing). All spent or already-seen orders; **not** the declared data.
- `regression-m5-<n>.json`: producer output on 16, 17, 18. Matches the known facts: order 16 has 0 SEP-bad states, order 17 has 8 (all depth 1) and 32 locked classes, order 18 has 0 (state counts 1116, 2146, 7900).
- `timing-m5-20.json`, `timing-m5-22.json`: producer output for cost extrapolation (order 22 is the first 120 graphs only). **Exploratory, post hoc, spent orders.** Order 20: 0 SEP-bad. Order 22 (120 graphs): 2 SEP-bad, both depth 1.
- Phase outputs for P1 (order 25) will be written here after the go-ahead and release.

## Exploratory readings on the spent orders 19-23 (21:36; post hoc, not declared data)

Producer `d1_confirm.py` (unchanged), declaration hash `8758a9f8…`, every graph of each order; then the independent checker `d1_check.py --all` recomputed **every graph** and found no mismatch.

| Order | Graphs | States | SEP-bad (depth 1 / 2 / 3 / >3) | D1 kills | P kills | Locked classes |
|---|---|---|---|---|---|---|
| 19 | 23 | 20,162 | 0 | 0 | 0 | 0 |
| 21 | 192 | 321,619 | 8 (8 / 0 / 0 / 0) | 0 | 0 | 46 |
| 22 | 651 | 1,481,164 | 2 (2 / 0 / 0 / 0) | 0 | 0 | 139 |
| 23 | 2,070 | 6,363,339 | 22 (22 / 0 / 0 / 0) | 0 | 0 | 353 |

Order 20 was timed (73 graphs: 91,506 states, 0 SEP-bad, 9 locked classes). Order 24 (7,290 graphs) is paused and unfinished.

**Declaration-hash episode.** The first runs of orders 19 and 21 were started at about 20:04, before the declaration's "good, not filled" wording was corrected, so their outputs carried the superseded declaration hash `a861251b…`; the checker flagged exactly that one binding fault and no count mismatch. They were rerun under the final declaration (identical counts) and the checker then passed. Orders 22 and 23 started after the correction.
