# Attack on pentagram confinement (Lemma star of MathTraceFourConnAttack §5)

Math research worker, 5 October 2026. Hand work; one small Python sanity test on graphs I built myself (§4). No census, no declared experiment, no status change. Builds on `MathTraceFourConnAttack.md` (Prop 2.2, Obs 3.1, Obs 3.2, §5).

## Verdict, first

Pentagram confinement is **not proved or refuted**. But it collapses to something simpler, and a dead end in the earlier page is reversed:

- **[hand] Theorem A (rotation closes up).** At a degree-5 vertex v, if the set 𝒯(v) of repeat pairs of targetless states is nonempty, it is **all five** pentagram edges. In particular it contains two disjoint pairs.
- **[hand] Corollary B.** The following are equivalent for an off-φ degree-5 vertex v (core, all five fans legal): (i) some fan at v is good; (ii) every fan at v is good; (iii) **no state with the hole at v is targetless** (v is "clean": every start at v reaches a filled state). So "confinement" is not about common repeat vertices at all. It is the plain statement "some degree-5 off-φ vertex is clean".
- Confinement fails iff every off-φ degree-5 vertex lies in the hole projection S of some targetless component. That is a covering statement, which I could not exclude. [open]

This reverses my own remark in MathTraceFourConnAttack §3/§7 that pairs "rotate but may stay confined": Theorem A shows they cannot stay confined once any targetless state exists at v.

## 1. Theorem A

Setup as in MathTraceFourConnAttack §2–3. Link x0..x4 of v in cyclic order, state s with colours (α,β,α,γ,δ), repeat pair {x0,x2}. Write "index j" for the pair {xj, xj+2} (indices mod 5).

**Step 1 [hand] (locks).** If s is unfilled and its component is targetless, then both locks hold: a βγ path x1~x3 and a βδ path x1~x4 in T−v. (Else swapping the βγ component of x1, resp. the βδ component of x1, makes x1 take γ or δ; that component contains no α vertex and no x3 (resp. x4), the link then misses β, so the state is filled; contradiction.) This is Obs 3.1; I only reuse it. It applies to **every** state of a targetless component, since each is unfilled.

**Step 2 [hand] (two rotating swaps).** Let P1 be the βγ path x1~x3, P2 the βδ path x1~x4. The closed curves C1 = v,x1,P1,x3,v and C2 = v,x1,P2,x4,v are simple.
- C2 separates x0 (on one side) from {x2,x3} (other side), because at v the edges to x1, x4 split the neighbours that way. C2 uses only colours β,δ, so no αγ path can join x0 to x2. Hence the αγ component K of x2 (which contains x3) misses x0. Swapping K gives link (α,β,γ,α,δ), pair {x0,x3}: index 3.
- C1 separates x2 from {x4,x0}, and uses only β,γ. So the αδ component of x0 (containing x4) misses x2. Swapping it gives link (δ,β,α,γ,α): pair {x2,x4}: index 2.
The swapped components contain no x1 and no other link vertex (K has colours α,γ, so it misses x1 (β) and x4 (δ); the other has colours α,δ, so it misses x1 and x3). Hence the new links are as stated.

So a swap takes index j (here j=0) to index j+3 or j+2.

**Step 3 [hand] (orbit).** The new states lie in the same component (swaps are moves, and components are closed under moves), so they are targetless and unfilled, and Step 1–2 apply to them again. Steps ±2 mod 5 generate Z5: 0 → 2 → 4 → 1 → 3. For instance {x0,x2} → {x0,x3} → {x1,x3}, which is disjoint from {x0,x2}. So every one of the five pairs occurs at v within the component. ∎

(Remark: no property of φ, of four-connectivity or of degrees other than deg v = 5 is used. φ may be recoloured by the swaps, which is allowed in the setting.)

## 2. Corollary B

Let v be off φ with degree 5, with all five fans legal (core). By Prop 2.2 fan xi is good iff xi lies in every pair of 𝒯(v). If 𝒯(v) ≠ ∅, Theorem A gives all five pairs, and no xi lies in all of them; so no fan is good. If 𝒯(v) = ∅, every fan is good. Hence "v has a good fan" = "v has no targetless state" = "v has all fans good". [hand]

