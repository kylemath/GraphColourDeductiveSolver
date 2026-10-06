# Revision 124: Studio teams added; H and HP have a second hand review; Tait lock criterion accepted; R* adversary search pre-registered

- **From:** Proof Navigator — main session
- **To:** Long Table; Math; Independent audit; SquireTeamSevern; Studio Math; Studio Intel
- **Sent:** 2026-10-06 14:04 MDT
- **Replies to:** Studio Math 14:05 and Studio Intel 14:05; Math 13:55; Long Table 13:56; audit 13:35 and 13:40 (all in `SolvingFrameworkPlan/messages/2026-10-06/`)
- **Asks for:** information; audit and Math, review Long Table's R\* Tait-angle page when convenient

## New teams

`START-HERE.md` §2 gains two rows:
- **Studio Intel** (`studiointel`) is the adversary-constructor for R\*.
- **Studio Math** (`studiomath`) does independent hand reviews and Lean.

A Studio Math review is a Math-team review, not an audit. A Studio Intel kill counts only after an independent check of its certificate.

## Status decisions

- **Theorems H and HP: no change in status word** (proved by hand). The wording now says "two independent Math-team hand reviews (a Math worker; Studio Math), not audited, not compiled". HP covers only (5,5,5,5,\*). HP's computed claims are still unchecked, and its order-22 example still needs a face list. A second hand review strengthens the record but does not replace the audit.
- **Tait lock criterion and its corollary:** new node `structural-tait-lock-criterion`, **proved [hand]**, on Math's own line-by-line review. Not audited. Severn may drop "unreviewed" for it.
- **R\* adversary search** (Studio Intel): new node, `unstarted`. I checked its `SHA256SUMS` and all six files are OK. Nothing has run. It is released by the coordinator for the Studio after T2, with a cap of 6,600 CPU-s.
- **Long Table's R\* Tait angle:** recorded as [hand, unreviewed]. It proves nothing about R\*.

## Also recorded

- The audit's claim check of the Six-Ring Trap page found seven findings, none fatal. They are for the page owner.
- The audit's P1 replay will use route A, a byte-identical file: the gzip is on branch `transfer-p1` (`2169b2b`). I did not decompress it. The coordinator reports SHA-256 `e68c44a3…793e`. The replay is queued after T2.
- WP20 is unchanged: produced and independently checked, not yet passed.
- The Navigator row of `START-HERE.md` §7 is updated to revision 124.

`planning.test.cjs` passes and `check-paths.cjs` reports 14 planned, 0 broken (run before this commit). No finite check is upgraded.
