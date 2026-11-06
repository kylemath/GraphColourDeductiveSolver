# f2b7 rejust audit: portable package

This package re-derives (re-justifies) the private-letter rules of the four-colour discharging rule file
`rules_studio_keep95p131f.json` (md5 `45a4c6d1275f4bb2adb9826e4d8c953c`). The test is the strict single-slot test
from the f2b7 review. The package holds the review's audit script `rejust.py`, everything that script reads, and a
wrapper (`audit_any.py`) that runs the same per-rule test on every group of the rule file.

The calculation is unchanged. In the copied scripts, only the hard-coded absolute path constants were rewritten.
`MANIFEST.tsv` lists every packaged file with its original path, its md5, and the md5 of the original file.

## Requirements

- Python 3.9 or later, standard library only. No numpy, highspy or other packages are imported.
- All packaged scripts parse under the Python 3.9 grammar (checked with `ast.parse(..., feature_version=(3, 9))`).
- The smoke test below ran with Python 3.13 on Linux. A `d9_w6` slice under Python 3.11 gave identical output.
  No 3.9 interpreter was available to run it here.
- Run with `python3 -I -B`. `-B` stops Python writing `__pycache__` into `tree/`. Without `-B` the results are the
  same, but the package's file set changes.

## Layout and path rewrite

```
scripts/            rejust.py audit_any.py variants.py ext.py hyp.py frame.py witness.py variants2.py
tree/P_own_lp/      what the scripts call P   (was /home/claude/GraphColourDeductiveSolver/.../loop/opus/P_own_lp)
tree/ex_A97/        what the scripts call EX = SC + '/ex_A97'   (SC was the session scratchpad)
ref/                outputs of the original review run (for calibration) and the sides-mode inputs
```

`rejust.py`, `variants.py` and `frame.py` each got the same lines at the top:

```python
ROOT = os.environ.get('F2B7_AUDIT_ROOT') or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # package root
SC = ROOT + '/tree'
P = ROOT + '/tree/P_own_lp'            # frame.py instead: DIS = ROOT + '/tree/ex_A97/.../discharge'
```

`variants.py` and `frame.py` also had `os` added to their import line.

Nothing else changed. In particular, `s16_filter.py`, `grow.py`, `rings.py` and `ball.py` are byte-identical
copies, and they find each other through relative paths that the layout preserves:
- `s16_filter.py` sets `LOOP = EX/backgroundMaterial/.../wheeldis/loop` and imports `grow` from `LOOP/k42`;
- `grow.py` finds `rings` in `discharge/b8b` and `unavoidable.conf` relative to its own file;
- `rings.py` imports `ball` from `discharge`.

You can set `F2B7_AUDIT_ROOT=/path/to/audit` to override the root. It is not a `PYTHON*` variable, so it still
works under `-I`.

**Do not add files under `tree/ex_A97/.../loop/k*/`.** `s16_filter.registry()` reads every regular file in
`loop/k[0-9]*/` (705 files, all packaged) and keeps the first matching kc line for each wanted name. Hidden files such
as `.DS_Store` and subdirectories such as `__pycache__` are ignored.

## Registry (same for all modes)

`s16_filter.registry()` with `donly=0` is built from:
- 582 RSST configurations: the `verdict=D2` or `verdict=C2cons` entries of `k44/rsst_verdicts.txt`, matched to
  `unavoidable.conf` through `k44/rsst.txt`;
- the A97 k3x names in `k3x_D_A97.out` and `k3x_C_A97.cfast`, read as kc lines from the `loop/k*` files.

These give base = 4949 configurations. With `reg=broad` (the default), the 5-field kc lines of `nl51_kc.txt` are added
(13149 names). The names in `exname_keep95p131f.txt` are then removed, leaving **12428**. Every run prints
`registry broad base 4949 with nl51 13149 after exname 12428`.

Containment is `grow.embeddings` (unchanged): exact degrees, induced, interior triangles mapped onto faces. A vertex
whose degree is set to 99 (`NEVER`) is never an exact match.

## Modes

### `rejust.py rules D SG part=k/n [reg=donly]`

Per-rule verdicts for group `d{D}_w7`, side `SG` (`1` or `-1`). Output: `rejust_rules_d{D}_{SG}_{k}_{n}.json` in cwd.

1. **Live filter (7-sides).** Only "live" rules are tested. A rule is skipped when both of these hold:
   - the slot-side link neighbour `c = w_{SG mod D}` is fixed to letters that are all below 7;
   - the slot-side apex (`s_0` for SG=1, `s_{D-1}` for SG=-1) is fixed below 7.
2. **Test row.** For each live rule `[p, w_req, s_req]`:
   - u has exact degree D;
   - `w_0 = 7`;
   - a link position whose rule entry allows exactly one letter gets that letter; every other link position gets 9;
   - apexes fixed by the rule get their value; every other apex gets 9;
   - 9 means never exact.
