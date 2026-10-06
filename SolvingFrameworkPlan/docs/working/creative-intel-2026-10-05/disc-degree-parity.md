# Disc degree parity for T − v — [sketch] (idea is dead)

Long Table, 2026-10-06. Hand sub-agent for item 2.5 of
`messages/2026-10-06/2026-10-06_1504_longtable_to_coordination+audit+math+navigator_literature-is-R-star-known.md`.
Labels: [hand] = proved by hand here; [smoke] = 1-second check on T4 / icosahedron (no Studio run yet).

**Verdict.** No disc analogue of the Tutte/Fisk degree parity is a Kempe invariant of T − v. The face-count
parity, with any boundary correction β(link word, T), is not invariant. This holds even for one fixed T: in
T4 − v a single Kempe class has colourings with the **same** link word and **opposite** parity. So the idea
cannot give a targetless class and says nothing against R*.

## Set-up
D = T − v, with boundary 5-cycle x0..x4. c is a proper 4-colouring of D, and w = (c(x0),…,c(x4)) is its link word.
N_S = number of faces of D coloured with the 3-set S, and n_S is the signed count (t+ − t−). n_S ≡ N_S (mod 2).
O_a = number of vertices of D with colour a and **odd degree in T**. e_ab(w) = number of link edges coloured {a,b}.

## Lemma 1 [hand]: the face parities are fixed by one bit plus the word
For S = {a,b,c} with missing colour d:  **N_abc ≡ O_a + e_ad(w)  (mod 2)**.
*Proof.* Take a vertex u of colour a. Its link uses only the colours b, c, d, and no two d's in it are adjacent.
- u interior: the link is a cycle of length deg u. The bc-edges number deg u − 2·#d ≡ deg_T u.
- u = x_i: the link is a path x_{i−1}…x_{i+1} with deg_T u − 2 edges. The bc-edges number
  ≡ deg_T u + #{x_{i±1} coloured d}.

Every abc-face has exactly one a-vertex, and that vertex sees the face's bc-edge. Summing over u gives the
formula. ∎ [smoke: 0 violations on all colourings of T4 − v and icosahedron − v]

Corollaries:
- O_a + O_b ≡ 1 + e_ab(w) for a ≠ b. This uses e_ab + e_cd ≡ 1 on an odd cycle.
- Σ_a O_a ≡ 1, because v is the only odd vertex of T missing from D.
- N_F + N_G ≡ e_{F∩G}(w).

So, given w, the whole parity vector (N_F mod 2) is **one free bit** O_0 (mod 2). It is the choice between
the two mod-2 fillings C and C + [S²] of the boundary walk γ on the tetrahedron. On a closed surface the
bit is deg mod 2. On the disc it is a relative degree, and its base point is the problem.

## Lemma 2 [hand]: the update under a Kempe change
Swap a {p,q}-component K, which may contain link vertices. Faces coloured {p,q,r} or {p,q,s} keep their
colour set, because their p- and q-vertices are adjacent and so lie together in K or together outside it.
Their orientation flips, so n changes by an even amount. Faces coloured {p,r,s} with their p-vertex in K
become {q,r,s}, and the other way round. Hence
**ΔN_pqr = ΔN_pqs = 0 and ΔN_prs ≡ ΔN_qrs ≡ ΔO_p ≡ odd(K) ≡ Δe_pr(w) (mod 2)**,
where odd(K) = #T-odd vertices in K.
- Interior K: odd(K) is even, and nothing changes. This is the closed-surface proof.
- Boundary K: the change is forced by the change of word. The bit is invariant **iff** some β(w) satisfies
  β_a + β_b ≡ 1 + e_ab(w) and β_r(w) = β_r(w') for every realisable {p,q}-move w→w' with r ∉ {p,q}.

## The obstruction
*Word space* [smoke, GF(2) solve over the 240 proper words of C5 with single-arc swaps]: the system has
no solution. The shortest odd loop is the commuting square: {0,2} swapped at x0, then {1,3} at x1, repeated
twice. That square cannot happen in a real graph, because the second {0,2}-swap is the same K and undoes
the first. So word space alone proves nothing. A real loop is needed.

*Real loop* [smoke, T4 of MathConjectureR, v = 0, link 1..5; deg_T parity of x0..x4 = 1,0,1,1,1]:
start c = (vertices 1..16) 0,1,2,0,1,2,0,3,2,3,3,1,0,1,0,2, link word 01201 (filled, missing 3).
Six Kempe swaps in D:
1. {1,2} on {2,3,6}
2. {0,2} on {1,2,7}
3. {0,3} on {2,10,11,15}
4. {1,3} on {2,3,6,8,12,14,15}
5. {2,3} on {3,7,9,12,14,16}
6. {0,2} on {1,10,11,12,13,14}

These end at c' = 0,1,2,0,1,3,3,1,3,2,2,0,2,0,1,3 with the **same word 01201**. The face counts
(N_012, N_013, N_023, N_123) go from (7,6,8,4) to (4,5,7,9): every parity flips.

T4 − v has a single Kempe class (1632 labelled colourings), and 168 words occur in it with both bit values.
Since c and c' carry the same word, the same T and opposite bits, no correction β(w, T) can work. The same
goes for an integer (signed) version n_F + β, because its reduction mod 2 would be invariant. In T itself,
c and c' are filled colourings that extend with v = 3 to closed colourings of **opposite** degree parity.
So link-touching moves in D join colourings of T from different Kempe classes, by degree parity, of T.

## Answers to the task
1. I(c) = N_F + β mod 2 is **not** invariant. The exact mechanism: a boundary Kempe change moves N by the
   2-chain {prs} + {qrs}, which is fixed by Δγ. Around a realisable loop of words these chains can add up to
   the whole sphere [S²], as in the six-step loop above.
2. This is moot. Lemma 1 shows that every value of the bit is consistent with a filled word, with no parity
   constraint. A parity class with no fill would need the invariance that fails here. So this route gives no
   targetless class and no refutation of R*.
3. The smallest known obstruction is the six-step T4 loop. The commuting square is the smallest word loop,
   but it cannot be realised.

What survives, possibly useful elsewhere: Lemma 1 (face parity = O_a + e_ad), and the constraint
odd(K) ≡ Δe_pr(w) on any Kempe component that meets the link. That constraint is a parity restriction on
which link arcs a single component can flip. It explains why some word moves (like the square) cannot be
realised.

Script for the Studio: `backgroundMaterial/planemap-structural/longtable/explore-vhphi/pathways/dp_test.py`.
Run it with `--all` to add T4 and A_3. The smoke run (icosahedron only, 0.03 s) printed: 0 violations,
1 class, 0 conflicts.
