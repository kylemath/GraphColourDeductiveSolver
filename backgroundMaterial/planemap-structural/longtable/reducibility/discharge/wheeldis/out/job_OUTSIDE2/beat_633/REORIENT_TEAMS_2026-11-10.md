# Team Reorientation Note — 10 Nov 2026 (22:36 CST)

## TL;DR — Two Major Milestones Just Crossed in `GraphColouringNov/`

1. **Full-Stack $t = 0$ `C2cons`-Only Proof Closed & Adversarial-Audited (`854` configs, `0` ring merges)**:
   - Locked in `/Users/kylemathewson/GraphColouringNov/fullstack_t0/` (`python3 -B -I verify_4ct_t0.py`, exit `0`).
   - Closes $c_{\text{final}}(u) \le 0$ across **all vertex degrees $d \ge 5$** (`d = 5..17` by exact 2-ball symbolic DFS + strict global-chirality `RotOcc` witnesses; $d \ge 15$ by exact rational $c^+$ tail bound) using **zero ring-merging C-configurations** (`581` RSST `D2`/`C2cons` + `273` `D`/`C2cons` drop-in replacements for the remaining 52 RSST configs, all verified on two independent engines `kc` + `dfast18`/`cfast` and `admissibleX` + `foldSafeX`).

2. **RSST's 633-Configuration Record Broken — Already Down to `598` Configurations (Pass 2 Running)**:
   - Active in `/Users/kylemathewson/GraphColouringNov/beat_633/` (`bin/fast_synthesize` + `solve_hitting_set.py` + `verify_compact_4ct.py`).
   - First proved via exact Benders MILP (`6,574` leaf cuts over a `4,095`-config candidate pool) that under RSST's unmodified 71 rule parts, **`633` is the exact global minimum cardinality** (`0` free drops, `0` $k$-for-$1$ swaps).
   - Unlocked sub-`633` compression by lifting the local 2-ball discharging cochain to **half-quantum signed integer weights (`scale_M = 20`)**:
     - **Half-quantum outgoing splits ($w > 0$, hubs $5 \le d \le 8$)**: splits residual `+0.10` (`+2`) leaf charge into `+1` + `+1` (`+0.05` each) across distinct `6..9+` spokes.
     - **`!open` incoming anti-rules ($w < 0$, hubs $d \ge 7$ including $d = 9..12$)**: local retention rules centered on `5..8` spokes that constrain only vertices inside hub $u$'s 2-ball (`!open`), subtracting $|w|$ from $u$'s `Window2Ball` upper bound while adding $+|w|$ to the sender's outgoing `plus_terms`.
     - **Exact 625-state 4-gram de Bruijn Karp coboundary potential $\phi^*$**: certifies the infinite degree tail ($d \ge d_0 = 15$, $\lambda^* = 12/1 < 20$) in exact `Fraction` arithmetic even when surgical rules touch isolated `9+` 5-grams.
   - **Live status**: Pass 1 just finished at **`598` configurations** (`-35` below RSST's `633`, including `15` ring-14 configs and `C_merge` `8.1540806`); Pass 2+ -> Benders MILP -> standalone `python3 -B -I verify_compact_4ct.py` -> fresh adversarial audit are running next.

---

## Reorientation by Track / Team

### 1. Lean Track 8 Team (RSST Seed Route `B1..B6` & Studio Queue)
- **Do NOT pause `certificate replay` or `containment` (`RotOcc`)**: Those two Lean bridges remain the critical-path bottleneck to turn computational $t = 0$ into a 100% kernel-checked Lean theorem, and **both** `fullstack_t0` (`854` `C2cons`) and `beat_633` (`<= 598` configs) plug directly into the exact same `Window2Ball` + `RotOcc` + `CGlue`/`CGlueM` architecture!
- **Studio Reducibility Queue (`212` configs) Triage**:
  - Deprioritize queuing any RSST configurations already eliminated in `beat_633/data/synth_active.txt` (35 already dropped in Pass 1, including heavy `r = 14` configs: `283.22803`, `219.61682`, `11762.8942`, `483.3927606`, `165.22802`, `1326.1028`, `7696.428`, `496.12422`, `126.78485226`, `1326.12422`, `7322.62406`, `7331.442817`, `186.1326120`, `7457.1307280`, `7457.1310580`, `7322.3711780`, `186.505320`, `126.1325768`, `122.62420`).
  - Conversely, if you want a **zero-`CGlueM` Lean proof first** (avoiding general ring-merging `NoClassChord` for the `9/51` non-`starB/chordB` `C_merge` configs), `fullstack_t0/data/registry_854.json` already gives a complete, verified `D`/`C2cons`-only unavoidable set (`0` ring merges).
- **Two minor schema extensions if porting `beat_633` into Lean after `633` closes**:
  1. Allow signed integer `Part.weight : Int` at `scale_M = 20` (with `!open` guard enforced on `minus_terms`).
  2. Replace the naive scalar $\max c^+$ tail bound with the 625-entry integer 4-gram potential vector `phi_625` (`Q * CP(a,b,c,d,e) + phi(b,c,d,e) - phi(a,b,c,d) <= P`), which is a trivial finite `decide` check over $5^5 = 3,125$ tuples.

### 2. Own-Rule LP Ladder Team (`ST-124`, `t = 0.0135154`)
- **Stop spending compute trying to push the coarse $d \le 8$ LP down to $t = 0$ from scratch**:
  - `t = 0` is **already closed** across all $d \ge 5$ on both `fullstack_t0` (`854` `C2cons`) and `beat_633` (`<= 598` configs and dropping).
  - Our exact Benders MILP + forced-leaf profiling revealed *why* coarse key families stall above `0`: positive leaves at $d = 7..11$ require **2-ball hat/fan hull specificity + signed `!open` anti-rules + 4-gram Karp potential**, not coarser 1-ball LP keys.
- **Where LP / MIP helps now**: Once `beat_633` Pass 2+ finishes, focus any remaining compression compute on **joint super-killer + rule synthesis** for configurations with `> 600` forced leaves (finding single `r <= 13` `D`/`C2cons` configurations that cover 90%+ of two RSST configs' leaves so 1–2 surgical 2-ball rules finish the merge).

### 3. Outside Argon Package Team
- **Status of Outside Argon Handoff (`HANDOFF-OUTSIDE-ARGON-2026-11-10.md`)**:
  - Fully audited and absorbed into `fullstack_t0/`. Specifically:
    - Fixed the two handoff blockers: elevated all `7` unverified `[E2-cand]` configs (`S4317`, `S4356`, `S5739`, `S7345`, `S4048`, `S6644`, `S7044`) to full two-engine `[E2]`, and closed all `21` previously open degree-$7+$ residual configurations (`N1` + `20` RSST configs across $d = 9..11$) using `115` two-engine-verified `D`/`C2cons` configurations (`0` unproved configs).
  - **Action**: Do **not** continue expanding partial $d = 5, 6$ replacements on the 16-rule subset; treat `fullstack_t0/` (`854` `C2cons`) and `beat_633/` (`< 600` general `D`/`C`) as the canonical full-world baselines going forward.
