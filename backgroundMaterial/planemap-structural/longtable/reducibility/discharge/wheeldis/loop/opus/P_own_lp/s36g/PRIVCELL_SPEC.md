# PRIVCELL_SPEC: private-cell names, their action on the engine's rows, and a twoeng guard (Opus s36g)

Long Table asked for this. It has three parts:

1. a name grammar that can carry private and ring-3 slots;
2. what such a name does to each row type of our engine, with a verdict on LT's mask hypothesis;
3. a guard rule for Studio's twoeng side.

Part 4 records the prototype (`s36g/eng`, a copy of `s28q/eng`) and its checks. No solve was run, and every check used
threads = 1.

The background specs are RELAY_SPEC §14′ (the strict unknown rule and the filt16 kill tables), RELAY_SPEC_s21 (l3q) and
RELAY_SPEC_s20 §s25c-g (how g7_ names are read). This spec replaces nothing in them. A `g7_` name stays readable as
before, and Part 1.6 converts it to the new form.

---

## Part 1. Name grammar (`q` names)

### 1.1 The frame

The frame is the u-frame of §14′/§s25c-g.1:

- **Centre and link.** The centre u has degree d. Its link is w_0..w_{d-1}, and the apex s_i is adjacent to w_i and
  w_{i+1}.
- **Privates.** w_i has n_i = deg(w_i) − 5 privates: its neighbours that are neither u, w_{i±1}, s_{i-1} nor s_i. In
  ring-2 order they run from the s_{i-1} side to the s_i side, so the ring-2 cycle reads
  … s_{i-1}, p_{i,1}, …, p_{i,n_i}, s_i, ….
- **Ring 3.** Ring-3 vertices are the vertices outside the 2-ball that are adjacent to ring 2.

The 2-ball is assumed to be this disc, as in §14′.

### 1.2 Syntax

```
name   := 'q' D C '_' LINK '_' SWORD '_' PRIV [ '_' R3 ]
D      := decimal centre degree of the frame (>= 5)
C      := 'u'  the centre is in the configuration (interior) with exact degree D
        | '-'  the centre is not in it (its degree is unconstrained; see 1.4 for where the name can be placed)
LINK   := D chars, slot w_i          SWORD := D chars, slot s_i
PRIV   := D groups joined by ':' ; group i holds the privates of w_i:
            ''                  no private of w_i is constrained
            c_1 .. c_n          (only when LINK[i] is an exact 5..8, so n = n_i): p_{i,1} .. p_{i,n}, all n_i
                                chars written, free ones as '.' (1.9 point 4)
            c_1..c_a '*' c'_b..c'_1   (only when LINK[i] is not exact): p_{i,L1..La} from the s_{i-1} end,
                                p_{i,Rb..R1} from the s_i end; the name requires n_i >= a + b (distinct vertices);
                                the '*' is always written, so an empty R part gives 'L*' and an empty L part '*R'
                                (1.9 point 3)
R3     := items joined by ',' ; item := CHAIN '=' c
CHAIN  := LAB '/' LAB ['/' LAB ..]   the ring-3 vertex adjacent to these consecutive ring-2 vertices, ALWAYS written
                                     in forward ring-2 order (s_{i-1}, p_{i,L1}, .., p_{i,R1}, s_i, ..; 1.9 point 1)
        | LAB '#' k                  the k-th ring-3 neighbour of LAB, counted from its ring-2 predecessor's side
LAB    := 's'i | 'p'i'L'k | 'p'i'R'k    (exact parent: always written 'L'k, k = 1..n_i)
c      := '.' | '5' | '6' | '7' | '8' | 'B' | '9'
```

The meaning of each char:

| char | meaning | letter set (LP letters 5..9, 9 = ≥ 9) |
|---|---|---|
| `.` | free: no constraint, and the slot is not a vertex of the pattern | – |
| `5`–`8` | exact degree (an interior vertex) | {k} |
| `B` | open ≥ 7 | {7, 8, 9} |
| `9` | open ≥ 9 | {9} |

### 1.3 Unknown and ≥ 9 slots (strict §14′)

- **No exact 9.** `9` is never an exact degree. The exact chars `5`–`8` never match an LP letter 9, because that letter
  means ≥ 9.
- **Open chars.** `9` and `B` are open sets. They are legal in the grammar for hand-written filters, but the guard
  (Part 3) admits no two-engine name that has them.
- **Unknown cannot be written.** A name cannot ask for "unknown". Unknown is a property of the *context* that a row
  reads, not of the name.
- **Matching rule.** A name instance fires on a context only if **every constrained slot (every non-`.`) lies on a
  vertex the context reads exactly**, and that vertex's letter is in the slot's set.
