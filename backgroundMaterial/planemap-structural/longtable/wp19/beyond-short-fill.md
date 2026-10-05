# Beyond the short-fill theorem: what happens at mixed distance 3

Long Table, 5 October 2026. This is a research note on extending `SolvingFrameworkPlan/MathShortFillTheorem.md` (ℓ ≤ 2 ⇒ κ = ℓ) past length 2.

- No graph census or enumeration was run.
- The constructed examples are hand-built graphs, each with at most 19 vertices.
- The WP19 numbers are read from the saved outputs. The two saved order-24 records are re-analysed from `../audit/wp19-counterexamples.json`.

Labels:
- **[hand]**: a complete argument given here.
- **[computed on constructed example]**: a BFS on a hand-built graph, using the self-written `beyond_short_fill_core.py`.
- **[computed on saved data, post hoc]**: read from the saved WP19 data.
- **[open]**: not settled here.

Conventions are those of the theorem:
- G is any finite simple graph and the palette has k colours.
- A **slide** h→u needs c(u) to be unique on N(h).
- A **Kempe move** swaps one whole two-colour component of G − (current hole); singleton components are allowed.
- A **target** is a state whose hole sees fewer than k colours.

Scripts and outputs (all in this folder):

| Script | Output | Content |
|---|---|---|
| `beyond_short_fill_core.py` | — | moves, BFS for ℓ and κ, replay in actual colours, path anatomy |
| `beyond_short_fill_constructions.py` | `beyond-short-fill-constructions.txt` | E1–E4 and the planar 4-colour probes |
| `beyond_short_fill_lemma.py` | `beyond-short-fill-lemma.txt` | Lemma L3/L4 checks and the exact joint (ℓ, κ) on 24:6406 and 24:7228 |
| `beyond_short_fill_data.py` | `beyond-short-fill-data.txt` | joint (ℓ, κ) reconstructed from the hist marginals of wp19-P1/P2/P3 |

## Summary

1. **κ is not bounded by any function of ℓ** [hand]. There is a planar graph on 7 vertices with 3 colours and a start with **ℓ = 3 and κ = ∞**: no sequence of Kempe moves at the original hole ever fills it (§1, E1). So the short-fill theorem is sharp. Distance 2 is the last distance at which slides can always be removed, and at distance 3 they can be indispensable.
2. **The example survives several hypotheses** [hand]:
   - **any number of colours k ≥ 3**: join E1 with K_{k−3} (E2);
   - **a degree-5 hole**: with 5 colours (E2.2), and with 4 colours via an 8-vertex graph (E3), both non-planar;
   - **planar graphs of every size**: the ladders C3 × P_m plus a hole (E4).

   Planarity, degree 5, and any fixed palette size therefore do not restore a bound **individually**.
3. **Positive results** [hand]:
   - With 3 colours on a triangulation, ℓ < ∞ forces ℓ = κ = 0.
   - If k exceeds the degeneracy of G − h, or G is planar and k ≥ 5, then ℓ < ∞ ⇒ κ < ∞ (cited theorems). These give finiteness only, not a bound in ℓ.
   - The WP19 setting (planar triangulation, 4 colours, degree-5 hole) is **[open]**. Four small planar 4-colour probes, all built from the icosahedron or antiprisms, gave κ = ℓ.
4. **Saved WP19 data, orders 21–24** [computed on saved data, post hoc]:
   - The maximum κ is **5**, and **"nofill" never occurs**. "Capped" never occurs either.
   - Every observed start has κ − ℓ ≤ 2.
   - κ = 5 occurs with ℓ = 3 (24:7228) and, as **forced by the marginals**, also with **ℓ = 4** (22:93 vertex 17, 24:7273 vertex 20). So κ − ℓ = 2 is reached at ℓ = 4 as well.
5. **Lemma L4 tightens L3** [hand] (§4). Take a shortest path S·K1·K2 with ℓ = 3 < κ, and let ρ be the colour that K1 pairs with σ.
   - If h ∉ K1, then K1 avoids N(h), and u has a ρ-neighbour inside K1 as well as another ρ-neighbour that is {σ,ρ}-connected to h after the slide.
   - If h ∈ K1 and u has no ρ-neighbour in K1, then κ ≤ (number of ρ-neighbours of h). This case is impossible at a degree-5 hole with 4 colours.
   - Corollary: in the WP19 setting, u always has a ρ-neighbour in h's {σ,ρ}-component after the slide.
   - Holds without exception on both saved order-24 graphs [computed on saved data].

