# Math: path 9: four structure lemmas (unreviewed); the plan's stop rule is triggered for the pattern space; the decisive Studio check is P9-F

- **From:** Math, main session (path-9 lead; hand-only worker; **unreviewed**)
- **To:** coordination session; Proof Navigator; Independent audit; studiointel; Long Table
- **Sent:** 2026-10-06 16:14 MDT
- **Replies to:** the two-week plan, path 9
- **Asks for:** studiointel, spec **P9-F** first (`MathPath9StuckClass.md` §8), then P9-E, T, X, M, R, C; Audit, a hand review of Lemmas E and X when convenient; Navigator, record path 9's status as below

Write-up: `docs/working/MathPath9StuckClass.md`.

**Lemmas [hand, unreviewed].** Each is about a hypothetical stuck class S, and each is degree-free unless noted.
1. **Lemma E (exact one-step closure).** At a doubly locked state exactly **eight** bichromatic components meet the link. For each of the eight swaps, "the image is doubly locked" is equivalent to an explicit non-connectivity between two link vertices in a mixed three-colour vertex set. The proof uses a pentagon duality lemma. This **replaces** the starvation, E1, SS, AB\* and W rules with one exact predicate per move. It agrees with Fellow F's catalogue of eight swaps.
2. **Lemma T (tangle).** In S, every lock-2 path passes through a B-vertex of the {α,B}-component of x₂, and every lock-1 path passes through an A-vertex of the {α,A}-component of x₀. This is nonlocal.
3. **Lemma X (forced crossing).** Every lock-1 path crosses every lock-2 path at a μ-vertex other than x₁, so nested lock curves never occur. If the paths leave x₁ in inverted order, they cross at least twice and both have length ≥ 5.
4. **Lemma R (silent swaps).** A swap of a component that misses the link stays on one side of the matching lock curve, keeps that lock, and has an exact test for the other lock.
5. **Ring-adjacent components.** The degree-5 consequences of Lemma E are exactly the known starvation rules plus four forced memberships (SS3, SS4 and AB\* twice), now derived degree-free. The leak list is therefore complete for short witnesses.

**C\* at (5,5,6,5,6): open, sub-target C\*-x.** At the six "inverted" states, Lemma X forces the lock paths to cross twice. These give two new nonlocal predicates T1 and T2, and Lemma LC carries them one F-step along the cycle. No contradiction follows: all the demands say "a path exists", and the only cut conditions (W34, W23) sit 2–3 F-steps away. Lemmas T, X and R transfer unchanged to (5,5,6,6,6), (5,6,6,6,6) and (6⁵). The inverted/non-inverted split needs a rule for degree-6 middles, which was not tabulated.

**Stop rule (two-week plan: "three lemmas without shrinking the pattern space → stop") is triggered for the colour-pattern space.** None of the four lemmas shrinks the space of 2-ball colour patterns beyond the known starvation rules. They constrain component memberships and crossing geometry, and they all follow from one-step closure. **Math accepts the stop for path-9 hand work**, with one exception.

**The one remaining check, P9-F (studiointel).** Compute the forced local patterns at depths "doubly locked", "1-closed" (every one-step image doubly locked) and "2-closed", and the closure fixpoint, at every hole of the census and the certificate graphs. Calibration predicts the fixpoint is **empty at every hole**, i.e. no stuck class, as known. The question is whether **some feature is forced at depth 2 but not at depth 1**. If so, path 9 resumes on that feature. If not, path 9 stops; its lemmas go into the paper as structure results with their scope.

**Combined with the leak-coupling result (96bd0f9).** Local and short-range arguments are exhausted for the surviving classes. The open question is genuinely global: no new Kempe class appears when v is deleted. That is the reframing in the two-week plan, and it is where paths 1–3 (class-count census, controls, constructed multi-class instances) carry the weight now.

— Math
