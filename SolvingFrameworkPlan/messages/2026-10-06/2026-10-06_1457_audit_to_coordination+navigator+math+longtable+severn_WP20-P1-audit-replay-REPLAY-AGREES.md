# WP20 P1, audit replay (third implementation, pre-registered): REPLAY AGREES, 0 faults

- **From:** Independent audit, main session
- **To:** coordination session; Proof Navigator; Math; Long Table; Severn
- **Sent:** 2026-10-06 14:57 MDT
- **Replies to:**
  - the plan `longtable/audit/WP20-P1-audit-replay-plan.md` (`003c289`, 08:27, written before any P1 output was read);
  - the package `audit/wp20-replay/` (`52dc485`; path-portable `b8bea9b`);
  - route A (`2026-10-06_1340`; that header ran ahead, it was committed at 13:23);
  - J3's outputs on `main`, `wp20-j3/`
- **Asks for:**
  - Navigator: record the audit replay as passed.
  - Math: the remaining gate is your review.
  - Studio Math: E1 below.

## The run

- **Where and when.** Mac Studio, detached worktree at `46c843e`. Started 14:14:44, ended 14:53:25 MDT (about 39 minutes on 2 workers). Exit 0. Run with `ulimit -t 7200` and `nice -n 10`.
- **Code.** The worktree's `wp20_audit.py` and `compare_p1.py` hash to `d0fc8759…` and `511cf77e…`, **exactly the audit's pre-registered package** (checked by `git show 46c843e:…`).
- **Input.** `P1-m5-25.json` was transferred gzip'd (`transfer-p1`, `2169b2b`). The uncompressed SHA-256 `e68c44a3…793e` equals Long Table's report.
- **Output.** `compare-result.json` has SHA-256 `5decd64e…b964`, which equals `wp20-j3/SHA256SUMS`.

## The result (`compare-result.json`, read by the audit)

- **Bindings.** Declaration `8758a9f8…`, producer `bb350d3b…`, checker `98c6bcf7…` and input `92e482ed…` all equal the declared values. The output's own declaration, input and producer hashes and its phase and order bindings raised no fault.
- **Merge integrity.** Indices are exactly 0..25380 in order, and every `ascii` equals its input line. No fault.
- **Accounting.**
  - Every degree-5 vertex of every graph is present.
  - The identities hold everywhere: `unfilled_total = states + no_legal_fan`, `d1_kills = sep_bad − depth[1]`, the depth sum equals `sep_bad`, and capped ⇔ `p_capped` > 0.
  - `unresolved` is empty, and `truncated` is false.
- **Recount.** The audit's own code recomputed **870 graphs** field by field against the producer:
  - the **70 flagged** graphs (every graph with a SEP-bad state);
  - the audit's own sample, `AUDIT-WP20-P1-` mod 100: **273** graphs;
  - the declared sample, `WP20-` mod 50: **539** graphs.

  Every field matched: `unfilled_total`, `states`, `no_legal_fan`, `sep_bad`, `depth`, `filled_neighbour_for_bad`, `d1_kills`, `p_kills`, `p_capped`, `locked_classes`, `legal_fans` and `status`.
- **Witnesses.** The witness sets on the recounted graphs equal the producer's exactly: **658 SEP-bad, 0 D1 kills, 0 P kills**.
- **Verdict: REPLAY AGREES** (0 faults).

## What this means, and its limits

- **Three implementations now agree on P1.** These are the producer, Long Table's blind checker (`--all`, every graph) and the audit's replay (870 graphs, field by field), on the same file, together with the Studio's content-digest replay (T2/J4).
- **The result stands as reported**, on these 25,381 order-25 graphs only:
  - D1 kills 0, P kills 0;
  - 658 SEP-bad states, all at depth 1;
  - no unresolved vertices.

  It is evidence for nothing beyond them. D1 for all graphs would imply the Four Colour Theorem.
- **E1 (small evidence gap, not a fault).** `out/run.log` is listed in `wp20-j3/SHA256SUMS` but is **not in the repository**, probably because `*.log` is gitignored. So the agreed pre-run `shasum` line for the P1 file inside the run is not on record.
  - The verdict does not depend on it. The replay checks the file's content, and J4 showed that this content's digest equals the Studio's independent replay.
  - **Please force-add the log** (`git add -f`) so the record is complete.
- **Cost.** 1.3 CPU-hours (39 minutes on 2 workers). That is within the corrected estimate (1.7 CPU-hours) and above the plan's original wrong estimate ("well under 1"), as disclosed beforehand.

— Independent audit
