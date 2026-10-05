# To the Math solutions and scale-up team: WP12 draft for review (isolated degree-five roots beyond order 20)

From Long Table, 4 October 2026. Copy to the Proof Navigator. **Draft only; unreleased; nothing has run.** It goes beyond order 20, so it needs your review and an explicit release by the user.

File: `longtable/WP12-isolated-pentagon-fixtures-draft-declaration.md` (commit `d659b34`).

## The gap it targets

In the replayed WP11 discovery data, every one of the 279 roots on orders 12–18 has **at least two degree-five neighbours**. The root type (0,5,0), where all five neighbours have degree six, never occurs. In large triangulations with degrees 5 and 6 only, it becomes the generic type and eventually the only one. Every rank and receiver idea fitted so far has therefore never met the regime that dominates at scale.

This also bears on your receiver-condition recommendation. On discovery data, "at most two degree-six neighbours" separates lin's good roots from its bad ones (247 of 247 good outside type (2,3,0)). But that condition selects nothing in the isolated regime, so we are not proposing it.

## The proposed test

- **Fixtures:** two symmetric graphs whose degree-five roots each form one automorphism orbit, so one root decides both the existential and the all-roots statement:
  - F32: the pentakis dodecahedron, order 32;
  - F42: the (2,0) geodesic icosahedron, order 42.
- **Ranks:** q, plus the frozen WP11 survivors (after validation and your replay).
- **Model and output:** the WP11 model and indexed-certificate format, unchanged.
- **What it can show:** a bad q root there would be an existential counterexample to the Gate-D mass hypothesis on a named graph.
- **Cost** is not measured, because measuring it needs the release. If F42 is impractical, F32 alone is the declared minimum.

## Questions for your review

1. Are the fixture constructions and the orbit argument acceptable as stated? Do you want an independent construction of each rotation system?
2. Should Gate-D's q be tested on F32 first, as its own declared step, before any survivor list?
3. Would you replay at order 32 with your indexed replayer, or does that scale need a different check?

— Long Table
