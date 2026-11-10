# RSST-FP2: decisions, flags and the §7 check (W6b, 10 Nov 2026)

`src/fp2.py` is a second engine, written from RSSTFP_SPEC.md (33338de6) alone. W6r's results were read only at the
comparison step, in `compare.py`. I read and imported nothing under `rsst_fp/code/`, `rsst_closure/code` or
`pubrules.py`.

Sources:
- `rsst_drules.v` (5ee470f8);
- `unavoidable.conf` (26aeba66);
- `rsst_verdicts.txt` (b6f7a314);
- `rsst_fp/inputs/dom_{A,T,B,C}.json`.

## Decisions where the spec leaves room

1. **Parts.** I parsed them from `rsst_drules.v`, following §3.1–3.2:
   - the bracket gives hat, then fans;
   - an exact 6..8 spoke has its fans padded with `*`;
   - `#2` marks a second copy;
   - a mirror is added unless m(p) ⊆ p.

   Result: 71 parts (6/14/40/11 by subpart count), and the same five carry no mirror. The list is identical, line by
   line, to `inputs/parts71.txt`.
2. **Window.** I built the rotations exactly as in §2:
   - rot(s_i) = w_{i+1}, w_i, a, ring-3 × (deg−4), b;
   - rot(p) = next, w_i, prev, ring-3 × 5. A private is drawn as degree 8 (§12); only its ring-3 slots depend on this,
     and every non-`*` read of ring 3 is OPEN.
   - A 9+ s_i is drawn with 9 slots.

   Every face corner is checked against the rotations, on every row.
3. **Fits.** I implemented §3.3–3.4 literally:
   - hat = succ_x(xp);
   - F = rot(x) strictly between succ_x(xp) and succ_xn(x);
   - |F| ≠ #fans fails the fit;
   - fans on a private or ring-3 spoke set OPEN.
4. **5-sites.** The domain must be exactly [(s_{j−1}, s_j)]. This is asserted on every row, and it held everywhere.
5. **Containment** (§7):
   - an injective map, interior → hosts, with exact letter = degree, and adjacency if and only if adjacency among hosts;
   - interior faces are triangles of E, so "faces map onto triangles" follows from the "iff";
   - configurations with an interior degree above 8 cannot map, and are skipped;
   - verdicts by rsst### index.
   - The matcher ignores orientation, so mirror-image appearances also kill. This is sound: a reflected reducible
     configuration is reducible.
6. **Kills.** I implemented §8.2 as written: minimal members per site under host-set inclusion, every combination must
   contain a configuration, and CMAX = 64 is conservative.
7. **Counting positive fillings: flag.**
   - §8.1 says a group stands for Π_j |class_j(g)| fillings, the product over **all** sites. `fp2.py` follows that.
   - W6r's `fills_*` fields leave out the factor of every site that has no relevant private. An alternative counter
     (`*_relsites`) that multiplies only over sites with relevant privates reproduces every W6r `fills_*` value exactly,
     on all rows of A, T, C and B.
   - So W6r's "+fills" columns, and the "223,020 positive fillings" of §11, understate the spec-exact counts. Spec-exact
     dom totals: A 494,980 (W6r 45,284); T 310,542 (10,749); C 228,600 (9,672).
   - The counting difference changes no maximum, no positive or negative row status, and no kill decision.
8. **Maxima after kills: flag.**
   - §8.3 kill-checks only groups with hi > 0, and W6r's `*_after` maxima are "max over the surviving positive groups,
     otherwise max over all groups with hi ≤ 0, unchecked".
   - §9 ("None means every filling was killed") suggests that every group is checked.
   - `fp2.py` reports both. `*_poskill` is the W6r style. The plain fields are spec-exact: groups are searched in
     descending value until one survives.
   - In many rows every hi = 0 group is killed as well, so the spec-exact maximum is −1 or lower where W6r reports 0.
   - Pass/fail is the same under both readings.

## §7 Assumption H: does the window graph sit induced in T, privates included?

**It holds.** The claim is that in an internally 6-connected triangulation T (no separating 3- or 4-cycle; a separating
5-cycle has a single vertex on one side), with minimum degree 5, the drawn window has no identifications and no edges
beyond those drawn, among u, the w's and the second ring R2 = (s's and privates).

Let d ≥ 5 be the degree of u.

1. **The link is chordless.**
   - The w_i are distinct, since T is simple.
   - A chord w_i w_j with j ≠ i±1 makes u w_i w_j a 3-cycle with link vertices strictly on both sides. That is a
     separating triangle.
2. **The R2 positions are distinct vertices.** Take one vertex x in two positions, a neighbour of w_i and a neighbour of
   w_j, and look at how far apart i and j are.
   - **i = j.** The positions are distinct because T is simple.
   - **j = i+1.** x ≠ s_i would give a triangle w_i w_{i+1} x that is not one of the two faces on w_i w_{i+1}. That
     triangle separates.
   - **|i − j| ≥ 2 both ways round.** u w_i x w_j is a 4-cycle with w's strictly on both sides.
   - A position also cannot be u or a w: a w there would be a link chord.
   - None of this uses exact degrees. It also covers the real, undrawn middle neighbours of a 9+ link vertex, so no drawn
     host coincides with one of them.
