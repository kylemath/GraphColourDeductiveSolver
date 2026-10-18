# Opus team on the remaining gap (18 Oct 2026, from 08:35Z) [exploratory, engine level]

Kyle (08:34Z): "assign an opus agent team to attack the remaining gap from all angles and make a run for the link".
Log in EXPLORE-LOG.md style, newest first. This file and `opus/*/` are the team's; COORDINATOR-STATE.md is not edited here.

## What the gap and the link are (my reading, 08:45Z)

- **The gap.** K <= 1 meets the claim rule. For K >= 2 (degree-5 senders with two or more big neighbours) the
  discharging LP has t* = 7/27 > 0 exactly on the full registry; charge-sharing (L2) gave no gain. The binders are
  d = 7 receiver rows whose windows at ring <= 16 are neither D nor C. H7 (README §7.1) shows the deeper reason: the
  defect D3 has net charge +1 and contains no configuration of the programme's R_opt, so **no local rule of any kind
  closes against R_opt**. The gap is the reducible set, not the rule class.
- **The link.** The step that would join the K <= 1 result to a full proof: a reducible set and rule class for which
  the K >= 2 LP reaches t* <= 0. Nothing in the state file names "link" as a specific step; the nearest is Job 26
  ("the last link from the LP to the Lean chain"), which is a soundness bridge, not the gap.

## Round O1 (08:50Z-): four angles in parallel

Pre-registered before any probe ran.

| angle | question | guess | plan-changer |
|---|---|---|---|
| A, RSST in the defects | Does each H7/K4/Job 28 defect (D1-D3, E1, E2, K4 survivors) contain one of RSST's 633 configurations? | Yes for all: RSST's theorem forces a configuration near any positive vertex of a locally 6-connected patch | Yes: the H7 obstruction is an artefact of R, and R + RSST is the candidate link. No: a patch error, or a gap in applying RSST locally |
| B, RSST forbids LP rows | How many free tight rows (7/27 binders, HARD28-like 49) are forbidden by an RSST configuration inside the row's fixed patch? | Few: a d = 7 row fixes little beyond u's link and second ring, and most RSST configurations need exact degrees further out | Many: rerun the LP with RSST patterns (lower bound plus a feasibility upper bound) |
| C, kc at ring 17-20 | Do the binders' untested windows at ring 17-20 turn D now that kc makes ring 18-19 a matter of minutes? | A minority (10-20%) turn D; ring 17 was 0 of 6 | A binder dies: the ring <= 16 supply limit in GATE-K2 §3-4 no longer binds |
| D, RSST rules vs the LP's rule class | Do RSST's 32 rules lie in a rule class the LP optimises over? If so, R + RSST makes the LP feasible by RSST's theorem | Mostly yes (class (a), sender 2-ball), with gaps at ">= d" degree letters and RSST's degree >= 12 hand argument | Yes with small gaps: the link is concrete and costable |

### O1 results so far

- **D (09:00Z): RSST's rules sit outside every LP rule class** (`D_rsst_rules/FINDINGS.md`) [cited, from Gonthier's
  fourcolor `theories/proof/discharge.v:73-140`]. The 32 rules are 38 parts, each moving 1/10 LP unit from a sender of
  degree 5..8 to a receiver >= 6, reading the sender's 2-ball over {5,6,7,8,9+}. Only rule 2 fits (a)/(c) whole; 6-senders,
  6-receivers and 7->8+ transfers fit nowhere. So RSST's theorem does not make the present LP feasible once RSST's
  configurations are added. The guaranteed hybrid is Gonthier's proof re-encoded; mixing "own rules for K <= 1, RSST's
  for the rest" voids both certificates (RSST's 5s pay their 6s). Gonthier's discharging covers degree >= 12 by a
  computed cap, not by hand. Guess check: "mostly class (a)" was wrong.
