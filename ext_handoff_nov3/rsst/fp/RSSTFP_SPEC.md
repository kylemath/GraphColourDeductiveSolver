# RSSTFP_SPEC: per-vertex realisation check of the RSST discharging fixed point, degrees 5..9+

W6r (claim L-1), round6/W6r-replay/rsst_fp/, 2026-11-10. The reference implementation is `code/fp_exact.py`, built on pubrules.py 95e8ce8a. The Studio should be able to build the check from this document alone, using only the input files listed in §1. Results for the d = 7 / 8 run are in §11 and test vectors are in §10.

## 0. What the check computes

Take a vertex u of degree d and a *row*: the letters of u's 2-ball that are fixed (the link w_0..w_{d-1} and the apexes s_0..s_{d-1}), plus a domain for each of the vertices that are not fixed (the *privates*). For **every** filling of the privates that the domain allows, the check computes u's final charge under the RSST discharging rules. It uses all 71 of Gonthier's parts, t = 0, and no LP variables. A test that reaches outside the 2-ball cannot be decided, so the charge is an interval [lo, hi].

For each row the check reports the following, under each of three kill models (domains only; domains + 582 proved RSST configurations; domains + all 633):

- the maximum lo and the maximum hi;
- an argmax filling;
- the number of positive fillings;
- the RSST configurations that cover each positive filling.

A row **passes** under a kill model when hi ≤ 0 for every filling that model does not kill. The check is exhaustive: it uses grouping or DP, never sampling. A row that is too large is reported as `not done`.

## 1. Inputs (md5)

| input | file | md5 (first 8) |
|---|---|---|
| parts | `loop/pubrules/data/rsst_drules.v` (Gonthier, discharge.v: drule1..drule32, `base_drules` = 38 entries) | 5ee470f8 |
| the 71 parts as parsed (cross-check for §3) | `rsst_fp/inputs/parts71.txt` | see MD5SUMS |
| RSST configurations (633) | studiointel `routeb/rsst/unavoidable.conf`, parsed by `rsst_parse` + `rsst_rows.prep` | 26aeba66 |
| matcher | Studio `loop/studio/rsstD/rsst_rows.py` (`contains`) | c9f344bd |
| verdicts | `loop/k44/rsst_verdicts.txt`: D2 249, C2cons 333, none 51 | b6f7a314 |
| d = 7 / 8 domains | V2ROW_SPEC §3 domains under the K3gB5n settings, dumped by `rsst_closure/code/r16p8_dom.py` → `rsst_fp/inputs/dom_{A,B,C,T}.json` | see MD5SUMS |
| reference code | `loop/pubrules/pubrules.py` (Window, rsst_fit, rsst_instances, u_ledger); `rsst_fp/code/fp_exact.py` | 95e8ce8a |

**Verdict classes.**
- **proved (582)**: D2 or C2cons, re-proved on our engines.
- **proved-modulo-admissibility (51)**: the configurations with verdict none, 2.126 among them. W6b's RSST-NONE (round16/round9_rsstnone/ADMISSIBILITY.md) found all 51 C-reducible with RSST's own contraction X, on `kc_rn -B` and `cfast --fixed`. Only ring-merge admissibility is still missing.
- **all 633** is the union of the two.

## 2. Letters and the window

**Letters.** 5, 6, 7 and 8 are exact degrees. 9 stands for "9+", degree ≥ 9 and never exact. A range test on a 9+ vertex reads the value 9.

**Vertices.** All indices are taken mod d.

- u, with degree d.
- w_i, the link of u in rotation order.
- s_i, the apex of the triangle w_i w_{i+1} s_i on the far side of the edge w_i w_{i+1}.
- The **privates** of w_i. If w_i has letter L ∈ {6, 7, 8}, it has L−5 privates p_i.1, …, p_i.(L−5). They are numbered from the s_{i−1} side to the s_i side, so the neighbours of w_i strictly between s_{i−1} and s_i are p_i.1..p_i.(L−5).
- A link letter of 9+ is drawn as an 8: it gets three privates p_i.1..p_i.3, and its degree is set to 9 (see §6).
- **Ring 3**: every vertex not listed above. Ring-3 vertices have unknown degree.

**Faces.** All faces are oriented the same way, which this document calls ccw.

- (u, w_i, w_{i+1}).
- (w_i, a, b) for each consecutive pair a, b in seg_i = [s_{i−1}, p_i.1, …, p_i.k, s_i]. A 5 has seg_i = [s_{i−1}, s_i], so s_{i−1} ~ s_i.
- (w_i, s_i, w_{i+1}).

Each face (x, y, z), read in any of its three cyclic shifts, defines succ_x(y) = z and opp(x, y) = z.

**Rotations.**
- rot(u) = w_0, w_1, …, w_{d−1}.
- rot(w_i) = u, w_{i−1}, s_{i−1}, p_i.1, …, p_i.k, s_i, w_{i+1}.

**Ring-2 edges.** The ring-2 cycle is R2 = s_{i−1}, p_i.1, …, p_i.k, s_i, p_{i+1}.1, …. For a ring-2 edge {a, b} with a, b consecutive in R2, the vertex opposite w_i is in **ring 3**. The rotations of s_i and of the privates therefore run through ring 3. Each still has exactly its own degree of slots: s_i has 2 w's, 2 ring-2 neighbours, and deg − 4 ring-3 neighbours.

**What is ring 3 in practice.** The following tests read a ring-3 vertex:
- a hat across a ring-2 edge;
- every fan of an s_i;
- every hat or fan of a private spoke.

The following tests stay inside the window:
- hats across an edge u–w_j: from a hub w_i, opp(w_{i−1}, u) = w_{i−2} and opp(u, w_{i+1}) = w_{i+2}; from the hub u, the hat of spoke w_j is opp(w_j, w_{j−1}) = s_{j−1};
- hats across w_i–s_i (they are p_{i+1}.1, or s_{i+1} when w_{i+1} = 5);
- hats across s_{i−1}–w_{i−1};
- every fan of u or of a w_j.

**Orientation of the V2ROW_SPEC domains.** In the row domains, x_j is the neighbour of w_j just before s_j and y_j is the one just after s_{j−1}:

| letter of w_j | privates | domain pair (x_j, y_j) |
|---|---|---|
| 5 | none | a single pair (s_{j−1}, s_j), fixed by the row; an empty list kills the row |
| 6 | p_j.1 = x_j = y_j | pairs (x, x) |
| 7 | p_j.1 = y_j, p_j.2 = x_j | |
| 8 | p_j.1 = y_j, p_j.3 = x_j, middle p_j.2 = m_j | the domain does not constrain m_j, so m_j ranges over 5..9+ |
| 9+ | y_j = p_j.1, x_j = p_j.3 | middles held at 9+ (§6) |

**Filling notation** (as written in the output): `p{j}=a` for a 6-site; `x{j}=a,y{j}=b` for a 7-site or a 9+ site; `x{j}=a,m{j}=c,y{j}=b` for an 8-site. A 5-site has nothing to write.

## 3. Parts and fits

### 3.1 Parsing a part

A part is written `Part $ [hat fan fan ...] spoke $ ... $.` The bracket is optional. Range tokens are:

| token | range |
|---|---|
| `*` | 5..9+ |
| `a?b` | a..b |
| `a+` | a..9+ |
| `a-` | 5..a |
| a digit a | exactly a |

A subpart is the triple (spoke range, hat range, fans). The hat range defaults to `*`. If the spoke range is an exact 6, 7 or 8, the fan list is padded with `*` up to spoke−5 entries.

### 3.2 The 71 parts

`base_drules` lists 38 names. A name that appears a second time is tagged `#2`; `drule1` is one of these, so a 5 sends 2 units through drule1. Each entry contributes its part p, plus its mirror m(p) with tag suffix `m`, unless m(p) ⊆ p. With n subparts:

- the mirror is m(p)[k2] = (spoke p[(4−k2) mod n], hat p[(5−k2) mod n], fans reversed(fans p[(4−k2) mod n]));
- p ⊆ q means the same n, spoke ⊆ spoke and hat ⊆ hat for every subpart, and fans ⊆ fans entrywise wherever q has fans (and p must then have them too).

This gives **71 parts**. By number of subparts there are 6 with 5, 14 with 6, 40 with 7 and 11 with 8. The parsed list is in `inputs/parts71.txt`. Five parts are mirror-equal and get no mirror: drule1, drule1#2, drule10', drule12 and drule31'. **No part has m(p) strictly inside p**, so the part set is closed under reflection, and a search may use rotation and reflection classes. Every fan list that is not all `*` sits on a spoke of exact degree 6..8 (checked on all 71 parts).

