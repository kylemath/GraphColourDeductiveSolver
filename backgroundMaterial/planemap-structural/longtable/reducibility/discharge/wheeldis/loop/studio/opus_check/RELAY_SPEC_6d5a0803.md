# RELAY_SPEC: the "s10-mode" relay LP class (R6x + L2), as used for s10, s13r and s14r

Agent S, Opus team, 18 Oct 2026. Written from the engine snapshot in `s14/` (`pcheck.py`, `psolve.py`,
`pslite.py`, `prelay.py`), the command `s14/cmd_s14r.sh`, FINDINGS.md stages 8, 9-10 and 11, and the JSON files.
Every statement here was checked against the code. Where FINDINGS and the code differ, this spec follows the code
and says so (see section 11).

The class is `pcheck.py solveR xon xcap=3` **without** the `gexact` flag. `prelay.py` is the same file (md5
`d3d4ceed906fc9477a1dadd4f106866a`) in `s14/`, in `s13/` and at the top of `P_own_lp/`. The three runs differ only
in the reducible registry (the args file):

| run  | args                                   | t*                  | dual rows |
|------|----------------------------------------|---------------------|-----------|
| s10  | `s9/argsA44.txt` + `rpat=rpatD.txt`    | 217/1129 = 0.192205 | 43        |
| s13r | `s13/argsA46.txt` + `rpat=../rpatD.txt`| 217/1129            | 43        |
| s14r | `s14/argsA47.txt` + `rpat=../rpatD.txt`| **19/102 = 0.186275** | 25      |

The s14r command, verbatim (from `s14/cmd_s14r.sh`, in `s14/`):

```
python3 pcheck.py solveR args=argsA47.txt rpat=../rpatD.txt root=<ROOT> xon xcap=3 xpen=1e-3 threads=3
        work=<tmp> warm=../s13/rows_s13r.txt,rows_s14.txt tag=s14r
```

Here `<ROOT>` is a mirror of the `wheeldis` directory (path `.../scratchpad/P/m/backgroundMaterial/.../wheeldis`).
`xpen=1e-3` puts a cost of 1e-3 per unit of x until a pass adds no rows. The cost is then set to 0 and the loop runs
again (s14r.log lines 58-60). The final LP and its duals therefore have objective `min t` only. `warm=` only seeds
receiver rows and has no effect on the model.

Notation. Letters are `LET = (5, 6, 7, 8, 9)`. Letter 9 means degree >= 9. A letter >= 7 is called **big**, and
5 and 6 are **small**. The letter index is `LI[l] = l - 5`. The **class** of a letter is `c(l) = 1 if l >= 7 else 0`,
and `CLS2 = {0: (5, 6), 1: (7, 8, 9)}`. All indices of cyclic words are taken mod the word length.

---------------------------------------------------------------------------------------------------------------

## 1. Charge model and what t means

Let G be a minimal counterexample: an internally 6-connected triangulation of minimum degree 5 that contains no
configuration of the reducible set R. Each vertex v gets initial charge `6 - deg(v)`, and the total charge is 12
(Euler). A degree-5 vertex (a **five**) starts with +1, a 6 starts with 0, and a vertex of degree d >= 7 starts with
`6 - d`.

Charge moves along edges only, by these rules:

- **y**: a five v sends `y[r]` to each big neighbour u. The key r is v's link word rooted at u (section 2.1).
- **g**: a five v sends `g[kg]` to each degree-6 neighbour x (section 2.3).
- **h**: a 6 x sends `h[kh]` to each big neighbour u (section 2.4). By the conservation rows (section 6), each 6
  passes on exactly what it receives, so it ends at charge 0.
- **x (L2)**: a big u sends `x[tau]` to each big neighbour u' (section 2.2), with `0 <= x <= xcap = 3`.

The LP is

```
minimise t   subject to
  every five ends with charge <= t           (senderR rows:  sum of what it sends >= 1 - t)
  every big u of degree d ends with <= t     (receiverR rows: load(u) <= d - 6 + t)
  every 6 ends with exactly 0                (cons rows, equalities)
  M[sig] >= h[k] for the unseen private      (mrowR rows)
  y, g, h, M >= 0;  0 <= x <= 3;  t free.
```

**Meaning of t.** In any feasible solution every vertex ends with charge at most `max(t, 0)`. If `t* <= 0`, the
total would be at most 0 < 12, a contradiction, so R would be unavoidable. If `t* > 0` this rule class cannot prove
that. A dual certificate proves `t >= t_low` for every rule in the class. s14r gives `t* = 19/102`, attained on
both sides: primal `sol_s14r.json` (upper bound) and dual `cert_s14r.json` (lower bound).

**What "reducible" means here.** The LP only counts local pictures that can occur in G:

- **R5**: forbidden 5-wheels (five-centred link words).
- **R6**: forbidden 6-wheels (6-centred link words).
- **RBIG**: forbidden links of a 7 or an 8.
- **Patterns**: forbidden partial arrangements around a big receiver.

Section 4.4 says exactly how each is used.

---------------------------------------------------------------------------------------------------------------

## 2. Variable families and their keys

The columns of the LP are `t`, `y[r]`, `x[tau]`, `g[kg]`, `h[kh]` and `M[sig]`. `sol_s14r.json` has these fields:

```
{"t": float, "model": "R6x", "xon": true, "gexact": false,
 "y": {"U|abcd": value, ...},          # only values > 0 are stored
 "g": [[[n1,c2,c3,c4,n5], value], ...],
 "h": [[[U,a,b,c,d,e], value], ...],
 "x": {"<int tau>": value, ...}}
```

A key that is absent has value 0. **M is not stored.** A checker must set
`M[sig] = max over k in cand(sig) of h[k]` (section 5), which is the smallest value the M rows allow. s14r stores
776 y, 45 g, 889 h and 8 x values.

### 2.1 y (five -> big)

A five v with link word `w = (l0..l4)` (its neighbours in cyclic order) sends `y[root(w, j)]` to each big spoke
`l_j`. The rooted key is

```
root(w, j): a = (w[j], w[j+1], w[j+2], w[j+3], w[j+4]);  b = (a[0], a[4], a[3], a[2], a[1]);  key = min(a, b)
```

(lexicographic min of tuples). The root letter is the receiver's letter U, and min over the two reading directions
is the canonicalisation under reflection. The JSON key is `"%d|%s" % (r[0], "".join(r[1:]))`, for example `"7|5566"`
for r = (7, 5, 5, 6, 6). The column set is `ROOTS`: all `root(w, j)` with w a sender word and `w_j >= 7`. There are
942 of them. y has no upper bound in solveR (lower bound 0).

### 2.2 x (L2, big -> big, with xcap)

`x[tau]` is the amount a big `fl` sends to an adjacent big `tl`. The edge (fl, tl) has two common neighbours
(triangles). For each side the key reads a triple `(c, a, b)`:

- c is the common neighbour;
- a is the other common neighbour of c and **fl** (not tl);
- b is the other common neighbour of c and **tl** (not fl).

```
side(c, a, b) = LI[c]*25 + LI[a]*5 + LI[b]                                  (0..124)
tau(fl, tl, s1, s2) = (((LI[fl]-2)*3 + (LI[tl]-2))*125 + min(s1,s2))*125 + max(s1,s2)
```

The two sides are unordered (min/max), and that is the reflection canonicalisation. fl and tl are letters 7, 8 or 9,
and a receiver uses `U = min(d, 9)`. The JSON key is `str(tau)`. Bounds are `0 <= x <= 3` (`xcap=3`).

Decoding: `hi = tau % 125`, `lo = (tau // 125) % 125`, `(fi, ti) = divmod(tau // 15625, 3)`, `fl = 7 + fi`,
`tl = 7 + ti`. Then each side code splits into `(c, a, b)` = `(5 + s//25, 5 + (s//5)%5, 5 + s%5)`. For example,
`x["16381"]`: 7 -> 8, sides (5,6,6), (5,6,6).

In a receiver u with link arrangement (section 4), a big `w_i` gives these two terms:

```
in  : + x[ tau(w_i, U, side(w_{i-1}, s_{i-1}, w_{i-2}), side(w_{i+1}, s_i, w_{i+2})) ]
out : - x[ tau(U, w_i, side(w_{i-1}, w_{i-2}, s_{i-1}), side(w_{i+1}, w_{i+2}, s_i)) ]
```

The key reads the same vertices from both ends, so the transfer is antisymmetric and conserved. If the in and out
keys are equal, the terms cancel and the coefficient is 0. Zero coefficients are dropped.

### 2.3 g (five -> 6), "five -> 6"

Take a five v with link `l0..l4`. Its **hat** `h_k` is the common neighbour of `l_k` and `l_{k+1}` other than v.
For a 6-spoke `l_k`, the wheel of `l_k` is the cyclic word `(v, l_{k+1}, h_k, f_k, h_{k-1}, l_{k-1})`. Here `f_k`
(the **fan**) is the vertex opposite v. v sends to `l_k`:

```
g[kg],  kg = min(a, reversed(a)),  a = (l_{k+1}, c(h_k), c(f_k), c(h_{k-1}), l_{k-1})
```

