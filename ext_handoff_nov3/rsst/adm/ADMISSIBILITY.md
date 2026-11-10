# RSST-NONE: why our engines reject the RSST "none" configurations (W6b, 10 Nov 2026)

## Answer

Round 44's "none" verdict needs one **conservative** X: kc -C accepts it and cfast --fixed confirms it. RSST's own contracts
for these 51 configurations put **two or three ring vertices in one X-component**, and kc's conservative mode refuses
exactly that. Nothing else refuses them:

- **The colouring check never fails.** With RSST's own X, every one of the 51 has leftover 0 on kc (broad mode, and forced
  mode) and on cfast --fixed.
- **Every local condition holds.** The Gonthier/RSST local conditions hold for all 51, checked independently. kc's broad
  distance rule (-C2) holds for all 51.
- **What is missing is admissibility, not reducibility.** These are C-reducible on both engines once a component may hold
  several ring vertices. That relaxation needs a global argument: no outside chord joins two ring vertices of one
  component. The argument is in the "Is adding it sound?" section. For all 51 it needs only "no separating 3- or 4-cycle",
  because every X-path between two ring vertices has length at most 3.
- **The Lean side lacks the same thing.** CGlue's `admissibleX` also requires distinct ring labels. The 3 registry
  ring-merge entries are held for this reason (CGLUE-SCOPE.md).

W6r's mscreen N on the 14 "none" configurations in its cover fits this picture: mscreen searches conservative X only.
I did not re-run mscreen.

## Inputs and mapping (checked)

The 4 configurations in W6r's 33-configuration cover:

| RSST | kc id | r | m | RSST X (kc notation) |
|---|---|---|---|---|
| 2.126 | rsst003_2o126 | 8 | 4 | {R0-I0,R2-I0,R4-I2,R6-I2} |
| 3.1324817 | rsst061_3o1324817 | 12 | 8 | {R0-I4,R6-I3,R8-I3,R10-I4} |
| 128.1324802 | rsst065_128o1324802 | 12 | 8 | {R0-I5,R6-I4,R8-I4,R10-I5} |
| 124.1324817 | rsst202_124o1324817 | 14 | 9 | {R0-I5,R8-I4,R10-I4,R12-I5} |

- **Sources.** Configurations come from `rsst_closure/inputs/rsst.txt` and X from `rsst_x.txt`. The 51 ids are the
  `verdict=none` rows of `rsst_verdicts.txt` (`none51.ids`).
- **Independent check against RSST's file** (`src/chkx.py`, `chkx.out`). The check reads `studiointel/routeb/rsst/unavoidable.conf`
  directly and does not use round 44's `rsst2kc.py`. For all 51:
  - the contract line (ring vertex v ≤ r → R(v−1), otherwise I(v−r−1)) equals the rsst_x.txt set: 0 mismatches;
  - the header (n, r, ext, bad) equals our (r + m, r, kc ext, cfast bad): 51/51.
  - I also read 2.126 by hand: header `12 8 81 154`, contract line `4  1 9 3 9 5 11 7 11`.

## Engines, and which take a fixed X (checked)

| Engine | Binary (md5) | Fixed-X interface | Admissibility used for a fixed X |
|---|---|---|---|
| kc (H-KC) | `/tmp/swarm-A3/bin/kc` = `/tmp/swarm-W13/bin/kcc_o3` (49393b29); source `/tmp/swarm-W13/bin/kc.cpp` (f9da2a70) | `-x FILE` (lines `name {X}`) prints `adm=no` or `adm=yes … leftover N of M bad` | Conservative. Broad admissibility is reachable only through `-C2`, which also runs the X search. A fixed X cannot be scored broad without the search. |
| kc_rn (this task) | `src/kc_rn` built from `src/kc_rn.cpp` (4b40c0ad), a copy of kc.cpp f9da2a70 | `-x FILE`, plus `-B` (broad, the same code path as `-C2`, without the search) and `-F` (no admissibility except "no loop inside K") | Prints the refusal reason: `adm=no(reason)` |
| cfast | `/tmp/swarm-A3/bin/cfast` = `/tmp/swarm-W13/bin/cfast` (e319f040); source `/tmp/swarm-W13/bin/cfast.cpp` (bd353d11) | `--fixed "R0-I0,…"` (`--nogonthier` drops sparse/triad) | Local only, Gonthier conditions included (next section). Ring vertices identified through X are allowed (`ringEq`, cfast.cpp:180). |
| `/tmp/swarm-W13/bin/kcc` (469527b4) | differs from kcc_o3 | not used | — |

- **cfast drops tokens silently.** `--fixed` ignores a token that is not an edge. I compared the printed edge count with
  |X| for every run: 37 four-edge and 14 three-edge X, all parsed in full.
- **kc_rn changes the source only where the header says.** It adds a 5-line header comment, the -B/-F flags and the
  `WHY` strings. Its D numbers (classes, ext, reached) agree with cfast's bad count for all 51.

## Results with RSST's own X

**The 4 cover configurations** (files `kc_cons_cover4.out`, `kc_rn_cover4.out`, `cfast_cover4.out`, `cover4.tsv`):

| kc id | bad classes | kc -x (A3 binary) | refusal reason (kc_rn) | kc_rn -B (broad) | kc_rn -F | cfast --fixed / --nogonthier | non-endpoint triad |
|---|---|---|---|---|---|---|---|
| rsst003_2o126 | 154 | adm=no | component holds R0 and R2 | adm=yes, leftover 0 of 154 | leftover 0 | C-REDUCIBLE, 4 edges, leftover 0 / same | I1, I3 |
| rsst061_3o1324817 | 11,189 | adm=no | component holds R6 and R8 | adm=yes, leftover 0 of 11,189 | leftover 0 | C-REDUCIBLE, 4 edges, leftover 0 / same | I0, I6 |
| rsst065_128o1324802 | 12,492 | adm=no | component holds R6 and R8 | adm=yes, leftover 0 of 12,492 | leftover 0 | C-REDUCIBLE, 4 edges, leftover 0 / same | I0, I7 |
| rsst202_124o1324817 | 133,573 | adm=no | component holds R8 and R10 | adm=yes, leftover 0 of 133,573 | leftover 0 | C-REDUCIBLE, 4 edges, leftover 0 / same | I0, I7 |

Each of the 4 has the same shape:
- X has two components.
- Each component is a ring vertex, an interior vertex, and a ring vertex two steps further round the ring. So the X-path
  length is l = 2 and the ring gap is 2.

**All 51 "none" configurations** (files `kc_rn_none51.out`, `cfast_none51.out`, `none51.tsv`; per-configuration table in
the appendix):

- **kc conservative:** refuses 51/51, every time with "component holds ring vertices Ra and Rb". There are no other
  refusal reasons.
