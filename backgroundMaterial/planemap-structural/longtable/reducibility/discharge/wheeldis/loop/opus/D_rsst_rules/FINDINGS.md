# D_rsst_rules — FINDINGS
Question: are RSST's 32 discharging rules (as in Gonthier fourcolor) inside an LP rule class (a)/(b)/(c)/L2, and would RSST's 633 configs as R make the LP feasible (t*<=0) — what gaps block that, and what minimal hybrid "link" closes it?
Guess: RSST rules are radius-<=2 "send 1 or 1/2 from big to 5 under degree-constrained 2-ball patterns" = mostly class (a)/(c)-like; the blocking gaps are pattern semantics (">=" degree bounds vs exact 5..8/9+), configs of radius >2 relative to the positive vertex, and RSST's deg>=12 hand case.
What would change the plan: if RSST rules read only the 2-ball with constraints expressible in the LP's letters, then adding RSST's 633 as forbidden 2-ball patterns gives a guaranteed feasible LP -> pivot K>=2 to "cite RSST unavoidability", keeping K<=1 own-config novelty.

---

Sources. Gonthier's development `math-comp/fourcolor`, cloned `--depth 1` into `fourcolor/` here (commit c1d6b1cd, 20 Aug 2026).
`FC/` below means `fourcolor/theories/proof/`. Repo paths are relative to `wheeldis/` (= W) unless they start with `SolvingFrameworkPlan/`
or `backgroundMaterial/`. Tags: [cited] = read in the file named; [hand] = my own argument from cited facts; [I] = inferred, not
checked by computation. The only computation was a parse of `unavoidable.conf` and of `FC/discharge.v` (one-liners, under 1 s).

## 0. Verdict in one paragraph

(1) RSST's 32 rules (38 parts in Gonthier's encoding) are **not** in (a), (b), (c) or L2. Each rule is a transfer of 1 unit (1/10 in LP units)
from a **sender of degree 5..8** to an **adjacent receiver of degree ≥ 6**. The rule reads only the **sender's 2-ball**, over the alphabet
{5,6,7,8,9+}, including fan degrees. The rule class (a)/(b)/(c)/L2 has no sender of degree 6, no receiver of degree 6, and no transfer
7→8+ or 8→8+. In (a)/(c) only drule2, plus the ≥7-receiver restrictions of drule1/drule3, fit. (2) The implication "RSST ⇒ t* ≤ 0"
**is valid for a widened LP**, not for the present one. Gonthier's proof is *exactly* a 2-ball-local row check at every hub of degree 5..11,
plus a per-edge cap that handles ≥ 12. Its alphabet is the LP's (letter 9 = ≥ 9), and its configurations are looked for only in the hub's
second neighbourhood. So the blocking gaps are three: the rule class, the row set (degree-6/8 hubs, fans), and the matcher (kernel embedding
of the 633, not the LP's receiver-centred or 5-centred patterns). Folding, ≥ 12 and C-certification are *not* blocking if the 633 are taken
from Gonthier. (3) The smallest guaranteed link is "RSST's 38 parts as fixed columns + the 633 as hub-2-ball patterns + hub rows for
degrees 5..11". It is Gonthier's theorem re-encoded and needs no LP. It makes the programme's own configurations logically redundant, because
the K ≤ 1/K ≥ 2 split does not survive RSST's charge flow (5s pay 6s). The programme's novelty survives only as **pruning**: replacing RSST
configurations by R_prog in Gonthier's presentation tree, which can be checked leaf by leaf. Details follow.

## 1. RSST's rules as Gonthier encodes them

**Encoding.**
- [cited] `FC/discharge.v:10-35`. "the 32 rules given by Robertson et al. to move charges across edges, … represented here by one or two
  part objects". A part that fits at dart x "transfers one unit from the face of x to that of edge (face^2 x)". The faces of Gonthier's
  cubic map are the vertices of the triangulation. So the part's **hub** is the sender and its **third spoke** is the receiver.
- [cited] The sign is unambiguous:
  - `dscore x = 60 − 10·arity x + Σ_{y∈face x}(dscore1(edge y) − dscore1 y)` (`FC/discharge.v:171-172`), with
    `dscore1 y = count (exact_fitp (inv_face2 y)) the_drules` (`:167`).
  - `dscore_cap1` (`:378-390`) uses incoming ≤ m per edge to bound big hubs.
  - `pick_source_drules` = "rules for taking score units from the hub face" (`:37-41,268-269`).
- [cited] A part = ranges of arities on the hub's **second neighbourhood**: spokes, hats, and fans (N−5 fans for a spoke of exact arity
  N ∈ 6..8) (`FC/part.v:9-24,59-63`). Ranges are [M,N] with M,N ∈ 5..9, "N=9 to indicate an unbounded range" (`FC/part.v:42-47`).
  Syntax: `*`, `M`, `M+`, `N-`, `M?N` (`FC/part.v:66-73`).
