# Lone-five family (16 Oct 2026, rounds 7-8) [exploratory, engine level: dfast/cfast only, no Lean]

A five is **lone** at a receiver u when u is its only neighbour of degree >= 7. A rule that moves charge only from a
5 to adjacent bigs must send a lone five's whole charge to u. At t = 0, a receiver of degree d with more than d - 6
lone fives therefore needs a forbidden (reducible) pattern. This is the counting bound behind the LP floor 2/7: d = 10
with six lone fives gives 6(1 - t) <= 4 + t.

## Tools

- `lone.py`: sep3 (wlp3's receiver oracle, same patterns as wlp3) with weight 1 on lone rooted words. It returns the
  pattern-free arrangements with more than d - 6 lone fives.
- `ufree.py`: receiver-free configurations, S + N(S) - u.
  - u stays on the ring with its degree free, so one verdict holds at every d.
  - `mkpat` writes the window as an f<d>_ pattern for d = 7..17 (`u*.pat`).
  - These lines are patterns only: never add them to a B-fixed verdict registry.
- `bfix.py`: B-fixed sets of lone fives (u at exact degree).
- `iter.sh`: count, build, dfast, repeat. `run16.sh` is the ring-16 batch.

## Round 7: the family

| d | before (max lone fives) | after rings <= 15 | limit d - 6 |
|---|---|---|---|
| 9 | 4 | 4 (2 arrangements) | 3 |
| 10 | 6 | 6 (31) | 4 |
| 11 | 7 | 6 (13) | 5 |
| 12 | 8 | 7 (2) | 6 |
| 13 / 14 / 15 | 8 / 9 / 10 | 7 / 8 / 9 (clear) | 7 / 8 / 9 |
| 16-20 | floor(2d/3) | clear on the old patterns | d - 6 |

- **Receiver-free D configurations at rings 10-15: 62** (u1, u2). Ring 16: 3 of 20 (u10).
- **B-fixed D at ring <= 15: 24** (b1, b6, b8).
- The leftovers are mostly lone fives alternating with 6s (5656565656) or 556 blocks, with every s = 6.

## Round 8: H-L3 ("the leftovers cannot be killed from distance-2 data")

**Geometry (checked with gen.py's builder, `hl3.py` output).** For a lone five w_i, x = s_i has these neighbours:
- w_i and w_i+1;
- s_i-1, at distance 2 and fixed by the s letters;
- p, the second-ring neighbour of w_i+1 when w_i+1 is a 6 (gen name ('p', i+1, 1)). p is at distance 2 from u and is
  NOT fixed by the (w, s) letters;
- two third-ring vertices.

So the sounding board's point holds: the non-6 vertex that the 566666 wheel forces can be p, at distance 2.

**Probe.**
- Arrangements: A1 = d 10, link 5656556565, all s = 6 (six lone fives); A2 = link 5656565656, all s = 6 (five lone
  fives).
- For each lone five, each (x, p), and each S containing it with |S| <= 3: the B-fixed configuration plus p at exact
  degree 5, 6, 7 or 8.
- That gives 30 distinct configurations at ring <= 16 (`hl3.txt`, map `hl3.txt.map`).
- dfast found 7 D (`hl3.out`). cfast --search on the 4 misses at ring <= 15 found 2 C (`hl3c.cfast`).

| arrangement | p = 5 | p = 6 | p = 7 | p = 8 |
|---|---|---|---|---|
| A1 | D (S of 3 lone fives, r15-16), and C (S = {2}, r14, one working X) | D (S of 3, r16) | none at ring <= 16 (r15 not C) | none (only r16 built) |
| A2 | C (S = {0,2}, r15, \|X\| = 3, 59,828 working X) | none | none | no configuration at ring <= 16 |

**Verdict: H-L3 dies as worded.**
- In A1, the all-6 completion around x (p = 6) is killed by a 2-ball configuration. What is left there is a BIG p
  (7, 8) at distance 2.
- A2 is not killed for p = 6 or 7 at ring <= 16.
- Reading (inferred): the cases still standing have a big vertex two steps from the lone five, through a 6. That is
  exactly what a 5 -> 6 -> big rule could use.

## Round 9: ring 16, and H-R1 (a 5 -> 6 -> big rule)

**Ring 16.** Receiver-free: 3 D of 20 (`u10.out`). B-fixed: 6 D of 29 (`b10.out`, five at d = 11, one at d = 9).
- z_5565655_666666 contains A1's window, so A1 is dead.
- Recount (`lone10.txt`, every pattern so far):

| d | max lone fives | arrangements above d - 6 |
|---|---|---|
| 9 | 4 | 2 |
| 10 | 5 | 15 |
| 11 | 6 | 7 |
| 12 | 6 | 0 |

**LP** (`loop/lp/wlp3s.py`, every pattern in `pats_hr1.txt`):
- The baseline certificate gives t* >= 0.2773 (33/119), set by five d = 7 receivers (`wlp3_hr1_base.txt`). The lone
  family no longer binds.
- `hr1_oracle.py` classifies certificate receivers as routed, unrouted or plain. Forbidding the 4 routed ones as an
  optimistic stand-in for the rule (`hr1_or1.pat`) still leaves t >= 3/11 (`wlp3_hr1_or1.txt`).
- That bound rests on a d = 7 receiver with no lone five, 5765756/5556666.
- At every binder, the second-ring fives that feed u through a link 6 are at least as many as the lone fives the
  rule could relieve.

**Verdict.** H-R1 dies (inferred). `TWOSTEP.md` says what a faithful two-step LP would need.