### 3.3 A fit

A part p with n subparts fits at hub h when **deg h = n exactly**, so h has letter 5..8. Let S = rot(h) and take an anchor a ∈ 0..n−1. For j = 0..n−1, let x = S[a+j], xp = S[a+j−1] and xn = S[a+j+1]. The fit requires every one of the following:

1. **Spoke.** deg x ∈ spoke_j.
2. **Hat.** If the hat range is not `*`: deg(opp(x, xp)) ∈ hat_j. This is the vertex across the edge xp–x from h.
3. **Fans.** If some fan is not `*`:
   - x must be u, a w or an s; for a private or ring-3 x the test is OPEN.
   - Let hv = opp(x, xp) and hn = opp(xn, x).
   - F is the list of vertices of rot(x) strictly after hv and strictly before hn, going ccw. In x's rotation the order is h, xp, hv, F…, hn, xn.
   - If |F| ≠ #fans the fit fails. Otherwise test each fan range on the vertex of F at the same position.

A fit moves **1 unit from h to S[a+2]**, its third spoke. Every (tag, hub, anchor) that fits counts on its own, so a duplicated tag counts twice.

### 3.4 Test semantics

- On u, a w or an s, a test is decided at once (true or false), with 9+ read as 9.
- A full range `*` is always true and never OPEN.
- On a private, a test becomes a condition `lo ≤ letter ≤ hi`, and conditions on the same private are intersected. An empty intersection fails the fit.
- On ring 3 (including a hat that does not exist), a non-`*` test sets OPEN.

A fit instance is therefore one conjunction (an *alternative*): a set of private intervals, plus an OPEN flag. For a filling f:
- the instance is **sure** if the conjunction holds on f and OPEN is false;
- it is **possible** if the conjunction holds on f, whatever OPEN is.

### 3.5 Fits that move u's charge

Only two kinds of fit move u's charge:
- hub = u, which needs d ∈ 5..8; the target is some w_i;
- hub = w_i with target u; the hub has letter 5..8.

No other hub has u as its third spoke. For d ≥ 9, u is never a hub, because no part has 9 or more subparts.

## 4. Charge

The base charge is 10(6−d), in RSST units; our 6−deg scale is the RSST unit divided by 10.

- lo(f) = base + #{fits into u that are sure on f} − #{fits out of u that are possible on f}
- hi(f) = base + #{fits into u that are possible on f} − #{fits out of u that are sure on f}

The true final charge of any extension of the 2-ball lies in [lo, hi]. The pass test uses hi. On every argmax found in the d = 7 / 8 run, lo = hi (§11).

## 5. Domains: what counts as a filling

- **d = 7, 8.** Per site, the list of pairs (x_j, y_j) from V2ROW_SPEC §3 (K3gB5n settings), in the JSON form `{"d LINK SWORD": [[ [x,y], ... ] per site j]}` and with the orientation table in §2. The fillings are the product over sites of the site options. An 8-site multiplies its options by 5 for m_j ∈ 5..9+. A 9+ site counts its middle as one letter with 5 values; this is a counting convention only, because the middle is never read (§6).
- **d = 5, 6.** cons2 has no kills in our model, so there are **no domains**. Every link letter is 5..9+, every apex is 5..9+, and every private is 5..9+. The rows are all (link, apex) words, which may be reduced to rotation and reflection classes (§3.2). Kills come only from RSST appearances (§7).
- **d ≥ 9.** As for d = 5, 6: every letter is free, and kills come only from RSST appearances. u never sends.

## 6. Exact 9+ handling (a link vertex of degree ≥ 9)

Draw w_j as an 8: privates p_j.1 = y_j, p_j.2 = middle, p_j.3 = x_j. Then set deg w_j = 9. This is **exact**, not a relaxation, for four reasons:

1. w_j is never a hub, because no part has 9 or more subparts.
2. Its fans are never read. Fans are read only on spokes of exact degree 6..8 (§3.2), and the spoke test fails first on a 9+.
3. Its middle privates (really ≥ 2 vertices of unknown degree) are adjacent only to w_j, to each other and to ring 3. So no fit at u or at a w_i reads them. They are not hats of any hub spoke pair, and they are fans only of w_j or of privates.
   - `fp_exact.py` asserts this on every row: `assert not [p for p in rel if link[p[1]] >= 9 and p[2] == 2]`.
4. y_j and x_j are real vertices: the neighbours of w_j after s_{j−1} and before s_j. They carry the domain letters, and their adjacencies inside the window (to w_j, to s_{j−1} or s_j, and to ring 3) are exact.

For kills (§7), the drawn middle is held at 9+, so it is never a host. This is automatic: the member with middle = 9+ is the minimal member at every 9+ site. The apexes s_i may be 9+ as well; they are never hubs and their fans are ring 3.

## 7. Kills by RSST appearance

**Host graph of a filling.**
- The hosts are u, w_i, s_i and the privates whose letter is exact (≤ 8). Each host t has the letter set {letter}.
- Not hosts: 9+ vertices, ring 3, the 9+ middles, and u when d ≥ 9.
- The edges of the host graph are the window edges (faces in §2) between hosts.

**Configuration graph** (rsst_rows.prep, applied to each of the 633 records of unavoidable.conf):
- The ring is vertices 1..r. The interior is r+1..n, with deg = |adj|.
- E is the set of interior–interior edges.
- The faces are the interior triangles, read off consecutive pairs of each interior rotation.

**Containment** (rsst_rows.contains): an injective map φ from the interior into the hosts such that:
- deg x is in the letter set of φ(x);
- x ~ y in E **iff** φ(x) ~ φ(y), so the image is induced;
- every interior face maps onto a triangle.

Ring vertices of the configuration are not mapped. This is the "relaxed" host rule of rsst_rows, extended from s_i to the privates. The argument is the same: the outer neighbours of a host are only ring vertices of K, which an RSST appearance does not constrain.