- Positions 1 and 5 hold exact letters (the two spokes next to the 6).
- Positions 2, 3, 4 hold **classes** 0/1 (hat, fan, hat): 0 = small (5 or 6), 1 = big (7, 8, 9).
- The reflection reverses the tuple, and the key is the lexicographic min. Python compares the mixed ints directly,
  so in practice `n1 <= n5`, with ties broken on the classes.

Seen from the 6 x with link `L = (L0..L5)` and a five at `L_i`, the same key is
`kg_of(L_{i+1}, L_{i+2}, L_{i+3}, L_{i+4}, L_{i+5})`, with classes applied to positions 2..4. The JSON value
`[5, 0, 1, 0, 6]` means: spokes 5 and 6 next to the 6, both hats small, fan big. s14r has 102 g columns.

### 2.4 h (6 -> big)

A 6 x with exact link `L = (L0..L5)` sends to each big `L_j`:

```
h[kh],  kh = kh_of(L, j) = min(a, b),  a = (L_j, L_{j+1}, ..., L_{j+5}),  b = (a[0], a[5], a[4], a[3], a[2], a[1])
```

This is the link rooted at the receiver, min over the two reading directions. The JSON value is the 6-list. s14r has
4,760 h columns, coming from the conservation and M rows.

### 2.5 M (inflow signatures)

A receiver u cannot see the **private** `p_j` of a link 6 `w_j`. That is the sixth vertex of `w_j`'s link, the one
not adjacent to u. u reads only

```
sig = sig_of(U, w_{j+1}, s_j, s_{j-1}, w_{j-1}) = min((U, wr, sr, sl, wl), (U, wl, sl, sr, wr))
```

where `wr = w_{j+1}`, `sr = s_j`, `sl = s_{j-1}`, `wl = w_{j-1}`. The 6's wheel is `(U, wr, sr, p, sl, wl)`.
`M[sig] >= 0` is a column, bounded below by the M rows (section 5). s14r has 975 signatures.

---------------------------------------------------------------------------------------------------------------

## 3. senderR rows (one five)

**Sender words.** `SENDERS` is the set of canonical 5-words w with these properties:

- canonical means `canon(w)` = the min over the 5 rotations of w and of reversed(w);
- w is not R5 (section 4.4);
- `max(w) >= 7`.

There are 342. The word in the label is this canonical form, as a digit string; positions 0..4 index it.

**Hidden letters.** Let `sixes = [k : w_k = 6]` in increasing order, and `hats = sorted({k, k-1 mod 5 : k in sixes})`.
A hat index m stands for the hat `h_m` between `l_m` and `l_{m+1}`. Two adjacent 6-spokes share a hat, and the hat
is one variable. An **assignment** is a pair `(H, F)`: `H[m] in {0,1}` for each m in hats, and `F[k] in {0,1}` for
each k in sixes. These are the flag bits.

**Admissible assignment.** For every k in sixes there must be letters `a in CLS2[H[k]]`, `q in CLS2[F[k]]` and
`b in CLS2[H[k-1]]` such that the 6-wheel `(5, w_{k+1}, a, q, b, w_{k-1})` is **not** R6. Each six is checked on its
own, and the sixes are coupled only through shared hat bits.

**Row.**

```
t + sum_{j : w_j >= 7} y[root(w, j)] + sum_{k in sixes} g[ min(a_k, rev(a_k)) ]  >=  1,
      a_k = (w_{k+1}, H[k], F[k], H[k-1], w_{k-1})
```

Repeated keys add up (for example `2*y[7|5576]` in 55767). "Moves out" of the five: the y terms are what it sends to
its big spokes (7, 8, 9) and the g terms are what it sends to its 6-spokes. With initial charge 1, the row says
`1 - out <= t`.

**Enumeration and dedupe in the code.** For each sender word, `itertools.product((0,1), repeat=len(hats))` is the
outer loop and `product((0,1), repeat=len(sixes))` the inner loop. Inadmissible assignments are skipped. An
assignment whose coefficient multiset is already present for that word is also skipped. s14r has 6,915 rows.

**Label.**

```
["senderR", WORD, [H[hats[0]], H[hats[1]], ..., "|", F[sixes[0]], F[sixes[1]], ...]]
```

The bits are JSON ints. The label is the **first** assignment (in that product order) that gives this coefficient
vector. A checker can simply rebuild the row from (WORD, bits) and check admissibility.

---------------------------------------------------------------------------------------------------------------

## 4. receiverR rows (big vertex u of degree d)

### 4.1 The arrangement

u has degree d >= 7 and letter `U = min(d, 9)`. Its link is `w_0..w_{d-1}` in cyclic order. The second ring is
`s_0..s_{d-1}`, where `s_i` is the common neighbour of `w_i` and `w_{i+1}` other than u. Letters run over 5..9.

The label strings are `LINK = w_0..w_{d-1}` and `SWORD = s_0..s_{d-1}`. What each link vertex sees:

- a five `w_i` has link `(U, w_{i+1}, s_i, s_{i-1}, w_{i-1})`, all visible;
- a 6 `w_j` has link `(U, w_{j+1}, s_j, p_j, s_{j-1}, w_{j-1})`, where the private `p_j` is unseen;
- a big `w_i` uses `w_{i±1}`, `w_{i±2}`, `s_{i-1}` and `s_i` for its x keys.

### 4.2 Row

```
-t + sum_{i : w_i = 5}  y[ root((U, w_{i+1}, s_i, s_{i-1}, w_{i-1}), 0) ]
   + sum_{j : w_j = 6}  M[ sig_of(U, w_{j+1}, s_j, s_{j-1}, w_{j-1}) ]
   + sum_{i : w_i >= 7} ( x[tau_in(i)] - x[tau_out(i)] )                (section 2.2)
   <=  d - 6
```

This is `(6 - d) + load <= t`. In the code an M term is added only when `cand(sig)` (section 5) is non-empty. That
is always true for an admissible arrangement.

Note what the receiver does **not** get: a 6 in the second ring is not adjacent to u and sends u nothing, and fives
send g only to 6s.

### 4.3 Label

```
["receiverR", d, LINK, SWORD]
```

Before a row is added, rows whose `(d, coefficient multiset)` repeats an earlier row are dropped. The stored label is
the first arrangement found, so a checker must rebuild the row from the label.

### 4.4 Admissibility (the arrangement must be possible in G)

An arrangement `(d, w, s)` is admissible iff all of these hold (`admissible()` in pcheck.py):

1. Every five `w_i` has `isR5((U, w_{i+1}, s_i, s_{i-1}, w_{i-1})) = False`.
2. **R6 condition.** Every 6 `w_j` has **some** `p in 5..9` with `isR6((U, w_{j+1}, s_j, p, s_{j-1}, w_{j-1})) = False`.
3. If d is 7 or 8, `canon(w)` (min over rotations and reflections, as a digit string) is not in RBIG.
4. No pattern instance of degree d matches (section 4.5).

The definitions of the reducible sets (pcheck.py, read from `<ROOT>`, with `DIS = dirname(<ROOT>)`):

- `R5`, `R6`: the canonical words in `DIS/studio17/wheels17_verdicts.txt` with verdict D, or verdict C where the word
  is not one of `565667 565676 565677 565757 565767 565777`. Family `c5` goes to R5, the others to R6.
- `FANS`: the lines of `<ROOT>/out/fans_dfast.out` with `D=true`.
- `isR5(w)` is true if `canon(w)` is in R5, or if some fan matches w in some rotation or reflection. In a fan
  pattern, `None` (`F`) is a wildcard.
- `isR6(w)` is true if `canon(w)` is in R6, **or** w has three cyclically consecutive 5s (the "2.122" rule).

The s14r sets, as loaded (letters, canonical):

```
R5 (24): 55555 55556 55557 55558 55566 55567 55568 55577 55578 55588 55656 55657 55658 55666 56566 56567
         56568 56577 56578 56588 56657 56658 56666 66666
R6 (31): 555555 555556 555557 555566 555567 555577 555656 555657 555666 555667 555676 555677 555757 555767
         555777 556556 556557 556566 556567 556576 556577 556657 556666 565656 565657 565666 566566 566567
         566577 566657 566666
FANS (7, position 0 first; F = any letter): F5565 F5656 F5555 F5665 FF555 F5556 FF565
```

RBIG (104 canonical 7- and 8-words) holds the `D=true` lines of these files:

- `<ROOT>/out/bigwheels_dfast.out`, all names;
- `bigwheels1516_dfast_partial.out` and `out/def_*.out`, names `c7_*` or `c8_*` only;
- `out/def_*.cfast`, blocks for 7-wheels (`c7_` or `*_w7_<n>_`) with a `C-REDUCIBLE` line.

The last two sources apply because the flag `now7plus` is not set. The 104 words:

```
5555555 55555555 55555556 55555557 5555556 55555566 55555567 5555557 55555656 55555657 5555566 55555666 55555667
5555567 55555676 55555757 5555577 55556556 55556557 5555656 55556566 55556567 5555657 55556576 55556657 5555666
55556666 5555667 5555676 5555677 5555757 5555767 5555777 55565556 55565557 5556556 55565566 55565567 5556557
55565576 55565656 55565657 5556566 55565666 5556567 55565756 5556576 5556577 55566557 55566566 55566567 5556657
55566576 55566657 5556666 55566666 55575557 55655656 55655657 5565566 55655666 5565567 5565577 55656557 5565656
55656566 5565657 55656656 55656657 5565666 55656666 5565667 5565676 5565756 55657566 5565757 5565766 55665566
5566557 55665657 5566566 55665666 5566567 5566576 5566657 5566666 55666666 56565656 56565657 5656566 56566566
56565666 5656567 56566666 5656657 5656666 56656657 5665666 56656666 56665666 5666567 5666577 5666657 5666666
```

