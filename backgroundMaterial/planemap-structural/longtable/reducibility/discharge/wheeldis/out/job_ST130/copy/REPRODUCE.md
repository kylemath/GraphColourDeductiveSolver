# Reproducing the sub-633 unavoidable-set result (beat_633)

Status as of 2026-11-11 00:25 CST. **Read the "What is and is not established" section before quoting any number.**

## 0. What is and is not established

| Claim | Status |
|---|---|
| `fullstack_t0/`: 854-config t = 0 proof, standalone verifier exit 0, adversarial audit PASS | Done (locked, `fullstack_t0/MD5SUMS`) |
| 588 RSST configs + 604 discharging parts (scale M = 60) give **0 positive-charge windows at all degrees 5..17**, plus a Karp tail bound for d >= 15 | Checked by **two engines**: the current `bin/fast_compress` (dynamic classes) and the **unmodified** pre-edit engine from `origin/main` (static classes). Both report `violated=0`. |
| Negative control: the same 588 set with the older 534-part rules (`synth_rules_598.txt`) | Fails as it should (`violated=96`) |
| 587 (free deletion of `504123.136`) | Found by the synthesizer in a run that is still going (task started 00:20). **Not yet independently re-checked.** |
| Replayable certificates, standalone `verify_compact_4ct.py` run, NC1..NC8, fresh-context audit **for 588** | **NOT DONE YET.** Until these pass, "588" is an engine result, not a verified proof. |
| Reducibility of every config used | Inherited from RSST's 633 (two-engine `kc` + `dfast18`/`cfast` logs from the fullstack_t0 work; the 51 C_merge configs are in `data/e2_rsst_cmerge/`). The 588 set is a **subset** of RSST's 633, so no new reducibility claims are needed. |

All of this is a computer-assisted discharging + reducibility argument, the same type of proof as RSST, and none of it is in Lean. The rules are our own surgical additions on top of RSST's 71 parts. The soundness of the 2-ball window bound (`Window2Ball`, `!open` anti-rules, bridge-zero 2-hop pairs) is checked only by sphere-conservation tests and negative controls. Nobody has re-proved it formally.

## 1. Constraints for any agent on this machine

- Treat `fullstack_t0/` as read-only. Check it with `cd fullstack_t0 && md5 -r $(awk '{print $2}' MD5SUMS) | diff - MD5SUMS` (or the equivalent).
- `/Users/kylemathewson/GraphColourDeductiveSolver/`, `maclane/` and `studio_lean_builds/` are read-only. Don't push.
- Prefix every compute command with `nice -n 15` and use 3 threads or fewer. Studio Lean builds run at `nice -n 20`.
- Write to a **copy** (for example `cp -R beat_633 /tmp/beat_633_repro`), not to the live `beat_633/`. The synthesizer overwrites `data/synth_active.txt`, `data/synth_rules.txt` and `data/word_embs_cache_v1.bin` in place.

## 2. Inputs (in `beat_633/data/`)

| File | md5 | Meaning |
|---|---|---|
| `pool_input.txt` | `a925b4c7c47ee899c5c9a130c3d71cd6` | 71 RSST parts (M = 10) + 4,095 configs (ids 0..632 = RSST, 633+ = external). Built by `build_pool.py` from the Studio worktree `WT=/Users/kylemathewson/GraphColourDeductiveSolver/.claude/worktrees/inspiring-lamport-831744` |
| `synth_rules_588.txt` | `50b1cf1b3c8ba27974dca9d2144879f5` | 604 parts, `SCALE 60` (71 RSST parts rescaled + surgical mirror-closed parts) |
| `synth_active_588.txt` | `6cf7baf94fb0ec554a02242db8f53efa` | 588 pool ids (all < 633) |
| `synth_rules_598.txt`, `synth_active_598.txt` | — | Earlier checkpoint (534 parts, SCALE 20, 598 configs) |
| `word_embs_cache_v1.bin` | `eaed4e68...` (changes when new words are added) | RotOcc embedding cache. Speed only; rebuilt automatically if deleted |

Rules file format: `SCALE M`, `PARTS n`, then one line per part: `tag hub_degree weight` followed, for each of the `hub_degree` slots, by `sp_lo sp_hi hat_lo hat_hi nfans [fan_lo fan_hi]*`. Degree 9 means ">= 9".

## 3. Build

```bash
cd /Users/kylemathewson/GraphColouringNov/beat_633
nice -n 15 clang++ -O3 -std=c++17 -pthread -o bin/fast_compress   fast_compress.cpp
nice -n 15 clang++ -O3 -std=c++17 -pthread -o bin/fast_synthesize fast_synthesize.cpp
```

Source md5 at the time of writing: `fast_compress.cpp ddf22d72...`, `fast_synthesize.cpp adfd8294...`, `verify_compact_4ct.py 85f236ea...`.

Independent second engine (pre-edit static-class version, extracted read-only from git):

