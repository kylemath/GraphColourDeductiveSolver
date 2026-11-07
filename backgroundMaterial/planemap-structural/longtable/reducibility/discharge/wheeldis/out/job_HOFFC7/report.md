# HOFFC7 (Studio, 7 Nov): Lean for the off-centre d7 kills — setup; Lean queued after HDK3c
**Inputs** (Opus claude/project-thread-7uelj0 b4b0fa12, s76_occ502/offc7/), copied byte-identically into in/: lean/OffcOcc.lean 3731ad81,
d7_lines.tsv c36e5a93, fans_d7.tsv afcafcec, kcmap_d7.tsv ce0ec21c, in/kc55.tsv 5821eafc (md5 prefixes all match). Opus scripts/ not read.

## HOFFC7-D: kc re-check (kccheck.py, our code; kccheck.tsv)
d7_lines.tsv has 68 lines: 66 D (66 distinct names), 2 C (hC already in CK108 k108Entries[14], [19]).
For every D line: registry entry re-found (FILE md5 + NAME with D=true, r, m; ST-32 Sources.lookup); kc line from kc55 has the same name, r, m;
kc interior graph + degrees isomorphic to K rebuilt from the name (OFFC_SPEC section 2, ST-32 build_K); kc line present verbatim in its kc_src.
- **53 D kills have a kc line: all 53 ok.** 52 kc lines are verbatim in their kc_src on main; the f10_......5555_......6775 kc line is verbatim
  in loop/opus/ext_check_oct30/mac_reruns/configs.in on b4b0fa12 (that file is not on main).
- f10_......5555_......6775: K(f10) is isomorphic (interior + degrees) to the kc line of HDC502's f8_....5555_....6775 (HDCV.hD_15), r=11 m=8 both: covered, not rebuilt.
- **Engines on the other 52** (eng/, dfast18 07cb1e0b + kc -C -s 60 -t 600 07e79fae): 52/52 D=true on both.
- **13 D kills with no kc line (stopped there; no Conf literals invented):** 12 from out/eq_D7_dfast.out and 1 from out/lp_dfast.out:
  e7_B5555B._65B56.._1111110 (r10 m9), e7_B5555B._B5B56.._1111110 (r9 m8), e7_B5555B._B6B56.._1111110 (r10 m8), e7_B5555.._65BB..._1111100 (r9 m7),
  e7_B5556.._65B5..._1111100 (r10 m8), e7_B5555.._B5BB..._1111100 (r8 m6), e7_B5555.._B5B5..._1111100 (r8 m7), e7_B5555.._B5B6..._1111100 (r9 m7),
  e7_B5555B._BBB6B.._1111110 (r9 m6), e7_B5555.._B6B6..._1111100 (r10 m7), e7_B5556.._B5B5..._1111100 (r9 m7), e7_B5556.._B6B5..._1111100 (r10 m7),
  e7_...6556_...5B5._0001111 (r10 m7, lp_dfast.out).

## Lean (lean/, build root out_hoffc7, nice 20; drive.sh waits for HDK3c GLUEDONE)
- (A) OffcOcc.lean as given (imports COccBridge, DCheckMirror from dc/).
- (D) gen_hd f743a82d on D_offc7.tsv (52 kc lines), MOD HDOF7, PFX hdof7, batch 1: HDOF7, HDOF7V00..51, HDOF7All.

## Addendum (7 Nov, 21:1x): the 13 e7 kills now have kc lines -> HDOF7 has 65 entries
- Inputs (Opus 31501745 offc7/e7kc/, data only, e7kc.py not read): e7kc_stored.tsv 9692e13b, compare.txt 71ecc756, README.md 30526ec1 in in/e7kc/.
- The 12 eq_D7 kc lines: extracted by us from eq_D7_k3.txt.gz (md5 2732ad76) by name (e7/extract_raw.txt); identical to e7kc_stored.tsv (sorted cmp clean;
  names not rotated). The lp kill e7_...6556_...5B5._0001111: Opus's rebuilt line (from the relay) used as is.
- e7/e7check.py (our code): all 13 ok — registry D entry re-found (r, m), kc r/m equal, kc interior + degrees isomorphic to K from the name.
- Engines (e7/e*.out): dfast18 and kc -C both D=true on all 13, each reproducing the registry classes/ext/reached exactly.
- gen_hd f743a82d rerun on D_offc7.tsv (52 + 13 = 65 lines; entries 0..51 unchanged, 52..64 the e7 kills): HDOF7, HDOF7V00..64, HDOF7All; drive.sh restarted, still waiting for HDK3c GLUEDONE.
- With f10 covered by HDC502 and the 2 C by CK108, all 68 d7 lines will then be Lean-backed.
