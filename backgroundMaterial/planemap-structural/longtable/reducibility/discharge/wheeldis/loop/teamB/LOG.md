# Team B log (K = 2 gap) [exploratory, engine level unless tagged]

Workspace: `wheeldis/loop/teamB/`. Branch `claude/team-b-gap-gnqh97`. Sealed: nothing under `wheeldis/loop/opus/` is read.
Tags as in the explore log: [E] engine, [E2] two engines agree, [I] inferred, [L] Lean/Coq.

## Round B1 (18 Oct 2026, 18:15Z-): how do the published RSST discharging rules pay for R*?

**Pre-registered 18:15Z, before any run.**
- **Why.** The 7/27 certificate (EXPLORE-LOG round 34 amendment) says no rooted-word rule can pay for R*: its lone five
  w0 must send all of 1 - t to u. RSST's 32 rules (as encoded in Gonthier's Coq development, `discharge.v`, fetched
  from github.com/math-comp/fourcolor master, copied here) move charge 5 -> 6+, 6 -> 7+ and 7 -> 7+ along edges, with
  amounts read from the source's second neighbourhood. Together with RSST's 633 configurations they are a complete,
  Coq-checked unavoidability proof, so they must pay for R* somehow. How they do it tells us which rule channels the
  programme's LP is missing.
- **Probe.** My own Python port of Gonthier's part syntax and fit semantics (`b1_rsst/rsst.py`), evaluated on explicit
  layered discs (`b8b/rings.py`): u (7) with R*'s link 5675765 and s-word 6,s1,7,7,s4,7,5, the 16 open fillings
  (s1, s4) in {6,7,8,9+}^2, the six privates in {5..9+}, third-ring degrees free in {5..9+}. Score of u in RSST units:
  10(6 - 7) + inflow - outflow. Report, per filling: max and min score over completions (upper bound: each neighbour's
  inflow maximised independently), and which rules carry the charge.
- **Self-checks.** (i) Total score is conserved on a closed sphere (sum = 120). (ii) The symmetrized rule list has
  Gonthier's documented count behaviour (38 base items). (iii) On a few explicit discs, every link-edge transfer
  satisfies the Hubcap bounds of the `present7.v` leaf the disc falls into.
- **Bars.** max score <= 0 on all 16 fillings: RSST's rules pay for R* inside u's 3-ball, and the channels used are the
  next LP rule class. Positive max somewhere: RSST needs a reducible configuration there (present7 says Reducible),
  which our forbidden set must then contain.