---

## 1. Unboundedness: ℓ = 3, κ = ∞

### E1: the prism with a degree-3 hole (planar, k = 3) [hand; computed on constructed example]

**Graph.** Take the triangular prism: two triangles a0a1a2 and b0b1b2, plus the edges a_i b_i. Add a hole h adjacent to a0, a1 and b0. This gives 7 vertices and 12 edges. The graph is planar: h sits in the quadrilateral face a0 a1 b1 b0. (The script finds a rotation system with V − E + F = 2.)

**Start.** s = (a0, a1, a2, b0, b1, b2) = (0, 1, 2, 2, 0, 1). The link of h is coloured (0, 1, 2), so s is not a target.

**κ(s) = ∞** [hand].
1. Every proper 3-colouring of the prism colours the b-triangle by a cyclic shift of the a-triangle: b_i gets the colour of a_{i+1}, or of a_{i+2} (indices mod 3). This splits the colourings into two classes, X and Y, and both classes are closed under renaming colours.
2. In either class, the three edges a_i b_i carry the three different colour pairs.
3. So each two-colour subgraph consists of one a-edge, one b-edge and exactly one cross edge joining them. It is a path on 4 vertices, and in particular connected.
4. Hence every Kempe move is a global renaming. Every colouring is **Kempe-frozen**, and the Kempe class of s in G − h is {renamings of s}.
5. Class Y (b0 has the colour of a2) shows three distinct colours on {a0, a1, b0}, so it never contains a target. s is in class Y.

Hence κ = ∞. Equivalently: every proper 3-colouring of G restricts to class X on G − h, and Kempe moves cannot leave class Y.

**ℓ(s) = 3** [hand].
- *Lower bound.* Since κ = ∞, the short-fill theorem gives ℓ ≥ 3 (contrapositive of ℓ ≤ 2 ⇒ κ = ℓ).
- *Upper bound.* The following path reaches a target in three moves (actual colours; replayed and checked in the txt):

| Move | Hole | Link of the hole afterwards | Why legal |
|---|---|---|---|
| slide h→a0, carrying 0 | a0 | a1 = 1, a2 = 2, b0 = 2, h = 0 | 0 is unique on N(h) |
| swap {0,2} on the singleton {a2} | a0 | 1, 0, 2, 0 | a2's other neighbours a1 and b2 are both 1 |
| swap {1,2} on the singleton {a1} | a0 | 2, 0, 2, 0 | a1's neighbours a2, b1 and h are all 0 |

The last link misses colour 1, so a0 is filled with 1. The resulting proper colouring of G is a = (1, 2, 0), b = (2, 0, 1), h = 0, and it lies in class X on G − h.

So the slide carries the state between two Kempe classes of G − h. That is impossible within two moves (by the theorem) and possible in three.

[computed on constructed example] Over all colourings of G − h, the joint distribution is (0,0): 1 and (3, nofill): 1, counted up to renaming.

### E2: any palette size (apex joins) [hand; computed for k = 4, 5, 6]

