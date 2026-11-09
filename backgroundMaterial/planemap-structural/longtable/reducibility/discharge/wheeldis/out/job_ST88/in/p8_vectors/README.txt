p8_vectors: payer-8/9 EDGE key test vectors for a spec-only harness (Studio ST-88, code_gk8)
==========================================================================================
Written by W6b on 9 Nov 2026 (about 17:40Z), next to PAYER8SPEC.md (md5 70f7ffa0). PAYER8SPEC.md and p8_test.json (ec18af58) are unchanged.
p8_test.json is a result summary. These files are the vectors behind it (section c) plus new vectors on the GS14_01 cert (sections a, b, d).
All files are plain text, one record per line. Lines starting with # are comments. SHA256SUMS lists every file. code/ holds the two
generators and their logs (they print the cross-checks quoted below).

CONVENTIONS
-----------
* Letters 5, 6, 7, 8, 9 are vertex degrees, and 9 means "9 or more". A letter set is written as one letter (5), as {56} (5 or 6), or as * (any of
  5..9). Classes: S = {56} and B = {789}.
* The 10 key positions are S.L+1 S.L+2 S.L+3 S.L-1 S.L-2 S.L-3 S.A+1 S.A-1 R.L+2 R.L-2. A key position that is not listed is *.
* A key is (payer set U, payee set V, a letter set per listed position). Every GS14 key used here has payer U = {8} or U = {9} and is a W5
  key: S.L+3 and S.L-3 are never listed.
* A row picture yields SLOTS. A slot is (role, payer letter -> payee letter, a letter set at each of the 10 positions):
    - an IN slot counts for the key when the payer is in U, the payee is in V, and every position's set MEETS the key's set (possible match);
    - an OUT slot counts when the payer is in U, the payee is in V, and every position's set is INSIDE the key's set (sure match).
  The key's coefficient in the row is:
    - receiver and cons2 rows: IN - OUT (the load on the centre);
    - sender rows: OUT - IN.
* Chirality: each oriented pair has two slots, sg = +1 and its mirror sg = -1. The mirror swaps every +/- position name:
  S.L+k <-> S.L-k, S.A+1 <-> S.A-1, R.L+2 <-> R.L-2.
* Indices: link w_0..w_{d-1} around the centre, and apex s_j between w_j and w_{j+1}. All indices are mod d.

ROW ENCODINGS (cert row -> text; rows_GS14_01.txt)
---------------------------------------------------
* receiverR2 [d, link, apex] -> `Rnnnn d=.. link=w_0..w_{d-1} apex=s_0..s_{d-1}`. Every link and apex letter is exact.
    - d = 7 rows are "picture" rows. Each link vertex of letter x has x - 5 private neighbours. Their letter sets are the stack masks of
      KEYSPEC section 5 (pmask & ~extra6 for a 6, MASK & ~extra7 for a 7, * for 8 / 9+), computed on the GS14 stack. They are printed after
      `privates`, one group per link vertex w_j, ordered from the s_{j-1} side to the s_j side. A 5 has none (-).
    - d >= 8 rows are gkwin "window" rows. They have no private list: their slots follow the window rule below.
* senderR2 [link, "H0 H1 H2 H3 H4 | F..."] -> `Snnnn d=5 link=.. apex_classes=.. six_private_classes=..`:
    - The centre is a 5. The link w_0..w_4 is exact.
    - apex_classes (e.g. SBSSS) is the class of apex s_0..s_4. It comes from the H bits: 0 -> S = {56}, 1 -> B = {789}.
    - six_private_classes `j:c` gives, for each link 6 at link position j, the class of its single private neighbour. These are the F bits,
      one per link 6 in link order. The field is `none` (in the JSON exports: an empty object / null) when the link has no 6.
    - Privates: a sender's 6 with a class has that class as its one private. A link letter x >= 7 has x - 5 privates, all *. A 5 has none.
    - In the coefs16s.json row tuples [type, d, link, apex-or-classes, w], d is null for sender and cons2 rows, because the centre degree is
      fixed (5 / 6). The 4th field is the apex class word (SBSSS) for senders and the exact apex witness word for cons2.
* cons2 [link, apex witness] -> `Cnnnn d=6 link=.. apex_classes=.. apex_witness=..`:
    - The centre is a 6. The link is exact.
    - apex_classes come from the witness word: 5 / 6 -> S, 7+ -> B. The picture uses only the classes; the witness is given for reference.
    - Every private is *.
* mrow rows carry no key terms and are not listed.

SLOT FORMULAS (the reference p8_ref.py, written from KEYSPEC section 5, DUAL_EXPORT gkwin, and PAYER8SPEC 3.1 / 3.2; chirality +1)
-----------------------------------------------------------------------------------------------------------------------------------
Picture rows (d = 7 receiver, sender, cons2), centre letter c:
  IN  payer w_j -> c:
      - S.L+1 = w_{j-1}, S.L-1 = w_{j+1}; S.L+2 = s_{j-1}, S.L-2 = s_j (apex sets); R.L+2 = w_{j-2}, R.L-2 = w_{j+2}.
      - S.L+3 / S.L-3: if w_j = 5, then s_j / s_{j-1}; otherwise w_j's private next to s_{j-1} / next to s_j (its first / last private).
      - S.A+1 = s_{j-2} if w_{j-1} = 5, else w_{j-1}'s private next to s_{j-1}.
      - S.A-1 = s_{j+1} if w_{j+1} = 5, else w_{j+1}'s private next to s_j.
  OUT c -> w_i:
      - S.L+k = w_{i+k}, S.L-k = w_{i-k} (k = 1, 2, 3, exact).
      - S.A+1 = s_{i+1}, S.A-1 = s_{i-2}; R.L+2 = s_i, R.L-2 = s_{i-1}.
      - The centre is 5, 6 or 7, so payer-8/9 keys never match these slots.