- **Guess.** Max score <= 0 on every filling. w0 sends 2+2 to u and to the 6s w1, s0 (drule1), and w1 forwards to w2
  (drule2'), so u gets far less than "all of w0".

**Round B1 result (18:50Z): RSST's rules pay for R* completely. u's RSST score is exactly 0 in every one of the 250,000
cases (16 fillings x 5^6 privates, any third ring), except the 24,375 cases (erratum 18:30Z: first written as 34,375, an addition slip; `nonzero.txt` has 24,375) with (s1 = 6 and p2a = 5) or (s4 = 6 and
p4b = 5), where it is +1 or +2** (`b1_rsst/sweep.py`, `sweep.out`; 0 errors; min = max over the third ring in every case).
- Those positive cases are exactly the ones explore round 42 found dead to RSST configurations ("s1 = 6 forces
  p2a >= 6; s4 = 6 forces p4b >= 6"): 0 mismatches. Two independent pieces of code agree, which is also the best check
  of my port so far. Mirror self-check: 0 mismatches on 4,871 directed edges of 60 random spheres (`mirrorcheck.py`).
- **How the charge moves** (RSST units, u starts at -10): w0 -> u 4, w6 -> u 4 (each five sends 2 to every 6+
  neighbour, so also to the 6s w1, s0 / w5, s5, plus 1 + 1 by rules 2, 3), w3 -> u 2, the 6s forward w1 -> u 3 and
  w5 -> u 1, and **u passes 2 each to its 7-neighbours w2 and w4** (rules 8, 9: a 7 whose spokes read 5, 6-, 7+ sends
  one unit to that 7+). Net 14 - 4 - 10 = 0.
- Reading [I]: what pays for R* is (i) fives parking charge on neighbouring 6s, (ii) 6s forwarding to bigs, (iii) a 7
  forwarding to the next 7 along a 5,6 run. The programme's LP has none of (i) and only restricted forms of (ii)
  (Rule T) and (iii) (L2), which is why it sticks at 7/27 / 11/71.
- Against the bar and guess: max <= 0 wherever no RSST configuration sits; the guess was right in outcome, wrong in
  detail (w1 adds to u's load; the relief comes from u -> w2, w4).

**Inventory (worker, `rsst633_inventory.md`).** RSST labels 249 D / 384 C (all ring <= 14). Lean `agreesRSST` gives
all 633 a D / not-D verdict (one engine). Second engine D: only ~14. C engines: 382 of the 384 C configurations have
never been run on cfast or kc -C.

## Round B2 (18 Oct 2026, 19:00Z-): do our own engines confirm all 633 RSST configurations?

**Pre-registered 19:00Z, before any run.**
- **Why.** B1 says RSST's rules pay for R*; the route "RSST rules + RSST's 633 as the forbidden set" then needs only
  reducibility of the 633 on two of our engines (unavoidability is Gonthier's Coq theorem; a local Coq 8.18 build of
  fourcolor v1.3.1 is running as our own check of it).
- **Run.** C (384): cfast with RSST's own contract X fixed, then kc -C (-C2 where X puts two ring vertices in one
  component) with the same X; C counts when both give leftover 0. D (249): kc, in addition to Lean `agreesRSST`.
- **Bars.** All 633 on two engines: the forbidden side of the route is [E2]. Any configuration not confirmed is
  listed with its leftover.
- **Kill line.** A cfast/kc leftover mismatch on the same X, or a kc not-D on an RSST D configuration.
- **Guess.** All 633 confirm; a few C ones need the broad (-C2) mode because RSST's X has ring-ring contracts.

## Round B3 (18 Oct 2026, 19:15Z-): an own rule family with B1's missing channels (PFH), and its t*

**Pre-registered 19:15Z, before any code.** Coordinator's ask (18:09Z): turn B1's diagnosis into a rule family the
programme owns. Runs beside B2.
- **Rule family PFH** (charge 6 - deg; all amounts are LP variables, nothing copied from RSST's amounts):
  - y: a 5 sends to an adjacent big, keyed by its link word rooted at the target (as now);
  - **P (parking):** a 5 sends to an adjacent 6, keyed the same way;
  - **F (forwarding):** a 6 sends to an adjacent big, keyed by the 6's link word rooted at the target;
  - **H (hand-off):** a 7 or 8 sends to an adjacent big, keyed by its link word rooted at the target.
- **Rows.** 5: out >= 1 - t for every 5-wheel not in R. 6: in - out <= t for every 6-wheel not in R, with the outer
  letters of its fives free (max). Big of exact degree d = 7..15: in - out <= d - 6 + t over all arrangements of u's
  2-ball (link, s, and the privates of every 6/7/8 link vertex, so their wheels are exact and checked against R);
  d >= 16 by a max-mean-cycle bound on the same transfer graph.
- **R, in two steps.** v0: wheel-level R only (Job 17 D/C 5-/6-wheels, RBIG 7-/8-wheels, fans), to price the channels.
  v1: plus the registry's receiver patterns (Job 30 set) as forbidden arrangements.
- **Engine.** Own code (`b3_pfh/`), HiGHS via scipy, exact-DP separation; reported t* is a converged LP optimum
  (upper bound from a feasible solution checked by an independent exhaustive pass, lower bound from the row set).
- **Bars.** v1 below 7/27: an own-rules gain to report. v1 <= 0: K=2 closed by own rules (then two-engine checks).
  v0 above the old wheel-level 3/5: the channels add nothing at wheel level.
- **Guess.** v0 around 0.3-0.4 (channels help wheel-level a lot); v1 between 0.1 and 0.2, binding at a 6 or at w2-type
  7s that take hand-offs.

**B1 confirmation (18:34Z): [E2].** Studio scored R*'s 250,000 cases with its own code straight from discharge.v
(commits bc3e3470, a3b52bb7, loop/studio/rsst_rules/). Its result matches `nonzero.txt` exactly: 24,375 cases, an
empty set difference in both directions, and 0 charge mismatches. Erratum to my 18:30Z note to the coordinator: I
called case 66565565 +1, but it has p4b = 6, so it scores 0 and is not in `nonzero.txt`.

**Round B2 result (19:35Z): all 633 RSST configurations confirmed on two of our engines** (`b2_rsst633/results.tsv`,
worker run, ~33 min on 2 cores).
- Validation first: both engines reproduce studio15's recorded numbers for 2.126 and 122.126 exactly.
- D (249/249): kc D and cfast's D closure both give D; kc ext = cfast ext = RSST's header count on all 249.
- C (384/384): with RSST's own contract X, cfast `--fixed` leftover 0 (all X Gonthier-admissible) and kc `-x` leftover
  0 (307 conservative, 77 under -C2: two ring vertices in one X component). On every one, classes, ext and reached
  agree between the engines, and the unreached count equals RSST's header.
- Kill line not hit: 0 mismatches, 0 unconfirmed. Guess right ("all confirm, a few need -C2").
- With Lean `agreesRSST` (one engine, all 633 D / not-D) this is three engines for D and two for C.

**Coq check of unavoidability (b2_coq/).** Gonthier's fourcolor v1.3.1 built from source in this container (Coq 8.18,
119 files, exit 0, ~23 min on 2 cores). `Print Assumptions` gives "Closed under the global context" for both
`unavoidability : reducibility -> forall G, ~ minimal_counter_example G` (RSST's 32 rules + 633 configurations) and
`four_color`. [L, Coq]

**Reading [E2 + Coq].** The published route is complete as far as this programme's checks go. The rules are RSST's 32,
and Coq proves them unavoidable against RSST's 633. Our engines independently confirm all 633 reducible on two
engines each. What remains is the programme's own bridge: whether "appears" in Gonthier's sense matches the Lean
ConfigOcc / Job 26 semantics. Coq covers that internally for its own proof.

**B3 channel spec (for Long Table's spec comparison; written 18:50Z).** Charge 6 - deg, so a 5 must get rid of
1 - t, a 6 may end at most t above 0, and a big vertex of degree d may take at most d - 6 + t net. Every amount is an
LP variable >= 0 and depends only on the sender's own wheel: its link word read around it, rooted at the receiver,
identified under reflection. Four channels, all along single edges, each with a fixed direction:
(y) 5 -> adjacent big (letter 7, 8 or 9+), keyed by the 5's link rooted at the big. This is the existing class.
(P) parking: 5 -> adjacent 6, keyed by the 5's link rooted at the 6.
(F) forwarding: 6 -> adjacent big, keyed by the 6's full link word (6 letters, privates included) rooted at the big.
(H) hand-on: a vertex of exact degree 7 -> adjacent big, keyed by the 7's full link word (7 letters) rooted at the
target. It is an oriented transfer: each ordered edge (7, big) with its key carries its own variable, so 7 -> 7
transfers in both directions are separate variables. Nothing from degree >= 8 senders yet.
What limits each weight: y and P are paid out of the 5's unit (5-row: sum of y + P >= 1 - t, one row per non-R
5-wheel). P is limited by the receiving 6's row: sum of P in - sum of F out <= t, over every non-R exact 6-wheel, with
the 6's second ring free (cyclic DP), so worst-case parking. F and incoming H are limited by the receiver's row
(d = 7..15 exact; letter 9 for d >= 9; d >= 16 by a max-cycle-mean bound). That row is maximised over u's whole
2-ball, i.e. link, s-ring and the privates of every 6/7 link vertex, so each neighbour's wheel is exact and is checked
against R. An outgoing H is limited by the sender 7's own row, which is charged in - out (H out is subtracted there).
No channel reads beyond the sender's wheel, so no rule needs distance-3 information.

## Round B5 (18 Oct 2026, 23:30Z, Long Table request via the coordinator): RSST on the d=7 receiver 7665566 / 6675666

Pre-registered question (from the request): do the 32 RSST rules pay in full for this receiver, i.e. is every case
with non-zero score dead to a published configuration? Bar: yes iff non-zero cases = cases with a hit.
Result: 15,625 cases, 3,072 score 0, 12,553 non-zero (max 6), and all 12,553 contain a published configuration
(own containment test, strict on 9+, second ring only). Details and control: `b5_lt7/README.md`, commit 9edf7d8b.
One engine; asks for Studio's cross-check.

## Round B3 progress note (23:35Z)

v0 (no patterns) lost to a container restart at a lower bound of 10/27. v2 (complete 849bd5fe snapshot, Studio
09cc8b69) runs; separation at d >= 8 hits its node limit, lower bound -1/8 after 4 iterations. Separator fixed once
(11dcebf4: hashed pattern groups); a stronger windowed pattern-aware bound (`b3_pfh/sepb2.cpp`) is being tested.