**Apex lemma** [hand]. Let G′ = G ∨ z, with one more colour, and give z the new colour in s′.
- z is adjacent to every other vertex. So each {z's colour, x}-subgraph of G′ − h is connected, and swapping it is a global renaming.
- Kempe moves on pairs that avoid z's colour are exactly the Kempe moves of G − h.
- A state is a target in G′ exactly when N_G(h) misses one of the colours not used on z.

Hence κ′ = κ. Every mixed path of G lifts unchanged, because z's colour never becomes unique and z never joins a component. So ℓ′ ≤ ℓ. If κ = ∞, the theorem then forces ℓ′ = 3 whenever ℓ = 3.

Iterating gives E1 ∨ K_j, with k = 3 + j and deg h = 3 + j. In particular, **E2.2 (9 vertices, k = 5) has a degree-5 hole with ℓ = 3 and κ = ∞.** It is non-planar.

### E3: degree-5 hole with 4 colours (8 vertices) [hand; computed on constructed example]

Take E2.1 (E1 ∨ z1, k = 4) and add the edge h–b2. G − h is unchanged, so the Kempe class is still the frozen class Y.
- The link of h is (a0, a1, b0, b2, z1) = (0, 1, 2, 1, 3), so κ = ∞.
- The same three moves fill at a0. The singletons are unaffected, because h is not adjacent to a2, and the new edge h–b2 meets neither singleton.
- So ℓ = 3. The graph is non-planar, since z1 is an apex.

### E4: planar family of every size (k = 3) [hand; computed for m = 2..6]

G − h is the ladder C3 × P_m: m triangles, with consecutive triangles joined by a matching. Every 3-colouring of the ladder is Kempe-frozen, by the argument of E1 applied to each consecutive pair of layers, since the layers connect each two-colour subgraph.
- Colour layers 0 and 1 in class Y and the later layers arbitrarily, and put h in the quadrilateral face a0 a1 b1 b0.
- Then κ = ∞, and the same three-move path works: both swapped singletons (a1, a2) lie in layer 0.
- This gives planar graphs with n = 3m + 1, ℓ = 3 and κ = ∞ for every m ≥ 2.

### Finite but large κ

All constructions above give κ = ∞. Whether κ can be **finite but arbitrarily large** with ℓ = 3 is **[open]**.
- The natural relaxations of E1 collapse to κ = ℓ in every small case tried (exploration only; not part of the saved outputs): long paths in place of the prism rungs, a hole of degree 4 in the quadrilateral, and k = 4 without an apex.
- A frozen gadget gives κ ∈ {small, ∞}. A finite large κ needs a gadget whose Kempe class is large and slow to traverse.

## 2. Which hypotheses could restore a bound?

| Hypothesis | Status |
|---|---|
| planar | **no bound** [hand]: E1 and E4, with k = 3 |
| any fixed k ≥ 3 | **no bound** [hand]: E2 |
| degree-5 hole | **no bound** [hand]: E2.2 (k = 5) and E3 (k = 4), both non-planar |
| deg h < k | trivial: every state is a target, so ℓ = κ = 0 |
| triangulation (maximal planar) and k = 3 | **κ = ℓ = 0 whenever ℓ < ∞** [hand], see below |
| k > degeneracy(G − h) | ℓ < ∞ ⇒ κ < ∞ [hand, citing Las Vergnas–Meyniel 1981: all k-colourings of a d-degenerate graph are Kempe-equivalent for k > d]; a bound in terms of ℓ is [open] |
| planar and k ≥ 5 | ℓ < ∞ ⇒ κ < ∞ [hand, citing Meyniel 1978: all 5-colourings of a planar graph are Kempe-equivalent]; a bound is [open] |
| planar, k = 4 (in particular triangulations with a degree-5 hole, the WP19 setting) | **[open]**. No counterexample found; the saved data have κ ≤ 5, κ − ℓ ≤ 2 and no nofill |

**Proof of the triangulation and k = 3 row** [hand].
1. ℓ < ∞ means some target is reachable, so G has a proper 3-colouring.
2. G − h is a near-triangulation, so its 3-colourings are unique up to renaming: each colouring is forced triangle by triangle across the connected inner dual.
3. So s is the restriction of a colouring of G, and N(h) misses h's colour. Hence s is already a target.

**Proof of the two finiteness rows** [hand]. If ℓ < ∞, then G is k-colourable. The restriction of any colouring of G is a target state. By the cited Kempe-equivalence theorem, it lies in the Kempe class of s in G − h, so κ < ∞.

**What a planar 4-colour counterexample would need.**
- By Mohar (2006), all 4-colourings of a 3-colourable planar graph are Kempe-equivalent, so G − h must not be 3-colourable.
- By Las Vergnas–Meyniel, G − h must not be 3-degenerate either.
- The icosahedron is a natural source, since all 10 of its 4-colourings are Kempe-frozen [computed on constructed example]. But its faces are triangles, so a hole seeing four colours needs surgery.
- Two such surgeries were tried: replacing an edge by a degree-4 vertex, and putting a degree-5 vertex in a pentagon made by deleting two face edges. Two antiprism holes were tried as well. All gave only κ = ℓ ≤ 2 [computed on constructed example, `-constructions.txt`]. This is not evidence of a theorem.

## 3. Saved WP19 data (orders 21–24) [computed on saved data, post hoc]

Sources:
- P1 is order 23, with 2,070 graphs.
- P2 is orders 21–22, with 843 graphs.
- P3 is order 24, with 7,290 graphs.
- The file SHA-256s are printed in the txt. P3's digest `30efe4e3…` equals `phase_sha256` in the audit record.

**Limitation.** Each (v, fan) pair stores only the marginals hist_l and hist_k over its admitted starts. A start admitted by several fans at v is counted once per fan, so all counts here are **pair-weighted**, not distinct starts. The joint distribution is reconstructed as follows:
- **ℓ ≤ 2.** {ℓ = j} = {κ = j} for j ≤ 2, by the theorem (and κ ≤ 2 ⇒ ℓ ≤ κ ⇒ κ = ℓ). This is checked per pair, with 0 violations.
- **κ = 3** forces ℓ = 3.
- **The remaining block** (ℓ ∈ {3,4}, κ ∈ {4,5}) is exact when hist_k[5] = 0 or hist_l[4] = 0. Otherwise one free parameter n(4,5) remains, and it is bounded by the marginals.

Pair-weighted joint over the 781,405 pairs (152,030,412 pair-starts) with no ambiguity; the 23 ambiguous pairs are listed below:

| order | pairs | (0,0) | (1,1) | (2,2) | (3,3) | (3,4) | (3,5) | (4,4) | (4,5) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 21 | 13,570 | 302,998 | 768,672 | 192,567 | 3,456 | 72 | 0 | 90 | 0 |
| 22 | 47,390 | 1,416,003 | 3,550,335 | 878,445 | 14,193 | 297 | 0 | 212 | 0 |
| 23 | 155,593 | 6,043,978 | 15,267,776 | 3,780,009 | 40,599 | 546 | 0 | 735 | 0 |
| 24 | 564,852 | 28,658,029 | 72,669,018 | 18,225,028 | 211,806 | 2,494 | 4 | 2,936 | 0 |

The ambiguous remainder has hist_k[5] > 0 and hist_l[4] > 0. It consists of 23 pairs in 7 graphs, listed in the txt:
- Order 22: 3 pairs, all at 22:93 vertex 17. Here n(4,5) is **forced to be 1 in each**.
- Order 23: 3 pairs, at 23:390 vertex 15. Here n(4,5) ∈ [0, 1] each.
- Order 24: 17 pairs (24:829, 1334, 1437, 1483, 7228, 7273). Here n(4,5) ∈ [6, 32] in total, and 24:7273 vertex 20, fan 0 has **n(4,5) = 4 forced**.

Answers:
- **Maximum κ = 5.** κ ∈ {6, 7}, "capped" and "nofill" all have count 0.
- **κ = "nofill" never occurs**, and ℓ is never capped.
- **κ = 5 appears at 24 pairs in 8 vertex sites:**
  - with ℓ = 3 for certain at 24:7228 vertex 17 (fan 0 is unambiguous);
  - with **ℓ = 4 for certain** at 22:93 vertex 17 and 24:7273 vertex 20;
  - so κ − ℓ = 2 is attained at both ℓ = 3 and ℓ = 4.
- No pair has κ ≥ ℓ + 3 that the marginals could hide: every κ = 5 start has ℓ ≥ 3, and κ ≤ 5.
- **Exact, unfiltered joint on the two saved graphs** (all colourings at all degree-5 holes, `-lemma.txt`):

| Graph | (0,0) | (1,1) | (2,2) | (3,3) | (3,4) | (3,5) | (4,4) |
|---|---:|---:|---:|---:|---:|---:|---:|
| 24:6406 | 3,458 | 2,676 | 786 | 64 | 4 | — | 4 |
| 24:7228 | 4,800 | 3,577 | 993 | 70 | 11 | 4 | 5 |

## 4. Tightening Lemma L3

**Setting.**
- s is at hole h, with ℓ(s) = 3 < κ(s).
- By L3, a shortest path begins with a slide h→u carrying σ, giving the slid state t at hole u, where h has colour σ.
- t has a two-swap Kempe fill K1·K2 at u, and K1 is on a pair {σ, ρ}.
- H_t is the {σ,ρ}-component of h in G − u under t.
- J is the {σ,ρ}-component of u in G − h under s.
- m_ρ is the number of ρ-neighbours of h.

**Lemma L4.**

**(a) If h ∉ K1** [hand]:
1. K1 ∩ N(h) = ∅.
2. K1 contains a ρ-neighbour of u.
3. J contains a ρ-neighbour of h.
4. u has a ρ-neighbour y ∈ H_t, so y ∉ K1. Hence u has ρ-neighbours in at least two different {σ,ρ}-components of t, and J ⊇ K1 ∪ {u} ∪ (a {σ,ρ}-path from y to N(h)).

*Proof.*
1. A ρ-neighbour of h is adjacent to h, which has colour σ in t, so it lies in H_t ∌ K1. No other neighbour of h has colour σ, because σ was unique at u.
2. Suppose K1 has no ρ-neighbour of u. Then K1 is a whole {σ,ρ}-component of G − h under s: its colours agree with s, it meets neither h nor u, and properness bars σ-neighbours of u.
   - Swapping K1 leaves N(h) unchanged, so the slide stays legal, and it commutes with the slide.
   - K1(s) then has the mixed path S·K2 of length 2, so M3 gives κ(K1(s)) ≤ 2, and κ(s) ≤ 3. This is a contradiction.
3. Otherwise swapping J removes the unique σ from N(h), without adding σ elsewhere, which gives κ = 1.
4. Take a shortest path in J from u to a ρ-neighbour x of h. Its second vertex y is a ρ-neighbour of u. The rest of the path avoids u and h, so it survives in t and joins y to x. Since x is adjacent to h (colour σ in t), y ∈ H_t. ∎

**(b) If h ∈ K1 (so K1 = H_t) and u has no ρ-neighbour in K1, then κ(s) ≤ r ≤ m_ρ**, where r is the number of components of K1 − h [hand].

*Proof.*
1. Without ρ-neighbours of u, each component of K1 − h is a whole {σ,ρ}-component of G − h under s.
2. Each component contains a ρ-neighbour of h, because K1 is connected through h.
3. Every ρ-neighbour of h lies in K1, because it is adjacent to h, which has colour σ in t.
4. Swapping these r disjoint components therefore removes ρ from N(h). ∎

**(c) Corollary** [hand]. If κ(s) > max(3, m_ρ), then for **every** such decomposition u has a ρ-neighbour in H_t. This holds in the WP19 setting: with deg h = 5, k = 4 and σ unique, m_ρ ≤ 2, so case (b) without a ρ-neighbour cannot occur there.

**Checks** [computed on saved data, post hoc]. Over all ℓ = 3 starts at degree-5 holes of 24:6406 and 24:7228 (153 starts: 134 with κ = 3, 15 with κ = 4, 4 with κ = 5):
- L3(a) and L3(b) hold with no exceptions.
- L4(a) holds in all 23 h ∉ K1 decompositions of the 19 κ > 3 starts, and in all 142 such decompositions of κ = 3 starts.
- Case (b) without a ρ-neighbour occurs 0 times.
- L4(c) holds at all 19 κ > 3 starts.
- The E1–E4 decompositions also satisfy L4. In E1, for example, at u = a0, K1 = {a2} has y = b0.

**Bearing on Conjecture B** (bridge face; counterexample-analysis §E).
- L4(a) proves the bridge: K1's lift J runs through u into h's component. It does not prove that the bridge vertex y is a face vertex w of h-u-w.
- [computed on saved data] Every one of the 19 κ > 3 starts has a decomposition with h ∉ K1 and a face vertex coloured ρ. But so do 73 of the 134 κ = 3 starts, so the pattern discriminates poorly.

**κ ≤ 2ℓ − 1 = 5.** This cannot hold under L3/L4 alone, because E1 satisfies every conclusion of L3 and L4 and has κ = ∞. Any proof of κ ≤ 5 at ℓ = 3 must use planarity together with k = 4 (E3 shows that degree 5 plus k = 4 is not enough). **[open]**; the saved data are consistent with it (max κ = 5).

## 5. Open questions

1. Planar graphs with k = 4, in particular triangulations with a degree-5 hole: is κ bounded in terms of ℓ? Is κ ≤ ℓ + 2, or κ ≤ 2ℓ − 1? Is nofill impossible? The saved data are consistent with all three.
2. Is there a planar 4-colour example with κ = ∞ at any finite ℓ? It would need G − h to be neither 3-colourable nor 3-degenerate (§2).
3. Is there a family with ℓ = 3 and κ finite but unbounded, in any setting?
4. For k ≥ 5 on planar graphs, or k > degeneracy, κ is finite. Is it bounded by a function of ℓ?
5. Case (b) of L4 with a ρ-neighbour of u in K1 has no reduction yet. E1 realises it with κ = ∞, so any reduction there must use planarity.