- **kc_rn -B (broad):** adm=yes, leftover 0, 51/51.
- **kc_rn -F:** leftover 0, 51/51.
- **cfast --fixed:** C-REDUCIBLE, leftover 0, 51/51; the same with `--nogonthier`.
- **Ring vertices per X-component:**
  - at most 2 in 43 configurations;
  - 3 in 8 configurations: rsst115, 142, 258, 433, 439, 468, 488, 600.
- **Ring pairs inside one component** (94 pairs, as (X-path length l, ring gap): count):

  (2,2): 65; (2,6): 7; (3,2): 6; (3,4): 5; (2,4): 3; (2,5): 2; (3,3): 2; (3,5): 2; (3,6): 1; (3,7): 1.

  Every inner vertex is interior, and the maximum l is 3. No pair is at gap 1.
- **Independent check** (`src/analyse_x.py`, own code, does not read kc/cfast source), 51/51:
  - no X-edge is a ring edge;
  - no loop: no configuration or ring edge outside X joins two vertices of one component;
  - X is sparse;
  - every 4-edge X (37) has a triad, and a triad that is not itself an X endpoint.
- **Round 44's search covered less.** Its own diagnostics (`k44/rsst_verdicts_C2.txt`) had kc -C2 broad *search*
  C-REDUCIBLE for 22 of the 51 and "pending" for 29. The fixed-X broad run above closes all 51.

## Admissibility side by side

| Condition | kc -C (conservative) | kc -C2 broad | cfast --fixed | Lean `admissibleX` (CGlue.lean:375) | RSST/Gonthier `valid_contract` (as recorded, see note) |
|---|---|---|---|---|---|
| 1 ≤ \|X\| ≤ 4 | yes (search size) | yes | yes (KMAX 4) | yes (CGlueU `admissibleXU` drops ≤ 4) | yes |
| X off the ring (each X-edge has an interior end) | yes | yes | yes | yes (X ⊆ listed ring-interior / interior edges) | yes ("disjoint from the ring darts") |
| ring–interior edges allowed in X | yes | yes | yes | yes | yes (Job 20) |
| no edge outside X inside one component (local loop) | yes, ring edges included | yes | yes, ring edges included | yes (labels: every other listed edge joins different labels) | sparse, which is weaker |
| sparse (no triangle with two X edges) | implied by the loop check | implied | yes (`--nogonthier` drops it) | implied by labels | yes |
| triad when \|X\| = 4 | no | no | yes (`--nogonthier` drops it) | no: "not needed", replaced by `XRingSimple` | yes |
| **at most one ring vertex per X-component** | **yes** | no | no | **yes** (last conjunct: distinct ring positions get distinct labels) | **no**: RSST's own contracts for these 51 break it (checked from unavoidable.conf) |
| several ring vertices per component | refused | X-path l ≤ 3, or l = 4 through interior vertices, unless gap 2 and the middle ring vertex sees all 3 inner vertices | allowed, no global check | refused | allowed per configuration; the global no-loop fact is proved once, outside the per-configuration check (see note) |
| global "no outside chord" | not needed (≤ 1 ring vertex) | argued in a source comment (kc.cpp:315-321), not checked | **not checked** (cfast.cpp:14-15 says so) | not needed today | proved once (see note) |

Note on the RSST/Gonthier column:
- **Source.** It is taken from Job 20 (`discharge/c66666/JOB20-HYPOTHESIS.md:40`, md5 0f75126c). Job 20 ran fourcolor
  1.4.3 on Studio: "valid_contract only requires the contract to be disjoint from the ring darts, sparse, of size 1–4,
  and to have a triad at size 4". cfast's header cites the same conditions from `theories/proof/coloring.v`.
- **Not re-checked in this task.** I did **not** read the RSST paper or fourcolor's `coloring.v`/`embed.v`. I did not run
  fourcolor on the 51 either; the Studio/Mac is out of bounds.
- **The global step.** That the per-configuration check is local, and the global step lives in the embedding argument,
  is Job 20's statement (line 46, `embed.v`). How embed.v uses sparse and the triad is **not verified** here.
- **What is checked.** RSST's contracts in unavoidable.conf contain components with 2–3 ring vertices, so RSST's
  admissibility allows them.

## Which of RSST's conditions we lack

1. **Ring-vertex merging inside one X-component.**
   - kc -C (conservative) and Lean `admissibleX`/`admissibleXU` both refuse it.
   - kc -C2 and cfast accept it, but neither has a checked global argument: kc's is a source comment, and cfast has none.
   - This is the only reason any of the 51 is "none".
2. **Sparse and the triad, as separate conditions.**
   - kc conservative and Lean replace sparse with the stronger label (no-loop) condition, and drop the triad in favour of
     `XRingSimple` plus ≤ 1 ring vertex per component.
   - Neither matters for the 51: all are sparse, and all 4-edge X have a triad.
   - The triad becomes relevant only if Lean wants to copy Gonthier's global argument instead of the chord argument below.
3. **Gonthier's global loop-freeness lemma.** We have nothing like it for ring-merging contracts, in C++ or in Lean.

## Is adding it sound? The argument

**Setting.**
- T is a minimal counterexample, so it is internally 6-connected. In Lean terms: `T.Triangulated`, which gives `NoSep`
  and `NoShortSepCycle` (`ClaimGlue.lean:64`: no cycle of length 3..5 with `BothSides`, two on each side for length
  5). For a minimal counterexample this is `MinimalCounterexample.noShortSep` (ClaimGlue.lean:88, via
  `colorable_of_short_separating_cycle` in SepAll.lean, Job 25). I did not re-check that dependency.
- The configuration K occurs in T, and X is a contract that passes the local checks above.
- Assume the touched ring positions are not folded. In Lean this is `XRingSimple`: a ring position touched by X is
  visited once.
- Contracting X yields a smaller map T/X. C-reducibility then needs T/X to be loopless: no edge e ∉ X may join two
  vertices of one X-component.

**Which edges could make a loop.**
- If either end of e is interior, e is a listed configuration edge, so the local check excludes it.
- If e is a ring edge, the local check excludes it too: kc and cfast put ring edges in the loop check, and no pair here
  has gap 1.
- What remains is an edge of the outside G between two ring vertices u = ρa and v = ρb of one component: a **chord**.

**Why there is no chord.**
- Let P be the X-path from u to v, of length l. Its l − 1 inner vertices are interior (checked for all 94 pairs).
- P together with the chord uv is a cycle C of length l + 1 in T.
- Inside the configuration disc, P separates the two ring arcs a+1..b−1 and b+1..a−1. Outside the disc, the chord
  separates them too. So the two arcs lie on opposite sides of C.
