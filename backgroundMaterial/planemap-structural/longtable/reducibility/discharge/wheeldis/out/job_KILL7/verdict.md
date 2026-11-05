# job KILL7: Studio checks of the 7 new kill6 configurations (Opus swarm), 5 Nov

**Result:**
- **(a)** All 7 have Lean hD, and so does their occurrence glue.
- **(b)** All 7 are D on kc, dfast18 and cfast.
- **(c)** All 7 written KILL6 entries follow from their configuration's induced embedding, in both orientations, and give
  exactly Opus's 222 new U7 bits.
  - **Our own table builder finds 298 new U7 bits**: the 222 plus 76 more. 0 of Opus's bits are missing from ours.
  - U8 and U9 are unchanged. The V7 and V8 masks are unchanged.
- **(d) not run.** The in04 solution uses flags our spec-only checker has no spec for.

## Independence statement
- **Studio engines and code only:**
  - kc 07e79fae, dfast18 07cb1e0b, cfast de59e72f;
  - gen_hd.py f743a82d;
  - out/job31/st16_filter.py (the table builder used for keep95p131f) and out/job_P870/prov_tables.py (the same builder with
    name tracking).
- **Opus's Lean glue** (b5a04c50) was compiled as given: byte copies, none edited.
- **Not run:** Opus Python and Team B material.
- **Inputs:** read-only, from 5f26e799 ext_handoff_nov3/kill7/. All 5 md5s match MD5SUMS.

## (a) Lean hD and occurrence glue
- **EXTRAFILE:** D_kill7.tsv (d2b3ad70), MOD HDK7, PFX hdk7. It and the module split were pushed first, at 38a1440a.
- **hD:**
  - HDK7 and HDK7V00..06: all exit 0, sorry 0. CPU per entry is 43–49 s at ring 12 and 224–295 s at ring 13, at about 0.52 GB.
  - HDK7All (`hD_all : Fin 7`): exit 0.
  - Axioms: propext, Classical.choice and Quot.sound, plus native_decide aux.
- **Glue** (b5a04c50, s76_occ502/hdk7/lean):
  - HQ_00..06, COccHQ_00..06 and **HDK7Occ**: all exit 0, sorry 0.
  - HDK7Occ: 14 axiom prints, only propext, Classical.choice, Quot.sound and native_decide aux. sorryAx appears 0 times.
  - **All 15 .lean files are byte-identical to b5a04c50.**

## (b) D verdicts (eng/l0..6.out)
| config | ring | kc -C -s 60 -t 600 | dfast18 | cfast | classes = reached |
|---|---|---|---|---|---|
| b7_u...5566_...576._p516 | 12 | D | D | D | 22,144 |
| b7_u65...65_6....67_p015 | 12 | D | D | D | 22,144 |
| b7_u5656..._576...5_p116 | 12 | D | D | D | 22,144 |
| b7_u5656..._576...._p116 | 12 | D | D | D | 22,144 |
| b7_u...5566_...5765_p516 | 13 | D | D | D | 66,430 |
| b7_u56656.._..76..._p215 | 13 | D | D | D | 66,430 |
| b7_u65...65_6....67_p016 | 13 | D | D | D | 66,430 |

## (c) Tables (tab/kill/, prov_kill7.json, entry_check.txt)
**Rebuild:** keep95p131f's forbidden set (12,268) plus the 7, which gives 12,275. The tables were rebuilt with st16_filter.py and,
separately, with name tracking through prov_tables.py. The two agree.

**U7 kill6 bits:**
| table | bits |
|---|---|
| keep95p131f | 84,396 |
| ours with the 7 | **84,694 (+298)** |
| Opus's kill6r_U7 | 84,618 (+222) |

- Neither table loses a bit.
- **Theirs ⊆ ours.** 0 bits are theirs only; **76 are ours only**.
- Our kill6_U7 md5 is b493a0ce (file).

**Opus's written entries:**
- Each KILL6 entry, with '.' meaning any letter, expanded in its own orientation and in the mirror orientation, comes to 250
  cells.
- Every cell is killed in our table with **that configuration** as a justifier: 25/25 + 25/25, 5/5 + 5/5 and so on for each
  of the 7.
- Of the 250, **222 are new**, matching their count exactly.

**Which configs set the 298 new bits** (a bit can have several justifiers; the "sole" column counts bits with only that one):
| config | new bits | sole |
|---|---|---|
| b7_u...5566_...576._p516 | 50 | 40 |
| b7_u65...65_6....67_p015 | 32 | 32 |
| b7_u5656..._576...5_p116 | 10 | 0 |
| b7_u5656..._576...._p116 | 98 | 78 |
| b7_u...5566_...5765_p516 | 10 | 0 |
| b7_u56656.._..76..._p215 | 40 | 30 |
| b7_u65...65_6....67_p016 | 88 | 88 |

**Our 76 extra bits** come from two configurations, 38 each: b7_u5656..._576...._p116 and b7_u65...65_6....67_p016. These are
further induced embeddings of those configurations into the U7 window frame, beyond the single entry each one states. Our builder
records every embedding that uses the private slot; this is the same rule used for every keep95p131f cell.

**U8 / U9:** byte-identical to keep95p131f (618eb300). Opus's kill6r_U8 also equals keep95p131f.

**V7 / V8 masks:** unchanged (400 / 100 letter kills, the same sets).

## (d) not run: flags without a spec in our checker
- **What in04 carries:** sol_q75B_in04_full.json (52722e4e, md5 df806931, t 0.038830783) has the keys
  - **zh** (with z: 39 entries),
  - **zr / zrflag** (zr: 80),
  - **hatrr / rr** (rr: 11),
  - **q7, q7m**,

  plus the zcap / q7rc / q7cap parameters the relay mentions.
- **What our checker does with them:** out/job31/st21_check_f2b.py implements hat5 only. It **explicitly fails on zh** (line
  354: "solution mode differs … zh"). It has no code and no spec for zr, hatrr / rr, q7, q7m, zcap, q7rc or q7cap.
- **So (d) stops here.** I did not improvise an implementation. To run it I need the RELAY_SPEC sections defining those
  families.
