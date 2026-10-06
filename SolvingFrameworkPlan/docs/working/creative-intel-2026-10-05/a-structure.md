# A-Structure: the stacked-antiprism family A_r and its infinite doubly-locked F-orbits

Team A-Structure (Long Table, Creative Intel), 6 October 2026. Exploratory. Labels: [hand] = every step written out here; [computed] = exact finite computation by the named script; [lead]; [conjecture]. No git add/commit. CPU: single process at a time, longest run 95 s (r = 7, 8 census), orders <= 42.

Scripts (all `backgroundMaterial/planemap-structural/longtable/explore-vhphi/`, stdlib, prefix `astruct_`): `core` (my own definitions of A_r, lock, F), `a3` (A_3 witness check), `census` (ring-transfer enumeration of ALL colourings), `list`, `twist`, `certify`, `local`, `layers`, `radius`, `chainhist`, `anat`/`anat2`/`comps`/`wave`/`sym`/`shapes`/`prefix`/`delete` (exploration).

## 0. Headline

1. [computed] On A_r for **r = 3, 4, 5, 6, 7, 8** (orders 17..42) an exhaustive enumeration (all proper 4-colourings of A_r - v with 4-coloured link, x0 = 0) finds infinite all-doubly-locked F-orbits; the number of colour-renaming classes is **20, 20, 60, 100, 220, 420 = 20 J_(r-2)** (J = Jacobsthal 0,1,1,3,5,11,21,...). Every such orbit has period 20 up to renaming and exactly 60 raw (r = 3 checked directly; for all r by Lemma B below). No orbit was cap-undecided. **r = 2: none, and in fact no state has even one lock.**
2. [hand] **Closing criterion (Lemma B):** on any A_r, if s, F s, F^2 s, F^3 s are doubly locked and F^4 s = pi o s o sigma (sigma = rotation t -> t+3 of the 5-fold symmetry, pi a colour permutation), then the chain is infinite. [computed] This hypothesis holds for **every** infinite-chain colouring found, r = 3..8 (all 4, 4, 12, 20, 44, 84 listed colourings with ring 0 fixed), with pi always a 3-cycle (one colour fixed), which is exactly why the raw period is 3 x 20 = 60.
3. [hand] r = 2 fails for a clear reason: the cap forces ring 1 to use <= 3 colours and then no first lock exists (section 3).
4. [computed, new structure] The infinite-chain colourings are **walks on a triangle K3**: from depth 2 on, each ring has exactly 3 possible colourings per depth and each has 2 successors; the full solution set equals the set of all paths of its own layered transition graph (window 2) for r = 4..8. Start and end vertices of the walk are distinct, which gives the count J_(r-2) = (2^(r-2) - (-1)^(r-2))/3 and the vanishing at r = 2 (J_0 = 0). **A complete proof for all r is NOT obtained**; the lemma needed is stated in section 4.
5. [computed] Kempe radius (swaps to a state with <= 3 link colours): 2 or 3 on A_3, exactly 2 on all colourings of A_4..A_8 (section 6).

## 1. The family A_r and my checker (task 1) [hand definitions, computed checks]

A_r, r >= 1: vertices v, ring vertices (i,t) with i = 0..r-1, t in Z_5, and a cap c; order 5r + 2. Edges: v~(0,t); ring edges (i,t)~(i,t+1); the antiprism strip between ring i and i+1: (i+1,t) ~ (i,t) and (i,t+1); c~(r-1,t). So (i,t) has down-neighbours (i+1,t-1),(i+1,t), up-neighbours (i-1,t),(i-1,t+1). Degrees: v, c and the rings 0 and r-1 have degree 5, middle rings 6 (12 degree-5 vertices for every r >= 2); r = 2 is the icosahedron. The rotation sigma_k: (i,t) -> (i,t+k), fixing v, c, is an automorphism preserving the cyclic order of the link x_t = (0,t), t = 0..4.

