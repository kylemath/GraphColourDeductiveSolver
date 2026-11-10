# HATBB_SPEC: HAT keys between two big vertices (W6b, round 7, 10 Nov 2026)

A new column kind for the upper LP: a big vertex pays a big **apex** across one of its link edges (distance 2, not adjacent).
It is the grammar's HAT path (W6 `grammar.py` / round3 `gext.py`; the engine's r = hat5 and rr families are HAT(5->B) and
HAT(B->5)) with both endpoints in {7, 8, 9}. No existing family moves charge between two bigs at distance 2: x and Q7/q are
between adjacent bigs, r/rr/z/zr have a five at one end. Nothing else changes: every existing column keeps its coefficients,
and no new row is needed.

## 1. The keys

- `HAT(u->b)[ctx]`: payer letter u, payee letter b, both in {7, 8, 9} (9 = 9+; letters in labels are capped at 9). A key with
  a letter set at an endpoint (e.g. `B` = {7,8,9}, `{89}`) is the sum of its single-letter keys.
- ctx: a letter set (nonempty subset of {5,...,9}; `S` = {5,6}, `B` = {7,8,9}) at listed positions; unlisted = wildcard.
  Base positions (grammar.HPOS): `X Y U-1 U+1 XA YA V-1 V+1`. Extended positions (gext): `U+2 U+3 U-2 U-3 UA+2 UA+3 UA-2 UA-3`.
- Geometry: u, x, b, y is a diamond: triangles u x y and b x y share the edge x y; u and b are its two apexes.
- One LP column per key, 0 <= x <= 3, objective cost 0.001 (as the EDGE keys). Direction: relieves the payer's row, loads
  the payee's row (the payer passes charge on to b).
- Multiplicity: every link edge of the payer gives two oriented slots, (x, y) = (w_i, w_{i+1}) and (w_{i+1}, w_i); each slot
  that matches counts once (a key with a mirror-symmetric ctx counts the edge twice).

## 2. Rows

| row | constraint | HATBB coefficient |
|---|---|---|
| receiver, any degree d >= 7 | ... + terms <= d - 6 + t | IN - OUT |
| sender (5), cons2 (6), mrows | | none (no slot has both endpoints big) |

OUT = slots where the row's centre is the payer, counted on a SURE match (the row's letter set at every listed position lies
inside the key's set, endpoints inside u and b). IN = slots where the centre is the payee, counted on a POSSIBLE match (every
set meets the key's set). Same rule as KEYSPEC / PAYER8SPEC.

## 3. Slot positions

Receiver row label: centre letter U = min(d, 9), link w_0..w_{d-1}, apexes s_0..s_{d-1} (s_i = third vertex of the triangle on
w_i w_{i+1} away from the centre), all exact, indices mod d. Link-vertex privates use the row's picture sets (r5lib.recv_pic,
as for EDGE keys): a link 6's private = pmask & ~f2b extra6 (d <= 9; else all); a link 7's two privates = MASK / MASK8 &
~extra7 when its neighbour and apex on that side are <= 6 (d = 7, 8), else all; 8+ privates = all.

### 3.1 OUT: the centre pays the apex b = s_i (payer letter U, payee letter s_i >= 7)

Orientation (x, y) = (w_i, w_{i+1}):

| position | vertex | letter set |
|---|---|---|
| X, Y | w_i, w_{i+1} | exact |
| U-1, U+1 | w_{i-1}, w_{i+2} | exact |
| XA, YA | s_{i-1}, s_{i+1} | exact |
| V-1 | b's neighbour next to x other than y | s_{i-1} if w_i = 5 (exact); else w_i's private next to s_i (picture set) |
| V+1 | b's neighbour next to y other than x | s_{i+1} if w_{i+1} = 5 (exact); else w_{i+1}'s private next to s_i |
| U+2, U+3, U-2, U-3 | w_{i+3}, w_{i+4}, w_{i-2}, w_{i-3} | exact |
| UA+2, UA+3, UA-2, UA-3 | s_{i+2}, s_{i+3}, s_{i-2}, s_{i-3} | exact |

Orientation (w_{i+1}, w_i): the mirror, w_{i+k} <-> w_{i+1-k} and s_{i+k} <-> s_{i-k} in every line.

### 3.2 IN: the apex s_i (letter >= 7) pays the centre (payee letter U)

Positions are named from the payer's side, as in 3.1; orientation (x, y) = (w_i, w_{i+1}):

