# Revision 127: P1 reproduced exactly on the Studio; Theorem HP audited by hand; two-degree-6 case opened; leaderboard

- **From:** Proof Navigator — main session
- **To:** Long Table; Math; Independent audit; Studio Intel; Studio Math; SquireTeamSevern; coordination session
- **Sent:** 2026-10-06 14:18 MDT
- **Replies to:** branch `studio-wp21` (`71bf0e1`, `e090ee1`); audit 14:30 and 14:45; Math 14:10 (×2) and 14:13; Studio Intel 14:10, 14:18 and 14:26; Studio Math 14:06; intern files in `docs/working/interns-2026-10-06/`. The senders' clocks run ahead of the machine clock, which read 14:18.
- **Asks for:** Math, the WP20 P1 review; audit, re-derive Theorem H next and report J3; Studio Math, the strategy export (Math 14:13)

## WP20 P1: reproduced exactly; still not "passed"

- **T2:** the Studio's replay is complete, 254 of 254 shards, 137,386 CPU-s.
- **J4:** the transferred first-Mac file (`e68c44a3…`) compared **IDENTICAL** to the replay. I checked that the two `DIGEST.json` files on the branch are equal: overall `39f1396e…4723d7`.
- **Gate (c), reproducibility: met.**
- **Still open:** (a) the audit's own replay J3, running since 14:14:44; and (b) Math's review.
- Severn: §6 may now add "reproduced exactly on a second machine (digest)".

## Theorems

- **Theorem HP:** **re-derived by hand by the audit** (14:30). It now has four independent hand reviews: a Math worker, Studio Math, intern C and the audit.
  - Status: proved by hand, **audited** (hand re-derivation), **not compiled**.
  - Scope: (5,5,5,5,\*) only.
  - Still outstanding: its computed claims, and the face list for its order-22 example.
- **Theorem H:** reviewed by a Math worker, Studio Math and intern C. **Not yet audited.**
- **Euler lemma in Lean** (Studio Math, `7178c2d`): built, not in an audit, so not yet compiled. The audit's reading: the statement is right for minimum degree 5, but not the relative form that link L5 needs.

## R\* with two degree-6 neighbours (new node `structural-rstar-two-six`, exploring)

- **Math's obstruction** [hand, worker, unreviewed]: HP's moves cycle on a 20-state set (adjacent class) and on a closed 28-state set (non-adjacent class).
- **Intern B's AB-unavailability lemma:** correct, by Math's hand check.
- **Intern A:** partly corrected by Math.
- **Plan:** certify the joint game's depth-7 and depth-14 strategies with independent code, plus the audit's soundness review. Success would be labelled [computed + hand].
- **Studio Intel data:** AB kills E2 in 628 of 628 records (exploratory).
- **Intern D's potential:** killed as a separator on three holes [computed, exploratory, Studio Intel; not replayed].

## Leaderboard (board as amended in `8dbcaf5`)

| Item | Evidence | Team | Points |
|---|---|---|---:|
| Requested hand re-derivation of Theorem HP (asked in Navigator revision 122); report posted | audit 14:30 message; node `structural-theorem-hp` | audit | 30 |
| Requested independent hand review of Theorems H and HP (one report; coordinator's role message) | `8ebcfd5`, `StudioMathReviewHPandH.md`; nodes H, HP | studiomath | 30 |
| Requested gap hunt in Theorem HP, two reports posted (verdict: no gap) | `intern-C.md`, `intern-C-cycle2.md` | intern-C | 30 |
| Requested check of intern B's argument (coordinator relay); verdict correct | Math 14:10 message; node `structural-rstar-two-six` | math | 30 |

**Not scored:**
- Studio T2/J4 replay: the Studio compute session is not a team on the board.
- The audit's Euler statement read: a reading, not a replay or re-derivation.
- Studio Intel's E2 and intern D tables: data, not a certified kill of a recorded conjecture.
- The Euler Lean build: not yet in an audit; it pays 80 when it is.
- Math's corrections of intern A: by an unreviewed worker, and intern A's claims were never accepted, so this is not the "error in an accepted result" bounty.

| Team | Running total |
|---|---:|
| longtable | 0 |
| math | 30 |
| audit | 30 |
| studiointel | 0 |
| studiomath | 30 |
| intern-A | 0 |
| intern-B | 0 |
| intern-C | 30 |
| intern-D | 0 |

The same totals are in `docs/core/BountyBoard.md`.

`planning.test.cjs` passes and `check-paths.cjs` reports 14 planned, 0 broken (run before this commit). No finite check is upgraded.
