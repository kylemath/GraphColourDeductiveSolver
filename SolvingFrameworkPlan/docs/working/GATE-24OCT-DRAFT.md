# 24 Oct gate (B8, discharging LP answer): DRAFT, 18 Oct 2026

Draft kept by the coordinator and revised as results land. Tags: **[L]** proved in Lean, **[E2]** two independent
engines agree, **[E]** one engine, **[I]** inferred. Evidence paths are relative to `longtable/reducibility/discharge/`.

## Answer in one paragraph

**K ≤ 1 (at most one big vertex in the configuration): closed.** Every discharging sender with one big
neighbour is in the reducible set R, so the forbidden-pattern LP has t* ≤ 0 on that case. This rests on Lean for 46
of the 47 large keys and two independent engines for the last one. Lean on that key finishes 22–25 Oct. All 2,855 smaller keys are Lean-checked (Job 24b, 34f14406). **K = 2: open.**
The best LP bound is t* = 2/13 ≈ 0.1538 exactly (need ≤ 0) [E2 upper and lower, the same configuration with conservation over all 1,424 types, registry 0125c46b, Opus 20ee527a + Studio c905eae0; the drop is from registry kills alone], with 16/101 ≈ 0.1584 [E2, closed] in the 6-centred relay class with the §14′ filter plus the §15 five→big-hat channel on registry 5fa0adb0, with 17/107 [E2 upper] on 880d25c6, with 65/406 [E2 upper] without the hat channel on 880d25c6 and exactly 4/25 [E2, upper = lower] without it on 5fa0adb0, with 8/47 [E2] without the filter, with 9/52 [E2] in the 6-relay class and 1/5 [E2] without a relay; down from 7/27, 1/4, 5/21, 11/47, 2/9 19/102 on 18 Oct, 23/134, 6/35 and 8/47 early 19 Oct once kills outside the old binding pattern
were allowed into the LP. What binds now is one family: a 7 whose link carries a 5-5-5 face (7665566, 7766556 and siblings). Under every rule shape tried on 19 Oct (stages 17–23: face pool, five→hat, oracle lemmas on the 7 and on the face fives, exact hat letters, face re-basing, reverse hat, sender registry filter) the 7 pays the whole face deficit and t* stays at 16/101. Neither the published 8,200-config set nor our engines to ring 16 kill the surviving rows (explore r51, fam51 e367efab).

## K ≤ 1 evidence

| Piece | Status | Where |
|---|---|---|
| K=1 sender keys at rings ≤ 16: 2,848 non-66666 keys all D; 5 others 66666-centred, covered by w66666 | [E] dfast; Lean for all 2,855 keys of the Studio-D set (Job 24b DONE 19 Oct ~01:18Z, 34f14406): D = true, 0 errors, 0 sorry, no duplicates | `studio14/`, `dcheck/occ24/results24b.txt` |
| 47 deferred keys at rings 17–19 | 46 [L] (3 early + studio14c 43/43, d627087b); k19 (ring 19, 48.4M classes) [E2]: dfast18 and kc agree on classes 48,427,561, ext 3,909,279, D, depth 4 | `studio14b/`, `wheeldis/loop/kc/` |
| kc validation (independent of dfast; no dfast, cfast or Lean source read) | 101 keys at rings 10–17 (82 not-D) + ring-18 D, all fields equal | `wheeldis/loop/kc/FINDINGS.md` |
| w66666 C-reducible | [E2] computation in Lean (C66666.lean, native_decide) + Coq/Gonthier independent; C-glue (C-reducible ⇒ colourable) not formalized in Lean | `c66666/`, `dcheck/C66666.lean` |
| Checker soundness, r ≤ 19 | [L] Jobs 19 and 23 | `dcheck/JOB19.md`, `dcheck/JOB23.md` |
| Per-key Occ modules (49) | [L] Job 24, hD closes as keys land | `dcheck/occ24/` |

