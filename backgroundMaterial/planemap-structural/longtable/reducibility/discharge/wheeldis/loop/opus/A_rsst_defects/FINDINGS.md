# A_rsst_defects: do the H7 defects contain an RSST unavoidable configuration?

Question: does each H7 defect patch (D1, D2, D3, E1, E2, K4 survivors; net charge +1 in a 6-sea) contain one of RSST's 633 configurations, with every image interior vertex's full neighbourhood inside the patch?
Guess: YES for every defect (RSST's discharging says any positive vertex in an int. 6-connected triangulation has a reducible config within distance 2); most likely hits are small C/D configs near the 5-5/5-7 clusters.
What would change the plan: YES for all -> admitting RSST configs into R kills the H7 obstruction (next step: LP with R_opt+RSST). NO for some -> either that patch is not int. 6-connected (excluded anyway) or RSST's local step fails; either way the "add RSST" link would be insufficient by itself.

## Result (18 Oct 2026, ~35 min wall, 1 core)

**Answer: YES, loudly. Every defect contains RSST configurations, D-reducible ones included, at rings 10-11.** [E]

Method [E]. `rsst_in_defect.py` builds each patch exactly as `defect_verify.py` does (b8b/rings.py Layered from the
full signature in `out/defect_K4_survivors.txt`, plus 6 all-6 sea rings). The outer ring's degree is set to -1, so
every image vertex has its full neighbourhood and exact degree in the patch. Containment is the
`studiointel/rsst_contain.py` notion: an injective map of the interior vertices, exact degrees, induced, every
configuration face onto a patch face. Every embedding is enumerated and deduplicated by image set. D means
k_contract = 0 in the conf file (249 of them), C means k_contract > 0 (384). Only 323 of the 633 have every interior
degree in {5,6,7}, so only those can occur.

Controls [E].
- Icosahedron (positive): only #0 (the Birkhoff diamond) hits, with 30 embeddings, one per edge. That is correct:
  2.122 needs a 6.
- Lone 5 in a 6-sea, `5|66666|...` (positive): only #20 hits, 5 embeddings. #20 is a 6 with link 566666, ring 11, D.
- Pure 6-sea (negative): 0 hits.
- Diamond (#0) and 2.122 (#1) never hit any defect, which agrees with `defect_verify`.

Per defect [E] (full lists in `survivors_summary.txt`, raw output in `survivors.jsonl`; dY = the image's maximum
distance from the cluster Y):

| defect | Y (5s/7s) | RSST hits | D | C | smallest D hits |
|---|---|---|---|---|---|
| D1 | 10/9 | 25 | 11 | 14 | #12 r10 (two 5s, four 6s), #17, #52, #104, #201 r11 |
| D2 | 11/10 | 21 | 6 | 15 | #8, #9 r10 (four 5s, three 6s), #201 r11 |
| D3 | 11/10 | 15 | 7 | 8 | **#110 r10: four 5s and two 7s, entirely inside Y**; #81, #120 r11; #246 r12 (five 5s, three 7s, inside Y) |
| E2 | 10/9 | 21 | 11 | 10 | #12 r10, #17, #52, #104, #201 r11 |
| E1 | 9/8 | 20 | 11 | 9 | #12 r10, #17, #52, #104, #201 r11 |

- Every hit has dY ≤ 2, i.e. it lies in the second neighbourhood of the cluster, as RSST's theorem predicts. Most have
  dY = 1: the cluster's 5s together with the 6s next to them. Few involve two 7s; the binding receivers of H7 are
  not needed.
- Engine cross-check [E], independent of the RSST file's claims. Each hit was re-extracted from the patch as it sits:
  interior = the image, ring = its neighbours (`extract_hits.py`). 109 had a simple induced ring at RSST's ring size;
  13 have a pinched or chorded ring in G and were not engine-tested.
  - All **50/50 D hits are D by the programme's own `dfast`** (`hits_D.dfast.out`, rings 10-14, at most 10 s each).
  - All **59/59 C hits are cfast C-candidates** with |X| ≤ 4 (`hits_C.cfast.out`; local admissibility only, as
    always with cfast).
- Sample beyond the five survivors [E] (`sample_sigs.txt`, `sample.jsonl`; seed 20261018). All 153 K=3 candidates
  and 300 random K=4 candidates (out of 418,551) were tested. **453/453 contain at least one RSST D configuration.**
  The smallest D hit has ring 8 in 279 of them, 9 in 122, 10 in 30 and 11 in 22. The median number of hits is 8 (K3)
  and 19 (K4).

Internal 6-connectivity was not re-checked: no defect came out empty, and `defect_verify` already found no separating
3-, 4- or nontrivial 5-cycles within distance 3 of Y.

## Reading [I]
- The H7 obstruction is an artefact of R_opt's shape (wheels plus single-7 receiver-centred configurations), not of
  reducibility. Every defect contains small D-reducible configurations at rings 10-11 that R_opt simply does not
  include. Examples are #12 (two 5s at distance 2 with four 6s) and #110 (two adjacent 7s with four 5s). The
  programme's own dfast certifies them in seconds, and the RSST D set is already Lean-checked in `dcheck/`, so
  admitting it costs no new compute.
- Plan change: put the 249 RSST D configurations (and the 384 C ones, which need the global contraction
  conditions) into R, then re-run the K≥2 LP / defect search against R_opt ∪ RSST_D.
  - Every K3/K4 defect candidate sampled is already killed by RSST_D alone.
  - Caveat: killing these defects does not by itself close the LP. Closing it with the programme's own rules still
    needs a rule class that "sees" these configurations (radius ≤ 2 from a 5). RSST's own rules do, and they are the
    known closing link.
