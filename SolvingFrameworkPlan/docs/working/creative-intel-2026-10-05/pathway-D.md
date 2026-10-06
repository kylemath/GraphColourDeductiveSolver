# Pathway P-D: Tait (edge-colouring) view of the hole

Long Table, 2026-10-06 (`date` at writing: Tue Oct 6 2026, about 12:00 MDT). Exploratory; nothing here is evidence for a theorem; "on these graphs" = A_2, A_3, A_4 (holes v and a ring-0 vertex) and T4 (all 12 degree-5 holes), x0 = 0 colourings. Code and outputs: `explore-vhphi/pathways/pd_*.py|.out` (reuse `astruct_core.py`; nothing existing edited). Every output [exploratory]. Total CPU about 10 s, one process.

## 1. Dictionary [hand; each line also checked by code, `pd_dict.out`]
- Colours = Z2xZ2. Tait colour of edge uw of G-v is c(u)+c(w), nonzero. At a triangle uvw the three sums are distinct and add to 0, so the dual edges at each triangle carry {1,2,3}: a proper Tait colouring of the dual H. Conversely, the sphere's cycle space is spanned by faces, so a Tait colouring gives a vertex colouring unique up to translation: 4 colourings per Tait colouring. Renaming colours (S4 = AGL(2,2)) = translation + permuting the 3 Tait colours.
- Hole: the 5 triangles at v merge into one dual node P of degree 5. Steps e_t = c(x_t)+c(x_{t+1}) sum to 0, so the colour counts are (3,1,1) with all odd. Triple colour beta, odd edges gamma, delta. **Filled link (<= 3 colours) <=> the two odd edges are adjacent at P** [checked on all 11,436 states: 0 exceptions]. A repeat link (alpha,beta,alpha,gamma,delta) reads beta,beta,gamma,beta,delta: odd edges at distance 2 (always, on all DL states: `dist` = 2 on 2316 of 2316).
- Kempe chain C of class s = the node of a tree T_s; its cut delta(C) (every edge has Tait colour not s) is the union of the (p,q)-bichromatic cycles on its boundary components, p,q = the other two colours. **A chain swap = swapping all Kempe cycles of its cut** (cut-edge identity verified on 28,000 swaps). Correction to the task text: one Tait Kempe-cycle swap alone is NOT a single vertex chain swap (it translates a whole side, possibly several chains and holes); only when the cut is one cycle. Observed identity (chains over the 3 classes) = (closed Kempe cycles avoiding P) + 8 on every link-4 state tested, so chain counting adds nothing beyond cycle counting.
- **Lock criterion** [hand, then code-verified equal to `locks()` on 2616 states]: m=x_{j+1}, a=x_{j+3}, b=x_{j+4}. The (beta,gamma)-path leaving P by the gamma edge e_{j+2} returns by e_{j+1} (cuts off x_{j+2}) iff m~a locked; the (beta,delta)-path leaving by e_{j+4} returns by e_j (cuts off x_j) iff m~b locked. Otherwise the gamma-path returns by e_{j+3} (resp. the delta-path by e_{j+3}), and swapping that cycle puts the two odd edges next to each other = a fill. **F** = swap of the (beta,delta)-cycle through P pairing e_{j+4},e_j: the delta particle jumps j+4 -> j, odd edges still at distance 2.
- Picture: two coloured "particles" on the pentagon Z5; a Kempe cycle through P moves a particle to its partner end; fill = adjacent. A lock = both cycles available move the particle away.

## 2. A_3 witness orbit in Tait terms (`pd_orbit.out`)
Checked by code, all 60 raw steps: the relative end-pattern (beta,gamma,delta roles) is one of 5 rotations of A A B A C (period 5 = the sigma_3 rotation); each step has both locks, the gamma-path pairs e_{j+2}~e_{j+1} and the delta-path pairs e_{j+4}~e_j; F's cut is always ONE Kempe cycle (13 or 19 edges, chain size 4 or 6, alternating 4,6,6,4,...). By hand: this is exactly the particle jumping across the same gap each time, the two odd edges never meet. Absolute colours: exactly one of the three 2-factors has closed cycles off P (2 or 1 of them, alternating 2,1,2,1) and the colour carrying them cycles with period 3, so the k-vector has period 6 and the full state period 60 (consistent with F^4 = sigma_3 composed with a 3-cycle of the Tait colours, which [hand] is what "pi a 3-cycle fixing alpha" means). NOT checked: the orbits on A_4+ by hand, any proof for general r.

