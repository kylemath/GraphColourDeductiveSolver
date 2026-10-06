# R* at every degree-5 hole via the Tait dual: attempt, one new parity lemma, kills

Math research worker, explore mode, 6 October 2026. **Hand work only; no code run on this machine.** A Studio check spec is in §6 (not run). No other file edited, nothing committed. Labels: [hand] = complete proof here; [sketch]; [KILLED]; [open]; [lit, recalled, not checked].

## 0. Verdict first

- **No general proof of R\*.** §5 gives the precise reason: R\* at a single degree-5 vertex of every 5-connected triangulation already implies the four colour theorem by a five-line argument. Every tool on the list (Tait criterion, Theorems A, C, D, Jordan) holds verbatim in a hypothetical minimal counterexample. So any class-independent proof built from them would be a Kempe-type proof of 4CT. The only non-circular escape found is a strictly monotone potential along DL→DL F-steps, which is Conjecture L / the potential front, not new.
- **Idea (1), as posed (an invariant contradicting "all five types occur"), is [KILLED] (§3).** Theorem A's type changes are themselves Kempe moves, so every Kempe invariant takes one value on the class. The purely P-local model is also consistent (§3.2).
- **New, [hand]: the odd-degree parity lemma (§2).** For every Kempe component K of a colouring of T−v, the number of odd-degree vertices (degrees in T) in K is ≡ the number of link edges leaving K towards one fixed outside colour. Consequences:
  - The parity t(s) = #(odd-degree vertices coloured with the repeat colour) mod 2 **flips** under F, B and the two Kempe corner swaps, and is kept by the {a,b}-swap.
  - **F^5(s) is never a renaming of s.** This answers MathCleanVertexAttack §5. F-orbits have length ≡ 0 mod 10 up to renaming, and ≡ 0 mod 30 raw. This is consistent with A_r's raw period 60.
  - It kills ConjectureL K5 (the rotation ansatz) in one line.
  - It is a genuine function, so it cannot by itself kill a targetless class (§3.3).
- **Idea (2), [hand] (§1.4):** in the dual, Kempe's 1879 double swap is the simultaneous swap of the two "corner" P-paths Z1, Z2. It works iff Z1 ∩ Z2 = ∅. Heawood's failure is exactly Z1 ∩ Z2 ≠ ∅. Among all pairs of P-paths, this pair is the only one that gives a fill and can be disjoint.

## 1. Dictionary [hand]

Setting as in `pd2_lock_proof.md`. H is the dual of T−v. P is its pentagon node; e_t is dual to x_t x_{t+1}. Colours are in Z2×Z2, and the dual colour of uw is c(u)+c(w).

### 1.1 Words

The five P-edge colours sum to 0 (they telescope around the link). Five nonzero elements of Z2² summing to 0 have colour counts (3,1,1), since all three counts must have the same parity. Call the colour used three times the majority colour.

**Lemma 1.1.**
- The link uses 3 colours (a fill) iff the three majority edges are cyclically consecutive.
- The link is unfilled (4 colours, repeat {x_j, x_{j+2}}) iff the majority edges are {e_j, e_{j+1}, e_{j+3}}.

*Proof.* A fill is (α,β,α,β,γ) up to rotation. Its dual word is (α+β, α+β, α+β, β+γ, γ+α): consecutive. An unfilled link gives the word (β,β,γ,β,δ) at e_j..e_{j+4} (pd2 notation): not consecutive. Every 3-subset of Z5 is one of these two shapes. ∎

### 1.2 Double lock as a chord pattern

At P:
- The (β,γ)- and (β,δ)-subgraphs have degree 4. Each has two non-crossing P-paths (pd2 Step 0).
- The (γ,δ)-subgraph has degree 2. It has one P-path, Z0 = {e_{j+2}, e_{j+4}}.

