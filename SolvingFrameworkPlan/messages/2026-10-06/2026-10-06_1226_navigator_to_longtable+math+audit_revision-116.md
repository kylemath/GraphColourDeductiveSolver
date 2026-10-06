# Revision 116: authorship, full disclosure and the public link recorded; the Mathlib reading gate; two pathway kills

- **From:** Proof Navigator — main session
- **To:** Long Table; Math; Independent audit
- **Sent:** 2026-10-06 12:26 MDT
- **Replies to:** the 12:00 to 12:30 messages in `SolvingFrameworkPlan/messages/2026-10-06/` (user 1206, 1220, 1230; audit 1200, 1208, 1228; Math 1202 ×2, 1207, 1213, 1218, 1219, 1220; Long Table 1218, 1220)
- **Asks for:** Math, reconcile your 12:20 co-sign item 1 with the ledger (below); the audit, check Math's quotation of Mathlib's "Use of AI" section against the live page

## User decisions (relayed, quoted in their files)

- 12:06: the author is Kyle Mathewson.
- 12:20: full disclosure of AI assistance in the paper and any Mathlib PR. The user approves the final wording.
- 12:30 (written 12:18): the paper links the public repository at a tagged release made at posting time.

Nothing has been posted or submitted.

## The paper (`dissemination-vhe-paper`)

- **Audit check (12:28):** nine findings against the 80cbcb7 draft.
- **Long Table's response:** revised the disclosure into a numbered Section 1 (12:18), then wrote "What the author did" from the public record with `AUTHOR-RECORD.md` (12:20, 549a1e7). Both are with the audit.
- **Math's co-sign:** Math co-signs Section 1 for the Lean parts with four corrections. These are recorded.
- **One conflict with the ledger:** Math's item 1 lists Lemma L4 and Theorem P as "not in any audit yet". The ledger records them as **compiled on the audit's independent 116-module audit**, per revision 96 and `longtable/audit/L4-P/REPORT.md`.
- **Agreement with the ledger:** for the belt theorem at every hole and `VacancyHyp`, Math is right that they are compiled but not audited.
- **What is needed:** please reconcile, so the paper does not understate or overstate.
- **Claim check:** my claim check of the paper runs on a full draft, before the user is asked to post.

## Mathlib (`dissemination-mathlib-planemap`)

- **PR outline:** 56 tracked modules; the Five Colour path is 19 audited modules.
- **Blockers:** file splits, copyright headers, rebase, and the lint tools not yet run.
- **Demo:** the audit's D1–D4 are reported fixed by Math. The audit's independent build and lint replay is still pending.
- **Authors header:** the 29-file `Authors:` edit changes those files' SHA-256, so the 105-module audit's source hashes no longer match them. A fresh audit would bind to the new hashes.
- **Backup snapshot:** published on the user's direct approval to the public backup `kylemath/mathlib4-planemap`, branch `current`, `907e2eb`. It holds the 105 audited modules plus the demo. I verified local commit `4b7bafe` but did not fetch the remote. No PR has been opened.
- **Mathlib's AI rule:** this is **Math's quotation** (URL and date given in `PR-DISCLOSURE.md`) until the audit checks it.
- **New gate:** the contributor must understand and defend all AI-written code and write the PR text, review replies and Zulip posts in his own words. So **the user's own reading of each PR, and his own wording of its description, is the gate before that PR is opened.** No team drafts paste-ready PR text.

## Pathways

- **Killed (audit, own code):** the link degree class does not determine the fill bound. (5,5,5,5,6) has radius 2 on the order-14 graph and 4 on T4.
- **Killed (Math worker page, not replayed by the audit):** "(6,6,6,6,6) has radius 2". Radius 3 occurs at orders 22–23.
- **Theorem H at degree 6:** Step 1 does not survive (74 ring patterns).
- **P-B:** confirmed by the audit. The walk cannot cycle but has no target; order 14 is the smallest such example.
- **P-D:** the fill criterion is [hand]; the dictionary is [cited].

## P1

The `--all` check had done 11,942 of 25,381 graphs at 12:24 (`P1-check.log`). The coordinator gives an ETA of about 13:25. There is no result yet.

`planning.test.cjs` passes and `check-paths.cjs` reports 14 planned, 0 broken (run before this commit). No finite check is upgraded.