## 3. What a lock looks like (`pd_cross.out`, 2148 DL link-4 states)
Not "crossing cycles". The lock is two cycles Z1 (beta,gamma) and Z2 (beta,delta) through P, each cutting a single link vertex (x_{j+2}, x_j) off from the rest. They share 0 non-P nodes in 1010 of 2148 states (disjoint but for P) and up to 14 nodes (shared edges are beta edges only, 0 to 7 of them) in the rest; cycle lengths 4 to 20. No fixed crossing number. Minimal case (length 4 each): the cycle is just the face ring of the link vertex.

## 4. Candidate invariants and tests (`pd_inv.out`, `pd_finv.out`)
Features: closed-cycle counts per 2-factor (sorted, sum, mod 2, relative to beta/gamma/delta), vertex-chain counts and parity, the product/sum of colours around the hole (trivially 0), parity of the P-cycle half-length, odd-edge distance. Status classes: FILLED 4,524, DL 2,316, one lock fails 3,336, both fail 1,260 (all graph@hole combinations pooled).
- Separate DL from FILLED/not-DL on these graphs: only odd-edge distance (2 vs 1), which is the definition restated. Every counting feature takes the same values on DL and FILLED (ksum%2: DL 1452/864 even/odd, FILLED 2412/2112; Mohar-Salas-type parity of cycle counts is therefore not a lock detector).
- Preserved by F: none. Under F, ksum changes on 1620 of 2148 DL states (parity on 1032); under F^2 parity changes on 252 DL states; on the A_3 orbit ksum alternates 2,1.
- A "twist" (winding of the closed 5-walk) is the same for every link-4 state (the pattern beta beta gamma beta delta), so it carries no information; the product of colour sums is 0.

## 5. Kill test and verdict
Kill test = Section 4, ~10 CPU seconds, 1 process, no plantri. **Verdict: dead in the form "a cycle-count / parity invariant of the Tait colouring forces a fill"; mutated into variant X.** What survives: (i) an exact dictionary with a clean fill criterion (odd edges adjacent) and lock criterion (two single-vertex-cutting bichromatic cycles through P); (ii) the particle-on-Z5 reading of F.
**Variant X (next):** the interior acts only through the non-crossing pairing of the 5 pentagon ends by bichromatic paths (a meander/Temperley-Lieb boundary datum, two choices for each of the two beta-classes). Ask: along the A_r layer walk (K3), what are the pairings contributed by each ring (ring type A/B vs the Tait colour of its radial edges), and does the pair (Z1 pairing, Z2 pairing) of a lock force the next pair by a local rule? That is a transfer-matrix check on A_r only (no search), and it would also give the missing step (ii) of A-Structure section 4.
Not checked: graphs beyond the six listed, holes of other types, non-minimal-degree-5 graphs; no proof that the dictionary's tree T_s statement holds beyond the verified swaps; invariants beyond those listed (e.g. Z-twist of a 4-edge-colouring of the dual with the pentagon resolved, signed cycle counts).

## Update (6 Oct, afternoon)

Written about 12:40 MDT (`date`). Code and outputs are in `explore-vhphi/pathways/pd2_*`; nothing existing was edited. It was one process, about 15 CPU-seconds in total. Following Audit's 12:08 notes, the fill criterion is [hand] by the Z2xZ2 step-sum argument, and the dictionary is [cited] (Tait 1880; Saaty–Kainen).

**Lock criterion [hand]** (`pd2_lock_proof.md`). It matches `astruct_core.locks`, where m~a means a is in the {c(m),c(a)}-component of m in G-v.
- The two (β,γ) P-paths cannot cross, by the Jordan curve theorem. So Z1 returns by e_{j+1} or by e_{j+3}.
- If it returns by e_{j+1} and the lock failed, the cut of a's chain would be a union of whole (β,γ)-paths containing e_{j+2} but not e_{j+1}, which is impossible.
- If it returns by e_{j+3}, Z1 closes into a curve that separates m from a and crosses no δ (= {μ,c(a)}) edge.
- Lock 2 is the same argument. This is Lemma D read in the dual.

