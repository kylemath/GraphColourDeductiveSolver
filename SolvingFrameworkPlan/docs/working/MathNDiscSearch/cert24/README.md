# Order-24 discs where (G*) fails (certificates)

Four locked discs from the N=24 search, one per file (`bad_24_<part>_<line>.txt`: part p0/p1/p3 and the line of `res2_24_<part>.txt` it came from). In each, one Case I neighbour reaches the third state in the locked branch (u1 not joined to u3 or u4 in [alpha,gamma]_3, chain {D,beta} intact), so the candidate fact (G*) fails there. (N) still holds on each disc.

Re-verify the disc itself, independently of the tester: `python3 ../recheck.py -f bad_24_p0_8.txt` (prints "N HOLDS" with both neighbours separable). The Case I / (G*) predicate was computed by the worker's scratch scripts, which were not saved (the shared helper is `../../MathNCaseI-scripts/tn_lib.py`; the Ia/Ib scripts are in `../../MathNIaIb-scripts/`). So the `recheck.py` output certifies the discs, not the (G*) failure itself; the audit would need to re-derive that predicate from the definition in `docs/working/MathNGstar.md`. [computed, exploratory, post hoc]
