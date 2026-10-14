# Hole wheels and 66666 2-balls: D-reducibility at scale (Studio Jobs 8–9, 14 Oct 2026) [exploratory]

These are plan items B5 and B6. D-reducibility uses the Birkhoff–Heesch closure exactly as `../../dcheck/DCheck.lean`
(`run`). "Not D-reducible" does not mean "not reducible": C-reducibility (with a contraction) is not tested here.

## Engines

| engine | what | validation |
|---|---|---|
| `../../dcheck/WheelMain.lean` → `wheelcheck` | Lean executable: reads configurations (`name r m ringAdj intAdj`) and runs `DCheck.run`; rings ≤ 15 | reproduces Long Table's `wheels-out.txt` exactly (55666, 56666, 66666 1241/2461, 66667 1893/7381) |
| `dfast.cpp` | C++ port of `DCheck.run` with the same level-synchronous closure; stuck-matching reach sets are cached; rings ≤ 16; about 20× faster | identical classes, ext, reached, D and depth on all 153 Job 8 wheels with ring ≤ 15 and on all 652 D-reducible 2-balls with ring ≤ 12 (Lean re-run) |
| `gen_words.py` | hole words: Track B 59 + 19 types plus all order-33 census hole words, up to rotation and reflection; `8+` instantiated as 8 and 9; wheels as in `../wheels.py` | |
| `gen_2ball.py` | 66666 2-balls: second-ring degrees in {5, 6, 7, 8} on p_0 s_0 … p_4 s_4, up to the wheel's dihedral symmetry; ring = Σ(d_p − 4) + Σ(d_s − 5); pruned if 2.122 or a diamond lies among the known-degree vertices | every built configuration has the stated degrees and a consistent ring cycle |

## Job 8 (B5): wheels at every hole type (`table8.md`, `table8_summary.txt`)

86 canonical words (instantiated as 154 wheels, rings 5–16) were run through the Lean executable; the ring-16 wheel
was run in `dfast` only.

- **D-reducible: 12 wheels.** 55555, 55556, 55557, 55566, 55567, 55656, 55657, 56566, 56567 (all in Track B's
  555/565 group), plus **55666 (= RSST 0.79077722), 56657 and 56666 (= RSST 0.79077962)**. The RSST matches agree on
  ring, interior size 6 and extendable count with `DCheckData`.
- **Not D-reducible: every other wheel**, including many with a degree-5 neighbour:
  - ring 8: 55558;
  - ring 9: 55577, 55667, 55676, 55757;
  - ring 10: 55668, 56676;
  - every wheel of ring ≥ 10.

  The seed observation ("a degree-5 neighbour makes the wheel D-reducible") holds only for these small cases.
- **Track B.** Of the 59 allowed hole types, only 55666, 56657 and 56666 are excluded by wheel D-reducibility.
  **56 types remain for PureClean/LPC** (or for larger configurations).

## Job 9 (B6): second-ring growth around 66666 (`summary9.txt`, `run9/`)

There are 106,912 second-ring degree patterns. 7,771 are pruned (they contain 2.122), and 91,677 have ring > 15 and
are not tested. The **7,464 with ring ≤ 15** were all run in `dfast`.

| ring | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 |
|---|---|---|---|---|---|---|---|---|
| D-reducible / tested | 2/2 | 13/13 | 56/57 | 171/183 | 410/484 | 788/1080 | 1223/2087 | 1560/3558 |

**Family results.**
- **Every tested 2-ball whose second ring has no vertex of degree ≥ 7 is D-reducible: 78/78.** This includes the all-6
  second ring (ring 15, 597,871 ring colourings, all reached at depth 3) and every 5/6 pattern with at least one 5.
- **Degree-7 and degree-8 vertices are what break reducibility.** By the margin (#5 − Σ_{d≥7}(d − 6)), the
  D-reducible fraction is 2/2, 13/13, 56/57, 171/183, 410/484, 788/1080, 1223/2087, 1560/3558 for margin 7 down to 0.
  Margin 0 is the only way to reach ring 15 with a 7/8.
- **Smallest non-D-reducible 2-ball:** 5556558556 (ring 10), then nine at ring 11. All of them contain an 8.

**Lean confirmation.**
- All 652 D-reducible 2-balls with ring ≤ 12 are confirmed by the Lean executable (identical output).
- The all-6 2-ball is confirmed in Lean: 597,871/597,871 reached at depth 3, in 455 s.
- A random ring 13–15 sample of 12 (2 D-reducible and 2 not at each ring) is also confirmed in Lean.
- 664 Lean re-runs in total, all identical to `dfast` (`lean9/`).

## Reading

- One ring around the hole is not enough except at the smallest words. Two rings around 66666 are enough whenever the
  second ring has degrees ≤ 6, which is the hexagonal-patch case behind the "66666 is the wall" worry.
- The obstruction moves to second rings containing degree 7/8 vertices. That is where a discharging argument at
  66666 must look next. Ring > 15 cases (91,677 patterns) are untested; ring 16 runs at about 44 s per configuration
  in `dfast`.
