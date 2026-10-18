# Review of Studio's rule T option F spec (out/job30f/SPEC.md, d6b647a9): sender-letter kill filter

18 Oct 2026, 12:05-12:25Z. Scripts: flip.py, mk.py, iso.py; data kp.txt, flip_check.out.

**Verdict: sound with conditions C1-C5.** No counterexample for the current 11 configurations, but one real gap in
how the matcher defines "embeds" (C1).

**Key point [hand].** A sub-row has the same inequality as its parent (Y and T do not read the new letters), so
splitting changes the LP only when every sub-row of a row is deleted. In effect a row is deleted only if every
filling of its read slots (5..9, 9 = degree >= 9) contains K on lettered vertices. Sound because every real five
falls into exactly one sub-row (min degree 5; >= 9 maps to 9) and second-ring letters do not change the 2-ball's shape.

**(a) No extra edges at distance 2: justified** [hand; README §3 step 1, rechecked for any link degrees, two bigs
included; the z's are second-ring t's]. A link chord gives a separating triangle. A second-ring vertex next to
non-consecutive link vertices gives a separating 4-cycle, which also rules out two slots being one vertex (z_a = z_e,
t_k = t_j). A second-ring chord gives a separating triangle, 4-cycle or non-trivial 5-cycle. README fix: its "s_k is
inside" the 5-cycle fails when y = t_k; a degree count closes it (x_{k+1} has degree >= 5 and at most 4 neighbours on
the cycle, so that side has >= 2 vertices). Every triangle in the 2-ball is a face.

**(b) Split depth <= |K|: no wrong deletion, only lost strength** [hand]. The cap can cut off kills, since different
fillings can die to different K or embeddings reading different slots, whose union can exceed |K|. Splitting always
terminates (at most 20 second-ring slots with exact link letters). Recommend dropping the cap: full product of 5..9
over the union of read slots.

**(c) Privates of a 9 left unsplit: sound** [hand]. Keeping a row is conservative; with a 9 the model states only true
facts (t_{k-1}, t_k distinct and non-adjacent; the 9 is never an interior image).

**Gap [E].** The spec's test (exact degrees, induced, triangles onto faces) is weaker than RSST's "appears" when K's
interior has a cut vertex: one block can be reflected alone, giving K' that still passes. grow.py avoided this by
re-cutting each image and verdicting the cut; F reuses those verdicts but re-embeds with the weaker test. All 24 cut
lines scanned: only 3.3700806 (rsst062, interior vertex 1) has an interior cut vertex; its flip K' is not isomorphic
to K or its mirror, and K' is C-reducible with the same X = {I2-I6} (kc -C C-REDUCIBLE; cfast --fixed leftover 0).
So nothing is wrongly deleted today. The other 10 have 2-connected interiors; all interior degrees <= 7, so a 9 is
never used as exact.

**Conditions.**
- C1 (required): the kill test and the §4 networkx check must check rotation (cyclic order plus ring-gap counts) at
  every interior vertex, up to one global mirror; or re-cut each image and verdict it as grow.py does; or accept only
  K with a 2-connected interior.
- C2: assert in code that no K interior vertex maps onto a vertex lettered 9 (link or z).
- C3: delete a row only when all its fillings over 5..9 are killed; drop the |K| cap (or report rows it cuts off).
- C4: reflection self-check (same class as the tcount side bug): a deletion must not change when the whole row is
  reflected (word, z_a <-> z_e, side, read-slot letters with each private order reversed); when q is a read slot the
  coupling filter must use that sub-row's exact q.
- C5 [I]: 122.1031's X has a ring-interior edge (R8-I3, or R6-I2 mirrored); its admissibility rests on the inherited
  RSST free-completion / ring-injectivity argument, the registry's existing "C cons." standard, not new to F.

## Check of Studio's built filter (bd8472d9, out/job30f/deleted_rows.txt), 12:50Z [E]

Own model and matcher (`M_deleted_rows/`; only wlp.py's registry reused, not Studio's filter): exact degrees, induced,
triangles onto faces, rotation at every interior vertex up to one global mirror, no interior vertex on a 9.
- **All 163 deletions confirmed**: every filling of each row's read slots over 5..9 contains a K. All 163 are killed
  by one configuration, k42_rsst025_xxxxxxx5 (ring 9, 5 interior). R5/R6 "cannot occur" never needed.
- Own enumeration gives 19,626 sender rows; all 163 are among them.
- Deleted set closed under every dihedral map fixing the word (z_a <-> z_e, side swapped): 0 failures.
- C1: on the 10 configurations with 2-connected interiors the rotation check never rejected an embedding that passed
  degrees/induced/triangles (9,302 embeddings on 3,000 rows); it does reject on rsst062. So 2-connected-only suffices.
- Completeness: 200 random kept rows (seed 1), 0 that should have been deleted; the full pass over 19,463 kept rows
  did not finish in 30 minutes.
