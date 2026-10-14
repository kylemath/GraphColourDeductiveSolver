# Hole wheels: is "hole + its 5 neighbours" D-reducible? (exploratory, 14 Oct 2026)

The question (Kyle): can the frustration at a degree-5 hole always be fixed by Kempe chains coming in from
outside, over the infinite family of all graphs containing that neighbourhood?
- That is exactly Birkhoff–Heesch **D-reducibility** of the configuration.
- The outside acts only through non-crossing Kempe-chain patterns on the ring (finitely many, by planarity).

**The configuration.**
- The hole v (degree 5) and its neighbours x_0..x_4, with the stated degrees.
- The ring is the neighbours' outer neighbours: length Σd − 20.
- Checked with `../dred.py`, the same closure that matched RSST on all ring-≤9 configurations.
- Script: `wheels.py`; output: `wheels-out.txt`.

| word | ring | ring colourings | extend directly | fixable against every outside | verdict |
|---|---|---|---|---|---|
| 55555 | 5 | 10 | 10 | 10 | D-reducible |
| 55556 | 6 | 31 | 22 | 31 | D-reducible |
| 55566 | 7 | 91 | 47 | 91 | D-reducible (contains a Birkhoff diamond) |
| 55656 | 7 | 91 | 52 | 91 | D-reducible (contains RSST 2.122) |
| 55666 | 8 | 274 | 104 | 274 | D-reducible = **RSST 0.79077722** (r=8, ext 104) |
| 56566 | 8 | 274 | 118 | 274 | D-reducible |
| 56666 | 9 | 820 | 257 | 820 | D-reducible = **RSST 0.79077962** (r=9, ext 257) |
| **66666** | 10 | 2461 | 530 | **1241** | **not D-reducible** |
| 55557 | 7 | 91 | 47 | 91 | D-reducible |
| 55567 | 8 | 274 | 100 | 274 | D-reducible |
| **66667** | 11 | 7381 | 1128 | **1893** | **not D-reducible** |

**Cross-check.** The two RSST matches agree exactly in ring size, interior size (6) and extendable count with
RSST's own data (`../rsst_scan_r9.txt`).

**Reading.**
- Every wheel tested *here* with at least one degree-5 neighbour is D-reducible. **CORRECTED 14 Oct (see below): this holds only for small wheels.** The outside can never lock such a hole
  in a minimal counterexample.
- The all-≥6 wheels 66666 and 66667 are **not**. There, some outside chain pattern defeats every Kempe repair
  of the first ring. This is the computation behind Fable's "66666 is the wall" and the old σ-exit
  observation that "every lemma needs three consecutive 5s".

**Next.**
- Run the same wheel test over all 59 Track B hole types, using the Lean `DCheck` for rings 10–14.
- Then grow the 66666 neighbourhood by a second ring (rings of about 15–20, which needs the Lean checker or the
  Studio) to see whether any 2-ball completion is reducible.

## Correction (14 Oct 2026, Studio Job 8, in progress)

**The run.**
- 154 wheels: the Track B hole types plus every census-33 hole word, up to symmetry, with 8+ instantiated as 8 and 9.
- Rings 5–16.
- Checked with a Lean executable (`dcheck/WheelMain.lean`) that reproduces the table above exactly.

**Results.**
- **D-reducible:** only the small wheels: those above, 55556, and 56657 (ring 9).
- **Not D-reducible:** most wheels *with* a degree-5 neighbour. Examples:
  - 55668 (ring 10: 856 of 2,461 ring colourings fixable);
  - 56676;
  - 55687, 55759, 56659 (ring 11: 2,826 of 7,381), 56677, 57577;
  - every ring-12 to ring-15 wheel tested so far.

**Revised reading.**
- The first ring around a hole is reducible only when the neighbour-degree sum is small (roughly Σw ≤ 29).
- Elsewhere the outside can defeat every Kempe repair of the first ring. Larger configurations are needed, which is consistent with RSST's list going up to ring 14.
- The earlier "every wheel with a 5-neighbour" generalised from too few cases. This is another instance of the falsification-first rule.