- Both arcs are non-empty because the gap is ≥ 2. Their vertices are off C: they are ring positions other than a and b,
  not folded onto a or b by `XRingSimple`, and C's other vertices are interior.
- So C is a separating cycle of length l + 1 with a vertex on each side.
  - For l + 1 ≤ 4 this contradicts `NoShortSepCycle` (Birkhoff).
  - For l + 1 = 5 it is a contradiction unless one side is a single vertex. The only shape that allows a single vertex is
    gap 2 with the middle ring vertex adjacent to all 3 inner vertices; kc -C2 refuses that shape.
- **All 51 have l ≤ 3, so only cycles of length ≤ 4 arise.** The length-5 clause is not needed.

**What else the colouring side needs.**
- The ring colouring induced by a colouring of T/X gives the merged ring vertices one colour, and it is proper on the
  ring because gap ≥ 2.
- cfast (`ringEq`, cfast.cpp:48-49) and Lean `extCAux` (C66666.lean:85) count a colouring only if it satisfies these
  equalities; kc documents the same rule (`C'(X)`, kc.cpp:321 comment; I did not read that code path). An interior vertex contracted to ring positions s and t must take both `col k s` and
  `col k t`.
- So the existing colouring checks already handle the merge. A leftover of 0 means each such colouring extends.

**Status of the argument.**
- **Planar step.** The step "P and the chord put the two arcs on opposite sides" is the usual Jordan-curve argument in the
  disc picture. It assumes the ring of K is a simple closed curve in T. It is **not** proved here for folded rings beyond
  the touched positions; for example, an untouched position folded onto a position in the other arc is not covered.
- **In Lean.** Sides are obtained differently there, through face apexes (`apex_sides`, CGlue.lean:916), and that route
  would need to be redone for this cycle shape (next section).
- **Kinds of contract.** Folds are a separate issue from chords. For one ring vertex per component they are handled by
  `foldSafeX`. The argument is the same as the one behind Job 21's refusal ("merging two ring vertices can create a loop
  if the outside has a chord", studio17/UNCERTIFIED.md). Only a chord can create a loop; an outside path cannot.
- **Unverified:** I have not compared this argument with how fourcolor's embed.v proves global loop-freeness. RSST/Gonthier
  may use sparse and the triad for exactly this step, and their route may differ.

## What Lean would need, compared with the existing hC glue

The existing glue (dcheck/CGlue.lean md5 5356f896, CGlueU.lean 4cef8d46, CContract.lean 6b6456eb) has these parts:
- `CEntry` {cf, eqR, eqI, lbl, hC : cReducible18, hadm : admissibleX};
- `CEntryF` adds `hfold : foldSafeX`;
- C4a `contract_subgraph_gen` (CContract.lean:742), proved for any subgraph H;
- C4b `xGraph_labels` / `XLoopFree`.

| Piece | Change for ring-merging X | Status |
|---|---|---|
| hC (`cReducible18` → `cReducibleT` → `extCAux`) | **None.** `extCAux` already forces `col k s = col k t` for ring positions contracted together (read: C66666.lean:85-93, CGlue.lean:126-140) | checked by reading |
| C4a (`contract_subgraph_gen`) | None: stated for any subgraph H | read the statement only (CContract.lean:742) |
| `admissibleX` / `admissibleXU` | Drop or weaken the last conjunct (distinct ring positions have distinct labels). Keep "every listed non-X edge joins different labels". Add "positions with equal labels are not consecutive on the ring" (gap ≥ 2). | not written |
| `xLabel` / `xLabel_ring` | Well-definedness already comes from `XRingSimple`. Equal labels at two touched positions do no harm there. | read; not re-proved |
| C4b, `G`-edge conjunct of `XLoopFree` | Today it uses distinct ring labels ("a G-edge joins two different ring vertices, which get distinct ring labels", docstring CGlue.lean:513-518). It needs a new case: a G-edge between two positions with one label is impossible, by the chord argument. | not written |
| New per-key certificate, e.g. `chordSafeX` | For each pair of touched positions with equal labels, an interior X-path of length l ≤ 3, plus an edge of the cycle (ring–interior or interior–interior) whose two face apexes are known configuration vertices off the cycle. Decidable, like `cycCertB` (CGlue.lean:801). For l = 2 the cycle has no interior–interior edge, so the crossing edge must be a ring–interior edge of P, which `cycCertB` does not support today. | not written; design only |
| Soundness lemma for it | Like `cyc_sound` (CGlue.lean:947), with `apex_sides` (CGlue.lean:916) and `NoShortSepCycle`. The cycle now contains one G-edge (the chord), so check whether `Cyc`/`apex_sides` accept a cycle with a non-configuration edge. | **not checked** |
| `foldSafeX` | Its D1/D2 pairs assume one ring label per component. With shared labels, the pair lists must cover every ring position of the component. | not checked |
| Registry | The 3 held ring-merge entries (job30/c_ringmerge_held.log) would become eligible under the same lemma, as would the 6 Job 21 wheels if their X fit. | not checked |

- **Size.** The closest existing piece is the fold block, CGlue.lean ~760-1160 (`exclB`, `cycCertB`, `cycEx`, `foldSafeX`,
  `excl_sound`, `apex_sides`, `cyc_sound`). The new work is similar in kind: a certificate plus a soundness lemma, with
  no change to hC. **I have not estimated its size with any evidence.**
- **No hC rerun needed.** hC needs no new native_decide runs beyond the per-key `cReducible18` the registry already uses.
  The C2 broad mode and cfast give leftover 0 with RSST's X. A Lean `cReducible18` run on these 51 has **not** been done.

## Verified / not verified

**Verified by me in this task:**
- The mapping of the 4 cover configurations and the 51 ids.
- RSST's X against unavoidable.conf (51/51).
- The header counts against the engines (51/51).
- All engine runs above: kc A3 `-x`; kc_rn conservative, -B and -F; cfast --fixed with and without --nogonthier.
- The refusal reasons.
- The independent local checks and the ring-pair shapes, including l ≤ 3 for all pairs.
- The Lean definitions quoted (by reading).

**Not verified:**
- RSST's paper text, and fourcolor's `valid_contract`/`embed.v` sources (taken from Job 20 and the cfast header).
- fourcolor on these 51.
- The chord argument for folded rings, and in Lean (no Lean written or run).
- Whether `apex_sides`/`Cyc` take a cycle with a G-edge.
- `foldSafeX` with shared labels.
- mscreen; the Lean effort estimate.

## Appendix: the 51 configurations (from none51.tsv)

Column notes:
- l is the X-path length; g is the ring gap.
- "bad" is the number of classes outside the D-closure, which equals RSST's header value.
- Gonthier local means: no ring edge in X, no loop, sparse, and a triad if |X| = 4.

