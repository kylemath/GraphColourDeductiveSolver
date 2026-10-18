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
cases (16 fillings x 5^6 privates, any third ring), except the 34,375 cases with (s1 = 6 and p2a = 5) or (s4 = 6 and
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