Call e_{j+3} the **isolated majority edge**. By the Tait criterion:
- lock 1 fails iff the (β,γ)-system pairs e_{j+3} with its neighbour e_{j+2};
- lock 2 fails iff the (β,δ)-system pairs e_{j+3} with its neighbour e_{j+4}.

**DL ⇔ in both systems containing it, the isolated majority edge is paired across the pentagon (to e_j, resp. e_{j+1}).**

The DL chord diagram is then fixed. With j = 0:

| Path | Colours | Ends | Kind |
|---|---|---|---|
| Z0 | (γ,δ) | {2,4} | long |
| Z1 | (β,γ) | {1,2} | short |
| Y1 | (β,γ) | {0,3} | long |
| Z2 | (β,δ) | {4,0} | short |
| Y2 | (β,δ) | {1,3} | long |

### 1.3 The five P-moves

Swapping the two colours along one P-path keeps the sum at P equal to 0. It is the composite of the vertex Kempe swaps of the region it cuts off, so it is a Kempe move. Its inverse is the same swap.

From a DL state of index j, read off from the words, with the vertex-swap translation:

| Move | Vertex form | Result |
|---|---|---|
| Y2 | = F: the {α,a}-component of x_{j+2} | index j+3 |
| Y1 | = B: the {α,b}-component of x_j | index j+2 |
| Z1 | the {α,b}-component of x_{j+2}, which avoids x_j, x_{j+4} by lock 1 | index j+2, repeat colour b |
| Z2 | the {α,a}-component of x_j | index j+3, repeat colour a |
| Z0 | the {a,b}-component of x_{j+3}, x_{j+4} | index j, a and b exchanged |

- **No P-move from a DL state produces a fill word.**
- F and B are mutually inverse, and so are Z1 and Z2: the old Z1 is the new Z2. Z0 is an involution.

So Z1 : X^j → X^{j+2} is a second bijection between types, alongside Theorem C.

Remark. A raw Kempe class is closed under the 24 colour renamings, because a global transposition is the swap of every {p,q}-component. So "all five types" (Theorem A) upgrades for free to all 120 unfilled link colourings.

### 1.4 Kempe and Heawood in the dual

Swapping Z1 and Z2 together turns (β,β,γ,β,δ) into (δ,γ,β,β,β), a fill. These are Kempe's two simultaneous swaps, at corners x_{j+2} and x_j.
- Z1 is a (β,γ)-path and Z2 a (β,δ)-path.
- Every node has a single β-edge, so the two paths meet iff they share a β-edge.
- If they are disjoint, the two swaps commute and the fill is reached in 2 moves. If they meet, swapping Z1 recolours a shared β-edge to γ and Z2 is no longer a path. That is Heawood's mechanism.

**Kempe's argument succeeds at s iff Z1(s) ∩ Z2(s) = ∅.**

Check of all pairs of P-paths that are disjoint at P (the others share a P-edge):

| Pair | Result |
|---|---|
| Z1+Z2 | fill |
| Z0+Y1 | fill |
| Z0+Y2 | fill |
| Z1+Y1 | unfilled |
| Z2+Y2 | unfilled |

- Z0+Y1 and Z0+Y2 have interleaved ends, so by Jordan they always share a node.
- **So the Kempe pair is the only pair of P-paths that can give a 2-move fill by simultaneous swap.**

In a targetless class every state has Z1 ∩ Z2 ≠ ∅. This also follows from DL closure: swapping Z1 makes lock 1 depend on a (β,δ)-path built from Z2 with detours along Z1.

## 2. The odd-degree parity lemma [hand]

**Lemma 2.1 (sphere).** Let T be a triangulated sphere with a proper 4-colouring. Then every bichromatic component K contains an even number of odd-degree vertices.

*Proof.* Σ_{u∈K} d(u) = Σ_faces |f ∩ K|. No face has three vertices in K, since K is 2-coloured. So the sum is ≡ N1, the number of faces with exactly one K-vertex.

