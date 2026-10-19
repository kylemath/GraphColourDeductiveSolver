# RELAY_SPEC §21: l3q, a 7 paying an adjacent 7, keyed out to link distance 3 (stage 28, Opus s28q)

Source: SolvingFrameworkPlan/docs/working/BORROWED-CHANNEL-7FACE.md (origin/main ≥ dc954db3). Pricing is in s28q/pricer28.log:
rc(q̂(7,7,6,6,5)) = −6/13 on cert_st24bL, and the mask-off control gives exactly 0.
This section is the **V = 7 subfamily (20 q columns)**, which is the one being solved. Everything in §1–§19 carries over
unchanged (§1 scale, charge 6 − d; a big's load is its inflow, at most d − 6 + t).

## 21.1 Transfer
- A vertex u of degree exactly 7 sends `q[κ] ≥ 0` to each link neighbour v = w_i of degree exactly 7, once **per side** σ ∈ {+1, −1}.
- **Key:** `κ = (c, a, a2) = (w_{i+σ}, w_{i+2σ}, w_{i+3σ})` in u's link. Every letter is exact, in 5..9 (9 means ≥ 9).
  - The family has c, a ∈ {5, 6} and a2 ∈ 5..9, so 2·2·5 = **20 columns** `lq[(c, a, a2)]`.
  - Keys with c ≥ 7 or a ≥ 7 are not columns (they are 0).
- The sides are separate transfers, and there is no reflection min.
  - The key is a directed path along u's link, moving away from v.
  - Reflecting the embedding swaps the two sides and swaps them identically at both ends (see §21.5).
- U = V = 7 is implicit; it is dropped from the stored key. For d = 7 the vertices w_{i+3} and w_{i−3} are distinct and adjacent.
- **Cap and penalty:** 0 ≤ q ≤ `lqcap` (default 3, like x). Under `keeppen`, q carries the x penalty `xpen` (1e−3), and the
  penalty is removed together with x's.

## 21.2 Payee credit
- The payee is the centre v of a receiverR2 row, of degree 7.
- For every link vertex u = w_j with letter 7, and each side σ:
  - c = w_{j+σ} (exact, in v's link);
  - a = s_j when σ = +1, or s_{j−1} when σ = −1, i.e. the apex across (w_j, w_{j+σ}) (exact);
  - **a2 = u's private adjacent to a** (unseen: v sees only a mask of the letters it can take, §21.4).
- v credits `+1 · Q[(c, a, m)]`, where m is the 5-bit mask (bit k = letter 5 + k). Signatures with c ≥ 7 or a ≥ 7 have no column.
- Q ≥ 0 is uncapped, and nothing gains from raising it.

## 21.3 Rows

| row | lq[(c, a, a2)] | lQ[(c, a, m)] |
|---|---|---|
| receiverR2 of a d = 7 row (payer centre u) | −1 for each link 7 w_i and side σ with key (c, a, a2) | — |
| receiverR2 of a d = 7 row (payee centre v) | — | +1 for each link 7 w_j and side σ with signature (c, a) and mask m |
| **mrowL** (new), ≤ 0, dual ≤ 0 | +1 | −1: `lq[(c, a, a2)] − lQ[(c, a, m)] ≤ 0` **for every a2 ∈ m** |
| senderR2, cons2, mrowR2, mrowV, mrowQ | 0 | 0 |

- The same d = 7 row is generally both payer and payee: the centre pays its link 7s and is paid by them. Both term sets are summed.
- Rows of d ≥ 8 are untouched: there U ≥ 8 and V ≥ 8, which are outside the subfamily.
- **The value of Q in the extended solution** is `Qeff(c, a, m) = max(LP value, max_{a2 ∈ m} q[(c, a, a2)])`, for every mask
  in the kill table and not only for the masks the LP has seen.
  - This satisfies every mrowL row, including rows not yet generated, and it does not change any row the LP already has.
  - Separation and upperR2 both use Qeff, so the solution the upper check certifies is fully specified.
- **lowerR2:** mrowL rows are checked for signature validity and for a2 ∈ m, with sign w ≤ 0.
  - An lq column with negative reduced cost is priced at its cap, like x and D.
  - An lQ column with negative reduced cost makes the certificate invalid.

## 21.4 Mask semantics (strict, as §14′)
- **Window, at the payee.** Known vertices:
  - v (degree 7);
  - u = w_j (7);
  - w_{j+σ}, w_{j+2σ}, w_{j+3σ}, w_{j+4σ} (= c, w2, w3, w4; for d = 7, w_{j+4σ} = w_{j−3σ});
  - a (the apex on the σ side);
  - o (u's other apex: s_{j−1} for σ = +, s_j for σ = −).
- **Free:** the single slot a2.
- **Unknown:** everything else in the 2-ball. That is w_{j−σ}, w_{j−2σ}, the other five apexes, u's other private and all other
  privates. Each unknown gets degree 99, under the **strict rule**: an embedding that touches an unknown vertex is no match.
  - Letter 9 is never an exact degree.
  - Unknown link vertices get structural letter 9. This does not affect matches, because no match may touch them or their privates.
- **Forbidden set:** the registry of the solve, via s16_filter `registry()`.
  - r52k (7360eb92) is ex60 with s29/k3x_{D,C}_7360eb92: 3,424 configurations.
  - Containment is k42 `grow.embeddings` (exact degrees, induced, interior triangles onto faces).
- A letter is **killed** when some embedding uses only known vertices plus a2 at that letter.
- The mask is the set of letters not killed. Since the payee credits Q at least the maximum over the mask, the credit is at least
  the true inflow (sound).
- **Table** (`s28q/l3qtab.py`, exhaustive): σ ∈ ±1, c, a ∈ {5, 6}, w2, w3, w4, o ∈ 5..9, so 2·2·2·625 = **5,000 masks**
  (`s28q/tab60_{+1,-1}.json`).
- **Check:** on 7665566/6675676 and 7665567/6765756 the table reproduces the row masks of `mask28.py`:
  - rsst180 kills a2 = 5 on both sides of w0 in the binder;
  - one side only of w0 (rsst180) and of w6 (rsst119) in the side-test row.

## 21.5 Both-ends visibility
- **Payer u.** It reads its own link, so κ is exact.
- **Payee v.**
  - c is in v's link.
  - a is the apex across (u, c), the third vertex of the face (u, c, ·) other than v, which v's row holds.
  - a2 is u's link vertex after a, moving away from c. In v's 2-ball this is the private of u adjacent to a.
  - So the payer key (c, a, a2) equals the payee signature (c, a) plus the true a2, side by side.
- **Physical test** (pricer28.py): random u (degree 7), v (degree 7..11), explicit rotations, random mirror and offset.
  - 0 key mismatches over 100,000.
  - The broken control, where the payee reads the apex across the wrong edge, gives 95,996 mismatches.

## 21.6 d = 7 separation (exact): window upper bound plus leaf correction (`bin/jsep5`)
- The payer term at w_i reads w_{i±1..±3}. The payee term reads w_{j±1..±4} plus s_{j−1} and s_j. Both leave the 9-slot window.
  At d = 7, though, the whole row is known at the leaf of jsep's enumeration.
- **Window term** (`l3q_win`, U = 7 only, so d = 7 only).
  - At a position with w_i = 7, the window adds `UB(e, r) + UB(b, q)`, where UB(c, a) = max over the table's masks for (c, a)
    of Qeff(c, a, m), and 0 off-family.
  - Here + side: c = w_{i+1} = e, a = s_i = r. − side: c = w_{i−1} = b, a = s_{i−1} = q.
  - The class table already separates (b, e, q, r) at a big position, so mode-2 classes stay consistent.
- **Leaf correction** (jsep5, argv[7] = `l3q.bin`). At the full row, for every link 7 i and side σ, it adds:
  - `QX = Qeff(c, a, mask(σ, c, w2, w3, w4, a, o)) − UB(c, a)`, which is ≤ 0;
  - `−PQ = −q[(w_{i+σ}, w_{i+2σ}, w_{i+3σ})]`, which is ≤ 0.
- **Why this is exact and sound.**
  - Every correction is ≤ 0, so the window sum stays an upper bound on the true load.
  - All of jsep's pruning bounds (H, V) stay valid.
  - The leaf value is the exact load.
  - jsep5 refuses a file with QX > 0 or PQ < 0 (exit 5 and 6).
- **Mode-2 distinctness.** Each row's class multiset is extended with one id per payer key and one per payee (c, a, m).
  Rows that differ only in their l3q terms therefore stay distinct.
- **Test** (`test_jsep5.py`).
  - Setup: random window tables, random q and Q, and a random mask table.
  - Result: 1,200 top rows, all of them carrying l3q terms (payer terms on 79 of them), with 0 mismatches between jsep5's load
    and the Python load (window sum plus `recv_coef_R2` l3q terms at Qeff).
  - The broken control, with no leaf correction, gives 1,200 mismatches.
- **d ≥ 8 and the tail d ≥ 18** are unchanged, since there are no l3q terms there.
- **upperR2** reads lq and lQ from the solution, writes the same l3q.bin with Qeff, and runs d = 7 through jsep5. Every other d is
  as before.

## 21.7 Flags and regression
- The flag is `l3q`, plus `l3qtab=tab_+1.json,tab_-1.json`. It also takes `lqcap=3`.
- The engine is s28q/eng/, a copy of s24d with the md5s of s24d/engine_md5.txt, patched as above.
- **Flag off:** `lowerR2` on s24d/cert_st24bL.json with argsA59 gives VALID t ≥ 2/13 (`s28q/reg_off_lower.log`).
- **Kill lines** (note): a gain over the same-registry baseline under 0.005, or a total q weight under 1e−3.
