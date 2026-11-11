# Standalone Full-Stack `t = 0` Four Colour Theorem Discharging & Unavoidability Certificate (`fullstack_t0/`)

This directory contains a self-contained, exact-arithmetic, rotation-verified (`RotOcc`) full-stack discharging, unavoidability, and infinite-tail certificate for the Four Colour Theorem across **all vertex degrees $d \ge 5$** on internally 6-connected planar triangulations, together with `wheeldis_v2_audit/` recording the exact-arithmetic audit and refutation of `cert_k86ML1_p1.json` (`LOWER-R2: INVALID` under `K3gB5b + 16fik`, with float `receiverV2` `cert_ml1_v2.json` hitting $t \approx 0.0$ on a zero-curvature `{5,6,8}` periodic torus; see sibling `../outside-argon-7nov/check.py` for the $d = 5..8$-only `t = -33/2000` baseline check).

## 1. Quick Verification (Zero Dependencies, Python Stdlib Only)

```bash
nice -n 15 python3 -B -I /Users/kylemathewson/GraphColouringNov/fullstack_t0/verify_4ct_t0.py
```

`verify_4ct_t0.py` imports **only** Python standard-library modules (`collections`, `fractions`, `itertools`, `json`, `os`, `time`), shares zero runtime state with the C++ generator `fast_unavoidable.cpp`, and independently verifies:

1. **79-Part Local Integer Discharging Rules (`data/parts79.json`)**:
   - `71` RSST unit parts (`rsst_drules.v`, MD5 `5ee470f8eb12ec93c993c3496682475f`) + `8` `N2` unit parts (`N2_97, N2_98, N2_99, N2_88` and mirrors, replacing `128.1324802`), cross-checked byte-for-byte against Lean `lean_parts.txt` and `lean_parts_n2.txt`.
   - Hub degrees $n \in \{5, 6, 7, 8\}$, 2-ball locality (fan ranges only on exact spokes $6, 7, 8$; $9+$ middle private never read), **exact multiset mirror involution** ($\operatorname{Counter}(P_{79}) = \operatorname{Counter}(\operatorname{mirror}(P_{79}))$), independent vertex-by-vertex `in`/`out` rule conservation summing to `+120` + `Window2Ball` interval bracketing (`win_lo <= c_final(u) <= win_hi <= ub0`) on concrete genus-0 sphere triangulations (`make_icosahedron` and a 48-vertex mixed-degree `{5,6,7,8,9,12}` sphere with 240 rule firings), and Euler's formula contradiction on every sphere triangulation $|E| = 3|V| - 6$:
     $$\sum_{v \in V(T)} c_{\text{final}}(v) = \sum_{v \in V(T)} 10(6 - \deg(v)) = 60|V| - 20|E| = 120 > 0.$$
2. **Reducible Configuration Registry, CGlue Fold-Safety & Provenance (`data/verified_registry.json`)**:
   - `878` verified configurations (`379` `[L]` = `83` `L_full` + `296` `L_eval`, plus `499` `[E2]`; **`0` unproved `none` configurations**), of which **`854` distinct configurations** (`78` `L_full` + `296` `L_eval` + `480` `E2`) are used in the proof:
     - `RSST_582`: `582` (`74` `L_full` with 0-sorry `.lean` reducibility + occurrence/colorability glue on disk [`51` `ST-113` D + `21` `ST-122` D + `2` `ST-122` `HA5` C], `296` `L_eval` with Lean 4 `cReducible18` kernel evaluation + `[E2]` two-engine check + `admissibleX` & `foldSafeX` verified pending per-key `CEntryF` glue, and `212` `E2` from `ST-120R`).
     - `RSST_2o126_LEAN`: `1` (`2.126` = `rsst003_2o126`, `L_full`, Lean 4 `0-sorry` via `ST-123` `CGlueM.lean` + `ST-125`).
     - `SUB_NL51`: `268` used (`2` `L_full` from `L7` + `266` `E2` D-reducible configurations from `nl51_kc.txt`, including `15` exact Whitney 2-flip partners and `90` Whitney-masked D-substitutes verified directly in `data/e2_recheck_nl/*.out`).
     - `SUB_WINDOW`: `3` used (`fix_63c8a193fe` = `P20` `L_full`, `fw_3ff67ce5f7` `E2` rim-free single-interior-edge `X={I1-I5}` C-window, and `fw_0d0449a2fa` `E2` pure D-window; **`0` non-Lean rim-pinned `SUB_WINDOW` C-windows**).
   - Uniform CCW `(R_t, R_{t+1})` ring orientation (`(b - a) % r == 1`) across all `878` configs, independent cycle reconstruction from `kc_line`, bidirectional `slotTri` (`COccBridge.lean:52-54`), Lean's exact **`admissibleX` and `foldSafeX`** (`CGlue.lean:375-838`) verified on **all `346` `C` configs** (including all `62` rim-pinned `RSST_582` C-configs), and **`admissibleXM` + `foldSafeX` + `coherB` + `starB` + `chordB`** (`ROUTE_I_PLAN.md:93-162`) verified on `2.126`.
3. **Infinite Tail Proof for All $d \ge 15$ (`data/cert_karp_tail_d15.json`)**:
   - Independent recomputation of all $5^5 = 3,125$ values of $c^+(a,b,c,d,e)$ ($\max = 6$, `cmax = {5:6, 6:6, 7:6, 8:4, 9:0}`), exact `Fraction` check of Karp's zero potential $\phi \equiv 0$ ($\lambda^* = 6/1$) on the 625-state 4-gram de Bruijn graph, and exact proof that $c_{\text{final}}(u) \le 10(6-d) + 6d = 60 - 4d \le 0$ for **all** $d \ge 15$.