**Scope caveat.** A 2-ball's ring can fold in large maps. Until Job 26 proves Kempe matching for a face-boundary-walk
ring, the K ≤ 1 claim covers appearances with a simple ring. Job 26 has proved FaceGlue (i) and Kempe matching for any face walk with distinct darts, so any number of pinches
and folds (FaceWalk.ringTNC/kempeMatching, 758a293b; sabotage test rejects). Only (iii) is left; its first half compiles (DCheckOccWalk.lean: the checker theorems hold for an occurrence whose ring is only a face walk). All 49 ring 17–19 keys now compile in walk form (488bf3f7). Dart-injectivity is now derived from the occurrence (41c2adbf; batch re-check running). Still to do: extracting the face walk
from an appearing 2-ball and wiring it into colorable_of_occ_dred. It has a 20 Nov kill, and the fallback is to state the simple-ring hypothesis in the paper. The Track 1 hand
argument (B2 + no separating triangle ⇒ injective, induced embedding) closes the gap on paper. Its Lean is Job 26 step 3a.

## K = 2 evidence

| Step | t* | Note |
|---|---|---|
| Job 28 rounds 1–12 | 5/17 → 13/49 | loop: find patch, kill with B-fixed D/C at ring ≤ 16 |
| Round 13 (+ win14, win8, win89) | 7/27 | binder d=7 5675765/6577575 |
| Job 29 L2: oriented big–big transfers, full registry (16,411 patterns) | 7/27 exactly [E2] | upper bound by an exhaustive separation of the x=0 solution; lower bound by row generation (feascheck.py). Charge-sharing adds nothing on this pattern set. Upper side independently checked (Opus J_lp_checker, own separation code, all d = 7..30 plus Karp tail; float primal, no exact-rational recheck yet) |
| 19 Oct: 0125c46b (argsA59), s22h configuration + consall (st24b) | **= 2/13 [E2, closed]** | Opus 20ee527a (upper FEASIBLE on 1,424 types; lower 36 rows) + Studio spec-only c905eae0: dcount 16,937 file-identical, senderR2 0/20,676, cons2 1,424×729, receivers d=7..17 exhaustive, Karp λ 0.5437, lower rebuilt exactly. Input diff vs s22h: only the k3x kills (+1,028 D / +180 C). Binders are face 7665566/6675676 (0.231) and two d10 rows (0.038 each). Stage 24 (D 9+ columns) gain 0. |
| 19 Oct: 5fa0adb0, L2, 6-centred relay + §14′ filter + §15 hat channel (s22h) | **= 16/101 [E2, closed]** | Opus fd6ea00e (upper; lower 114 rows) + Studio spec-only 6a5f89a0: senderR2 20,676, cons2 1,424×729, receivers d=7..17 exhaustive (SEP_EXACT6+SEP_RTAB), Karp λ 0.5573, lower rebuilt exactly. Binders are the face family (7665566, 7676556). Stages 19, 19b, 20 and 22 (lemma oracles, exact hats, face re-basing) are all null |
| 19 Oct: 5fa0adb0 (869 D / 658 C), L2, 6-centred relay + §14′ filter, no hat channel (s22f) | **= 4/25 [E2, closed]** | Opus 85efba87 (upper and lower 90 rows) + Studio spec-only 14feb53c: senders 7,074, cons2 1,424×729, receivers d=7..17 exhaustive, Karp λ 0.5267, lower rebuilt exactly. The d=8 binder is gone; the face family 7665566 binds. st18h is also upper-feasible at 17/107 on 5fa0adb0 |
| 19 Oct: 880d25c6, L2, 6-centred relay + §14′ filter + §15 hat channel (a five sends r[K] to a big hat at distance 2; key read identically from both ends) (st18h) | **≤ 17/107 [E2 upper]** | Opus (8f71209b, prose fix ee11d33e; lower 10/63 VALID, Studio-rebuilt) + Studio spec-only check 7c9320e4: key 0 mismatches over 9,139 diamonds (broken-key control 12,706), senderR2 20,676 rows, cons2 1,424×729, receivers d=7..17 exhaustive (SEP_EXACT6+SEP_RTAB), Karp λ 0.5561. No independent re-solve (Studio LP cannot express the class). Face family 7665566 / 7655667 still tight: the hat channel does not pay it |
| 19 Oct: 880d25c6 (841 D / 633 C), L2, 6-centred relay + §14′ filter (privates whose 3-ball contains a twoeng/conservative-RSST config are dropped; strict unknown rule) (s21f) | **≤ 65/406 [E2 upper]** | Opus (4e505eb6; lower 4/25 VALID) + Studio spec-only check 8fb18bd1: kill tables rebuilt (md5 match), check 4 3,072/7,500, senders 7,074, cons2 1,424×729, receivers d=7..17 exhaustive (SEP_EXACT6), Karp λ 0.5401. Stage 16 removed binder 7665566 from the dual. st16ap 6/37 also [E2 upper] (62bbfe0b) |
| 19 Oct: 8e008f86 (837 D / 623 C), L2, reduced 6-centred relay class (s20c) | **8/47 [E2]** | Opus + Studio §12 spec-only checker (38de2a15): senders 7,074, cons2 1,424×64, receivers d=7..15 exhaustive, Karp λ 0.5319, lower 41 rows exact. Binders 5566766/5666667 (R*-like) and d=10 6565656565/6655666666 |
| 19 Oct: 09d8ac38 (815 D / 612 C), L2, reduced 6-centred relay class (s19c) | **6/35 [E2]** | Opus + Studio §12 spec-only checker (50150249): receivers d=7..15 exhaustive, DP+Karp λ 11/21, lower 91 rows exact. Same registry: s10 relay 37/214 (one engine; 9/52 [E2] on b88ed8b7, 85d68733), main line 1/5 [E2] (s18, 113da331). Binder 5566766/5666667 R*-like to ring 16 (explore round 50) |
| 19 Oct: d43ba26a (510 D / 522 C), L2, reduced 6-centred relay class (s12r, RELAY_SPEC §12) | **23/134 [E2]** | Opus s12r50 + Studio spec-only checker (139b490e): senders 7,074, conservation 1,424×64, receivers d=7..15 exhaustive (arrangement-keyed), DP+Karp d=16..30, lower 57 rows exact. Stage 14 (7→7 inflow) left it unchanged; binder 5566766/5666667 needs radius-3 information |
| 19 Oct: d43ba26a, L2, 6-relay class (s17r) | **31/178 [E2]** | Opus + Studio spec-only checker (d667219b). Main line without relay on same registry: 1/5 [E2] |
| 18 Oct: 42c4c876 + r_5..r_8 (round 48 loaded), L2, Opus 6-relay class (5→6 pull, 6→big split, 994 conservation rows) | **19/102 [E2]** | Opus's LP (39f457ba) + Studio standalone checker written from RELAY_SPEC.md only (24c69bf8): upper incl. senders/conservation/receivers d=7..15/DP+Karp, lower 25 rows exact. Same registry without relay: 1/5 [E2] (32c82928). Relay receiver d=7 7665566/6675666 has no D/C at ring ≤ 14 (R*-like) |
| 18 Oct: 2/9 registry + rounds 46 kills + k45 +5 D (aee20e3b), no T, L2 | **1/5 [E2]** | Opus's LP (d065b212) + Studio feascheck, sendercheck (342/342), lowercheck (4 rows) and parsed-pattern load count 15,466 D (df4e94b5, 9aca31ac). Dual: receiver d=7 7765556/6575765 + senders 55757, 55767, 57667 — all killed in round 48 |
| 18 Oct: s7 minus 16 unsound k43 names + RSST containment patterns (k44, 377; 249 D + 333 conservative C of the 633 on our engines) + k45 own D, no T, L2 | **2/9 [E2]** | Opus's LP (f1a052b4) + Studio feascheck and 6-row lowercheck (d86b4a95); 16,587 patterns |
| 18 Oct: 5/21 registry + full k43 batch (382) + rsstD + Rule T (option B), L2 | **11/47 [E2]** | Opus's LP (bbd46d73) + Studio feascheckt d=7..15 and 24-row lowercheckt (8f45fca8). Top binder d=7 7565765/6855555 |
| 18 Oct: 1/4 registry + round-43 d=8 kill (RSST 7322.126 window, C ring 10) | **5/21 [E2]** | Opus's LP (9a914f8c) + Studio feascheck and 25-row rebuild (68294ae5). Dual over 25 rows, max weight 0.127 |
| 18 Oct: run A's 12 whole-arrangement kills + 2 ring-16 C + 10 k42map windows, L2 | **1/4 exactly [E2]** | Opus's LP engine + Studio feascheck and row rebuild (d64c8442). Binder moves to d=8 receiver 85556565/65866655 with senders 55688, 66668, 55858, 58668 |
| Explore rounds 24–32 | (restricted-LP values were under-separated; superseded) | ~30 binding rows forbidden; all windows second-engined |

