# WP20 P1: independent audit replay plan

Independent audit, 6 October 2026, 08:35 MDT. **Written before any P1 attempt-2 output was read.** At this time only chunks 0–1 of attempt 2 exist on disk, and the audit has not opened them. This plan fixes how the audit will replay P1. Nothing in it changes the WP20 declaration (`WP20-D1-declaration.md`, SHA-256 `8758a9f8409f17b4ca755d7688ba9f1bc996d35e40d0c173b5f9e64a3ca62fef`).

## Independence

- The replay code is the audit's own, written from `WP20-D1-declaration.md` and `WP20-output-format.md` only.
- It imports and reads neither `d1_confirm.py` (producer, `bb350d3b…`) nor `d1_check.py` (Long Table's blind checker, `98c6bcf7…`).
- It has its own plantri parser, colouring enumerator, Kempe component code and canonical renaming.
- So this is a third implementation, beside the producer and Long Table's checker.

## Steps, in order

1. **Bindings.** Recompute the SHA-256 of the declaration, producer, checker and `wp20/input-m5-25.txt`. Check that the input is `92e482ed…` with 25,381 graphs. Check that every chunk file and the merged output carry the declaration, input and producer hashes.
2. **Merge integrity.** Chunks cover indices 0..25380 exactly once, with no gaps, overlaps or reordering. Each graph's `ascii` equals line i of the input. The merged file equals the concatenation, by the audit's own merge rather than `wp_merge.py`.
3. **Accounting.** Every graph has `status` complete. Every degree-5 vertex of every graph appears, recomputed from the input by the audit. All the identities in the format file hold, including `unfilled_total = states + no_legal_fan`, `d1_kills = sep_bad − depth["1"]` and `capped ⇔ p_capped > 0`. Any interrupted or capped vertex is listed as unresolved, never as a pass.
4. **Certificates.** Every witness is re-verified from scratch: each `sep_bad` (with its depth), each `d1_kills` and each `p_kills`. A P kill is re-verified by complete enumeration of the hole-fixed Kempe class, under the declared 200,000 cap.
5. **Full recount on flagged graphs.** For every graph with a SEP-bad state, a kill or an unresolved vertex, recompute every per-vertex count and compare exactly.
6. **Audit's own sample, fixed now.** Graph i is sampled when `int(sha256("AUDIT-WP20-P1-" + str(i)).hexdigest()[:8], 16) % 100 == 0`. That is about 1% of graphs, disjoint in rule from the declared `"WP20-"` sample. On each sampled graph, recompute every count and compare exactly.
7. **Declared sample.** Also recompute the declaration's 2% sample (`"WP20-"` rule), so that Long Table's checker and the audit cover the same graphs.

## Verdicts

- **Replay agrees:** every check above passes. The audit then reports the producer's counts as replayed on the stated graphs. A pass of D1 or P is "no counterexample among the order-25 graphs run", never more.
- **Fault:** any mismatch. The audit reports it with the graph, vertex and both values, and the phase result is not accepted until it is explained.

## Cost

Run after Long Table's own `d1_check.py --all` reports, at most 2 workers, so as not to compete with P1 or with WP21. Estimated cost is well under 1 CPU-hour, extrapolated from P1's rate of about 1.6 graphs per second on several workers.

## Also to report

- The chronology issues in `wp20/CHRONOLOGY.md`, as recorded, without judgement beyond the facts:
  - P1 attempt 1 started before Math's written go-ahead; the user's release is on file.
  - The four-minute SIGSTOP pause.
  - The overnight loss of attempt 1.
- Attempt 1 produced no output, so it has no data to replay.
