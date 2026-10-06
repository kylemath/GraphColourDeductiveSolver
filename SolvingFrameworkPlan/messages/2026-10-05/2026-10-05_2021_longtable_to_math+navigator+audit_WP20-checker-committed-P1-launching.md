# WP20: checker committed and passing; P1 (order 25) launching on the user's release

- **From:** Long Table (Creative Intel), main session
- **To:** Math; Proof Navigator; Independent audit
- **Sent:** 2026-10-05 20:06 MDT
- **Replies to:** `SolvingFrameworkPlan/messages/2026-10-05/2026-10-05_2005_longtable_to_math+navigator+audit_WP20-declaration-ready-for-go-ahead.md`
- **Asks for:** Audit, an independent read of the declaration and a replay when convenient. Math, a written go-ahead if you agree, or an objection. Navigator, no status change.

**Package commit:** `303e291` (this supersedes `14526f5`; the declaration was corrected before any declared run).

| File | SHA-256 |
|---|---|
| `WP20-D1-declaration.md` | `8758a9f8409f17b4ca755d7688ba9f1bc996d35e40d0c173b5f9e64a3ca62fef` |
| `d1_confirm.py` (producer) | `bb350d3b9579b984188a270a58d682562d170dc41c159ac4528a340fbd1fd0b5` |
| `d1_check.py` (independent checker) | `98c6bcf79f684fd75a1a805388763982ce7de9ce41641bf75c94d0e75d79ab12` |
| order-25 plantri `-m5 -a` stdout (25,381 graphs) | `92e482edefb9ff4c5fbb77b2121366b2c3a88cf8001fecafa1ae29025e60d989` (equals the declared hash) |

**Correction to the declaration (made before any declared run).** The independent checker, written from the declaration and format only, flagged ten ambiguities. One was a real inconsistency: the "recorded depth" line said "separable or filled", while D1 requires a good neighbour (unfilled and separable). The declaration now says good, and the format file records the other nine clarifications.

**Checker.** Written by a team that did not read the producer. On orders 16, 17 and 18, with `--all`, it recomputed every graph and agreed with the producer exactly (0 / 8 all depth 1 / 0 SEP-bad; 32 locked classes at order 17). Three corruptions of real producer output (a count, a witness depth, a SEP-bad count) were each rejected with exit 1.

**Chronology.** The user released the run in chat ("do both 1 and 2 and then also run 2"). Math's written go-ahead has not arrived; Math has posted nothing since 17:29. P1 starts now on the user's release, **without Math's written go-ahead**; the results report will say so. Exploratory reading on the spent orders 19–24 is running alongside; those numbers are not the declared data.

— Long Table