| kc id | RSST | r | m | X | ring vertices per X-component | ring pairs (l, gap) | bad | kc conservative | kc -B | kc -F | cfast --fixed | Gonthier local |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| rsst003_2o126 (cover) | 2.126 | 8 | 4 | `{R0-I0,R2-I0,R4-I2,R6-I2}` | [R0,R2] [R4,R6] | R0-R2 l=2 g=2; R4-R6 l=2 g=2 | 154 | no (2 ring v. in a component) | yes, leftover 0 | leftover 0 | C, 4 edges, leftover 0 | True |
| rsst010_3o1324802 | 3.1324802 | 10 | 7 | `{R0-I4,R4-I3,R6-I3,R8-I4}` | [R0,R8] [R4,R6] | R0-R8 l=2 g=2; R4-R6 l=2 g=2 | 1074 | no (2 ring v. in a component) | yes, leftover 0 | leftover 0 | C, 4 edges, leftover 0 | True |
| rsst014_3o1324806 | 3.1324806 | 11 | 7 | `{R0-I4,R5-I3,R7-I3,R9-I4}` | [R0,R9] [R5,R7] | R0-R9 l=2 g=2; R5-R7 l=2 g=2 | 3707 | no (2 ring v. in a component) | yes, leftover 0 | leftover 0 | C, 4 edges, leftover 0 | True |
| rsst019_8o1540806 | 8.1540806 | 12 | 8 | `{R0-I1,R6-I2,R2-I1,R4-I2}` | [R0,R2] [R4,R6] | R0-R2 l=2 g=2; R4-R6 l=2 g=2 | 11466 | no (2 ring v. in a component) | yes, leftover 0 | leftover 0 | C, 4 edges, leftover 0 | True |
| rsst022_8o1551606 | 8.1551606 | 13 | 8 | `{R0-I1,R6-I2,R2-I1,R4-I2}` | [R0,R2] [R4,R6] | R0-R2 l=2 g=2; R4-R6 l=2 g=2 | 39449 | no (2 ring v. in a component) | yes, leftover 0 | leftover 0 | C, 4 edges, leftover 0 | True |
| rsst028_126o442802 | 126.442802 | 10 | 7 | `{R0-I0,R6-I0,R2-I2,R4-I2}` | [R0,R6] [R2,R4] | R0-R6 l=2 g=4; R2-R4 l=2 g=2 | 1008 | no (2 ring v. in a component) | yes, leftover 0 | leftover 0 | C, 4 edges, leftover 0 | True |
| rsst038_122o1324802 | 122.1324802 | 11 | 7 | `{R0-I5,R5-I4,R7-I4,R9-I5}` | [R0,R9] [R5,R7] | R0-R9 l=2 g=2; R5-R7 l=2 g=2 | 3830 | no (2 ring v. in a component) | yes, leftover 0 | leftover 0 | C, 4 edges, leftover 0 | True |
| rsst039_126o1306802 | 126.1306802 | 11 | 7 | `{R0-I0,R6-I0,R2-I2,R4-I2}` | [R0,R6] [R2,R4] | R0-R6 l=2 g=5; R2-R4 l=2 g=2 | 3680 | no (2 ring v. in a component) | yes, leftover 0 | leftover 0 | C, 4 edges, leftover 0 | True |
| rsst061_3o1324817 (cover) | 3.1324817 | 12 | 8 | `{R0-I4,R6-I3,R8-I3,R10-I4}` | [R0,R10] [R6,R8] | R0-R10 l=2 g=2; R6-R8 l=2 g=2 | 11189 | no (2 ring v. in a component) | yes, leftover 0 | leftover 0 | C, 4 edges, leftover 0 | True |
| rsst063_126o687602 | 126.687602 | 12 | 8 | `{R0-I0,R6-I0,R2-I2,R4-I2}` | [R0,R6] [R2,R4] | R0-R6 l=2 g=6; R2-R4 l=2 g=2 | 11402 | no (2 ring v. in a component) | yes, leftover 0 | leftover 0 | C, 4 edges, leftover 0 | True |
| rsst065_128o1324802 (cover) | 128.1324802 | 12 | 8 | `{R0-I5,R6-I4,R8-I4,R10-I5}` | [R0,R10] [R6,R8] | R0-R10 l=2 g=2; R6-R8 l=2 g=2 | 12492 | no (2 ring v. in a component) | yes, leftover 0 | leftover 0 | C, 4 edges, leftover 0 | True |
| rsst082_126o1551602 | 126.1551602 | 13 | 8 | `{R0-I0,R6-I0,R2-I2,R4-I2}` | [R0,R6] [R2,R4] | R0-R6 l=2 g=6; R2-R4 l=2 g=2 | 40215 | no (2 ring v. in a component) | yes, leftover 0 | leftover 0 | C, 4 edges, leftover 0 | True |
| rsst088_184o1324806 | 184.1324806 | 12 | 9 | `{R0-I5,R6-I4,R8-I4,R10-I5}` | [R0,R10] [R6,R8] | R0-R10 l=2 g=2; R6-R8 l=2 g=2 | 10048 | no (2 ring v. in a component) | yes, leftover 0 | leftover 0 | C, 4 edges, leftover 0 | True |
| rsst089_483o1324806 | 483.1324806 | 12 | 9 | `{R0-I5,R6-I4,R8-I4,R10-I5}` | [R0,R10] [R6,R8] | R0-R10 l=2 g=2; R6-R8 l=2 g=2 | 10093 | no (2 ring v. in a component) | yes, leftover 0 | leftover 0 | C, 4 edges, leftover 0 | True |
| rsst115_128o136 | 128.136 | 11 | 6 | `{I0-I3,R0-I0,R2-I0,R9-I3}` | [R0,R2,R9] | R0-R2 l=2 g=2; R0-R9 l=3 g=2; R2-R9 l=3 g=4 | 2020 | no (2 ring v. in a component) | yes, leftover 0 | leftover 0 | C, 4 edges, leftover 0 | True |
| rsst127_126o3682802 | 126.3682802 | 12 | 8 | `{R0-I0,R6-I0,R2-I2,R4-I2}` | [R0,R6] [R2,R4] | R0-R6 l=2 g=6; R2-R4 l=2 g=2 | 11121 | no (2 ring v. in a component) | yes, leftover 0 | leftover 0 | C, 4 edges, leftover 0 | True |
| rsst142_126o8168 | 126.8168 | 12 | 7 | `{I3-I4,R5-I3,R8-I4,R10-I4}` | [R5,R8,R10] | R5-R8 l=3 g=3; R5-R10 l=3 g=5; R8-R10 l=2 g=2 | 6863 | no (2 ring v. in a component) | yes, leftover 0 | leftover 0 | C, 4 edges, leftover 0 | True |
| rsst151_126o3686402 | 126.3686402 | 13 | 8 | `{R0-I0,R6-I0,R2-I2,R4-I2}` | [R0,R6] [R2,R4] | R0-R6 l=2 g=6; R2-R4 l=2 g=2 | 45099 | no (2 ring v. in a component) | yes, leftover 0 | leftover 0 | C, 4 edges, leftover 0 | True |
| rsst165_142o1324802 | 142.1324802 | 13 | 9 | `{R0-I5,R7-I4,R9-I4,R11-I5}` | [R0,R11] [R7,R9] | R0-R11 l=2 g=2; R7-R9 l=2 g=2 | 33838 | no (2 ring v. in a component) | yes, leftover 0 | leftover 0 | C, 4 edges, leftover 0 | True |
| rsst168_200o1324802 | 200.1324802 | 13 | 9 | `{R0-I5,R7-I4,R9-I4,R11-I5}` | [R0,R11] [R7,R9] | R0-R11 l=2 g=2; R7-R9 l=2 g=2 | 38602 | no (2 ring v. in a component) | yes, leftover 0 | leftover 0 | C, 4 edges, leftover 0 | True |
| rsst202_124o1324817 (cover) | 124.1324817 | 14 | 9 | `{R0-I5,R8-I4,R10-I4,R12-I5}` | [R0,R12] [R8,R10] | R0-R12 l=2 g=2; R8-R10 l=2 g=2 | 133573 | no (2 ring v. in a component) | yes, leftover 0 | leftover 0 | C, 4 edges, leftover 0 | True |
| rsst206_142o1324806 | 142.1324806 | 14 | 9 | `{R0-I5,R8-I4,R10-I4,R12-I5}` | [R0,R12] [R8,R10] | R0-R12 l=2 g=2; R8-R10 l=2 g=2 | 125583 | no (2 ring v. in a component) | yes, leftover 0 | leftover 0 | C, 4 edges, leftover 0 | True |
| rsst215_188o1324817 | 188.1324817 | 14 | 10 | `{R0-I5,R8-I4,R10-I4,R12-I5}` | [R0,R12] [R8,R10] | R0-R12 l=2 g=2; R8-R10 l=2 g=2 | 109952 | no (2 ring v. in a component) | yes, leftover 0 | leftover 0 | C, 4 edges, leftover 0 | True |
| rsst216_209o1324802 | 209.1324802 | 14 | 10 | `{R0-I5,R8-I4,R10-I4,R12-I5}` | [R0,R12] [R8,R10] | R0-R12 l=2 g=2; R8-R10 l=2 g=2 | 114213 | no (2 ring v. in a component) | yes, leftover 0 | leftover 0 | C, 4 edges, leftover 0 | True |
| rsst258_140o8406 | 140.8406 | 13 | 8 | `{I0-I2,R1-I0,R3-I2,R5-I2}` | [R1,R3,R5] | R1-R3 l=3 g=2; R1-R5 l=3 g=4; R3-R5 l=2 g=2 | 18039 | no (2 ring v. in a component) | yes, leftover 0 | leftover 0 | C, 4 edges, leftover 0 | True |
| rsst287_126o62942 | 126.62942 | 14 | 9 | `{I0-I4,I0-I2,R0-I0,R5-I2}` | [R0,R5] | R0-R5 l=3 g=5 | 84125 | no (2 ring v. in a component) | yes, leftover 0 | leftover 0 | C, 4 edges, leftover 0 | True |
| rsst329_7322o453720 | 7322.453720 | 11 | 7 | `{R0-I0,R5-I0,R7-I5,R9-I5}` | [R0,R5] [R7,R9] | R0-R5 l=2 g=5; R7-R9 l=2 g=2 | 3855 | no (2 ring v. in a component) | yes, leftover 0 | leftover 0 | C, 4 edges, leftover 0 | True |
| rsst342_7322o1324802 | 7322.1324802 | 12 | 8 | `{R0-I6,R6-I5,R8-I5,R10-I6}` | [R0,R10] [R6,R8] | R0-R10 l=2 g=2; R6-R8 l=2 g=2 | 11979 | no (2 ring v. in a component) | yes, leftover 0 | leftover 0 | C, 4 edges, leftover 0 | True |
| rsst346_7562o460920 | 7562.460920 | 12 | 8 | `{R0-I0,R6-I0,R2-I2,R4-I2}` | [R0,R6] [R2,R4] | R0-R6 l=2 g=6; R2-R4 l=2 g=2 | 12795 | no (2 ring v. in a component) | yes, leftover 0 | leftover 0 | C, 4 edges, leftover 0 | True |
| rsst356_7566o128 | 7566.128 | 12 | 7 | `{I0-I3,R6-I3,R8-I3}` | [R6,R8] | R6-R8 l=2 g=2 | 13033 | no (2 ring v. in a component) | yes, leftover 0 | leftover 0 | C, 3 edges, leftover 0 | True |
| rsst370_7562o1307280 | 7562.1307280 | 12 | 9 | `{R0-I0,R6-I0,R2-I2,R4-I2}` | [R0,R6] [R2,R4] | R0-R6 l=2 g=6; R2-R4 l=2 g=2 | 10036 | no (2 ring v. in a component) | yes, leftover 0 | leftover 0 | C, 4 edges, leftover 0 | True |
| rsst371_7562o1310580 | 7562.1310580 | 12 | 9 | `{R0-I0,R6-I0,R2-I2,R4-I2}` | [R0,R6] [R2,R4] | R0-R6 l=2 g=6; R2-R4 l=2 g=2 | 9916 | no (2 ring v. in a component) | yes, leftover 0 | leftover 0 | C, 4 edges, leftover 0 | True |
| rsst393_7566o372 | 7566.372 | 14 | 8 | `{I0-I3,R8-I3,R6-I3}` | [R6,R8] | R6-R8 l=2 g=2 | 129789 | no (2 ring v. in a component) | yes, leftover 0 | leftover 0 | C, 3 edges, leftover 0 | True |
| rsst433_8406o123 | 8406.123 | 12 | 8 | `{I0-I2,R0-I0,R2-I0,R4-I2}` | [R0,R2,R4] | R0-R2 l=2 g=2; R0-R4 l=3 g=4; R2-R4 l=3 g=2 | 4329 | no (2 ring v. in a component) | yes, leftover 0 | leftover 0 | C, 4 edges, leftover 0 | True |
| rsst439_7696o442802 | 7696.442802 | 13 | 9 | `{I0-I3,R0-I0,R9-I0,R7-I3}` | [R0,R7,R9] | R0-R7 l=3 g=6; R0-R9 l=2 g=4; R7-R9 l=3 g=2 | 14084 | no (2 ring v. in a component) | yes, leftover 0 | leftover 0 | C, 4 edges, leftover 0 | True |
| rsst461_7580o363 | 7580.363 | 12 | 8 | `{I0-I3,R6-I3,R8-I3}` | [R6,R8] | R6-R8 l=2 g=2 | 8528 | no (2 ring v. in a component) | yes, leftover 0 | leftover 0 | C, 3 edges, leftover 0 | True |
| rsst462_7587o123 | 7587.123 | 12 | 8 | `{I0-I3,R6-I3,R8-I3}` | [R6,R8] | R6-R8 l=2 g=2 | 8537 | no (2 ring v. in a component) | yes, leftover 0 | leftover 0 | C, 3 edges, leftover 0 | True |
| rsst468_8406o363 | 8406.363 | 13 | 8 | `{I0-I2,R0-I0,R2-I0,R4-I2}` | [R0,R2,R4] | R0-R2 l=2 g=2; R0-R4 l=3 g=4; R2-R4 l=3 g=2 | 14685 | no (2 ring v. in a component) | yes, leftover 0 | leftover 0 | C, 4 edges, leftover 0 | True |
| rsst469_11166o140 | 11166.140 | 13 | 8 | `{I0-I3,R6-I3,R8-I3}` | [R6,R8] | R6-R8 l=2 g=2 | 42746 | no (2 ring v. in a component) | yes, leftover 0 | leftover 0 | C, 3 edges, leftover 0 | True |
| rsst488_7877o442802 | 7877.442802 | 14 | 10 | `{I0-I2,R0-I0,R10-I0,R3-I2}` | [R0,R3,R10] | R0-R3 l=3 g=3; R0-R10 l=2 g=4; R3-R10 l=3 g=7 | 47722 | no (2 ring v. in a component) | yes, leftover 0 | leftover 0 | C, 4 edges, leftover 0 | True |
| rsst519_7322o1040 | 7322.1040 | 13 | 8 | `{I0-I4,R0-I0,R2-I0}` | [R0,R2] | R0-R2 l=2 g=2 | 30899 | no (2 ring v. in a component) | yes, leftover 0 | leftover 0 | C, 3 edges, leftover 0 | True |
| rsst544_11780o363 | 11780.363 | 13 | 9 | `{I0-I3,R7-I3,R9-I3}` | [R7,R9] | R7-R9 l=2 g=2 | 27676 | no (2 ring v. in a component) | yes, leftover 0 | leftover 0 | C, 3 edges, leftover 0 | True |
| rsst563_7566o9723 | 7566.9723 | 14 | 9 | `{I0-I3,R7-I3,R5-I3}` | [R5,R7] | R5-R7 l=2 g=2 | 77021 | no (2 ring v. in a component) | yes, leftover 0 | leftover 0 | C, 3 edges, leftover 0 | True |
| rsst574_439326o126 | 439326.126 | 12 | 7 | `{I0-I4,R6-I4,R8-I4}` | [R6,R8] | R6-R8 l=2 g=2 | 9397 | no (2 ring v. in a component) | yes, leftover 0 | leftover 0 | C, 3 edges, leftover 0 | True |
| rsst583_443166o126 | 443166.126 | 13 | 8 | `{I0-I4,R7-I4,R9-I4}` | [R7,R9] | R7-R9 l=2 g=2 | 39359 | no (2 ring v. in a component) | yes, leftover 0 | leftover 0 | C, 3 edges, leftover 0 | True |
| rsst588_453963o126 | 453963.126 | 13 | 8 | `{I0-I3,R8-I3,R6-I3}` | [R6,R8] | R6-R8 l=2 g=2 | 28062 | no (2 ring v. in a component) | yes, leftover 0 | leftover 0 | C, 3 edges, leftover 0 | True |
| rsst595_453963o364 | 453963.364 | 13 | 9 | `{I0-I3,R8-I3,R6-I3}` | [R6,R8] | R6-R8 l=2 g=2 | 25454 | no (2 ring v. in a component) | yes, leftover 0 | leftover 0 | C, 3 edges, leftover 0 | True |
| rsst600_439328o136 | 439328.136 | 13 | 8 | `{I0-I5,R0-I0,R2-I0,R11-I5}` | [R0,R2,R11] | R0-R2 l=2 g=2; R0-R11 l=3 g=2; R2-R11 l=3 g=4 | 14471 | no (2 ring v. in a component) | yes, leftover 0 | leftover 0 | C, 4 edges, leftover 0 | True |
| rsst612_453963o136 | 453963.136 | 14 | 8 | `{I0-I3,R8-I3,R6-I3}` | [R6,R8] | R6-R8 l=2 g=2 | 137874 | no (2 ring v. in a component) | yes, leftover 0 | leftover 0 | C, 3 edges, leftover 0 | True |
| rsst614_439589o122 | 439589.122 | 14 | 9 | `{I0-I3,I4-I5,R5-I3,R7-I3}` | [R5,R7] [] | R5-R7 l=2 g=2 | 93016 | no (2 ring v. in a component) | yes, leftover 0 | leftover 0 | C, 4 edges, leftover 0 | True |
| rsst624_26359326o126 | 26359326.126 | 13 | 8 | `{I0-I5,R7-I5,R9-I5}` | [R7,R9] | R7-R9 l=2 g=2 | 27408 | no (2 ring v. in a component) | yes, leftover 0 | leftover 0 | C, 3 edges, leftover 0 | True |