- **Unknowns never match.** A constrained slot that falls on an unknown never matches, whatever its char, including `B`
  and `9`. This is the §14′ rule word for word.
- **Free slots.** A free slot imposes nothing and may fall on an unknown.

### 1.4 Canonical form, symmetry and placement

**Symmetries.** The 2D symmetries of the frame are the rotations r and the reflections:

| | rotation r | reflection (i → r − i) |
|---|---|---|
| w_i | w_{i+r} | w_{r−i} |
| s_i | s_{i+r} | s_{r−i−1} |
| p_{i,Lk} / p_{i,Rk} | p_{i+r,Lk} / p_{i+r,Rk} | p_{r−i,Rk} / p_{r−i,Lk} |
| chains | — | reversed, so they stay in forward ring-2 order |
| y#k | — | y'#(m+1−k), where m is y's ring-3 count (needs y exact, 1.5) |

After each image, a label p_{i,Rk} with an exact parent is rewritten as p_{i,L(n_i+1−k)}.

**Canonical form.** The canonical name is the bytewise minimum of the rendered string over the 2D images. Rendering
also normalises:

- a group of an exact parent that has no constrained private is written `''`;
- in a non-exact group, trailing free chars of the L part and leading free chars of the R part are dropped, and the
  `*` stays even when one side is empty (`5*`, `*5`);
- every chain is put in forward ring-2 order, cyclically (after a reflection this is the reversed chain). A name whose
  chain is not written forward is read, but it is not canonical, so it fails G0's round-trip until rewritten;
- R3 items are sorted.

The loader canonicalises on read, and two names are the same name iff their canonical strings are equal. (Code:
`pc_canon` in `eng/privcell.py`. Every converted g7 name round-trips: `pc_canon(pc_parse(c)) == c`.)

**Placement degree.**

- A `u` name is placed only at centre degree d' = D.
- A `-` name is placed at d' = D and at every d' ≥ max(5, |A| + 1). Here A is the minimal cyclic interval of link
  positions the name touches:
  - w_i touches i;
  - s_i touches i and i + 1;
  - p_{i,·} touches i;
  - a chain touches its labels' positions.
- |A| + 1 keeps the first and last touched spokes non-adjacent, so the induced pattern is the same at every such d'.
  Offsets along A are kept; no wrap-around is allowed.

### 1.5 Name → containment pattern

**Vertex list.** The vertex list is the constrained slots, each with its letter set:

- u (with {D}) if C = `u`;
- every w_i and s_i not `.`;
- every constrained private;
- every R3 item.

