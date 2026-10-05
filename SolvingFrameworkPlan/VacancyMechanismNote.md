# Vacancy motion: the productive move and its exact obstruction

4 October 2026. Internal math inquiry, no inter-team message. The parent supplied the discovery sweeps; this note does not claim to independently replay those sweeps.

## What is now formalized

`PlaneMap/VacancySlide.lean` and `MathlibTest/PlaneMapVacancySlide.lean` compile warning-free against the fresh 79-module overlay. Generic proofs use only `propext`; actual colouring constructions use the standard three axioms.

For ANY simple graph and ANY colour type, a total function proper away from a vacancy r can slide the vacancy to x when the colour at x occurs uniquely among neighbours of r. Set c'(r)=c(x), retain all other values, and treat x as vacant. Properness away from x follows. If rx is an edge, the reverse slide is legal: r is uniquely coloured among neighbours of x. Reversal restores all values away from the original vacancy. The stored value at a vacant vertex is irrelevant. The module also constructs actual colourings of induced deletions and spherical isolate graphs.

No theorem restricts the new vacancy's degree, and no theorem claims progress. Restricting movement to degree-five vacancies is already killed by the order17 graph0 root4 witness.

## A conservation law that explains the new kill

Define the colour population on COLOURED vertices only:

    N_i(r,c) = |{v != r : c(v)=i}|.

A singleton slide replaces one coloured vertex x by r WITH THE SAME COLOUR, so each named N_i is exactly conserved. Colour canonicalization can permute the four entries; their sorted multiset remains conserved. This is a hand proof, not yet a Lean counting theorem.

Consequently, if a slide-only path ends at a fillable vacancy, the graph has a full four-colouring whose population is N+e_i for some i. This gives an obstruction independent of BFS depth, local rank, symmetry or root choice. It is only a necessary condition: compatible population does NOT prove slide reachability.

The parent's new computations find exactly this obstruction: order18 graph10 has 16 failed slide-only starts, each with a complete 32-state vacancy component. Their population is sorted (2,5,5,5); any completion would have sorted (3,5,5,5) or (2,5,5,6), while all full four-colourings have (4,4,5,5). A single Kempe change at a slide-reachable state unlocks each recorded failure.

## This graph is the two-pole family member G8

Independent inspection of the frozen graph adjacency gives degree-eight poles 3 and 6, with no edge between them. Their disjoint induced cyclic neighbours are

    A = [0,2,8,9,10,11,12,4]
    B = [1,5,13,14,15,16,17,7].

They partition all sixteen nonpole vertices. Reversing B's orientation gives the interleaving antiprism edges: each A vertex is adjacent to exactly two consecutive vertices of B. These are precisely two triangulated caps on an eight-antiprism belt, the topology of Florek's G8.

Florek's Lemmas 2.2–2.3 give equal sizes within two colour pairs for G8, with a+b=9 and 4<=b<=floor(16/3)=5. Thus its full colour-population multiset must be (4,4,5,5), proving the obstruction structurally. His Theorem 3.1 establishes bounded Kempe equivalence after deleting a pole, unlike the whole graph. [Primary paper](https://arxiv.org/pdf/2511.00485).

This does not generalize pole-deletion equivalence to arbitrary holes. The deleted degree-five vertex can move, and reaching a pole via singleton slides is a separate obligation. Moving to a pole does not automatically fix an incompatible population: Kempe moves are needed there too.

## Five-colour interpretation

Give the vacant vertex a unique fifth colour *. A legal vacancy slide along rx is EXACTLY a (*,c(x))-Kempe swap whose component is the two-vertex edge {r,x}. Uniqueness at N(r) ensures this, since r is the only * vertex. The number of * vertices stays one.

Thus our proposed move system is a restricted five-colour Kempe reconfiguration system:

- ordinary two-colour swaps among colours 0..3 act on G-r;
- two-vertex fifth-colour swaps move the vacancy;
- a terminal move recolours the unique * vertex with a missing boundary colour.

This perspective makes the missing hypothesis precise. General five-colour Kempe equivalence does not supply a path constrained to one fifth-coloured vertex, and choosing an already existing four-colouring as a target would assume the theorem we want.

## A concrete exploratory target

For every minimum-degree-five spherical triangulation T and every proper four-colouring of T-r at a degree-five root, the following hybrid claim is worth attempting:

    some finite sequence of singleton slides, then zero or one ordinary component
    Kempe swap, then some finite sequence of singleton slides reaches a
    fillable vacancy (either slide segment may be empty).

This is a new, unproved reachability conjecture, NOT a polynomial rank. It strictly differs from fixed-root two-swap descent and survived the discovery starts reported by the parent. The first kill is one starting partial colouring whose ENTIRE singleton-slide component has no target and such that EVERY ordinary component swap at EVERY state of that component leads to another targetless slide component. It needs neither a selected root nor all-roots failure to refute the stated universal-colouring claim.

A sound stronger polynomial theorem would require a named potential on actual (r,c), a polynomial bound on slide search or a directed slide rule, and a proof that a hybrid block lowers that potential. Population mismatch cannot itself be that computable rank unless its allowed target populations are defined structurally; 'distance to the full-colouring population set' imports the unknown solution.

Smallest available adversary: G8 order18 graph10. It already kills slide-only universality. The hybrid conjecture's next hard case should have two independent belt defects requiring two genuinely necessary population-changing Kempe swaps, not merely a longer path inside one belt. No such witness is claimed here.