### 4.5 Patterns

The patterns come from the args file: whitespace-separated tokens, paths relative to `<ROOT>` unless absolute.

- `pat=FILE` takes every line with `D=true` (every line if FILE ends in `:all`).
- `cpat=FILE` takes each block header (a line that contains ` r=` and does not start with a space) that is followed
  by a `C-REDUCIBLE` line.
- Only names matching `^[epf]\d+_` are used. The token `w7plus` in argsA47 is ignored.
- In s14r, 287 files were read. Two were missing (`out/job28/r_3.cfast`, `r_4.cfast`) and were skipped as in the run.

A name is `K<d>_<LINK>_<SWORD>[_...]` with K in {e, p, f}. Fields after the third are ignored. Slot `('w', i)` is
LINK[i] and slot `('s', i)` is SWORD[i]. Each character gives an allowed set:

| char | allowed letters |
|------|-----------------|
| `.`  | free            |
| `5`  | {5}             |
| `6`  | {6}             |
| `7`  | {7} (only in f-names) |
| `8`  | {8} (only in f-names) |
| `B`  | {7, 8, 9}       |

In p-names a `9` in LINK and a `0` in SWORD also mean free. They do **not** mean letter 9.

Raw `rpat=rpatD.txt` lines read `d k (i m)*k # comment`. Each entry `(i, m)` sets `w_i = 5` and gives the slots
`(w_{i+1}, s_i, s_{i-1}, w_{i-1})` the masks `m >> 5t` for t = 0..3. Bit b of each 5-bit group allows `LET[b]`.
Slots that several entries name are intersected.

A pattern P at degree d **matches** an arrangement if for some rotation r in 0..d-1, without or with reflection,
every slot holds an allowed letter. Without reflection, `('w',i) -> w_{i+r}` and `('s',i) -> s_{i+r}`. With
reflection, `('w',i) -> w_{r-i}` and `('s',i) -> s_{r-i-1}`.

Distinct patterns by d in s14r:

| d   | 7     | 8     | 9     | 10    | 11  | 12 | 13..17 |
|-----|-------|-------|-------|-------|-----|----|--------|
| count | 9,663 | 4,469 | 1,233 | 1,028 | 347 | 84 | 65 each |

By kind: D 15,497, C 1,494, RPAT 158. These counts are a check value for an independent loader.

---------------------------------------------------------------------------------------------------------------

## 5. mrowR rows (bounded inflow M)

For a signature `sig = (U, wr, sr, sl, wl)` (canonical, U in 7, 8, 9), the candidate h keys are

```
cand(sig) = { kh_of((U, wr, sr, p, sl, wl), 0) : p in 5..9, not isR6((U, wr, sr, p, sl, wl)) }
```

These are the h keys the link 6 might be paying u, over its unseen private p. Reading the signature the other way
gives the same set, because kh_of is reflection-canonical. For every sig with non-empty cand and every k in cand
there is one row:

```
h[k] - M[sig] <= 0          label: ["mrowR", list(sig), list(k)]
```

So `M[sig] >= max_{k in cand(sig)} h[k]`. This is the conservative max over the unseen private, the same max the
receiver's 6-term uses. The rows are built for every `U in (7,8,9)` and every `(wr, sr, sl, wl)` in `LET^4`. s14r
has 975 signatures and 4,760 M rows. `lowerR` accepts a label when k is in `cand(sig)` or in the candidate set of
the reversed signature, and requires `w <= 0`.

---------------------------------------------------------------------------------------------------------------

## 6. cons rows (one per non-R6 6-word that contains a five)

`relay_words()` is every canonical 6-word L with these properties:

- canonical means `canon6(L)` = the min over the 6 rotations of L and of reversed(L);
- L contains at least one 5;
- `isR6(L)` is False.

There are 994. For each one there is the equality

```
sum_{i : L_i = 5}  g[ kg_of(L_{i+1}, L_{i+2}, L_{i+3}, L_{i+4}, L_{i+5}) ]  -  sum_{j : L_j >= 7}  h[ kh_of(L, j) ]  =  0
label: ["cons", list(L)]
```

where `kg_of(n1..n5) = min(a, rev(a))` with `a = (n1, c(n2), c(n3), c(n4), n5)`. Equal keys add up. The row is
added only when it has a g term, which is always the case.

Meaning: a 6 x with link L receives exactly what it sends on, so it ends at 0. If L has no big letter, the g of its
fives is forced to 0. `lowerR` requires `canon6(L) == L` and `not isR6(L)`. The dual sign is free.

---------------------------------------------------------------------------------------------------------------

## 7. Primal (upper) check of sol_s14r.json

This is `upperR`, with `EPS = 1e-9`.

1. **Reconstruct M.** Set `M[sig] = max_{k in cand(sig)} h[k]` (missing h counts as 0). Also check that every stored
   value is >= 0 and every x is <= 3. upperR does not check either. Both hold in s14r: only values > 0 are stored,
   and max x = 0.0687.
2. **Senders.** For every sender word and every admissible assignment (section 3), the sum of y and g must be at
   least `1 - t - EPS`. Result: 0 violated.
3. **Conservation.** For each of the 994 relay words, `|sum g - sum h| <= 1e-9`. Result: 0 violated.
4. **Receivers, d = 7..17, exhaustive.** The row value is a sum of windows. For position i, the window value
   `W[w_{i-2}, w_{i-1}, w_i, w_{i+1}, w_{i+2}; s_{i-2}, s_{i-1}, s_i, s_{i+1}]` is:
   - for `w_i = 5`: `y[root((U, w_{i+1}, s_i, s_{i-1}, w_{i-1}), 0)]`, or -inf if that word is R5;
   - for `w_i = 6`: `max_{k in cand(sig)} h[k]`, or -inf if no p is non-R6;
   - for big `w_i`: `x_in - x_out`.

   The separator `bin/jsep3` (mode 0, source `P_own_lp/jsep3.cpp`) enumerates **every** admissible cyclic
   arrangement of length d. It applies the -inf windows, RBIG at d = 7 and 8, and all pattern instances at that d.
   It reports every arrangement whose sum exceeds `d - 6 + t + EPS` (capped at 20 reports). Result: 0 at every d.
5. **Tail d = 18..30 (relaxed DP).** For d >= 9 the letter is U = 9, so one window table `W9` serves every d.
   - The relaxed transfer matrix is 125 x 125 over states `(w_{i-1}, s_{i-1}, w_i)`. The edge
     `(b, q, c) -> (c, r, e)` has weight `max over (w_{i-2}, w_{i+2}, s_{i-2}, s_{i+1}) of W9`.
   - Patterns and RBIG are dropped, which only enlarges the set, so the bound stays sound.
   - `closed_max(M, d)` is the max weight of a closed walk of length d (the max-plus trace of M^d).
   - If it is at most `d - 6 + t + EPS`, d is covered. Otherwise the exact pattern-free DFS must find no violation
     at that d. In s14r every d in 18..30 passed the DP test.
