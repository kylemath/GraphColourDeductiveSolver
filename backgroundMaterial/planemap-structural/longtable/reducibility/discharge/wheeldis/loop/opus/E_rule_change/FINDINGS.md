# E_rule_change — FINDINGS
Question: can a rule extension in (a+) (5->6, 6->big, 7->8+) or a two-step 5->6->big scheme unload the three 5s of the unique t*=7/27 binder (u=7, link 5675765, ring 6577575) away from u, without the charge piling up elsewhere; what is the new row inequality and the restricted-LP bound?
Guess: the 6s in the binder's link (two of them) touch at most 1-2 of the binding 5s, and each such 6 is adjacent to bigs only in a way that makes the 6 a receiver from several 5s; a 5->6->big relay helps this row but a nearby "6 surrounded by 5s" row rebinds near 1/4.
What would change the plan: if the relay drops this row's bound well below 7/27 AND a restricted LP with the relay columns gives t* clearly lower with a feasibility upper bound, the K>=2 attack should switch to rule-change instead of windows.

---
Tags: [E] = computed here (scipy/HiGHS LP, sep3 pattern check, no reducibility runs); [hand] = my argument; [I] = inferred.
Scripts: `hatlp.py` (rule H restricted LP; `noh` = baseline), logs `hatlp_*.log`, solutions `hatlp_*.json`, `bin/sep3` (compiled from W/sep3.cpp, unchanged).

## 1. The certificate as a patch [hand, from the j28_13 dual + wlp.py's R5/R6]

u = 7, link w0..w6 = 5 6 7 5 7 6 5, second ring s0..s6 = 6 5 7 7 5 7 5 (s_i common to w_i, w_i+1). Privates p1, p5 of the link 6s.

| vertex | deg | neighbours (cyclic) | role |
|---|---|---|---|
| w0 | 5 | u, w1=6, s0=6, s6=5, w6=5 | sender 55667, **lone five** (only big = u): pays u 1-t |
| w6 | 5 | u, w0=5, s6=5, s5=7, w5=6 | sender 55767, bigs u and s5; the rooted word 7\|5576 is the same from both, so u gets (1-t)/2 |
| w3 | 5 | u, w2=7, s2=7, s3=7, w4=7 | sender 77777, u gets (1-t)/5 |
| w1 | 6 | u, w2=7, s1=5, p1, s0=6, w0=5 | link 6; **p1 in {7,8,9} is forced**: p1=5 or 6 makes the 6-wheel R (wlp.py isR6) [E] |
| w5 | 6 | u, w6=5, s5=7, p5, s4=5, w4=7 | link 6; every p5 non-R; the LP's worst choice is p5=5 |
| s0 | 6 | w0, w1, p1 (big), two outer vertices, s6=5 | ring-2 6, not adjacent to u |
| s6 | 5 | w0, s0, x, s5, w6 | ring-2 five |

Sum: 1 + 1/2 + 1/5 = 1.7, so 1.7(1-t) <= 1+t, t >= 7/27.
- 6s adjacent to the senders: w0 has w1 and s0 (consecutive spokes); w6 has w5 only; w3 has none.
- Bigs beyond them: w1 -> u, w2 (7), p1 (>= 7, forced). s0 -> p1 (forced) plus two free outer vertices. w5 -> u, w4, s5, and p5 (free, 5 in the worst case).
- **Key fact:** p1 is the *hat* of w0's 66 spoke pair (w1, s0) (common neighbour of w1 and s0 other than w0), and R forces it big.
  So the lone five w0 always has a big vertex at distance 2, reached through two 6s, that is not u.

