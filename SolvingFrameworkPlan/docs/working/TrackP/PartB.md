# Track P, Part B: attempt on Conjecture N1 by Euler-level counting [hand, unreviewed] + [data]

Setting (any graph): G, hole h of degree 5 with induced link x₀…x₄; nv = n − 1 = |V(G − h)|; a *state* is a proper
4-colouring of G − h up to renaming; roles (α, μ, A, B) at an unfilled state as in TrackJ §1.1; pair graphs in role order
αμ, AB, αA, μB, αB, μA; P1 = {αμ|AB}, P2 = {αA|μB}, P3 = {αB|μA}. A *law R-cycle* is a π-cycle of DL states with N ≤ 9
obeying the chain-parity law at every step; by J5 it alternates rigid (N = 8) and in-shape (N = 9) states.
For a state s, B(s) is the total cycle rank (first Betti number) of the six pair graphs.

## B1. The excess is a cycle-rank budget (identity, any graph, any proper colouring)

**Lemma P1.** For every proper 4-colouring s of G − h:  N(s) − B(s) = 3·nv − |E(G − h)|.

*Proof.* Every vertex lies in exactly three of the six pair graphs and every edge in exactly one, so
Σ_pairs (|V| − |E|) = 3nv − |E|; and |V| − |E| = (#components) − (cycle rank) for each pair graph. ∎

Write e := |E(G − h)| − (3nv − 8) (the *excess*; e = 0 is the sphere count 3n − 11, e = 3(2 − χ_S) for a triangulated
surface of Euler characteristic χ_S). Then along a law R-cycle

  B(s) = e at every rigid state,   B(s) = e + 1 at every in-shape state.

Consequences.
1. TrackN's "skeleton edge excess" (min |K| − (3n − 11) over partition-preserving delete-only surgeries) is exactly
   the minimum, over such skeletons, of the number of independent bichromatic cycles at a rigid state.
   (TrackN's per-state Lemma-E deviation equals e at rigid states whenever the cycle ranks are spread as there.)
2. **For law R-cycles, "Lemma E constants (2,3,3) at every state" ⇔ e = 0.** (⇒: (2,3,3) at one state gives
   |E| = 3nv − 8. ⇐: e = 0 makes every rigid state all-forest, hence (2,3,3) there; at an in-shape c, P2(c) and P3(c) are
   *as graphs* P3(πc) and P2(π⁻¹c) (J2), so forests with (2,1) chains, χ-sums 3, 3; and N − B = 8 gives the P1 sum 2.)
   So N1 restricted to law cycles reads: **no law R-cycle in a graph with |E(G − h)| = 3nv − 8**; equivalently, no law
   R-cycle all of whose rigid states have no bichromatic cycle at all (and whose in-shape states have exactly one, Γ_c,
   lying in A_cB_c by Lemma S).
3. At e = 0 each rigid state's three partitions are spanning forests of G − h with 2, 3, 3 trees (nv − 2, nv − 3, nv − 3
   edges): G − h is a union of three forests (arboricity ≤ 3, Nash-Williams |E(H)| ≤ 3(|V(H)| − 1) for all H).

Data: identity at every state of 128 law cycles (85 TrackN skeletons + 43 TrackJ rung-d graphs), 0 failures
(`out/struct_lawcycles.jsonl`).

## B2. Monodromy (any graph)

Along a π-orbit, α (the repeated colour) is the same colour at every state, and the other three roles rotate
(μ, A, B)_{t+1} = (B, μ, A)_t (TrackL §2.2). The swapped colour A_t therefore has period 3. Following *actual*
colourings a_t (not up to renaming), a π-cycle of length L closes as a_L = ρ ∘ a_0 with ρ fixing α and acting on
{μ₀, A₀, B₀} as the 3-cycle shift^L. J5 lengths are ≡ 0 (mod 10); for L ≢ 0 (mod 3) (e.g. L = 10, 20, the only lengths
ever observed) ρ is a fixed-point-free 3-cycle on the non-α colours.

**Lemma P2.** Let C be a law R-cycle (or any π-cycle) with L ≢ 0 (mod 3). Then
(a) every vertex of non-α colour at a_0 is swapped at least twice in one period, its colour trajectory being
    X → α → Y → α → … → ρ(X), with each move X → α at a step t with A_t = X and α → Y at a step with A_t = Y;
(b) every edge of G − h has exactly one end in some swap set K_t.

*Proof.* (a) A vertex coloured X ≠ α can only change colour inside some K_t with A_t = X, and then becomes α; it must end
at ρ(X) ≠ X. (b) Label each edge by the perfect matching of K4 that contains its colour pair (three labels Q_μ, Q_A, Q_B,
named by α's partner). An edge's label changes at step t iff exactly one end lies in K_t (if both ends are in K_t the pair is
{α, A_t} before and after; if neither, nothing changes; if one end x ∈ K_t, the other end has colour ∉ {α, A_t}, and the
label switches Q_{μ_t} ↔ Q_{B_t}). After L steps every label is permuted by ρ, which has no fixed label. ∎

Data: 128 / 128 law cycles have ρ ≠ id, every edge cut, every non-α vertex swapped (in fact every α vertex too).

## B3. Role labels, cut balance and windings (any graph)

Give an edge at time t the role label r ∈ Z/3 (P1 = 0, P2 = 1, P3 = 2). One π step acts by
- edge not cut by K_t: r ↦ r + 1;
- edge cut by K_t: r = 0 ↦ 0 and r = 2 ↦ 1 (a cut edge is never in P2).

Hence (cut balance) cutP1_t − cutP3_t = E_{P1}(t + 1) − E_{P3}(t), and at e = 0 (constants (2,3,3) at all states)
**cutP1_t − cutP3_t = 1 at every step**. Lifting to Z, each edge has a winding D(e) = #uncut − #cut-at-P3 over one period,
and D(e) ≡ 0 (mod 3) because the role labels return. Summing,

  Σ_e D(e) = L(|E| − 1) − 3 Σ_t cutP3_t   (at e = 0),

so the windings are integral iff L(|E| − 1) ≡ 0 (mod 3), and |E| = 3nv − 8 ≡ 1 (mod 3) satisfies this for every L.
Similarly, at e = 0 the signed degree sum Σ_{K_α}(deg − 1) − Σ_{K_A}(deg − 1) equals +1 at rigid→in-shape steps and −1 at
in-shape→rigid steps (this is the star identity at colour α in degree form), and it telescopes to 0 per vertex.

Data (128 law cycles): cut-balance identity 128/128; winding rule and D(e) ≡ 0 (mod 3) at every edge, 0 failures; the
observed windings D(e)/3 lie in {2, 3, 4} (e.g. 55 / 14 / 28 edges in `jd631_169_1246_K`).

## B4. Where the attempt stops

The quantities that Lemma E, St, J2, the monodromy and the role windings control are all consistent with e = 0:
- per state: TrackL's χ-recursion has the alternating orbit (1,1,2,1,2,1) ↔ (2,0,2,1,2,1) (one free integer per step);
- per colour class: W(X) = −Σ_Y χ(XY) = Σ_{v ∈ X}(deg v − 2) − nv takes the role-determined values
  (α: −5/−6; μ: −3/−4; A, B: −4/−3 at rigid/in-shape) and is transported correctly by every step;
- per step: cut balance cutP1 − cutP3 = 1 and the edge-label counts (nv − 2, nv − 3, nv − 3) are preserved for *any*
  cut numbers obeying it;
- per period: all windings integral since 3nv − 8 ≡ 1 (mod 3); every vertex swapped, every edge cut — no contradiction.

So an integer "that must change by a fixed nonzero amount per two-step and return" does not exist among these
(each candidate changes by +1 then −1). I also checked whether the excess of the known (RP²-lineage, e ≥ 3) cycles is
carried by *persistent* bichromatic cycles (a cycle-space class common to all states, which a monodromy argument might
force): the intersection of the bichromatic cycle spaces over all 20 states, and over the 10 rigid states, is **0** in all
12 skeletons tested (`tp_cyclespace.py`); consecutive states share 0–5 dimensions. So the "+3" is not a persistent
homology-like class in these examples, and a proof of e ≥ 1 cannot come from a cycle that survives the whole orbit.

**Status: N1 not proved.** Reductions obtained [hand, unreviewed, data-checked]:
(i) N1 for law cycles ⇔ no law R-cycle with |E(G − h)| = 3nv − 8 ⇔ no law R-cycle whose rigid states are all
    bichromatic-cycle-free (B1);
(ii) at e = 0 the orbit has rigid states with a 3-forest decomposition (2,3,3 trees) and in-shape states with a single
     bichromatic cycle Γ_c ⊂ A_cB_c, Γ_{c} = Γ_{Z(c)};
(iii) every Euler/χ/degree/winding invariant available is consistent with (ii) (B3–B4).
What is missing is genuinely component-level: e.g. how the two αA trees K, K′ at c are merged by the swap J at c → π(c)
while Γ_c is opened by the same J (TrackJL-review's corrected §2.2). A proof would have to show these merge/split events
cannot be periodic with no spare cycle rank; in matroid terms, that the three colour-induced spanning forests of a
3nv − 8 edge graph cannot be "rotated" through a full period by Kempe tree swaps.
