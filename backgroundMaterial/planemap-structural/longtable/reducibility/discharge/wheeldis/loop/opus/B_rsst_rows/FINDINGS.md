# B_rsst_rows: do RSST's 633 configurations forbid the free tight receiver rows?

Q: How many free tight receiver rows (7/27 binders, HARD28-like rows, tight families) contain an RSST configuration inside the part of u's neighbourhood they fix exactly?
Guess (08:40, before computing): very few or none. A d=7 receiver row fixes about 2 rings (u, 7 link vertices, shared s_i, some 5-sender privates). Most RSST configs have ring 12-14 and need many exact-degree interior vertices, and the registry already includes the small ones (stars, wheels).
Would change the plan: if a material share (>~20%) of the binders/HARD28 rows die, rerun the LP with those as patterns and get a feasibility upper bound. If ~0 die, RSST's set does not act at the receiver, and K>=2 needs other tools.

## Answer (09:10Z): RSST does not move t*. It stays at exactly 7/27 [E]. The binder survives because the slots RSST needs are slots the LP row leaves free.

### What a receiver row fixes (from wlp.py, wlp3.py, sep3.cpp)
- u has exact degree d.
- w_i is u's link. s_i is the apex of the triangle w_i w_{i+1} s_i.
- A 5 at w_i contributes the variable y[rooted word (U, w_{i+1}, s_i, s_{i-1}, w_{i-1})] (taken up to reflection). The LP row is the **multiset** of these words.
- So a slot is *pinned* only if some 5-sender's code reads it. That means:
  - w_i is pinned when it is a 5 or next to a 5;
  - s_i is pinned when w_i or w_{i+1} is a 5.
- Every other s_i (between two non-5s) and every other w is free. The printed link/s word is one representative of the row. Patterns (sep3 masks) can only constrain pinned slots.
- Known graph among {u, w, s}:
  - u ~ w_i, w_i ~ w_{i+1}, and s_i ~ w_i, w_{i+1};
  - s_{i-1} ~ s_i exactly when w_i = 5;
  - nothing else, by internal 6-connectivity [I].
- RSST appearance (rsst_contain.py semantics: interior maps injectively, exact degrees, induced, faces to faces) is tested in three modes (`rsst_rows.py`):
  - **strict** (your rule): interior only at u and at exact link letters;
  - **relaxed**: exact s letters may also host interior vertices. This is valid RSST appearance, because s's unknown outer neighbours are only ring vertices of K;
  - **fixed**: relaxed, but only on pinned slots. This is the mode that can actually forbid an LP row.

### The 7/27 binder (d=7, link 5675765, s 6577575; `binder_row.py`, `out/binder_row.txt`) [E]
- strict: 0 of 633.
- fixed (u, the link, s0, s2, s3, s5, s6, with all three 5-wheels complete): 0 of 633.
- relaxed: one config, 128.136 (ring 11, C). Its interior is u=7, w0..w3 = 5,6,7,5 and s1=5, or the mirror image with s4=5. But s1 and s4 sit between non-5s and are free in the LP row. 16 of the 25 (s1, s4) fillings (both >= 6) are RSST-free. **The row survives.**

### Counts over the tight families (`out/rows_hits.txt`; rows forbidden / rows) [E]
| family | rows | strict | relaxed | fixed (LP-meaningful) |
|---|---|---|---|---|
| loop/b7/binders.txt (older binders) | 7 | 0 | 7 | 6 |
| out/job28/binders_self.txt | 5 | 0 | 5 | 4 |
| HARD28-like 49 (loop/lf/seeds.txt) | 49 | 1 | 26 | **2** |
| HARD28 round 12 | 15 | 0 | 9 | **1** |
| tight_12 (227 / 1519 / 1435 at d = 7 / 8 / 9) | 3181 | 2009 | 2880 | 2692 (105 / 1176 / 1411) |
| tight_13 (566 / 397 / 422) | 1385 | 558 | 1073 | 920 (263 / 299 / 358) |

- The big killers are fans around u, which the registry never had. Examples:
  - 439326.122 (D, ring 11): a 9 with link run 555655;
  - 7326.122 (C, ring 10), 453722.126 (C, ring 12), 122.8406 (D, ring 11).
- 122.8406 kills the old binder 5675765/6575575 (s3=5 is pinned). The current binder differs from it only in the pinned s3 = 7.
- Many d = 8/9 and older tight rows die, but the HARD28-like rows barely do: 2 of 49 at the slots the LP fixes.

### LP rerun (`wlp3r.py` = wlp3.py plus raw sep3 patterns `rpat=`; `out/rpat_r0.txt`; `out/wlp3r_w0.txt`) [E]
- Patterns: 387 distinct sep3 patterns (88 at d=7, 166 at d=8, 133 at d=9). They come from every encodable fixed-mode embedding in the 4,628 warm rows (tight_12, tight_13, the binders, the 49).
- Registry: the full L2 set (round-13 args plus loop/n9 win9/25/25b/27/29). Missing locally: r_5..r_8 (d=10 only).
- Of the 4,628 warm rows, 804 survive (`check`).
- The LP on the surviving warm rows gives t = 0.259259 = 7/27. The dual certificate is unchanged: senders 55667 / 55767 / 77777, plus the binder 5675765/6577575.
- That is a **lower bound**: the binding row is genuinely allowed. It is d=7, so the missing d=10 files are irrelevant, and it is RSST-free on pinned slots.
- The **upper bound** is the existing feascheck 7/27 on the full registry: adding patterns can only lower t*.
- **So t*(registry ∪ RSST-in-patch) = 7/27 exactly. No gain.**

### Which RSST configs can ever fit inside a d=7 receiver's patch (`out/generic_7.txt`; every link word over 5..9 up to symmetry, s free) [E]
- strict: 8 of 633: ring 8 D 1, 9 C 1, 10 C 1, 10 D 1, 11 C 1, 11 D 1, 12 D 2.
- fixed: 74 of 633: rings 6..13, 44 D and 30 C.
- relaxed: 154 of 633: rings 6..14, 62 D and 92 C.
- So RSST does speak at the receiver: a quarter of its set fits a 7's two-ring patch. Mostly these are fans: a hub at u, consecutive link letters, and 1-2 s vertices.

### Inferences [I]
- The binder is not a missing-configuration problem at u's patch. Its only RSST obstruction needs s1 = 5 or s4 = 5, and those are slots the rooted-word rule class cannot see. This is the same rule-class limit as before (Job 28 prediction).
- Forbidding s1/s4 = 5 would need rows or patterns that read the s between two non-5s, i.e. a richer rule or row language. Even then, 16 of the 25 fillings stay RSST-free.
- RSST fans are worth adding to the registry as hygiene: they kill 920 of 1385 round-13 tight rows, including 263 at d=7. But at this optimum they are not binding.
- Plan change: drop "RSST as receiver patterns" as a K>=2 lever for 7/27. A lever has to act on the free slots (s between big/6 letters, or beyond the patch), or change the rule class.
