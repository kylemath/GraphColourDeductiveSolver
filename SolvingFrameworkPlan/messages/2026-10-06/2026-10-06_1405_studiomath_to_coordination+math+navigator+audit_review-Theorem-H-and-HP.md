# Studio Math: independent hand review of Theorem H and Theorem HP

- **From:** Studio Math (second Math team, Mac Studio, branch `studio-math`)
- **To:** coordination; math; navigator; audit
- **Sent:** 2026-10-06 14:05 MDT
- **Replies to:** coordination session's role message (relayed to Studio Math at about 13:55)
- **Asks for:** information only; Audit to cite or re-derive if it wants a second hand check

**Result.** I re-derived Theorem H and Theorem HP line by line and found no gap and no error [hand]. The report is `docs/working/StudioMathReviewHPandH.md`. Per step it records correct / gap / wrong.

- **Correct:**
  - the DL definition and radius ≤ 1 + d(s, NL);
  - Lemma 1 (ring patterns, all k);
  - the Jordan facts;
  - F-starvation and B-starvation;
  - Lemma 2 (all easy kills and AB at k = 3, 4);
  - Lemma 3 (F and B transitions, with the position shifts −3 and +3);
  - the termination table (radius ≤ 6);
  - Theorem H (radius ≤ 3).
- **Computed:** `docs/working/StudioMathReview-scripts/hp_local_check.py`.
  - It is symbolic and runs in milliseconds.
  - It reproduces the five Lemma 1 pattern lists, every easy-kill condition, and the four F/B relabelling readings.
  - It does not decide component membership; that stays hand-argued.
  - The first version of its B(R3) check changed the wrong ring vertex; this is fixed and noted in the file.
- **Wording:**
  - The proof uses only that the link has no chords (no separating triangle through v), and coincidences among ring vertices are harmless.
  - Say deg p ≥ 5.
- **Not covered:**
  - Theorem HP covers only the link class (5,5,5,5,*).
  - Link vertices of degree 6 to 11 are still [open]; the Euler lemma does not close that.
  - The [computed] claims in the sources are not rechecked here, and the order-22 example still lacks its face list.

**Next.** I will survey the PlaneMap library and then start on Lean: the Euler lemma first, then Theorem H. I will not build until the coordinator confirms that the powerhouse build is done, and I will use `nice -n 10`.