**Assumption H** (carried over from rsst_rows' docstring, where it is stated for {u, w, s}): in an internally 6-connected triangulation, the window has no edges or identifications beyond those drawn, so induced-ness may be checked on the window. Its extension to the privates is the same separating-cycle argument and has **not been re-proved here**. The Studio should check it.

**Kill models.** A filling is killed under:
- **K582** if some configuration with verdict D2 or C2cons is contained;
- **K633** if any of the 633 is contained.

The difference K633 \ K582 is reported as **proved-modulo-admissibility**: fillings killed only by one of the 51 "none" configurations (§1).

**Monotonicity.** Containment is monotone in the host assignment, meaning the set of (vertex, letter) pairs with letter ≤ 8. Turning a host into 9+ removes it. Turning a private from 9+ into an exact letter can only create containments. §8.2 relies on this.

## 8. Exhaustive evaluation

### 8.1 d = 7, 8 (as run): grouping by relevant privates

1. Collect the fits of §3.5 (`instances`).
2. The **relevant** privates are the union of the condition keys over all of these fits.
3. For each site, project its options onto the relevant privates. Options with the same projection form one **class**, whose size is its multiplicity.
4. A **group** is one class per site. There are G = Π_j #classes_j groups, and group g stands for Π_j |class_j(g)| fillings, an exact integer.
5. lo and hi are constant on a group, because the ledger reads only relevant privates. Evaluate every group once, with the irrelevant columns set to anything, for example 9.

The worst case in this run is G = 2,166,000 groups for 2,166,000 fillings (B: 7 5757777 5555755). The limit is GMAX = 4·10^6 groups; a larger row would be `not done`. No row reached it.

### 8.2 Kills on a group

The members of a group differ only in irrelevant letters. At each site, keep the **minimal** members: those whose host assignment on the irrelevant privates contains no other member's assignment. Where the domain allows it, this is the member with 9+ on the irrelevant privates.

By monotonicity (§7), the group is killed under a model **iff every combination of minimal members (one per site) contains a configuration of that model**. If there are more than CMAX = 64 combinations, the group is kept (not killed) and counted in `inexact_groups`. This is conservative. The count was 0 in every set run (§11).

### 8.3 d = 5, 6: same algorithm over all (link, apex) words

Each row is one (link, apex) word, taken up to rotation and reflection, with all privates in 5..9+. The run is the §8.1 grouping followed by §8.2 kills on the groups with hi > 0. Sizes:

| d | words | classes (rotation + reflection, about) |
|---|---|---|
| 5 | 5^10 ≈ 9.8 M | ≈ 1 M |
| 6 | 5^12 ≈ 244 M | ≈ 20 M |

That needs a compiled implementation. A safe prune runs first, per word: an upper bound hi⁺ = base + #{fits into u that are possible for some filling} − #{fits out of u that are sure for every filling}. Each fit is judged on its own, which is valid because every fit is a conjunction of intervals. If hi⁺ ≤ 0, the word passes without enumerating privates.

Two alternatives:
- Hub-u fits read every site, since n = d: subpart j tests w_{a+j}, the hat s_{a+j−1}, and the fans, which are the privates of w_{a+j}. They are conjunctions of per-site tests, so a cyclic DP over sites can carry a bitmask of the hub-u alternatives still alive. That is d·#parts(n = d) bits: 30 for d = 5, 84 for d = 6.
- The hub-w_i fits are local (§8.4), and could be run the same way.

The random fillings in §10.2 show positive hi at both degrees (up to 10 at d = 5, 16 at d = 6), so **kills are needed at d = 5 and d = 6**.

### 8.4 d ≥ 9: local sums, a max-plus closed walk, and a Karp tail

At d ≥ 9 u never sends, so the final charge is

charge = 10(6−d) + Σ_i c_i = 60 + Σ_i (c_i − 10),

where c_i is the number of fits at hub w_i with target u. Only parts whose third-spoke range contains 9+ can contribute: 6 parts with 5 subparts, 14 with 6, 28 with 7 and 9 with 8.

**Locality.** c_i reads only sites i−2..i+2. Fix the anchor so that S[a+2] = u. With rot(w_i) = u, w_{i−1}, s_{i−1}, p_i.1, …, p_i.k, s_i, w_{i+1}, the anchor is a = n−2, and the subparts j = 0, 1, 2, 3, 4, 5, …, n−1 sit on s_i, w_{i+1}, u, w_{i−1}, s_{i−1}, p_i.1, …, p_i.k. In detail:
- Hats: across u–w_{i+1} it is w_{i+2}; across w_{i−1}–u it is w_{i−2}; across s_i–w_{i+1} it is p_{i+1}.1 or s_{i+1}; across s_{i−1}–w_{i−1} it is p_{i−1}.last or s_{i−2}.
- Fans: of w_{i+1}, they are p_{i+1}.2.., s_{i+1}; of w_{i−1}, they are s_{i−2}, p_{i−1}.1...
- Fans of u are never read, since u is 9+.
- Every other read is ring 3, so OPEN.

Writing σ_j = (w_j, s_j, privates of w_j), c_i is a function of (w_{i−2}, s_{i−2}), σ_{i−1}, σ_i, σ_{i+1} and w_{i+2}.

**Exact maximum.** max Σ_i (c_i − 10) over cyclic words of length d is a maximum-weight closed walk of length d in the de Bruijn-type graph on windows (σ_{i−2}, …, σ_{i+1}). Project σ onto what neighbours actually read, and use the relevance grouping of §8.1 inside a site.

**Tail.** Let λ be the maximum cycle mean of (c − 10), computed with Karp's algorithm on the same graph (or on a cheaper upper-bounding graph). Then charge ≤ 60 + dλ. If λ < 0, every d > 60/(−λ) passes with no kills. Only 9 ≤ d ≤ 60/(−λ) need the exact walk.

A cheap upper-bounding graph has nodes (L_{i−2}, L_{i−1}, L_i, L_{i+1}), and each step appends L_{i+2} with weight c⁺(L_{i−2}..L_{i+2}) − 10. Here c⁺ is the maximum over all apexes and privates of the fits from w_i into u that are possible. The graph is small: 625 states and 3125 edges.

**Kills at d ≥ 9.** Run the walk DP for max hi first. Then backtrack the walks with hi > 0; they are few and highly structured. Test each one under §7 with u not a host. A walk that is killed is excluded, and the next-best walk is taken. This stays exact because a kill is a property of a whole filling.

**Computed here** (`code/fp_tail9.py` → `results/tail9.json`, and `code/fp_all5.py` → `results/all5_d9plus.json`):

- **c⁺ per hub.** c⁺ is computed exactly for every 5-letter link window (L_{i−2}..L_{i+2}, each 5..9+), maximising over all apexes and privates.
  - Windows are built for (L_i, L_{i±1}, s_{i−1}, s_i), which fixes every rotation the fits read. w_{i±2}, s_{i−2} and s_{i+1} are read only by range tests, so they are enumerated as variables together with the relevant privates, by interval breakpoint classes.
  - The maximum c⁺ by hub letter is 6 for 5, 6 for 6, 6 for 7, 4 for 8 and 0 for 9+. The same values hold for sure fits.
- **Karp.** λ = −4, so UB(d) ≤ 60 − 4d. The max-plus closed walk gives exactly **UB(d) = 60 − 4d** for d = 9..40: 24, 20, 16, 12, 8, 4 at d = 9..14, and 0 at d = 15.
- **The bound is attained.** At the all-5 filling (every link letter and every apex 5), every w_i sends 6 sure units into u, through drule1, drule1#2, drule2, drule2m, drule3 and drule3m. So lo = hi = 60 − 4d exactly.
- **Consequence.** With no kills, every d ≥ 15 passes and **d = 9..14 fail**. The no-kill maximum is exactly 60 − 4d.
  - The all-5 filling contains exactly one RSST configuration, 0.7322 (D2, proved), at every d = 9..15. So it is killed under both K582 and K633.
  - d = 9..14 need the joint walk DP with kills. The per-hub bound cannot settle them, because it is tight.
- **Random samples.** The random fillings of §10.2 reached hi = 4 at d = 9, −2 at d = 10 and −3 at d = 11. They only test the ledger and the matcher; they prove nothing.

## 9. Output per row

These are the fields of `results/fp_<SET>.json`; the `.tsv` file holds the scalar columns.

- **Row size:** `n_fill`, `n_groups`, `relevant` (count of relevant privates; `rel_8mid` counts the relevant 8-site middles), `n_inst` (fits touching u).
- **Domains only:** `lo_max`, `hi_max`, `argmax_lo`, `argmax_hi`, `fills_lo_pos`, `fills_hi_pos`, `groups_lo_pos`, `groups_hi_pos`.
- **K633:** `groups_hi_pos_killed`, `groups_hi_pos_kept`, `inexact_groups`, `lo_max_after`, `hi_max_after`, `argmax_lo_after`, `argmax_hi_after`, `fills_lo_pos_after`, `fills_hi_pos_after`. `None` means every filling was killed.
- **K582:** `groups_hi_pos_killed_proved`, `lo_max_after_proved`, `hi_max_after_proved`, `argmax_hi_after_proved`, `fills_hi_pos_after_proved`.
- `configs_used`: configuration → number of killed positive groups whose tested combinations contain it.
- `positives` (the first 400 groups with hi > 0): `filling`, `lo`, `hi`, `fills` (multiplicity), `killed`, `killed_proved`, `minimal_combinations`, `configs` = [[name, verdict], …].

## 10. Test vectors

### 10.1 d = 7 / 8 rows (`results/test_vectors.json`, from `code/fp_vectors.py`)

Each vector holds:
- the row summary;
- every fit touching u, as (part tag, hub, target, condition text, for example `p0.1=5 & p0.2=5`);
- for `argmax_lo`, `argmax_lo_after` and (where present) `argmax_hi_after_proved`: the full private letters, lo and hi, the fits that fire (sure or possible), and the RSST configurations contained.

<!--VECTORS-->
**A 7 7676766 6565665**: n_fill 9765625, groups 390625, relevant privates 8, fits touching u 15. Domains: lo_max 5, hi_max 5, 817 positive fillings. K633: hi_max 0. K582: hi_max 0.

- fits touching u: drule8m@w0→u [always]; drule9@w0→u [p0.2=5]; drule9m@w0→u [p0.1=5]; drule20m@w0→u [p0.1=5 & p0.2=5]; drule8m@w2→u [always]; drule9@w2→u [p2.2=5]; drule9m@w2→u [p2.1=5]; drule20m@w2→u [p2.1=5 & p2.2=5]; drule8m@w4→u [always]; drule9@w4→u [p4.2=5]; drule9m@w4→u [p4.1=5]; drule20m@w4→u [p4.1=5 & p4.2=5]; drule4'@w5→u [p6.1=5]; drule5@w5→u [p6.1<=6]; drule4'm@w6→u [p5.1=5]
- argmax_lo `x0=5,y0=5 p1=9 x2=5,y2=5 p3=9 x4=5,y4=5 p5=5 p6=5`: lo 5, hi 5. Fires: drule8m@w0→u, drule9@w0→u, drule9m@w0→u, drule20m@w0→u, drule8m@w2→u, drule9@w2→u, drule9m@w2→u, drule20m@w2→u, drule8m@w4→u, drule9@w4→u, drule9m@w4→u, drule20m@w4→u, drule4'@w5→u, drule5@w5→u, drule4'm@w6→u. Contains: 2.7566 (D2), 122.363 (D2), 122.368 (C2cons), 3.1324817 (none), 126.469626 (D2), 497.1028 (C2cons)
- argmax_lo_after `x0=5,y0=5 p1=9 x2=5,y2=5 p3=9 x4=5,y4=6 p5=6 p6=7`: lo 0, hi 0. Fires: drule8m@w0→u, drule9@w0→u, drule9m@w0→u, drule20m@w0→u, drule8m@w2→u, drule9@w2→u, drule9m@w2→u, drule20m@w2→u, drule8m@w4→u, drule9@w4→u. Contains: 497.1028 (C2cons)
- argmax_hi_after_proved `x0=5,y0=5 p1=9 x2=5,y2=5 p3=9 x4=5,y4=6 p5=6 p6=7`: lo 0, hi 0. Fires: drule8m@w0→u, drule9@w0→u, drule9m@w0→u, drule20m@w0→u, drule8m@w2→u, drule9@w2→u, drule9m@w2→u, drule20m@w2→u, drule8m@w4→u, drule9@w4→u. Contains: 497.1028 (C2cons)

**A 7 5557557 5777977**: n_fill 500, groups 1, relevant privates 0, fits touching u 26. Domains: lo_max 0, hi_max 0, 0 positive fillings. K633: hi_max 0. K582: hi_max 0.

- fits touching u: drule8@u→w3 [always]; drule8m@u→w3 [always]; drule9@u→w3 [always]; drule10'@u→w3 [always]; drule8@u→w6 [always]; drule8m@u→w6 [always]; drule9m@u→w6 [always]; drule10'@u→w6 [always]; drule1@w0→u [always]; drule1#2@w0→u [always]; drule2@w0→u [always]; drule3@w0→u [always]; drule1@w1→u [always]; drule1#2@w1→u [always]; drule2@w1→u [always]; drule2m@w1→u [always]; drule3m@w1→u [always]; drule1@w2→u [always]; drule1#2@w2→u [always]; drule2m@w2→u [always]; drule1@w4→u [always]; drule1#2@w4→u [always]; drule2@w4→u [always]; drule1@w5→u [always]; drule1#2@w5→u [always]; drule2m@w5→u [always]
- argmax_lo `x3=9,y3=9 x6=9,y6=9`: lo 0, hi 0. Fires: drule8@u→w3, drule8m@u→w3, drule9@u→w3, drule10'@u→w3, drule8@u→w6, drule8m@u→w6, drule9m@u→w6, drule10'@u→w6, drule1@w0→u, drule1#2@w0→u, drule2@w0→u, drule3@w0→u, drule1@w1→u, drule1#2@w1→u, drule2@w1→u, drule2m@w1→u, drule3m@w1→u, drule1@w2→u, drule1#2@w2→u, drule2m@w2→u, drule1@w4→u, drule1#2@w4→u, drule2@w4→u, drule1@w5→u, drule1#2@w5→u, drule2m@w5→u. Contains: no configuration
- argmax_lo_after `x3=9,y3=9 x6=9,y6=9`: lo 0, hi 0. Fires: drule8@u→w3, drule8m@u→w3, drule9@u→w3, drule10'@u→w3, drule8@u→w6, drule8m@u→w6, drule9m@u→w6, drule10'@u→w6, drule1@w0→u, drule1#2@w0→u, drule2@w0→u, drule3@w0→u, drule1@w1→u, drule1#2@w1→u, drule2@w1→u, drule2m@w1→u, drule3m@w1→u, drule1@w2→u, drule1#2@w2→u, drule2m@w2→u, drule1@w4→u, drule1#2@w4→u, drule2@w4→u, drule1@w5→u, drule1#2@w5→u, drule2m@w5→u. Contains: no configuration
- argmax_hi_after_proved `x3=9,y3=9 x6=9,y6=9`: lo 0, hi 0. Fires: drule8@u→w3, drule8m@u→w3, drule9@u→w3, drule10'@u→w3, drule8@u→w6, drule8m@u→w6, drule9m@u→w6, drule10'@u→w6, drule1@w0→u, drule1#2@w0→u, drule2@w0→u, drule3@w0→u, drule1@w1→u, drule1#2@w1→u, drule2@w1→u, drule2m@w1→u, drule3m@w1→u, drule1@w2→u, drule1#2@w2→u, drule2m@w2→u, drule1@w4→u, drule1#2@w4→u, drule2@w4→u, drule1@w5→u, drule1#2@w5→u, drule2m@w5→u. Contains: no configuration

**A 8 55556859 58576556**: n_fill 62500, groups 1, relevant privates 0, fits touching u 22. Domains: lo_max 0, hi_max 0, 0 positive fillings. K633: hi_max 0. K582: hi_max 0.

- fits touching u: drule29m@u→w7 [always]; drule1@w0→u [always]; drule1#2@w0→u [always]; drule2@w0→u [always]; drule3@w0→u [always]; drule1@w1→u [always]; drule1#2@w1→u [always]; drule2@w1→u [always]; drule2m@w1→u [always]; drule3m@w1→u [always]; drule1@w2→u [always]; drule1#2@w2→u [always]; drule2@w2→u [always]; drule2m@w2→u [always]; drule3@w2→u [always]; drule1@w3→u [always]; drule1#2@w3→u [always]; drule2m@w3→u [always]; drule3m@w3→u [always]; drule2'm@w4→u [always]; drule1@w6→u [always]; drule1#2@w6→u [always]
- argmax_lo `p4=9 x5=9,m5=9,y5=9 x7=9,y7=9`: lo 0, hi 0. Fires: drule29m@u→w7, drule1@w0→u, drule1#2@w0→u, drule2@w0→u, drule3@w0→u, drule1@w1→u, drule1#2@w1→u, drule2@w1→u, drule2m@w1→u, drule3m@w1→u, drule1@w2→u, drule1#2@w2→u, drule2@w2→u, drule2m@w2→u, drule3@w2→u, drule1@w3→u, drule1#2@w3→u, drule2m@w3→u, drule3m@w3→u, drule2'm@w4→u, drule1@w6→u, drule1#2@w6→u. Contains: no configuration
- argmax_lo_after `p4=9 x5=9,m5=9,y5=9 x7=9,y7=9`: lo 0, hi 0. Fires: drule29m@u→w7, drule1@w0→u, drule1#2@w0→u, drule2@w0→u, drule3@w0→u, drule1@w1→u, drule1#2@w1→u, drule2@w1→u, drule2m@w1→u, drule3m@w1→u, drule1@w2→u, drule1#2@w2→u, drule2@w2→u, drule2m@w2→u, drule3@w2→u, drule1@w3→u, drule1#2@w3→u, drule2m@w3→u, drule3m@w3→u, drule2'm@w4→u, drule1@w6→u, drule1#2@w6→u. Contains: no configuration
- argmax_hi_after_proved `p4=9 x5=9,m5=9,y5=9 x7=9,y7=9`: lo 0, hi 0. Fires: drule29m@u→w7, drule1@w0→u, drule1#2@w0→u, drule2@w0→u, drule3@w0→u, drule1@w1→u, drule1#2@w1→u, drule2@w1→u, drule2m@w1→u, drule3m@w1→u, drule1@w2→u, drule1#2@w2→u, drule2@w2→u, drule2m@w2→u, drule3@w2→u, drule1@w3→u, drule1#2@w3→u, drule2m@w3→u, drule3m@w3→u, drule2'm@w4→u, drule1@w6→u, drule1#2@w6→u. Contains: no configuration

**A 8 55556858 58576557**: n_fill 62500, groups 25, relevant privates 2, fits touching u 23. Domains: lo_max 1, hi_max 1, 5 positive fillings. K633: hi_max 0. K582: hi_max 0.

- fits touching u: drule29m@u→w7 [always]; drule1@w0→u [always]; drule1#2@w0→u [always]; drule2@w0→u [always]; drule3@w0→u [always]; drule1@w1→u [always]; drule1#2@w1→u [always]; drule2@w1→u [always]; drule2m@w1→u [always]; drule3m@w1→u [always]; drule1@w2→u [always]; drule1#2@w2→u [always]; drule2@w2→u [always]; drule2m@w2→u [always]; drule3@w2→u [always]; drule1@w3→u [always]; drule1#2@w3→u [always]; drule2m@w3→u [always]; drule3m@w3→u [always]; drule2'm@w4→u [always]; drule1@w6→u [always]; drule1#2@w6→u [always]; drule29m@w7→u [p7.1=5 & p7.2=5]
- argmax_lo `p4=9 x5=9,m5=9,y5=9 x7=9,m7=5,y7=5`: lo 1, hi 1. Fires: drule29m@u→w7, drule1@w0→u, drule1#2@w0→u, drule2@w0→u, drule3@w0→u, drule1@w1→u, drule1#2@w1→u, drule2@w1→u, drule2m@w1→u, drule3m@w1→u, drule1@w2→u, drule1#2@w2→u, drule2@w2→u, drule2m@w2→u, drule3@w2→u, drule1@w3→u, drule1#2@w3→u, drule2m@w3→u, drule3m@w3→u, drule2'm@w4→u, drule1@w6→u, drule1#2@w6→u, drule29m@w7→u. Contains: 7322.165 (D2)
- argmax_lo_after `p4=9 x5=9,m5=9,y5=9 x7=9,m7=6,y7=5`: lo 0, hi 0. Fires: drule29m@u→w7, drule1@w0→u, drule1#2@w0→u, drule2@w0→u, drule3@w0→u, drule1@w1→u, drule1#2@w1→u, drule2@w1→u, drule2m@w1→u, drule3m@w1→u, drule1@w2→u, drule1#2@w2→u, drule2@w2→u, drule2m@w2→u, drule3@w2→u, drule1@w3→u, drule1#2@w3→u, drule2m@w3→u, drule3m@w3→u, drule2'm@w4→u, drule1@w6→u, drule1#2@w6→u. Contains: 7322.165 (D2)
- argmax_hi_after_proved `p4=9 x5=9,m5=9,y5=9 x7=9,m7=6,y7=5`: lo 0, hi 0. Fires: drule29m@u→w7, drule1@w0→u, drule1#2@w0→u, drule2@w0→u, drule3@w0→u, drule1@w1→u, drule1#2@w1→u, drule2@w1→u, drule2m@w1→u, drule3m@w1→u, drule1@w2→u, drule1#2@w2→u, drule2@w2→u, drule2m@w2→u, drule3@w2→u, drule1@w3→u, drule1#2@w3→u, drule2m@w3→u, drule3m@w3→u, drule2'm@w4→u, drule1@w6→u, drule1#2@w6→u. Contains: 7322.165 (D2)

**T 8 56765767 56655555**: n_fill 640000, groups 40000, relevant privates 7, fits touching u 26. Domains: lo_max 2, hi_max 2, 87 positive fillings. K633: hi_max 0. K582: hi_max 1.

- fits touching u: drule1@w0→u [always]; drule1#2@w0→u [always]; drule3@w0→u [always]; drule2'm@w1→u [always]; drule3'm@w1→u [always]; drule4m@w1→u [always]; drule9@w2→u [p2.2=5]; drule9m@w2→u [p2.1=5]; drule2'@w3→u [always]; drule3'@w3→u [always]; drule4@w3→u [always]; drule1@w4→u [always]; drule1#2@w4→u [always]; drule3m@w4→u [always]; drule8@w5→u [always]; drule8m@w5→u [always]; drule9@w5→u [p5.2=5]; drule9m@w5→u [p5.1=5]; drule14@w5→u [p6.1=5]; drule17@w5→u [p5.1>=7 & p5.2=5 & p6.1=6]; drule8@w7→u [always]; drule8m@w7→u [always]; drule9@w7→u [p7.2=5]; drule9m@w7→u [p7.1=5]; drule14m@w7→u [p6.1=5]; drule17m@w7→u [p6.1=6 & p7.1=5 & p7.2>=7]
- argmax_lo `p1=9 x2=5,y2=5 p3=9 x5=5,y5=7 p6=6 x7=7,y7=5`: lo 2, hi 2. Fires: drule1@w0→u, drule1#2@w0→u, drule3@w0→u, drule2'm@w1→u, drule3'm@w1→u, drule4m@w1→u, drule9@w2→u, drule9m@w2→u, drule2'@w3→u, drule3'@w3→u, drule4@w3→u, drule1@w4→u, drule1#2@w4→u, drule3m@w4→u, drule8@w5→u, drule8m@w5→u, drule9@w5→u, drule17@w5→u, drule8@w7→u, drule8m@w7→u, drule9m@w7→u, drule17m@w7→u. Contains: 2.126 (none), 3.3700802 (C2cons)
- argmax_lo_after `p1=9 x2=5,y2=5 p3=9 x5=5,y5=6 p6=6 x7=6,y7=5`: lo 0, hi 0. Fires: drule1@w0→u, drule1#2@w0→u, drule3@w0→u, drule2'm@w1→u, drule3'm@w1→u, drule4m@w1→u, drule9@w2→u, drule9m@w2→u, drule2'@w3→u, drule3'@w3→u, drule4@w3→u, drule1@w4→u, drule1#2@w4→u, drule3m@w4→u, drule8@w5→u, drule8m@w5→u, drule9@w5→u, drule8@w7→u, drule8m@w7→u, drule9m@w7→u. Contains: 2.126 (none), 122.126 (C2cons), 3.3700802 (C2cons)
- argmax_hi_after_proved `p1=9 x2=5,y2=6 p3=9 x5=5,y5=7 p6=6 x7=7,y7=5`: lo 1, hi 1. Fires: drule1@w0→u, drule1#2@w0→u, drule3@w0→u, drule2'm@w1→u, drule3'm@w1→u, drule4m@w1→u, drule9@w2→u, drule2'@w3→u, drule3'@w3→u, drule4@w3→u, drule1@w4→u, drule1#2@w4→u, drule3m@w4→u, drule8@w5→u, drule8m@w5→u, drule9@w5→u, drule17@w5→u, drule8@w7→u, drule8m@w7→u, drule9m@w7→u, drule17m@w7→u. Contains: 2.126 (none)

**C 7 5566776 5666657**: n_fill 14400, groups 960, relevant privates 5, fits touching u 23. Domains: lo_max 1, hi_max 1, 240 positive fillings. K633: hi_max 0. K582: hi_max 0.

- fits touching u: drule9@u→w4 [always]; drule8m@u→w5 [always]; drule9m@u→w5 [always]; drule1@w0→u [always]; drule1#2@w0→u [always]; drule2@w0→u [always]; drule3@w0→u [always]; drule1@w1→u [always]; drule1#2@w1→u [always]; drule2m@w1→u [always]; drule3m@w1→u [always]; drule2'm@w2→u [always]; drule4m@w2→u [always]; drule4'@w2→u [p3.1=5]; drule6m@w2→u [always]; drule4'm@w3→u [p2.1=5]; drule7m@w3→u [p2.1=6]; drule9m@w4→u [p4.1=5]; drule8@w5→u [always]; drule9@w5→u [p5.2=5]; drule21@w5→u [p5.1=5 & p5.2=5]; drule22@w5→u [p5.1=5 & p5.2=6]; drule2'@w6→u [always]
- argmax_lo `p2=7 p3=6 x4=9,y4=6 x5=6,y5=5 p6=9`: lo 1, hi 1. Fires: drule9@u→w4, drule8m@u→w5, drule9m@u→w5, drule1@w0→u, drule1#2@w0→u, drule2@w0→u, drule3@w0→u, drule1@w1→u, drule1#2@w1→u, drule2m@w1→u, drule3m@w1→u, drule2'm@w2→u, drule4m@w2→u, drule6m@w2→u, drule8@w5→u, drule22@w5→u, drule2'@w6→u. Contains: 126.61682 (C2cons)
- argmax_lo_after `p2=7 p3=6 x4=9,y4=6 x5=6,y5=6 p6=9`: lo 0, hi 0. Fires: drule9@u→w4, drule8m@u→w5, drule9m@u→w5, drule1@w0→u, drule1#2@w0→u, drule2@w0→u, drule3@w0→u, drule1@w1→u, drule1#2@w1→u, drule2m@w1→u, drule3m@w1→u, drule2'm@w2→u, drule4m@w2→u, drule6m@w2→u, drule8@w5→u, drule2'@w6→u. Contains: no configuration
- argmax_hi_after_proved `p2=7 p3=6 x4=9,y4=6 x5=6,y5=6 p6=9`: lo 0, hi 0. Fires: drule9@u→w4, drule8m@u→w5, drule9m@u→w5, drule1@w0→u, drule1#2@w0→u, drule2@w0→u, drule3@w0→u, drule1@w1→u, drule1#2@w1→u, drule2m@w1→u, drule3m@w1→u, drule2'm@w2→u, drule4m@w2→u, drule6m@w2→u, drule8@w5→u, drule2'@w6→u. Contains: no configuration

**B 7 7676666 6656565**: n_fill 1250000, groups 250000, relevant privates 8, fits touching u 20. Domains: lo_max 6, hi_max 6, 17376 positive fillings. K633: hi_max 0. K582: hi_max 0.

- fits touching u: drule8m@w0→u [always]; drule9@w0→u [p0.2=5]; drule9m@w0→u [p0.1=5]; drule20m@w0→u [p0.1=5 & p0.2=5]; drule8@w2→u [always]; drule9@w2→u [p2.2=5]; drule9m@w2→u [p2.1=5]; drule20@w2→u [p2.1=5 & p2.2=5]; drule4'@w3→u [p4.1=5]; drule5@w3→u [p4.1<=6]; drule3'@w4→u [always]; drule4'@w4→u [p5.1=5]; drule4'm@w4→u [p3.1=5]; drule5m@w4→u [p3.1<=6]; drule3'm@w5→u [always]; drule4'@w5→u [p6.1=5]; drule4'm@w5→u [p4.1=5]; drule5@w5→u [p6.1<=6]; drule4'm@w6→u [p5.1=5]; drule5m@w6→u [p5.1<=6]
- argmax_lo `x0=5,y0=6 p1=9 x2=6,y2=5 p3=5 p4=5 p5=5 p6=5`: lo 6, hi 6. Fires: drule8m@w0→u, drule9@w0→u, drule8@w2→u, drule9m@w2→u, drule4'@w3→u, drule5@w3→u, drule3'@w4→u, drule4'@w4→u, drule4'm@w4→u, drule5m@w4→u, drule3'm@w5→u, drule4'@w5→u, drule4'm@w5→u, drule5@w5→u, drule4'm@w6→u, drule5m@w6→u. Contains: 0.453962 (D2), 2.7566 (D2), 3.1324806 (none), 126.363 (C2cons), 126.469626 (D2)
- argmax_lo_after `x0=5,y0=6 p1=9 x2=6,y2=5 p3=5 p4=6 p5=6 p6=7`: lo 0, hi 0. Fires: drule8m@w0→u, drule9@w0→u, drule8@w2→u, drule9m@w2→u, drule5@w3→u, drule3'@w4→u, drule4'm@w4→u, drule5m@w4→u, drule3'm@w5→u, drule5m@w6→u. Contains: 2.22086 (D2), 126.363 (C2cons), 126.469626 (D2)
- argmax_hi_after_proved `x0=5,y0=6 p1=9 x2=6,y2=5 p3=5 p4=6 p5=6 p6=7`: lo 0, hi 0. Fires: drule8m@w0→u, drule9@w0→u, drule8@w2→u, drule9m@w2→u, drule5@w3→u, drule3'@w4→u, drule4'm@w4→u, drule5m@w4→u, drule3'm@w5→u, drule5m@w6→u. Contains: 2.22086 (D2), 126.363 (C2cons), 126.469626 (D2)

**B 8 76576756 65555556**: n_fill 640000, groups 40000, relevant privates 7, fits touching u 26. Domains: lo_max 2, hi_max 2, 87 positive fillings. K633: hi_max 0. K582: hi_max 1.

- fits touching u: drule9@w0→u [p0.2=5]; drule9m@w0→u [p0.1=5]; drule2'@w1→u [always]; drule3'@w1→u [always]; drule4@w1→u [always]; drule1@w2→u [always]; drule1#2@w2→u [always]; drule3m@w2→u [always]; drule8@w3→u [always]; drule8m@w3→u [always]; drule9@w3→u [p3.2=5]; drule9m@w3→u [p3.1=5]; drule14@w3→u [p4.1=5]; drule17@w3→u [p3.1>=7 & p3.2=5 & p4.1=6]; drule8@w5→u [always]; drule8m@w5→u [always]; drule9@w5→u [p5.2=5]; drule9m@w5→u [p5.1=5]; drule14m@w5→u [p4.1=5]; drule17m@w5→u [p4.1=6 & p5.1=5 & p5.2>=7]; drule1@w6→u [always]; drule1#2@w6→u [always]; drule3@w6→u [always]; drule2'm@w7→u [always]; drule3'm@w7→u [always]; drule4m@w7→u [always]
- argmax_lo `x0=5,y0=5 p1=9 x3=5,y3=7 p4=6 x5=7,y5=5 p7=9`: lo 2, hi 2. Fires: drule9@w0→u, drule9m@w0→u, drule2'@w1→u, drule3'@w1→u, drule4@w1→u, drule1@w2→u, drule1#2@w2→u, drule3m@w2→u, drule8@w3→u, drule8m@w3→u, drule9@w3→u, drule17@w3→u, drule8@w5→u, drule8m@w5→u, drule9m@w5→u, drule17m@w5→u, drule1@w6→u, drule1#2@w6→u, drule3@w6→u, drule2'm@w7→u, drule3'm@w7→u, drule4m@w7→u. Contains: 2.126 (none), 3.3700802 (C2cons)
- argmax_lo_after `x0=5,y0=5 p1=9 x3=5,y3=6 p4=6 x5=6,y5=5 p7=9`: lo 0, hi 0. Fires: drule9@w0→u, drule9m@w0→u, drule2'@w1→u, drule3'@w1→u, drule4@w1→u, drule1@w2→u, drule1#2@w2→u, drule3m@w2→u, drule8@w3→u, drule8m@w3→u, drule9@w3→u, drule8@w5→u, drule8m@w5→u, drule9m@w5→u, drule1@w6→u, drule1#2@w6→u, drule3@w6→u, drule2'm@w7→u, drule3'm@w7→u, drule4m@w7→u. Contains: 2.126 (none), 122.126 (C2cons), 3.3700802 (C2cons)
- argmax_hi_after_proved `x0=5,y0=6 p1=9 x3=5,y3=7 p4=6 x5=7,y5=5 p7=9`: lo 1, hi 1. Fires: drule9@w0→u, drule2'@w1→u, drule3'@w1→u, drule4@w1→u, drule1@w2→u, drule1#2@w2→u, drule3m@w2→u, drule8@w3→u, drule8m@w3→u, drule9@w3→u, drule17@w3→u, drule8@w5→u, drule8m@w5→u, drule9m@w5→u, drule17m@w5→u, drule1@w6→u, drule1#2@w6→u, drule3@w6→u, drule2'm@w7→u, drule3'm@w7→u, drule4m@w7→u. Contains: 2.126 (none)
<!--/VECTORS-->

### 10.2 Fixed fillings at d = 5, 6, 9, 10, 11 (`results/test_vectors_ext.json`, from `code/fp_vectors_ext.py`, seed 20261110, 120 random 2-balls per degree)

Per degree the file keeps the filling with the largest hi, the one with the smallest lo, the two with the most fits, and the largest-hi filling that contains no configuration. Each comes with its privates, lo, hi, the fits that fire, and the configurations contained (u is not a host at d ≥ 9). These vectors test the ledger and the matcher only. They prove nothing about maxima.

<!--EXT-->
| d | why | link | apexes | privates (letter by p_i.k in order) | lo | hi | fits fired | configs contained |
|---|---|---|---|---|---|---|---|---|
| 5 | max_hi | 55555 | 69757 | - | 10 | 10 | 0 | 0.7322, 122.363 |
| 5 | min_lo | 65977 | 57659 | p0.1=6 p2.1=7 p2.2=9 p2.3=7 p3.1=6 p3.2=7 p4.1=5 p4.2=6 | 0 | 0 | 10 | 2.122 |
| 5 | most_fits_1 | 65977 | 57659 | p0.1=6 p2.1=7 p2.2=9 p2.3=7 p3.1=6 p3.2=7 p4.1=5 p4.2=6 | 0 | 0 | 10 | 2.122 |
| 5 | most_fits_2 | 98659 | 75555 | p0.1=6 p0.2=9 p0.3=8 p1.1=5 p1.2=5 p1.3=6 p2.1=6 p4.1=5 p4.2=9 p4.3=5 | 0 | 0 | 10 | 2.122, 2.126, 7562.126 |
| 5 | max_hi_no_config | 57577 | 68976 | p1.1=6 p1.2=8 p3.1=5 p3.2=9 p4.1=6 p4.2=6 | 0 | 0 | 10 | - |
| 6 | max_hi | 556555 | 755955 | p2.1=8 | 16 | 16 | 20 | 0.7322, 2.122, 2.126, 0.453962 … |
| 6 | min_lo | 569558 | 566588 | p1.1=9 p2.1=5 p2.2=9 p2.3=5 p5.1=7 p5.2=5 p5.3=8 | 0 | 0 | 20 | 3.1306802 |
| 6 | most_fits_1 | 556595 | 565675 | p2.1=9 p4.1=5 p4.2=9 p4.3=7 | 8 | 8 | 22 | 0.7322, 2.122, 2.126, 3.1306802 … |
| 6 | most_fits_2 | 656555 | 585565 | p0.1=5 p2.1=9 | 13 | 13 | 21 | 0.7322, 2.122, 2.126, 0.453962 … |
| 6 | max_hi_no_config | 685866 | 666599 | p0.1=8 p1.1=6 p1.2=6 p1.3=6 p3.1=6 p3.2=5 p3.3=9 p4.1=8 p5.1=5 | 0 | 0 | 4 | - |
| 9 | max_hi | 555576655 | 558855855 | p4.1=6 p4.2=9 p5.1=9 p6.1=6 | 4 | 4 | 34 | 0.7322 |
| 9 | min_lo | 998676976 | 779878658 | p0.1=6 p0.2=9 p0.3=5 p1.1=7 p1.2=9 p1.3=5 p2.1=7 p2.2=7 p2.3=5 p3.1=7 p4.1=6 p4.2=9 p5.1=9 p6.1=5 p6.2=9 p6.3=6 p7.1=7 p7.2=8 p8.1=6 | -29 | -29 | 1 | - |
| 9 | most_fits_1 | 555576655 | 558855855 | p4.1=6 p4.2=9 p5.1=9 p6.1=6 | 4 | 4 | 34 | 0.7322 |
| 9 | most_fits_2 | 566565555 | 868565986 | p1.1=6 p2.1=6 p4.1=5 | 0 | 0 | 30 | 2.122, 2.126 |
| 9 | max_hi_no_config | 566555755 | 767589658 | p1.1=6 p2.1=7 p6.1=6 p6.2=8 | -3 | -3 | 27 | - |
| 10 | max_hi | 8555555655 | 6895577659 | p0.1=6 p0.2=8 p0.3=5 p7.1=8 | -2 | -2 | 38 | 0.7322 |
| 10 | min_lo | 5878989667 | 5886695895 | p1.1=6 p1.2=9 p1.3=5 p2.1=8 p2.2=8 p3.1=5 p3.2=5 p3.3=6 p4.1=5 p4.2=9 p4.3=6 p5.1=7 p5.2=6 p5.3=6 p6.1=7 p6.2=9 p6.3=6 p7.1=7 p8.1=6 p9.1=6 p9.2=7 | -37 | -37 | 3 | - |
| 10 | most_fits_1 | 8555555655 | 6895577659 | p0.1=6 p0.2=8 p0.3=5 p7.1=8 | -2 | -2 | 38 | 0.7322 |
| 10 | most_fits_2 | 6855556555 | 5585595586 | p0.1=5 p1.1=5 p1.2=7 p1.3=5 p6.1=8 | -4 | -4 | 36 | 0.7322, 2.126 |
| 10 | max_hi_no_config | 5559576655 | 9576755886 | p3.1=5 p3.2=9 p3.3=5 p5.1=6 p5.2=6 p6.1=8 p7.1=9 | -14 | -14 | 26 | - |
| 11 | max_hi | 55556555655 | 66755556777 | p4.1=6 p8.1=6 | -3 | -3 | 47 | 0.7322, 2.126, 0.453962, 122.363 |
| 11 | min_lo | 97588866886 | 65966685566 | p0.1=7 p0.2=9 p0.3=6 p1.1=5 p1.2=7 p3.1=6 p3.2=8 p3.3=9 p4.1=9 p4.2=7 p4.3=7 p5.1=8 p5.2=6 p5.3=5 p6.1=6 p7.1=5 p8.1=6 p8.2=5 p8.3=6 p9.1=5 p9.2=9 p9.3=8 p10.1=6 | -47 | -47 | 3 | 7562.126 |
| 11 | most_fits_1 | 55556555655 | 66755556777 | p4.1=6 p8.1=6 | -3 | -3 | 47 | 0.7322, 2.126, 0.453962, 122.363 |
| 11 | most_fits_2 | 65555855555 | 69555697689 | p0.1=5 p5.1=9 p5.2=8 p5.3=9 | -12 | -12 | 38 | 0.7322, 2.126 |
| 11 | max_hi_no_config | 95655596555 | 78975757856 | p0.1=5 p0.2=9 p0.3=6 p2.1=6 p6.1=5 p6.2=9 p6.3=8 p7.1=5 | -21 | -21 | 29 | - |

**All-5 fillings at d ≥ 9** (`results/all5_d9plus.json`): d=9 lo=hi=24 (54 fits, contains 0.7322); d=10 lo=hi=20 (60 fits, contains 0.7322); d=11 lo=hi=16 (66 fits, contains 0.7322); d=12 lo=hi=12 (72 fits, contains 0.7322); d=13 lo=hi=8 (78 fits, contains 0.7322); d=14 lo=hi=4 (84 fits, contains 0.7322); d=15 lo=hi=0 (90 fits, contains 0.7322)
<!--/EXT-->

## 11. Results: the d = 7 / 8 run (rsst_closure §3(b) sets and the ST-102 tneg list)

**Sets.**
- A: binder, 162 rows.
- B: GS16, 495 rows.
- C: pos6-alive, 281 rows.
- T: the ST-102 tneg list, 305 labels (48 at d7, 257 at d8), from `round6/W17-studio-kstar/from_studio/sol_repK2MW_04__K3l5n_k268/` (tneg md5 4a181f67).

All 71 parts are used as written, with the K3gB5n per-filling domains. The counts are in RSST units. "+rows" means rows with a positive filling.

The columns:
- **dom** = domains only;
- **582** = domains + proved configurations;
- **mod-adm** = rows positive under K582 but not under K633, that is, killed only by a configuration that is proved-modulo-admissibility;
- **633** = domains + all configurations.

<!--TABLES-->
| set | d | rows | not done | fillings | +rows dom | max lo | max hi | +fills dom | +rows 582 | max 582 | +fills 582 | rows mod-adm | +rows 633 | +fills 633 | inexact |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| A | 7 | 56 | 0 | 43251521 | 13 | 5 | 5 | 45064 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| A | 8 | 106 | 0 | 2742825 | 25 | 1 | 1 | 220 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| A | all | 162 | 0 | 45994346 | 38 | 5 | 5 | 45284 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| B | 7 | 369 | 0 | 409765956 | 81 | 6 | 6 | 125985 | 3 | 1 | 656 | 3 | 0 | 0 | 0 |
| B | 8 | 126 | 0 | 14491941 | 17 | 6 | 6 | 31330 | 1 | 1 | 72 | 1 | 0 | 0 | 0 |
| B | all | 495 | 0 | 424257897 | 98 | 6 | 6 | 157315 | 4 | 1 | 728 | 4 | 0 | 0 | 0 |
| C | 7 | 281 | 0 | 27137688 | 25 | 1 | 1 | 9672 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| C | 8 | 0 | 0 | 0 | 0 | - | - | 0 | 0 | - | 0 | 0 | 0 | 0 | 0 |
| C | all | 281 | 0 | 27137688 | 25 | 1 | 1 | 9672 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| T | 7 | 48 | 0 | 33697870 | 10 | 5 | 5 | 10542 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| T | 8 | 257 | 0 | 10464995 | 25 | 2 | 2 | 207 | 1 | 1 | 72 | 1 | 0 | 0 | 0 |
| T | all | 305 | 0 | 44162865 | 35 | 5 | 5 | 10749 | 1 | 1 | 72 | 1 | 0 | 0 | 0 |

configurations used to cover positive fillings: 98 (90 proved D2/C2cons, 8 none = proved-modulo-admissibility)

**Rows that need a proved-modulo-admissibility configuration** (positive under K582, killed under K633): 5.

| set | row | max hi (dom) | max hi after K582 | argmax after K582 | fillings killed only by a none configuration |
|---|---|---|---|---|---|
| B | 8 76576756 65555556 | 2 | 1 | `x0=5,y0=6 p1=9 x3=5,y3=7 p4=6 x5=7,y5=5 p7=9` | 2.126:72 |
| B | 7 8557766 7565755 | 1 | 1 | `x0=9,m0=9,y0=9 x3=9,y3=5 x4=9,y4=6 p5=5 p6=6` | 124.1324817:320 2.126:80 |
| B | 7 8565766 5557657 | 1 | 1 | `x0=9,m0=9,y0=9 p2=9 x4=6,y4=9 p5=7 p6=6` | 128.1324802:192 |
| B | 7 8565766 5557656 | 1 | 1 | `x0=9,m0=9,y0=9 p2=9 x4=6,y4=9 p5=7 p6=7` | 128.1324802:144 |
| T | 8 56765767 56655555 | 2 | 1 | `p1=9 x2=5,y2=6 p3=9 x5=5,y5=7 p6=6 x7=7,y7=5` | 2.126:72 |

**Largest positive rows under the domains alone** (every one is killed under both K582 and K633 unless listed above; all rows are in `results/positive_rows.tsv`):

| set | row | fillings | max lo = max hi | argmax filling | positive fillings | top covering configurations (name:verdict:#fillings) |
|---|---|---|---|---|---|---|
| B | 7 7676666 6656565 | 1250000 | 6 | `x0=5,y0=6 p1=9 x2=6,y2=5 p3=5 p4=5 p5=5 p6=5` | 17376 | 126.469626:D2:220 126.363:C2cons:206 2.7566:D2:191 3.1324806:none:181 |
| B | 8 75766666 55565565 | 1562500 | 6 | `x0=5,y0=5 x2=5,y2=5 p3=5 p4=5 p5=6 p6=5 p7=5` | 15136 | 122.122:D2:400 123.442806:D2:364 3.1324817:none:317 122.363:D2:316 |
| A | 7 6676767 6565565 | 8593750 | 5 | `p0=5 p1=5 x2=5,y2=5 p3=9 x4=5,y4=7 p5=9 x6=5,y6=5` | 3606 | 2.7566:D2:400 122.363:D2:400 3.1324817:none:400 126.469626:D2:400 |
| A | 7 6767676 5655656 | 8593750 | 5 | `p0=5 x1=5,y1=5 p2=9 x3=5,y3=7 p4=9 x5=5,y5=5 p6=5` | 3606 | 122.363:D2:400 126.469626:D2:400 3.1324817:none:212 2.7566:D2:180 |
| A | 7 7676766 6565665 | 9765625 | 5 | `x0=5,y0=5 p1=9 x2=5,y2=5 p3=9 x4=5,y4=5 p5=5 p6=5` | 817 | 497.1028:C2cons:268 122.363:D2:244 126.469626:D2:244 3.1324817:none:172 |
| B | 7 7676766 6556565 | 8593750 | 5 | `x0=5,y0=5 p1=9 x2=5,y2=7 p3=9 x4=5,y4=5 p5=5 p6=5` | 3606 | 126.469626:D2:246 3.1324817:none:209 122.363:D2:206 497.1028:C2cons:195 |
| B | 8 75666675 65656557 | 200000 | 5 | `x0=5,y0=9 p2=6 p3=5 p4=5 p5=5 x6=6,y6=5` | 4600 | 7566.372:none:1164 2.22086:D2:992 0.453962:D2:744 2.7566:D2:744 |
| T | 7 6676767 6565565 | 8593750 | 5 | `p0=5 p1=5 x2=5,y2=5 p3=9 x4=5,y4=7 p5=9 x6=5,y6=5` | 3606 | 2.7566:D2:400 122.363:D2:400 3.1324817:none:400 126.469626:D2:400 |
| T | 7 6767676 5655656 | 8593750 | 5 | `p0=5 x1=5,y1=5 p2=9 x3=5,y3=7 p4=9 x5=5,y5=5 p6=5` | 3606 | 122.363:D2:400 126.469626:D2:400 3.1324817:none:212 2.7566:D2:180 |
| A | 7 7666676 6656666 | 1953125 | 4 | `x0=5,y0=5 p1=5 p2=5 p3=5 p4=5 x5=5,y5=5 p6=9` | 1601 | 0.453962:D2:362 2.7566:D2:256 3.1324806:none:256 122.368:C2cons:167 |
| B | 7 8666666 5656765 | 1953125 | 4 | `x0=9,m0=9,y0=9 p1=5 p2=5 p3=5 p4=5 p5=5 p6=5` | 172 | 2.7566:D2:152 0.453962:D2:144 3.1324806:none:131 2.22086:D2:62 |
| A | 7 7767666 6565655 | 6250000 | 3 | `x0=9,y0=5 x1=5,y1=9 p2=9 x3=6,y3=5 p4=5 p5=5 p6=6` | 31200 | 667.1028:C2cons:9600 2.7566:D2:5600 2.22086:D2:3200 2.126:none:2500 |

**Configurations that cover positive fillings:** 98 in all, 8 of them none (proved-modulo-admissibility). The 15 most used are listed here; the full list is `results/covering_configs.tsv`, with columns per set. A count is the number of positive fillings (group multiplicity) in which some tested minimal combination contains the configuration. It is taken over the positive groups stored per row, which are capped at 400; 19 rows reach the cap (A 5, B 12, T 2), so their counts are partial. The kill decisions use every group.

| configuration | verdict | positive fillings containing it (all sets) |
|---|---|---|
| 2.7566 | D2 | 34010 |
| 667.1028 | C2cons | 28536 |
| 2.22086 | D2 | 11076 |
| 7385.137 | C2cons | 10590 |
| 2.126 | none (mod-adm) | 10073 |
| 7365.363 | D2 | 10000 |
| 0.174369782 | D2 | 6408 |
| 196.9902 | D2 | 6375 |
| 7322.122 | D2 | 5510 |
| 7322.439320 | D2 | 5510 |
| 7322.442802 | D2 | 5510 |
| 219.1023 | D2 | 3920 |
| 126.469626 | D2 | 3910 |
| 482.1148 | C2cons | 3589 |
| 3.3686402 | C2cons | 3589 |
<!--/TABLES-->

**Findings (d = 7 / 8, exhaustive).** No row is `not done`, no domain is empty, and `inexact_groups` = 0 in every set. In every cell of the table, max lo = max hi.

- **Domains only.** 196 of 1,243 rows have positive fillings: A 38, B 98, C 25, T 35. That is 223,020 positive fillings out of 541.6 M.
  - The maxima are +6 RSST units (+0.6 ours), in B at both d7 and d8.
  - A, the binder set, agrees with the sampled REPORT §3(b): 13 of 56 rows positive at d7 and 25 at d8. The d8 count is now out of 106 rows, because the rows with a 9+ link letter are included exactly.
- **K633** (582 proved + 51 proved-modulo-admissibility). **Every filling of every row has final charge ≤ 0.** After kills the maximum is 0 in every set.
- **K582** (proved only). 5 rows keep positive fillings, each with max hi = +1 (+0.1 ours): B 4 rows (728 fillings) and T 1 row (72 fillings). Each is killed only by a configuration with verdict none:
  - 2.126: B 8 76576756 65555556 and T 8 56765767 56655555;
  - 124.1324817 and 2.126: B 7 8557766 7565755;
  - 128.1324802: B 7 8565766 5557657 and 5557656.
  - **So for the d7/d8 sets, the RSST fixed point rests on W6b's ring-merge admissibility for these 3 configurations** (2.126, 124.1324817, 128.1324802), and on nothing else.
- **d ≥ 9 (§8.4).** The no-kill maximum is exactly 60 − 4d. d ≥ 15 passes without kills. d = 9..14 need the joint DP with kills.


## 12. Flags and limits

- **Assumption H** (§7) is inherited, not re-proved, for the privates.
- **Counting convention.** n_fill counts an 8-site middle as 5 letters and a 9+ site middle as one 5-letter vertex. This changes no maximum and no positive/negative status.
- **Window and ring 3.** pubrules draws ring 3 with each private's degree taken as 8 when it lays out the ring-3 joints. That only decides *which* ring-3 vertex a read lands on. Every non-`*` read of ring 3 is OPEN whatever its shape, and the fan counts of u, w and s are their exact degrees, so the drawing does not affect lo or hi.
- **Kill side.** A group with more than 64 minimal combinations is kept (conservative); none occurred.
- **Scope.** This run checks u's own charge only, not the charges of the other vertices of the 2-ball, and it adds no LP or t terms.