- **A (09:05Z): every H7 defect contains RSST configurations, D-reducible ones among them** (`A_rsst_defects/FINDINGS.md`)
  [E]. D1 25 hits (11 D), D2 21 (6 D), D3 15 (7 D; #110 at ring 10, four 5s and two 7s, wholly inside the cluster), E1 20
  (11 D), E2 21 (11 D). All 50 D hits re-extracted and D by dfast; all 59 C hits are cfast C-candidates (|X| <= 4).
  453 of 453 sampled K = 3 / K = 4 defect candidates contain an RSST D configuration (rings 8-11). Controls: icosahedron
  hits only the diamond; pure 6-sea none. Reading [I]: H7's "no local rule closes against R_opt" is a fact about R_opt's
  shape (wheels and u-centred configurations), not about reducibility. Adding RSST's 249 D configurations (already
  Lean-checked in `dcheck/`) to R removes every known defect. It does not by itself close the LP: the rules must see
  these configurations within radius 2 of a 5. Guess check: right.
- **B (09:25Z): RSST's 633 as receiver patterns leave t* = 7/27 exactly** (`B_rsst_rows/FINDINGS.md`) [E]. A row
  fixes only the slots its 5-senders read. On the certificate row d = 7 5675765/6577575, 0 of 633 fit the fixed slots;
  only 128.136 (C, ring 11) fits, and only with s1 = 5 or s4 = 5, slots no sender reads, so the 16 fillings with
  s1, s4 >= 6 stay RSST-free. Elsewhere RSST does reach the receiver (74 configurations fit a d = 7 row's fixed slots,
  44 D, mostly fans around u) and forbids many non-binding rows: 920 of 1,385 tight_13 rows, 6 of 7 old binders, but
  only 2 of 49 HARD28-like. LP with 387 RSST patterns added: 7/27 with the same certificate; upper bound from the
  existing feascheck, since patterns only lower t*. Lever dropped. Guess check: "few" was right for the binders.
- **F (09:50Z): the 16 fillings with s1, s4 >= 6 stay RSST-free** (`F_free_slots/FINDINGS.md`) [E]. On the fixed
  patch none of the 16 contains an RSST configuration. With one more ring (the six privates of the non-5 link
  vertices at 5..9+) every filling gains hits, but each hit needs a private at 5 or 6, and all six privates at 7 is
  RSST-free for all 16. So RSST does not forbid the row even under a receiver-2-ball rule class. 6 u-centred kc windows
  at rings 13-14 without s1, s4: not D. The explore thread (round 34 part C) covers these fillings with u-centred
  windows; it killed the 9 fillings with a 5 at s1 or s4 by D at ring 13 on two engines.
- **E (10:05Z): a rule through the 6s voids the 7/27 certificate in all 16 open fillings, LP effect not computed**
  (`E_rule_change/FINDINGS.md`) [hand, plus a restricted LP]. **Rule T:** a five with big neighbour u and a
  6-neighbour x adjacent to u sends tau to z, the other common neighbour of u and x, when z is big (here
  w0 -> w1 -> w2 and w6 -> w5 -> w4; both z are 7s). Inflow into u comes only from a five in an s-slot between a link
  6 and a link big, i.e. s1 or s4, so none in the open fillings; the reflection swapping u and w2 maps w0 (a 5) to
  s1 (>= 6), so it escapes self-pairing. Row: t >= (0.7 - tau0 - tau6)/2.7. Open risk: the load lands on w2/w4 and
  may rebind near 1/4. Rule H (lone five sends past two consecutive 6s) acts only when s1 = 5, already killed;
  restricted LP with H: t >= 1/5, not converged, new binder d = 7 5568586/5755756, lower bound only, no gain claimed.
  Within 2-ball rules that send only to adjacent bigs, w6 and w3 self-pair, giving a 3/17 floor for this row.
- **Explore's review of rule T (via the coordinator, 09:22Z), accepted in part.** (a) T helps only if the five pays u
  less when z is big, so it is a sender-2-ball rule, not an additive tau. H7 floors that class at 1/21 against R_opt,
  but only via D3, and D3 contains RSST #110 (D, ring 10; angle A), so the floor does not hold against R_opt + RSST's
  D set. (b) A restricted LP over the 7/27-tight rows is under-separated exactly where T moves load: no restricted run
  is claimed.