Why the other two fives cannot be helped by any 2-ball-type rule [hand]:
- w6 (55767): u and s5 can be made mirror images across the edge w6-w5 (reflection swapping u<->s5, w0<->s6, w4<->p5, fixing w5, w6; needs p5 = 7, which is non-R). Then every isomorphism-invariant rule pays u and s5 the same: (1-t)/2. Its only 6 (w5) is adjacent to u, w4, s5 and p5, and a 5->w5->w4 relay is matched by the inflow s4->w5->u (s4 = 5) in the same mirror. Self-pairing (GATE-K2 §5) holds here.
- w3 (77777): the D5-symmetric "flower" (w3 centre, five 7s each with link 5675765, a 6 shared by consecutive 7s, two private 5s per 7) is consistent with u's row (s1=5, s2=s3=7, s4=5 all match), so every rule pays 1/5 to each. w3 has no 6-neighbour, so no relay exists. [hand; flower non-R not checked beyond the wheels in the row]
- So only the lone five w0 can be relieved. Best case (w0 fully relieved): 0.7(1-t) <= 1+t, t >= 3/17 = 0.1765 for this row.

The older H-R1 failure (5->6->big through a *link* 6, matched by inflow from a second-ring 5) does not apply to the hat route:
- The relay w0 -> w1 -> w2 would be matched by s1 -> w1 -> u (s1 = 5). The reflection through w1, w3 (u<->w2) would make this exact, but it maps s0 <-> p1, i.e. 6 <-> big, so it is **not** available here. That route is still a wash in the LP's worst case [I].
- The hat route w0 -> p1 does not touch u at all. A big z receives hat charge only from a five s_j adjacent to two *consecutive* link 6s w_j, w_j+1 of z. u's link 5675765 has no two consecutive 6s, so **u takes no hat inflow**.

## 2. The extension: rule H (smallest one found) [hand]

**Rule H.** A lone five v (exactly one neighbour of degree >= 7) with two consecutive degree-6 spokes x, y whose hat z (the other common neighbour of x and y) has degree >= 7 sends h[w, k] to z. Here w is v's rooted link word and k the position of the pair. Physically this is a 5 -> {x, y} -> z relay, half through each 6, with nothing kept at the 6s. Its payment to its own big becomes y[w, F], where F is the set of its 66 pairs with a big hat.
- In (a+) terms: a sender 5 reads its 2-ball (link + hats), and it is a two-step 5->6->big rule whose 6-step is forced (each 6 forwards what it received across the opposite edge). It is not a one-step (a+) rule, because the receiver is at distance 2. As a one-step (a+) rule it is the pair "5 -> 6 (sender 2-ball)" plus "6 -> big (6's 2-ball: forward to the hat)" [hand].
- New variables: 48 (h and y[w, F]); new sender rows: one per (lone word, F).
- **This row** becomes y(7|5566, F={(w1,s0)}) + h(55667 @ hat) >= 1 - t on w0's sender side. u's row is unchanged, so: (1 - t - h) + (1-t)/2 + (1-t)/5 <= 1 + t, i.e. **t >= (0.7 - h)/2.7**. h is limited only by the hat's (p1's) own row.
- Where the charge lands: p1, a big adjacent to w1, s0 and s1 (s1 = 5, but s1 also has w2 as a big, so it is not lone). The hat receives h for each 66 pair of its link that has a lone five as its s. A link like 5675765 has none, so the binder-type 7s do not take hat load; the 7s that do are 6-rich and have slack [I, checked by the LP below].
- **Self-pairing:** rule H moves charge across a distance-2 pair (v, z), not across an edge between two 2-balls, and z is never the five's own receiver. The edge-reflection argument that froze 7->7 transfers (GATE-K2 §5) needs an isometry swapping the two ends. Here that would swap a 5 with a big, which is impossible. So rule H escapes the self-pairing obstruction for this row. It does **not** help w6 or w3, which stay self-paired [hand].

## 3. Coordinator's lead: the 16 open fillings (s1, s4 >= 6). This changes the verdict on rule H [E + hand]

