# HA5b inputs (Studio, 7 Nov): the 54 witnesses new in W18 A-5 FINAL (ST-18, 92c8a166)
- hD: D_a5b.tsv (45), gen_hd f743a82d, MOD **HDA5B**, PFX **hda5b**: HDA5B, HDA5BV00..44 (`HDA5BV.hD_i`), HDA5BAll; hd/module_split.tsv
- hC: extraC.tsv (9, same literals and X as their CA5F entries) -> hc/CA5B.lean (gen_ccover3, a5bEntries; XRData.ok / admissibleX / foldSafeX proved, exit 0); A5BV00..08 (`A5BV.hC_i`), A5BVAll (`A5BV.hC_all (k : Fin 9)`, W3PVAll form); hc/module_split.tsv
- Build queued after HA5 (drive.sh).
