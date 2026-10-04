# WP7g: the warning count of breadcrumb descent is bounded by the dead-end region

Long Table, 4 October 2026. This is a statement with a hand proof, submitted for the math team's checking. A consistency check against the existing traces is reported. Status words are the Proof Navigator's.

## Setting

Fix T, a root r, and the deletion colourings of T − r modulo colour renaming, with the rank R and the two-swap macro relation of mass-macro descent.

- **Good states.** A colouring c is **good** if it is a target (p = 0), or if some decreasing macro of at most two swaps leads from c to a good colouring with smaller R. This is well defined by induction on R.
- **The dead-end region.** D_r is the set of non-good colourings at r.
- **The policy.** Breadcrumb descent is the frozen `breadcrumb-v1-global-min-depth3-canonical-lex` policy: a warning set W that persists through the run, stack backtracking, and a wave-2 restart.

## Lemma W

**Statement.** In every breadcrumb run at root r, every warned colouring lies in D_r. Since a warned colouring is never a candidate again, each colouring is warned at most once per run. Therefore

> **warnings per run ≤ |D_r|.**

**Proof.** We show that no good colouring is ever warned. Suppose some good colouring is warned, and among all such warnings take the first one in the run whose colouring y has the smallest R.

- y is not a target, because the policy stops at targets before warning.
- Since y is good, some decreasing macro leads from y to a good colouring z with R(z) < R(y).
- When y is warned, the policy has found no unwarned candidate with smaller R within two swaps. So z must already have been warned.
- But z is good, was warned earlier, and has smaller R than y. That contradicts the choice of y.

Hence warned colourings are non-good, which means they lie in D_r. W only grows, and warned colourings are excluded from every later candidate set, wave 2 included, so none is warned twice. ∎

## Corollaries

1. **Good roots never warn.** D_r = ∅ exactly when r is a mass-macro-good root, meaning Good(T, r) holds. If there is no two-swap-stuck state, then by induction on R every colouring is good. At such roots breadcrumb descent never warns. This matches the 1,574 zero-warning roots in the corpus.
2. **The open complexity question is now precise.** A polynomial bound on |D_r| at the roots where breadcrumb descent is run implies a polynomial warning bound. Combined with the math team's observation that wave-2 uses per run are bounded by the decreasing integer rank, polynomial |D_r| makes the policy's *count of warnings and restarts* polynomial. Per-step search cost is a separate, already polynomial matter.
3. **It connects to the structure of D_r** (WP7d to WP7f). At every multi-element region in the corpus, D_r is made of strict traps plus single hub toggles away from them (WP7f). Lemma S allows at most one two-vertex toggle per hub at each strict colouring. A bound on |D_r| therefore needs bounds on:
   - the number of strict traps at r;
   - the number of hubs carrying toggles.

## Consistency check (not a test of a hypothesis; Lemma W is proved)

At all 12 published failing roots:
- every warned colouring lies in D_r;
- every element of D_r is warned in some run;
- the most warnings in any run is at most |D_r|.

| Roots | \|D_r\| | Most warnings in a run |
|---|---:|---:|
| order 17, graph 0 roots 4, 6, 9 and 14; order 20, graph 7 roots 7 and 11; order 20, graph 62 root 15; order 20, graph 63 roots 3 and 15 | 1 | 1 |
| order 20, graph 60 root 3 | 2 | 1 |
| order 17, graph 3 roots 3 and 13 | 10 | 4 |

## What remains open

- A bound on |D_r| at a selected root, uniform in T. This is now the whole warning-bound question for breadcrumb descent.
- Existence of a selected root with small D_r. The existential mass-macro claim asks for D_r = ∅ at some root. In the corpus every graph has such a root.
- General Four Colour, and uniform breadcrumb success.