Window rows (d >= 8), centre letter U = min(d, 9):
  IN  payer w_j -> U:
      - S.L+1 = w_{j-1}, S.L-1 = w_{j+1}, S.L+2 = s_{j-1}, S.L-2 = s_j, R.L+2 = w_{j-2}, R.L-2 = w_{j+2}.
      - S.L+3 / S.L-3: payer 5 -> s_j / s_{j-1}; payer 6 -> amask(j) for both; payer 7, 8, 9 -> * (own privates; PAYER8SPEC 3.2: the gate is
        widened to payers 5..9, and 8 / 9 take the payer-7 branch).
      - S.A+1: w_{j-1} = 5 -> s_{j-2}; w_{j-1} = 6 -> amask(j-1) with (w_{j-3}, s_{j-3}) free; otherwise *.
      - S.A-1: w_{j+1} = 5 -> s_{j+1}; w_{j+1} = 6 -> amask(j+1) with (w_{j+3}, s_{j+2}) free; otherwise *.
      - amask(k) = OR of pmask(U, w_{k-2}, w_{k-1}, w_{k+1}, w_{k+2}, s_{k-2}, s_{k-1}, s_k, s_{k+1}) over the free arguments. pmask is a stack
        table, so the resulting sets are printed in the slot files and the harness does not need the table.
  OUT U -> w_i (PAYER8SPEC 3.1; payer-8 keys only at d = 8, payer-9 keys at every d >= 9):
      - S.L+1 = w_{i+1}, S.L+2 = w_{i+2}, S.L-1 = w_{i-1}, S.L-2 = w_{i-2}.
      - S.A+1 = s_{i+1}, S.A-1 = s_{i-2}; R.L+2 = s_i, R.L-2 = s_{i-1}.
      - S.L+3 = S.L-3 = * in mode W5 (so an OUT slot counts only if the key leaves them free); w_{i+3} / w_{i-3} exactly in mode W7.
  In the OUT lines of a_*.txt only the 8 positions the spec defines are printed (S.L+-3 are * in W5). slots_GS14_01.txt prints all 10.

FILES
-----
rows_GS14_01.txt (1,132 rows)
    The receiverR2 / senderR2 / cons2 rows of lpdual_k86GS14_01.json (abb4c752), in cert order. Ids are R/S/C + index.
slots_GS14_01.txt
    Every reference slot (IN and OUT, both chiralities, all 10 positions) of every row above, W5.
a_receivers_GS14_01.txt  [request (a)]
    For each of the 24 keys of cg_keys_w6b16s_p8_k86GS14.txt (b8bcafba): every receiver row of the cert (d = 7 and d >= 8) with at least one
    matching slot, given as `IN= OUT= coef=`, then one line per matching slot (OUT lines: i, sg and the 8 defined positions; IN lines: j, sg
    and the 10 positions). 4,206 (key, row) entries.
b_senders_cons2_GS14_01.txt  [request (b)]
    The same for sender and cons2 rows (sender coef = OUT - IN). 3,037 entries. Payer-8/9 keys give only IN here (a link 8 / 9 paying the
    centre).
    Every coefficient in a / b was also computed by the pricing builder (p8lib.row_items + G.coef_rows, mode W5, GS14 stack, P8F2B7PIC=0):
    0 mismatches (code/p8vec_gs14.log).
c_A_out_slots.txt, c_B_window_in_slots.txt, c_C_rows_slots.txt, c_C_keys.txt, c_C_values.txt  [request (c)]
    p8_test.py sections (A), (B), (C) of round 14b, regenerated with the same rng stream (seed 14) in the same round-14b A97+F environment.
    The counts reproduce p8_test.json exactly:
      (A) 2,256 OUT slots;
      (B) 1,128 window IN slots, 246 of them with payer 8 / 9;
      (C) 120,000 (row, key) pairs, 20,390 nonzero in W5 and 21,240 in W7, 0 builder-vs-reference mismatches.
    (A) lists the OUT slots of 63 window rows W00..W62 in W5 and in W7 (checked against grammar.edge_vec).
    (B) lists the IN slots of the same rows (payers 5..9).
    (C) has:
      - 400 random rows X000..X399 with every slot spelled out;
      - 300 random keys K000..K299. Some have mixed payer sets such as {89}; the reference reads "payer letter in U". Real PAYER8SPEC keys
        have payer exactly 8 or 9.
      - c_C_values.txt: lines `row key W5 W7` for all 120,000 pairs.
    The d = 7 privates and amask sets of section (c) belong to the A97+F stack, not the GS14 stack. They are spelled out in the slot lines.
d_controls.txt  [request (d)]
    8 planted-control lines. Each gives (bug, key, GS14 row, correct coef, the wrong value the bug gives):
      - outposs: OUT counted on a possible match. Keys with an S.L+-3 condition then get OUT, e.g. coef -10 instead of 0.
      - outmirror: for sg = -1, S.A+-1 of the OUT slot are not mirrored.
    A harness that reproduces the wrong value has the bug.
code/
    p8vec_gs14.py (sections a, b, d; GS14 stack) and p8vec_t14.py (section c; built from p8_test.py), with their logs.
