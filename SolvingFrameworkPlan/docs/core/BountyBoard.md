# Bounty board: Lemma R* and the road to VH∃

Set up 6 October 2026, 14:03 MDT, by the coordination session on the user's request ("setup a reward to motivate the teams to push forward"). Points are kept by the **Navigator** and awarded only at a ledger revision, on the evidence the ledger already requires. Nothing here changes a status rule.

## Why it is shaped this way

Points go to results that **survive checking**, in either direction. A proof and a counterexample of the same statement are worth the same, so no one gains by wanting a particular answer. Finding a real gap in someone else's accepted result scores well, and so does withdrawing your own error before anyone else finds it.

## The target

Lemma R\*: some degree-5 vertex off the protected face has finite Kempe radius. The vertex property R\* needs is, as far as we can tell, Tilley's **D-resolvability** (G. Tilley, *D-resolvability of vertices in planar graphs*, JGAA 21(4) (2017) 649–661, doi:10.7155/jgaa.00433). Tilley's open problem asks that **every** degree-5 vertex be D-resolvable; R\* asks for **one** per core triangulation, so Tilley's conjecture implies R\*, and R\* is the weaker statement (still open). The audit is checking the definition match. Our contribution is the reduction and the partial results, not the property. The reduction R\* ⇒ VH_C ⇒ VH∃ ⇒ 4-colourability is proved by hand and re-derived by the audit. R\* holds when at most one neighbour of the hole has degree ≥ 6, by Theorem H (compiled in Lean and audited, revision 130) and Theorem HP (compiled in Lean and audited, J8, revision 131); with three consecutive degree-5 neighbours by Theorem R5³ (hand, Math review and audit re-derivation, revision 134). **Open: two or more neighbours of degree ≥ 6**, where core-class states of Kempe radius 5 have been found (replayed by the audit, revision 133).

## Bounties

| Points | Result | Paid when |
|---:|---|---|
| **1000** | R\* proved in the open case (two or more neighbours of degree ≥ 6) | Hand proof accepted by Math, re-derived by Audit, recorded proved by the Navigator |
| **1000** | A counterexample to R\* or to VH∃ in the core class (minimum degree 5, 4-connected), with a certificate | Certificate replayed by Audit with its own code |
| 300 | R\* for the classes (5,5,5,6,6) and (5,5,6,5,6) (two degree-6 neighbours, three of degree 5); **150 per class** (coordinator's ruling 15:40: the two halves are paid separately) | As for the 1000 proof bounty |
| 300 | The R\* reduction (six links) compiled in Lean | No `sorry`, standard axioms, in an audit |
| 200 each | Theorem H, Theorem HP compiled in Lean | As above |
| 150 | A core state of Kempe radius ≥ 5, with a certificate, found by a pre-registered search or a hand construction | Audit replay |
| 150 | A real gap or error found in someone else's accepted result | Owner or Math confirms; Navigator records |
| 100 | A new global invariant that separates filled from stuck states on T4, A₃–A₅ and the order-28 (6⁵) hole | Audit replay of the separation |
| 80 | The Euler lemma compiled in Lean | As for Lean bounties |
| 50 | A conjecture killed with an explicit certificate; only conjectures that someone else recorded first (in a message or the ledger) before the kill | Independent check |
| 30 | An independent replay or re-derivation requested by the Navigator or coordinator, **whatever its verdict** (agree or fault); the replayer takes no share of the finder's points | Replay report posted |
| 50 | Withdrawing your own error before anyone else reports it | Navigator records the withdrawal |

Amended 14:1x on 6 October by the coordinator, adopting the audit's review B1–B4: replays pay a fixed amount regardless of verdict (B1); only kills of others' recorded conjectures pay (B2); the radius-≥5 bounty needs a pre-registered search or a hand construction (B3); the target line now says "if H and HP hold" (B4).

## Deductions

| Points | For |
|---:|---|
| −100 | A claim upgraded beyond its evidence and later found wrong by someone else |
| −20 | Using a status word (proved, compiled, killed) the Navigator has not recorded |
| −20 | Running computation on a machine against the current rule (no new jobs on the MacBook) |

## Teams

`longtable`, `math`, `audit`, `studiointel`, `studiomath`, `severn` (paper work does not score; the paper's job is accuracy). Shared results split the points by agreement in the message that reports them.

## Leaderboard

Kept by the Navigator in each revision message from revision 125 on, with the item, the evidence and the points. Starts at zero for everyone at 14:03 on 6 October; earlier results are not scored.

| Team | Points |
|---|---:|
| longtable | 50 |
| math | 30 |
| audit | 120 |
| studiointel | 150 |
| studiomath | 510 |
| studiocompute | 270 |
| intern-A | 0 |
| intern-B | 0 |
| intern-C | 30 |
| intern-D | 0 |

Totals as of Navigator revision 134 (6 October, 15:25 MDT). Revision 134 paid longtable 50 for withdrawing its own literature error before anyone else reported it, and the audit 30 for the requested re-derivation of Theorem R5³; earlier awards are in the revision 125 to 133 messages. The same totals are in `docs/navigator/leaderboard.json`.