## Files (round9_rsstnone/)

- **`ADMISSIBILITY.md`** — this file.
- **`code/`:**
  - `kc_rn.cpp`: a kc.cpp copy with -B/-F and refusal reasons; build with `g++ -O3 -std=c++17 -o kc_rn kc_rn.cpp`.
  - `analyse_x.py`: independent components, ring pairs and local conditions, merged with the engine outputs into the TSV.
  - `chkx.py`: unavoidable.conf against rsst_x.txt and the headers.
  - `run_cfast.sh`, `run51.sh`: the drivers.
- **`inputs/`:**
  - the cover 4 and the 51: `cover4.txt`, `cover4_x.txt`, `cover4_kcx.txt`, `none51.ids`, `none51.txt`, `none51_x.txt`,
    `none51_kcx.txt`;
  - `*_x.txt` is `name {X}`; `*_kcx.txt` is the same in kc's `-x` format.
- **`results/`:** `kc_cons_cover4.out` (A3 kc -x), `kc_rn_cover4.out`, `kc_rn_none51.out` (three blocks: conservative,
  -B, -F), `cfast_cover4.out`, `cfast_none51.out`, `cover4.tsv`, `none51.tsv`, `chkx.out`.

**Reproduce:**
```
python3 -I -B code/analyse_x.py inputs/none51.txt inputs/none51_x.txt results/kc_rn_none51.out results/cfast_none51.out none51.tsv
```

