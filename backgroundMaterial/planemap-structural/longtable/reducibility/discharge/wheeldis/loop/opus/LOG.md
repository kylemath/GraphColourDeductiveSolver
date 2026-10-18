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