What blocks K = 2 [E]: one row. The 7/27 certificate is a single receiver row R = d7 5675765/6577575, whose
fives are of sender types 55667, 55767 and 77777. With the sender rows forcing Σy ≥ 1 − t, row R gives
1.7(1 − t) ≤ 1 + t, so t ≥ 7/27 exactly (dual weights 10/27, 10/27, 5/27, 2/27; EXPLORE-LOG 08:50Z, 98d63411).
So only a kill of R itself, or of one of its three sender types, can move the LP. Transfers can't move it
either: R fits as its own 7-neighbour (self-pairing, rounds 12 and 20). R's three B-fixed windows (rings 16–17)
are not D [E2: kc and dfast18 agree on every count]. The certificate breaks only if all 25 (s1, s4) fillings of R die:
9 (a 5 at s1 or s4) are dead by ring-13 D on both engines, and 16 remain (loop/k34/fill.txt). A C verdict on R's ring-16/17
windows would cover all 16. kc -C (independent, matches cfast on 163 configs: 30/30 C, 133/133 not C) and Studio's
cfast agree that R16, R17a and R17b (rings 16–17) are neither D nor C. No D window lies inside R's own patch once s1, s4 ≥ 6 (Opus: exhaustive to ring 14, sampled to 16, 0 of 1,131), so any kill of the 16 must reach outside the patch, as explore's ring-13 C window at w2 does (C on two engines, round 37).