State at v: proper 4-colouring of A_r - v with 4 colours on the link; one colour repeats at x_j, x_{j+2}; m = x_{j+1}, a = x_{j+3}, b = x_{j+4}. Doubly locked: m,a in one component of the subgraph induced by {col m, col a}; m,b in one component of {col m, col b} (components in A_r - v). F: swap alpha = col x_j and col a on the {alpha, col a}-component of x_{j+2}. Implemented in `astruct_core.py` (own code; the graph was checked equal to the A3_FACES graph of `lattack_witness.py`, with v = 0, ring i vertex t = 1+5i+t, cap 16).

[computed] `astruct_a3.py`: the witness colouring (rings 01023 | 23101 | 02323, cap 1) has an F-orbit of raw period **60**, every state doubly locked; up to renaming the period is 20 (confirmed independent of the earlier team). Repeat indices run 0,3,1,4,2,... (+3 per step).

## 2. Structural results on the orbit

**Lemma A (equivariance) [hand].** For an automorphism sigma of A_r fixing v and preserving the orientation of the link, and any colour permutation pi: doubly(pi o s o sigma) = doubly(s) and F(pi o s o sigma) = pi o F(s) o sigma. Proof: the definitions of j, m, a, b, the pair-induced components and the swap use only adjacency, the cyclic order of the link and which vertices have equal colours; sigma maps the link x_t to x_{t+k}, shifts j accordingly, and maps components to components. [computed: checked on 4 x (number of solutions) states for each r = 3..8, 0 failures, `astruct_certify.py`].

**Lemma B (closing criterion) [hand].** Let s, F s, F^2 s, F^3 s be doubly locked and F^4 s = pi o s o sigma. Then F^n s is doubly locked for all n and F^20 s = pi^5-type renaming of s. Proof: F^(4+n) s = F^n(pi s sigma) = pi (F^n s) sigma by Lemma A; so F^4 s is doubly locked (Lemma A, first part), and by induction on n every F^n s is a pi-renamed sigma-image of F^(n-4) s. With sigma = rotation by 3: sigma^5 = id and F^20 s = pi^5 o s o sigma^5-type, which is s renamed; with pi of order 3, F^60 s = s. QED. Why sigma by 3 and not another: the repeat index of F s is j+3 (Theorem A, MathVHLine), so F^4 s has repeat index j+12 = j+2 mod 5, and s o sigma_3 has repeat index j-3 = j+2: the link patterns are compatible. This explains the index, not that the whole colouring (not just the link) is carried to its rotation.

**Computed fact C1.** For every infinite-chain colouring on A_3..A_8: F^4 s = pi o s o sigma_3 exactly, pi a 3-cycle on the colours (fixing the repeated colour alpha, as the link bookkeeping of MathVHLine predicts). So Lemma B applies and **an infinite orbit on A_r is certified by four lock checks and one equality**. (`astruct_certify.py`; output: all of 4, 4, 12, 20, 44, 84 solutions pass.)

[computed] Radial hairpin picture (`astruct_anat2.py`, A_5 example): in the orbit the lock paths are "hairpins": a radial path from the link down through all rings to ring r-1 (or the cap), a turn at the bottom, and a radial path back up to the other link vertex; the swapped component K of F is likewise a small radial path (size 4..9, one or two vertices per ring). It is NOT a ring-wrapping chain: the locks go radially along the strips. This corrects the earlier [lead] "lock paths wrap around v along rings" (L-Attack section 3).
[computed] The orbit is a delay line: from depth 3 on, ring (i+1) at time n equals ring i at time n+d (up to renaming), d odd, for r = 6, 8 samples (`astruct_wave.py`).

## 3. Why r = 2 fails (task 2) [hand]

