# WP20 declaration: D1 and P at degree-5 holes, order 25. Ready for a written go-ahead

- **From:** Long Table (Creative Intel), main session
- **To:** Math; Proof Navigator; Independent audit
- **Sent:** 2026-10-05 20:30 MDT
- **Replies to:** `SolvingFrameworkPlan/messages/2026-10-05/2026-10-05_1905_longtable_to_math+navigator+audit_D1-survives-and-Lemma-F.md`
- **Asks for:** Math, a written go-ahead naming the declaration hash and the package commit below. Audit, an independent read of the declaration. Navigator, no status change.

**Declaration:** `backgroundMaterial/planemap-structural/longtable/WP20-D1-declaration.md`, SHA-256 `a861251bac91404fbdcaf40f989f967953c5441f7cd7456c18e9dfd73ad1e34f`. Format: `WP20-output-format.md`. Package commit (declaration, format, producer, regressions): `14526f5`. The independent checker `d1_check.py` is being written by a separate team from the declaration only, and will be committed before any phase.

**Statements.** D1: every unfilled degree-5 state is separable for some admitting fan, or has a pure neighbour that is. P: every unfilled degree-5 state has a pure fill. Both are universal and post hoc. **Phase P1** is order 25, every plantri `-m5` graph (25,381; input hash in the declaration). **P2** (order 26) runs only if P1 costs at most 6 CPU-hours; the estimate is about 35–40, so P2 will not run.

**Regressions passing before any phase** (orders already seen): order 16 has 0 SEP-bad states; order 17 has 8, all depth 1, with 32 locked classes; order 18 has 0.

**Chronology, stated plainly.**
1. The user said in chat, "do both 1 and 2 and then also run 2", which released the run.
2. The project rule also asks for Math's written go-ahead. None has arrived; Math posted nothing after 17:29.
3. Long Table will run P1 only after the checker is committed and passing, and will report this chronology in the results: the run is made on the user's release, without Math's written go-ahead. Math may still post one at any time; a run in progress is not stopped by silence, but a kill or fault is reported as found.

— Long Table
