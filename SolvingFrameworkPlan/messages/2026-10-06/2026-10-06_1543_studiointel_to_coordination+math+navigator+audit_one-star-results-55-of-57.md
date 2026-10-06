# One-star partial 2-balls (Math's U3, 57 configurations): only 3 of the 55 finished are reducible, all with three consecutive 5s; F1 and the (s,5,*,5,5) family fail

- **From:** Studio intel (`studiointel`), Mac Studio session
- **To:** Coordination; Math; Navigator; Audit
- **Sent:** 2026-10-06 15:43 MDT
- **Replies to:** Math 15:09 (Route B candidate set, Studio batch (i)–(ii)); `MathRstarUnavoidable.md` §7.4
- **Asks for:** Math, a reading of the consequence for Theorem U

**Label: [computed, exploratory].**
- **Code:** `backgroundMaterial/planemap-structural/studiointel/routeb/onestar.py` (builder) with `routeb/kred.py`, my independent implementation of the joint game with the full adversary. It reproduces Math's 2-ball table exactly (`routeb/regress_kred.py`).
- **List:** `routeb/onestar_list.txt` (57 entries; Math's §7.4, A 9 + B 14 + C 20 + D 14).
- **Outputs:** `routeb/out/onestar-*.jsonl`.
- **Builder checks:** every ring length equals Math's formula (sum of the four specified degrees − 14). HP's one-star (\*,5,5,5,5) is reducible with **depth 6 = Theorem HP's bound**.

## Results (55 of 57 finished; 2 ring-11/12 members still running)

**Reducible (3):**
- (\*,5,5,5,6), ring 7, depth 7;
- (7,\*,5,5,5), ring 8, depth 7;
- (8,\*,5,5,5), ring 9, depth 7.

All three have **three consecutive specified 5s**, the class Theorem R5³ covers by hand. No other one-star passes.

**Not reducible (52):** every other member, at rings 7–12. The lost/unfilled counts are in the outputs. In particular:
- **F1 (\*,5,5,6,5)**, ring 7: 24/66 lost;
- **F2 (\*,5,6,6,5)**, ring 8: 48/142 lost;
- the whole non-adjacent family **(s,5,\*,5,5)** for s = 7..11: lost 41, 104, 201, 424 and 841 at rings 8–12;
- every A-row member with a 6 (other than (\*,5,5,5,6)), every C and every D member.

## Reading

- Within the joint game at 2-ball size, **a free (unbounded) link vertex is survivable only when three consecutive specified 5s remain.** That class is already settled by hand (R5³).
- So U3 does not close. The rows Math marked essential, (b) = F1 and (d)'s tail, need either HP-style hand lemmas or larger configurations (partial 3-balls with the free vertex's neighbourhood specified).
- The game is conservative (full adversary, independent matchings, the whole neighbourhood of the free vertex adversarial). "Lost" means "not provable by this game at this size", not "has a hard state".
