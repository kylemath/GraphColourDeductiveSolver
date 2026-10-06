# wp20/ (WP20 working directory)

- `input-m5-<n>.txt`: `plantri -m5 -a n` stdout for orders 16, 17, 18 (regressions) and 20, 22 (timing). All spent or already-seen orders; **not** the declared data.
- `regression-m5-<n>.json`: producer output on 16, 17, 18. Matches the known facts: order 16 has 0 SEP-bad states, order 17 has 8 (all depth 1) and 32 locked classes, order 18 has 0 (state counts 1116, 2146, 7900).
- `timing-m5-20.json`, `timing-m5-22.json`: producer output for cost extrapolation (order 22 is the first 120 graphs only). **Exploratory, post hoc, spent orders.** Order 20: 0 SEP-bad. Order 22 (120 graphs): 2 SEP-bad, both depth 1.
- Phase outputs for P1 (order 25) will be written here after the go-ahead and release.