## RSST-NONE2: the 51 against Gonthier's `valid_contract`, from the source text (W6b, 10 Nov 2026)

**Sources.** `fourcolor_src/` holds math-comp/fourcolor master, fetched by the lead (see SOURCE.txt); `md5sum -c MD5SUMS`
passes. The definitions and theorems used:
- `coloring.v`: `sparse` :444, `sparse_cons` :446, `triad` :458, `valid_contract` :462;
- `contract.v`: `contract_ring` :25, `sparse_contract_ring` :46, `contract_ring_max` :150, `contract3_valid` :173,
  `triad_valid` :183, `contract_coloring` :249;
- `birkhoff.v`: `Birkhoff` :345;
- `embed.v`: `embed_valid_contract` :1377.

**Definitions missing from the supplied files.** `insertE`, `kernel`, `fband`, `adj`, `rlink`, `cnode`, `simple`/`permF`
and the hypermap axiom are defined in `hypermap.v`/`geometry.v`, which `coloring.v` imports but which were not supplied.
I could not ask for them: this role has no message channel. What I used, and the evidence for each:

| Object | Meaning used | Evidence in the supplied files | Effect on the result |
|---|---|---|---|
| `insertE p` | the list x, edge x for each x in p | `mem_insertE plainG : (x \in insertE p) = has (cedge x) p`, used with `plain_orbit` at contract.v:153-155 and cfcontract.v:191/226/241/274 | none: no X here repeats an edge, so only membership matters |
| `kernel r` | `predC (fband r)`, the darts on faces that hold no ring dart, i.e. the interior regions | `kernel_off_ring`, `kernelF`, `adj_kernel_min` (embed.v:42-43, 739); "kernel faces" (birkhoff.v:23-28) | none: every triad found lies on an interior region, and no config has a triad only outside the kernel (`triad_any_dart` column) |
| `adj x y` | some z in face x has `edge z` in face y | `adjP` as used in `at_radius2P` (coloring.v:399-405) | — |
| `sparse` | no two darts of p in one node orbit | `sparse_cons` (coloring.v:446), stated in the file | — |
| hypermap axiom | `node (face (edge x)) = x` | not in the files; checked instead that the node orbits come out as the facial triangles | — |

