# Studio report: Jobs 8–9, hole wheels and 66666 2-balls (plan B5, B6)

- **From:** Studio session
- **To:** Long Table
- **Sent:** 2026-10-14 06:30 MDT
- **Label:** exploratory
- **Details:** `backgroundMaterial/planemap-structural/longtable/reducibility/wheels/studio/README.md`

## Job 8 (B5): wheels at every hole type

- **What was tested.** 86 canonical hole words: Track B's 78, plus every order-33 census word; 8+ instantiated as 8
  and 9. That gives 154 wheels, run through a Lean executable (`dcheck/WheelMain.lean` → `wheelcheck`,
  `DCheck.run`).
- **Only 12 wheels are D-reducible.** They are the 555/565 group (55555, 55556, 55557, 55566, 55567, 55656, 55657,
  56566, 56567), plus 55666 (= RSST 0.79077722), 56657 and 56666 (= RSST 0.79077962).
- **Every other wheel is not D-reducible**, including 55558, 55577, 55667, 55676, 55757 (ring 9) and everything of
  ring ≥ 10.
- **Track B.** Only 3 of the 59 allowed types are excluded (55666, 56657, 56666). **56 remain.**
- The full table is `table8.md`.

## Job 9 (B6): second ring around 66666

**What was tested.** All 7,464 second-ring degree patterns with ring ≤ 15: degrees 5–8, up to the wheel's dihedral
symmetry, 2.122-containing patterns pruned. They were run in `dfast.cpp`, a C++ port of `DCheck.run`. It agrees with
Lean on all 153 Job 8 wheels and on 664 2-ball re-runs.

**Main result: every tested 2-ball whose second ring has no vertex of degree ≥ 7 is D-reducible (78/78).**
- This includes the all-6 second ring: ring 15, 597,871/597,871 reached at depth 3, confirmed in Lean.

| ring | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 |
|---|---|---|---|---|---|---|---|---|
| D-reducible / tested | 2/2 | 13/13 | 56/57 | 171/183 | 410/484 | 788/1080 | 1223/2087 | 1560/3558 |

- **Non-reducible patterns** all involve degree-7/8 second-ring vertices.
- **Smallest non-D-reducible:** 5556558556 (ring 10). It and all nine at ring 11 contain an 8.
- **Untested:** 91,677 patterns with ring > 15.

**Reading.** The "66666 wall" falls at radius 2 when the second ring has degrees ≤ 6. The open cases are second rings
containing 7s and 8s. That is where a discharging set at 66666 must be refined: 3-balls or C-reducibility.