Consequences:
1. The fan is irrelevant to goodness at a given v; it matters only for legality (and admission is vacuous). The quantifier "one fan for every start" is automatically met once v is clean.
2. Lemma star ⇔ **there exists an off-φ degree-5 vertex v, no targetless component of which has v in its hole projection.** Any argument for a good pair must be of this "clean vertex" type; no argument via common repeat vertex can work separately.
3. Each degree-5 vertex of a projection S carries at least five states of the component (one per pair) [hand]. This is a mild strengthening of the mobility facts "≥ 3 projected neighbours".
4. The total picture of a counterexample: a family of targetless components whose projections cover all off-φ degree-5 vertices (at least 7 of them at order ≥ 12 in the core), each such vertex with all five pair types present and both locks (βγ- and βδ-type) in each of its states.

## 3. What I tried next, and dead ends

**Try 1: contradict the locks in the rotated states.** The swap in Step 2 changes colours on K, and the rotated state s' = (α,β,γ,α,δ) must again be doubly locked: a δβ path x4~x1 (this exists: P2 is untouched, K avoids δ,β) and a δγ path Q from x4 to x2 in the **new** colouring. Q must cross P1 (C1 separates x2 from x4) at a vertex that is γ in the new colouring. P1's vertices in K have switched γ to α, but P1 has other γ vertices (outside K) unless P1∩γ ⊆ K. I found no contradiction: a path is available whenever P1 has an old-γ vertex outside K from which δγ paths run. A contradiction would need to place all of P1's γ vertices in K; nothing forces that. [open; dead end]

**Try 2: all-degree-5 projection and a winding invariant.** An invariant that distinguishes pair indices cannot exist as a quantity preserved by swaps, since Theorem A moves every index to every other. So the "invariant of pair under swaps" idea of §5.2 of the earlier page is **dead**. What is conceivable is an invariant of the *pair of lock paths relative to φ* that is violated at some v; I found none.

**Try 3: reduce to φ-relative counting.** A clean vertex exists if some off-φ degree-5 v has a neighbour w with a "mobility" fill (known for deg-≤4 neighbour). Math already has that; it needs a degree-≤4 vertex, which the core excludes (off φ). Nothing new.

**Try 4: the targetless component must be closed under slides to degree-5 neighbours.** Together with Corollary B, a slide from v to a degree-5 neighbour w in S leaves w with five pair types too. This gives the cycle structure already in Math's work (S contains a cycle if all holes have degree 5), but no contradiction. [hand, no gain]

So the honest status: the problem is exactly the existence of one clean degree-5 vertex off φ, equivalently "VH∃ at one vertex for all starts". It is the original open question restated with the red herring (repeat vertices) removed. I do not have a proof or a counterexample shape beyond the covering description in §2.4.

## 4. Sanity test [computed; checks Step 2 only, no universal content]

Script in the session scratchpad (not committed). I built random planar triangulations on 10–16 vertices (random face insertions followed by 60 random edge flips, edge count 3n−6 verified), picked degree-5 vertices, sampled random proper 4-colourings of G−v, kept those that are doubly locked (4170 such), applied the two swaps of Step 2 and compared the new repeat pair with the predicted ones. 8340 swaps tested, 0 mismatches. Checks that the Jordan-curve claim of Step 2 holds on explicit examples; the theorem itself is a hand proof. This tests Step 2 on locked (not necessarily targetless) states, which is all Step 2 needs.

## 5. Claim ledger

- Theorem A, Corollary B, items B.1–B.4: [hand]; Step 2 spot-checked [computed, 8340 swaps, 0 failures].
- Lemma star in the corrected form (some off-φ degree-5 vertex is clean), VH∃ in the core, and the covering statement of §2.4: [open].
- Try 1, Try 2 (invariant), Try 3, Try 4: dead ends, no claim.
- Not edited: no other file. Nothing here changes a status word.