6. **Karp tail, d >= 31.** Let λ be the maximum cycle mean of the relaxed matrix (Karp's algorithm). A closed walk of
   length d weighs at most `d λ`, so every d >= `d0 = (6 - t)/(1 - λ)` is covered. The check requires
   `d0 <= DTAIL + 1 = 31`. s14r: λ = 0.516339869 (= 79/153 to 9 digits) and d0 = 12.020, so the Karp bound alone
   covers d >= 13.

Result in `upper_s14r.log`: `UPPER-R: FEASIBLE at t = 0.186274509804`.

---------------------------------------------------------------------------------------------------------------

## 8. Dual certificate cert_s14r.json: labels and how to rebuild each row

The file is a JSON list of `{"w": float, "row": label}`. The weights are HiGHS row duals of the final LP, with their
signs, and only `|w| > 1e-11` is kept. No bound duals are written; x upper bounds are priced in the check.

| label | row (rebuild as in section) | bound b | allowed sign of w |
|---|---|---|---|
| `["senderR", WORD, BITS]` | section 3, with `+t` | `>= 1` | w >= 0 |
| `["receiverR", d, LINK, SWORD]` | section 4.2, with `-t`; label must be admissible (4.4) | `<= d - 6` | w <= 0 |
| `["cons", L]` | section 6; L canonical and non-R6 | `= 0` | any |
| `["mrowR", SIG, HKEY]` | `h[HKEY] - M[SIG]`; HKEY in cand(SIG) | `<= 0` | w <= 0 |

`mrowG` and `xcap` labels do not occur in this class (`mrowG` is `gexact` only, and `xcap` belongs to `solve2`).

**The check (`lowerR`, exact):**

1. Rationalise every weight with `Fraction(w).limit_denominator(10**7)`. For s14r every weight is p/306 exactly.
2. Rebuild each row. Form `tot[k] = sum_i w_i A_ik` over every column k other than t, and
   `tco = sum_sender w - sum_receiver w` (the t-column of `sum w_i A_i`). Require `tco > 0`.
3. Form `D = (sum_sender w * 1 + sum_receiver w * (d - 6)) / tco`. Cons and M rows have b = 0.
4. Compute the reduced cost `rc_k = -tot[k] / tco` for every column. For y, g, h and M (bounds `[0, inf)`) require
   `rc_k >= 0`. For an x with `rc_k < 0`, add `rc_k * 3` to D (it is priced at its cap).
5. Then `t >= D` for every feasible point. The reason: `sum w_i (A_i z - b_i) >= 0` term by term, by the signs.

Result in `lower_s14r.log`: `LOWER-R: VALID t >= 19/102 (25 rows)`.

---------------------------------------------------------------------------------------------------------------

## 9. Worked example on cert_s14r.json

### 9.1 The 25 rows rebuilt (weights in units of 1/306)

```
w*306  label                                           row
 +56  senderR 55667 [0,0,0,|,1,0]       t + y[7|5566] + g[50106] + g[60007]               >= 1
 +16  senderR 55667 [1,0,0,|,0,0]       t + y[7|5566] + g[51006] + g[60007]               >= 1
  +8  senderR 55696 [0,0,0,0,|,0,0]     t + y[9|6556] + 2 g[50009]                        >= 1
 +36  senderR 55767 [0,0,|,0]           t + 2 y[7|5576] + g[70007]                        >= 1
 +20  senderR 56669 [0,1,0,0,|,0,0,0]   t + y[9|5666] + g[50016] + g[60009] + g[60016]    >= 1
 +21  senderR 56696 [1,0,0,0,0,|,0,0,0] t + y[9|6566] + g[50009] + g[51006] + g[60009]    >= 1
 +52  senderR 66669 [0,0,0,0,0,|,0,1,1,0] t + y[9|6666] + 2 g[60009] + 2 g[60106]        >= 1
 -12  cons 556569    g[50009] + g[51006] + g[60016] - h[955656]                           = 0
 -56  cons 556596    g[50016] + g[50106] + g[60009] - h[956556]                           = 0
 -25  cons 556659    g[50009] + g[51006] + g[60009] - h[955665]                           = 0
 -32  cons 565659    2 g[60009] + g[60106] - h[956565]                                    = 0
 -72  cons 565667    g[60007] + g[60106] - h[756566]                                      = 0
  -4  cons 565696    2 g[60016] - h[965656]                                               = 0
 -36  cons 576667    g[70007] - 2 h[757666]                                               = 0
 -72  mrowR 75666 / 756566    h[756566] - M[75666] <= 0
 -72  mrowR 75766 / 757666    h[757666] - M[75766] <= 0
 -12  mrowR 95556 / 955656    h[955656] - M[95556] <= 0
 -25  mrowR 95565 / 955665    h[955665] - M[95565] <= 0
 -56  mrowR 95656 / 956556    h[956556] - M[95656] <= 0
 -32  mrowR 95665 / 956565    h[956565] - M[95665] <= 0
  -4  mrowR 96556 / 965656    h[965656] - M[96556] <= 0
  -4  receiverR 9 656656665 665555555   -t + 2 y[9|6556] + y[9|6666] + 3 M[95556] + M[95565] + M[95656] + M[96556] <= 3
  -5  receiverR 10 6556656556 6665656665 -t + 4 y[9|5666] + y[9|6566] + M[95565] + 4 M[95656]          <= 4
 -16  receiverR 9 656565665 665666566   -t + y[9|6566] + 3 y[9|6666] + M[95565] + 2 M[95656] + 2 M[95665] <= 3
 -72  receiverR 7 7665566 6675666       -t + y[7|5566] + y[7|5576] + M[75666] + M[75766] + 2 M[76667] <= 1
```

The g keys are written with their digits run together: `g[50106]` = `[5,0,1,0,6]`. All four receiver labels pass
`admissible()`. No x term survives: the only big link letter is `w_0 = 7` in the d = 7 row, and its in and out keys
are equal (section 9.3).

### 9.2 Hand expansion: senderR 55667 [0,0,0,|,1,0]

- `w = (5,5,6,6,7)`, `sixes = [2,3]`, `hats = sorted{2,1,3,2} = [1,2,3]`.
- The bits give `H1 = 0`, `H2 = 0`, `H3 = 0`, `F2 = 1`, `F3 = 0`.
- **y:** the big is `j = 4`. `root(w,4)`: a = (7,5,5,6,6), b = (7,6,6,5,5), min = (7,5,5,6,6) -> `y[7|5566]`.
- **Six k = 2:** `a = (w3, H2, F2, H1, w1) = (6,0,1,0,5)`; rev = (5,0,1,0,6) is smaller -> `g[50106]`.
  Admissible: the wheel (5, 6, a, q, b, 5) with a, b in {5,6} and q in {7,8,9} has a non-R6 choice, e.g.
  (5,6,6,7,6,5), whose canon 556676 is not in R6 and has no 555.
- **Six k = 3:** `a = (w4, H3, F3, H2, w2) = (7,0,0,0,6)`; rev = (6,0,0,0,7) -> `g[60007]`. Admissible, e.g.
  (5,7,6,6,6,6).
- Row: `t + y[7|5566] + g[50106] + g[60007] >= 1`.
- At the solution: 0.62255 + 0.10294 + 0.08824 = 0.81373 = 1 - t, so the row is tight.

### 9.3 Hand expansion: receiverR 7 7665566 6675666

`U = 7`, `w = (7,6,6,5,5,6,6)`, `s = (6,6,7,5,6,6,6)`.

| i | w_i | what u reads | term |
|---|-----|--------------|------|
| 0 | 7 | in `tau(7,7, side(w6=6,s6=6,w5=6), side(w1=6,s0=6,w2=6))`; out `tau(7,7, side(6,w5=6,s6=6), side(6,w2=6,s0=6))` | equal keys, coefficient 0 |
| 1 | 6 | (U,wr,sr,sl,wl) = (7, w2=6, s1=6, s0=6, w0=7); min with (7,7,6,6,6) | `M[76667]` |
| 2 | 6 | (7, w3=5, s2=7, s1=6, w1=6) vs (7,6,6,7,5) | `M[75766]` |
| 3 | 5 | five word (7, w4=5, s3=5, s2=7, w2=6); root = min((7,5,5,7,6),(7,6,7,5,5)) | `y[7|5576]` |
| 4 | 5 | (7, w5=6, s4=6, s3=5, w3=5) -> min with (7,5,5,6,6) | `y[7|5566]` |
| 5 | 6 | (7, w6=6, s5=6, s4=6, w4=5) vs (7,5,6,6,6) | `M[75666]` |
| 6 | 6 | (7, w0=7, s6=6, s5=6, w5=6) vs (7,6,6,6,7) | `M[76667]` |

- Row: `-t + y[7|5566] + y[7|5576] + M[75666] + M[75766] + 2 M[76667] <= 1`.
- At the solution: 0.62255 + 0.33824 + 0.15686 + 0.06863 + 0 = 1.18627 = 1 + t, so the row is tight.
- The M values come from cand: `cand(7,5,6,6,6) = {(7,5,6,p,6,6)}` gives max h = h[756566] = 0.15686;
  `cand(75766)` gives max h = h[757666] = 0.06863; every h in `cand(76667)` is 0.

### 9.4 Hand expansion: cons 576667 and mrowR 75766 / 757666

`L = (5,7,6,6,6,7)` (canonical; not R6).

- **The five at i = 0:** `kg_of(7,6,6,6,7) = (7,0,0,0,7)` -> `+g[70007]`.
- **Big j = 1:** `kh_of(L,1)`: a = (7,6,6,6,7,5), b = (7,5,7,6,6,6), min = (7,5,7,6,6,6).
- **Big j = 5:** a = (7,5,7,6,6,6) -> the same key.
- Row: `g[70007] - 2 h[757666] = 0`. At the solution: 0.13725 - 2 * 0.06863 = 0.

**The mrowR.** `cand(7,5,7,6,6) = {(7,5,7,p,6,6) : p = 5..9}`. All five are non-R6, and `kh_of` keeps them as written
because (7,5,...) < (7,6,...). The row is `h[757666] - M[75766] <= 0`.

**The chain.** Rows 55767 (+36), cons 576667 (-36), mrowR 75766 (-72) and the d = 7 receiver (-72) cancel on
`g[70007]`, `h[757666]`, `M[75766]` and `y[7|5576]` (see 9.5).

### 9.5 The weighted sum (ledger, units of 1/306)

```
t          : +56 +16 +8 +36 +20 +21 +52 (senders)  +4 +5 +16 +72 (receivers, -w * -1)   = +306
y[7|5566]  : +56 +16 -72 = 0          y[7|5576]  : +72 -72 = 0
y[9|5666]  : +20 -20 = 0              y[9|6556]  : +8 -8 = 0
y[9|6566]  : +21 -5 -16 = 0           y[9|6666]  : +52 -4 -48 = 0
g[50009]   : +16 +21 -12 -25 = 0      g[51006]   : +16 +21 -12 -25 = 0
g[50106]   : +56 -56 = 0              g[60007]   : +56 +16 -72 = 0
g[60009]   : +20 +21 +104 -56 -25 -64 = 0
g[60016]   : +20 -12 -8 = 0           g[60106]   : +104 -32 -72 = 0
g[70007]   : +36 -36 = 0              g[50016]   : +20 -56 = -36
h[...]     : each of the 7 h keys +w(mrowR) - w(cons) = 0
M[75666], M[75766], M[95556], M[95565], M[95656], M[95665], M[96556] : 0
M[76667]   : 2 * (-72) = -144
```

- `tco = 306/306 = 1`.
- Reduced costs: `rc(g[50016]) = +36/306 >= 0`, `rc(M[76667]) = +144/306 >= 0`, every other column 0. No x appears.
- Dual objective:

```
D = sum_sender w * 1 + sum_receiver w * (d - 6)
  = (56+16+8+36+20+21+52)/306 + (-4*3 - 5*4 - 16*3 - 72*1)/306
  = 209/306 - 152/306 = 57/306 = 19/102.
```

So for every feasible point, `t - (36/306) g[50016] - (144/306) M[76667] >= 19/102`, and hence `t >= 19/102`. The
primal `sol_s14r.json` attains `t = 0.18627450980392155 = 19/102` (to double precision).

---------------------------------------------------------------------------------------------------------------

## 10. Sizes in s14r (check values for an independent builder)

| item | count |
|---|---|
| sender words | 342 |
| y roots | 942 |
| senderR rows | 6,915 |
| g columns | 102 |
| h columns | 4,760 |
| conservation rows | 994 (all non-R6 6-words with a five) |
| signatures | 975 |
| M rows | 4,760 |
| final LP | 57,851 rows, 15,414 columns |
| receiver rows logged in `rows_s14r.txt` | 24,791 |
| iterations | 52 |

Orientation self-test (`orientR`): 3,125 kg and sig cases plus 15,625 L x 6 kh cases, 0 mismatches (FINDINGS stage 8).

## 11. Where FINDINGS and the code differ (the code is followed)

- FINDINGS stage 8 says the sender rows enumerate hats and fans "as in S-lite B mode". S-lite only uses hats next to a
  big root. `prelay.py` uses the hats on both sides of **every** 6-spoke (`{k, k-1}` for each six), whatever the
  roots are, and one fan per six. Section 3 follows the code.
- FINDINGS does not state the bounds. In solveR, y, g, h and M are in `[0, inf)` and x in `[0, 3]`. The older `solve`
  (jcheck) had y in `[0, 1]`; that does not apply here.
- FINDINGS writes `kg = (n1, c(n2), c(n3), c(n4), n5)`. That is the code's key, and section 2.3 adds its
  lexicographic tie-breaking on mixed letter/class tuples.
- FINDINGS 8 says M[sig] covers "every p that keeps that 6-wheel non-R6". This matches `cand`. The receiver adds the
  M term only when cand is non-empty, which admissibility already forces.
- s10 was run before the `s13/` and `s14/` snapshots existed, presumably with the top-level `P_own_lp/pcheck.py`. Its md5 now differs from `s14/pcheck.py`. The diff is only
  the command dispatch table (two extra R2 commands), and `prelay.py` is identical, so the class is the same.

---------------------------------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------------------------------

## 12. The reduced 6-centred extension ("s12r mode": R6x2 + apexcls + L2)

Used for s12r (35/183 on argsA44), **s12r47** (21/113 on `s14/argsA47.txt`) and **s12r50** (**t\* = 23/134 =
0.171641791** on `s17/argsA50.txt`).

### 12.0 Which code

The class is `pcheck.py solveR2 xon xcap=3 apexcls` (+ `consbasis=cons2basis_cls.json`, `xpen=1e-3`), with the
flags `zh`, `q7` and `noapex` all **off**. The code is `prelay2.py` at the top level of `P_own_lp/`.

- The `s14/` and `s17/` snapshots of prelay2.py (md5 `4a57bc28...`) predate the `apexcls` flag. They are **not** the
  s12r engine.
- No `cmd_s12r50.sh` exists. The flags above are inferred from `sol_s12r50.json` (`"apex": true`,
  `"apexcls": true`, `"zh": false`, no `q` field), from the log line
  `R6x2 (apex True): 7074 sender rows ... 11533 initial cons rows`, and from the basis size: 994 rows with s = 555555
  plus the 10,539 new rows of the 10,750-row `cons2basis_cls.json` gives 11,533.
- The current top-level prelay2.py (23:26) has the later `zh` and `q7` options. With both off it gives the same rows.
  I checked this by rerunning `lowerR2 xon xcap=3 apexcls cert=cert_s12r50.json args=s17/argsA50.txt
  rpat=rpatD.txt` on a read-only copy of the top-level engine: **VALID t >= 23/134 (57 rows)**, identical to
  `lower_s12r50.log`.
- The `noapex` setting of the same command is s10 mode: FINDINGS stage 12, V1 reproduced 217/1129.

The registry for argsA50 is argsA47 with the k3x files swapped (d43ba26a). Patterns by d:

| d   | 7     | 8     | 9     | 10    | 11  | 12 | 13..17 |
|-----|-------|-------|-------|-------|-----|----|--------|
| count | 9,663 | 4,469 | 1,360 | 1,028 | 347 | 84 | 65 each |

By kind: D 15,550, C 1,568, RPAT 158. R5, R6, FANS and RBIG are as in section 4.4.

Everything in sections 1-11 carries over (charge model, y, x, receiver admissibility, patterns, tail argument, dual
sign rules) **except** the g, h and M keys, the conservation rows and the row labels, which change as follows.

### 12.1 Apex letters

For a 6 x with link `L = (L0..L5)`, the **apex** `s_i` is the common neighbour of `L_i` and `L_{i+1}` other than x.
The 6-centred arrangement `(L, s)` is x's 2-ball, like a d = 6 receiver arrangement. With `apexcls`, every apex letter
enters a key only through

```
ap(l) = 7 if l >= 7 else 5          (5 = "small" witness, 7 = "big" witness)
```

So an apex is a class, written with the letters 5 and 7. Hats and fans stay 0/1 classes as in s10.

### 12.2 Keys (JSON formats in sol_s12r50.json)

The sol file has fields `t`, `model="R6x2"`, `apex=true`, `apexcls=true`, `zh=false`, `xon`, `y`, `g`, `h`, `x` and
`z=[]`.

- **y** and **x**: as in sections 2.1 and 2.2.
- **M**: not stored, as before. Set `M[sig] = max_{k in cand2(sig)} h[k]`.

The sizes in s12r50 are 781 y, 191 g, 3,432 h and 4 x values. The new keys:

**g2 (five -> 6), 7-tuple.** For a five at `L_i` of a 6 with arrangement `(L, s)`:

```
g2 = min(a, b),
a = (L_{i+1}, c(L_{i+2}), c(L_{i+3}), c(L_{i+4}), L_{i+5}, ap(s_i),     ap(s_{i-1}))
b = (L_{i+5}, c(L_{i+4}), c(L_{i+3}), c(L_{i+2}), L_{i+1}, ap(s_{i-1}), ap(s_i))
```

That is s10's kg followed by the classes of the apexes of the five's two edges at x. The reflection reverses the five
letters and swaps the two apexes. JSON: `[n1, c, c, c, n5, ar, al]`, for example `[5,0,1,0,6,5,7]`.

Seen from the five v with 6-spoke `l_k`, `s_i = l_{k+2}` and `s_{i-1} = l_{k-2}`. These are v's own spokes, so the
sender reads them exactly and then applies ap.

**h2 (6 -> big), 8-tuple.** For a big `L_j`, with `m = (L_j, L_{j+1}, ..., L_{j+5})`:

```
h2 = min( m + (ap(s_j), ap(s_{j-1})),   (m0, m5, m4, m3, m2, m1) + (ap(s_{j-1}), ap(s_j)) )
```

Here `s_j` is the apex beyond the edge (m0, m1) and `s_{j-1}` the one beyond (m5, m0). JSON: the 8-list, for example
`[8,5,5,6,5,5,5,5]`.

**sig2 (inflow signature), 7-tuple.** In a receiver u (letter U), a link 6 `w_j` has link
`(U, w_{j+1}, s_j, p_j, s_{j-1}, w_{j-1})`. The apexes of x's edges to u's neighbours are `w_{j+2}` (beyond the edge
u-w_{j+1}) and `w_{j-2}` (beyond u-w_{j-1}). Both are visible to u.

```
sig2 = min( (U, w_{j+1}, s_j, s_{j-1}, w_{j-1}, ap(w_{j+2}), ap(w_{j-2})),
            (U, w_{j-1}, s_{j-1}, s_j, w_{j+1}, ap(w_{j-2}), ap(w_{j+2})) )
cand2(sig2) = { h2 of the arrangement ((U, wr, sr, p, sl, wl), apexes (wrr, wll)) : p in 5..9,
                not isR6((U, wr, sr, p, sl, wl)) }
```

In code, `cand2` is `sig2_keys(sig) = {h2_of((U,wr,sr,p,sl,wl), wrr, wll)}`.

Orientation self-test (`orientR2`, FINDINGS stage 12, V2): 0 mismatches. It covers g2/sig2 reflections, h2
reflections and 20,000 random physical rotations and reflections of `cons2_coef`.

### 12.3 senderR2 rows

The hidden letters, the bits, the admissibility test and the dedupe are exactly as in section 3. The label format is
the same: `["senderR2", WORD, [hat bits, "|", fan bits]]`. Only the g key changes. For each six k:

```
g2_of(w_{k+1}, L5(H[k]), L5(F[k]), L5(H[k-1]), w_{k-1}, w_{k+2}, w_{k-2})      with L5(c) = 7 if c else 5
```

The code passes letter witnesses 5/7 for the classes, and g2_of re-classes them, so the result is the same as using
the classes directly. The apexes are the exact sender letters `w_{k±2}` after ap.

```
t + sum_{j: w_j >= 7} y[root(w, j)] + sum_{k in sixes} g2[...]  >= 1
```

s12r50 has 7,074 rows; s10 mode had 6,915. More rows survive the dedupe because the g2 keys separate more of them.

**Correction (key count).** **381** g2 keys appear in the sender rows; an earlier version of this section said 393.
The log's "393 g keys in senders" counts every g column that exists when the line is printed, and by then the
initial cons2 rows (s = 555555 plus the basis) have already been added. Checked on the engine snapshot
`snap/s12r50_solve`:

| set | g2 keys |
|---|---|
| deduped admissible sender rows | 381 |
| including inadmissible assignments | 386 (adds 5000657, 5000675, 5000677, 6000657, 6000677) |
| all g2 keys of all cons2 rows | 393 = the 381 + 12 |

The 12 extra keys are exactly the keys with spokes `n1, n5` in {5,6} and both apexes small (ending 5,5): 5001655,
5010655, 5011655, 5100655, 5101655, 5110655, 5111655, 6001655, 6010655, 6011655, 6101655, 6111655.

- **Why no sender has them.** Such a five has all five spokes small. Every small 5-word is R5, so no sender row
  contains these keys and they are unpaid columns.
- **Why that is still sound.** These keys occur only in cons2 rows for arrangements (L, s) that contain such a five,
  and those arrangements cannot occur in G.
- **In the solution.** 10 of the 12 are positive in `sol_s12r50.json`, which gives Studio's 391 = 381 + 10. The two
  that are not positive are 6101655 and 6111655.
- **s10 mode.** This does not happen there: kg has no apexes, so every kg key a cons row uses is also a sender key.

### 12.4 cons2 rows (conservation per 6-type over apex words)

For every 6-type L and **every** apex word `s in {5..9}^6` there is the equality

```
sum_{i: L_i = 5} g2(L, s, i)  -  sum_{j: L_j >= 7} h2(L, s, j)  =  0          label ["cons2", L, s]
```

This holds with no admissibility filter on s. That only shrinks the class, so it is sound. Because of ap, only the
small/big pattern of s matters: 2^6 distinct rows per L at most.

**Which L.** The solver builds rows for the 994 canonical non-R6 6-words that contain a five:

1. one row per L with s = 555555;
2. the `consbasis` rows (a QR basis per 6-type that implies every (L, s) row; `cmd_consbasisR2`);
3. every iteration, for each L, the argmax and argmin over all 5^6 s of `sum g2 - sum h2`, added if
   `|.| > 1e-9`.

The class's conservation is all (L, s), not only the rows actually in the LP:

- The upper check (12.7) tests all **1,424** canonical non-R6 6-words, including words with no five (those force
  their h2 sum to 0), times all 5^6 apex words.
- `lowerR2` accepts a `cons2` label when L is non-R6 and every letter of L and s is in 5..9. It does **not** require
  L to be canonical or to contain a five. Any such row is valid for the class.

Rebuild a label with `cons2_coef(L, s)`, exactly as above. Indices are mod 6, and `s_{i-1}` for i = 0 is `s_5`.

### 12.5 receiverR2 rows

```
-t + sum_{i: w_i = 5}  y[root((U, w_{i+1}, s_i, s_{i-1}, w_{i-1}), 0)]
   + sum_{j: w_j = 6}  M[sig2(j)]
   + sum_{i: w_i >= 7} (x[tau_in(i)] - x[tau_out(i)])     <=  d - 6        label ["receiverR2", d, LINK, SWORD]
```

Admissibility is section 4.4, unchanged. The only change from s10 is that the M signature now carries
`ap(w_{j+2})` and `ap(w_{j-2})`.

### 12.6 mrowR2 rows

```
h2[k] - M[sig2] <= 0   for k in cand2(sig2)        label ["mrowR2", sig2 (7-list), k (8-list)]
```

The solver adds all `cand2` rows of a signature the first time a receiver row uses it. The initial 1,055
signatures come from the warm rows. In s10 mode every signature was enumerated up front.

`lowerR2` checks three things:

- sig2 is canonical (`sig == sig2_of(*sig)`);
- k is in `cand2(sig)` (only the stored orientation; s10's lowerR also accepted the reversed one);
- `w <= 0`.

### 12.7 Primal check (upperR2)

1. **Senders.** Every senderR2 row over all admissible assignments must be at least `1 - t - EPS`.
2. **Conservation.** All 1,424 canonical non-R6 6-words times 5^6 apex words, with `|sum g2 - sum h2| <= 1e-9`.
   s12r50 worst: 3.9e-15.
3. **Receivers, d = 7..17, exhaustive with jsep3.** The window at a 6 position, with M = max over cand2 of h2, now
   depends on `(w_{i-2}, w_{i-1}, w_{i+1}, w_{i+2}, s_{i-1}, s_i)`. That is still inside the 9-slot window, so the
   separator stays exact. The jsep3 class table `clsR2` reflects this.
4. **Tail d = 18..30 (relaxed DP), then Karp.** As in section 7, with one change: the relaxed matrix now also
   maximises over `w_{i±2}` at 6 positions, as it already did for x at big positions.

s12r50 (`upper_s12r50.log`): senders 0 violated; conservation 0; d = 7..17 exhaustive 0; DP 18..30 all within
the cap; Karp λ = 0.522388060 (= 35/67) and d0 = 12.203. **UPPER-R2: FEASIBLE at t = 0.171641791045.**

### 12.8 Certificate check (lowerR2)

Same as section 8:

| label | sign of w | bound b |
|---|---|---|
| senderR2 | w >= 0 | 1 |
| receiverR2 | w <= 0 | d - 6 |
| cons2 | any | 0 |
| mrowR2 | w <= 0 | 0 |

`tco = sum_sender w - sum_receiver w`, `D = (sum_sender w + sum_receiver w (d - 6)) / tco`, every reduced cost
`-tot[k] / tco >= 0` except x, which is priced at its cap 3 if negative. senderR2 rows are looked up by
`(WORD, bits)` among the deduped rows, as in section 3.

### 12.9 Worked rebuild of cert_s12r50.json (57 rows; weights in units of 1/268)

Every weight rationalises (`limit_denominator(10**7)`) to an integer over 268. The rows by type are 11 senderR2,
26 cons2, 15 mrowR2 and 5 receiverR2. Each rebuilt row is listed with its value at sol_s12r50.json. All senderR2 and
receiverR2 rows are tight: sender LHS = 1, receiver LHS = d - 6.

```
w*268 label                                row
 +18 senderR2 55667 [0,0,0|1,0]   t + y[7|5566] + g[5010657] + g[6000755]                   >= 1
 +24 senderR2 55667 [0,1,0|0,0]   t + y[7|5566] + g[5001657] + g[6100755]                   >= 1
 +22 senderR2 55667 [1,0,0|0,0]   t + y[7|5566] + g[5100657] + g[6000755]                   >= 1
  +8 senderR2 55696 [0,0,0,0|0,0] t + y[9|6556] + 2 g[5000955]                              >= 1
 +20 senderR2 55767 [0,0|0]       t + 2 y[7|5576] + g[7000755]                              >= 1
 +12 senderR2 55767 [0,1|0]       t + 2 y[7|5576] + g[7001755]                              >= 1
 +12 senderR2 56669 [0,0,0,0|1,1,0] t + y[9|5666] + g[5010675] + g[6000955] + g[6010657]    >= 1
 +12 senderR2 56669 [0,1,0,0|0,1,0] t + y[9|5666] + g[5001675] + g[6000955] + g[6011675]    >= 1
  +6 senderR2 56696 [0,0,0,0,0|1,0,0] t + y[9|6566] + g[5000955] + g[5010657] + g[6000955]  >= 1
 +12 senderR2 66667 [0,0,0,0,0|0,1,1,0] t + y[7|6666] + 2 g[6000755] + 2 g[6010657]         >= 1
 +32 senderR2 66669 [0,0,0,0,0|0,1,1,0] t + y[9|6666] + 2 g[6000955] + 2 g[6010657]         >= 1
 +11 cons2 556558 555555   2 g[5000855] + 2 g[5100655] - h[85565555]                         = 0
 -22 cons2 556659 555555   g[5000955] + g[5100655] + g[6000955] - h[95566555]                = 0
 -24 cons2 565659 555555   2 g[6000955] + g[6010655] - h[95656555]                           = 0
 +12 cons2 565678 555555   g[6001855] + g[6011655] - h[76565855] - h[85656755]               = 0
 -12 cons2 566659 555555   2 g[6000955] - h[95666555]                                        = 0
 -64 cons2 566667 555555   g[6000755] - h[75666655]                                          = 0
 +76 cons2 566766 555555   g[6010655] - h[76656655]                                          = 0
 -12 cons2 566776 555555   g[6011655] - h[76566755] - h[76656755]                            = 0
  -6 cons2 567567 555555   2 g[6100755] - 2 h[75675655]                                      = 0
 -12 cons2 576677 555555   g[7001755] - h[75766755] - h[75776655] - h[76675755]              = 0
 -11 cons2 556558 577555   2 g[5000855] + 2 g[5100657] - h[85565555]                         = 0
 -24 cons2 556596 577557   g[5001657] + g[5010657] + g[6000975] - h[95655655]                = 0
 -12 cons2 556676 755755   g[5001675] + g[5010675] - h[76556657]                             = 0
 -12 cons2 565667 757555   g[6000775] + g[6010657] - h[75656655]                             = 0
 -52 cons2 565667 755575   g[6000775] + g[6010655] - h[75656657]                             = 0
 -12 cons2 565678 557555   g[6001855] + g[6011657] - h[76565855] - h[85656755]               = 0
 +12 cons2 566659 755755   2 g[6000975] - h[95666555]                                        = 0
 +64 cons2 566667 755555   g[6000775] - h[75666655]                                          = 0
 -12 cons2 566766 555757   g[6010657] - h[76656657]                                          = 0
 -76 cons2 566766 555557   g[6010657] - h[76656655]                                          = 0
 -12 cons2 566876 757575   g[6011675] - h[76566875] - h[86656775]                            = 0
 +12 cons2 566876 557577   g[6011657] - h[76566875] - h[86656775]                            = 0
  -6 cons2 567567 575575   2 g[6100755] - 2 h[75675657]                                      = 0
 -20 cons2 576667 575575   g[7000755] - 2 h[75766657]                                        = 0
 -12 cons2 576677 575775   g[7001755] - h[75766757] - h[75776657] - h[76675777]              = 0
 +12 cons2 576677 555775   g[7001755] - h[75766757] - h[75776655] - h[76675777]              = 0
 -24 mrowR2 9565655 / 95655655    h - M <= 0
 -24 mrowR2 9566555 / 95656555
 -22 mrowR2 9556555 / 95566555
 -12 mrowR2 7665755 / 76675755
 -52 mrowR2 7566657 / 75656657
 -12 mrowR2 7576755 / 75766755
 -12 mrowR2 7666755 / 76656755
 -12 mrowR2 7566655 / 75656655
 -12 mrowR2 7666657 / 76656657
 -12 mrowR2 7565657 / 75675657
 -12 mrowR2 7656755 / 76566755
 -40 mrowR2 7576657 / 75766657
 -12 mrowR2 7576657 / 75776657
 -12 mrowR2 7656657 / 76556657
 -12 mrowR2 7565655 / 75675655
  -8 receiverR2 10 6565656565 6655666666  -t + y[9|6556] + 4 y[9|6666] + 2 M[9556555] + 3 M[9566555]          <= 4
  -6 receiverR2 10 6556656556 6665656665  -t + 4 y[9|5666] + y[9|6566] + M[9556555] + 4 M[9565655]           <= 4
 -52 receiverR2 7 7665566 6675666  -t + y[7|5566] + y[7|5576] + M[7566657] + M[7576657] + 2 M[7666755]        <= 1
 -12 receiverR2 7 7665666 6566565  -t + y[7|6666] + M[7565655] + M[7565657] + M[7656657] + M[7656755]
                                       + M[7665755] + x[3281] - x[3781]                                       <= 1
 -12 receiverR2 7 7655666 6756666  -t + y[7|5566] + y[7|5576] + M[7566655] + M[7576755] + M[7666657]
                                       + M[7666755] - x[3281] + x[3781]                                       <= 1
```

Keys are written with their digits run together: `g[5010657]` is `[5,0,1,0,6,5,7]` and `h[75766657]` is
`[7,5,7,6,6,6,5,7]`.

**Hand expansion: senderR2 55767 [0,1|0].**

- `w = (5,5,7,6,7)`, `sixes = [3]`, `hats = [2,3]`, so `H2 = 0`, `H3 = 1`, `F3 = 0`.
- **y:** both 7s root to (7,5,5,7,6), giving `2 y[7|5576]`.
- **Six k = 3:** `a = (w4=7, c=1, c=0, c=0, w2=7, ap(w0=5)=5, ap(w1=5)=5) = (7,1,0,0,7,5,5)`.
  The reflection is `(7,0,0,1,7,5,5)`, which is smaller, giving `g[7001755]`.
- Admissible: the wheel `(5,7,a,q,b,7)` with a in {7,8,9} and q, b in {5,6} has a non-R6 choice, e.g. (5,7,7,6,6,7) with
  canon 576677, not in R6.
- The [0,0|0] row differs only in the hat bit and gives `g[7000755]`.

**Hand expansion: receiverR2 7 7665566 6675666.** `U = 7`, `w = (7,6,6,5,5,6,6)`, `s = (6,6,7,5,6,6,6)`.

| j | w_j | (U, w_{j+1}, s_j, s_{j-1}, w_{j-1}, ap w_{j+2}, ap w_{j-2}) | its reflection | term |
|---|-----|------------------------------------------------------------|----------------|------|
| 0 | 7 | x in and out keys equal | | 0 |
| 1 | 6 | (7,6,6,6,7, ap5=5, ap6=5) | (7,7,6,6,6,5,5) | `M[7666755]` |
| 2 | 6 | (7,5,7,6,6, ap5=5, ap7=7) | (7,6,6,7,5,7,5) | `M[7576657]` |
| 3 | 5 | five word (7,5,5,7,6) | | `y[7|5576]` |
| 4 | 5 | five word (7,6,6,5,5) | | `y[7|5566]` |
| 5 | 6 | (7,6,6,6,5, ap7=7, ap5=5) | (7,5,6,6,6,5,7) | `M[7566657]` |
| 6 | 6 | (7,7,6,6,6, ap6=5, ap5=5) | | `M[7666755]` (second) |

Row: `-t + y[7|5566] + y[7|5576] + M[7566657] + M[7576657] + 2 M[7666755] <= 1`.

**Hand expansion: mrowR2 7576657 / 75766657.**

- `cand2(7,5,7,6,6,5,7)` is the h2 of `((7,5,7,p,6,6), apexes 5, 7)`. The first orientation `(7,5,7,p,6,6,5,7)` is
  the smaller one, so `cand2 = {(7,5,7,p,6,6,5,7) : p = 5..9}`.
- p = 6 gives `h[75766657] - M[7576657] <= 0`.

**Hand expansion: cons2 576667 / 575575.**

- `L = (5,7,6,6,6,7)`, `s = (5,7,5,5,7,5)`.
- **The five at i = 0:** `(7,0,0,0,7, ap(s0)=5, ap(s5)=5)` gives `g[7000755]`.
- **Big j = 1:** `m = (7,6,6,6,7,5)` with `(ap s1, ap s0) = (7,5)`. The reflection `(7,5,7,6,6,6,5,7)` is smaller.
- **Big j = 5:** `m = (7,5,7,6,6,6)` with `(ap s5, ap s4) = (5,7)`, giving the same key.
- Row: `g[7000755] - 2 h[75766657] = 0`.

**The chain.** These four rows link up:

- senderR2 55767 [0,0|0] (+20) and cons2 576667/575575 (-20) cancel `g[7000755]`.
- That cons2 row (-20 x -2 = +40) and mrowR2 7576657/75766657 (-40) cancel `h[75766657]`.
- `M[7576657]` gets +40 and +12 from the two mrowR2 rows on that signature, and -52 from the d = 7 receiver.

**Ledger (sum of w * coefficient, units of 1/268).** Every y, g, h and x key nets to 0. In particular `x[3281]` and
`x[3781]` cancel between the two d = 7 receivers 7665666/6566565 and 7655666/6756666. Only two entries are left:

```
t           : senders 18+24+22+8+20+12+12+12+6+12+32 = 178 ; receivers 8+6+52+12+12 = 90 ; total 268 -> tco = 1
M[7666755]  : +12 (mrowR2) - 104 (2 x d=7 receiver 7665566) - 12 (receiver 7655666) = -104  -> rc = +104/268 >= 0
D = 178/268 + (-8*4 - 6*4 - 52*1 - 12*1 - 12*1)/268 = 178/268 - 132/268 = 46/268 = 23/134.
```

So for every feasible point, `t - (104/268) M[7666755] >= 23/134`, hence `t >= 23/134`. The primal attains
`t = 0.17164179104477612 = 23/134`.

### 12.10 Differences from s10 mode, in one place

| item | s10 mode (solveR) | s12r mode (solveR2 apexcls) |
|---|---|---|
| g key | 5-tuple `(n1,c,c,c,n5)` | 7-tuple, plus `(ap(s_i), ap(s_{i-1}))`; the sender reads `w_{k±2}` |
| h key | 6-tuple (rooted link) | 8-tuple, plus `(ap(s_j), ap(s_{j-1}))` |
| M signature | 5-tuple | 7-tuple, plus `(ap(w_{j+2}), ap(w_{j-2}))`; window at a 6 reads `w_{i±2}` |
| conservation | one equality per 6-type L (994) | one per (L, s) for all apex words s (effectively 2^6 class words); LP holds 994 s = 555555 rows + basis + separated rows; upper checks all 1,424 non-R6 L (also no-five L) x 5^6 |
| M rows | all 975 signatures up front | lazily, per signature used |
| lowerR mrow check | accepts either orientation | canonical signature only |
| labels | `senderR`, `receiverR`, `cons [L]`, `mrowR` | `senderR2`, `receiverR2`, `cons2 [L, s]` (L any non-R6, not necessarily canonical), `mrowR2` |
| tail relaxation | maximises over `w_{i±2}` only at big positions | also at 6 positions |
| sol JSON | `model "R6x"`, `gexact` | `model "R6x2"`, `apex`, `apexcls`, `zh`, `z` (empty) |

Unchanged: the charge model, y, x (L2, cap 3), sender bit format and admissibility, receiver admissibility,
patterns, RBIG, d = 7..17 exhaustive, DP to 30, Karp.

Because the class contains s10's (take g2 and h2 constant in the apex classes), t*(s12r) <= t*(s10). On argsA47
this gives 21/113 < 19/102.

### 12.11 Ambiguities (s12r mode)

- No command file exists for s12r47 or s12r50. The flags and the basis file are inferred (12.0).
- The engine that ran s12r50 is an earlier edit of the top-level prelay2.py, since the sol file lacks the `q` field
  the current code writes. Its exact text is not preserved. The current code with `zh` and `q7` off reproduces the
  certificate exactly, and I did not re-run upperR2.
- The 1,424-word upper conservation check is stricter than the LP's 994 relay words. A no-five 6-type's h2 keys are
  free in the LP (bounded only through M), but upper requires their sum to be 0 for every s. They are 0 in s12r50, so
  this holds, but a different primal of the same LP could fail upperR2 while being LP-feasible.

## 13. Stage 15: the 6 -> 7 pass-on ("s16 mode": s12r mode + v6)

Written by Opus (the builder) before the solve. Run tag `st15`, registry `s17/argsA50.txt`. This section only
adds to section 12. Everything there carries over unchanged, including apexcls for g2, h2 and sig2.

### 13.0 Which code

`pcheck.py solveR2 xon xcap=3 xpen=1e-3 apexcls v6 consbasis=cons2basis_v6.json`, with `zh`, `q7` and `noapex` off.
The code is the top-level `prelay2.py`. The engine snapshot and md5s are in `snap/st15/`, and the commands are in
`cmd_st15.sh`.

`cons2basis_v6.json` comes from `pcheck.py consbasisR2 apexcls v6 out=cons2basis_v6.json`. It has 15,649 (L, s)
rows: a QR-pivoted basis of each 6-type's block, now including the v columns.

### 13.1 New keys

**cv (3-class apex reading, used only by the new keys):** `cv(l) = l if l < 7 else 7`, so 5 / 6 / big. The g2, h2 and
sig2 keys keep `ap` (5 / big).

**v (6 -> 7 pass-on), 8-tuple.** In a 6-centred arrangement (L, s) (section 12.1), take each position j with
`L_j = 7` (a neighbour of degree exactly 7; letters 8 and 9 get no v). With `m = (L_j, L_{j+1}, ..., L_{j+5})`:

```
v = min( m + (cv(s_j), cv(s_{j-1})),   (m0, m5, m4, m3, m2, m1) + (cv(s_{j-1}), cv(s_j)) )
```

This has the same shape as h2, but with cv in place of ap. v >= 0 is charge the 6 sends **to** that 7. JSON in
`sol_st15.json`: field `v`, a list of `[8-list, value]`. The flag is `"v6": true`.

**V (pass-on inflow signature), 7-tuple, only in receivers of letter U = 7 (d = 7).** For a link 6 `w_j` of u:

```
sigV = min( (7, w_{j+1}, s_j, s_{j-1}, w_{j-1}, cv(w_{j+2}), cv(w_{j-2})),
            (7, w_{j-1}, s_{j-1}, s_j, w_{j+1}, cv(w_{j-2}), cv(w_{j+2})) )
candV(sigV) = { v of the arrangement ((7, wr, sr, p, sl, wl), apexes (wrr, wll)) : p in 5..9,
                not isR6((7, wr, sr, p, sl, wl)) }        (code: sigv_keys)
```

The 6's link read from u is `(U, w_{j+1}, s_j, p_j, s_{j-1}, w_{j-1})`. Its apexes beyond the edges u-w_{j+1} and
u-w_{j-1} are `w_{j+2}` and `w_{j-2}`. u sees everything except the private p_j.

**Example (the target).** In 7665566/6675666, x = w2 = 6 has link (from u) `(7, w3=5, s2=7, p, s1=6, w1=6)` with
apexes `w4 = 5` and `w0 = 7`. So `sigV = min((7,5,7,6,6,5,7), (7,6,6,7,5,7,5))`. The 6 at w2 sees both fives.

### 13.2 Changed rows

**cons2** (section 12.4) gains the v terms. For every non-R6 L and every s in {5..9}^6:

```
sum_{i: L_i = 5} g2(L,s,i) + sum_{j: L_j = 7} v(L,s,j) - sum_{j: L_j >= 7} h2(L,s,j) = 0      label ["cons2", L, s]
```

`cons2_coef(L, s)` (with v6) rebuilds it. A 6 still passes on exactly what it receives: its fives and its 7s are paid
from its h inflow. Because of cv, a block now has at most 3^6 distinct rows.

**receiverR2** (section 12.5): only for d = 7 (U = 7), add

```
- sum_{j: w_j = 6, candV(sigV(j)) nonempty} V[sigV(j)]
```

to the left side. The rest is unchanged.

**New: mrowV rows.**

```
V[sigV] - v[k] <= 0   for every k in candV(sigV)        label ["mrowV", sigV (7-list), k (8-list)]
```

They are added lazily the first time a receiver uses sigV. Since V enters the receiver with a minus sign, it is
bounded by the **minimum** of v over the unseen p_j. That is the conservative choice for inflow: u counts only what
it receives whatever p_j is.

**Rebuilding V (answer to Studio).** V is not needed in the solution: rebuild it as `V[sigV] = min_{k in candV(sigV)} v[k]`, with v
missing from the sol taken as 0. That is the largest value mrowV allows, and it is exactly what upperR2 and the
separator use. From st15 on, `sol_*.json` also stores `V` as `[sigV, LP value, min over candV of v]` for every
signature in the LP, so the rebuild can be compared. The LP value can be below the min (that only makes u's load
larger), and upperR2 uses the min.

**Which L (soundness fix, 01:40Z).** With v6, the conservation rows must cover **all 1,424** canonical non-R6
6-types, including those without a five. In s12 mode, a no-five 6's h2 only costs, so 994 relay words were enough.
With v6, a no-five 6 next to a 7 could otherwise send v with no h coming in, which is free charge. Run 2 of st15 did
exactly that, and upperR2 rejected it on 48 such 6-types. In v6 mode the solver, the per-L separation and
`consbasisR2` therefore all loop over `all6_words()`. The basis has 22,126 rows. Run tag `st15f`, commands in
`cmd_st15f.sh`.

### 13.3 Window / separator

The window entry at a 6 position (c = 6) for U = 7 gets `- min_{k in candV(sigV)} v[k]`. The window reads
`(w_{i-2}, w_{i-1}, w_{i+1}, w_{i+2}, s_{i-1}, s_i)`, which are already window slots, and the jsep3 class table
`clsR2` already keys the c = 6 class by those slots. d = 7..17 stays exhaustive.

The tail d >= 18 uses the U = 9 window, which has no V, so it is unchanged and sound.

### 13.4 Checks

**upperR2:**

1. Senders, as before.
2. Conservation over all 1,424 non-R6 L times 5^6 s, with the v terms (`cons2_delta` adds `+v` at the 7 positions).
3. d = 7..17 exhaustive with the new window term (min over candV).
4. Tail and Karp.

**lowerR2:** as in section 12.8, plus:

| label | sign of w | bound b | check |
|---|---|---|---|
| mrowV | w <= 0 | 0 | `sigV == sigv_of(*sigV)` and `k in candV(sigV)` |

The reduced costs of v and V come from the generic ledger: v appears in cons2 (+) and mrowV (-); V appears in
receivers (-) and mrowV (+).

### 13.5 Sizes before the solve (s16_struct.txt)

| item | value |
|---|---|
| v keys | 13,869 (9,165 over the 994 five-containing types only) |
| V signatures | 2,850 (13,869 mrowV rows if all used) |
| h2 keys | 18,683 (12,347 over 994 types) |
| g2 keys | 393 |
| 6-types in conservation | 1,424 (all non-R6) |
| conservation rows over all (L, s) | 219,610 distinct (151,056 over 994 types) |
| conservation rank | 20,147 (994-type version: 13,670; s12r mode: 8,771) |

### 13.6 Class inclusion and kill lines

The class contains s12r's (take v = 0), so t*(st15) <= 23/134.

Kill lines:

1. 7665566/6675666 stays tight at 23/134.
2. The solve runs past 3 x s12r50's wall time (3 x 713 s) without t* moving below 23/134; then I stop and report.

### 13.7 Ambiguities

- v goes only to neighbours of letter 7 (degree exactly 7). An 8 or 9 next to the 6 gets none. That is a restriction
  of the class, so it is sound.
- cv reads an apex of letter 8 or 9 as 7. Same remark.