3. **Geometry.** This is the real 2-ball geometry, `s16_filter.build(D, test_link)`.
4. **Slot.** The slot is the private of `w_0` adjacent to `s_0` (SG=1) or to `s_{D-1}` (SG=-1). Every other
   private is never exact (strict 14'). An assertion checks that the slot is adjacent to exactly `w_0`, its apex and
   the other private of `w_0`.
5. **Verdict.** A slot value is killed when some registry configuration embeds and needs only the slot.
   `justified` = letter `p` is killed. `witness` = the first killing configuration in registry order.

Each entry has: `p, w_req, s_req, test_link, test_apex, justified, witness`.

### `rejust.py sides FILE.json part=k/n`

The input is a list of degree-7 sides `{link, apex, j, sg, rmask}`. The original run used `ref/extra_sides.json`,
the 176 sides of `f2b7_all.json` where `c >= 7` or `ap >= 7` and the rule file kills more letters than f2b's own
mask (made by `cmp_all.py`, not packaged).

1. **Test row.** The whole link and all apexes are exact (9 = never). The slot is the private of `w_j` adjacent to
   `s_j` (sg=+1) or to `s_{j-1}` (sg=-1). Every other private is never exact.
2. **Mask.** `broad_mask` has bit `L-5` set when letter L is NOT killed. `rmask` uses the same convention.
3. **Verdict.** `unjustified_letters` are the letters the rule kills but the registry does not. `why` maps each
   killed letter to its first killing configuration.

Output: `rejust_sides_{k}_{n}.json`.

### `audit_any.py GROUP [SG] [part=k/n] [live=1] [reg=donly]`: new, any group

This runs the `rules` test on any group: `d7_w6`, `d8_w6`, `d9_w6`, `d7_w7 1|-1`, `d8_w7 1|-1`.

**How it reuses rejust.py.** It execs `rejust.py`'s own preamble unchanged, which gives it the same registry and the
same `build`/`kills`. It then builds each test row exactly as `rules` mode does, with `w_0 = 7` for w7 groups and
`w_0 = 6` for w6 groups.

**w7 groups.** The test is `rejust.py`'s `kills()`, called as `rules` mode calls it. By default every rule of the
group is tested. `live=1` applies rejust's 7-side filter, so `d7_w7 1 live=1 part=k/4` reproduces
`rejust_rules_d7_1_k_4.json`.

**w6 groups.** The slot is the private of the link-6 vertex `w_0`. A degree-6 link vertex has exactly one private,
and it is adjacent to both `s_0` and `s_{D-1}`.
- `kills()` cannot run on this case. Its geometry assertion is written for a link-7 vertex with two privates, and it
  fails here.
- So the wrapper uses `ext.py`'s existing `strict()`, copied verbatim. It is the same computation as `kills()` (same
  slot rule, same never-exact handling, same embedding loop), without the assertions. It runs on rejust's registry.
- One new sanity assertion checks that `w_0` has exactly one private, adjacent to exactly `{w_0, s_0, s_{D-1}}`.
- No other semantics were added. w6 rules have no side split, and the slot is unique, so SG is not used.