- **G (10:30Z): rule T written as a sender-2-ball rule for a sep3x/wlp3x job** (`G_ruleT_lp/FINDINGS.md`) [E counts
  only, no LP]. Y[r, za, ze] replaces y[r] and T[r, za, ze, side] pays big z. Reading z as small/big costs 1,356 Y +
  504 T and 1,194 sender rows (today 942 y, 342 rows). The outflow at u uses the 7-letter window sep3x already
  resolves; the inflow at z is a per-transition weight on (w_j, s_j, w_{j+1}), sound for an upper bound. The exact bound
  needs 625 DP states (about 5x per build). Validation: T = 0 must reproduce 7/27 and the j28_13 dual. Note [I]: L2's
  u -> w2 transfer already reads (6, 5, s1) against (6, s1, 5), so once the s1 = 5 kill enters L2 (explore's proposed
  sep3x state extension), L2 alone may already make this move. Run that first; T is the fallback.
- **Cross-checks from the explore thread (via the coordinator, 09:41-09:44Z).** D3 contains RSST #110 on explore's
  own containment code (vertices 1, 2, 6, 7, 16, 17, all inside Y); kc D with ext 496 = RSST's count, so D on two
  engines with our dfast. H7's 1/21 floor is now logged as R_opt-specific. D1, D2, E1, E2 rest on our engines only.
  Explore round 36: w2/w4 absorb at most T = 0.1506 at first order, so rule T's gain through this row floors near
  t = 0.155 (hand second-order argument; independent check H running). Job 30 (Studio): part A puts the s1/s4 = 5
  kill into L2 with non-five s-letters; part B (rule T) runs only if A holds 7/27. RSST-D (158 patterns) is in the
  LP and t* stays 7/27 exactly, matching angle B.
- **H (10:55Z): explore's rule-T floor t >= 11/71 = 0.1549 at (6,6) checked independently and holds**
  (`H_floor_check/FINDINGS.md`) [hand + frame.py]. It is a floor for the whole rule-T class, not first order, unless
  w2/w4 can pass charge on (L2 transfer) or one of four arrangements is killed. So Job 30's order is right: part A
  (L2 with the s1/s4 = 5 kill) is what can go below 0.155; rule T alone cannot.
- **C (10:00Z): no window inside R's fixed patch kills any of the 16 open fillings** (`C_kc_ring17/FINDINGS.md`,
  `fillings_opus.txt`) [E, kc; D windows also dfast]. 1,350 windows on 2 cores. Windows not centred on u (connected
  subsets of u, w0-w6, s0-s6 at exact degrees): with s1, s4 >= 6, 0 D of 1,131 at rings 6-16 (every subset at ring
  <= 14 run). The 9 D windows found (rings 11-12, both engines) all use a five at s1 or s4, i.e. the 9 fillings explore
  had already killed. R's 4 B-fixed windows at u (rings 11, 16, 17, 17) are all not D. 1,644 untested windows at
  rings 15-20 listed in `untested_r15_20.txt`. Reading [I]: killing the open fillings needs vertices outside R's
  patch, case-split by degree, which is what explore's round 37 did (w2's link, C at ring 13). Guess check: "10-20%
  of binder windows D at ring 17-20" was wrong (0 of 7 at ring 16-17).
- **H round 2 (10:15Z): after explore's round-37 kill, the provable rule-T floor through R drops to t >= 1/21**
  (`H_floor_check/FINDINGS2.md`) [hand + sep3 c-check]. w2/w4's own rows give no floor (c = 1/5 at link 7665675);
  five e now routes to s2 through e' = 6, and the chain through s2's best surviving frame (5765557 / 7575757, c2 =
  7/10) gives 1/21. A lower bound only; true floor between 1/21 and explore's first-order 0.122.
- **I (10:30Z): rule S, a 6-relay generalising T and H, gives e a sound unpaired route, but onto a 7/27-tight big**
  (`I_route_e/FINDINGS.md`). On frame 7665675, x4's T inflow through y can self-pair with e's, restoring 11/71 [hand];
  this conflicts with H round 2's 1/21 (which dropped x4's inflow) and is being reconciled. Rule H's route to the
  forced big b lands on tight rows (cap 0 at first order). Kill target: u at (6,6) + w2 frame + b's tight row.