### Gonthier's objects in kc/RSST terms

Gonthier's configuration map is the cubic dual of RSST's free completion, closed off by one outer node.
`src/vc_check.py` builds it explicitly from the rotations in `unavoidable.conf`:

| Gonthier (hypermap) | kc / RSST |
|---|---|
| dart | an oriented edge u>w of the free completion (2 per edge, ring edges included); its face is u |
| `edge` orbit {u>w, w>u} | the edge uw. An E-link joins the faces u and w, so a colouring gives adjacent regions different colours. |
| `face` orbit (arity = order) | a region, i.e. a vertex: ring faces are R0..R(r-1) (RSST 1..r), kernel faces are I0..I(m-1) (RSST r+1..n); arity = degree in the free completion |
| `node` orbit | a facial triangle of the free completion (cubic node), plus one outer node of order r |
| ring `r` (`scycle rlink`) | the darts R0>R1, R1>R2, …: one dart per ring face; it is the outer node |
| `kernel r` | the darts of the interior regions I0..I(m-1) |
| `cc` (a transversal) | one dart per contracted edge; `size cc` = \|X\| |
| `insertE cc` | both darts of every X edge; its faces are exactly the endpoints of X |
| contract colouring (`cc_coloring`) | the endpoints of each X edge get one colour, which is identifying them as X does |

The four conjuncts in kc terms:
- **off-ring** `[disjoint r & insertE cc]`: no X edge is a ring edge Ri-Ri+1. Ring-interior edges are allowed, and
  nothing limits how many ring vertices one X-component holds.
- **sparse** `sparse (insertE cc)`: no node holds two contract darts. Equivalently, no facial triangle of the free
  completion (ring triangles included) contains two X edges, and no X edge appears twice.
- **size** `pred4 1 2 3 4 (size cc)`: 1 ≤ \|X\| ≤ 4.
- **triad** (\|X\| = 4) `~~ [disjoint kernel r & triad (insertE cc)]`: some interior vertex v has at least 3 neighbours
  among the X endpoints, and v is not adjacent to every X endpoint.
  - The count runs over v's darts, so over v's neighbours. Ring endpoints count.
  - The second part holds automatically when v is itself an endpoint, because no region is adjacent to itself.

### Check, conjunct by conjunct (`src/vc_check.py`, `results/vc_none51.tsv`, `results/vc_all633.tsv`)

**Checks on the map.** For every configuration the built map passes:
- `node (face (edge x)) = x`, and `edge` is an involution without fixed points;
- genus 0 (edge + node + face orbits = darts + 2);
- the node orbits are the facial triangles plus one outer node of order r;
- the ring is a simple rlink cycle and is the outer node.

The conjuncts are then evaluated as the definitions read: `sparse` by the `sparse_cons` recursion, `triad` by its
definition with `adjP`'s `adj`.

| On the 51 "none" X | result |
|---|---|
| off-ring | 51/51 |
| sparse | 51/51 |
| size in 1..4 | 51/51 (37 with \|X\| = 4, 14 with \|X\| = 3) |
| triad in the kernel (\|X\| = 4) | 37/37 |
| **`valid_contract`, verbatim** | **51/51** |
| our Lean `admissibleX` on the same X | 0/51: all fail the ring-distinct conjunct; local loop-freeness holds for 51/51 |

- **Agreement with last round.** The result agrees with last round's `analyse_x.py` (triad list, sparse, local
  verdict) on 51/51.
- **Translation check on all 633.** All 384 RSST contracts in unavoidable.conf (633 minus the 249 D configurations) are
  `valid_contract`. This is what Gonthier's development checks for these configurations, so the translation passes. I
  have not compared his encodings with RSST's file, so this is a consistency check, not a proof of equivalence.
- **The 77 ring-merging contracts.** `admissibleX` fails on 77 of the 384 RSST contracts, always on the ring-distinct
  conjunct: 51 "none" plus 26 that round 44 closed with another, conservative X. It holds on the other 307. No RSST
  contract passes `admissibleX` and fails `valid_contract`.

### Is our Lean `admissibleX` strictly stronger than `valid_contract`?

No. Neither implies the other.

**Where `admissibleX` is stronger:**
1. **Distinct ring labels**, i.e. at most one ring vertex per X-component. `valid_contract` has nothing like it. This is
   the only point on which the 51 (and the 77) fail.
2. **Local loop-freeness.** Every listed edge outside X must join different X-components. This is stronger than sparse.
   - It implies sparse. In a triangle with two X edges, the third edge is either a listed edge, which is a loop, or a
     ring edge Ri-Ri+1, which the ring-distinct conjunct refuses.
   - It also refuses shapes that sparse allows, for example an X-path a-b-c-d closed by a configuration edge a-d.
   - Duplicate pairs in eqR/eqI are not rejected by `admissibleX`, but are by `sparse`. Deduplicating when building cc
     removes the difference.

