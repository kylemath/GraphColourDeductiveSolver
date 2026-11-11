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
- Not hosts: 9+ vertices, ring 3 and the 9+ middles. u is always a host, with its exact letter d, at every degree (erratum E1; the first version of this spec left u out at d ≥ 9).
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
**A 7 7676766 6565665**: n_fill 9765625, groups 390625, relevant privates 8, fits touching u 15. Domains: lo_max 5, hi_max 5, 20425 positive fillings. K633: hi_max 0. K582: hi_max 0.

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

**A 8 55556858 58576557**: n_fill 62500, groups 25, relevant privates 2, fits touching u 23. Domains: lo_max 1, hi_max 1, 2500 positive fillings. K633: hi_max 0. K582: hi_max 0.

- fits touching u: drule29m@u→w7 [always]; drule1@w0→u [always]; drule1#2@w0→u [always]; drule2@w0→u [always]; drule3@w0→u [always]; drule1@w1→u [always]; drule1#2@w1→u [always]; drule2@w1→u [always]; drule2m@w1→u [always]; drule3m@w1→u [always]; drule1@w2→u [always]; drule1#2@w2→u [always]; drule2@w2→u [always]; drule2m@w2→u [always]; drule3@w2→u [always]; drule1@w3→u [always]; drule1#2@w3→u [always]; drule2m@w3→u [always]; drule3m@w3→u [always]; drule2'm@w4→u [always]; drule1@w6→u [always]; drule1#2@w6→u [always]; drule29m@w7→u [p7.1=5 & p7.2=5]
- argmax_lo `p4=9 x5=9,m5=9,y5=9 x7=9,m7=5,y7=5`: lo 1, hi 1. Fires: drule29m@u→w7, drule1@w0→u, drule1#2@w0→u, drule2@w0→u, drule3@w0→u, drule1@w1→u, drule1#2@w1→u, drule2@w1→u, drule2m@w1→u, drule3m@w1→u, drule1@w2→u, drule1#2@w2→u, drule2@w2→u, drule2m@w2→u, drule3@w2→u, drule1@w3→u, drule1#2@w3→u, drule2m@w3→u, drule3m@w3→u, drule2'm@w4→u, drule1@w6→u, drule1#2@w6→u, drule29m@w7→u. Contains: 7322.165 (D2)
- argmax_lo_after `p4=9 x5=9,m5=9,y5=9 x7=9,m7=6,y7=5`: lo 0, hi 0. Fires: drule29m@u→w7, drule1@w0→u, drule1#2@w0→u, drule2@w0→u, drule3@w0→u, drule1@w1→u, drule1#2@w1→u, drule2@w1→u, drule2m@w1→u, drule3m@w1→u, drule1@w2→u, drule1#2@w2→u, drule2@w2→u, drule2m@w2→u, drule3@w2→u, drule1@w3→u, drule1#2@w3→u, drule2m@w3→u, drule3m@w3→u, drule2'm@w4→u, drule1@w6→u, drule1#2@w6→u. Contains: 7322.165 (D2)
- argmax_hi_after_proved `p4=9 x5=9,m5=9,y5=9 x7=9,m7=6,y7=5`: lo 0, hi 0. Fires: drule29m@u→w7, drule1@w0→u, drule1#2@w0→u, drule2@w0→u, drule3@w0→u, drule1@w1→u, drule1#2@w1→u, drule2@w1→u, drule2m@w1→u, drule3m@w1→u, drule1@w2→u, drule1#2@w2→u, drule2@w2→u, drule2m@w2→u, drule3@w2→u, drule1@w3→u, drule1#2@w3→u, drule2m@w3→u, drule3m@w3→u, drule2'm@w4→u, drule1@w6→u, drule1#2@w6→u. Contains: 7322.165 (D2)

**T 8 56765767 56655555**: n_fill 640000, groups 40000, relevant privates 7, fits touching u 26. Domains: lo_max 2, hi_max 2, 1392 positive fillings. K633: hi_max 0. K582: hi_max 1.

- fits touching u: drule1@w0→u [always]; drule1#2@w0→u [always]; drule3@w0→u [always]; drule2'm@w1→u [always]; drule3'm@w1→u [always]; drule4m@w1→u [always]; drule9@w2→u [p2.2=5]; drule9m@w2→u [p2.1=5]; drule2'@w3→u [always]; drule3'@w3→u [always]; drule4@w3→u [always]; drule1@w4→u [always]; drule1#2@w4→u [always]; drule3m@w4→u [always]; drule8@w5→u [always]; drule8m@w5→u [always]; drule9@w5→u [p5.2=5]; drule9m@w5→u [p5.1=5]; drule14@w5→u [p6.1=5]; drule17@w5→u [p5.1>=7 & p5.2=5 & p6.1=6]; drule8@w7→u [always]; drule8m@w7→u [always]; drule9@w7→u [p7.2=5]; drule9m@w7→u [p7.1=5]; drule14m@w7→u [p6.1=5]; drule17m@w7→u [p6.1=6 & p7.1=5 & p7.2>=7]
- argmax_lo `p1=9 x2=5,y2=5 p3=9 x5=5,y5=7 p6=6 x7=7,y7=5`: lo 2, hi 2. Fires: drule1@w0→u, drule1#2@w0→u, drule3@w0→u, drule2'm@w1→u, drule3'm@w1→u, drule4m@w1→u, drule9@w2→u, drule9m@w2→u, drule2'@w3→u, drule3'@w3→u, drule4@w3→u, drule1@w4→u, drule1#2@w4→u, drule3m@w4→u, drule8@w5→u, drule8m@w5→u, drule9@w5→u, drule17@w5→u, drule8@w7→u, drule8m@w7→u, drule9m@w7→u, drule17m@w7→u. Contains: 2.126 (none), 3.3700802 (C2cons)
- argmax_lo_after `p1=9 x2=5,y2=5 p3=9 x5=5,y5=6 p6=6 x7=6,y7=5`: lo 0, hi 0. Fires: drule1@w0→u, drule1#2@w0→u, drule3@w0→u, drule2'm@w1→u, drule3'm@w1→u, drule4m@w1→u, drule9@w2→u, drule9m@w2→u, drule2'@w3→u, drule3'@w3→u, drule4@w3→u, drule1@w4→u, drule1#2@w4→u, drule3m@w4→u, drule8@w5→u, drule8m@w5→u, drule9@w5→u, drule8@w7→u, drule8m@w7→u, drule9m@w7→u. Contains: 2.126 (none), 122.126 (C2cons), 3.3700802 (C2cons)
- argmax_hi_after_proved `p1=9 x2=5,y2=6 p3=9 x5=5,y5=7 p6=6 x7=7,y7=5`: lo 1, hi 1. Fires: drule1@w0→u, drule1#2@w0→u, drule3@w0→u, drule2'm@w1→u, drule3'm@w1→u, drule4m@w1→u, drule9@w2→u, drule2'@w3→u, drule3'@w3→u, drule4@w3→u, drule1@w4→u, drule1#2@w4→u, drule3m@w4→u, drule8@w5→u, drule8m@w5→u, drule9@w5→u, drule17@w5→u, drule8@w7→u, drule8m@w7→u, drule9m@w7→u, drule17m@w7→u. Contains: 2.126 (none)

**C 7 5566776 5666657**: n_fill 14400, groups 960, relevant privates 5, fits touching u 23. Domains: lo_max 1, hi_max 1, 720 positive fillings. K633: hi_max 0. K582: hi_max 0.

- fits touching u: drule9@u→w4 [always]; drule8m@u→w5 [always]; drule9m@u→w5 [always]; drule1@w0→u [always]; drule1#2@w0→u [always]; drule2@w0→u [always]; drule3@w0→u [always]; drule1@w1→u [always]; drule1#2@w1→u [always]; drule2m@w1→u [always]; drule3m@w1→u [always]; drule2'm@w2→u [always]; drule4m@w2→u [always]; drule4'@w2→u [p3.1=5]; drule6m@w2→u [always]; drule4'm@w3→u [p2.1=5]; drule7m@w3→u [p2.1=6]; drule9m@w4→u [p4.1=5]; drule8@w5→u [always]; drule9@w5→u [p5.2=5]; drule21@w5→u [p5.1=5 & p5.2=5]; drule22@w5→u [p5.1=5 & p5.2=6]; drule2'@w6→u [always]
- argmax_lo `p2=7 p3=6 x4=9,y4=6 x5=6,y5=5 p6=9`: lo 1, hi 1. Fires: drule9@u→w4, drule8m@u→w5, drule9m@u→w5, drule1@w0→u, drule1#2@w0→u, drule2@w0→u, drule3@w0→u, drule1@w1→u, drule1#2@w1→u, drule2m@w1→u, drule3m@w1→u, drule2'm@w2→u, drule4m@w2→u, drule6m@w2→u, drule8@w5→u, drule22@w5→u, drule2'@w6→u. Contains: 126.61682 (C2cons)
- argmax_lo_after `p2=7 p3=6 x4=9,y4=6 x5=6,y5=6 p6=9`: lo 0, hi 0. Fires: drule9@u→w4, drule8m@u→w5, drule9m@u→w5, drule1@w0→u, drule1#2@w0→u, drule2@w0→u, drule3@w0→u, drule1@w1→u, drule1#2@w1→u, drule2m@w1→u, drule3m@w1→u, drule2'm@w2→u, drule4m@w2→u, drule6m@w2→u, drule8@w5→u, drule2'@w6→u. Contains: no configuration
- argmax_hi_after_proved `p2=7 p3=6 x4=9,y4=6 x5=6,y5=6 p6=9`: lo 0, hi 0. Fires: drule9@u→w4, drule8m@u→w5, drule9m@u→w5, drule1@w0→u, drule1#2@w0→u, drule2@w0→u, drule3@w0→u, drule1@w1→u, drule1#2@w1→u, drule2m@w1→u, drule3m@w1→u, drule2'm@w2→u, drule4m@w2→u, drule6m@w2→u, drule8@w5→u, drule2'@w6→u. Contains: no configuration

**B 7 7676666 6656565**: n_fill 1250000, groups 250000, relevant privates 8, fits touching u 20. Domains: lo_max 6, hi_max 6, 86880 positive fillings. K633: hi_max 0. K582: hi_max 0.

