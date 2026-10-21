# pubrules: published discharging rules on our binder rows

A diagnostic map, not a claim. When the K = 2 LP stalls, run this on the binder rows of the stalled cert. It lists which
published discharging rules move charge into or out of the binding vertex u, what each rule conditions on, and where
u's net charge ends under each published rule set. Use the output to see the shape of the rule we are missing. Anything
we then adopt is restated as our own rule and goes through our LP, two engines and Lean as usual ("own rules only";
published sets are a map).

## How to run (about 1 s per row)

```
cd backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/pubrules
python3 pubrules.py --self-test                       # must print two "self-test OK" lines
python3 pubrules.py ROWS.txt --out REPORT.md          # default sets: rsst,nl26
```

`ROWS.txt` takes the receiverR2 lines we already pass around (explore's `rows58.txt` format works as is):

```
# w        d  link     sword     free-text tag
-0.05701   7  7766556  6567568   A78 r58b face
7 8665556 7675865                # weight optional
```

To build ROWS.txt from a cert: take its `receiverR2` rows (`["receiverR2", d, LINK, SWORD]`, weight `w`).
Options: `--sets rsst` or `--sets nl26` for one set only; `--max-fill N` caps the private fillings (all 5^m fillings if
5^m <= N, otherwise a fixed-seed sample of N).

## What it reads (all vendored here, nothing from either racing team)

- `data/rsst_drules.v`: Robertson, Sanders, Seymour and Thomas's 32 rules, in Gonthier's Coq encoding. These are the
  `drule1..drule32` and `base_drules` lines from coq-community/fourcolor `theories/proof/discharge.v` (CeCILL-B, md5
  5b8491c3…, the same file as BORROWED-CHANNEL-7FACE.md). There are 38 parts with multiplicity and 71 after symmetrize.
  The fit semantics are Studio's `studio/rsst_rules/rsst_score.py`: a part fits at hub h when deg h equals the number of
  subparts and every spoke, hat and fan range holds. Each fit moves 1 unit from h to its third spoke. "m" marks a mirror
  part, and `drule1#2` is drule1's second copy.
- `data/nl2026/R/*.rule`: Inoue et al. 2026's 43 rules (84 files with mirrors), from github.com/near-linear-4ct/
  discharging-rules at d85bfe09 (MIT, see `data/nl2026/LICENSE`).
  - File format: the header is `n src dst amount`, then one line per vertex, `id lo hi nbrs...` (hi 0 = unbounded).
  - A neighbour list ending in -1 is a consecutive arc of that vertex's rotation. A list without -1 is the whole rotation.
  - Our reading: a rule applies once per (file, source, target) pair when its graph embeds. The embedding is injective,
    places every arc on consecutive rotation slots, and puts every degree in range.
  - Mirrors are matched in one fixed orientation, so our `_1`/`_2` may be swapped relative to the authors' drawings. The
    set is mirror-closed, so totals are unaffected.
- Both sets use charge 10(6 − deg). One unit is 0.1 in our 6 − d scale.

## Window and what "condition" means

The window is u, the link w_i, the apexes s_i (s_i is the apex of w_i w_{i+1}, as in RELAY_SPEC_s39o §39.1), each
w_i's d_i − 5 privates `p_i.k`, and a fresh third ring.
- A rule test on a known vertex is decided.
- A test on a private becomes a condition such as `p0.2=5`.
- A test that reads ring 3 or beyond is OPEN. It counts toward "possible" but not toward "certain".
- For every filling of the privates (5..9, 9 = 9+), u's net charge `10(6 − d) + in − out` is an interval
  [certain, possible].
- The report gives the whole range, and also the range with every private ≥ 6. That second range is where explore's
  survivors live, since a 5 private usually dies to the registry.

## Checks

`--self-test` reproduces two earlier hand ledgers exactly:
- Long Table's BORROWED-CHANNEL-7FACE ledger on 7665566/6675676: u ends at 0 in 6,400 of 15,625 fillings, max +4.
- Studio's `rsst_lt7.txt` histogram on 7665566/6675666: {0: 3,072, 1: 5,888, 2: 4,480, 3: 1,760, 4: 380, 5: 43, 6: 2}.

The NL26 matcher has no published ledger to check against. Its rules 008/009 restate RSST drule8/9, and on every row
run so far they fire exactly where drule8/9 fire.

## Limits

- Only u's ledger (rules whose source or target is u). Transfers elsewhere in the window are not listed.
- A link letter of 9 (9+) is not supported, because its private count is unknown.
- Steinberger 2010's 42 rules are not included. No machine-readable copy was reachable from here.
- A rule that needs ring 4 shows as OPEN; it is never counted as certain.