**Where `admissibleX` is weaker:**
- **No triad at \|X\| = 4.** CGlue replaces it with `XRingSimple` plus the label argument (docstring at CGlue.lean:365-374),
  so a 4-edge X without a triad can pass `admissibleX`.
- None of the RSST contracts is such a case.
- I did not check whether the registry's 4-edge entries all have triads. cfast enforces the triad unless run with
  `--nogonthier`.
- **`CGlueU.admissibleXU`** also drops \|X\| ≤ 4.

**So:** `admissibleX` plus the triad implies `valid_contract`, modulo deduplication. Off-ring holds because X uses only
listed edges, each with an interior end; sparse holds as shown above.

### What a Lean port of `valid_contract` as the admissibility target would need

**What Gonthier proves.**
- `contract_coloring` (contract.v:249): in a minimal counterexample G, `valid_contract r cc -> cc_colorable cc`.
- It has two halves:
  1. no **contract ring** exists (contract.v:25: a simple rlink cycle all of whose darts but the first are contract darts,
     i.e. a cycle closed by one uncontracted edge, which contraction would turn into a loop);
  2. an induction that contracts one edge at a time and uses minimality.
- Half 1 uses these lemmas:
  - `contract_ring_max`: size ≤ \|cc\| + 1;
  - `sparse_contract_ring`: every contract ring has a face strictly on each side (`nontrivial_ring 0`), from sparse alone;
  - `Birkhoff` (birkhoff.v:345): in a minimal counterexample a ring of size ≤ 5 is trivial, and a 5-ring has a single
    face on one side;
  - `contract3_valid`: \|cc\| ≤ 3 gives ring size ≤ 4, which contradicts Birkhoff;
  - `triad_valid`: \|cc\| = 4 gives a 5-ring with one face on a side, and the triad contradicts that.
- `embed_valid_contract` (embed.v:1377) lifts validity from the configuration to its image in the minimal counterexample,
  as `valid_contract [::] ccr`. The ring condition becomes moot.

| Piece | Our counterpart | What is needed |
|---|---|---|
| per-key `validContract cf eqR eqI` (decide) | `admissibleX` | Write it. Off-ring is free (listed edges only), with size, triad and sparse. Sparse needs the configuration's facial triangles. Graph triangles are a sound superset: graph-sparse implies facial-sparse. |
| `Birkhoff` (sizes 3, 4, 5) | `NoShortSepCycle` (ClaimGlue.lean:64) and `MinimalCounterexample.noShortSep` (:88) | Nothing new for the length-5 case. The definition covers cycles of length 3..5, with `BothSides2` (two on each side) at length 5. Its docstring reads "no separating 5-cycle other than one around a single vertex". So the worry that "our noShortSep only covers length ≤ 4" does not hold. **Not checked:** that `BothSides2` matches `nontrivial_ring 1` exactly (faces of the cubic map are vertices of T, so the objects agree). |
| `contract_ring` | none | Define it on `SphericalMap`: a cycle of T all of whose edges but one are X edges, under the occurrence. |
| `contract_ring_max` | none | A short graph lemma: a path inside an X-component uses at most \|X\| edges. |
| `sparse_contract_ring` (contract.v:46-149, ~100 lines Coq) | partly `apex_sides`/`CycPotential` (CGlue.lean:916) | The main planar lemma: a contract cycle has a vertex strictly on each side, from sparse. |
| `contract3_valid`, `triad_valid` (contract.v:173-247, ~75 lines) | none | Port them on top of `noShortSep`. |
| `embed_valid_contract` (embed.v:1377-1401, 25 lines, on top of embed.v's morphism) | `ConfigOccW`, `OccExact`, `NbrInj`, `ApexFacts` | Lift sparse and the triad to T. The faces at an X edge (which has an interior end) are configuration faces. The triad vertex is interior, so its T-neighbours are exactly its listed ones (true degree, `NbrInj`). |
| `contract_coloring` induction (contract.v:249-428) | C4a `contract_subgraph_gen` and C4b `XLoopFree` | Not needed. C4a already contracts any subgraph; the no-contract-ring lemma would supply C4b's G-edge conjunct in place of the ring-label argument. |
| hC (`cReducible18`/`extCAux`) | unchanged | Nothing: `extCAux` already identifies ring colours through eqR. |
| `XRingSimple`, `foldSafeX` | today's fold handling | In Gonthier's route the loop argument runs in the big map, so folds of touched ring positions do not affect it. **Not checked:** whether the rest of CGlue (`xLabel` well-definedness) can drop `XRingSimple`. |

- **Coq sizes.** The line counts above are measured from the files.
- **Not estimated:** the size of a Lean port.

### The two weak spots flagged in our chord argument

**1. "The short cycle might bound only faces."**
- Moot under Gonthier's route. `sparse_contract_ring` derives a face strictly on each side of any contract ring from
  sparsity alone, before Birkhoff is used. A cycle with nothing but triangles on one side is exactly what sparse excludes.
- Our argument instead took a vertex on each side from the two ring arcs, in the disc picture. That needs the
  configuration ring unfolded. Gonthier's does not use the configuration ring at all (`valid_contract [::] ccr`).

**2. \|X\| = 4.**
- Moot under Gonthier's route. Contract rings of size 5 are handled by `Birkhoff` at size 5 together with the triad
  (`triad_valid`).
- Our argument covered only X-path length ≤ 3 (cycles ≤ 4). That is enough for the 51 but not general.

**Caveat.** Both are moot only once the pieces in the table above are ported: `sparse_contract_ring`, `triad_valid`, and
the lift. Until then they stay open for a Lean proof.

**Verified here:**
- the 51, and all 384 RSST contracts, against the four conjuncts on an explicitly built hypermap;
- the hypermap checks;
- agreement with last round;
- the `admissibleX` comparison on RSST data;
- the source-text citations above.

**Not verified:**
- the text of `insertE`, `kernel`, `adj` and the hypermap axiom (files not supplied; evidence in the table above);
- Gonthier's own encodings of these configurations, and his contract indices;
- `BothSides2` matching `nontrivial_ring 1`;
- the registry's 4-edge entries for triads;
- any Lean.

Files added: `code/vc_check.py`; `results/vc_none51.tsv` (the per-configuration TSV for the 51); `results/vc_none51.out`;
`results/vc_all633.tsv`; `results/vc_all633.out`.

Reproduce:
```
python3 -I -B code/vc_check.py unavoidable.conf inputs/none51.ids vc_none51.tsv
```
Pass `-` in place of the ids file for all 633.