**Edges.** The edges are the frame adjacencies among the listed vertices (the same list Studio's g7_check (c) uses):

- u–w_i, w_i–w_{i+1}, w_i–s_{i-1} and w_i–s_i;
- w_i–p_{i,·};
- the ring-2 chain s_{i-1}–p_{i,1}–…–p_{i,n}–s_i when n_i is exact. When n_i = 0 this is the edge s_{i-1}–s_i. When
  w_i is not exact, only the end pieces s_{i-1}–p_{i,L1}–…–p_{i,La} and p_{i,Rb}–…–p_{i,R1}–s_i are determined;
- t–each label of its chain, and t(y#k)–y.

**Faces.** The faces are the frame triangles among the listed vertices (and, for G5, every 3-cycle of listed vertices
must be one of them; 1.9 point 5): (u, w_i, w_{i+1}), (w_i, w_{i+1}, s_i),
(w_i, consecutive ring-2 pair of its chain) and (t, consecutive chain pair).

**Determinacy (well-formedness).** A name is well formed only if every label and adjacency it uses is fixed by its own
exact degrees:

- An exact-parent private needs k ≤ n_i.
- A chain x/y must be consecutive in ring 2. For example, s_{i-1}/s_i needs w_i = `5`, and p_{i,Ln}/s_i needs an exact
  parent.
- y#k needs y exact. Its ring-3 count is m = deg − 4 for an apex and deg − 3 for a private.
- Two ring-3 vertices that share a ring-2 neighbour are never declared adjacent by the frame. If the configuration has
  such an edge, the name under-describes it, and the guard (3.1 G4) holds the name.

**Slot form.** For the LP side, the pattern's *slot form* is the map {slot → letter set}, as in `pcheck.pname`: an
f-name is the special case with an empty PRIV group everywhere and no R3. Code: `pc_pattern(N)` (vertex list and
edges) and `pc_arc(N)`.

### 1.6 g7_ → q

A g7 name `g7_<C><W>_<S>_<T>` is written on the fixed row R* = 7 7665566/6765766. Its frame degrees of w are known
(7665566), and so is its slot order: p01 p02 p11 p21 p51 p61 t(p21/s2) t(s2/s3/s4) t(s4) t(p51/s4).

The conversion (`g7_to_q`):

- **Centre, link, apexes.** d = 7. C, W and S are copied.
- **A private whose parent the name pins.** It becomes L k.
- **A private whose parent is `.`.** It keeps the frame adjacency to a named apex. An apex counts as named for p_{I,K}
  if its own slot is constrained, or if a constrained ring-3 slot's chain contains both p_{I,K} and that apex
  (1.9 point 2):
  - L1 if it is the first private and s_{I-1} is named for it;
  - R1 if it is the last private and s_I is named for it;
  - if both apply with n = 1, the name cannot be written without pinning w_I, and the converter refuses it. This does
    not happen for the 10 names.
- **Ring-3 slots.**
  - t(a/b/..) becomes a chain in forward ring-2 order, **sorted after the labels are converted**, whatever order the g7
    slot is spelt in. For example t(p51/s4) is spelt backwards: forward order is s4/p5L1, which the reflection in
    #5 turns into p3R1/s3.
  - t(s4) becomes s4#2, the middle one of s4's three ring-3 neighbours t(s2/s3/s4), t(s4), t(s4/p51); it needs s4
    exact, and s4 = 7 in that name.

The 10 names of `s25c/g7_names.txt` in canonical q-form (`s36g/g7_q.txt`):

| # | g7 name | q name (canonical) | Studio verdict |
|---|---|---|---|
| 1 | g7_-..655.._..65..._...5...... | `q7-_....556_....56._::::::5` | D, ring 8 |
| 2 | g7_u76.5566_6..5..._..5....... | `q7u_.556676_.5...6._::::::5` | C X={I0-I2}, ring 14 |
| 3 | g7_-..655.._..65..._...5..5... | `q7-_....556_....56._::::::5_s5/p6L1=5` | D, ring 8 |
| 4 | g7_u..655.._..65..._...5..5... | `q7u_....556_....56._::::::5_s5/p6L1=5` | D, ring 9 |
| 5 | g7_-..655.._..657.._...5.....5 | `q7-_....556_...756._::::::5_p3R1/s3=5` | C, ring 11 |
| 6 | g7_-..655.._..657.._...5....5. | `q7-_....556_...756._::::::5_s3#2=5` | C, ring 11 |
| 7 | g7_-.6655.._..65..._..55...... | `q7-_...5566_...56.._:::::5:5` | C, ring 11 |
| 8 | g7_-..655.._.765..._..55...... | `q7-_....556_....567_5*::::::5` | C, ring 11 |
| 9 | g7_-.6655.._.765..._..55...... | `q7-_...5566_...567._:::::5:5` | C, ring 11 |
| 10 | g7_u7665566_6.65..._..5...5... | `q7u_5566766_5...6.6_:::::5:_p6L1/s6=5` | D, ring 15 |

The patterns (vertex list and edges) of all 10 are printed in `s36g/selftest.log`. `s36g/framecheck.py` checks them
against the kc lines of Studio's held file (origin/main `loop/studio/sender_held/g7_53/held53_7_7665566_6765766.txt`).
All 10 have the same vertex set and degrees as the m interior vertices, and their interior–interior kc edges **equal**
the pattern edges, which is stronger than "forced ⊆ kc" (`framecheck.log`, 0 failures).

### 1.9 Resolved ambiguities (Studio 9a4c2e79)

These are Studio's seven points from `loop/studio/opus_check/privcell_verdict.md` (9a4c2e79, merge fb968de7). The rule
text above has been edited so each point reads on its own.

1. **Chain order when a g7 slot is not spelt forward (#5). Adopted.** A chain is always written in forward ring-2 order,
   cyclically, so it reads s_{i-1}, p_{i,L1}, .., p_{i,R1}, s_i, and the start is placed after the largest cyclic gap.
   - The converter now sorts each chain after converting its labels, and every image re-sorts. Before the fix it kept
     the g7 slot's literal order t(p51/s4) and then reversed it under reflection, so #5 came out as `s3/p3R1`.
   - #5 is now `..._p3R1/s3=5`. The pattern is unchanged; only the string, and therefore name identity and dedup,
     changed.
   - A non-forward chain is still read, but it is not canonical (1.4).
2. **"Shares a chain with a named private" (1.6). Replaced by a precise rule.** An apex counts as named for p_{I,K} if
   its own slot is constrained, *or* if a constrained ring-3 chain contains both p_{I,K} and that apex. Then L1 is
   used next to a named s_{I-1}, and R1 next to a named s_I.
   - The old clause meant this, but its wording did not.
   - It is not exercised by the 10 names: wherever it would apply, the apex is also named directly. So Studio's
     reading, the two apex clauses only, gives the same result on all 10.
   - The extra clause matters only for a name that pins t(p/s) but leaves s free.
3. **R-empty non-exact group. Adopted:** written `L*`, and an L-empty group `*R`. The `*` is never dropped. #8's `5*`
   is this case.
4. **Exact-parent group. Adopted:** written with all n_i chars, free ones as `.`. For example, a 7 with only its
   second private constrained is `.5`.
5. **G5 triangles. Adopted:** every 3-cycle among the kc interior vertices must be a frame face.
   - This is at least as strict as reading "interior face": a separating interior 3-cycle is held. That is the safe
     direction, because the frame disc has no separating triangle among named vertices.
   - Face counts agree on all 10.
6. **The u centre is a constrained slot. Adopted:** for C = `u` it is a vertex of the pattern (1.5) with degree D, and
   it takes part in G3's bijection. This matches every m here (#2: 10, #4: 8, #10: 13).
7. **k3p lines and the absorption class. Adopted:** there is no required class. The coordinator's suggestion is
   adopted as an optional, ignorable `class=` token (3.1).
   - Values: `amask`, `l3q`, `fpat`, `sepx`, `M2`, `r3h`, `cluster`. `sepx` is added for case A′, which needs
     separator state only.
   - Opus's reading for the 10 names:

     | # | class |
     |---|---|
     | 1 | amask |
     | 2 | sepx |
     | 3, 4, 5, 6, 10 | r3h,cluster |
     | 7, 8, 9 | M2,cluster |

**Status.** After the fix, all 10 canonical strings in `s36g/g7_q.txt` are byte-identical to Studio's table, and the
checks (Part 4) were re-run.

---

## Part 2. Loader and parser semantics, by row type

**Common rule.** A name acts on a row through a **mask slot**: the one vertex whose letter the row ranges over in a
max or min term, or whose value it enumerates.

- For each context the row reads, the loader places every image of the name (1.4).
- An image *absorbs* at that context iff:
  - (i) its constrained slots, other than the mask slot, all lie in the readable set R of the row type;
  - (ii) their letters are in the slot sets;
  - (iii) the mask slot is the only constrained vertex outside R.
- The letters of the image's mask-slot set are then removed from the mask. With no mask slot (an f-name), the context
  itself is removed.
- **Union rule.** Several names may jointly kill a letter or a context. Removal is sound iff, for every completion of
  the other unread slots, some name fires. Only the single-name case is implemented. No g7 name gains from the union
  rule; see 2.2.

**Soundness.** A minimal counterexample contains no reducible configuration. Removing a letter that some embedding needs
at that letter, or a context in which some configuration embeds, only discards impossible cases. The strict rule (1.3)
makes every embedding use only vertices the row actually knows.

### 2.1 receiverR2 (lowerR2 rows; separator jsep3 / jsep5, exhaustive for d = 7..17; Karp tail for d ≥ 18)

**R** (what the row reads exactly):

- the centre u, of exact degree d;
- the link w (letters 5..9);
- the apexes s.
- In the window and class tables, U = min(d, 9), so at d ≥ 9 the window does not know d exactly.

The row reads no private and no ring-3 vertex. The privates of a 6 at w_j enter only through
`M[(sig2, mask)] = max over p in mask of h(U, w_{j+1}, s_j, p, s_{j-1}, w_{j-1}; classes)`, and the mask is the filt16
amask of the window. That window is a = w_{j−2}, b = w_{j−1}, e = w_{j+1}, f = w_{j+2}, and s_{j−2..j+1}.

What a name does here:

| Case | Name shape | Effect | Where it acts |
|---|---|---|---|
| (F) | No private or R3 constraint (an f-name) | A receiver pattern: the context is not admissible. Added to `PATS[d']` | `admissible()` (lowerR2) and the separator's pattern masks (the sep3-style 4×5-bit slot masks), for every d' in 7..17 placeable by 1.4; a `-` name gets one slot form per d' |
| (A) | Exactly one constrained private, of a spoke that can be a 6 (p_{j,L1} or p_{j,R1}, parent set ∋ 6); every other constrained slot in the 9-slot window around j, with w_j ∋ 6 | Absorbed as amask bits (2.3): M's mask loses those letters | One function, `amask`, feeds lowerR2 (`recv_coef_R2`), the separator window table (`window_table_R2`, c = 1 entries) and the tail (W9). The class table already splits c = 1 by (a, b, e, f, q, r, p, s), so upper and lower stay consistent with no class change. A centre-free name acts at U = 7, 8 and 9; a `u` name only at U = d ≤ 8, because U = 9 means d ≥ 9 and is not exact |
| (A′) | One 6-private, but a constrained slot outside the 9-slot window (g7 #2: around its 6 at w6 it needs w2, w3 and s1, i.e. w_{j+3}, w_{j+4} and s_{j+2}, with the centre) | **Expressible in the LP with no new column**: the M family is keyed by (sig2, mask), and a wider mask only adds keys | Not absorbable in the separator as it stands: the window table cannot evaluate a mask that reads beyond the window. It needs new separator state, either a wider window or, for `u` names at d = 7, a jsep5-style leaf correction on M like the l3q one (RELAY_SPEC_s21 §21.6). Not prototyped, so the name is logged "not absorbed" |
| (L) | One private of a 7-spoke adjacent to an apex, with every other constrained slot in the l3q window | Absorbed as l3q mask bits (2.4) | — |
| (X) | **Two or more constrained privates on different spokes, or any R3 constraint** | Not absorbable as a mask on this row. This is **LP-visible only with a new variable family** (2.6) | — |

### 2.2 senderR2

**R:** the five v (degree 5) and its link w, exactly. Hats h_k and the fans of 6-spokes are read **as classes only**:
CLS2 0 = {5, 6} and 1 = {7, 8, 9}. The row's own existential check (`allow`: some exact (hat, fan, hat) in the classes
makes each 6-wheel non-R6) enumerates exact letters inside the classes, but the row's terms do not depend on them.

A sender context (H, Fn) can be dropped only if **every** exact completion inside its classes is killed. An exact
interior letter (`5`, `6`) kills one letter of a two-letter class, so it never closes a class. Only `B` on a big-class
slot does that, and `B` is not an exact degree.

- **Result.** A two-engine private-cell name is never absorbed by a sender row on its own. It acts only when all its
  constrained slots are on v's link, which makes it an R5-type link kill, already handled through `isR5`.
- **Mechanism.** There is one for context skips if one is ever needed: the `wf19` skip list (`R2_sender_rows`). No
  "sender sep3 mask" exists in our engine. The sep3-style masks are the receiver slot masks of 2.1 (F), and they read
  only link and apex slots, never privates.
- **g7 names.** Seen from the five w3 next to the 6 w2 (g7 coordinates), every g7 name pins the 6's private hat (p21)
  to exactly 5. The class {5, 6} survives through 6, so none of the 10 names, alone or together, drops a sender
  context.

### 2.3 filt16 3-ball kill tables (`KT[U][a,b,e,f,s0,s1,s2,s3]`, bit i = letter 5+i killed)

This is the storage behind 2.1 (A). An absorbed name ORs its mask-slot letters into
`KT[U][window letters in the name's sets]`, for every image:

- for a centre-free name, U ∈ {7, 8, 9};
- for a `u` name with d = 7, U = 7;
- for a `u` name with d = 8, U = 8.

The prototype holds these bits in a separate array (`PCAM`) and applies them inside `amask`, so the .npy files are not
touched. Writing them into a new `kill6pc_U*.npy` would be the same thing.

**U = 8 note (§14′ correction).** The shipped KT8 = KT9, because u is unknown at U = 8 there. A `u`-8 name makes
KT8 ≠ KT9. That is sound: U = 8 rows have exactly d = 8.

**What the tables could not express.** It is exactly the 2.1 (A′) and (X) names. The table index *is* the window: one
6, its single private and nothing else.

### 2.4 l3q masks (`L3T[(σ, c, w2, w3, w4, a, o)]`, RELAY_SPEC_s21 §21.4)

**R:** the payee v (d = 7, letter 7), the payer u = w_j (7), w_{j+σ..j+4σ} = (c, w2, w3, w4), the apex a = s_j
(σ = +1) or s_{j−1} (σ = −1), and the other apex o. The free slot is a2, u's private adjacent to a.

- **When it absorbs.** A name absorbs iff:
  - it has exactly one constrained private, of a spoke that can be a 7;
  - that private is adjacent to an apex:
    - L1 (or R2): next to s_{j−1}, giving σ = −1;
    - L2 (or R1): next to s_j, giving σ = +1;
  - every other constrained slot lies in R;
  - the name is placeable at d' = 7.
- **Effect.** L3T[key] loses the name's letters for every key with c, a ≤ 6 that is consistent with the name's sets.
  Qeff and the mrowL check in lowerR2 then read the smaller mask.
- **Same reading as Studio.** Only an embedding that uses a2 kills a letter. A name without the a2 slot is not an l3q
  name; it is (F) or nothing.
- **Unreadable.** Here, as in the table builder, unreadable means w_{j−σ}, w_{j−2σ}, the other apexes and every other
  private.
- **g7 names.** None of the 10 constrains a private of a 7 (p01 and p02 are free in all of them), so L3T is unchanged.

### 2.5 Cluster rows (s25c `pricer25g7.py`: the binder's cell rows)

A cluster row of a receiver (d, w, s) enumerates, **exactly**, the privates of its link spokes and the ring-3 slots it
names. That is the *cell*. In each cell, the binder's M terms become the exact h of the cell's privates.

- A name acts by **cell kill**: a cell is dead iff, for every completion of the enumerated ring-3 letters, some image of
  some name fires on known vertices only. This is the strict rule; `cell_dead` implements it.
- This is the only row type here on which (X) names act.
- The cluster rows themselves use **existing columns** (h, and the binder's other terms). They are a row split, not a
  new column.
- On the st24bL binder 7665566/6675676, the 10 names give these cell constraints:
  - {p51:5} and {p61:5};
  - {p51:5, t:5} ×4;
  - {p61:5, p51:5} ×3;
  - {p61:5, t:5}.
  
  The g7 kills alone already break cert_st24bL (s25c: h with p51 = 5 at −3/13).

### 2.6 Verdict on LT's hypothesis, and the kill line

**Hypothesis.** "A private-cell kill can be expressed as a mask on existing rows, with no new LP column."

**True (a mask on an existing row, no new column)** for:

1. **filt16 kill-table bits = the receiverR2 M mask.** This covers one 6-private with every other constraint inside
   its 9-slot window, for a centre-free name or a `u` name with d ≤ 8. It acts the same way in lowerR2, in the
   d = 7..17 sweep and in the tail.
2. **l3q mask bits.** This covers one 7-private adjacent to an apex, inside the l3q window, at d = 7.
3. **Receiver f-patterns (sep3-style slot masks).** These are names with no private or ring-3 constraint.
4. **cons2 row skip.** This applies to a name whose constrained slots all lie in one 6's closed 2-ball (link plus six
   apexes), with that 6 at w_i. The cons2 row (L, s) of that 6 is vacuous and can be skipped. lowerR2 must then reject
   a cert that uses a skipped row. This is *reported, not applied* by the prototype (logged `cons2-row skip possible`).
   It holds for g7 #1, #3, #4, #7, #8 and #9. Note that it relaxes conservation only; it does not touch M.
5. **Cluster cell kills.** These are on the split rows of 2.5, which use existing columns.

**Not a mask on the existing rows; LT's kill line:**

- **receiverR2 with two or more constrained privates on different spokes (case X; g7 #7, #8, #9).**
  - The receiver row's dependence on privates is separable: Σ_j M_j, with M_j = max over p_j in mask_j.
  - A joint kill removes a non-rectangular set of cells from Π_j mask_j. Any per-spoke mask that is sound must keep
    every letter that survives with *some* letter of the other spoke, so it keeps everything, and the gain is zero.
  - To use the kill, the row needs a variable equal to the joint maximum: **a new variable family M2[(two-spoke
    window, joint mask)] ≥ h_j + h_{j'}** over the surviving joint cells. The separator then needs a two-spoke window
    term, which is new state for jsep3 and jsep5.
  - The alternative is cluster rows (2.5). They avoid the new column, but only on listed binder rows; they do not
    cover the exhaustive d = 7..17 sweep.
- **receiverR2 with any ring-3 constraint (case X; g7 #3, #4, #5, #6, #10).**
  - No receiver term reads ring 3. The key of h stops at the 6's link plus the two apex classes next to u. A ring-3
    vertex such as t(s5/p6L1) is one of the 6's *other* apexes, which only cons2 reads.
  - A kill conditional on t cannot shrink a max over p unless it holds for every t. That is the union rule, and it does
    not hold for any of these names.
  - Using it needs **h split by that apex**: a new h family keyed on more of the 6's 2-ball, with M and cons2 re-keyed
    to match. That is a new variable family. Cluster rows are again the no-new-column route, on listed rows only.
  - #3 and #4 are also inside w6's 2-ball and can be cons2 skips (item 4), but that does not reach M.
- **receiverR2, one private outside the window (case A′, g7 #2).** This needs no new family but does need new separator
  state (2.1). It is listed so it is not mistaken for a mask.

**The 10 g7 names in one line:** 1 absorbed as an existing mask (#1, amask), 1 needs separator state only (#2), and 8
need a new variable family or cluster rows (#3–#10). Six of them (#1, #3, #4, #7, #8, #9) are additionally cons2-skip
candidates.

---

## Part 3. twoeng guard rule for private-cell names (Studio's checker side)

### 3.1 Rule

A two-engine name in q-form, or any form the converter maps to q-form, is **admitted to the private-cell list**
(`k3p_D.out` / `k3p_C.cfast`, never k3x) iff all of the following hold.

- **G0 (form).** The name parses and is well formed (1.5 determinacy). It is written canonically, or the loader
  canonicalises it and dedups.
  - Prefix: the existing k3x `plain()` guard (0339586b) already holds every `q` and `g7` name out of k3x. This rule
    adds a second, separate output and leaves k3x unchanged.
- **G1 (two engines).** As for k3x:
  - D means kc D and dfast18 D.
  - C means kc C-REDUCIBLE X and cfast `--fixed X` with leftover 0.
- **G2 (ring-merge).** For C: run the union-find of `out/job30/twoeng.py ringmerge` on X. If a component holds two or
  more ring vertices, the name is held. X must merge interior vertices only.
- **G3 (interior = named).** There is a bijection between the kc line's m interior vertices and the name's constrained
  slots, with equal exact degrees. For C = `u` the centre is one of those slots, with degree D (1.9 point 6). This is Studio's g7_check (a) and (b).
  - Every constrained slot is an exact `5`–`8`.
  - A `9` or `B` anywhere means held. This is the letter-9 rule: an LP letter 9 is ≥ 9 and never an exact degree, and
    `B` is a family that the engines did not check.
  - A `u` centre must have degree exactly D. D ≥ 9 is admitted, but it acts only on rows of exact degree D (2.1: no
    U = 9 action).
- **G4 (frame = induced).** The kc edges among the m interior vertices **equal** the pattern edges of 1.5.
  - Every adjacency the frame forces is present (g7_check (c)).
  - There is no kc edge that the frame does not force. In particular, there is no edge between two named ring-3
    vertices, and no edge between named vertices that the frame keeps at distance ≥ 2.
  - The containment matcher is induced, so a missing or extra edge would make the name fire where the configuration
    does not embed.
- **G5 (faces).** Every 3-cycle among the kc line's interior vertices maps onto a frame face of 1.5 (1.9 point 5).
  This covers grow.embeddings' face condition, and it also holds a separating interior triangle.
- **G6 (placement).** A `-` name's arc A satisfies |A| ≤ D − 1, or the name is marked "D only". Otherwise 1.4 lets it be
  placed at d' ≠ D, where its induced pattern differs.

An admitted k3p line **may** carry an optional token `class=<c>[,<c>..]` naming the Part 2 absorption the loader will
use. It goes after the kc fields and before the parenthesised comment. The values are:

| value | meaning |
|---|---|
| `amask` | case A |
| `l3q` | case L |
| `fpat` | case F |
| `sepx` | case A′, separator state |
| `M2` | case X with two or more privates |
| `r3h` | case X with ring 3 |
| `cluster` | the cluster-row route |

The token is a **hint only**. The guard never reads it, a missing or wrong token never changes admissibility, and the
Opus loader recomputes the class itself (`pc_class_hint` in `eng/privcell.py`) and logs any disagreement (1.9
point 7).

### 3.2 Worked examples

**(a) g7_-..655.._..65..._...5...... (D, ring 8, m = 6).**
- q-form: `q7-_....556_....56._::::::5`. The vertex list is w4 = 5, w5 = 5, w6 = 6, s4 = 5, s5 = 6, p6L1 = 5, with 9
  edges: w4–w5, w5–w6, s4–w4, s4–w5, s5–w5, s5–w6, s4–s5 (w5 = 5, so s4 and s5 are ring-2 neighbours), p6L1–w6 and
  p6L1–s5.
- G1: D by kc and dfast18 (Studio dc1ff9f9). G2 does not apply, since the name is D.
- G3: the 6 named slots are exact, matching m = 6.
- G4: the 9 edges are exactly the kc line's interior edges (`framecheck.log`). The frame faces among them are (w4, w5,
  s4), which is the 5-5-5 face, plus (w5, s4, s5), (w5, w6, s5) and (w6, s5, p6L1).
- G6: A = {4, 5, 6}, |A| = 3, so the name is placeable at every d' ≥ 5.
- **Admitted, class A** at U = 7, 8, 9 (14 images). Also a cons2 skip at w6.

**(b) g7_-.6655.._..65..._..55...... (C, X = {I0-I1}, ring 11, m = 8).**
- q-form: `q7-_...5566_...56.._:::::5:5`. Its constraints are w3 = w4 = 5, w5 = w6 = 6, s3 = 5, s4 = 6, p5L1 = 5 and
  p6L1 = 5.
- G1: C by kc X and cfast --fixed X with leftover 0. G2: X = {I0-I1} joins two interior vertices, so the ring-merge
  check passes.
- G3: 8 exact slots, matching m = 8. G4: the forced edges, including s3–s4 (w4 = 5) and p5L1–s4. p6L1 has no named ring-2
  neighbour, because s5 and s6 are free. There are 11 edges, equal to the kc line's.
- **Admitted, class X** (two privates, p5 and p6). The loader does not absorb it in M. It acts through cluster rows,
  where it is the {p61:5, p51:5} cell kill of 2.5, and is a cons2 skip at w5. For an LP-wide effect it needs the M2
  family (2.6).

**(c) g7_u76.5566_6..5..._..5....... (C, X = {I0-I2}, ring 14).**
- q-form: `q7u_.556676_.5...6._::::::5`. The centre is in X with degree exactly 7.
- G1 and G2 pass (Studio: X interior-only). G3: m = 10 exact slots, including u = 7.
- G6: a `u` name is placed only at d' = 7.
- **Admitted, class A′.** Its single private is p6L1 of the 6 at w6, but it needs w2, w3 and s1, which are outside
  w6's 9-slot window (w4..w1, s4..s0). It is held from the amask and logged. It is a candidate for a d = 7 M leaf correction in jsep5
  (2.1 A′).

**(d) A held example.**
- Take a name like (a) with s4 written `9` instead of `5` (or `B`).
- G3 fails: it is not an exact interior degree (letter-9 rule). It is **held**, even if a hand filter might want it.
- Likewise, a chain `s4/s5` with w5 = `.` fails G0: s4 and s5 are ring-2 neighbours only if w5 = 5 exactly, so the
  adjacency is undetermined. The name is **held** until w5 is pinned.

---

## Part 4. Prototype (`s36g/eng`) and checks

**Engine.** `s36g/eng` is a copy of `s28q/eng`. The solve outputs cert_/sol_/rows_ were not copied. md5s are in
`s36g/engine_md5.txt`. The changes:

- `privcell.py` (new):
  - the parser, canonicaliser and pattern builder;
  - the g7 → q converter;
  - `pc_build`, which absorbs a name as (A) amask bits, (L) l3q bits or (F) PATS, and logs every other name with its
    reason and any cons2-skip site;
  - standalone use: `python3 privcell.py canon|g7|pattern NAME..`.
- `prelay2.py`:
  - option `pcell=FILE` (one name per line);
  - `amask` ANDs out `PCAM` bits;
  - `l3q_load` ANDs out `PCL3` bits;
  - `PATS` gets the (F) patterns;
  - new command `pcellcheck`.
  - With no `pcell=` option, none of these paths runs.
- `pcheck.py`: the `pcellcheck` command is registered.

**Commands.** `bash s36g/run_checks.sh`, `bash s36g/selftest.sh` and `python3 s36g/framecheck.py HELDFILE` (the held
file from `git show origin/main:.../held53_7_7665566_6765766.txt`).

| check | result |
|---|---|
| amask over all 3 × 5^8 = 1,171,875 entries, with `pcell=g7_q.txt`, vs the s25c `g7` flag formula | **0 differences** (3,499 entries differ from the plain kill table: exactly g7 #1's bits) — `pcellcheck.log` |
| amask with no names vs the plain kill table | 0 differences |
| lowerR2 cert_st24bL, `pcell=g7_q.txt` (F0 flags, argsA59) | **INVALID**, rc ('M',(9,5,6,5,6,5,5,29)) −1/26, ('M',(9,5,6,6,5,5,5,29)) −1/26, ('M',(7,5,6,7,6,5,7,31)) −3/13: **identical** to `s25c/lower_oldcert_g7.log` |
| lowerR2 cert_st24bL, no option / empty name file | VALID 2/13 / VALID 2/13 (unchanged) |
| lowerR2 cert_s28A60L with `l3q` (argsA60, tab60), no option / empty file | VALID 47/320 / VALID 47/320, the same as `s28q/lower_s28A60L.log` |
| the same, `pcell=g7_q.txt` | l3q keys hit 0 (L3T unchanged). INVALID through M only: ('M',(8,5,6,5,8,5,5,29)) −1/80, ('M',(8,5,6,5,7,5,5,29)) −7/160, ('M',(8,5,6,6,6,5,5,31)) −7/160. The g7 #1 kill also breaks the s28q cert |
| framecheck (G3/G4) on the 10 names vs Studio's kc lines | 10/10 same vertex set and degrees; interior kc edges = pattern edges (`framecheck.log`). G5 (faces) not checked |
| selftest, synthetic names (**not kills**) | The l3q path changes 200 of 5,000 masks; the f-pattern path adds 14 d = 7 patterns and makes the binder 7665566/6675676 not admissible (`selftest.log`) |

**Absorption of the 10 names (logged on every run):**

- #1 absorbed: A7/A8/A9, 14 images each.
- #2 not absorbed: A′, outside the window.
- #3, #4, #5, #6, #10 not absorbed: ring 3.
- #7, #8, #9 not absorbed: two privates.
- cons2-skip sites, reported only: #1 w6, #3 w6, #4 w6, #7 w5, #8 w6, #9 w5.

**Not done:** no solve, and no upperR2. The window table goes through the same `amask` function that `pcellcheck`
verifies over its whole domain. The union rule, the cons2 skip, A′ leaf corrections and M2 are spec only.
