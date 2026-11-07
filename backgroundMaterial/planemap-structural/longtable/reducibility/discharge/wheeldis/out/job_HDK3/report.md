# job HDK3: Lean hD + occurrence glue for the 6 K-3 D kills (Studio, 7 Nov)
- **Input:** D_k3.tsv: b8_u.56.5656_56...55., b9_u...575655_...5..65. (K3CHK); b8_u.56656.._..566..., b8_u.56.5556_56....5., b8_u.56.5756_.5..555. (K3CHK2); b9_u75..65656_5...55... (K3CHK3). All D on kc -C + dfast18 (those reports).
- **Lean hD:** gen_hd f743a82d, MOD HDK3, PFX hdk3 (HDK3.lean byte-identical to Opus's own run): HDK3, HDK3V00..05, HDK3All — all exit 0, sorry 0.
- **Glue** (Opus 01739289, HK3D_ / HDK3Occ 2c6fae49): byte-identical (cmp clean); check_literals 6 / 0; HK3D_00..05, COccHK3D_00..05, HDK3Occ all exit 0, sorry 0.
- **Axioms:** propext, Classical.choice, Quot.sound + native_decide aux only; sorryAx in 0 logs.
- The two K-3 C kills: K3CHK2 (K3C2V.hC_0 / hC_all, HK3C2Occ) and K3CHK3 (K3C3V.hC_0 / hC_all, HK3C3Occ), all exit 0, sorry 0. So all 8 K-3 kills are Lean-backed with occurrence glue.
