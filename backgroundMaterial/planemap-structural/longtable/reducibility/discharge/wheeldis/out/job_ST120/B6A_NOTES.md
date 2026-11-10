# ST-120 B6a: what an occurrence needs, and what B6 must build (reading only, 10 Nov ~16:00Z)

Sources [read]: `dcheck/DCheckOccWalk.lean:18` (ConfigOccW), `dcheck/ClaimGlue.lean:102` (OccursW),
`dcheck/CGlue.lean:1459` (OccursCXF), `dcheck/COccBridge.lean` (RotOcc, rotOK, RotOcc.occExact / nbrInj / apexFacts,
occursCXF_of_rot), and the per-entry glue `out/job_HCK5P17/lean/{HK5P17_00, COccHK5P17_00}.lean`.

## 1. What `OccursW` / `OccursCXF` require

- **`ConfigOccW T G r m ρ ι intAdj ringAdj`:**
  - `ι` is injective;
  - `ρ t ≠ ι a`;
  - G is T minus the interior (`hG`);
  - **`nbr`**: every T-neighbour of a host is a listed interior neighbour or a listed ring slot;
  - **`ring : FaceWalk G r ρ`**: distinct darts, vertices may repeat (folds and pinches).
- **`OccursCXF`** adds three facts. All three are derived **generically** from `RotOcc` + `rotOK` (COccBridge:112-190):
  - `OccExact`
  - `NbrInj`
  - `ApexFacts`
- **Answer to review note 3 (ring-3 images):** occurrence needs only **host-level** data.
  - `RotOcc` gives the exact degree of each host and the rotation of T at each host. In it, ring slots are indices into ρ.
  - ρ itself is the face walk of G around the hole, determined by the host rotations and the faces.
  - So K's ring image may sit on ring 3, where B3 says nothing, at no cost. Nothing about ring-3 vertices is needed beyond
    their being where the host rotations say.
  - The hosts need exact degrees. In the window, hosts have exact letters 5–8, and a 9+ middle is never a host (spec §6).
- **Gap counts at cut and pendant hosts:**
  - `RotOcc.deg` requires deg T (ι a) = length (rot a), so every slot of a host's rotation is listed, ring slots included.
  - `rotOK` checks the slot list against the config: listed neighbours, plus `slotTri` (a ring slot just before an interior
    slot b is a ring neighbour of b).
  - At cut and pendant hosts, the number of consecutive ring slots is exactly the config's gap. B6 must read it off the
    window rotation (B4 note 1, orientation coherence), not off adjacency alone.
- **Mirrors:** the glue proves `colorable_of_mirror_occ_*` by applying the same entry to `T.mirror`. That needs only
  `mirror_triangulated`.
  - B6 must therefore produce `Occ` for T or for T.mirror, by chirality: a window match read cw vs ccw.
  - No separate mirror proof per config is needed, but B3/B4 must be available for `T.mirror`. B3 needs `Internally6`
    of `T.mirror`; a mirror-invariance lemma for each Internally6 field is [inf] about 1 pd.

## 2. What exists versus what B6 must build

| step | today | for B6 |
|---|---|---|
| window match ⇒ `Occ` / `RotOcc` (host rotations as `Nx` facts) | per entry, generated (`rotOcc_of_occ`, ~110 lines each) | **generic**: from B3/B4's iso and a K-embedding into the drawn window |
| `RotOcc` + `rotOK` ⇒ OccExact / NbrInj / ApexFacts | **generic** (COccBridge) | reuse |
| `Occ` ⇒ `ConfigOccW` (build G, ring face walk, darts distinct) | per entry, generated (`configOcc`, ~600 of HK_00's ~1,350 lines) | **generic** `configOccW_of_rotOcc`: the main new theorem |
| `OccursW` / `OccursCXF` ⇒ colourable | generic (`colorable_of_occ_*`, `DEntry`, `CEntryF`) | reuse |
| mirror | `T.mirror` + `mirror_triangulated` | add `Internally6` mirror invariance |

**B6 estimate stays at 6–10 pd [inf].** The core is a generic `configOccW_of_rotOcc` that replaces 582 copies of generated
`configOcc`. Its proof pattern exists 20+ times in generated form, which lowers the risk. OccToRing.lean's `iterate_chain`,
`nbr_of_chain` and `RingFace.mk_lt` are the generic helpers it rests on.
