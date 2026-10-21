# A97 (main 8ec00aea, adm62k) tables pre-built for s53 (Studio, 21 Oct)
- **k3x at 8ec00aea:** D 3,057 lines (md5 d76bc52f), C 1,310 (9f8cfe39). **Forbidden set:** 582 RSST + 4,367 twoeng = 4,949.
- **Kill tables:** kill6 U7 27a64538, U8 = U9 6dc44bba (unchanged since A78). Check 4: 3,072 / 7,500 survivors.
- **l3q masks:** V = 7: 190 of 30 per side, md5 22e1f5ef. V = 8: 50 of 30 per side, md5 2e8e8f5e. Both unchanged.
- **dcount (patterns distinct):** D 18,097, C 2,228, RPAT 158 (dryrun_counts.log).
- **Ring-merge sweep at A97 (ringmerge_sweep_A97.out):** 129 FAIL, the same set as the 129-FAIL set (a2ec92e5). FAIL minus
  f9_....5565B_....6655. = exname_rm128 (the held 128).
- **args:** argsA97_local_rpat_held128.txt = the A83 args with the two k3x files swapped. Opus's reg_A97 / tabV8_A97 are not yet
  committed on claude/project-thread-7uelj0 (only s47/tabV8_A97.sh), so there is no data diff yet.
