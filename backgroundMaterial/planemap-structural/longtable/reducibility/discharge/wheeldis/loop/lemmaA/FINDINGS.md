# Lemma A as a finite check (16 Oct 2026) [exploratory, engine level: dfast/cfast only, no Lean]

Stream A of the stepped-up exploration loop (EXPLORE-LOG.md, round 5). Scripts and outputs are in this folder.

## Statement (pre-registered 07:47Z; also the docstring of `la.py`)

**A(k).** Let u have degree exactly 7, with link w0..w6 over {5, 6, 7, 8, 9+} and at least k fives (positions F).
- For each j in F ∪ (F−1), the degree σ_j of s_j is given, also over 5..9+. (s_j is the common neighbour of w_j and
  w_{j+1} other than u.)
- The local disc is generic (free completion).

**Hypothesis.** The data force no wheel in R_opt:
- 5-wheels: Job 17 D/C words, plus the D fans and the diamond;
- 6-wheels: Job 17 D/C words, plus 2.122;
- u's own 7-wheel: D, or a cfast C-candidate;
- a wheel with unknown letters counts only if it is bad for every completion;
- untested words containing 8 or 9+ count as not reducible.

**Conclusion.** Some S ⊆ F with |S| >= 2 has K(S) = u + S + N(S) either D (dfast, ring <= 16) or a cfast
C-candidate. In K(S), vertices of degree 5..8 are inside at their exact degree, and 9+ vertices stay on the ring.

**Guess.** A(4) and A(5) hold with D alone at ring <= 15; A(3) fails on 5-15% of situations.

**Builder check.** `la.build` / `la.KS` agrees with the configurations taken from the round-1 patches: 1,507 of 1,507.

## Counts

Canonical up to the dihedral group, with situations that contain an R_opt configuration removed.

| k | full alphabet 5..9+ | degrees <= 7 only |
|---|---|---|
| 6 | 39,360 (links 5555558, 5555559) | 0 |
| 5 | >= 539,648 (listing stopped; ~0.7 M estimated) | 291 (all on link 5557557) |
| 4 | ~3.0 M (sampled) | 2,773 |
| 3 | ~3.1 M (sampled) | ~6.3 k |

dfast cost per configuration by ring: 13 → 1.5 s, 14 → 8 s, 15 → 41 s, 16 → 166 s, 17 → ~1 h (dfast18).

## Verdicts at ring <= 14 (`inst.py`, greedy by ascending ring, D only)

| run | D found | miss |
|---|---|---|
| k = 5, degrees <= 7, exhaustive | 252 / 291 | 39 |
| k = 4, degrees <= 7, sample | 14 / 20 | 6 |
| k = 5, full alphabet, sample | 14 / 38 | 24 |
| k = 4, full alphabet, sample | 1 / 30 | 29 |

- **k = 5, degrees <= 7.**
  - The 39 misses are all on link 5557557, with mostly-7 outer neighbours.
  - Each still has untested candidates: 165 at ring 15 and 196 at ring 16.
  - cfast at ring <= 12 rescues 1 of them.
- **k = 4, full alphabet.** The misses' candidates are mostly at ring 17-19 or >= 20. One miss has no candidate
  below ring 18.

## k = 3 (`bf3.py`, from the round-1 patch instances)

- 421 instances:
  - 290 have a D configuration at ring <= 15;
  - 87 have none (all candidates up to ring 15 tested; cfast rescues 3);
  - 44 are open, waiting on 33 untested ring-15 configurations (`k3_need15.txt`).
- Shapes of the 87 (positions of the three fives): (1,1,5) a block of three fives: 36; (1,3,3): 27; (1,2,4): 15;
  (2,2,3): 9.

## Kernels (`kern.py`)

Greedy vertex deletion, keeping D, on 40 k = 5 hits at ring <= 11. They collapse to 5 kernels:
- **29 of 40:** a ring-9 kernel: u = 7, fives at w0, w1, w2, with s0 = 5, s1 = 7, s2 = 5.
- **7 of 40:** a second ring-9 kernel.
- 4: three kernels at rings 10-11.

## Reading

1. **A blanket lemma A is not available.**
   - With outer neighbours of degree 8 or 9+, ~97% of k = 4 situations miss at ring <= 14.
   - Their candidates sit at ring >= 17, which is about 10^6 CPU-h.
   - Even the degree <= 7 version has 39 open k = 5 cases.
2. **Why round 1's 186/186 doesn't carry over.** Round 1 sampled 7s inside 6-sea defect patches. There the
   neighbourhood is mostly 6s, which is the regime the defect search covers, not every neighbourhood.
3. **Consequences for the K = 2 plan.**
   - It has to stay defect- and LP-driven (Job 28): test only the neighbourhoods the LP or the defects actually use.
   - The defect search itself uses degrees 5-7 only, so defects that contain a vertex of degree >= 8 are an open gap
     (G9).
4. **Two candidates.**
   - The ring-9 kernel is a small, Lean-cheap reducible configuration.
   - Two reformulations to try:
     - keep every vertex of degree >= 8 free on the ring;
     - add a rule that sends a five's charge to an adjacent vertex of degree >= 8.

## Job spec

- Stage 1, degrees <= 7: `inst.py SITFILE 19 TAG cfast` (dfast18 is used above ring 16).
  - The 39 k = 5 misses: <= 11 CPU-h.
  - k = 4 (2,773 situations): ~2 h at ring <= 14, plus up to ~90 h at rings 15-16.
- Stage 2, degrees 8 and 9+: infeasible as a blanket run. Reformulate first (point 4).
