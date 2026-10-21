# s48 judgment: capacity transport vs the existing big->big columns at the A78 receiver rows

Numbers are from `s48/stage1_loads_A78.txt`: the 13 receiverR2 rows of cert_q42aA78L, evaluated at sol_q42aA78 (t = 0.109439) with the engine's own row coefficients. Each big neighbour's spare is taken over every filling of its unseen cells that is admissible as its own row.

**Verdict: dominated at these rows.** Where the rule is guaranteed to pay anything at all, it pays far less than the linear L2/l3q columns already pay, and a radius-2 column sees everything the min sees.

- **Stage 1 alone (fives pay bigs, L1).** Nine of the 13 rows are overloaded. Two of them (d = 10 and d = 11) have no big link neighbour, so adjacency transport pays them nothing. At the other seven, the worst-case spare after stage 1 is exactly 0 at every big neighbour except two:
  - 7766556/6567568 w0, spare 0.0062 against σ(u) = 0.268;
  - 8665566/6765765 w0, spare 0.0221 against σ(u) = 0.241.

  So at the worst filling the rule moves at most 0.006 and 0.022 (less once divided by m(v) ≥ 1), and u stays at 0.26 and 0.22, well above t.
- **The existing columns already move more at the same rows.** l3q takes 0.159 off 7766556/6567568 (lq, u to its link 7), and the L2 tau column x takes 0.132 off 8665566/6765765 (it reappears as +0.132 in the 8's row 76555566/66757666). Both bring u down to t. The only other row with positive worst-case spare is 7656766/6556656 (0.106 at w0 and at w4), and its u is not overloaded after stage 1 (L1 = -0.108).
- **Run on top of the LP's own charges (LF), the rule pays exactly 0.** For every big neighbour of every row, the worst admissible filling has LF(v) ≥ 0.105 > 0, and for most of them LF(v) = t. The worst fillings are often binder rows themselves; for example, 8677656/5566555's w2 is worst at 7766556/6567568.
- **Why the min does not help.** The min reads v's own load and m(v), which lie outside u's 2-ball. That buys nothing while the worst case over v's unseen neighbourhood has no spare. The rule then pays 0 at the adversary's filling, and an LP column keyed on the same radius is priced at that same worst case, so it sees exactly as much. Big2 (D, the second-neighbourhood big->big family) already gave gain 0 in the earlier stage-24 test, and fb6 is a 7->6 channel that the big->big rule does not have at all. The 5 face rows' k-vertices are 6s (RELAY_SPEC_s44).
- **Where a gain could still come from.** Only from killing v's low-spare fillings by configurations that span u's and v's balls (radius 3). Joint reducibility is not checked here. That is the saturation census: if it gains anything, the gain comes from new reducible configurations, not from the min rule. Dropping those fillings would raise the same worst case that any keyed column is priced at.