Claim: in the icosahedron A_2 no state at v has the lock m ~ a (so none is doubly locked); [computed] confirmed: all 60 states (x0 = 0) have both locks false (`astruct_chainhist.py`).
Proof. By the rotation symmetry take j = 0, link (al, be, al, ga, de) (alpha, beta, gamma, delta), m = x1, a = x3. Ring 1 vertices w_t ~ x_t, x_{t+1}, cap c ~ all w_t. Properness gives w0, w1 in {ga,de}; w2 in {be,de}; w3 in {al,be}; w4 in {be,ga}; and c must be a colour missing from ring 1.
Case w0,w1 = ga,de: w4 != w0 forces be, w3 != w4 forces al, w2 != w1 forces be: ring 1 = (ga,de,be,al,be) uses all four colours, no colour for c. Impossible.
Case w0,w1 = de,ga: ring 1 must miss a colour, so not both al and be occur. If w3 = al then w2 = de and w4 = ga (no be): ring 1 = (de,ga,de,al,ga), c = be; x3 = ga has neighbours x2 = al, x4 = de, w2 = de, w3 = al, none in {be,ga}, so x3 is isolated in the {be,ga}-subgraph: no lock. If w3 = be then w2 = de, w4 = ga, ring 1 = (de,ga,de,be,ga), c = al; the {be,ga}-component of x1 is {x1,w1} (w1 = ga has neighbours w0 = de, w2 = de, x2 = al, c = al), so x3 is not in it: no lock. QED.
What is missing: the lock path must be a hairpin that goes down and turns; with only two rings the cap condition (ring 1 uses <= 3 colours) and the link condition (ring 0 uses 4) leave no room for the turn. In the walk picture of section 4 this is J_0 = 0: no walk of length 0 between distinct vertices.

## 4. The family for all r: what is proved and what is exactly missing (task 2)

[computed] Census (all colourings, x0 = 0; classes up to renaming, all with period 20 up to renaming):

| r | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|
| order | 12 | 17 | 22 | 27 | 32 | 37 | 42 |
| colourings with 4-colour link (x0 = 0) | 60 | 360 | 1920 | 10080 | 52800 | 276480 | 1447680 |
| infinite all-locked classes | 0 | 20 | 20 | 60 | 100 | 220 | 420 |
| with ring 0 = 01023 fixed | 0 | 4 | 4 | 12 | 20 | 44 | 84 |

(r = 3, 4, 5 agree with the 120/120/360 raw counts of the L-Attack and the audit: 20, 20, 60 classes x 6.) Chain-length histogram on A_3 (x0 = 0, raw): length 0: 180, 1: 60, infinity: 120; A_5: 0: 6900, 1: 2460, 2: 240, 3: 120, infinity: 360 (`astruct_chainhist.py`).

[computed] **Layer structure** (`astruct_layers.py`, `astruct_local.py`; ring 0 = 01023): depth 1 has 2 ring colourings, depths 2, 3, ... have 3 each, every one with exactly 2 successors, the three states of a layer forming a triangle (each pair of states shares a successor): the layered graph is a walk on K3. The set of solutions equals the set of all paths of the layered union graph (window 2, position dependent), r = 4..8. The first 5 rings of the r = 7 and r = 8 solutions are the same 16 sequences (2^4 free binary choices); the last rings impose an end condition. Every ring is of shape "A" (4 colours, pattern 01023) or "B" (3 colours, pattern 01012); no BB occurs except at the very end. The number of walks on K3 of length n from a vertex to a different vertex is (2^n - (-1)^n)/3 = J_n, matching 4 J_(r-2).
**[conjecture J]** For all r >= 3 the set of infinite-chain colourings of A_r (ring 0 fixed) is the set of walks of length r-2 on K3 between the start vertex fixed by the first rings and a distinct end vertex fixed by the cap , times 4 (the factor 4 is only observed; I did not identify its origin; the last ring and cap come in pairs differing by a {0,1}-swap of one ring vertex and the cap); hence count 4 J_(r-2) >= 1 for every r >= 3 and 0 for r = 2. Checked r = 3..8 only.