The coordinator reports that fillings with s1 = 5 or s4 = 5 are killed (D, ring 13). The j28 dual row itself has s1 = s4 = 5, so it is one of the killed fillings.
- p1 is forced big **only because s1 = 5**. For s1 in {6,7,8,9}, every p1 in 5..9 gives a non-R 6-wheel at w1 [E, wlp.py isR6]. In the 16 open fillings the adversary therefore sets p1 <= 6.
- **Rule H does not void the certificate in the open fillings.** It voids it only in the already-killed ones. Its LP gain (below) is real for the j28 registry, but it overlaps the kill the coordinator already has.

**What does void it in the open fillings: rule T ("redirect across a 6 to the next big").** [hand]
- *Rule.* A five v has a big neighbour u and a 6-neighbour x adjacent to u (x consecutive with u in v's link). Let z be the other common neighbour of u and x. If z is big, v pays tau[w, side] to z instead of to u, routed through x.
  - The sender row becomes y[w, flags] + Σ_{big z} tau >= 1 - t.
  - The flags record which of the (at most 2 per big neighbour) z's are big. They are read from v's 2-ball: z is adjacent to x, so it is at distance 2 from v.
  - It is the same as a two-step 5 -> 6 -> big rule in which the 6 forwards across its edge to u. Equivalently, it is a u -> z big-big transfer gated on "a 6 x, with the five v on the other side of x".
- *In the binder* (link w0..w6 = 5675765, so w1 and w5 are 6):
  - w0 -> (w1) -> w2 = 7 and w6 -> (w5) -> w4 = 7. Both z's are big for every filling: w2 and w4 are fixed 7s.
  - Inflow to u by rule T comes only from a five sitting in an s-slot between a link 6 and a link big, i.e. s1 (between w1, w2) and s4 (between w4, w5). These are exactly the coordinator's s1/s4. They are >= 6 in the open fillings, so **u takes no T-inflow**.
  - The other s-slots next to the 6s are s0 (between w0 = 5 and w1) and s5 (between w5 and w6 = 5). Their neighbour across is a five, not a big, so they give no inflow.
  - The H-R1 / L2 self-pairing needs the reflection through w1 and w3 (u <-> w2), which maps w0 <-> s1, i.e. 5 <-> (>= 6). It fails in the open fillings, so **rule T escapes self-pairing there**. (At s1 = 5 it self-pairs; that is the coordinator's "R(5,5) cancels".)
- *This row under T*: (1 - t - tau0) + ((1 - t)/2 - tau6) + (1 - t)/5 <= 1 + t, i.e. **t >= (0.7 - tau0 - tau6)/2.7**.
  - tau0 = tau[55667 rooted 7|5566, side of the 6 w1]; tau6 = tau[55767, side of w5].
  - Any tau0 + tau6 > 0 voids the 7/27 certificate in all 16 open fillings [hand]. If w0 is fully relieved and w6's u-half too, the floor for the row is 3/17 = 0.176 (w3/77777 is untouched; see §1).
- *Where the charge lands*: w2 and w4. In w2's own frame, w0 sits in w2's s-slot between w1 (6) and u (7). So rule T loads a big z by its own "5 in an s-slot between a link 6 and a link big" pattern. Whether that rebinds near 1/4 is **not computed** [I]. It is the same kind of slot the kill uses, so the 16 open fillings' w2/w4 rows are the first to check.

**Exact spec for the Studio sep3x job (columns, reads, separation state)** [hand]:
1. **Columns.**
   - tau[r, side] for each non-R sender word, rooted at a big letter r = (B, a, b, c, e), with side in {a, e}, firing when that spoke is 6. Optional refinement: tau indexed also by deg z in {7, 8, 9}.
   - y split into y[r, f_a, f_e], with f = "z on that side is big".
2. **Sender rows**: y[r, f] + Σ_{sides with f = 1} tau[r, side] >= 1 - t, summed over big roots, for every flag vector.
3. **Receiver row of u, link 5s.**
   - The 5 at w_i uses y[r, f], with f_a = [w_{i+1} = 6 and w_{i+2} big] and f_e = [w_{i-1} = 6 and w_{i-2} big].
   - The separation state needs **one more link letter**: (w_{i-2}, w_{i-1}, s_{i-1}, w_i), 625 states × 25 choices. Alternatively, put the flag on the transition into w_{i+2}.
4. **Receiver row of u, T-inflow.**
   - Add tau whenever s_j = 5 with {w_j, w_{j+1}} = {6, big}. The five s_j's word is (w_big, w_6 = 6, p_j, ?, ?) rooted at w_big, side = w_6.
   - Its letters p_j, ? and ? are outside sep3's state, so use max over non-R completions. That is a per-transition constant on (w_j, s_j, w_{j+1}), so it is **already expressible in sep3's (wp, sp, wc) -> (sc, wn) transition**.
   - This is the "state letter at a non-five s position" the job is adding.
5. Rows d >= 16 / letter 9: same DP. tau into a letter-9 big is d-independent, so the Karp bound is unchanged in form.

## 4. Restricted LP for rule H (`hatlp.py`) [E]

- **Rows**: the 1,385 rows of `out/job28/tight_13.txt` (tight at 7/27), each maximised over the privates p_j of its link 6s (non-R 6-wheels) and the outer hats.
- **Pattern registry**: j28_13. 10 files of it are absent in this checkout (job28 r_3..r_8; d = 10 patterns only).
- **Baseline check** (`python3 hatlp.py noh`): t = 0.259259 = 7/27, with the same dual as j28_13 (55667, 55767, 77777, d = 7 5675765/6577575, p1 = 7, p5 = 5). The restricted row set reproduces the binder.
- **Rule H, rows above only**: **t >= 1/5** (0.200000; `hatlp_h_dp.log`, iteration 0).
  - New dual: 0.4·sender 55667 (F = ∅, hat small) + 0.2·sender 55767 + 0.4·receiver d = 7 link 5568586, s 5755756 (p's = 5, 5), i.e. 1.5(1-t) <= 1+t.
  - The old binder row is no longer binding.
- **Not converged, and the gain is not proven.**
  - The first round of DP separation (a pattern-free DP over (w, p, s), with candidates checked by sep3 'c') found 5 new allowed d = 7 rows and 11 new d = 8 rows violated at t = 1/5. So the true restricted optimum is **> 1/5**, by an unknown amount.
  - The d = 9 row maximisation (brute force over p's, 5^#6s) was too slow for the cap. I stopped the run there, after ~20 min of 1 core.
- **Bound status**: 1/5 is a lower bound on the row set used, and not even the restricted LP's value. There is **no feasibility upper bound**: feascheck/sep3x carry no p_j or hat state, so no exhaustive separation exists for rule H. **No gain is claimed.**
- In any case (§3), rule H's relief at this binder exists only when s1 = 5, which the coordinator's kill already removes.

## 5. Verdict

1. The patch is the one in §1. The 6s next to the senders are w1, s0 (for w0) and w5 (for w6); 77777 has none. Beyond them: w2 = 7, p1, w4 = 7, s5 = 7, and p5.
2. Two extensions void the row:
   - Rule H (the hat over a 66 spoke pair) works only when s1 = 5, a filling the coordinator already kills.
   - **Rule T** (a five redirects across a 6 to the next link big, here w0 -> w1 -> w2 and w6 -> w5 -> w4) voids 1.7(1-t) <= 1+t in all 16 open fillings. It gives t >= (0.7 - tau0 - tau6)/2.7 for this row, with no inflow because s1, s4 >= 6, and it escapes self-pairing because the u <-> w2 reflection maps w0 <-> s1.
   - The 77777 share (1-t)/5 cannot be moved by any rule (D5 flower). The row floor under any rule is 3/17.
3. The global LP was run for H only: >= 1/5 on a partial row set, not converged, with no upper bound. Rule T is not run; its spec is in §3 for the sep3x job. Where T's load lands (w2/w4 rows: "5 in an s-slot between a 6 and a big") is the open risk [I].
