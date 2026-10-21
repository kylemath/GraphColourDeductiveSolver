# s47 A84 [E2] upper (sol_q47A84.json at 86f93859, md5 f86bfe03; claim FEASIBLE at t = 0.104204341825): Studio spec-only check

**Verdict: pending.** Runs (a) fb on + V = 8, and (b) fb off + V = 8 kept, are in progress. The registry and table checks below are done.

## Registry A84 (main 517b0129, 128 rm128 held out): Studio's own build vs Opus's reg_A84 / tabV8_A84 (62bae93a, data)
- **k3x:** D 2,707 (md5 efdd2d6c) and C 1,218 (808b8aff). These are byte-identical to reg_A84 k3x_D_A84 / k3x_C_A84.
- **Forbidden set:** 582 RSST + 3,925 twoeng = 4,507. dcount: D 17,747, which equals reg_A84 dcount.txt TOTAL newpat 17,747 (C 2,136,
  RPAT 158).
- **Kill tables:** kill6 U7 27a64538, U8 = U9 6dc44bba. These equal reg_A84 md5_prep. Check 4 gives 3,072 / 7,500 survivors.
- **l3q V = 7 masks:** 190 of 30 per side. They equal reg_A84 tab_±1 entry by entry (2,500 per side, 0 mismatches).
- **l3q V = 8 masks:** 50 of 30 per side. They equal Opus's s47/tabV8_A84/tabV8_{1,-1}.json (md5 b0115b14 / 38c23474) entry by entry
  (2,500 per side, 0 mismatches).
- **Ring-merge sweep at 517b0129:** 129 FAIL, the same set as the 129-FAIL set (a2ec92e5). That set minus f9_....5565B_....6655. is
  exactly exname_rm128.

## Other registries (Opus's s33z/reg_A85..A87 at 62bae93a, data) vs Studio's builds
| reg | main | k3x D / C (Opus = Studio) | dcount newpat (Opus) | kill6 (Opus = Studio) | l3q tab_±1 |
|---|---|---|---|---|---|
| A85 | bd503acc | cf3a0094 / 7575c7ca (= main's out/job30 k3x; no Studio table build) | 17,751 | 27a64538 / 6dc44bba | not built |
| A86 | ea8944db | c1b1b4e1 / 6c27df6f, identical | 17,755 | identical | 0 mismatches |
| A87 | b253a4ad | d3901238 / 9001e009, identical | 17,771 | identical | 0 mismatches |