## Options for K = 2 after the gate

- **A. Ring 17–18 windows at the binders.** These were dead on cost (dfast18: 60–70 min per ring-18 D). kc does ring 18
  in about 5 minutes, so this is cheap now. Running overnight 18 Oct (explore round 34). Claims still need dfast18.
- **D. Defect-style search at R's 16 fillings: done 18 Oct (round 42), and it fails.** After one ring of growth with
  RSST plus two-engine kills forbidden, 160,552 of 250,000 cases survive, including every case with all privates ≥ 7. Together
  with no D/C on R's patch to ring 15 (round 41), R is not forbiddable by known configurations, so it must be paid for by rules (E).
- **E. Change the rule class** (Opus team, 18 Oct): send charge through 6s, which could void R's certificate
  without killing R. After explore's rounds 37–38 killed 1,140 frames at w2 (C on two engines), there is no positive hand bound left on what Rule T can buy (Opus, floor.py, rerun after a side-map fix; all kills used are conservative two-engine C). Studio's Job 30 part B is the deciding run. Also: RSST's 249 D configurations, already Lean-checked, remove every known K ≤ 4 defect but not R. H7's 1/21 floor is specific to its LP solution: its defect D3 contains RSST #110, D on two engines (explore 4b12ef00).
- **C. Narrow.** State K = 2 as open with the evidence above. Track 1's paper becomes "K ≤ 1 closed by 2-ball
  reducibility; K = 2 obstructed by self-pairing", and the long shot moves to 3-balls.

## Open items before 24 Oct (to fill in)

- [ ] run29d: 7/27 binders and the xcap=1000 cap test (Studio).
- [ ] Explore round 34+: ring 17–18 kc sweep on binders; any re-solved t*.
- [ ] k19 Lean (22–25 Oct): upgrade [E2] → [L] if it lands.
- [x] Job 26 status (18 Oct 09:05Z): multi-pinch proved; only (iii) left.
- [x] Recommendation line (draft, 19 Oct 12:45Z): **go with C (Narrow) for 24 Oct**: K ≤ 1 closed ([L] except k19 [E2]); K = 2 open at t* = 2/13 [E2], with the obstruction named as the 7 with a 5-5-5 face. After the gate, keep two lanes on K = 2: ring 17–18 reducibility on the surviving face receivers, and a new rule structure keyed on a 7's whole second neighbourhood (design first; it must show a negatively priced column on the current certificate before any solve). Kyle decides.
