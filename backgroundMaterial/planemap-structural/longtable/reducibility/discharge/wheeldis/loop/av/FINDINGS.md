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
