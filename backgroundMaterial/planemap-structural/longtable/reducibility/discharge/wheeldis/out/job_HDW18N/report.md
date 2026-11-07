# job HDW18N: Lean hD + occurrence glue for the 15 nl51 witnesses of W18's 428 (Studio, 7 Nov)
- **Input:** D_w18n.tsv (4df706df): the 15 nl51 witnesses of keep95p131f/w18_428/witness_noLean.txt (34 of the 428 rules rest on them); rings 10 (1), 12 (4), 13 (5), 14 (5).
- **Engines (re-confirmation, eng/):** kc -C -s 60 -t 600 (07e79fae) 15 / 15 D; dfast18 (07cb1e0b) 15 / 15 D.
- **Lean hD:** gen_hd f743a82d, MOD HDW18N, PFX hdw18n, batch 1 (module_split.tsv pushed first, 2c3559f1): HDW18N, HDW18NV00..14, HDW18NAll —
  **all exit 0, sorry 0**; total hD CPU 8,303 s.
- **Glue** (Opus --hd, 5e4e9a04 s76_occ502/hdw18n/lean, 31 files; HDW18NOcc d39cdcea): byte-identical in in/glue and lean/ (cmp clean);
  check_literals (D variant) on HDW18N.lean: **15 entries, 0 mismatches**; HWN_00..14, COccHWN_00..14, HDW18NOcc: **all exit 0, sorry 0**.
- **Axioms:** HDW18NAll and HDW18NOcc (30 prints): propext, Classical.choice, Quot.sound + native_decide aux only; sorryAx in 0 logs. 48 / 48 modules exit 0.
- With HDW18N, every witness of the 428 W18 rules is Lean-backed (C: hC lists; RSST: agreesRSST; nl51: hD).
