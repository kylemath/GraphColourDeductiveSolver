# f2b041 self-test diff: Opus's f2b implementation vs Studio's (job 1, relay 3 Nov 01:37Z)

**Result: 0 differing cells.** I compared 212,970 rule-match cells over 9,960 arrangements, and 59,753 of those cells have a
nonzero mask.

## Source
- **Opus's code:** branch claude/project-thread-7uelj0, commit **1240de60ba97f183b13d365b0f9f61712275ce6e** (the 39-character
  prefix 1240de60…ce6 resolved uniquely), directory loop/opus/ext_check_oct30/f2b_impl/.
- **Files read** (copied read-only into opus_f2b_impl/): MD5SUMS.txt, REPORT.md, f2b.py, f2b_selftest.py, sep3r_f2b.cpp and
  st21_f2b.py. All md5s match MD5SUMS.txt:
  - f2b.py 0f78e528
  - f2b_selftest.py 7fb0a323
  - sep3r_f2b.cpp 435a702f
  - st21_f2b.py bd21af57
  - REPORT.md d5075435
- **Not opened:** s60_f2b/eng/ (Opus's engine: pcheck, offc, psolve, jsep*, …), run.sh and run_mac.sh. Nothing of theirs was run
  except `import f2b`.
- Studio's verdict 80287bd3 was committed before any of these files were opened.

## Method (selftest_diff.py, selftest_diff.log)
I wanted a comparison that needed no edits to their code.
- **Their side:** Opus's f2b.py is imported unchanged and loads the rules with `f2b.load(rules)`.
- **Our side:** Studio's matcher, `f2b_extra` with its rule compiler, is exec'd from out/job31/st21_check_f2b.py.
- **Inputs:** both read the same rules JSON (b9de962e). The group counts are equal: 1386 / 1176 / 60 / 938 / 938 / 728 / 728.

For every arrangement, every position i, and every side, I compared the killed-letter mask:
- `f2b.extra6` against Studio's ('w6', d) mask at d = 7..9;
- `f2b.extra7` against Studio's ('w7', d, ±1) mask at d = 7, 8.

The comparison covers every cell, not only the cells the row reads. Two arrangement sets were used:
- **Studio's 6,000 self-test arrangements** (seed 41, 85% rule-driven, rotated): 129,204 cells, 34,382 nonzero, **0 differ**.
- **Opus's f2b_selftest.py cases**, replayed with their `_gen` and their Random(12345) sampling order: up to 400 per group (all 60 for
  d9_w6), plus 1,500 random rows at d = 7..10. That is 3,960 arrangements and 83,766 cells, 23,371 nonzero, **0 differ**. Per group:

| group | cells | nonzero | differ |
|---|---|---|---|
| d7_w6 | 8,400 | 3,433 | 0 |
| d7_w7 +1 / −1 | 8,400 / 8,400 | 3,184 / 3,202 | 0 / 0 |
| d8_w6 | 9,600 | 2,721 | 0 |
| d8_w7 +1 / −1 | 9,600 / 9,600 | 2,544 / 2,420 | 0 / 0 |
| d9_w6 | 540 | 80 | 0 |
| random | 20,826 | 2,787 | 0 |

The masks feed both the Python row and the C++ leaf. In each implementation, Python and C++ already agree to 1e-9 on that team's own
self-test: ours was 6,000 arrangements with 0 mismatches. The two value-table layers are built from the same M / Qeff / Qeff8
definitions over the same tables, so equal masks give equal rows.

## Code diff notes
**sep3r_f2b.cpp (Opus) vs sep3r_f2bS.cpp (Studio).** Both are copies of the frozen sep3r_l3q.cpp with an opt-in leaf delta, an
`f d link s` self-test command, and a binary table file.
- **Rule match:** the design is the same. Both rotate the word into bitsets `rw` / `rs` (bit 5·off + letter), use forbidden-letter
  sets `fw` / `fs`, and bucket by (s_{i−1}, s_i).
  - Opus buckets in Python at serialisation time, using the s_req at offsets −1 and 0. It also merges identical (fw, fs) into one
    entry with OR'd kill bits.
  - Studio buckets in C++ at load time, testing fs at offsets d−1 and 0, and keeps one entry per rule.
- **Link-6 delta:** Opus uses EXM[window][m0 & ~ex] − EX6[idx8]; Studio uses MT[window][m0 & ~ex] − MT[window][m0]. These are
  equal because Studio checks MT[m0] = EX6 on all 1,171,875 windows, 0 mismatches. The window keys are the same; only the index
  order differs.
- **Link-7 delta:** Opus uses QM7/QM8[c][a][mk] − L3QEX/L8X[q]; Studio uses QF[c][a][mk] − QF[c][a][m0]. These are the same, since
  L3QEX[q] = Qeff(c, a, m0).
- **Gating:**
  - Opus applies the link-7 branch at d = 7, 8 whenever SEP_F2B is set. Studio also requires HASL (d = 7) / HASL8 (d = 8). In this
    run L3Q and L3Q8 are both on, so the two agree.
  - Opus adds the delta before the FB block; Studio adds it after every exact term. With FB = 0 these are the same, and both add it
    before the threshold return.
- **Validity:** neither copy changes the relaxed window bound. The delta is ≤ 0 in both, by monotonicity (Studio checks this).

**st21_f2b.py (Opus) vs out/job31/st21_check_f2b.py (Studio).**
- **Opus:** a wrapper that reads Studio's st21_check.py at run time and applies string replacements. It makes the same three
  recv_spec mask shrinks (`& ~f2b.extra6`, `& ~f2b.extra7` on MASK and MASK8) and swaps in the f2b binary. It also adds:
  - controls NVIOL / VIOLSUM, THRSHIFT, STOPIFVIOL, DSTART / DSTOP;
  - modes F2B_MODE = on / off / half, where half drops 50% of the rules at random by seed;
  - F2B_BIN = old for the frozen sep3r_l3q;
  - OUTD for the tables.
- **Studio:** a committed copy of st21_check.py with the same three shrinks, guarded by F2B. It also has:
  - F2BHALF = 0 / 1, which keeps the even- or odd-indexed rules (a deterministic half);
  - DLIST for degree splits;
  - its own table writer and self-test, with consistency and monotonicity checks.
- **Equivalence:** the row logic is identical. Both shrink before the cand2 test, so an emptied mask drops the M term in both, and
  an emptied l3q mask gives lQ key (c, a, 0) → Qeff = 0 in both.
