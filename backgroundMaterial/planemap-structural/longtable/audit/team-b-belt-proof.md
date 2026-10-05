# Team B: complete unequal-pole belt slide argument

5 October 2026. Candidate proof for independent review. Covers both requested tasks; no new census. The proof uses the already checked local A/B and doubled-1 lemmas, but supplies all eight doubled-0 openings and finite traversal boundaries.

## Conventions and completeness

For n >= 5, edges are a-u_i, b-v_i, u_i-u_(i+1), v_i-v_(i+1), u_i-v_i, u_i-v_(i-1). Fix a=0,b=1 and {rho,tau}={2,3}. A proper deletion colouring has one hole. A singleton slide transfers the unique occurrence of its colour from a neighbouring vertex to the old hole. Three colours on a hole link permit a fill. Both poles stay fixed throughout this proof.

By rotation take an upper-ring hole u_0. A lower-ring hole is equivalent: the graph automorphism a↔b, u_i↔v_(-i), followed by interchanging colour labels 0 and 1, puts it in these conventions. Reflection u_i↦u_(-i), v_i↦v_(-i-1) fixes a,b and reverses the direction.

The link order at u_i is (a,u_(i+1),v_i,v_(i-1),u_(i-1)). Four colours on five positions mean exactly one repeated colour. There are fourteen proper four-colour words: eight repeat 0, two repeat 1, four repeat rho or tau. The following cases exhaust them; links using fewer colours fill immediately.

## All eight doubled-0 words

Reflection makes v_(i-1)=0, v_i=rho. Since the two upper neighbours and rho must supply colours 1,rho,tau, and u_(i+1) is adjacent to v_i, precisely two representatives remain:

    I:  (0,1,rho,0,tau)
    II: (0,tau,rho,0,1).

Two reflections and two exchanges of rho,tau give all eight words.

### I: fill or enter the tight-edge proof

Write z=c(v_(i+1)). Its original neighbours b=1,v_i=rho,u_(i+1)=1 force z∈{0,tau}.

If z=0, slide u_i→v_i. The new link is (1,0,rho,1,0), so fill with tau.

If z=tau, the original neighbours a=0,u_(i+1)=1,v_(i+1)=tau force c(u_(i+2))=rho. Slide u_i→u_(i+1), writing 1 at u_i. The new hole link is (0,rho,tau,rho,1), one of the four tight-edge words treated below. The slide uses the unique 1 on the old link.

### II: a finite upper-ring walk

Slide u_i→u_(i+1), writing tau at u_i. Originally v_(i+1)=0, forced by b=1,v_i=rho,u_(i+1)=tau. The new hole link is

    (0,s,0,rho,tau),  s=c_original(u_(i+2))∈{1,rho}.

If s=rho, fill with 1. If s=1, slide onward to u_(i+2), writing 1 at u_(i+1). Put q=c_original(v_(i+2)). Original adjacency to b=1,v_(i+1)=0,u_(i+2)=1 gives q∈{rho,tau}. Original adjacency to a=0,u_(i+2)=1,v_(i+2)=q forces u_(i+3) to the other colour p in {rho,tau}. The new link is (0,p,q,0,1), another II word, two indices forward. Both slides are singleton slides. No lower vertex is rewritten.

To prove termination, unwrap the original rings as indices -1,0,...,n-1, with original u_(n-1)=1,v_(n-1)=0. Each nonfilling return increases the hole index by 2 and leaves every still-ahead vertex unchanged. Thus all uses of "original" above remain justified before the cap is met.

If n is even, a return from i=n-4 would require original u_(n-2)=1. This is adjacent to the fixed original u_(n-1)=1, impossible. Therefore that block, or an earlier block, takes the filling branch.

If n is odd, a return from i=n-5 would produce II at i=n-3. That return already forces original v_(n-3)=q and original u_(n-2)=p, the two distinct nonpole colours. Together with b=1, these neighbours force original v_(n-2)=0, adjacent to the fixed original v_(n-1)=0, impossible. Therefore that return cannot occur; the filling branch occurs no later than i=n-5. This includes n=5, where a nonfilling first block is already impossible. There is no cyclic wrap or appeal to an unproved global measure.

## Doubled-1 words: finite upper-ring return

The word is (0,1,rho,tau,1). The audited doubled-1 lemma says: if c(v_(i+1))=tau, u_i→v_i fills after one slide; if c(v_(i+1))=0, the three slides

    u_i→v_i→v_(i+1)→u_(i+2)

return (0,1,q,p,1) two indices forward, with p,q the two nonpole colours. The original u_(i+3)=1 is forced in a return.

Unwrap at u_0. Keep original u_(n-1)=1 and original v_(n-1)=tau as the fixed cap; no return before the cap modifies them. Every return consumes two fresh indices. For odd n, the possible last return at i=n-3 would require original u_(n-2)=1 (the forward upper neighbour) and original u_(n-1)∈{rho,tau} (the destination colour), contradicting the cap value 1; equivalently the forward original upper chain has already made two adjacent original vertices colour 1. Therefore a filling branch occurs earlier. For even n, the last possible hole is u_(n-2). Its forward lower vertex v_(n-1) is the untouched nonzero cap colour. The local lemma permits only 0 or its current tau there; hence it is the current tau and the one-slide fill applies. The walk cannot revisit its start.