3. **No w–R2 or u–R2 edge exists beyond those drawn.**
   - u's neighbours are exactly the w's.
   - An extra edge w_i–x, with x an R2 vertex drawn at w_j, would put x in rot(w_i). That is an identification of two
     positions, excluded by step 2.
4. **R2 has no chord.** Let a ~ b with a, b not consecutive in R2. Take a ∈ N(w_i) and b ∈ N(w_j) with i, j as close
   together as possible.
   - **i = j.** The triangle w_i a b must be a face, so a and b are consecutive in rot(w_i), hence in R2.
   - **j = i+1** (and neither of a, b is s_i). C = w_i a b w_{i+1} is a 4-cycle. At w_i, s_i lies strictly between a
     and w_{i+1} in the rotation, and u lies on the other side. So C separates s_i from u, which is a contradiction.
   - **i and j at least 2 apart both ways.** C = a b w_j u w_i is a 5-cycle.
     - It splits the link into w_{i+1}..w_{j−1} on one side and w_{j+1}..w_{i−1} on the other, and both are non-empty.
     - Internal 6-connectivity then forces one side to be a single vertex, say w_{i+1} with j = i+2. All its
       neighbours lie on C.
     - So w_{i+1} has degree 5 and {a, b} = {s_i, s_{i+1}}. But when w_{i+1} = 5, s_i s_{i+1} is a drawn ring-2 edge,
       so it is not a chord.

**So every T-edge among hosts is a window edge.** Every triangle of hosts is a face of T (no separating triangle), and a
host letter is an exact T-degree. An injective, letter-exact map that is induced on the window is therefore an RSST
appearance in T, with the ring unconstrained.

- **Mirror images.** As in decision 5, the matcher ignores orientation; this is sound by reflection invariance.
- **Ring 3 never matters.** A ring-3 slot of the drawing is a T-vertex at distance 3 from u. By steps 2–4 it cannot be a
  host, so hosts are never compared with ring 3.

**Hypotheses used:**
- minimum degree ≥ 5;
- no separating 3- or 4-cycle;
- a separating 5-cycle has one side a single vertex, used only in the last case of step 4. This is Birkhoff's ring-5
  clause, as in our Lean `NoShortSepCycle`.

**Not checked:** this argument has not been checked in Lean or by machine.

## Results (fp2 against W6r's fp_<SET>.json, row by row)

| set | rows | field mismatches (W6r convention) | +rows dom (mine / W6r) | +rows K582 | +rows K633 | max hi dom / K582 / K633 (mine = W6r) |
|---|---|---|---|---|---|---|
| A | 162 | 0 | 38 / 38 | 0 / 0 | 0 / 0 | 5 / 0 / 0 |
| T | 305 | 0 | 35 / 35 | 1 / 1 | 0 / 0 | 5 / 1 / 0 |
| B | 495 | 0 | 98 / 98 | 4 / 4 | 0 / 0 | 6 / 1 / 0 |
| C (extra) | 281 | 0 | 25 / 25 | 0 / 0 | 0 / 0 | 1 / 0 / 0 |

**What was compared.**
- Per row: status, n_fill, n_groups, relevant, rel_8mid, n_inst, lo_max, hi_max, groups_hi_pos, groups_lo_pos,
  groups_hi_pos_killed / kept / killed_proved, inexact_groups.
- The W6r-style fills and after-maxima, for both kill models.
- Over the 1,243 rows, no field differs.

**Spec-exact view.** Every group is kill-checked, and fillings are counted over all sites.
- The maximum after K633 is 0 in every set, and after K582 it is 1. These maxima exclude B's 14 capped rows, for which
  the spec-exact value is only known to be at most the W6r-style one.
- Positive fillings under the domains alone: A 494,980, T 310,542, B 2,897,748, C 228,600.
- Positive fillings after K582: T 1,152 and B 167,152. W6r reports 72 and 728, because of the counting flag above.
- Positive fillings after K633: 0 everywhere.

**The 5 none-dependent rows** (positive under K582, killed under K633) are identical to W6r's, and so are their none
configurations:
- B 8 76576756 65555556 — 2.126;
- B 7 8557766 7565755 — 124.1324817 and 2.126;
- B 7 8565766 5557657 — 128.1324802;
- B 7 8565766 5557656 — 128.1324802;
- T 8 56765767 56655555 — 2.126.

**Worked argmax fillings after K582.** The filling text is identical to W6r's §11, and each filling has lo = hi = 1. Each
contains only "none" configurations: `results/worked_none_dependent.txt` gives its privates, fits and configurations.

**test_vectors.json.**
- All 8 vectors pass: the fits touching u and their condition text, every listed filling's lo, hi, fits fired
  (sure/possible) and the configurations it contains, and every summary field.
- This holds under the W6r convention for fills and after-maxima (`results/out_vectors_conv.txt`).
- Under the spec-exact convention, 6 vectors differ, and only in those two kinds of field (`results/out_vectors.txt`).

**B rows 204..494** ran with `fp2c.py`. It is fp2.py with only a row-range option and a cap of 2,000 kill-checks on the
spec-exact after-kill search. The W6r-style fields are unaffected.
