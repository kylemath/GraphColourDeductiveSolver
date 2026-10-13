# Heavy runs for the Studio: the full RSST D-reducibility pass in Lean, and gluing at order 34

- **From:** Long Table (the MacBook session)
- **To:** Studio session
- **Sent:** 2026-10-13 11:28 MDT
- **Repo state:** `main` at `8a923844` (pushed). Pull first.

Kyle has approved both runs. Respect the Studio caps in `CoordinatorPlan.md` (`nice -n 10`, at most 14 workers, EEGLearn has priority). Label everything exploratory. Commit only your own files, by explicit path. Report back in a message file in `messages/2026-10-13/`.

## Job 1: all 633 RSST configurations through the Lean D-reducibility checker

**Where:** `backgroundMaterial/planemap-structural/longtable/reducibility/dcheck/`. It is a Lake package on core Lean v4.35.0-rc3 plus Std, with no Mathlib. See the README there, section "Run 2".

**Approved:** Kyle approved `native_decide` for this run. Each theorem gets one auxiliary axiom; record it with `#print axioms`.

**Steps:**
1. Build `DCheck.lean` and check that `DCheckThms.lean` (ring ≤ 9) and `DCheckThms11.lean` (ring 10–11) reproduce, in 1.6 s and about 140 s on the MacBook.
2. Write the remaining configurations as about 16 theorem files, grouped by ring 12, 13 and 14. Build them in parallel with at most 14 workers in total.
3. For each configuration, prove its agreement with RSST's data (`DCheckData.lean`): the extendable count equals the header field, and `dReducible = true` exactly when the contract size is 0.
   - The expected result is 249 D-reducible, and 384 that are not D-reducible (C-reducible in RSST).
   - Any disagreement is a finding: report it with the configuration's name.
4. Optional, before step 2: the speed-ups in the README (a Gray-code subset loop, not rescanning stuck matchings). They are probably worth 3–10×.

**Estimate:** about 12–15 CPU-hours as the code stands, mostly at rings 13–14.

**Report:**
- timings by ring;
- the agreement count;
- the axiom lines.

## Job 2: gluing at order 34, and gluing along 4-cycles

**Where:** `backgroundMaterial/planemap-structural/longtable/gluing/`. See `GLUING.md`.

**Tools:**
- `sepcyc.c` counts nontrivial separating 4- and 5-cycles.
- `glue.py` and `run_glue.py` do the vertex substitution along 5-cycles, then run the `frame` filter and `picyc --full`.

**What the MacBook found:**
- The frame census at orders 22–33 has no nontrivial separating 4- or 5-cycles.
- On 330 glued frame graphs (orders 37–57) the floor and R\* hold.
- Gluing makes floor-tight holes about 4× as common.

**Steps:**
1. Run `sepcyc` on the order-34 frame list (`Census34/out/frame-34.txt`, which is only on the Studio). Does the "internally 6-connected" fact still hold at order 34?
2. Glue a wider range of graphs:
   - B ranging over all frame graphs at orders 22–26, not only p22;
   - A ranging over the order-27/28 seeds with floor-tight holes, and the order-33 holes with mf = 1/4 (8,556 holes; the list is in `Census33/out/eval-33.jsonl.gz`, field `mf`).
3. Add a gluing along separating 4-cycles: delete an edge on each side and glue the two quadrilateral faces.
4. Aim gluings next to the holes that carry positive-winding π-cycles (the round-1 hits are in `run-tight.jsonl`). The goal is to make positive winding occur inside a small class.

**Report:**
- min class F/N;
- the number of frozen classes;
- positive cycles together with their class sizes;
- any class below 1/4, re-checked with a second engine (TrackM `tm_lib`).

## Not for the Studio (MacBook agents still running)

- The exact SAT search for T1-v (law + A5v, `longtable/axioms/`).
- The literature check and induction test for Bound A′ (`longtable/flips/`).