## Tight-edge words: prepared-zero traversal and terminal cap

Reflection and colour exchange reduce all four words to

    link(u_0)=(0,1,rho,tau,rho).

Original adjacency forces v_(n-2)=0. The two opening slides u_0→v_(n-1)→v_(n-2) produce a prepared hole v_R, R=n-2, with crossed side u_(R+1)=rho,v_(R+1)=0. They rewrite u_0=tau and v_(n-1)=0; the fixed cap also includes u_1=1,v_0=rho.

The original v-ring has a zero. Away from the original hole edge, successive nonzero runs have length 1 or 2: three consecutive nonzero lower vertices would force two adjacent upper vertices to 1. Thus its original gaps between zeros are A (distance 2) or B (distance 3). At the other cap end, either v_1=0 (short cap, L=1), or v_1=tau and v_2=0,u_2=rho (long cap, L=2).

Unwrap the untouched original interval [L,R]. At each ordinary prepared-hole boundary v_j, the crossed vertices have u_(j+1)=rho,v_(j+1)=0; all vertices strictly ahead, toward smaller indices, are still original. Process the next original A/B gap. The independently checked local lemmas give:

* A_rho with outer upper colour 1: immediate fill.
* A_rho with outer upper colour tau: two slides fill, or four slides return at j-2 with the same crossed colour rho.
* A_tau: its only proper orientation returns at j-2 in two slides.
* B_rho: improper because it repeats rho on an upper edge.
* B_tau: four slides return at j-3 with the same crossed colour rho.

No such macro-return modifies vertices below its destination. Consequently the finite number of original gaps still between the hole and L decreases by one at each nonterminal ordinary macro-step. Microsteps need no separate global measure: each macro-step has at most four slides. The algorithm checks for a fill at intermediate states.

### Short cap

If the walk reaches v_1, its link is (1,rho,1,rho,0). Fill with tau. No gap can jump past L: L is an original zero and each macro destination is the next original zero. For n=5, R=3,L=1, so this reasoning uses a single gap with distinct named vertices.

### Long cap

The prepared hole cannot land on v_2: crossed u_3=rho would be adjacent to cap u_2=rho. Consider the last original gap abutting v_2.

If it is B, its only prepared-compatible orientation is B_tau, whose low upper vertex u_3=rho repeats the cap colour on u_2u_3. This is impossible. If it is A_tau, its inner upper vertex u_3=rho makes the same improper edge. Thus the last gap must be A_rho, with right endpoint v_4 and middle v_3=rho. If u_4=1, v_4 already has the three-colour prepared link. If u_4=tau, the first two slides v_4→u_4→u_3 give link (0,1,rho,0,rho), using cap u_2=rho,v_2=0; fill with tau.

For n=5 the long cap is impossible: original v_2=0 and v_(n-2)=v_3=0 would be adjacent. For every n>=6 the remaining long-cap terminal vertices v_2,v_3,v_4 and u_2,u_3,u_4 are distinct. Extra edges from cyclic wrap do not alter the full five-neighbour links, and every step is checked on those links. In particular n=8 causes no unhandled overlap.

The reflected tight-edge case follows from the displayed graph automorphism, not from an assumed directional analogy.

## One common finite-progress principle

Each repeating mechanism consumes a fresh interval of the original belt in its chosen direction: II consumes two upper indices, doubled-1 consumes two belt indices, and prepared-zero consumes one original zero-to-zero gap. The untouched interval shrinks strictly at every nonterminal macro-return; the fixed opening cap forces a fill before a full cyclic circuit. Case I is a one-time reduction into the tight-edge phase. A lexicographic measure is (phase rank, number of still-unprocessed original indices): rank 1 for I and 0 for all stable traversal phases. Only I changes phase, decreasing rank. Each rank-0 return decreases the finite unprocessed count. Bounded microsteps implement a macro transition. This supplies termination for all repeating patterns without asserting that the cyclic hole index itself decreases.

## Result and scope

Subject to independent checking of this assembly and the cited local tile lemmas, every proper unequal-pole deletion colouring at any belt vertex of G_n, n>=5, has a finite sequence of singleton slides using only belt vertices to a three-colour link. Both poles retain their colours. This is a constructive slide-only claim, not a mixed-move fallback and not a new enumeration result. Pole holes and equal-pole starts remain outside this particular theorem.

## Executable named-fixture verification

`team-b-belt-controller.py` implements the constructive policy without shortest-path search and emits original-coordinate slide certificates in `team-b-belt-controller-results.json`. All 19 unequal G5 starts, all 121 unequal G8 starts, and all 807 unequal G11 starts succeed: 947 existing named-fixture starts total. It checks full-neighbour singleton legality and properness after every step, independently replays emitted paths after reflection mapping, and verifies fixed poles and three-colour terminal links. The longest chosen paths are respectively 4,10,14 slides; these are constructive paths, not shortest-distance claims. The audit chat independently implemented the same policy with its own graph/slide routines and reported matching success for all 947 starts. The finite check supports the assembly but does not replace the termination proof above.