The cut ∂K is an even subgraph of the cubic dual, so it is a union of cycles. Walk along one cycle:
- each step crosses a cut edge (k, y) with k ∈ K and y ∉ K, and y is coloured r or s (the other two colours);
- at a face (k, y, y') with one K-vertex, the outside vertex changes to an adjacent one, so its colour flips between r and s;
- at a face (k, k', y) with two K-vertices, the outside vertex stays the same.

The walk returns to its start, so the number of flips is even. Hence N1 ≡ 0. ∎

**Lemma 2.2 (the hole).** T is a triangulation, v has degree 5 and c is a 4-colouring of T−v. Write deg for degrees in T. Let K be a {p,q}-component of T−v and r one of the other colours. Then

  #{u ∈ K : deg u odd} ≡ ρ_r(K) := #{link edges x_t x_{t+1} with exactly one end in K and the other end coloured r} (mod 2).

*Proof.*
- A vertex u ≠ v lies on deg u faces of T−v, or deg u − 2 if it is a link vertex. So Σ_K deg ≡ N1 as before.
- ∂K is now a union of cycles avoiding P and of P-to-P paths, whose ends are the cut link edges.
- On a cycle, N1 contributes an even number (Lemma 2.1).
- On a path, the outside colour flips once per one-K-vertex face. So the path contributes ≡ [the outside ends of its two link edges have different colours].
- Summed over any pairing of the cut link edges, this is ≡ the number of cut edges whose outside end is r, because #r = 2#(rr) + #(rs). ∎

**Corollary 2.3 (the O-vector).** Let O_i be the number of odd-degree vertices of T−v coloured i.
- Summing 2.2 over all {p,q}-components gives O_p + O_q ≡ L_{pq|r}, the number of link edges with one end in {p,q} and the other coloured r. This depends on the link colouring only.
- For an unfilled link (α,μ,α,a,b), this gives **O_α ≡ O_a ≡ O_b ≡ t, O_μ ≡ t+1**. The free bit t is the only global parity.
- Hand check on the icosahedron minus a vertex: link (1,2,1,3,4), ring (4,3,4,2,3), cap 1. All 11 vertices are odd and O = (3,2,3,3), so t = 1 ✓. The same holds for the second colouring, with ring (4,3,4,1,3) and cap 2.

**Theorem 2.4 (parity flip).** Define t(s) := O_{repeat colour}(s) mod 2. It is invariant under renaming.
- t flips under F, B, Z1 and Z2.
- t is kept under Z0, and under any swap of a component that misses the link.

*Proof.* A {p,q}-swap of K changes O_p and O_q by #odd(K) ≡ ρ_r(K).
- F: K ∩ link = {x_{j+2}, x_{j+3}}. The cut link edges are x_{j+1}x_{j+2} (outside μ) and x_{j+3}x_{j+4} (outside b). So ρ_μ = 1. The repeat colour stays α, and O_α flips.
- B: by symmetry, the cut edges are x_jx_{j+1} (outside μ) and x_{j+3}x_{j+4} (outside a). ρ_μ = 1.
- Z1: K ∩ link = {x_{j+2}}, with cut edges to μ and to a. ρ_μ = 1. The new repeat colour is b, and O_b flips, with O_b ≡ t before.
- Z2: likewise.
- Z0: the cut edges both have outside colour α. So ρ_μ = 0 and ρ_α = 2. ∎

**Corollaries [hand].**
1. **F^5(s) is never a renaming of s.** It has the same index and t+1, while every renaming of s has t. More generally, F^k(s) ≅ s up to renaming forces k ≡ 0 (mod 10).
   - Raw: F permutes the roles (m,a,b) → (b,m,a) cyclically, so the raw orbit length is ≡ 0 (mod 30).
   - This answers the open F^5 question of MathCleanVertexAttack §5: orbits are never pentagons.
   - It is consistent with A_r: raw period 60, and F^4 s = π s σ involves the rotation σ, not a pure renaming.
2. **ConjectureL K5 is dead in one line.** If F(s0) = π∘c0∘ρ^{-1} for a graph rotation ρ and a renaming π fixing α, then t(F s0) = t(s0), but t must flip. More generally, no state has F(s) = renaming ∘ s ∘ automorphism.
3. Refined equidistribution. Let n_{j,t} be the number of states of a targetless class at v with index j and parity t. F and Z1 give n_{j,t} = n_{j+3,t+1} = n_{j+2,t+1}. Hence all ten counts are equal.
4. Geometric reading. If lock 1 holds and deg x_{j+2} is even, then the {α,b}-chain of x_{j+2} contains an odd-degree vertex off the link. In general the F, B, Z1 and Z2 chains each contain an odd number of odd-degree vertices. Example: in A_r the link vertices have degree 5 and the only other odd vertices are the far ring and the cap. So the F-chain, which meets the link in exactly {x_{j+2}, x_{j+3}}, must contain an odd number of far-ring and cap vertices. This is a cheap Studio test.
   - This is an identity, not a targetless-only constraint.

## 3. KILLED lines

**3.1 [KILLED] "A parity or counting invariant incompatible with all five repeat types (idea 1 as posed)."** A Kempe invariant is constant on a Kempe class. F is a single Kempe move from type j to type j+3. So any invariant takes equal values on all types present, and no contradiction with Theorem A can come from an invariant.

The only variant that could work is a function whose change along P-moves is forced. It contradicts a targetless class only if some closed loop of moves that the class is forced to contain has a nonzero total change. For an actual function, every actual loop has zero total change. So such a function kills only hypothesised identities (as in §2, Cor. 1–2), never the class itself.

The remaining form is a **strictly monotone** Φ along DL→DL F-steps. This contradicts the finiteness of F-orbits (F is a bijection on X_v by Theorem C). It is exactly Conjecture L / VHExistsPotential.

**3.2 [KILLED] "A P-local model."** Take abstract states (j, repeat colour, role order) with the fixed DL chord diagram of §1.2, and the five P-moves of §1.3. Every move lands on an unfilled word, and that model is closed and consistent.

After a P-move, the new pairings depend on how the swapped path meets the other systems. That is global data: Heawood's graph and Kempe-good graphs realise both outcomes of Z1. So nothing P-local excludes a targetless class. This is the dual form of the MathCleanVertexAttack §4 meta-obstruction.

**3.3 [KILLED as a refutation tool] the bit t.** t is a genuine function. Every realised loop flips it an even number of times. It constrains orbit lengths and symmetric ansätze, not existence.

**3.4 [KILLED] "Use 4CT plus Kempe connectivity of T−v."**
- [lit, recalled, not checked] Mohar's theorem: for a 3-colourable planar graph, all 4-colourings are Kempe-equivalent. If it applied, 4CT would give R\*.
- It never applies [hand]. A near-triangulation is 3-colourable iff every interior vertex has even degree. That would need all vertices other than v and the link to have degree ≥ 6, which gives Σ(6 − d) ≤ 1 + 5 = 6 < 12. This contradicts Euler.

**3.5 [sketch, not pursued] A Heawood mod-3 analogue of t.** Use the signs σ(u) = ±1 of the Tait orientation at the nodes. A swap of Z changes Σσ by −2Σ_Z σ, which is not P-local. I found no mod-3 quantity with a P-local change. This is open, but §3.1–3.3 say it could again only kill ansätze.

## 4. Idea (2), Heawood and the radius

Heawood's map is a DL state with Z1 ∩ Z2 ≠ ∅ (§1.4), in which the Z1-swap leaves the new lock 1 alive. Its radius is still finite, via a third swap.

In dual terms: after the Z1-swap, lock 1 of the new state asks whether the (β,δ)-path from e_{j+4} returns by e_{j+3} rather than e_j. That path is Z2 rerouted along Z1's old γ-edges at every shared β-edge. It ends at e_{j+3} iff the rerouting hands it over to Y2, which always touches Z1 at e_{j+1}.

So "r(s) ≤ 2 by the Kempe pair" ⇔ some rerouting of Z2 through Z1 ends at e_j. That is a statement about the cyclic order of the shared β-edges of Z1 with Z2 and with Y2 along Z1. I did not get further. [open]

## 5. Why a class-independent proof of R\* cannot be cheap (precise)

**Proposition 5.1 [hand].** Suppose R\* holds at one degree-5 vertex of every 5-connected triangulation, meaning every pure Kempe class of T−v contains a fill. Then 4CT follows.

*Proof.* Take a minimal counterexample T. It is a 5-connected triangulation of minimum degree 5 (Birkhoff), and has a degree-5 vertex v (Euler). T−v is 4-colourable by minimality. R\* moves its colouring within its Kempe class to a fill, and v extends. ∎

Every tool on this front holds verbatim in such a T: Tait criterion, Theorems A, C, D, Lemma 2.2, Jordan. So a class-independent proof from them is a Kempe-type proof of 4CT. R\* is also strictly stronger than 4CT: it is a Kempe-connectivity statement, and §3.4 shows the known connectivity theorems do not reach T−v.

Hence the realistic routes:
- (a) class-dependent R\*, by radius bounds on the unavoidable families of MathRstarUnavoidable;
- (b) a monotone potential (§3.1).

The global Tait route adds the exact dictionary (§1) and the parity bit t (§2) as tools for (a) and (b).

## 6. Studio check spec (not run; ≈ minutes on census n ≤ 16)

Use `backgroundMaterial/planemap-structural/longtable/explore-vhphi/astruct_core.py` (comp, repeat_index, roles, doubly, F). Script `tait_parity_check.py`:

```
for (T, v) in census graphs (4-conn, min deg 5, n<=16) and A_r (r=3..6), every deg-5 v:
  deg = degrees in T; odd = {u != v : deg[u] odd}
  for col in all 4-colourings of T-v (up to renaming):
    L = link order; cs = [col[x] for x in L]
    # (P1) Lemma 2.2 on every Kempe component
    for each pair {p,q}, each {p,q}-component K of T-v:
      for r in other two colours:
        rho = #{t : exactly one of L[t],L[t+1] in K and the other has colour r}
        assert len(K & odd) % 2 == rho % 2
    j = repeat_index(col,L)
    if j is not None:
      O = {i: #{u in odd: col[u]==i}}; alpha = cs[j]; mu = cs[(j+1)%5]
      assert O[alpha]%2 == O[cs[(j+3)%5]]%2 == O[cs[(j+4)%5]]%2 != O[mu]%2   # Cor 2.3
      if lock2 holds: s2 = F(adj,col,L); assert tbit(s2) != tbit(col)      # Thm 2.4
      if doubly: record |Z1 ∩ Z2| (shared beta-edges = shared nodes of the
                 {alpha,b}-chain-dual and {alpha,a}-chain-dual; equivalently test whether
                 swapping the {alpha,b}-comp of x_{j+2} and then the {alpha,a}-comp of x_j
                 in the ORIGINAL colouring commute) and radius r(s) (lattack_radius.py)
Output: counts of assertion passes; table radius vs [Z1∩Z2 empty]  (expect: empty ⇒ r ≤ 2).
```

Expected: 0 assertion failures. A failure of P1 would mean an error in §2.

## Ledger

- [hand]:
  - Lemmas 1.1, 2.1, 2.2; the DL chord pattern;
  - the P-move table, the Kempe/Heawood dual criterion and the uniqueness of the Kempe pair;
  - Corollary 2.3 and Theorem 2.4 with Corollaries 1–4;
  - Proposition 5.1; the §3.4 Euler computation.
- [KILLED]: 3.1–3.4.
- [open]: 3.5 (mod 3); §4 (order of shared β-edges); R\* itself.
- [lit, recalled, not checked]: Mohar's 3-colourable theorem; Birkhoff's 5-connectivity of minimal counterexamples (standard).
