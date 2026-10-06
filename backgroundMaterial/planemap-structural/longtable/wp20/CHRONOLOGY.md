# WP20 chronology (as stated by Long Table and Math; not bound to any hash)

All times MDT, 5 October 2026. Machine-clock readings are Long Table's; Math's message headers carry Math's own times.

1. Declaration, format and producer committed (`14526f5`); regressions on orders 16–18 pass.
2. Independent checker written blind from the declaration and format, committed with the corrected declaration (`303e291`). Checker agrees with the producer on orders 16, 17, 18 with `--all`; three corruptions of real output are rejected.
3. **P1 started at 20:06** (order 25, every graph, 25,381; input hash equals the declared `92e482ed…d989`), on the user's chat release ("do both 1 and 2 and then also run 2"). No written Math go-ahead existed at that time. Math had posted nothing since 17:29. Long Table recorded this in `messages/2026-10-05/…_2005_…` and `…_2006_…`.
4. Math's written go-ahead for **P1 only** is `messages/2026-10-05/2026-10-05_2042_math_to_longtable+navigator+audit_catch-up-reviews-and-WP20-go-ahead.md`. Its header says Sent 20:42; Long Table found the file at about 20:39 on the machine clock. The two clocks disagree by a few minutes, and either way the go-ahead is **after** P1 started. It does not backdate P1. The go-ahead names declaration `8758a9f8409f17b4ca755d7688ba9f1bc996d35e40d0c173b5f9e64a3ca62fef`, package commit `303e291`, producer `bb350d3b…fd0b5`, checker `98c6bcf7…ab12`, and input hash `92e482ed…d989`. P2 is not covered and does not run under the declaration's own cost rule.
5. The user's release reached Math only through Long Table's quotation of the chat; the user may confirm it.
6. Condition from Math: the results report must list every D1 kill with its P verdict and its `filled_neighbour` count, so that a wording kill is not read as a failure of the pure fill. The checker is to be run with `--all` after P1.

The results report will keep stating that P1 started before Math's written go-ahead.

## Coordination (added 20:47)

7. **The user's own statements to Long Table, in chat**, are the authority. A few minutes earlier the user told Long Table that the coordination session ("Agent team coordination and navigation") is coordinating all three agent teams, and that the Math agent works the math side. Asked whether the coordinator has authority, the user answered **"yes the coordinator has authority"**.
8. **The coordination session's message** (about 20:47) is recorded **as a relay only**: it says the user told it, in chat, that it may prioritise and sequence work, route messages, resolve ordering disputes, and ask teams to proceed without waiting for confirmation. It states that this is **not a release of any new computation**: WP experiments still need a declaration, a written go-ahead naming its hash, and the user's release (`START-HERE.md` §5) unless the user states otherwise for a specific run. Long Table agrees with that scope.
9. P1's release is item 3 above and is unchanged by items 7 and 8. P2 is not covered by any release and does not run.

## Relayed standing release (added 20:49)

10. The coordination session relayed a user statement from 20:48 ("push forward don't wait for my release follow the plan the navigator leads the way and gates success", file `messages/2026-10-05/2026-10-05_2048_user_to_longtable+math+navigator+audit_standing-release-navigator-gates.md`). It reached Long Table **only as a relay**, not from the user. P1 does not depend on it: P1 was released by the user directly in chat (item 3). The checker run and the results report are not new experiments. Long Table will **not** start a new declared phase on the strength of the relay alone; if one is wanted, Long Table asks the user directly. This is a narrower reading than the file allows; the coordination session invited such readings by message.
