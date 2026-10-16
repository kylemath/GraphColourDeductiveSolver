# Round 12: H-AV, pair averaging between adjacent bigs (16 Oct 2026) [exploratory; exact LP-duality argument, no new reducibility]

**Hypothesis** (pre-registered by Long Table, 13:47Z). A pair-averaging row charge(u) + charge(v) <= 2t on adjacent
bigs, with v's arrangement consistent with u's 2-ball, takes t* below 3/11. **Kill:** t* stays >= 3/11.

## Test (`pairs.py`, `certpair.py`)

A wlp3 certificate is a nonnegative combination of sender rows and single-receiver rows.
- Suppose its receivers can be split into adjacent, consistent pairs (A at u, B at a link big v of u), with weights
  that add up to the dual weights.
- Then the same combination, written with pair rows (row A + row B), is a certificate for the pair-averaging model.
- So that model cannot go below the certificate's t.

**Consistency.** v's arrangement must agree with every letter that u's arrangement fixes:
- v's link: u, w_i+1, s_i, the p slots (free), s_i-1, w_i-1;
- v's s word: w_i+2; then s_i+1 if w_i+1 = 5, else free; then free letters; then s_i-2 if w_i-1 = 5, else free;
  then w_i-2.

## Result

| certificate | t | receivers | fitting pairs | pair certificate |
|---|---|---|---|---|
| Studio round 11 (`out/wlp3_j28_11.txt`) | 3/11 | 5756575/6565666, 5765756/5566666 | each fits next to a copy of itself | yes |
| Studio round 10 | 3/11 | 5675675/6566566, 5765676/5566556 | all four combinations | yes |
| explore oracle (`wlp3_hr1_or1.txt`) | 3/11 | 5676575/6556666, 5765756/5556666 | self-pairs | yes |
| Studio round 9 | 3/11 | 5 receivers | 3 pairs | no (some receivers have no partner in the certificate) |
| explore baseline | 33/119 | 5 receivers | 2 pairs | no |

**Verdict: H-AV dies.**
- The current 3/11 certificate is also a certificate for pair averaging, so pair rows cannot take t* below 3/11 with
  the current patterns.
- This holds exactly for the pair-row model. It does not settle rule class (b), transfers that depend on both
  2-balls: in the round-11 self-pair, u sees v at link position 1 and v sees u at position 5, which are not symmetric,
  so the edge is oriented and a transfer along it is not forced to 0.

## What a larger family would need instead

The plateau is a family. Studio's rounds 9-11 each killed the certificate pair (4-5 D per round), and a new pair
appeared at the same 3/11.
- In the round-11 pair, every five is **shared**: adjacent to u and to a link 7 of u. The binding senders are
  56677 / 66677 / 56776, fives with two 7-neighbours.
- So the obstruction is 7-5-7 triangles, the way the 2/7 floor was lone fives.

The analogue of the lone-five attack:
1. **Count the family.** A `lone.py`-style sep3 query with weight on the shared-five rooted words gives the d = 7
   arrangements that carry more shared-five load than 1 + t allows, together with the counting bound behind 3/11.
2. **Edge-centred configurations.** Two adjacent 7s u, v with their common fives and those fives' neighbours, both
   7s at exact degree. Like ufree's receiver-free configurations, one D verdict kills every arrangement that contains
   the window. They are built with gen.py's builder (a 7-5-7 strip around the link) and can be expressed as f7_
   windows once they are D.
3. **Only after that,** if the family survives at ring <= 16: an LP with 7 <-> 7 transfer variables. That needs the
   joint (u, v) arrangement DP, which sep3 does not have.

# Round 19: H-B0, can a joint (u, v) LP beat the single-receiver bound? (16 Oct 2026) [exploratory, no new dfast]

**Test** (`b0.py`, `bridge.py`). For every fitting pair (B at a link big v of A, as `pairs.py`):
- One patch is built from A at u. B supplies v's p slots and v's ring-3 letters. Unknown letters are 6 fillers and
  never sit inside a configuration.
- At u and at v, every S of the centre's fives: B-fixed and receiver-centred configurations, with defect_check2's
  ring repair.
- Each configuration is looked up by `la.ckey` in `bridge.pkl`: 10,757 existing D/C verdicts with dfast lines.
- Kill classes: *single* (inside the centre's own arrangement) and *joint* (needs letters of both).
- Positive control: the single kills on Studio's round-11 receivers are exactly the f7_ windows Studio later found D
  (f7_..55756_..6656., f7_..65756_..5656., ...).

**Certificates** (`cert_b0.txt`): Studio rounds 9-12 and the explore oracle/baseline. 23 fitting pairs.
- 10 pairs built: **0 joint kills**. Every kill is single, and these certificates' receivers are now forbidden on
  their own by later verdicts, so they are stale.
- 13 pairs could not be built. Layered cannot close a ring-3 vertex of degree 5 with three inner neighbours. These
  are not shown inconsistent.
- **Why joint kills are structurally rare:** a configuration centred at u over u's fives lives inside u's 2-ball
  (A's letters), and one at v inside v's (B's letters). Only a pinched-ring repair can mix the two. Configurations
  centred at u or v cannot be the lever; the round-18 kills sat at other 7s of the patch.

**Hard rows** (`hard_b0.txt`). For the 49 HARD28-like rows, which rows of the LP's tight set fit at each link 7/8?
The tight set is the 617 d = 7 rows plus Studio's 1,519 d = 8 tight rows.

| rows | a link big with no tight partner | a link big whose tight partners are all forbidden | free tight partners at every link big |
|---|---|---|---|
| all 49 | 41 | 2 | 6 |
| the 15 HARD28 | 12 | 1 | 2 |

- For 41 of the 49 rows, every arrangement that can sit at some big neighbour v is slack at t* (none is tight).
- A transfer along the edge u-v would lower u's tight row without making v bind. This is evidence for a
  neighbour-aware rule (transfer variables between adjacent bigs). It is not evidence for pair infeasibility.
- Caveat: "tight" depends on the LP's chosen optimum (the LP is degenerate). The tight set is a small sample of all
  arrangements.

**Verdict: H-B0 dies as pre-registered.** No certificate has every fitting pair killed by a joint configuration (0
joint kills in the 10 built pairs). The single kills only say the stale receivers are forbidden on their own. The
neighbour-slack count above is the positive side for option B, through transfer variables rather than pair
infeasibility.
