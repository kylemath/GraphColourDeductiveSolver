# job HD0: Lean hD calibration (Studio, 5 Nov)

## Template
- **Generator:** out/job_HD0/gen_hd.py, **md5 c1c30c9a9b073767164d2d50eebcd204**. This is the committed 0604923f version (b08d0f9d)
  plus one fix.
  - **The fix:** the hD_all assembly module imports `Mathlib.Tactic.FinCases` and `Mathlib.Data.Fintype.Fin`.
  - **Why it was needed:** DCheck18 does not import Mathlib. Without these, `fin_cases` is an unknown tactic and Fintype (Fin n)
    cannot be found.
  - **Scope:** the data and per-entry modules are unchanged; regenerating them gives byte-identical output. The README input
    format is unchanged. **Anyone building on b08d0f9d needs this two-line fix in the All module.**
- **What it emits:**
  - `<PFX>Confs : List DCheck18.Conf` and its length;
  - per entry, `hD_i : DCheck18.dReducible (Confs.get ⟨i,_⟩) = true := by native_decide`. This is ClaimGlue.DEntry.hD;
  - `hD_all (k : Fin n)` by fin_cases.

## Build and measurement
- **Build:** ~/studio_lean_builds/rsst118_fb35d2d1, the dcheck chain at fb35d2d1. Lean v4.35.0-rc3, the mathlib oleans read-only,
  no lake, nice 15. Mostly 4 modules ran in parallel, alongside the other Lean jobs and k19.
- **Measurement:** one entry per module. Times are from /usr/bin/time -l (wall, user, sys, maximum RSS), per module, in
  lean/status.txt.

## Control: 3 RSST D2 entries at ring 10, all with agreesRSST
- The entries are rsst008_3o460806, rsst009_3o1306806 and rsst012_2o22086.
- **hD_0..2: exit 0, sorry 0, about 3.5 s CPU each, 512 MB.**
- HDCtrlAll: exit 0.

## Calibration: 30 two-engine D entries from nl51 (10 per ring, seed 13; all in the keep95p131f table D side)
- **All 30 hD: exit 0, sorry 0.**
- **HD30All (hD_all, Fin 30): exit 0.**
- **Axioms** (`#print axioms HD30V.hD_all`): propext, Classical.choice, Quot.sound, hd30Confs_length._native.native_decide.ax_1_1
  and the 30 HD30V.hD_i._native.native_decide.ax_1_1. There is no sorryAx.

**Per ring** (CPU = user + sys; wall time is within 1% of it):
| ring | n | median CPU s | max CPU s | median CPU h | max CPU h | max RSS MB |
|---|---|---|---|---|---|---|
| 13 | 10 | 223 | 295 | 0.062 | 0.08 | 519 |
| 14 | 10 | 1151 | 1519 | 0.320 | 0.42 | 533 |
| 15 | 10 | 6412 | 7138 | 1.781 | 1.98 | 567 |

**Reading:**
- CPU per hD is about **4 min at ring 13**, **19 min at ring 14** and **1.8 h at ring 15**: roughly ×5–6 per ring step.
- Memory is **about 0.55 GB per entry**, flat across rings.
- **Extrapolating** the ×5.5 ratio, not measured: about 10 h at ring 16, about 2–3 days at ring 17 and about 2 weeks at ring 18
  per entry.
  - The compiled checker (wheelcheck, a native executable) was faster at rings 16–18: k02 ring 18 took about 32 h.
  - So for rings ≥ 16, the compiled checker route, or per-entry splitting, may be cheaper than in-kernel native_decide.

## Per-entry table
| # | name | ring | m | exit | wall s | CPU s (user+sys) | peak RSS MB |
|---|---|---|---|---|---|---|---|
| 0 | nl2019_r13 | 13 | 11 | 0 | 228 | 228 | 519 |
| 1 | nl2180_r13 | 13 | 12 | 0 | 193 | 192 | 519 |
| 2 | nl5592_r13 | 13 | 10 | 0 | 236 | 236 | 519 |
| 3 | nl7576_r13 | 13 | 9 | 0 | 296 | 295 | 519 |
| 4 | nl5589_r13 | 13 | 10 | 0 | 218 | 218 | 519 |
| 5 | nl6424_r13 | 13 | 11 | 0 | 185 | 184 | 519 |
| 6 | nl7285_r13 | 13 | 10 | 0 | 210 | 210 | 519 |
| 7 | nl7417_r13 | 13 | 11 | 0 | 167 | 167 | 519 |
| 8 | nl1745_r13 | 13 | 9 | 0 | 250 | 249 | 519 |
| 9 | nl5506_r13 | 13 | 10 | 0 | 234 | 234 | 519 |
| 10 | nl3496_r14 | 14 | 10 | 0 | 1521 | 1519 | 525 |
| 11 | nl8088_r14 | 14 | 12 | 0 | 895 | 894 | 526 |
| 12 | nl2362_r14 | 14 | 10 | 0 | 1451 | 1449 | 532 |
| 13 | nl3474_r14 | 14 | 10 | 0 | 1260 | 1258 | 531 |
| 14 | nl7805_r14 | 14 | 11 | 0 | 1155 | 1154 | 526 |
| 15 | nl2992_r14 | 14 | 11 | 0 | 909 | 908 | 532 |
| 16 | nl2215_r14 | 14 | 11 | 0 | 1174 | 1173 | 532 |
| 17 | nl1094_r14 | 14 | 11 | 0 | 1053 | 1052 | 526 |
| 18 | nl6629_r14 | 14 | 12 | 0 | 849 | 848 | 533 |
| 19 | nl3384_r14 | 14 | 11 | 0 | 1150 | 1148 | 526 |
| 20 | nl7221_r15 | 15 | 13 | 0 | 4834 | 4830 | 556 |
| 21 | nl3832_r15 | 15 | 12 | 0 | 4731 | 4727 | 556 |
| 22 | nl1121_r15 | 15 | 11 | 0 | 6448 | 6443 | 556 |
| 23 | nl4615_r15 | 15 | 12 | 0 | 5976 | 5972 | 557 |
| 24 | nl1502_r15 | 15 | 12 | 0 | 6909 | 6906 | 566 |
| 25 | nl6881_r15 | 15 | 15 | 0 | 3704 | 3701 | 567 |
| 26 | nl6613_r15 | 15 | 11 | 0 | 6382 | 6381 | 555 |
| 27 | nl0776_r15 | 15 | 11 | 0 | 6699 | 6698 | 556 |
| 28 | nl3781_r15 | 15 | 11 | 0 | 7138 | 7138 | 555 |
| 29 | nl2247_r15 | 15 | 11 | 0 | 6943 | 6942 | 566 |