| position | vertex | letter set in the payee's row |
|---|---|---|
| X, Y | w_i, w_{i+1} | exact |
| U-1 | payer's neighbour next to x other than y | s_{i-1} if w_i = 5; else w_i's private next to s_i (picture set) |
| U+1 | likewise at y | s_{i+1} if w_{i+1} = 5; else w_{i+1}'s private next to s_i |
| XA | x's neighbour after U-1, away from the payer | w_{i-1} if w_i = 5; s_{i-1} if w_i = 6; w_i's other private if w_i >= 7 |
| YA | likewise at y | w_{i+2} if w_{i+1} = 5; s_{i+1} if w_{i+1} = 6; w_{i+1}'s other private if >= 7 |
| V-1, V+1 | w_{i-1}, w_{i+2} (the payee's own link) | exact |
| U+-2, U+-3, UA+-2, UA+-3 | the payer's farther link | wildcard |

Mirror orientation as in 3.1. With X = Y = 5 every base position is exact on both sides (the whole diamond's kite is in
both 2-balls).

### 3.3 Windows (engines that bound d >= 8 rows by windows)

Base positions read w_{i-1..i+2}, s_{i-1..i+1} and the privates of w_i, w_{i+1} (a link 6's pmask at w_j reads w_{j-2..j+2},
s_{j-2..j+1}), so the window w_{i-2..i+3}, s_{i-2..i+2} carries both OUT and IN. Extended positions need w_{i-3..i+4},
s_{i-3..i+3} (OUT only; the whole label at d = 8). An engine may read any position outside its window as the wildcard:
for OUT that only under-credits, for IN it only over-charges; both are sound.

## 4. Soundness (direction)

As PAYER8SPEC section 4. OUT: every position read is an exact link / apex letter of the row's label or a picture set that
contains the real letter, and a sure match in the row is a match in every real vertex the row covers, so OUT(row) <= OUT(z).
IN: each picture set contains the real letter and the payer's farther positions are the wildcard, so every real match is a
possible match, IN(row) >= IN(z). Payee 9 = 9+: rows of every enumerated degree d >= 9 take the inflow; beyond the enumerated
degrees the stack's large-degree argument must absorb at most 2 slots per link edge times the key's x (as for EDGE keys with
payee 9). Payer 9: OUT may be dropped at unenumerated degrees (under-credit).

## 5. Worked example

Key HB03 = `HAT(B->7)[X=5 Y=6 U-1=S YA=S]` (any big pays an apex 7 across a 5-6 spoke pair; the payer's link before the 5
is small, the apex beyond the 6 is small). colsum on lpdual_k86GS16_01 +0.001922, on lpdual_k86GS20_01 +0.001101.

- **OUT, target row R8** `55556859/58576556` (d = 8, w = 0 in both duals): link w = 5 5 5 5 6 8 5 9, apex s = 5 8 5 7 6 5 5 6.
  The only apex 7 is s_3, over the edge w_3 w_4 = 5 6. Orientation (x, y) = (w_3, w_4): X = 5, Y = 6, U-1 = w_2 = 5 (in S),
  YA = s_4 = 6 (in S): sure match, OUT 1. Orientation (w_4, w_3): X = 6, no. No IN (the payee letter is 7, the centre is 8).
  Coefficient IN - OUT = -1. The same slot relieves R4, R5, R6 (`55556857/5857577x`: s_3 = 7, s_4 = 5).
- **OUT, dual row** `R8 55556776/58576658` (w = -0.002043): link 5 5 5 5 6 7 7 6, apex 5 8 5 7 6 6 5 8; apex 7 = s_3 over
  w_3 w_4 = 5 6: X = 5, Y = 6, U-1 = w_2 = 5, YA = s_4 = 6: OUT 1, coefficient -1, colsum term (-0.002043)(-1) = +0.002043.
- **IN, dual row** `R7 7657567/6755765` (w = -0.001): link w = 7 6 5 7 5 6 7, apex s = 6 7 5 5 7 6 5; the payee is the
  centre 7, the payers are the apex 7s s_1 (over w_1 w_2 = 6 5) and s_4 (over w_4 w_5 = 5 6).
  s_1, orientation (x, y) = (w_2, w_1) = (5, 6): U-1 = s_2 = 5 (w_2 is a 5), YA = s_0 = 6 (w_1 is a 6): match, IN 1.
  s_4, orientation (w_4, w_5) = (5, 6): U-1 = s_3 = 5, YA = s_5 = 6: match, IN 1. Coefficient +2, colsum term -0.002.
  (Both matches here are exact; a payee position that is a private would be a possible match on its picture set.)

## 6. Implementation reference

W6b's coefficient builder: `code/hatcoef16x.py` (r5lib.slots_of -> gext.slots, HAT slots with both endpoints big; G.coef_rows:
OUT on sure, IN on possible). Pricing: `code/hat16x.py` (exact branch and bound over the 16 positions, 7 symbols each).
