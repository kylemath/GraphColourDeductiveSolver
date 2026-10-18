# G_ruleT_lp — FINDINGS
Question: in E's restricted LP framework (1,385 rows tight at 7/27, rows maximised over link-6 privates), what is t* with rule T (five -> across a link-6 to the next big z), which rows bind, and does the load moved onto w2/w4 rebind near 1/4?
Guess: T removes the 7/27 binder but the restricted optimum stays high (~0.24-0.25): the receiving 7s whose link has a 6 next to a 5 in an s-slot (the binder's own w2/w4 frame) carry ~1.7 already, and the 55767-type sender's u-half cannot all move; rebind near 1/4 likely.
What would change the plan: restricted t* well below 1/4 that survives at least one d=7/8 separation pass with T inflow included (then T is worth a full sep3x job); t* staying >= ~0.25 means rule T is not the lever.

---
**Task changed at ~09:25Z (coordinator):** do not run the restricted LP. Write rule T as a sender-2-ball rule spec for a Studio sep3x/wlp3x job.
Nothing was run except variable and row counts (`tcount.py`, `tcount_flag.py`). The 3-line guess above is therefore untested.
Tags: [E] = computed here (counts only), [hand] = my reading of sep3x.cpp / wlp3x.py, [I] = inferred.

## 1. Rule T as a sender-2-ball rule [hand]

**Notation.**
- v is a non-R five and u is a big neighbour (the root). v's link oriented from u is (B, a, b, c, e): a and e are the spokes next to u, as in wlp.py's root().
- If a = 6: z_a is the other common neighbour of u and a (not v). It is at distance 2 from v, so it lies inside v's 2-ball.
- If e = 6: z_e is defined the same way.
- In u's own arrangement, with v = w_i: a = w_{i+1}, z_a = w_{i+2}; e = w_{i-1}, z_e = w_{i-2}.

**Variables.** All are keyed up to the reflection (B,a,b,c,e; za,ze) ~ (B,e,c,b,a; ze,za), which also swaps side a and side e.
- Y[r, za, ze] >= 0: what v sends to u. It replaces wlp3's y[r].
  - za is in {5,...,9} if a = 6, and '-' otherwise. ze is the same for e.
- T[r, za, ze, side] >= 0: what v sends to z_side. It exists only when that spoke is 6 and z_side >= 7.
- Option F (full letters): **3,048 Y + 2,007 T** [E, tcount.py].
- Option B (z read only as small {5,6} or big {7,8,9+}): **1,356 Y + 444 T** [E, tcount_flag.py].
- Today's base: 942 rooted y.
- Recommendation: run B first. F matters only if the gain depends on z's exact degree. T's inflow at z depends on z's letter through the receiver row anyway.

**Sender rows.** For every non-R five-word, and every assignment of z letters to the (big root, 6-spoke) pairs it has:
- Σ_{big roots j} ( Y[r_j, za_j, ze_j] + Σ_{sides with z >= 7} T[r_j, za_j, ze_j, side] ) >= 1 - t.
- Admissible assignments are coupled through each 6-spoke at position k. Its wheel (5, x[k+1], zR, q, zL, x[k-1]) must be non-R6 for some q:
  - zL is root k-1's z_a;
  - zR is root k+1's z_e.
- Row counts [E]:
  - Option F: **19,626 sender rows** (base 342).
  - Option B: **1,194**.
  - These are LP rows, not DP rows, so either size is trivial for HiGHS.

**Self-check on the 7/27 binder (open fillings, s1, s4 >= 6)** [hand]:
- u's outflow uses Y[7|6655, za = w2 = 7] for w0 and Y[7|5576, ze = w4 = 7] for w6.
- u's inflow is zero. The only (big,6) / (6,big) link pairs are (w1,w2) and (w4,w5), and their s-slots s1 and s4 are not 5.
- So the row becomes t >= (0.7 - T0 - T6)/2.7, as in E's FINDINGS §3.

## 2. Receiver-row contributions (receiver R of letter U = min(d,9), arrangement w_i, s_i) [hand]

**(i) Outflow at R** (replaces y[root]). For each i with w_i = 5:
- add Y[r_i, za, ze], where r_i = (U, w_{i+1}, s_i, s_{i-1}, w_{i-1});
- za = w_{i+2} if w_{i+1} = 6, else '-';
- ze = w_{i-2} if w_{i-1} = 6, else '-'.

It reads the 7-letter window (w_{i-2}, w_{i-1}, s_{i-1}, w_i, s_i, w_{i+1}, w_{i+2}). **This is exactly the window sep3x already resolves for its transfer terms.** `buildRes()`/`RES[]` resolve position j once w_{j±2} and s_{j-1}, s_j are fixed, so the branch-and-bound needs no new state.

**(ii) Inflow at R** (R plays z). For each j with s_j = 5 and {w_j, w_{j+1}} = {big, 6}:
- Case w_j big, w_{j+1} = 6. The five s_j, rooted at w_j and oriented towards the 6, reads (w_j, 6, p, m, o).
  - p = p_{j+1} is the 6's private on s_j's side. In the 6's wheel (U, w_{j+2}, s_{j+1}, p, s_j, w_j), p sits next to s_j.
  - m and o are s_j's outer letters, with o adjacent to w_j.
  - Its za is R itself, so za = U.
  - Its ze is the letter z' after o in w_j's link if o = 6, else '-'. z' is never in R's arrangement.
- Add  max over (p, m, o, z')  of  T[(w_j, 6, p, m, o), za = U, ze, side a], subject to:
  - the five-word (w_j, 6, p, m, o) is non-R5;
  - p admits a non-R 6-wheel (U, w_{j+2}, s_{j+1}, p, 5, w_j).
- Case w_j = 6, w_{j+1} big: mirror image, with p = p_j and the 6-wheel (U, w_{j+1}, 5, p, s_{j-1}, w_{j-1}).
- **Conservative per-transition version** (recommended first): drop the 6-wheel side condition and maximise p freely over non-R five-words.
  - The term then depends only on (w_j, s_j, w_{j+1}), which is exactly sep3's transition (wc, sc, wn).
  - So it goes into W[st][c] for a non-5 wc. sep3 already adds W for every allowed transition (VA = -1 today). No state growth.
  - It over-counts the load, so it is sound for a feasibility upper bound. It is not tight.
- **Exact version:** resolve the term one step later, once s_{j+1} and w_{j+2} are fixed (j+2 is inside sep3x's resolution window too).
  - If two inflows share one 6 (s_j = s_{j+1} = 5, with w_j and w_{j+2} both big), they share p.
  - Taking the two maxima independently is still conservative. Exact needs p as a branched letter on those 6-positions only (<= 5 branches each).

**Bookkeeping notes.**
- Every T is counted once outgoing (in the sender row) and once incoming (at z). u's own outflow Y is already net of T, so u needs no "-T" term.
- With any T > 0, an arrangement with no link 5 can be loaded by inflow alone. sep3x's start-state rule already covers this: with HASX it searches every start letter. T needs the same flag.
- An admissible bound like XINMAX: per-transition inflow is already inside W, so the Bnd matrix covers it with no extra term.

## 3. DP state and growth vs today's sep3x [hand]

| piece | today (sep3x / wlp3x) | rule T |
|---|---|---|
| DFS (d <= DMAXP): state (w_{i-1}, s_{i-1}, w_i) | 125 states, 25 choices | same; outflow resolved by RES (as transfers); inflow per transition |
| Bnd (max-plus bound) | 125x125 dense, about 2e6 ops per k | (a) keep 125 states with W = max over (za, ze): admissible but weaker; or (b) exact: 625 states (w_{i-2}, w_{i-1}, s_{i-1}, w_i), 15,625 transitions, sparse product about 1e7 ops per k, Bnd memory about 3 MB per k (about 50 MB at d = 15) |
| start states (w_0 = 5) | 25 per d | (b) 125 (w_{-2} added) |
| d > DMAXP rows (letter-9 DP) and Karp bound | 125 states | 625 states for exact flags; Karp O(n·E), about 1e7 ops. Or 125 with max over z: conservative |
| pattern codes CO | unchanged | unchanged (patterns read only the 5s' 4 slots) |
| LP | 942 y + transfer columns, 342 sender rows | +414 (B) / +2,106 (F) Y columns, +444 / +2,007 T columns, 1,194 / 19,626 sender rows |

**Estimates and checks.**
- Growth estimate [I]: (b) costs about 5x per Bnd build, and the DFS node count should fall, since the bound is tighter than (a). (a) costs nothing extra per build, but may inflate nodes wherever the LP sets Y[r, flagged] far below Y[r, unflagged]. That is the binder's own case. So use (b) [I].
- Exactness check for the implementation: with every T fixed at 0 and Y[r, ·] = y[r], the job must reproduce 7/27 and the j28_13 dual.

## 4. Relation to sep3x's transfers (L2), worth checking before a new job [I]

- At the charge level, T is a gated u -> z big-big transfer. "v pays Y = y - T to u and T to z" gives the same vertex charges as "v pays y to u, and u passes T to z".
- sep3x's transfer type on the edge u -> w2 (v = w0) has side codes (c, at-u, at-z) = (w1 = 6, w0 = 5, s1).
  - The reverse direction reads (6, s1, 5). So for s1 >= 6 (the open fillings), L2 can already move charge u -> w2 with no self-pairing.
- The two index sets differ:
  - T keys on the five's word (s0, s6, w6) and on z's letter.
  - L2 keys on the far side (w3, w4, s2) and on s1.
  - Neither class contains the other.
- **Check:** did wlp3x (non-notx) reach 7/27 with the s1/s4 kills in its pattern set? If it did, the u -> w2 move was available and the LP declined it. That would be direct evidence that the w2/w4 rebind (the open risk) is real, and T would likely also stall near the same value.

## 5. Files

- `tcount.py`, `tcount_flag.py`: the counts above [E].
- `sep3t.cpp`, `bin/sep3t`: **unrun prototype, built before the task changed**, kept only as a starting point.
  - It is sep3 with flag-version (option B, outflow-only flags) weights W4[a][c][f], lazy flag resolution and exact leaf weights.
  - It has not been run or validated. Do not cite it.
- `bin/sep3`: a symlink to E's binary.
- No LP was run. **No t* value, and no bound of either kind, is claimed.**

**Erratum (18 Oct, 11:15Z).** tcount.py and tcount_flag.py added the side label after key() had reflected the word,
without swapping the side, so reflected roots got the wrong side (found by Studio, commit 78ed61e7, loop/studio/tc/
tdiff.py). Fixed with tkey(), which carries the physical side through the reflection. Corrected counts: T = 444
(small/big, equal to Studio's) and 2,007 (full letters); Y and sender rows unchanged. floor.py and I_route_e do not use
these scripts.
