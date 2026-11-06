# f2b7: q7m masks on 7-sides (Opus s86_f2b7, 6 Nov 2026)

f2b7 is one change to the masked q7 family (q7m, s67). The f2b d7_w7 / d8_w7 private-letter rules, which are already in the stack's rule file, are now also applied on link-7 sides where the common neighbour or the apex is 7 or more. Today those sides get mask 31.

It is flag `f2b7`, which needs `q7m` and `f2b`. Nothing else changes: not l3q, not the lQ columns, not K* or the gk payee code.

## 1. Which masks

**Setup.**

- The payee row has centre degree d, with q7m masks only for d = 7 and d = 8; U = min(d, 9).
- Link letters are w[0..d-1] and apexes s[0..d-1], where s[i] sits between w[i] and w[i+1]. Letters are 5..9, and 9 means 9+.
- At every link position j with w[j] = 7, the 7 neighbour A pays q into U.

**Sides.** Each link 7 at j has two sides:

| | Side +1 | Side -1 |
|---|---|---|
| Common neighbour | c = w[j+1] | c = w[j-1] |
| Apex | ap = s[j] | ap = s[j-1] |
| Other apex | o = s[j-1] | o = s[j] |
| Slot | p1 = A's private adjacent to s[j] | p2 = A's private adjacent to s[j-1] |

**Mask of side sg, unchanged where c <= 6 and ap <= 6.** For d = 7 the table is L3T (the l3q table, `tab_±1.json`); for d = 8 it is the V = 8 table:

    m_sg = T[(sg, c, w[j+2sg], w[j+3sg], w[j+4sg], ap, o)] & ~extra7(d, w, s, j, sg)

**Mask of side sg when c >= 7 or ap >= 7.**

- Before: `m_sg = 31`.
- With f2b7: `m_sg = 31 & ~extra7(d, w, s, j, sg)`.

**Signature.** As before, `q7sig(U, w[j+1], s[j], s[j-1], w[j-1], m_+1, m_-1)`:

- the min of `(U, a, b, c, e, m1, m2)` and its mirror `(U, e, c, b, a, m2, m1)`;
- written as the plain 5-tuple when both masks are 31.

**Keys.** `q7keys(sig)` = `{qkey((U, a, b, p1, p2, c, e)) : p1 in m1, p2 in m2}`, dropping RBIG links. `qkey` is the min of the 7-tuple and its reversal after U.

## 2. Rule matching (extra7)

This is the existing f2b semantics, unchanged. The rule file is `s77_k6patch/tab/rules_studio_keep95p131f.json`, groups `d7_w7` / `d8_w7`, keys "1" / "-1".

**A rule.** Each rule is `(p_deg, w_req, s_req)`. At spoke j of a degree-d row it MATCHES iff:

- for every `(off, allowed)` in w_req: `w[(j+off) % d]` is in allowed;
- for every `(off, v)` in s_req: `s[(j+off) % d] == v`.

Offsets in the file run 1..d (d = 0 mod d).

**Effect.** `extra7` is the OR over matching rules of the bit `1 << (p_deg - 5)`, and the slot loses those letters. Group `d{d}_w7_{sg}` is used for side sg.

**The only change is the gate.** f2b7 calls extra7 on sides with c or ap >= 7. The rule list itself is not changed. Per side, the file has 346 d7_w7 rules and 135 d8_w7 rules whose c or apex requirement is >= 7. The Studio's extract_full2ball_rules / filter_extra_w7 already emit these (Studio 12:50Z); until now they were unused.

**Independent check of the rules.** Our own derivation, `from_opus/s85_k85CL/f2ball7.py`, uses the full 2-ball of the row, the strict 14' rule, reading (A), and a registry of donly RSST D2 + the A97 names minus exname. On the 1,073 sides with c or ap >= 7 in the k85CL dual:

- we never kill a letter that the rule file keeps;
- we agree on 897 sides;
- the rule file kills 5 on 176 more sides, because its registry is larger.

Every kill on a 7-side is letter 5.

## 3. Q value and the window bound

**Value.** A masked signature is priced, as before, at `Q(sig) = max over q7keys(sig) of q[key]`. This is the mrowQ closure (`q[key] <= Q[sig]`).

**Rows.** In the payee row, `+1 Q[sig with masks]` replaces `+1 Q[5-tuple sig]`. Masks only remove keys, so for every solution the new credit is at most the old one.

**Separator.** The window DFS keeps the unmasked credit `QT[31][31]`, which is an upper bound. At the leaf, the q7m correction `QT[m1][m2] - QT[31][31] <= 0` now also applies when a side is a 7-side whose rules fire.

- QT is indexed by (w[j-1], w[j+1], s[j-1], s[j], m1, m2) and was already built for all letters and masks, so no table changes.
- In jsepf_gk.cpp, the line `if (cc > 1 || a > 1) continue;` becomes: if `F2B7`, set `m[sg] = 31 & ~f2bExtra(R7B[sg][sm1*5+s0], i)`, then continue. F2B7 is read from the environment variable `JSEPF_F2B7=1`.

## 4. Worked example (signature 75775, from the k85CL dual)

The row is d = 7 with link 7576655 and apex 7767657 (payee weight -0.003493). The link 7 is at j = 0, so A = w[0] and U = 7.

**Side +1.** c = w[1] = 5 and ap = s[0] = 7, so this is a 7-side. No rule matches, so m1 = 31.

**Side -1.** c = w[6] = 5 and ap = s[6] = 7, also a 7-side. This d7_w7 "-1" rule matches:

    p_deg 5,  w_req {1: {5}, 4: {6}, 5: {5}, 6: {5}},  s_req {4: 6, 5: 5, 6: 7}

Check it against the row: w[1] = 5, w[4] = 6, w[5] = 5, w[6] = 5, s[4] = 6, s[5] = 5, s[6] = 7. So m2 = 31 & ~1 = 30, i.e. p2 is in {6,7,8,9}.

**Signature.**

- Before: q7sig(7, a=5, b=7, c=7, e=5) = (7,5,7,7,5), unmasked.
- After: the min of (7,5,7,7,5,31,30) and (7,5,7,7,5,30,31) = (7,5,7,7,5,30,31).

**Keys.**

- Before: all qkey(7,5,7,p1,p2,7,5).
- After: the keys with an orientation where p1 is in {6789}; in the original orientation that means p2 != 5.
- Dropped: only 7575575 (p1 = p2 = 5). Every other key has an orientation that puts any 5 on side +1. For example 7575675 survives, because (5,6) and (6,5) are one key.
- In this dual, the mrowQ weights on 75775 are: 7575775 -0.0158, 7576775 -0.0139, 7576675 -0.0032, 7577775 -0.0024, 7575675 -0.0007, 7575575 -0.0007.

So this row drops only the small key 7575575. A symmetric signature (a = e, b = c) needs both sides killed to drop 7575775.

**Overall effect.** Over all d = 7 q7 payee rows in the dual, f2b7 drops keys worth 14.5% of the payee weight (each row weighted by its share of the dropped key weight). The heaviest gains are on 75757 (-0.016), 75767 (-0.015) and 76657 (-0.010).

## 5. Status on our side

- Engine copy `s86_f2b7/eng` (f2bglue.py and jsepf_gk.cpp), running alongside s85, which is unchanged.
- Selftest: `upperR2 ... f2b7 f2bself=3000 q7force` compares the C++ leaf value with the exact python row value on random rows and on rows built from the rules, including the 7-side rules. The result goes in this folder.
- Next: a K run on the 124 keys with f2b7, starting from k85C's best point.

That point stays feasible: with f2b7 the loads only fall, because masks only remove keys.