- [cited] Normalisation `10·(6−deg)`, total 120 (`FC/discharge.v:30-31,201`). LP: `6−deg`, total 12 (README.md:5). One RSST unit = 1/10
  LP unit. drule1 is listed twice (`FC/discharge.v:17-19,145`), so it moves 2/10 = 1/5.
- [cited] The 38 parts are at `FC/discharge.v:73-140`; the list is at `:144-149`. The mirror images are added by `symmetrize_drules`
  (`:151-158`).

**What each part reads.** My parse of `FC/discharge.v:73-140` [cited data, hand classification]:

| sender (hub) degree | parts | receiver (spoke 3) range | reads beyond the sender's link? |
|---|---|---|---|
| 5 | drule1 (×2), drule2, drule3 | 6+, 7+, 6+ | no: spokes only |
| 6 | drule2', 3', 4, 4', 5, 6, 7 | 7+, 6+, 6+, 6+, 6+, 7+, 7+ | hats in 4, 4', 6, 7; a **fan** in 5 (`[6- 5] 6`) and 7 (`[6 6-] 6`) |
| 7 | drule8..27 + 10' (21 parts) | 7+ mostly; exactly 7 in 18, 21, 22, 24, 26, 27; 8+ in 13, 19 | hats in many; fans in 25 (`[* * 5] 7`), 27 (`[6 5 6+] 7`) |
| 8 | drule28..32 + 31' (6 parts) | 7+ (exactly 7 in 32) | hats; spoke 8 of the sender |

- drule2/3 are specialised to hub 5 and hub 6, i.e. RSST's rule has sender "≤ 6" (`FC/discharge.v:19-20`).
- Sender range 5..8 (`source_drules_range`, `FC/discharge.v:392-398`).
- Every receiver range is ⊆ 6+, so **5s never receive** [hand, from the table].
- **Radius.** Every rule is a function of the sender's closed 2-ball (spokes, hats, fans), and the receiver is adjacent to the sender.
  No rule reads the receiver's own 2-ball beyond what lies in the sender's [cited `FC/part.v:9-24`].

**Membership in the programme's classes** (classes as written at README.md:10-15, 338-342, loop/l2/FINDINGS.md:5-8) [hand]:
- **Base class / (c)** (5→7+, rooted link word or receiver 2-ball):
  - drule2 fits in full: a 5 next to a 5 sends 1/10 extra to their common 7+ neighbour.
  - drule1 and drule3 fit only after restricting the receiver to ≥ 7. Their 6-receiver halves are outside: the classes have "u of
    degree ≥ 7" only (README.md:338).
