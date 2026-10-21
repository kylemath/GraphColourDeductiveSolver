# Studio farm staging (21 Oct)
- **run_bin.py:** from claude/project-thread-idl1b5, md5 e73486a6. Reviewed: it writes only NAME.txt / NAME.txt.timeout / NAME.txt.tmp inside
  OUTDIR, makes no network or git calls, uses ThreadPoolExecutor(N), and runs on Python 3.9.
  - Concern 1: preexec_fn with threads (NICE) is officially not fork-safe; it works in practice on macOS.
  - Concern 2: there is no memory gate, so the 30 GB rule for heavy calls must come from the slot count.
- **kc.cpp:** md5 f9da2a70 in Studio's tree = main = the farm's. Studio's kc binary (md5 07e79fae, built 18 Oct) gives output byte-identical to a
  fresh -O2 rebuild of that source on 4 windows (timing aside). The binary md5 differs because the original flags are not recorded.
- **kcf.cpp:** 6be804c4 farm63/kcf.cpp, md5 7fd660a6 = kc.cpp + the fillings module (option -F TMAX; after a non-D run, A chord-only,
  B separator+chord, C0 / C1 contraction into one ring vertex, D an uncapped general-contraction local search: "FZERO" when leftover 0).
  No system or network calls; it writes a file only if DUMPBAD is set.
  Built with `g++ -O3 -march=native -I<shim> -o kcf kcf.cpp` (Apple clang 17.0.0, local bits/stdc++.h shim, nothing installed):
  **bin/farm/kcf md5 391f2d13ae420ae63d59d930dd7b475b**.
- **Self-test** (kcf_selftest_*.out, 3 ring-16 windows; kcf -C -F 8 vs kc -C -s 60 -t 600): D and C lines are identical apart from timing.
  - r7665566_6675676_w0_priv66: D=true.
  - f8_..556856_....5566: D=false, C-REDUCIBLE X={I0-I1}. kcf also prints FZERO (groups[0,7,2,3,4,5,6,7,8,5,10R7], pinned), as
    expected for a known C entry.
  - a7_-7...655_6..7.5.: neither (the same best X and leftover 13,349). Fillings best leftover 2,694, no FZERO.
