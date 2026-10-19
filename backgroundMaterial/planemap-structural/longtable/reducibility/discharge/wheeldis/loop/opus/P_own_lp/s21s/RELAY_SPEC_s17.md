## 17. Stage 21: sender 2-ball registry filter (flag `s2b`, requires `hat5`). Written before any run

Engine: `P_own_lp/s21s/` = a byte copy of `s22/hf/` (s22h engine, md5s in `s22/hf/md5.txt`) plus the flag `s2b sdrop=FILE`.
Drop list builder: `s21s/sdrop.py`. Baseline: s22h, 16/101 on `s22/argsA55.txt` (5fa0adb0), `killtab=s22/f/kill/kill6`,
flags `xon apexcls filt16 hat5`.

**Why.** Sender rows were registry-independent: a hat5 context (§15) was dropped only by the per-spoke R6 class test.
`sndchk/` showed 0.297 of the 0.677 sender dual weight in cert_s22hL sits on contexts in which every completion of the
sender's 2-ball contains a forbidden configuration. Such a five cannot occur in a minimal counterexample.

### 17.1 Contexts

A context is exactly a hat5 sender context of the engine (`R2_sender_rows`, §12.3 and §15):

- the canonical sender word w = w0..w4 (`SENDERS`: canonical 5-words, not R5, some letter >= 7);
- H[0..4], with H[k] the class of the hat s_k between w_k and w_{k+1} (0 = {5,6}, 1 = {7,8,>=9});
- F, one class per 6-spoke, listed in increasing spoke order (F[i] is the class of the private of the i-th 6-spoke);
- only contexts that pass the engine's existing per-spoke R6 class test.

### 17.2 Frame (the sender's 2-ball)

The frame is built exactly as `s16_filter.build` (§14′), with centre degree 5:
`rings.Layered(5)`, `add_ring(w)` (link letters, letter 9 built as degree 9), ring-2 vertices named by their link
neighbours, then a ring of 9s added only so that every ring-2 face exists. Names:

- `v` (the five), `w_k` (k = 0..4);
- `s_k` = the ring-2 vertex adjacent to both w_k and w_{k+1} (the hat; asserted in code);
- `p_{k,i}` (i = 1..deg(w_k) - 5) = the privates of w_k, in rotation order.

P = {v, w_k, s_k, p_{k,i}}. Adjacency and faces are those of the layered disc induced on P (a ring-3 vertex is not in
P). As in §14′ and census50, the 2-ball of v is assumed to be this disc: its vertices are distinct and it has no other
edges among P.

### 17.3 Completion domain

| vertex | status | letters |
|---|---|---|
| v | fixed | 5 |
| w_k with letter 5..8 | fixed | its letter |
| w_k with letter 9 (>= 9) | **unknown** | never matches |
| s_k | free | {5,6} if H[k] = 0; {7, 8, >=9} if H[k] = 1 |
| p_{k,1} of a 6-spoke w_k | free | {5,6} if its F class is 0; {7, 8, >=9} if 1 |
| p_{k,i} of a 7- or 8-spoke | free | {5, 6, 7, 8, >=9} |
| p_{k,i} of a >=9 spoke | **unknown** | never matches (their number and positions are not known) |
| every vertex outside P | unknown | never matches |

A completion assigns one letter from its range to every free vertex. Domain size = product of the range sizes over
the free vertices. `>=9` is coded 99: it never equals a configuration degree. **Strict rule, as §14′:** an embedding
with any image on an unknown vertex is not a match (unknown vertices are coded 99, so grow.embeddings cannot use them;
outside vertices are not in P at all).

### 17.4 Containment and drop rule

- **Forbidden set.** `s22/f/s16_filter.registry()` at 5fa0adb0: the 582 RSST configurations of §14′ plus every name
  in `s22/k3x_D_5fa0adb0.out` (md5 86005e82...) and `s22/k3x_C_5fa0adb0.cfast` (md5 0f6a0004...), read from their kc
  lines over `loop/k[0-9]*/*`, total 2,109 (as in the `s22/f/kill/kill6_U*.log` headers). The md5 of the sorted name list
  is logged.
- **Containment** = `k42/grow.embeddings(c, P, pa, pf, fd)` unchanged: injective, exact degrees, induced, interior
  triangles onto faces. `fd` holds v, the fixed link letters, and 99 for unknown vertices. Free vertices are left out of
  `fd`, so an embedding returns its required degree at each free vertex it uses. A completion a contains c iff for some
  embedding a[x] equals the required degree at every free x in the image. This is identical to running grow.embeddings
  with fd = the full completion, because completion letters are 5..8 or 99.
- **Drop rule.** A context is dropped **only if every completion in its domain contains a forbidden configuration**.
- **Exhaustiveness.** No sampling and no cap. Coverage is decided by an exact complete case split: branch on a free
  vertex, one branch per letter in its range, and keep the requirement sets still consistent. A branch is covered when
  some requirement set has all its vertices fixed to the required letters; a branch is live when no consistent
  requirement set is left. This is equivalent to enumerating every completion. Where the domain is at most 2,000,000,
  the builder also literally enumerates every completion, and the two answers must agree (any disagreement aborts).
- Every context's true domain size is logged.

### 17.5 Use in the LP

- `R2_sender_rows` skips a dropped (word, H|F) context before computing its coefficients and before the
  coefficient-level dedup. A coefficient row survives iff some non-dropped context produces it.
- solveR2, lowerR2 and upperR2 all build sender rows through `R2_sender_rows`. So **upperR2's sender check enumerates the
  same filtered sender set**, and lowerR2 rejects a cert row naming a dropped context ("NOT A SENDER ROW").
- Keys, receiver rows, cons2, mrowR2, the window and the tail are unchanged. With the flag off, the engine is s22h's.

### 17.6 Controls (all required)

- (a) An empty forbidden set drops 0 contexts.
- (b) A broken-containment control (every configuration degree shifted by +1) gives a different drop set.
- (c) For every dropped context: one witness completion per killer configuration, i.e. per configuration that kills at
  least one completion, in `s21s/witness.txt`. Each line has the context, the configuration, the full completion (letter
  per free vertex) and the embedding image.
- A literal-enumeration cross-check (17.4) runs on every context with domain <= 2,000,000.

### 17.7 Run and kill line

The s22h recipe on `s22/argsA55.txt` with the s22 kill tables, plus `s2b sdrop=s21s/sdrop.txt`: solveR2 keeppen, then
solveR2 nosep, then lowerR2 on the nosep cert, then upperR2 nomax on the keeppen solution. These are compared like for
like with s22h (16/101).

**Kill line:** the gain is below 0.005 (upper bound > 16/101 - 0.005 = 0.15342), or any control fails.
