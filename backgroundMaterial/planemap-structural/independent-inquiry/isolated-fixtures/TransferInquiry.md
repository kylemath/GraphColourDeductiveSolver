# Width-five transfer: compression and genuinely independent interior switches

Only ring tuples were enumerated: 240 proper named colourings of C5, ten up to global colour permutation. Adjacent rings a,b are compatible exactly when b[j] differs from both a[j] and a[j+1]. The ten-pattern quotient transition graph has one strongly connected component, directed diameter three, and a self-loop at every pattern. Exact transitions are in transfer.json. Each quotient walk lifts to named colourings by transporting the next-ring witness with the palette permutation identifying its source. Independently prescribed named colours at both ends require an additional palette-holonomy check; quotient connectivity alone does not supply that.

For arbitrary cylinder length, take initial ring (0,1,0,1,2) and obtain each succeeding ring by palette permutation π=(0→2,1→3,2→1,3→0). The next ring is (2,3,2,3,1), which satisfies all diagonal inequalities. Applying the same permutation preserves compatibility, so this repeats with period four and works for every number of rings. Every ring uses three colours; cap each end by its missing colour. This is a direct linear-time constructive colouring of the whole capped-cylinder family, with no odd/even obstruction. It proves existence for this family, not recolouring reachability from an arbitrary deletion colouring.

## An actual independent-switch mechanism

Use the named period-three layer motif:

A=(0,1,0,2,3), B=(3,2,1,0,1), C=(1,3,2,3,0).

The compatibility inequalities directly verify A→B→C→A. At column 4 of each B layer the vertex has colour 1. Its six neighbours are:

- same layer, columns 3 and 0: colours 0 and 3;
- previous A layer, columns 4 and 0: colours 3 and 0;
- next C layer, columns 4 and 3: colours 0 and 3.

Consequently that vertex is an isolated component in the {1,2}-induced graph. Changing it from 1 to 2 is a legal single-component Kempe swap. These vertices in distinct B layers are nonadjacent, and no swap changes any of the six neighbours of another such vertex. All k switches commute and remain available after every subset of earlier switches. They give 2^k distinct proper named colourings.

The motif closes into a genuine capped sphere with fixed end colours. Use prefix rings (0,1,0,1,2), (2,3,2,3,1), then k copies of A,B,C, then suffix (0,1,0,1,2). All joins satisfy the inequalities; both cap hubs get colour 3. There are m=3k+3 rings and n=15k+17 vertices. The graph still has exactly twelve degree-five vertices, all others degree six. Every switched vertex is interior and both cap boundaries remain fixed. The associated {1,2} components meeting the cap boundary remain unchanged because these are isolated interior components.

This supplies unbounded independent interior switches with fixed curvature budget and fixed cap boundary colours. Root symmetry is unnecessary. It does **not** establish that the states are traps, produce breadcrumb warnings, or preserve connectivity of the other five colour pairs. Indeed the cap boundaries already use three colours, so at a cap hub these are already extension targets. Turning this construction into an obstruction to a warning charge would require coupling the independent switches to a locked cap or proving that a proposed observation ignores every relevant effect.

An important opportunity runs in the opposite direction: because the corridor has fixed width, proper-colouring extension admits a finite transfer description. A corridor compression theorem might retain palette transport plus the six bichromatic boundary partitions and prove that irrelevant isolated switches can be discarded. Transfer of proper colourings alone is easier than transfer of Kempe reachability, because the latter must preserve components crossing many layers. The independent-switch motif tells us precisely which extra freedom such a theorem must handle.

Files: transfer.py, transfer.json, local_switch.py, independent-switch-motif.json. No full F32/F42 colouring census, producer experiment, or external-team message was performed.