- **(a)** (5→7+, the sender's rooted 2-ball): the same three, no more. The 5-sender rules read only the link.
- **(b)** ("7→7, 8→7, depending on both endpoints' 2-balls", README.md:340-341):
  - Fully inside: the parts with receiver exactly 7, i.e. drule18, 21, 22, 24, 26, 27, 32.
  - Partly inside: the other 7- and 8-sender parts, but only their exact-7-receiver slices. 7→8+ (drule13, 19), 7→8, 7→9+, 8→8 and
    8→9+ are outside.
- **L2** (`loop/l2/FINDINGS.md:5-8`): the edge type τ is "(deg from, deg to, the two sides of the edge)", with side letters 7, 8, 9.
  - This is a *coarse* projection of the two 2-balls: it does not see the 5/6 pattern on the sender's other spokes. drule15 needs the
    sender's whole link `5 6 7+ 5 7+ 5 6`.
  - So L2's variables cannot express RSST's big-sender rules unless τ is refined to the sender's full 2-ball [hand].
- **Outside every class:** the 6-senders (drule2', 3', 4, 4', 5, 6, 7) and the 6-receivers (drule1, 3, 3', 4, 4', 5). Through these, RSST
  **relays charge through 6s**. The programme makes the 6s inert (README.md:10; "charge moves only between adjacent vertices of
  degree ≠ 6", README.md:350).
  - The nearest object the programme tried is the composite 5→6→big (H-R1, GATE-K2.md:27, "dies [I]"). It was tried against the
    programme's own R, not RSST's.
  - RSST also has 6→6 transfers (drule3', 4, 4', 5 have receiver 6+). Composing chains into direct 5→big rules therefore gives rules of
    unbounded reach in principle [I]. They are not equivalent to any finite-radius 5→adjacent-big rule.

**The class that does contain them** [hand]. Call it **(a+)**: a sender s with deg s ∈ 5..8 sends y(P, j) to its j-th neighbour, where
deg ≥ 6. Here P is s's 2-ball over {5,6,7,8,9+} with fans, rooted at that neighbour.
- (a) is the slice deg s = 5, receiver ≥ 7; (b) is roughly the slice deg s ∈ {7,8}, receiver = 7.
- RSST is one 0/1/2-valued point of (a+), scaled by 1/10.
- (a+) is inside the "umbrella (G)" of README.md:343. So test G's argument (README.md:350-352, 6-sea defects) applies to (a+) only with
  reach ρ through 6s, and gives t* ≥ c(Y)/|N_ρ(Y)|.

## 2. Does RSST's theorem imply LP feasibility? Precisely when

**What Gonthier proves.**
- [cited] `unavoidability : reducibility -> forall G, ~ minimal_counter_example G` (`FC/unavoidability.v:20-34`).
- The proof is the following.
  - Some face has `dscore > 0` (`posz_dscore`, `FC/discharge.v:212-217`).
  - Hubs of arity ≥ 12 are excluded by `dscore_cap1 G 5` (`FC/unavoidability.v:26`; `FC/discharge.v:378-390`): at most 5 units
    cross any edge. This is proved **by computation, using reducibility** (`check_dbound1` over `pcons_ n` for n ∈ 5..8, with
    `no_fit_the_redpart`; `FC/unavoidability.v:28-33`, `FC/hubcap.v:38-46`). So it replaces RSST's hand argument. A d ≥ 12 hub then
    has ≤ 60 − 10d + 5d < 0.
  - Arities 5..11 are excluded by `exclude5..exclude11` (`FC/present5.v:17` … `FC/present11.v:17`).
- **Each `excludeN` is a finite case tree over the hub's 2-ball** [cited `FC/present.v:10-60,88-93`]. Every leaf is one of:
  - `Reducible`: every 2-ball fitting the leaf part contains the kernel of one of the 633 configurations (`redpart`,
    `FC/redpart.v:9-17`);
  - `Hubcap`: an upper bound on Σ dscore2 around the hub, computed from source rules at the hub and **converse rules restricted to the
    hub's 2-ball** (`FC/part.v:113-120`: constraints outside the 2nd neighbourhood are dropped, which over-approximates incoming
    charge), with redp pruning (`FC/hubcap.v:47-60`);
  - `Similar`: a symmetry.
- Leaf counts (my grep of `FC/present{5..11}.v`), as Hubcap / Reducible / Similar:

  | hub | Hubcap | Reducible | Similar |
  |---|---|---|---|
  | 5 | 10 | 5 | 10 |
  | 6 | 236 | 21 | 62 |
  | 7 | 1989 | 480 | 181 |
  | 8 | 1715 | 387 | 110 |
  | 9 | 1015 | 301 | 88 |
  | 10 | 256 | 103 | 74 |
  | 11 | 53 | 27 | 91 |

  Total 5,274 Hubcap and 1,324 Reducible leaves [cited counts]. Fan splits (`f[1..3]`) occur 843 times (`grep -c`), at hubs 6..11.

**Translation** [hand]. Take the LP whose
- columns are (a+) (or just the 38 RSST parts, fixed at 1/10);
- rows are, for every hub degree 5..11, every 2-ball pattern (exact degrees 5..8, letter 9, fans for spokes 6..8), with the hub's net
  charge bounded using incoming rules evaluated on the hub's 2-ball. Either take the worst case over completions, or use Gonthier's
  over-approximation;
- forbidden patterns are "contains a 633-kernel in the hub's 2nd neighbourhood";
- and which carries a per-edge cap of 1/2 for d ≥ 12.

Then RSST's assignment satisfies every row with t = 0. The reason: each row value is ≤ Gonthier's leaf bound ≤ 0. The worst-case-completion
row is pointwise ≤ the over-approximated row, so exact 3-ball rows are fine too. **So yes, t* ≤ 0 for that LP.**

Gaps between that LP and the programme's LP, one by one:

1. **Rule class: BLOCKING.** See §1. Even with R ⊇ RSST633, the programme's columns cannot reproduce RSST's flow. No 6s move charge,
   there are no 7→8+ or 8→8+ transfers, and L2's τ is too coarse. Whether R_prog ∪ RSST633 makes the *present* classes feasible is
   open: RSST's theorem says nothing about it [I].
   - One structural reason it might still fail: the self-pairing obstruction (loop/l2/FINDINGS.md:21-26, GATE-K2.md:66-69) also
     binds RSST's 7→7 rules, since they read only the sender's 2-ball.
   - RSST escapes it through different rows (5s pay 6s first), not through better 7→7 rules [I].
2. **Row set: BLOCKING.** RSST needs positive-hub rows for degree 6 (`exclude6`: 236 hubcaps, 21 reducible leaves) and for 7/8 as
   *senders*.
   - The LP has sender rows only for 5s and receiver rows d = 7..15 (README.md:10-15, 214-219).
   - The LP's receiver row stores link + hats (s_i) + an existential fan for 6-spokes, but **no fans of 7/8 spokes** (README.md:11-14).
     Gonthier splits on fans 843 times. So the LP rows must be refined by fans, or maximised over fan fillings, which is weaker and may
     lose RSST's closure [I].
3. **"Appears": BLOCKING as implemented, but compatible in principle.**
   - The alphabet matches exactly: LP letter 9 = "≥ 9" (README.md:8); Gonthier `Pr59` = "9+" (`FC/part.v:45-47`).
   - The RSST matcher needs inner config vertices of degree ≤ 8 except the hub (`FC/redpart.v:15-16`). My count over
     `backgroundMaterial/planemap-structural/studiointel/routeb/rsst/unavoidable.conf`:
     - 566 of the 633 have every inner degree ≤ 8;
     - 67 have exactly one inner vertex of degree 9..11 (never two), which must then be the exact-degree hub;
     - every kernel has inner radius ≤ 2 (591 radius 2, 42 radius 1).
     So **every one of the 633 is expressible in the LP's alphabet when centred at the right hub** [cited data + hand].
   - But the LP's registry patterns are receiver-centred (u + S + links of S, B free; README.md:222-225) or 5-centred keys. Neither is
     "kernel embeds somewhere in the hub's 2nd neighbourhood". A new matcher is needed: Gonthier's quiz tree (`FC/redpart.v`,
     `quiztree.v`), or a subgraph-iso on `ball.build`.
   - "Link words with 9 are non-R" (README.md:8) must be dropped for hub-centred matches.
4. **Configs counted only via the second neighbourhood of the positive vertex.** Not a gap: it is the same semantics in both
   (`FC/redpart.v:9-17`; the LP's patterns live in u's 2-ball). RSST never needs a configuration outside the hub's 2-ball.
5. **Degree ≥ 12.** Not a gap. Gonthier replaces RSST's hand argument by the computed per-edge cap of 5 units = 1/2 LP unit
   (`FC/unavoidability.v:26-33`). Any (a+) solution with per-edge outflow ≤ 1/2 handles d ≥ 12 trivially (6 − d + d/2 ≤ 0). This is
   stronger than the LP's Karp/letter-9 bound (README.md:17-19).
6. **Internal 6-connectivity, regular 2-balls.**
   - Gonthier needs only `plain_cubic_pentagonal` plus "no config fits anywhere" for the discharging half (`FC/discharge.v:320`,
     `FC/redpart.v:44-46`, `FC/present.v:168-176`).
   - Parts are matched at the dart level, so a folded or non-simple 2-ball is handled without a regularity lemma [cited
     `FC/part.v:9-24`].
   - The programme's matcher assumes a regular 2-ball. This is proved for 5-centres (README.md:21-25, §3). For 7..15-centres it is
     "unproved" (README.md:244, 311) and only hand-argued via B2 (`SolvingFrameworkPlan/docs/working/COORDINATOR-STATE.md:51,151`).
   - A hub-row LP needs it for hubs 6..11. Gap: small (a hand lemma), but real.
7. **Folded rings (Job 26) and C-certification.** Not a gap for the 633 if cited. Gonthier certifies all 633 C-reducible in Coq
   (`FC/job001to106.v:12` … `FC/task*.v`, `the_configs` in `FC/configurations.v:11`), including the embedding of an appearance into a
   minimal counterexample (`FC/embed.v`, `FC/birkhoff.v:669`). It still is a gap for R_prog itself
   (COORDINATOR-STATE.md:51: K ≤ 1 claim scoped to simple rings).

**Does Gonthier check the discharging step in a form the LP could cite or reproduce?**
- **Cite: yes, but only wholesale.**
  - The unavoidability half is `FC/discharge.v` + `FC/hubcap.v` + `FC/redpart.v` + `FC/present*.v` + `FC/unavoidability.v`, all
    Coq-checked.
  - Correction to the brief: `job*.v` are the **reducibility** proofs of the 633 (`FC/job001to106.v:7-12`), not unavoidability.
  - The citable statements are `exclude5..exclude11` and `unavoidability`. All take `reducibility` (all 633, `FC/present.v:72`) as
    hypothesis, and `valid_hub` includes `minimal_counter_example` (`FC/present.v:74`).
  - So one cannot cite a *subset* of the 633 or a different rule set. Any change means re-running the scripts.
- **Reproduce: yes, cheaply in principle** [I].
  - The presentation scripts are explicit data: ~6.6k leaves, Pcase thresholds on spokes, hats and fans.
  - Re-checking needs four things: `fitp`, `converse_part` (with the over-approximation), the hubcap bound with redp pruning, and a
    633-kernel matcher on parts.
  - Caveat: `redpart` is proved sound but is "only complete … empirically" (`FC/redpart.v:18-24`). A reimplementation must reproduce the
    tree's `Reducible` leaves, not merely find *a* config.

## 3. The smallest hybrid "link", and what novelty survives

**(L0) Guaranteed, minimal.** Add three things.
- (i) Columns: the 38 RSST parts as fixed columns, 1/10 each, in class (a+).
- (ii) Rows: hub-2-ball rows for degrees 5..11 with fans, plus the 1/2 per-edge cap.
- (iii) Patterns: the 633 as hub-2-ball kernel patterns, with Gonthier cited for their reducibility.

Feasibility is then Gonthier's theorem, and nothing needs optimising. **Novelty surviving: none for unavoidability.**
- R_prog's K ≤ 1 configurations become logically redundant. RSST's 633 are already unavoidable.
- Worse, the K split does not transfer [hand, from drule1]. Under RSST's rules every 5 pays every 6+ neighbour 1/5, so a lone 5 such as
  66667 sits at 0 after drule1 alone. The K ≤ 1 difficulty the programme solved with its own configurations is absorbed by RSST's
  6-relays, and the load moves to hub-6/7/8 rows.
- So "K ≤ 1 by own configs, K ≥ 2 by RSST" is **not** a consistent decomposition. The two discharging schemes route charge differently.
  A big receiver's RSST hubcap bound assumes every neighbouring 5 follows RSST's rules. Mixing schemes voids both certificates
  [hand; mixing a convex combination does not help, since the programme's scheme is not ≤ 0 at K ≥ 2 rows].

**(L1) Smallest link that keeps measurable novelty: prune RSST's configurations, keep RSST's rules.**
- Re-run Gonthier's presentation tree with the leaf oracle "contains a kernel from R_prog ∪ S", greedily shrinking S ⊂ RSST633.
- R_prog patterns that fit are those lying inside a hub's 2-ball: receiver-centred u + S + links do; 5-centred keys do only at hub 5 or
  when they lie within distance 2 of the hub.
- Hubcap leaves also call redp (`FC/hubcap.v:47-60`), so dropping a config can break a hubcap as well as a Reducible leaf. Both are
  re-checkable.
- Product: an unavoidable set R_prog ∪ S. Its unavoidability is RSST's rules, re-checked, and its reducibility is the programme's (Lean)
  for R_prog plus Gonthier's for S.
- Novelty = |RSST633 \ S|, i.e. how much of RSST the 2-ball/K ≤ 1 work replaces. Prediction [I]: small. RSST's load sits in hub-7/8 leaves
  (867 of 1,324 Reducible leaves), where R_prog's receiver-centred windows are strongest (d = 7/8 rows). So this is the place to measure.
- Allowing the rules to re-optimise inside (a+) (an LP over (a+) columns with R_prog ∪ S rows) is the next size up. It keeps
  feasibility for S = RSST633 by (L0) and can only enlarge the prunable set.

**What would change this verdict.** A demonstration that the programme's *present* classes are feasible with R_prog ∪ RSST633 would revive
"K ≤ 1 own + K ≥ 2 by RSST configs, programme's own rules". Test it by adding the 633 kernel matcher to `sep3`'s pattern check on the
current binders (e.g. d = 7 5567576/5756756, GATE-K2 binders). That is the B_rsst_rows probe, not done here. My guess is that it fails at
the self-paired d = 7 rows unless a 633 kernel sits in every filling of their 2-balls [I].