```bash
P=backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/out/job_OUTSIDE2/beat_633
git -C /Users/kylemathewson/GraphColourDeductiveSolver show origin/main:$P/fast_compress.cpp > /tmp/fast_compress_old.cpp
nice -n 15 clang++ -O3 -std=c++17 -pthread -w -o /tmp/fast_compress_old /tmp/fast_compress_old.cpp
```

## 4. Reproduce the 588 check (about 30 s new engine, about 3 min old engine)

```bash
cd /Users/kylemathewson/GraphColouringNov/beat_633
nice -n 15 ./bin/fast_compress --mode sep --rules data/synth_rules_588.txt \
   --active data/synth_active_588.txt --out /tmp/sep_588.jsonl --threads 3
nice -n 15 /tmp/fast_compress_old --mode sep --rules data/synth_rules_588.txt \
   --active data/synth_active_588.txt --out /tmp/sep_588_old.jsonl --threads 3
```

Expected for both: header `[KARP] scale_M=60 parts=604 active_cfgs=588 max_cp=36 lambda*=36/1 tail_d0=15`, then `violated=0` on every line d = 5..17, ending with `[DONE] mode=sep violated=0 thin=0`. Exit code 0 (non-zero means violations).

Word counts per degree (both engines): d5 377, d6 1505, d7 5895, d8 25395 (all canonical words); d9 3110, d10 2098, d11 990, d12 267, d13 30, d14 2, d15+ 0 (only words whose Karp c+ bound is still positive).

**Negative control. This must FAIL:**

```bash
nice -n 15 ./bin/fast_compress --mode sep --rules data/synth_rules_598.txt \
   --active data/synth_active_588.txt --out /tmp/sep_nc.jsonl --threads 3
# expected: [DONE] mode=sep violated=96 ..., exit 1
```

Meaning of a pass: for every vertex degree d >= 5 and every 2-ball neighbourhood type, either the signed upper bound on final charge is <= 0, or one of the 588 configurations is forced to appear (RotOcc embedding with chirality respected). For d >= 15 the bound comes from the exact Karp potential: M(6 - d) + λ* d <= 0 with λ* = 36 < M = 60.

## 5. Continue the search (synthesizer)

```bash
nice -n 15 ./bin/fast_synthesize --in-rules data/synth_rules_588.txt \
   --in-active data/synth_active_588.txt --scale-mult 1 --max-leaves 3500 --passes 4 --threads 3
```

- Use `--scale-mult 1` because the 588 rules are already at SCALE 60.
- Output goes to `data/synth_active.txt` and `data/synth_rules.txt`, checkpointed every 10 deletions and at the end of each pass.
- The scan phase is a heuristic single-pass profiler that only orders candidates. Every deletion is accepted only after the exact `check_word_dfs` re-check on all affected words plus the receiver-safety and Karp-tail checks.
- **Always re-run step 4 on any new checkpoint with both engines.** Don't trust the synthesizer's own log.

## 6. Turning a checkpoint into a verified proof (not yet done for 588)

1. `nice -n 15 python3 -B -u export_final.py`: Benders hitting-set over the full 4,095 pool (may swap in external configs; each one gets two-engine `kc`+`dfast18` or `kc -C2`+`cfast` runs into `data/e2_super/`). It writes `data/final_rules.json`, `data/final_registry.json`, `data/cert_karp_tail.json` and `data/certs/cert_d*.jsonl`. Note that it reads `data/synth_rules.txt` and `data/synth_active.txt`, so copy the checkpoint you want into those names first.
2. `nice -n 15 python3 -B -I -u verify_compact_4ct.py > verify.log 2>&1`. This is a zero-dependency stdlib verifier. It recomputes all 3,125 c+ entries, the Karp potential, word completeness (all 5^d raw words for d <= 8), RotOcc witnesses, symbolic DFS replay with ub/kill leaf counts matched against the certificate, and the planted negative controls NC1..NC8. It needs exit 0.
3. Fresh-context adversarial audit (a different agent tries to break it) before anything is reported as a result.

Recent change to watch: `replay_signed_dfs` in `verify_compact_4ct.py` and `--mode cert` in `fast_compress.cpp` now both compute variable classes **dynamically from currently-alive terms**, replacing the old static per-word classes, and they must stay in lockstep for the leaf counts to match. This is sound because an unconstrained variable behaves identically on every value, but it is new and not yet exercised end-to-end.

## 7. Where things came from

- RSST 633 configs and 71 rules: Studio worktree above (`WD=$WT/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis`). Engines are at `$WD/loop/kc/kc`, `$WD/out/job52/dfast18` and `$WD/out/job52/cfast`.
- Earlier exact Benders result: with RSST's **unmodified** 71 rules, 633 is the minimum over this pool. Every reduction below 633 comes from the added surgical rules, not from dropping configs under RSST's rules.
- History and rationale: `REORIENT_TEAMS_2026-11-10.md` and the conversation walkthrough.