- fits touching u: drule8m@w0→u [always]; drule9@w0→u [p0.2=5]; drule9m@w0→u [p0.1=5]; drule20m@w0→u [p0.1=5 & p0.2=5]; drule8@w2→u [always]; drule9@w2→u [p2.2=5]; drule9m@w2→u [p2.1=5]; drule20@w2→u [p2.1=5 & p2.2=5]; drule4'@w3→u [p4.1=5]; drule5@w3→u [p4.1<=6]; drule3'@w4→u [always]; drule4'@w4→u [p5.1=5]; drule4'm@w4→u [p3.1=5]; drule5m@w4→u [p3.1<=6]; drule3'm@w5→u [always]; drule4'@w5→u [p6.1=5]; drule4'm@w5→u [p4.1=5]; drule5@w5→u [p6.1<=6]; drule4'm@w6→u [p5.1=5]; drule5m@w6→u [p5.1<=6]
- argmax_lo `x0=5,y0=6 p1=9 x2=6,y2=5 p3=5 p4=5 p5=5 p6=5`: lo 6, hi 6. Fires: drule8m@w0→u, drule9@w0→u, drule8@w2→u, drule9m@w2→u, drule4'@w3→u, drule5@w3→u, drule3'@w4→u, drule4'@w4→u, drule4'm@w4→u, drule5m@w4→u, drule3'm@w5→u, drule4'@w5→u, drule4'm@w5→u, drule5@w5→u, drule4'm@w6→u, drule5m@w6→u. Contains: 0.453962 (D2), 2.7566 (D2), 3.1324806 (none), 126.363 (C2cons), 126.469626 (D2)
- argmax_lo_after `x0=5,y0=6 p1=9 x2=6,y2=5 p3=5 p4=6 p5=6 p6=7`: lo 0, hi 0. Fires: drule8m@w0→u, drule9@w0→u, drule8@w2→u, drule9m@w2→u, drule5@w3→u, drule3'@w4→u, drule4'm@w4→u, drule5m@w4→u, drule3'm@w5→u, drule5m@w6→u. Contains: 2.22086 (D2), 126.363 (C2cons), 126.469626 (D2)
- argmax_hi_after_proved `x0=5,y0=6 p1=9 x2=6,y2=5 p3=5 p4=6 p5=6 p6=7`: lo 0, hi 0. Fires: drule8m@w0→u, drule9@w0→u, drule8@w2→u, drule9m@w2→u, drule5@w3→u, drule3'@w4→u, drule4'm@w4→u, drule5m@w4→u, drule3'm@w5→u, drule5m@w6→u. Contains: 2.22086 (D2), 126.363 (C2cons), 126.469626 (D2)

**B 8 76576756 65555556**: n_fill 640000, groups 40000, relevant privates 7, fits touching u 26. Domains: lo_max 2, hi_max 2, 1392 positive fillings. K633: hi_max 0. K582: hi_max 1.

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
| 9 | max_hi | 555576655 | 558855855 | p4.1=6 p4.2=9 p5.1=9 p6.1=6 | 4 | 4 | 34 | 0.7322, 439322.122, 439322.368 |
| 9 | min_lo | 998676976 | 779878658 | p0.1=6 p0.2=9 p0.3=5 p1.1=7 p1.2=9 p1.3=5 p2.1=7 p2.2=7 p2.3=5 p3.1=7 p4.1=6 p4.2=9 p5.1=9 p6.1=5 p6.2=9 p6.3=6 p7.1=7 p7.2=8 p8.1=6 | -29 | -29 | 1 | - |
| 9 | most_fits_1 | 555576655 | 558855855 | p4.1=6 p4.2=9 p5.1=9 p6.1=6 | 4 | 4 | 34 | 0.7322, 439322.122, 439322.368 |
| 9 | most_fits_2 | 566565555 | 868565986 | p1.1=6 p2.1=6 p4.1=5 | 0 | 0 | 30 | 2.122, 2.126, 439322.126, 439326.126 … |
| 9 | max_hi_no_config | 575595855 | 875657757 | p1.1=7 p1.2=9 p4.1=9 p4.2=9 p4.3=5 p6.1=8 p6.2=9 p6.3=8 | -8 | -8 | 22 | - |
| 10 | max_hi | 8555555655 | 6895577659 | p0.1=6 p0.2=8 p0.3=5 p7.1=8 | -2 | -2 | 38 | 0.7322, 26359322.126, 26359326.122 |
| 10 | min_lo | 5878989667 | 5886695895 | p1.1=6 p1.2=9 p1.3=5 p2.1=8 p2.2=8 p3.1=5 p3.2=5 p3.3=6 p4.1=5 p4.2=9 p4.3=6 p5.1=7 p5.2=6 p5.3=6 p6.1=7 p6.2=9 p6.3=6 p7.1=7 p8.1=6 p9.1=6 p9.2=7 | -37 | -37 | 3 | - |
| 10 | most_fits_1 | 8555555655 | 6895577659 | p0.1=6 p0.2=8 p0.3=5 p7.1=8 | -2 | -2 | 38 | 0.7322, 26359322.126, 26359326.122 |
| 10 | most_fits_2 | 6855556555 | 5585595586 | p0.1=5 p1.1=5 p1.2=7 p1.3=5 p6.1=8 | -4 | -4 | 36 | 0.7322, 2.126, 26359326.122 |
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
| A | 7 | 56 | 0 | 43251521 | 13 | 5 | 5 | 422480 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| A | 8 | 106 | 0 | 2742825 | 25 | 1 | 1 | 72500 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| A | all | 162 | 0 | 45994346 | 38 | 5 | 5 | 494980 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| B | 7 | 369 | 0 | 409765956 | 81 | 6 | 6 | 2831087 | 3 | 1 | 166000 | 3 | 0 | 0 | 0 |
| B | 8 | 126 | 0 | 14491941 | 17 | 6 | 6 | 66661 | 1 | 1 | 1152 | 1 | 0 | 0 | 0 |
| B | all | 495 | 0 | 424257897 | 98 | 6 | 6 | 2897748 | 4 | 1 | 167152 | 4 | 0 | 0 | 0 |
| C | 7 | 281 | 0 | 27137688 | 25 | 1 | 1 | 228600 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| C | 8 | 0 | 0 | 0 | 0 | - | - | 0 | 0 | - | 0 | 0 | 0 | 0 | 0 |
| C | all | 281 | 0 | 27137688 | 25 | 1 | 1 | 228600 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| T | 7 | 48 | 0 | 33697870 | 10 | 5 | 5 | 249150 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| T | 8 | 257 | 0 | 10464995 | 25 | 2 | 2 | 61392 | 1 | 1 | 1152 | 1 | 0 | 0 | 0 |
| T | all | 305 | 0 | 44162865 | 35 | 5 | 5 | 310542 | 1 | 1 | 1152 | 1 | 0 | 0 | 0 |

configurations used to cover positive fillings: 98 (90 proved D2/C2cons, 8 none = proved-modulo-admissibility)

**Rows that need a proved-modulo-admissibility configuration** (positive under K582, killed under K633): 5.

| set | row | max hi (dom) | max hi after K582 | argmax after K582 | fillings killed only by a none configuration |
|---|---|---|---|---|---|
| B | 8 76576756 65555556 | 2 | 1 | `x0=5,y0=6 p1=9 x3=5,y3=7 p4=6 x5=7,y5=5 p7=9` | 2.126:1152 |
| B | 7 8557766 7565755 | 1 | 1 | `x0=9,m0=9,y0=9 x3=9,y3=5 x4=9,y4=6 p5=5 p6=6` | 124.1324817:40000 2.126:10000 |
| B | 7 8565766 5557657 | 1 | 1 | `x0=9,m0=9,y0=9 p2=9 x4=6,y4=9 p5=7 p6=6` | 128.1324802:72000 |
| B | 7 8565766 5557656 | 1 | 1 | `x0=9,m0=9,y0=9 p2=9 x4=6,y4=9 p5=7 p6=7` | 128.1324802:54000 |
| T | 8 56765767 56655555 | 2 | 1 | `p1=9 x2=5,y2=6 p3=9 x5=5,y5=7 p6=6 x7=7,y7=5` | 2.126:1152 |

**Largest positive rows under the domains alone** (every one is killed under both K582 and K633 unless listed above; all rows are in `results/positive_rows.tsv`):