**Corollary [hand].** Lock 2 of s implies that x_j is not in F's chain and that lock 1 of F s holds, because it is the same {μ,c(b)}-chain: F does not touch it. So "F keeps both locks" is one chain condition: lock 2 of F s.

**Variant X, adversary first** (`pd2_x.py` [B]) [exploratory, these graphs only]. The rule tested: "whether F s is doubly locked is a function of the pairing of the five P-ends by the three bichromatic subgraphs plus local data".
- On T4's 26 radius-4 (hole, state) pairs every rule survives, but only vacuously: all 26 are doubly locked (DL) and F keeps both locks on all 26.
- On all 234 DL states of T4:
  - X0, the pairings alone, is **killed**. By the criterion above the pairings are the same at every DL state, and F s is DL at some of them and not at others.
  - X2, pairings plus the radius-1 Tait datum and link degrees, is **killed**: 6 clashing keys out of 72.
  - X3, pairings plus every colour within distance 2 of v, per graph and hole, is **killed**: 3 clashing keys out of 212. One example is at T4@0: two colourings agree on N2(v), and F s is DL for one and not for the other (states in `pd2_x.out`).
  - X1, "F s is DL iff the cut of F's chain is one Kempe cycle", is **killed** on T4 (70 + 24 exceptions) and on A_3/A_4 (300).
- On A_3 and A_4 (640 DL states), X2 and X3 survive. This is exactly the A_r regularity that Audit predicted would mislead. Verdict: Variant X in the form "pairing plus local data" is dead on T4.

**What shortest fills do on T4** (`pd2_x.py` [C], `pd2_runs.py`) [exploratory]. Every state at radius >= 2 is DL; radius 1 means unfilled with at most one lock (the last swap is the hand swap of a failing-lock chain). We followed all shortest paths from the 26 radius-4 states; the 26 states give 63 distinct step patterns. Each step swaps one vertex chain whose cut has one or two Kempe cycles and crosses P in 0, 2 or 4 edges.
- The most common pattern is three steps of F' and then the fill, on 242 paths. F' is the mirror of F (it swaps the {α,c(b)} chain of x_j); the gap moves +2 each step.
- Next is three steps of F and then the fill, on 118 paths; the gap moves +3 each step.
- The rest are mixes that include a β-class swap, which leaves the odd edges in place and swaps their colours.
- Here the gap is the lone β edge between the two odd edges.

So the particle picture holds: F and F' each make one jump, and β-swaps recolour the particles.

The data rule out "radius = 1 + the shorter run of F or F' before a lock breaks":
- On T4 it holds for 186 of 234 DL states, including 20 of the 26 at radius 4.
- On A_3 it fails at the infinite-orbit states, which have radius 2–3.

**Monotone quantity: none found** (`pd2_x.py` [D]). We tested 20 candidates on DL states with radius >= 3 under two requirements: some successor on a shortest fill has a strictly smaller value, and every DL state has a swap that leaves DL or decreases the value. The candidates were:
- A1 and A2, the number of vertices cut off by Z1 and by Z2, with their sums, min and max;
- the areas of the other two P-paths;
- the lengths of Z1 and Z2, the number of nodes they share, and the length of the (γ,δ)-path W joining the odd edges and the area it cuts off;
- the number of closed Kempe cycles, |K|, and the sizes of the lock chains;
- nDL, the number of swaps that stay DL;
- the negatives of several of these.

All 20 fail on T4. The best are nDL (fails at 18 of 72 states) and len(Z1)+len(Z2) (fails at 28 of 72). Most pass on A_3 and A_4, but those tests are almost vacuous: A_4 has no DL state of radius >= 3 at any degree-5 hole, and A_3 has 20. Radius against (A1,A2) on T4 shows no order: radius-4 states have A1,A2 in {2,4,6}, and radius-2 states run from 1 to 8.

**Not checked:** the "any one swap keeps both locks" version (only F was tested); keys that combine nonlocal pairings, such as the meander of ∂K against the (γ,δ)-system, which would be an exact but tautological rule; graphs other than T4, A_3 and A_4; and potentials that are not functions of a single state. Next candidate, if any: a potential on pairs (state, last move), since along F-runs the invariant 2-factor rotates.
