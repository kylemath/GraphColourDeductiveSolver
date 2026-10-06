# WP20 chronology (as stated by Long Table and Math; not bound to any hash)

All times MDT, 5 October 2026. Machine-clock readings are Long Table's; Math's message headers carry Math's own times.

1. Declaration, format and producer committed (`14526f5`); regressions on orders 16–18 pass.
2. Independent checker written blind from the declaration and format, committed with the corrected declaration (`303e291`). Checker agrees with the producer on orders 16, 17, 18 with `--all`; three corruptions of real output are rejected.
3. **P1 started at 20:06** (order 25, every graph, 25,381; input hash equals the declared `92e482ed…d989`), on the user's chat release ("do both 1 and 2 and then also run 2"). No written Math go-ahead existed at that time. Math had posted nothing since 17:29. Long Table recorded this in `messages/2026-10-05/…_2005_…` and `…_2006_…`.
4. Math's written go-ahead for **P1 only** is `messages/2026-10-05/2026-10-05_2042_math_to_longtable+navigator+audit_catch-up-reviews-and-WP20-go-ahead.md`. Its header says Sent 20:42; Long Table found the file at about 20:39 on the machine clock. The two clocks disagree by a few minutes, and either way the go-ahead is **after** P1 started. It does not backdate P1. The go-ahead names declaration `8758a9f8409f17b4ca755d7688ba9f1bc996d35e40d0c173b5f9e64a3ca62fef`, package commit `303e291`, producer `bb350d3b…fd0b5`, checker `98c6bcf7…ab12`, and input hash `92e482ed…d989`. P2 is not covered and does not run under the declaration's own cost rule.
5. The user's release reached Math only through Long Table's quotation of the chat; the user may confirm it.
6. Condition from Math: the results report must list every D1 kill with its P verdict and its `filled_neighbour` count, so that a wording kill is not read as a failure of the pure fill. The checker is to be run with `--all` after P1.

The results report will keep stating that P1 started before Math's written go-ahead.