Output: `anyrule_{GROUP}_{sg1|sg-1|w6}_{k}_{n}[_live].json`. Each entry has `group, sg, idx` (the index in the
group's rule list) and then the rejust fields.

**Limits** (all inherited from rejust.py's row construction):
- A link entry that allows several letters (for example `[7, 8]`) is tested as 9 (never exact), as in rejust.py.
  Configurations that need an exact degree there do not count. No completion is enumerated.
- u always has exact degree D, also for `d9_w6`.
- `live=1` is rejust's 7-side filter, so it exists only for w7 groups.
- Results are written once, at the end of each part. Use `part=k/n` to chunk a long run.
- "NOT justified" means the strict single-slot test with this registry does not reproduce the kill. It does not
  mean the rule is wrong. `hyp.py` and `ext.py` test looser semantics and larger registries.

Group sizes in this rule file: d7_w6 2437, d8_w6 1738, d9_w6 463, d7_w7 1440 + 1440, d8_w7 904 + 904, total
**9326** rules.

### Follow-up scripts (unchanged apart from paths)

These need **cwd to contain `variants.py`** (they `exec(open('variants.py'))`) and, for `ext.py` and `hyp.py`, the
`rejust_rules_d*_*_4.json` files (`ext.py sides` also reads `unjustified_sides.json`).

- `variants.py ROW...`, where ROW = `link,apex,j,sg`: tests a row under four variants: broad strict, exname-held
  strict, RSST none-verdict strict, broad non-strict.
- `ext.py rules D SG` / `ext.py sides`: re-tests the unjustified items against an extended registry. The extended
  registry adds the exname-held configurations, RSST none-verdict, `s49/kpriv_kc.txt`, and grow's 12 explore kills.
- `hyp.py D SG k/n`: explains each unjustified rule by one of four hypotheses:
  - H4: the exname-held or none-verdict configurations;
  - H5: the other private;
  - H1: the other own private left free;
  - H2: all privates left free.
- `witness.py ROW...`: lists the joint requirements with the slot, and with slot plus other private free.
- `variants2.py ROW...`: other-side strict kills and the joint requirements with both privates of `w_j` free.
- `frame.py`: a 2-ball naming and convention check, with no inputs.

## How to run

```sh
cd audit && mkdir -p work && cd work           # outputs go to cwd
python3 -I -B ../scripts/rejust.py rules 7 1 part=0/4      # calibration: must equal ../ref/rejust_rules_d7_1_0_4.json
cmp rejust_rules_d7_1_0_4.json ../ref/rejust_rules_d7_1_0_4.json && echo CALIBRATION OK

# full audit of every group, 8 parts each, in parallel (adjust -P to your core count)
for g in d7_w6 d8_w6 d9_w6 "d7_w7 1" "d7_w7 -1" "d8_w7 1" "d8_w7 -1"; do
  for k in 0 1 2 3 4 5 6 7; do echo "$g part=$k/8"; done
done | xargs -P 8 -I{} sh -c 'python3 -I -B ../scripts/audit_any.py {} > "log_$(echo {} | tr " /=" "___").txt" 2>&1'

# follow-ups (need variants.py and the rejust outputs in cwd)
cp ../scripts/variants.py ../ref/rejust_rules_d*_4.json ../ref/unjustified_sides.json .
python3 -I -B ../scripts/hyp.py 7 1 0/4          # must equal ../ref/hyp_d7_1_0_4.json
```

To check the package's integrity:

```sh
python3 -c "import hashlib;[print('BAD',p) for h,p in (l.rstrip('\n').split('  ',1) for l in open('MD5SUMS')) if hashlib.md5(open(p,'rb').read()).hexdigest()!=h]"
```

Run it from `audit/`. It prints nothing when everything matches. On Linux, `md5sum -c MD5SUMS` does the same.

## Smoke test (this package copy, 2026-11-06)

The test ran from the shared-folder copy of the package, with cwd inside the package, `python3 -I -B`, `nice -n 19`,
one process at a time. The 4-core Linux machine was busy with LP runs (load about 4). Python 3.13.

| run | rules | result |
|---|---|---|
| `rejust.py rules 7 1 part=0/4` | 88 | **88/88 entries identical** to `ref/rejust_rules_d7_1_0_4.json`: same justified flags (18 not justified) and same witnesses; file byte-identical, md5 `4b85ee08bc8a3cab99a8a33274af1cf9` |
| `audit_any.py d7_w7 1 live=1 part=0/4` | 88 | 88/88 identical on all 7 rejust fields |
| `hyp.py 7 1 0/4` | 21 | byte-identical to `ref/hyp_d7_1_0_4.json` |
| `ext.py rules 7 1` | 84 | runs; "justified by extended registry 0"; strace shows no file opened outside the package |

strace of `rejust.py` and `ext.py` from the package showed only stdlib and package files opened.

## Measured runtime

Single process, `nice -n 19`, on the busy machine above. The registry load adds about 3 s per process, on top of the
per-rule times in the table.

| run | rules | per rule mean | max |
|---|---|---|---|
| `rejust.py rules 7 1 part=0/4` | 88 | **0.76 s** (67 s loop, 70 s wall) | n/a |
| `audit_any.py d7_w7 1 live=1 part=0/4` | 88 | 0.73 s | 0.97 s |
| `audit_any.py d7_w6 part=0/50` | 49 | 0.64 s | 0.77 s |
| `audit_any.py d8_w6 part=0/50` | 35 | 0.63 s | 0.91 s |
| `audit_any.py d9_w6 part=0/20` | 24 | 0.70 s | 0.89 s |
| `audit_any.py d7_w7 1 part=0/60` | 24 | 0.70 s | 0.89 s |
| `audit_any.py d7_w7 -1 part=0/60` | 24 | 0.67 s | 0.89 s |
| `audit_any.py d8_w7 1 part=0/40` | 23 | 0.65 s | 0.76 s |
| `audit_any.py d8_w7 -1 part=0/40` | 23 | 0.71 s | 0.95 s |

A full audit of all 9326 rules at about 0.7 s per rule takes about 1.8 CPU-hours on this machine, split over as many
parts as you have cores.

Smoke-slice verdicts, which are not an audit result: not justified d7_w6 13/49, d8_w6 13/35, d9_w6 18/24,
d7_w7 1 7/24, d7_w7 -1 6/24, d8_w7 1 6/23, d8_w7 -1 4/23.

## Not packaged

The review folder's other helpers belong to a separate provenance check, with inputs outside this closure:
- `fire.py`, `prov_check.py`, `prov_check2.py`, `xtab.py`, `scope6.py`, `tally.py`, `unj.py` and `six.py` need
  `P_own_lp/s63_minconf/prov.pkl`;
- `cmp_all.py`, `impact.py`, `six_sides.py` and `unj.py` also need the f2b engine `s86_f2b7/eng/f2b.py` and
  shared-folder JSONs (`s85_k85CL/f2b7_all.json`, `dual_rows_k85CL_p1_00.json`);
- `outside_run.py` and `outside_swap.py` need `ext_check_oct30/.../build_upgraded_kills.py`.

None of these is read by `rejust.py` or `audit_any.py`.