4. **Exhaustive Word Completeness & Strict `rotOK` (`RotOcc`) Certificate Replay ($d = 5 \dots 17$)**:
   - Explicit iteration over **all** $5^d$ link words at $d = 5, 6, 7, 8$ (`3,125 + 15,625 + 78,125 + 390,625 = 487,500` words) and independent branch-and-bound enumeration of all canonical $c^+$-positive link words at $d = 9 \dots 17$ (`39,235` canonical words total; `0` positive words at $d = 15, 16, 17$).
   - Direct $O(m \cdot \bar{g})$ deterministic verification of all `181,138` `[cfg_id, phi, sigma, shifts]` `RotOcc` witnesses (enforcing `ιinj`, `disj`, exact degrees, single global chirality $\sigma \in \{+1, -1\}$, cyclic slot matching, single-valued ring map $\rho$, distinct $9+$ middle placeholders $q_{i,L} \ne q_{i,R}$, and degree-5 $s_i$ outside-apex merges), plus replay of all `59,480,669` symbolic DFS nodes.
5. **7 Planted Negative Controls (`NC1..NC7`)**:
   - `NC1`: Dropping `2.126` on $d=6$ `565667` -> DFS replay rejects.
   - `NC2`: Dropping `N2` parts on $d=7$ `5657669` (without `128.1324802`) -> DFS replay rejects.
   - `NC3`: Dropping `0.7322` on $d=5$ `55555` -> DFS replay rejects.
   - `NC4`: Corrupting cyclic shifts AND testing the Whitney 2-isomorphism flip (`nl0194_r12` on $d=7$ `5567667`) directly via `verify_rot_witness` -> rejects both.
   - `NC5`: Dropping mirror parts AND duplicating a chiral part without its mirror -> multiset involution rejects both.
   - `NC6`: Perturbing `Window2Ball.succ` spoke orientation AND perturbing receiver anchor on the 48-vertex sphere $T_{\text{mix}}$ -> rejects both.
   - `NC7`: Corrupting `admissibleX` ring labels, D1 `foldSafeX` ring pins, and `2.126` `chordB` -> rejects all three.

## 2. Critical Upstream Bug Discovered & Repaired: Whitney 1-Cut & 2-Cut Containment Mismatches

Upstream scripts (`job_RSST1SHOT/code/rcore.py`, `job_ST119` `fwsub.py`, `job_ST120/b5/py/export_cert.py`, and `r2_scheck.py`) test configuration containment using **abstract induced-subgraph isomorphism** (`deg` + `int_adj`) **without** checking cyclic vertex rotations (`rotOK` / `RotOcc`).

Whenever a configuration's interior graph has a 1-vertex or 2-vertex cut (by Whitney's 2-Isomorphism Theorem), flipping one component across the cut yields a **non-planar-isomorphic configuration** ($\sigma = +1$ and $\sigma = -1$ both fail!) with the **identical** abstract interior graph and degrees:
- **Inside `RSST_582` itself (`ST-120 B5` certificate exporter bug)**: On $d=7$ link `5567757`, `export_cert.py` emits `184.3686406` (`phi = [0,1,2,3,6,5,8,9,12,28]`), which fails `RotOcc` across the 2-cut `{u, s_4}`, masking `54` positive leaves from `NEEDS_NONE.tsv.gz` whose true RSST planar killer was the `none` config `126.62942`.
- **Inside `SUB_NL51` (`ST-119` greedy cover bug)**: `15` `nl51` configurations (including `nl0078_r11` in `L7`!) require their Whitney 2-flip partners (`nl0079_r11`, `nl0196_r12`, etc.), plus `90` additional D-substitutes (`data/discovered_whitney_subs.txt`) for leaves masked by `RSST_582` Whitney flips.
- **Inside `SUB_WINDOW` (`fw_f7c75a21e2`)**: `u` (`I9`) is a 1-vertex articulation point of `fw_f7c75a21e2`, so reflected occurrences on `5657578` require `fw_3ff67ce5f7` (`X={I1-I5}`, rim-free).

## 3. Exact Theorem Scope & Reducibility Subtiers

- **Graph Class**: Internally 6-connected planar (spherical) triangulations (`ClaimGlue.Internally6`: triangulated, minimum degree $\ge 5$, every triangle facial `NoSep`, no separating 4-cycle or two-sided 5-cycle `NoShortSepCycle`). Reduction from general planar graphs to minimal counterexamples that are internally 6-connected planar triangulations holds by classical Kempe (1879) ($\le 4$-vertices and separating $\le 4$-cycles) and Birkhoff (1913) (separating 5-cycles).
- **Discharging + Unavoidability + Tail ($t = 0$)**: 100% verified in exact integer / `Fraction` arithmetic across **all** $d \ge 5$ (`verify.log`).
- **Reducibility Subtiers (`854` used configs)**:
  - `L_full` (`78` used / `83` in registry): Full `.lean` reducibility + occurrence/colorability glue (`0 sorry`) on disk (`51` `ST-113` D + `21` `ST-122` D + `2` `HA5` C + `1` `2.126` + `2` `L7` D + `1` `P20` C).
  - `L_eval` (`296` used / `296` in registry): Lean 4 `0-sorry` `cReducible18` kernel evaluation + `[E2]` two-engine (`kc -C` + `cfast --fixed`) + Lean's `admissibleX` & `foldSafeX` verified (`CEntryF` per-key occurrence glue pending).
  - `E2` (`480` used / `499` in registry): Independently verified reducible on two separate C/C++ Kempe-chain engines (`kc` and `dfast18`/`cfast`), with `admissibleX` & `foldSafeX` verified on every C-config (`6` in `RSST_582`, `1` rim-free in `SUB_WINDOW`).