| set | row | fillings | max lo = max hi | argmax filling | positive fillings | top covering configurations (name:verdict:#fillings) |
|---|---|---|---|---|---|---|
| B | 7 7676666 6656565 | 1250000 | 6 | `x0=5,y0=6 p1=9 x2=6,y2=5 p3=5 p4=5 p5=5 p6=5` | 86880 | 126.469626:D2:1100 126.363:C2cons:1030 2.7566:D2:955 3.1324806:none:905 |
| B | 8 75766666 55565565 | 1562500 | 6 | `x0=5,y0=5 x2=5,y2=5 p3=5 p4=5 p5=6 p6=5 p7=5` | 15136 | 122.122:D2:400 123.442806:D2:364 3.1324817:none:317 122.363:D2:316 |
| A | 7 6676767 6565565 | 8593750 | 5 | `p0=5 p1=5 x2=5,y2=5 p3=9 x4=5,y4=7 p5=9 x6=5,y6=5` | 90150 | 2.7566:D2:10000 122.363:D2:10000 3.1324817:none:10000 126.469626:D2:10000 |
| A | 7 6767676 5655656 | 8593750 | 5 | `p0=5 x1=5,y1=5 p2=9 x3=5,y3=7 p4=9 x5=5,y5=5 p6=5` | 90150 | 122.363:D2:10000 126.469626:D2:10000 3.1324817:none:5300 2.7566:D2:4500 |
| A | 7 7676766 6565665 | 9765625 | 5 | `x0=5,y0=5 p1=9 x2=5,y2=5 p3=9 x4=5,y4=5 p5=5 p6=5` | 20425 | 497.1028:C2cons:6700 122.363:D2:6100 126.469626:D2:6100 3.1324817:none:4300 |
| B | 7 7676766 6556565 | 8593750 | 5 | `x0=5,y0=5 p1=9 x2=5,y2=7 p3=9 x4=5,y4=5 p5=5 p6=5` | 90150 | 126.469626:D2:6150 3.1324817:none:5225 122.363:D2:5150 497.1028:C2cons:4875 |
| B | 8 75666675 65656557 | 200000 | 5 | `x0=5,y0=9 p2=6 p3=5 p4=5 p5=5 x6=6,y6=5` | 4600 | 7566.372:none:1164 2.22086:D2:992 0.453962:D2:744 2.7566:D2:744 |
| T | 7 6676767 6565565 | 8593750 | 5 | `p0=5 p1=5 x2=5,y2=5 p3=9 x4=5,y4=7 p5=9 x6=5,y6=5` | 90150 | 2.7566:D2:10000 122.363:D2:10000 3.1324817:none:10000 126.469626:D2:10000 |
| T | 7 6767676 5655656 | 8593750 | 5 | `p0=5 x1=5,y1=5 p2=9 x3=5,y3=7 p4=9 x5=5,y5=5 p6=5` | 90150 | 122.363:D2:10000 126.469626:D2:10000 3.1324817:none:5300 2.7566:D2:4500 |
| A | 7 7666676 6656666 | 1953125 | 4 | `x0=5,y0=5 p1=5 p2=5 p3=5 p4=5 x5=5,y5=5 p6=9` | 8005 | 0.453962:D2:1810 2.7566:D2:1280 3.1324806:none:1280 122.368:C2cons:835 |
| B | 7 8666666 5656765 | 1953125 | 4 | `x0=9,m0=9,y0=9 p1=5 p2=5 p3=5 p4=5 p5=5 p6=5` | 21500 | 2.7566:D2:19000 0.453962:D2:18000 3.1324806:none:16375 2.22086:D2:7750 |
| A | 7 7767666 6565655 | 6250000 | 3 | `x0=9,y0=5 x1=5,y1=9 p2=9 x3=6,y3=5 p4=5 p5=5 p6=6` | 156000 | 667.1028:C2cons:48000 2.7566:D2:28000 2.22086:D2:16000 2.126:none:12500 |

**Configurations that cover positive fillings:** 98 in all, 8 of them none (proved-modulo-admissibility). The 15 most used are listed here; the full list is `results/covering_configs.tsv`, with columns per set. A count is the number of positive fillings (group multiplicity) in which some tested minimal combination contains the configuration. It is taken over the positive groups stored per row, which are capped at 400; 19 rows reach the cap (A 5, B 12, T 2), so their counts are partial. The kill decisions use every group.

| configuration | verdict | positive fillings containing it (all sets) |
|---|---|---|
| 7322.207 | D2 | 470100 |
| 7322.149 | C2cons | 468750 |
| 196.9902 | D2 | 424575 |
| 482.1148 | C2cons | 386895 |
| 3.3686402 | C2cons | 374895 |
| 7385.137 | C2cons | 276950 |
| 3.3700802 | C2cons | 251644 |
| 3.3682802 | D2 | 246072 |
| 122.70022 | C2cons | 207520 |
| 7322.165 | D2 | 166600 |
| 2.22086 | D2 | 164540 |
| 0.174369782 | D2 | 145800 |
| 128.1324802 | none (mod-adm) | 126000 |
| 3.1324802 | none (mod-adm) | 125820 |
| 219.1023 | D2 | 123600 |
<!--/TABLES-->

**Findings (d = 7 / 8, exhaustive).** No row is `not done`, no domain is empty, and `inexact_groups` = 0 in every set. In every cell of the table, max lo = max hi.

- **Domains only.** 196 of 1,243 rows have positive fillings: A 38, B 98, C 25, T 35. That is 3,931,870 positive fillings out of 541.6 M, counted over all sites (erratum E3).
  - The maxima are +6 RSST units (+0.6 ours), in B at both d7 and d8.
  - A, the binder set, agrees with the sampled REPORT §3(b): 13 of 56 rows positive at d7 and 25 at d8. The d8 count is now out of 106 rows, because the rows with a 9+ link letter are included exactly.
- **K633** (582 proved + 51 proved-modulo-admissibility). **Every filling of every row has final charge ≤ 0.** After kills the maximum is 0 in every set.
- **K582** (proved only). 5 rows keep positive fillings, each with max hi = +1 (+0.1 ours): B 4 rows (167,152 fillings) and T 1 row (1,152 fillings), counted over all sites (erratum E3). Each is killed only by a configuration with verdict none:
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
- **W6b's reporting flags on §11** (they change no verdict). (1) The `fills_*` counts multiply group multiplicities only over sites that have a relevant private. A site with no relevant private is skipped (`if sizes[j] == 1 and not cls[j][0][0]: continue` in `fp_exact.py`), so the positive-filling counts in §11 are too low by the product of those sites' option counts. `n_fill`, every maximum and every kill status are unaffected. (2) Only groups with hi > 0 are kill-checked. This is correct for the pass test, but it means `configs_used` and the coverage counts describe positive groups only. W6b argues in round16/round10_rsstfp2/DECISIONS.md that Assumption H (§7) holds.
- **Scope.** This run checks u's own charge only, not the charges of the other vertices of the 2-ball, and it adds no LP or t terms.

## 13. Addendum A (RSST-FP9): exact check at d = 9..14

Files: `d9plus/` (code, results, logs, MD5SUMS). This section is enough to replicate the check. The code is a reference only.

### A.1 Statement and model

**What is certified.** For every d ∈ {9, …, 14}, every link word and every filling, the final charge of u under all 71 parts is at most 0, once the kill model's configurations are excluded.

**Charge.**
- u has exact degree d. To the parts u reads as 9+, so its fans are never read (§6).
- u is never a hub, so it never sends.
- hi = 10(6−d) + #{fits at hubs w_i (letter 5..8) with target u that are possible}. lo uses sure fits instead.
- The pass test uses hi.

**Letters.** Every link letter, apex and private is free in 5..9+.
- For d ≥ 9 our pipeline has no K3gB5n / V2ROW domains; V2ROW_SPEC §3 is defined only for d = 7 and 8. So the only kills are RSST appearances, and the check is at least as strong as one that also used domains.
- A 9+ link vertex is drawn as an 8 (§6). Its y = p.1 and x = p.3 are free letters. Its middle is held at 9+ and never read.

**Hosts** (§7, with one change: u is a host).
- u, with its exact letter d. RSST interiors have degrees up to 11, so u can be matched for d ≤ 11.
- Every w, s and private whose letter is exact (≤ 8). 9+ is never a host.

**Host-graph edges** are the window edges among hosts:
- u–w_j, w_j–w_{j+1}, w_j–s_{j−1}, w_j–s_j, w_j–p_j.k;
- the chain s_{j−1}–p_j.1–…–p_j.k–s_j (for a 9+ site the drawn chain is s_{j−1}–y–m–x–s_j, with m never a host);
- s_{j−1}–s_j when w_j = 5.

**Containment** is induced and injective with exact degrees (§7). The face condition is implied: every interior face is a triangle of interior edges, and induced matching keeps all three of them.

### A.2 The fits from hub w_i into u, as interval conditions

Take a hub w_i with letter n = L_i ∈ 5..8. Its rotation is rot(w_i) = u, w_{i−1}, s_{i−1}, p_i.1..p_i.k, s_i, w_{i+1} (k = n−5). The target S[a+2] = u forces the anchor a = n−2.

For each part with n subparts, apply §3.3 and §3.4. The subpart reads are:

| subpart j | spoke | hat (across xp–x) | fans |
|---|---|---|---|
| 0 | s_i | ring 3 (OPEN unless `*`) | s spoke: OPEN unless all `*` |
| 1 | w_{i+1} | p_{i+1}.1 if L_{i+1} ≥ 6 (y_{i+1} for 9+); s_{i+1} if L_{i+1} = 5 | if L_{i+1} is exact 6..8: p_{i+1}.2, …, p_{i+1}.(L_{i+1}−5), s_{i+1} |
| 2 | u (read as 9) | w_{i+2} | never read (§6) |
| 3 | w_{i−1} | w_{i−2} | if L_{i−1} is exact 6..8: s_{i−2}, p_{i−1}.1, …, p_{i−1}.(L_{i−1}−6) |
| 4 | s_{i−1} | p_{i−1}.last if L_{i−1} ≥ 6 (x_{i−1} for 9+); s_{i−2} if L_{i−1} = 5 | OPEN unless all `*` |
| 5..n−1 | p_i.1..p_i.k | ring 3 (OPEN unless `*`) | private spoke: OPEN unless all `*` |

How the tests resolve:
- Tests on the link letters L_{i−1}, L_i and L_{i+1} are decided from the *hub class* (L_{i−1}, L_i, L_{i+1}).
- Tests on W±2 = L_{i±2}, on S−2..S+1 = s_{i−2}..s_{i+1} and on the privates of w_{i−1}, w_i and w_{i+1} become interval conditions.
- A fit is the conjunction of its conditions, plus an OPEN flag.

These are the only letters a fit into u reads. In the reference code this is asserted for every class (`d9_export.py`).

**Checksums** (`results/hubs.txt`):
- Summed over the 25 neighbour classes, the number of fits that survive the class-level tests is 80 for hub letter 5, 80 for 6, 70 for 7 and 9 for 8.
- c⁺, the maximum number of possible fits over all non-link letters, is 6, 6, 6 and 4 for hub letters 5, 6, 7 and 8, and 0 for 9+. `results/cplus.txt` gives c⁺ for every 5-letter link window; it agrees with `../results/tail9.json`.

### A.3 The exact search

**1. Link words.**
- Enumerate the link words L_0..L_{d−1} up to rotation and reflection. The parts are mirror-closed and the matcher is orientation-free, so these symmetries are safe.
- Run a DFS in site order, letters 5..9, that keeps only words starting with their least letter.
- Bound a partial word by 10(6−d) + Σ_i b_i, where:
  - b_i = c⁺(L_{i−2..i+2}) if the window is already assigned;
  - b_i = cmax(L_i) = 6, 6, 6, 4, 0 if only L_i is known;
  - b_i = 6 otherwise.
- At a full word, check that it is the dihedral minimum, then apply the cyclic c⁺ bound.
- **Link-level kill check**: with hosts u and the exact w's only, test every configuration of the variant. A word that is killed here is done.

**2. Variables of a word.**
- In site order: s_j, then p_j.1..p_j.k. A 9+ site contributes only y and x.
- The fit instances are the fits of A.2 at every hub. W±2 conditions are already decided by the word.
- **Domain of a variable**: {9} together with each a ∈ 5..8 whose truth pattern on that variable's conditions differs from 9's.
  - This is a dominance argument. A letter with the same pattern as 9 gives the same charge, and it adds a host, so by monotonicity it can only add kills. So it never beats 9.
- Values are tried in order of the most conditions satisfied first, with 9 first on ties.

**3. DFS over the variables.**
- Bound = 10(6−d) + the number of fit instances that no assigned value violates. This is valid because each instance is a conjunction.
- Prune when bound ≤ threshold.
- After an exact letter is assigned to vertex v, run an **anchored kill check**: is any configuration of the variant contained with some interior vertex mapped to v?
  - Try each configuration vertex x0 with deg x0 = letter(v), and extend in breadth-first order from x0. Interiors are connected.
  - Candidate hosts for the next vertex x: hosts with letter deg x that are not yet used, adjacent to the images of x's mapped neighbours, and not adjacent to the images of its mapped non-neighbours.
  - In the 633 variant the proved configurations are tried first.
- If a configuration is contained, the node is killed for every completion, by monotonicity (§7).
- At a leaf every condition is decided, so hi = bound exactly.

**4. Modes.**
- **max**: the threshold is the best hi found so far, starting from S. The result is the exact maximum over unkilled states when it is greater than S; otherwise the run certifies max ≤ S. S = 0 gives the pass test. Lower S gives the exact maximum.
- **enum**: the threshold is fixed at 0. Every leaf is a positive state that the 582 configurations do not kill. Each one is tested against the 51 none configurations, which classifies it as either killed only by proved-modulo-admissibility configurations, or genuinely positive.

**5. Why it is exact.** The search is complete over link words (symmetry), fillings (dominance) and pruning (valid bounds plus monotone kills).
- Every occurrence of a configuration is found: when its last host is assigned (anchored check), or at link level when it uses only u and w's.
- The leaf charge equals pubrules' ledger.

**Cross-checks.**
- 600 seeded random d = 9..14 2-balls (`results/xval.txt`): hi, lo and the full set of contained configurations agree with pubrules and rsst_rows on all 600.
- Every state the search reports is re-evaluated on pubrules + rsst_rows (`results/recheck.json`).
- The no-kill variant reproduces 60 − 4d (§8.4).
- A planted control (kill set minus 2.122 and 0.7322) finds positive states again.

### A.4 Results

<!--D9TABLES-->
| d | no kills: max (argmax link / apexes / privates) | 582 proved: max | 633: max | 633 search: words, link-killed words, nodes, s | 582 enum: positive states left by 582 (killed only by none configs / genuine) |
|---|---|---|---|---|---|
| 9 | 24 `555555555 / 555555555 / 9..9` | 7 `555665566 / 595565666 / 999999999699599999999699699` | <= 0 certified; exact max 0 `555556757 / 595966566 / 999999999999999999659999999` | 17826, 433, 3876089, 75.7 | 31139 / 0 |
| 10 | 20 `5555555555 / 5555555555 / 9..9` | 3 `5555556657 / 5959566556 / 999999999999999999999699999959` | <= 0 certified; exact max 0 `5555556666 / 5959565556 / 9..9` | 15169, 351, 1559927, 18.9 | 409 / 0 |
| 11 | 16 `55555555555 / 55555555555 / 9..9` | <= 0  | <= 0 certified; exact max 0 `55555556556 / 59595955956 / 9..9` | 8906, 65, 340799, 2.3 | 0 / 0 |
| 12 | 12 `555555555555 / 555555555555 / 9..9` | <= 0  | <= 0 certified; exact max 0 `555555555555 / 595959595959 / 9..9` | 3476, 0, 31672, 0.1 | 0 / 0 |
| 13 | 8 `5555555555555 / 5555555555555 / 9..9` | <= 0  | <= 0 certified; exact max -6 `5555555555555 / 5959595959599 / 9..9` | 639, 0, 964, 0.0 | 0 / 0 |
| 14 | 4 `55555555555555 / 55555555555555 / 9..9` | <= 0  | <= 0 certified; exact max <= -10  | 46, 0, 11, 0.0 | 0 / 0 |

**States that only a proved-modulo-admissibility configuration kills.** These are the leaves of the 582 enumeration (positive and unkilled by the 582), grouped by the set of none configurations they contain, and counted as dominance-reduced states per d:

Totals: d9: 31139, d10: 409 dominance-reduced states, 238 distinct sets, 21 none configurations involved. Every state contains at least one none configuration, and none is genuinely positive.

| none configuration | states containing it (per d) | states where it is the ONLY none configuration (per d) |
|---|---|---|
| 439326.126 | d9: 21708 | d9: 3591 |
| 2.126 | d9: 21195, d10: 273 | d9: 367, d10: 60 |
| 453963.364 | d9: 9794 | d9: 154 |
| 439328.136 | d9: 4551 | d9: 219 |
| 453963.136 | d9: 2908 | d9: 153 |
| 3.1324806 | d9: 2125, d10: 16 | d9: 64, d10: 4 |
| 126.1306802 | d9: 2016, d10: 72 | d9: 454, d10: 32 |
| 453963.126 | d9: 1826 | d9: 316 |
| 126.442802 | d9: 1300, d10: 42 | d9: 41, d10: 9 |
| 439589.122 | d9: 1197 | d9: 62 |
| 443166.126 | d9: 1095 | d9: 22 |
| 3.1324802 | d9: 578, d10: 20 | d9: 31 |
| 26359326.126 | d10: 298 | d10: 53 |
| 7322.453720 | d9: 197 | - |
| 128.1324802 | d9: 183 | - |
| 7562.460920 | d9: 110 | - |
| 122.1324802 | d9: 90 | - |
| 126.1551602 | d9: 30 | - |
| 8.1551606 | d9: 30 | - |
| 126.3682802 | d9: 4 | - |
| 126.687602 | d9: 1 | - |

Configurations that are the only killer of some state, and so needed for any proof by this route (13): 126.1306802, 126.442802, 2.126, 26359326.126, 3.1324802, 3.1324806, 439326.126, 439328.136, 439589.122, 443166.126, 453963.126, 453963.136, 453963.364. Together with nothing else they hit every set, so this is a hitting set of 13 none configurations: **126.1306802, 126.442802, 2.126, 26359326.126, 3.1324802, 3.1324806, 439326.126, 439328.136, 439589.122, 443166.126, 453963.126, 453963.136, 453963.364**. The full list of sets is in `results/modadm_sets.tsv`.

**Kill events of the 633 search** (pruned nodes whose bound was still positive, by the first killing configuration; proved configurations are tried first), top 8 per d:

- d=9: 2.122:D2 250324, 0.7322:D2 140861, 2.126:none 132324, 122.122:D2 124682, 122.126:C2cons 94665, 2.7566:D2 51204, 2.22086:D2 43096, 0.453962:D2 22374; link-level: 439322.122:D2 65, 439320.439322:D2 10, 439322.126:C2cons 100, 439326.122:D2 74, 439326.126:none 96, 453722.126:C2cons 53, 439562.7326:D2 13, 453722.7566:C2cons 22
- d=10: 2.122:D2 134223, 0.7322:D2 99799, 2.126:none 70869, 122.122:D2 45595, 122.126:C2cons 31396, 2.7566:D2 23461, 2.22086:D2 18284, 3.1306802:D2 8394; link-level: 26359322.122:D2 65, 26359322.126:C2cons 81, 26359326.122:D2 61, 26359326.126:none 59, 26373722.126:C2cons 49, 27223322.126:C2cons 36
- d=11: 0.7322:D2 38939, 2.122:D2 34107, 2.126:none 16430, 122.122:D2 6486, 2.7566:D2 5073, 122.126:C2cons 3637, 3.1306802:D2 3216, 2.22086:D2 3165; link-level: 26359322.-7322:D2 65
- d=12: 0.7322:D2 7052, 2.122:D2 2994, 2.126:none 748, 3.460806:D2 418, 3.1306802:D2 260, 2.7566:D2 201, 122.122:D2 171, 2.1551966:D2 98; link-level: none
- d=13: 0.7322:D2 419, 2.122:D2 48, 3.460806:D2 5; link-level: none
- d=14: 0.7322:D2 5, 2.122:D2 1; link-level: none

**Planted control** (d = 9, 633 minus 2.122 and 0.7322): max 7, argmax `556655676 / 555555555 / 999999999999999999999599999`. The search does find positive states once kills are removed.

**Re-check on pubrules + rsst_rows** (`code/d9_recheck.py`): 114 reported states re-evaluated (hi, lo, no proved configuration contained, the none set as reported; for the planted control, only the dropped configurations), 0 disagreements.

**Test vectors** (all of them re-evaluated on pubrules + rsst_rows; the privates are listed 3 per site in site order, with 9 meaning 9+ or absent; full fit lists are in `d9plus/results/recheck.json`):

| d | what | link | apexes | privates | hi = lo | contained configurations |
|---|---|---|---|---|---|---|
| 9 | all 5 (no-kill argmax, 60-4d) | 555555555 | 555555555 | 9..9 | 24 | 0.7322 (D2), 439322.122 (D2), 439320.439322 (D2), 439322.442802 (D2) |
| 10 | all 5 (no-kill argmax, 60-4d) | 5555555555 | 5555555555 | 9..9 | 20 | 0.7322 (D2), 26359322.122 (D2) |
| 11 | all 5 (no-kill argmax, 60-4d) | 55555555555 | 55555555555 | 9..9 | 16 | 0.7322 (D2), 26359322.-7322 (D2) |
| 12 | all 5 (no-kill argmax, 60-4d) | 555555555555 | 555555555555 | 9..9 | 12 | 0.7322 (D2) |
| 13 | all 5 (no-kill argmax, 60-4d) | 5555555555555 | 5555555555555 | 9..9 | 8 | 0.7322 (D2) |
| 14 | all 5 (no-kill argmax, 60-4d) | 55555555555555 | 55555555555555 | 9..9 | 4 | 0.7322 (D2) |
| 9 | all-5 link, apexes and privates 9+ | 555555555 | 999999999 | 9..9 | 6 | 439322.122 (D2), 439320.439322 (D2) |
| 10 | all-5 link, apexes and privates 9+ | 5555555555 | 9999999999 | 9..9 | 0 | 26359322.122 (D2) |
| 11 | all-5 link, apexes and privates 9+ | 55555555555 | 99999999999 | 9..9 | -6 | 26359322.-7322 (D2) |
| 12 | all-5 link, apexes and privates 9+ | 555555555555 | 999999999999 | 9..9 | -12 | - |
| 13 | all-5 link, apexes and privates 9+ | 5555555555555 | 9999999999999 | 9..9 | -18 | - |
| 14 | all-5 link, apexes and privates 9+ | 55555555555555 | 99999999999999 | 9..9 | -24 | - |
| 9 | control argmax (633 minus 2.122, 0.7322) | 556655676 | 555555555 | 999999999999999999999599999 | 7 | 0.7322 (D2) |
| 10 | 582 argmax (positive; killed only by none) | 5555556657 | 5959566556 | 999999999999999999999699999959 | 3 | 126.442802 (none), 26359326.126 (none) |
| 9 | 582 argmax (positive; killed only by none) | 555665566 | 595565666 | 999999999699599999999699699 | 7 | 2.126 (none), 439326.126 (none), 453963.364 (none) |
| 10 | 633 exact argmax | 5555556666 | 5959565556 | 9..9 | 0 | - |
| 11 | 633 exact argmax | 55555556556 | 59595955956 | 9..9 | 0 | - |
| 12 | 633 exact argmax | 555555555555 | 595959595959 | 9..9 | 0 | - |
| 13 | 633 exact argmax | 5555555555555 | 5959595959599 | 9..9 | -6 | - |
| 9 | 633 exact argmax | 555556757 | 595966566 | 999999999999999999659999999 | 0 | - |

Fits for one vector, so the ledger can be checked: d = 9, 582 argmax: 555665566/595565666/999999999699599999999699699, 37 fits into u: drule1@w0, drule1#2@w0, drule2@w0, drule3@w0, drule1@w1, drule1#2@w1, drule2@w1, drule2m@w1, drule3m@w1, drule1@w2, drule1#2@w2, drule2m@w2, drule3@w2, drule2'm@w3, drule3'@w3, drule3'm@w3, drule4'@w3, drule2'@w4, drule3'm@w4, drule4@w4, drule6@w4, drule1@w5, drule1#2@w5, drule2@w5, drule3@w5, drule1@w6, drule1#2@w6, drule2m@w6, drule3m@w6, drule2'm@w7, drule4m@w7, drule6m@w7, drule7@w7, drule2'@w8, drule4@w8, drule6@w8, drule7m@w8
<!--/D9TABLES-->

**Findings (d = 9..14).**
- **All 633** (582 proved + 51 proved-modulo-admissibility): **every d = 9..14 is certified, with final charge ≤ 0.** Every search is complete, with no time limit and no cap hit. The exact maximum is 0 at d = 9..12, −6 at d = 13 and ≤ −10 at d = 14.
- **582 proved only.** d = 11..14 are certified by the proved configurations alone. d = 9 and 10 are not: the maxima are +7 and +3, and there are 31,139 and 409 positive dominance-reduced states.
  - None of these states is genuinely positive: each contains at least one of 21 none configurations.
  - 13 of them (listed above) are the only killer of some state, and those 13 already hit every state.
  - So at d = 9 and 10 the certification rests on the admissibility of those 13 configurations, which include 2.126.
- **No kills.** The maximum is exactly 60 − 4d (all-5 filling).
- **How the kills are found.** At d = 9..11 several kills use u itself as a host (configurations with an interior vertex of degree 9, 10 or 11). The all-5 link with 9+ apexes is killed at link level at d = 9 and 10 (439322.122 at d = 9, 26359322.122 at d = 10).
- **No K3gB5n domains were used** (none exist for d ≥ 9 in our pipeline). The certificate is therefore independent of them.



## 14. Erratum (RSST-FPW): the three Studio flags, one convention each

These conventions hold for every run in this folder: §11 (after the fix below), §13 and §15.

- **E1. u is a host at every degree, with its exact letter d.**
  - u's degree is exact in a per-vertex check, so u is a legitimate host. RSST interiors reach degree 11.
  - §7 used to exclude u at d ≥ 9. The ext vectors in §10.2 were generated that way.
  - §7 is corrected. `results/test_vectors_ext.json` and the §10.2 table are regenerated with u as a host. At d = 9..11 the contained-configuration lists of some vectors grow. For example, the d = 9 max-hi vector `555576655/558855855` now contains 3 configurations instead of 1.
  - §11 (d7/d8) and §13 always had u as a host.
  - No verdict changes: §10.2 vectors are fixed fillings and carry no claim.
- **E2. Only positive states are kill-checked.**
  - A state (filling) with hi ≤ 0 is never tested for kills and never counted.
  - A *survivor* under a kill model is a state with hi > 0 that the model does not kill. "Killed", "covered by" and every configuration count refer to positive states only.
  - Where it applies:
    - fp_exact second pass: groups with hi > 0.
    - §13 and §15 searches: kill checks only on nodes whose bound is > the threshold, and the threshold is ≥ 0.
  - This is verdict-neutral, because the pass test reads only positive states. The Studio's all-groups variant (`from_studio_RSST1SHOT/results/summary_sets.tsv`, `*_allkill`) gives the same maxima.
- **E3. Filling counts multiply over all sites, as §8.1 says.**
  - The first pass of `fp_exact.py` skipped the multiplicity of every site with no relevant private (`if sizes[j] == 1 and not cls[j][0][0]: continue`).
  - Every group of a row misses the same factor: the product of the option counts of those sites. `code/fp_fillfix.py` multiplies the `fills_*` fields and `positives[*].fills` of `results/fp_*.json` by this factor, and keeps the old values as `*_relsites` and the factor as `fills_site_factor`.
  - A brute-force recount with pubrules' ledger over every filling of 8 rows agrees exactly (`results/fillfix_checks.json`).
  - The corrected counts equal the Studio's spec-exact `summary_sets.tsv`, for example A d7 422,480 and B d7 2,831,087 positive fillings.
  - §11 tables, `test_vectors.json` and the §11 findings are regenerated. n_fill, maxima and kill status do not change.

## 15. Full world at d = 5..8 (RSST-FPW, second engine)

Files: `fullworld/` (code, results, logs, MD5SUMS).

**Setting.**
- Every link letter, apex and private is free in 5..9+.
- No domains.
- All 71 parts.
- u's own ledger as in §4: hub-u fits send, hub-w_i fits into u receive.
- Hosts per E1.

**Method.** This is the §13 search with one change: the fit tables are built per link word.

1. **Fit tables.**
   - For each link word (one per rotation-and-reflection class: the lexicographically least), list every fit that moves u's charge:
     - OUT: hub u, target w_j, d = 5..8;
     - IN: hub w_i with letter 5..8, target u.
   - Read them by §3.3 in the window of §2. Every apex and every private is a variable:
     - a range test on it becomes an interval condition;
     - a fan read on an apex spoke is OPEN, since it is ring 3 whatever the apex degree.
   - Tests on link letters are decided by the word. This includes u's own fans when u is an exact-degree spoke of a hub w_i: they are w_{i+3}..w_{i−3}.
   - Each (part, hub, target) has one anchor, so every fit is one conjunction.
2. **Charge and bound.**
   - hi = 10(6−d) + #IN possible − #OUT sure.
   - During the search the bound is 10(6−d) + #IN not yet violated − #OUT already sure. An OUT fit is sure once every one of its conditions is assigned and satisfied and it is not OPEN.
   - The bound is valid and exact at a leaf. lo = 10(6−d) + #IN sure − #OUT possible.
3. **Dominance.** As in §13 A.3.2, with the truth pattern taken over all IN and OUT conditions on the variable. Values are tried by (#IN conditions satisfied − #OUT conditions satisfied).
4. **Kills.** The link-level check, the anchored incremental containment and the modes are as in §13 A.3.

**State definition** (what the counts count). A state is:
- a canonical link word,
- plus one value per variable (s_j, then p_j.1..k; y and x at a 9+ site), each from its dominance-reduced domain.

A word with a nontrivial symmetry is not reduced further. With E2, the counts are the leaves: positive states left by the kill model.

**Cross-check.** 800 seeded random d = 5..8 2-balls (`fullworld/results/xval.txt`). In the per-word tables the apexes are variables; pubrules evaluates them with the apexes known. hi, lo and the contained configurations (u as a host) agree on all 800.

<!--FWTABLES-->
| d | link classes | no kills: max (argmax link / apexes / privates) | K633: max; words with positive bound, link-killed words, nodes, s | K582: positive states left (killed only by none configs / genuine); max charge among them | none configs involved / sole killers | Studio RSST-1SHOT (classes, max, K582 states, none / sole) | agree |
|---|---|---|---|---|---|---|---|
| 5 | 377 | 10 `55555 / 99999 / 9..9` | <= 0 (complete); 29, 29, 0, 0 | 0 / 0; - | 0 / 0 | 377, 10, 0, 0 / 0 | yes |
| 6 | 1505 | 24 `555555 / 555555 / 9..9` | <= 0 (complete); 799, 153, 147751, 0 | 3917 / 0; 9 | 1 / 1 | 1505, 24, 3917, 1 / 1 | yes |
| 7 | 5895 | 32 `5555555 / 5555555 / 9..9` | <= 0 (complete); 2751, 229, 3191626, 74 | 84292 / 0; 4 | 29 / 26 | 5895, 32, 84292, 29 / 26 | yes |
| 8 | 25395 | 28 `55555555 / 55555555 / 9..9` | <= 0 (complete); 5738, 351, 5192212, 161 | 55752 / 0; 8 | 30 / 23 | 25395, 28, 55752, 30 / 23 | yes |

Genuine survivors (positive states that contain no configuration at all): 0 at every d. K633 leaves no positive state at any d = 5..8. Every figure equals the Studio's.

**K582 leaves by none configuration** (dominance-reduced states per d; full list of sets in `fullworld/results/modadm_sets_fw.tsv`): 339 distinct sets, 43 none configurations involved.

| none configuration | states containing it (per d) | states where it is the ONLY none configuration (per d) |
|---|---|---|
| 2.126 | d6: 3917, d7: 23570, d8: 26210 | d6: 3917, d7: 142, d8: 3096 |
| 128.136 | d7: 43781 | d7: 20380 |
| 8406.123 | d8: 15872 | d8: 3959 |
| 11166.140 | d8: 10742 | d8: 2234 |
| 7566.128 | d8: 9498 | d8: 4304 |
| 142.1324802 | d7: 8900 | d7: 1254 |
| 200.1324802 | d7: 8135 | d7: 491 |
| 124.1324817 | d7: 6658 | d7: 5980 |
| 126.8168 | d7: 6615 | d7: 3591 |
| 122.1324802 | d7: 5501, d8: 296 | d7: 4788 |
| 126.1306802 | d7: 2485, d8: 3150 | d7: 1146, d8: 1007 |
| 128.1324802 | d7: 5306, d8: 51 | d7: 4368 |
| 140.8406 | d7: 4593 | d7: 560 |
| 11780.363 | d8: 3994 | d8: 2015 |
| 3.1324802 | d7: 74, d8: 3894 | d7: 62, d8: 79 |
| 7322.1324802 | d8: 3740 | d8: 3578 |
| 8406.363 | d8: 3204 | d8: 553 |
| 7587.123 | d7: 197, d8: 2968 | d8: 80 |
| 7580.363 | d8: 2768 | d8: 1111 |
| 126.442802 | d7: 1718, d8: 647 | d7: 867, d8: 154 |
| 184.1324806 | d7: 1980 | d7: 1896 |
| 7566.372 | d8: 1673 | d8: 70 |
| 3.1324806 | d7: 224, d8: 1197 | d7: 46, d8: 26 |
| 7696.442802 | d8: 1332 | d8: 82 |
| 483.1324806 | d7: 1104 | d7: 1068 |
| 7566.9723 | d8: 1045 | d8: 213 |
| 126.62942 | d7: 983 | d7: 498 |
| 209.1324802 | d7: 953 | d7: 323 |
| 7322.453720 | d7: 180, d8: 740 | d8: 522 |
| 142.1324806 | d7: 807 | d7: 460 |
| 7562.460920 | d7: 107, d8: 463 | d8: 442 |
| 8.1551606 | d7: 72, d8: 356 | d7: 32, d8: 16 |
| 7562.1310580 | d8: 410 | d8: 295 |
| 188.1324817 | d7: 350 | d7: 272 |
| 126.3686402 | d7: 297, d8: 8 | d7: 164 |
| 7322.1040 | d8: 217 | d8: 217 |
| 7877.442802 | d8: 183 | d8: 85 |
| 126.3682802 | d7: 144, d8: 7 | d7: 120 |
| 126.1551602 | d7: 73, d8: 62 | d7: 70 |
| 8.1540806 | d7: 76, d8: 48 | d7: 24 |
| 7562.1307280 | d8: 100 | d8: 100 |
| 126.687602 | d7: 44 | d7: 35 |
| 3.1324817 | d7: 12, d8: 12 | d7: 12 |

Sole killers over d = 5..8 (43): 11166.140, 11780.363, 122.1324802, 124.1324817, 126.1306802, 126.1551602, 126.3682802, 126.3686402, 126.442802, 126.62942, 126.687602, 126.8168, 128.1324802, 128.136, 140.8406, 142.1324802, 142.1324806, 184.1324806, 188.1324817, 2.126, 200.1324802, 209.1324802, 3.1324802, 3.1324806, 3.1324817, 483.1324806, 7322.1040, 7322.1324802, 7322.453720, 7562.1307280, 7562.1310580, 7562.460920, 7566.128, 7566.372, 7566.9723, 7580.363, 7587.123, 7696.442802, 7877.442802, 8.1540806, 8.1551606, 8406.123, 8406.363. With nothing else they hit every set: a hitting set of 43 none configurations.

**Link-level kills.** K633: d5 0.7322:D2 15, 2.122:D2 14; d6 2.122:D2 65, 2.126:none 68, 2.7566:D2 14, 2.453966:D2 4, 2.79077962:D2 1, 2.79077966:D2 1; d7 122.122:D2 65, 122.126:C2cons 110, 122.7566:D2 22, 126.7562:C2cons 10, 126.7566:C2cons 13, 126.453962:D2 3, 126.453966:D2 5, 122.79077966:D2 1; d8 7322.122:D2 65, 7322.439320:D2 10, 7322.126:C2cons 116, 7326.122:C2cons 50, 7322.453720:none 6, 7562.126:C2cons 69, 7562.7562:C2cons 10, 7562.7566:C2cons 22, 7562.453962:D2 3. K582 enumeration: d5 0.7322:D2 15, 2.122:D2 14; d6 2.122:D2 65, 2.7566:D2 14, 2.453966:D2 4, 2.79077962:D2 1, 2.79077966:D2 1; d7 122.122:D2 65, 122.126:C2cons 110, 122.7566:D2 22, 126.7562:C2cons 10, 126.7566:C2cons 13, 126.453962:D2 3, 126.453966:D2 5, 122.79077966:D2 1; d8 7322.122:D2 65, 7322.439320:D2 10, 7322.126:C2cons 116, 7326.122:C2cons 50, 7562.126:C2cons 69, 7562.7562:C2cons 10, 7562.7566:C2cons 22, 7562.453962:D2 3.

**Re-check on pubrules + rsst_rows** (`fullworld/code/fw_recheck.py`): 154 reported states (argmax states and up to 50 K582 leaves per d) re-evaluated for hi, lo, no proved configuration contained and the none set as reported: 0 disagreements.
<!--/FWTABLES-->

**Findings (§15).**
- Both engines agree on every figure at d = 5..8. That covers the link classes, the no-kill maxima and their argmax, K633 (no positive state at any d), the K582 state counts (0 / 3,917 / 84,292 / 55,752), the number of none configurations (0 / 1 / 29 / 30) and the sole killers (0 / 1 / 26 / 23).
- Because the counts are equal, the state definition above (canonical word, one value per variable from its dominance-reduced domain, no further symmetry reduction) and the dominance rule are the same in both engines. No verdict differs.
- The full world (no domains) needs far more none configurations than the d7/d8 domain sets of §11.
  - The 43 sole killers at d = 5..8 plus the 13 of §13 (5 are shared) give all 51 none configurations.
  - So the domain-free route needs every none configuration. The domain route (§11 plus §13) needs 15.
- d5 and d6 need no proved-modulo-admissibility configuration beyond 2.126:
  - d5: the 29 positive words are all killed at link level by 0.7322 and 2.122 (D2).
  - d6: every one of the 3,917 states needs exactly 2.126.

## 16. RULE2: trigger parts instead of 2.126 and 128.1324802 (RSST-RULE2)

Files: `rule2/` (code, tables, results, logs, REPORT.md, MD5SUMS). Question: can new parts of our own replace the kills by 2.126 (d6) and 128.1324802 (d7) on the 426 full-world leaves RSST-SUB2 left (W6b `round12_rsstsub2/results/cf_still.tsv`), with kills = the 582 proved configurations + the substitutes, and no survivor anywhere?

### 16.1 Grammar and conventions (all parts below)

- A part is written as in §3: hub degree = number of positions; positions 0, 1, ... run ccw around the hub from the anchor; the target is the spoke at position 2; each position is `spoke[hat]`, where the hat is the apex before the spoke (the vertex across the edge to the previous spoke); `*` is free; `=k`, `>=k` are letter ranges, 9 = 9+.
- **Mirror:** the part reflected about its target (pubrules `mirror`), added unless contained in the part. A part symmetric about its target therefore counts once.
- **Amount:** a units are sent from the hub to the target for every fitting (part, anchor). Fits add up, as for the 71 parts. Two occurrences of a configuration at one hub fire separately; a vertex that is the target of several fits receives each.
- Every part below transfers between adjacent vertices, in whole RSST units, and its condition reads only the hub's link letters and the hats (inside the hub's 2-ball). So all of them meet the Lean B4 constraints 1–3.
- **Occurrence geometry.** 2.126 is an edge X b of two 6-vertices whose two common neighbours a, c are 5s. Both X and b are centres. At a centre X the run a b c occupies three consecutive spokes; the other three spokes are the far neighbours: f_a (next to a), f_o (opposite b), f_c (next to c). 128.1324802 is a 7-vertex X with spokes `6, 5, g2, 6, 6, g5, 5` and 5-hats on the edges (spoke 0, spoke 1) and (spoke 3, spoke 4). The two free spokes g2, g5 are its gaps.

### 16.2 The parts tested

| name | hub | spokes [hats], positions 0.. (target = position 2) | amount | targets |
|---|---|---|---|---|
| T1 (W6b) | 6 | `* * >=9 =5 =6 =5` | 2 | f_a (mirror: f_c) |
| T1b (W6b) | 6 | `=5 * >=9 * =5 =6` (own mirror) | 2 | f_o |
| T2 (W6b) | 7 | `=6 =5[=5] >=9 =6 =6[=5] * =5` | 1 | g2 (mirror: the reflected occurrence's g2) |
| T1/T1b link variant | 6 | as T1/T1b with target `>=7` | 2 | as above |
| T2 link variant | 7 | as T2 with target `>=8` | 1 | as above |
| N1 (narrow) | 6 | the hub's whole link fixed to a link word of the 345 2.126 leaves, read from the run: target f_o if f_o has the largest far letter m (amount 2); else f_a and f_c if both have m (1 each); else the one side with m (2). Fires only if m >= 7. Spokes for target f_a: `f_c f_o R =5 =6 =5`; for target f_o: `=5 f_c R f_a =5 =6`, with exact letters (9 = 9+). | 2 / 1 | 45 far-letter triples (`code/r2_parts.py`) |
| N2 (narrow) | 7 | `=6 =5[=5] g2 =6 =6[=5] g5 =5` with (g2, g5) one of the gap pairs of the 81 128.1324802 leaves, exact letters, and g2 >= 8, g2 >= g5 | 1 | g2: pairs (9,7), (9,8), (9,9), (8,8) |

**Pay-through to a 9+ at distance 2** (W6b's two-step proposal). In the Lean form, step 1 is u → w_j and step 2 is a part at hub w_j → s (its 9+ neighbour). For 2.126 with w_j = b, the whole occurrence lies in b's 1-ball, and also for w_j = a or c. For 128.1324802, w_j's 2-ball holds the whole image only when w_j is the gap g2. From the gap g5, the hat on the edge (spoke 0, spoke 1) is at distance 3; from an image spoke at position 0 or 1, the hat on (spoke 3, spoke 4) is at distance 3.

This form is not developed further, because of 16.4(a). No rule that pays into a 9+ vertex within distance 2 of u can discharge those states, whatever its form, its target order or its tie-break.

### 16.3 Method

- **The 426 leaves and their refinements.**
  - Each leaf is read into the §2 window (pubrules + rsst_rows).
  - A leaf's 9 stands for every letter of the variable's dominance class (§13 A.3.2: the letters whose truth pattern over the word's fits equals 9's).
  - For kills, reading 9 as a non-host is sound, because kills are monotone. A rule that needs a 9+ target, however, fires only in the refinements where that vertex really is 9+.
  - So every refinement with all of a rule's possible targets at 5..8 is tested, holding the other variables at 9 (fewest hosts). A DFS with kill pruning then tests every 2-ball variable at 5..8.
- **Full world d6..d8** (`fw_bb_r2`, the §15 engine): per-word fit tables with the new parts added (`code/r2_fwexport.py`, amount 2 written as two unit fits). Mode enum 582, with every leaf exported.
- **Receivers d >= 9** (`d9bb_r2`, the §13 engine): hub tables with the new parts (`code/r2_d9export.py`). The link-word bound's per-letter c+ maxima are read from the table. Mode `maxT` is the maximum over states where some new part fits (sure or possible).
- **Substitute pool** (`code/r2_scheck.py`; every exported leaf, or an evenly spaced sample where marked):
  - the 2026 set `nl51_kc.txt` (8,200 D, b9bc6e8b);
  - all 284 C/D windows W6b screened in rounds 11–13 (`results/w6b_windows_kc.txt`). These include the 13 SUB2 windows and the round-11 windows.
  - Placement is anywhere among the leaf's hosts: injective, letter = degree, induced (W6b's matcher semantics).
  - **Correction (2026-11-10).** This pool is *not* a superset of the SUB/SUB2 substitute set, as the first version of this section said. The extraction kept only W6b's table rows marked C/D, so it left out 26 of W6b's 310 windows. Among them are three of our own validated windows: the SUB2 substitutes fix_50f4aa3e7d and fix_b80e8a0990, and P21 (fix_404d45e819).
    - The refinement results (§16.4, §16.5(a)) are therefore restated with two kill sets. **(P) The proof set** is 582 proved + the 184 SUB/SUB2 substitutes + nl2208_r13 (`results/proofset185_kc.txt`, the same as W6b's proofset184_kc.txt). **(B) The broad pool** is 582 proved + the 2026 set + all 310 W6b C/D windows (`results/pool310_kc.txt`, which is nl51_kc.txt + W6b's pool_all_kc.txt).
    - The receiver and full-world survivors of the 284-window pool (d9: 327; d7: 58 and 651) were screened against the 26 missing windows. None of them is killed, so §16.4's survivor columns and §16.5(b)–(c) stand. (d) has 0 survivors, which a larger pool cannot change.
- **Tail:** the maximum mean of c+ over cyclic link words (Karp). Then charge <= 10(6 - d) + d * mean.

### 16.4 Results

<!--RULE2TABLES-->
**The 426 leaves** (W6b cf_still.tsv, read into the spec window): d6 T (9+ far link neighbour): 197; d6 distance 2 only: 148; d7 T2 (9+ gap): 75; d7 distance 2 only: 6. Charges and contained configurations reproduce W6b exactly (d6: lo = hi = 2, only 2.126; d7: lo = hi = 1, only 128.1324802).

**Refinements of the 154 distance-2 leaves.** Two kill sets: (P) the proof set: 582 proved + the 184 SUB/SUB2 substitutes + nl2208_r13 (`proofset185_kc.txt`); (B) the broad pool: 582 proved + 2026 set (8,200) + all 310 W6b C/D windows (`pool310_kc.txt`).

| target set of the rule (9-valued variables of the leaf) | leaves | refinements with every target at 5..8 | not killed (P) | leaves with one (P) | not killed (B) | leaves with one (B) |
|---|---|---|---|---|---|---|
| every vertex adjacent to the occurrence | 154 | 3952 | 1408 | 49 | 875 | 35 |
| the partner b's three far neighbours (2.126) | 148 | 2368 | 616 | 43 | 107 | 29 |
| the vertex opposite u in b's rotation (2.126) | 148 | 592 | 592 | 148 | 592 | 148 |
| apexes next to the gap spokes (128.1324802) | 6 | 126 | 126 | 6 | 120 | 6 |

Every 2-ball variable at 5..8 (DFS with kill pruning), kill set (P): **49 of 154 leaves** keep a refinement that nothing kills (d6: 43 of 148, so 105 d6 leaves are killed in every refinement; d7: 6 of 6), 0 capped. The witnesses are verified on pubrules + rsst_rows (`results/witnesses_proofset.tsv`): lo = hi = e, no proved configuration and nothing from the kill set contained, only none configurations, no 9+ vertex in u's 2-ball. With N2 added, the d7 witnesses have hi <= -1.

Every 2-ball variable at 5..8 (DFS with kill pruning), kill set (B): **35 of 154 leaves** keep a refinement that nothing kills (d6: 29 of 148, so 119 d6 leaves are killed in every refinement; d7: 6 of 6), 0 capped. The witnesses are verified on pubrules + rsst_rows (`results/witnesses_pool310.tsv`): lo = hi = e, no proved configuration and nothing from the kill set contained, only none configurations, no 9+ vertex in u's 2-ball. With N2 added, the d7 witnesses have hi <= -1.

**Receivers u of degree d >= 9** (d9bb_r2; old = d9plus, 71 parts only; kills K582 in the engine, +2.126 for the N2-only variant; survivors = leaves the substitute pool does not kill):

| d | old: no kills / K582 | variant | no kills, only where a new part fits | K582 max (all states / where a new part fits) | survivors of the pool |
|---|---|---|---|---|---|
| 9 | 24 / 7 | T1/T1b/T2 (target 9+; W6b) | 24 | 14 / 14 | 327 of 3000 (sample of 987768), search incomplete; max hi 6 |
| 9 | 24 / 7 | N1 + N2 (narrow) | 20 | 9 / 9 | - |
| 9 | 24 / 7 | N2 only, with 2.126 as a kill | 14 | 6 / 1 | 0 of 12040 |
| 10 | 20 / 3 | T1/T1b/T2 (target 9+; W6b) | 20 | 12 / 12 | - |
| 10 | 20 / 3 | N1 + N2 (narrow) | 16 | - / - | - |
| 10 | 20 / 3 | N2 only, with 2.126 as a kill | 10 | 3 / <= 0 | 0 of 136 |
| 11 | 16 / <= 0 | T1/T1b/T2 (target 9+; W6b) | 16 | 8 / 8 | - |
| 11 | 16 / <= 0 | N2 only, with 2.126 as a kill | 6 | <= 0 / <= 0 | - |
| 12 | 12 / <= 0 | T1/T1b/T2 (target 9+; W6b) | 12 | 4 / 4 | 0 of 83 |
| 12 | 12 / <= 0 | N2 only, with 2.126 as a kill | 2 | <= 0 / <= 0 | - |
| 13 | 8 / <= 0 | T1/T1b/T2 (target 9+; W6b) | 8 | <= 0 / <= 0 | - |
| 13 | 8 / <= 0 | N2 only, with 2.126 as a kill | <= 0 | <= 0 / <= 0 | - |
| 14 | 4 / <= 0 | T1/T1b/T2 (target 9+; W6b) | 4 | <= 0 / <= 0 | - |
| 14 | 4 / <= 0 | N2 only, with 2.126 as a kill | <= 0 | <= 0 / <= 0 | - |
| 15 | - / - | T1/T1b/T2 (target 9+; W6b) | <= 0 | <= 0 / <= 0 | - |
| 15 | - / - | N2 only, with 2.126 as a kill | <= 0 | <= 0 / <= 0 | - |
| 16 | - / - | T1/T1b/T2 (target 9+; W6b) | <= 0 | <= 0 / <= 0 | - |
| 16 | - / - | N2 only, with 2.126 as a kill | <= 0 | <= 0 / <= 0 | - |
| 17 | - / - | T1/T1b/T2 (target 9+; W6b) | <= 0 | <= 0 / <= 0 | - |
| 17 | - / - | N2 only, with 2.126 as a kill | <= 0 | <= 0 / <= 0 | - |

**Full world d6..d8** (fw_bb_r2; old = fullworld/, 71 parts; K582 leaves = positive states the in-engine kills leave):

| d | variant | K582 leaves: old / new (max hi) | survivors of the pool |
|---|---|---|---|
| 5 | N2 only, with 2.126 as a kill | 0 / 0 | - |
| 6 | T1/T1b >= 7, T2 >= 8 (link variant) | 3917 / 1282 (9) | 0 of 1282 |
| 6 | N1 + N2 (narrow) | 3917 / 2316 (9) | 0 of 2316 |
| 6 | N2 only, with 2.126 as a kill | 3917 / 0 | - |
| 7 | T1/T1b >= 7, T2 >= 8 (link variant) | 84292 / 1540391 (8) | 58 of 4000 (sample of 1540391); max hi 2 |
| 7 | N1 + N2 (narrow) | 84292 / 290715 (6) | 651 of 20000 (sample of 290715); max hi 3 |
| 7 | N2 only, with 2.126 as a kill | 84292 / 60349 (3) | 0 of 60349 |
| 8 | N2 only, with 2.126 as a kill | 55752 / 44470 (8) | 0 of 44470 |

**Tail d >= 15** (max mean of c+ over cyclic link words, Karp; charge <= 10(6 - d) + d * mean):

| tables | max c+ at a 6 / 7 hub | max mean c+ per link edge | bound <= 0 for all d >= |
|---|---|---|---|
| 71 parts (d9plus) | 6 / 6 | 6.0000 | 15 |
| + T1/T1b/T2 (d9tables) | 10 / 6 | 6.6667 | 18 |
| + N1/N2 (d9tables_n) | 7 / 6 | 6.0000 | 15 |
| + N2 only (d9tables_n2) | 6 / 6 | 6.0000 | 15 |

**Substitutes the N2-only variant uses** (RSST-SUB/SUB2 set of 184 tried first, `results/subsub2_set.txt`): 158 distinct (d7 72, d8 67, d9 35, d10 8). Outside that set: nl2208_r13 (1 leaf). Windows: fw_f7c75a21e2 144, fix_63c8a193fe 46, fw_980b7e87e4 35; all are in SUB2's checked set (P20 = fix_63c8a193fe already proved).
<!--/RULE2TABLES-->

### 16.5 Findings

- **(a) No rule that pays into a 9+ vertex within distance 2 can replace either configuration** (counts corrected 2026-11-10; the first version said every one of the 154 leaves keeps a witness). This covers W6b's T1, T1b and T2, the pay-through in any form, and any target order.
  - **The leaves.** There are 154 leaves without a 9+ link vertex next to the occurrence: 148 for 2.126 and 6 for 128.1324802. In each of them the leaf's 9s stand for letters 5..8 as well. A DFS with kill pruning tests every 2-ball variable at 5..8 (§16.4).
  - **Proof set (P).** 105 of the 148 d6 leaves are killed in every refinement. 43 d6 leaves and the 6 d7 leaves keep a witness. Adding P21 changes nothing.
  - **Broad pool (B).** 119 d6 leaves are killed, and 29 d6 + 6 d7 leaves keep a witness.
  - **What a witness is.** A refinement with every vertex of u's 2-ball at 5..8 that is still positive: lo = hi = 2 at d6, and 1 at d7. It contains no proved configuration and nothing from the kill set. Its only RSST configurations are none configurations: 2.126 (a few also contain 7322.1040, 7322.453720 or 126.8168) or 128.1324802. The witnesses are in `results/witnesses_proofset.tsv` and `results/witnesses_pool310.tsv`.
  - **Why no such rule fires there.** A witness has no 9+ vertex within distance 2 of u. So the 43 (P) or 29 (B) witnesses of 2.126 are enough: no rule of this kind replaces 2.126. The 6 d7 witnesses of 128.1324802 have hi = -1 once N2 is added, so they do not touch (d).
  - **The killed leaves.** In the other 105 (P) or 119 (B) d6 leaves, every unkilled positive state has a 9+ vertex within distance 2. There the witness argument does not exclude a 9+-target rule. W6b's "a 9+ vertex is always nearby" therefore holds for those leaves, and for every leaf read with 9 = 9+, but not for the 43 (29).
  - **Narrow targets.** A rule that pays only into the vertex opposite u in b's rotation is excluded in all 148 d6 leaves, under both kill sets.
  - **Agreement.** W6b's second engine (round16/round14_rule2e/RULE2E.md, `code/refine.py`) gives the same outcome leaf by leaf for both kill sets (154 of 154 rows equal).
- **(b) T1/T1b/T2 also break the receivers.** The K582 maxima rise to 14 / 12 / 8 / 4 at d = 9..12 (they were 7 / 3 / <= 0 / <= 0). At d9 the export holds at least 987,768 states, and 327 of an even sample of 3,000 survive the pool (max hi 6). The tail's mean rises to 6.67, but d = 15..17 still have no positive state even without kills.
- **(c) Link targets close the senders but not the receivers.** With targets of letter >= 7 (T1/T1b) and >= 8 (T2), every leaf has an exact link target. d6 then closes (0 survivors, also with the narrow N1). The 7-vertices that receive the 2.126 triggers do not close: 58 of 4,000 sampled d7 leaves survive (broad version, 1,540,391 leaves), and 651 of 20,000 (narrow N1, 290,715 leaves). Every survivor contains 2.126.
  - The 38 leaves whose largest far letter is 7 can pay only into that 7-vertex, or into a 9+ at distance 2. (a) excludes the second option for 9 of the 38 under both kill sets; the corrected (a) does not decide the other 29. The conclusion below rests on the d7 survivors, not on this point.
  - So **2.126 is still needed** as a kill with rules of this family.
- **(d) 128.1324802 can be replaced.** Rules = 71 parts + N2 (4 gap pairs with mirrors: 8 unit parts, amount 1, adjacent, conditions on the hub's link and two hats). Kills = 582 proved + 2.126 + substitutes. There are 0 survivors at every degree:

  | d | positive states unkilled by the 582 proved configurations and 2.126 | after the substitutes |
  |---|---|---|
  | 5 | 0 | 0 |
  | 6 | 0 | 0 |
  | 7 | 60,349 | 0 |
  | 8 | 44,470 | 0 |
  | 9 | 12,040 | 0 |
  | 10 | 136 | 0 |
  | 11..17 | none (max <= 0) | 0 |

  - Tail d >= 18: the c+ table is unchanged (mean 6). The bound <= 0 holds for d >= 15; d = 15..17 are also searched exactly.
  - Every leaf was checked, with no sampling: 158 substitutes in all, every one in the RSST-SUB/SUB2 set except **nl2208_r13** (2026 set, 1 d8 leaf). The windows used are fw_f7c75a21e2 (C), fix_63c8a193fe (P20) and fw_980b7e87e4 (D), all in SUB2's checked set.
  - A pubrules + rsst_rows re-check of 160 leaves (40 per run, N2 included) gives 0 disagreements.
- **(e) Largest final charge where the new parts fire** (receivers, `maxT`):

  | rules | kills | d9 | d10 | d11 |
  |---|---|---|---|---|
  | N2 | none | 14 | 10 | 6 |
  | N2 | 582 + 2.126 | 1 | <= 0 | <= 0 |
  | W6b's T1/T1b/T2 | none | 24 | 20 | 16 |
  | W6b's T1/T1b/T2 | 582 | 14 | 12 | 8 |

  With N2, every state where the new part fires and the charge is positive (d9: max 1) is killed by a substitute.


## 17. Rotation-aware kills (RSST-ROT)

W6r, 11 Nov 2026, [P]. Code: `rot/code/` (rot.py, gen_configs.py, fw_bb_rot.cpp, d9bb_rot.cpp, xcheck_contain.py, rot_leaves.py).

### 17.1 Why

- The matchers in §2–§16 test only an injective, induced, degree-exact embedding of a configuration's interior into the window's hosts. They do not check cyclic order.
- Such an embedding can mirror one block of the configuration across a 1- or 2-vertex cut of its interior. That placement is not a real occurrence (RotOcc / OccursCXF needs the host's rotation at every interior vertex).
- §17 adds the missing condition. Plain kills overcount: a state killed only by a mirrored placement is not killed.

### 17.2 The configuration's rotation

- kc line `name r m ra ia`. Take the ring cycle 0..r-1, the interior, and one hub joined to every ring vertex. This is a simple sphere triangulation; the code checks that every vertex link is a cycle and that E = 3V - 6.
- A sphere triangulation's rotation system is unique up to one global reflection. So the rotation is computed from the graph: each link cycle is oriented by propagation (a face (v, a, b) read at v means b is followed by v at a), and the orientation is checked on every edge.
- For the 583 RSST configurations, the result equals unavoidable.conf's own cyclic lists in the same orientation (583 of 583, asserted). The kc rotation does not depend on how kc orders its lists.

### 17.3 The host's rotation (fw_bb numbering)

- u's rotation is w_0..w_{d-1}.
- w_j's rotation is (u, w_{j-1}, s_{j-1}, p_j.1..k, s_j, w_{j+1}), which is complete. A 9+ site is drawn as an 8, as before, and is never a host.
- An apex or private has as its rotation the arc of its window neighbours, read off the oriented faces of the w_j, followed by deg - |arc| ring-3 slots. The arc always has at most 4 vertices, so at least one ring-3 slot exists at every letter 5..8.

### 17.4 Matching rule

An embedding phi counts as a kill only if it is injective, induced and degree-exact (as before), and in addition one sign sigma in {+1, -1} works for the whole embedding, as follows. At every interior vertex x, place K's rotation at x on the host rotation at phi(x), reversed when sigma = -1, anchored at one interior neighbour. Every interior neighbour y of x must then land on the slot of phi(y).

- Ring neighbours of K are free: any slot, known or ring 3.
- This is B6's RotOcc condition with one global chirality.
- The check is applied to each complete embedding; the search moves on to the next embedding when it fails. Containment stays monotone in the hosts, so pruning at partial assignments stays sound.
- The dihedral reduction of link words stays valid: reflecting the window maps a respecting embedding with sigma to one with -sigma.

### 17.5 Validation

- **Mirror demo, d7 link 5567757, Studio K768** (st127/k767_kc.txt, 768 configurations): all embeddings into the window with free apex and private letters.
  - 256 respect rotation and 30 do not.
  - The configurations whose only embeddings are mirrored are nl0078_r11, rsst163, rsst173, rsst213 and rsst248, as the Studio reports.
- **K768:** the K768 here (582 + 2.126 + proofset185, `rot/k768/`) has the same 768 names as the Studio's.
- **C++ against Python:** on 3,000 random filled 2-balls (d = 5..12), fw_bb_rot's contain mode equals rot.py, both with rotation (7,756 hits) and without (7,862). 97 states differ between the two modes.
- **Regression:** at d7 with K583 and ROT=0 the engine gives the rule2 count of 60,349 leaves. With ROT=1 it gives 60,659 = 60,349 + 310 leaves that have only a mirrored K583 kill.

### 17.6 Full world, 79 parts (71 + N2), kills K768 rotation-aware

The run is complete and exact at d5..d14 (enum, every positive leaf exported). The tail d >= 15 is unchanged: the c+ table is the rule2 N2 one, with mean 6 and bound <= 0 for d >= 15; the bound does not use kills.

| d | positive leaves with no rotation-respecting kill | link words | max hi | with a plain (mirrored) K768 kill | with no kill at all |
|---|---|---|---|---|---|
| 5, 6 | 0 | – | – | – | 0 |
| 7 | 2,590 | 46 | 1 | 2,590 | 0 |
| 8 | 1,370 | 30 | 2 | 1,370 | 0 |
| 9 | 406 | 18 | 3 | 406 | 0 |
| 10 | 32 | 2 | 2 | 32 | 0 |
| 11..14 | 0 | – | – | – | 0 |

- **Every one of the 4,398 leaves is re-checked on rot.py.** None of them contains a K768 configuration with a rotation-respecting embedding. Each has at least one configuration whose only embeddings are mirrored, and the engine's plain killer is among them (0 mismatches). They are listed in `rot/results/mirror_only_states.tsv`.
- **Configurations that kill only by mirroring**, with the number of leaves:
  - substitutes: nl0078_r11 2,349; nl3352_r13 1,012; nl0194_r12 374; fw_f7c75a21e2 68; nl0019_r11 58; nl0026_r12 41; nl5458_r16 36; fw_980b7e87e4 25; nl1998_r14 13; nl2892_r13 6; nl1681_r12 4; nl5979_r14 3;
  - RSST configurations: rsst213 225; rsst438 202; rsst489 115; rsst167 8; rsst040 6; rsst062 2.
  - In 4,249 leaves exactly one configuration is mirror-only.
- **What a leaf stands for:** a leaf is dominance-reduced, with 9 = 9+ read as a non-host. Some states it stands for may contain a real occurrence once a 9 is refined. The leaves are what the engine cannot close as it stands; each needs a real substitute, or a split.
- **Plain matching, for comparison:** K768 kills every positive state at every degree (§16.5(d)). So plain matching overstated the kills on exactly these 4,398 leaves.
