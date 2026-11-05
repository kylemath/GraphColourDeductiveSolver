# HDC502 inputs to gen_hd.py (for the occurrence glue)

- **EXTRAFILE:** `out/job_HDC502/D_todo.tsv` (md5 219b58ad1a2eaf3129e40cabea153798). 370 lines of `name<TAB>r m ringadj intadj`,
  exactly as fed, in ring order (8 → 15). There is one batch only.
- **Generator:** out/job_HD0/gen_hd.py, **md5 f743a82d2b5ca15a42adbc8d68d0ee99**. This is c1c30c9a plus
  `set_option maxRecDepth 100000` in the data module, which a 370-entry list literal needs; gen_ccover3 has the same line. The Conf
  literals are unchanged.
- **Call:** `python3 out/job_HD0/gen_hd.py out/job_HDC502/D_todo.tsv out/job_HDC502/lean HDC hdc 1`, so **MOD = HDC, PFX = hdc**,
  batch 1.
- **Modules:**
  - `HDC.lean` defines `HDC.hdcConfs` and its length.
  - `HDCVnn.lean` holds entry nn: `HDCV.hD_nn : DCheck18.dReducible (hdcConfs.get ⟨nn, _⟩) = true`. The module number is
    `%02d` of the index, so HDCV00 … HDCV369.
  - `HDCAll.lean` proves `HDCV.hD_all (k : Fin 370)`.
- **Module split:** `out/job_HDC502/module_split.tsv` gives index → module → theorem → name → ring.
- **Namespace note:** HD0's control module HDCtrl also uses PFX hdc, but in namespace HDCtrl (`HDCtrl.hdcConfs`), so it does not
  clash with `HDC.hdcConfs`.