**What a full proof needs (stated precisely).** (i) Define the three ring types at each depth intrinsically (they are not yet identified with, e.g., the Tait colour of the radial edges); (ii) prove that for a colouring in the walk family, the {be,ga}- and {be,de}-components at the link are the hairpins (radial path down, turn at the first ring where the walk "reflects", radial path back) for every length and every walk; (iii) prove that F, which swaps one small radial component, maps the family to itself, i.e. acts on walks as a local rewriting rule; (iv) check that F^4 s = pi s sigma_3. Steps (ii) and (iii) are a connectivity statement through r strips; I could not write them out for general r. A cheaper partial route: Lemma B reduces everything to four locks and one equality for ONE explicit colouring per r, and C1 shows the equality is always true in the data; what is missing is a parametrised closed form for such a colouring in r (e.g. a periodic interior ABAB... with a boundary word) together with a uniform proof of its Kempe components. I did not find the closed form; the alternating word ABABAB... exists for r = 8 (8 colourings with ring shapes A B A B A B A B), see `astruct_shapes.py` output on the r = 8 listing.
The colouring itself is NOT invariant under a combination of sigma and a colour permutation (checked on the A_3 witness: `astruct_sym.py`, no rotation equals any renaming of s itself); instead the orbit is: sigma_3 s is a colour renaming of F^4 s. So the right symmetry is "F^4 = sigma_3 up to a 3-cycle", not a ring colouring invariant under rotation and permutation.

## 5. r = 6, 7, 8 (task 3) [computed]

The pattern persists: 100, 220, 420 classes (previous table), all period 20 up to renaming; every listed colouring of r = 6, 7, 8 (20, 44, 84 with ring 0 fixed) satisfies C1 and Lemma B's hypothesis. Run times: r = 6: 2 s, r = 7: 12 s, r = 8: 69 s (single process).

## 6. Consequences for VH-exists and clean vertices; radius lead (task 4)

[computed] `astruct_radius.py` (BFS over Kempe swaps of every bichromatic component of A_r - v, canonical states, depth <= 5): the minimum number of swaps from an infinite-chain colouring to a state with <= 3 link colours is **3 for 2 of 4 colourings on A_3, 2 for the others, and exactly 2 for all colourings on A_4, A_5, A_6, A_7, A_8** (4, 12, 20, 44, 84 colourings). Never 1 (consistent with the lock theory: a doubly locked state is not filled by a single swap).
Feature that keeps the radius small [lead]: the radius counts swaps, not vertices. In the r = 6 example the first swap is the {al,be}-component of three consecutive link vertices of size 9 living in rings 0..2 (profile 3,3,3,0,0,0,0), independent of r; the second swap is a {al,ga} radial path crossing all rings (7 vertices). So a long radial hairpin costs one swap; a depth-r structure cannot increase the distance. This suggests, for Conjecture R: bound the radius by exhibiting, at a doubly locked state, one local swap near v (confined to a bounded disc) that changes which pair is repeated, followed by one swap of a lock-type chain. I did not formalise this; the same two-swap shape appeared in the one example printed, not checked on all.
Consequence: **none for VH-exists or clean vertices.** In A_r the Kempe class of such a state contains filled states at distance <= 3, so these are not targetless components; infinite F-chains are therefore not an obstruction to cleanliness, only the failure of Conjecture L (which was only a route). A_r has no protected face (not checked against the project's protected-face definition). The point v of A_r is not clean or unclean by these data: cleanliness is a statement about all colourings, not an F-orbit.

## 7. Ledger

[hand]: definitions; Lemma A; Lemma B; the r = 2 non-existence of the first lock (full case analysis).
[computed]: census r = 2..8; period 60/20; F^4 = pi s sigma_3 with pi a 3-cycle for all solutions r = 3..8; equivariance on those states; K3/layer structure and window-2 locality r = 4..8; radius table; chain histograms r = 2..5.
[conjecture]: J (the walk description for all r). [lead]: radial hairpin mechanism and the two-swap radius shape.
Not proved: existence of an infinite orbit on A_r for r >= 9, and any claim for general r beyond the data above. Not claimed: anything about the core, VH-exists, or targetless components.
