# Parallel belt proof review

5 October 2026. Independent audit. Both requested gaps now have complete hand arguments that pass this review: all eight doubled-0 opening words are covered, and the selected walks terminate before wrapping around the belt. This is an unequal-pole, belt-hole result for every n >= 5. Both poles keep their original colours, and the walks use slides only.

## Competing teams and attribution

As requested, Team A and Team B each received both tasks and worked independently. The incentive was lead credit for the first complete argument surviving review. Team A supplied the first complete candidate and its constructive replay passes, so receives lead credit for the competing-team result. Team B supplied a different doubled-0 reduction and an independently checked assembly. Both deserve attribution. Long Table's separate `swarm/belt-joined.md` supplies the joined theorem; this review does not replace its authorship or its files.

Team A reduces the doubled-0 words to two representatives with u_1=1. One moves to the opposite ring and becomes doubled-1 by a graph symmetry. The other reaches the prepared-zero walk. Team B makes v_(n-1)=0 instead: one representative enters the tight-edge walk, while the other has a two-slide upper-ring return. These are different valid strategies; their distance histograms need not agree.

## Opening coverage

A nonfillable belt link has four colours on five vertices, with one colour doubled. Pole adjacency and the three link edges leave exactly 14 words: eight doubled-0, two doubled-1, and four doubled-nonpole. Reflection and exchanging the nonpole colour names reduce the eight missing words to two representatives. Every representative either fills or enters a proved repeating state.

The original gap report was a coverage objection, not a counterexample. These arguments close that objection.

## Why the walks terminate

Every selected macro-return consumes fresh vertices in a fixed, unwrapped interval of the input colouring. The still-ahead vertices retain their original colours. The opening establishes a fixed cap at the opposite end. An ordinary A/B return consumes two or three indices; doubled-1 and Team B's additional doubled-0 return consume two. The cap colours force a fill or make a proposed nonfilling return improper before the interval could wrap.

For prepared zeros, the ordered list of original zero-to-zero gaps shrinks. A short cap gives the three-colour link (1,rho,1,rho,0). A long cap has u_2=rho, which excludes a returned prepared zero at v_2; the final legal A_rho gap fills within two slides. The n=5 long cap would have adjacent original zeros and is impossible.

For doubled-1, the untouched cap u_(n-1)=1,v_(n-1) nonzero blocks the last nonfilling return. The even case takes the one-slide filling branch at its last possible hole. The odd case would force a nonpole colour at u_(n-1), or adjacent original upper vertices coloured 1. Team B's additional doubled-0 recurrence closes by analogous adjacent-1 or adjacent-0 contradictions.

The measure is for the chosen strategy at macro boundaries. It does not claim that every legal slide decreases a potential. Each macro has at most four slides, so macro termination gives an actual finite slide path.

## Independent checks and joined proof

The root audit wrote `audit/belt_strategy_replay.py` without importing either competing controller or Long Table's move code. It constructs and validates the full graph rotation, applies each selected singleton slide on the full neighbour set, checks properness and unchanged poles, and maps certificates back to the original coordinates after any symmetry. Finally it fills the hole and checks every edge of the completed colouring. No breadth-first search is used.

All 947 unequal-pole starts on the already studied named G5/G8/G11 fixtures pass: 19, 121 and 807 starts. The longest chosen paths have 4, 10 and 14 slides, respectively. These are strategy lengths, not shortest distances. Each is within the joined proof's 2n bound. Both competing controllers also pass these same starts; their enumeration shares the audit's independent restricted-growth enumerator, so this is three separately implemented move strategies, not three unrelated enumeration implementations.

I read Long Table's `swarm/belt-joined.md` in full. Its all-14-word opening classification, full Z-state table, rewrite sets, linear invariant, cap contradictions, and 2n bound agree with the arguments above. In its notation the untouched-vertex potential is 2j for Z and 2(n-i)-1 for D. Returns decrease it by 4 or 6; openings and terminal partial steps account for the remaining slides. The distinctness and n=5 arguments prevent using a wrapped local recurrence at the terminal cap. No mathematical gap was found in the unequal-pole assembly. This is a hand review plus regression replay, not compilation or acceptance on behalf of Math.

### Scope of the complete theorem

The equal-pole singleton-star argument in the joined page also checks by inspection: the (A,B)-component of b is exactly b and the B-coloured lower neighbours, and swapping it removes the chosen singleton colour from the hole link. This argument does not require n congruent to 2 modulo 3.

The remaining pole-hole case uses an external result. I checked Theorem 3.1 and the definition H_n=G_n-b in [Florek's primary paper](https://arxiv.org/pdf/2511.00485), printed page 24. It states Kempe connectivity of all four-colourings of the pole-deleted graph, with the residue-dependent bounds quoted by Long Table. A restriction of the joined page's explicit proper full colouring supplies a fillable endpoint. This checks the citation's conclusion, not every step of Florek's proof or an independent classification of all triangulations with the same degree sequence. Exact identification of the family remains a cited dependency. The n=5 pole case needs no connectivity citation: a four-colour ring of length five has a singleton, so the hand reduction already applies.

The two tasks assigned to the competing teams are complete under this review. The whole-family mixed theorem depends on the stated external citation and Math's acceptance; no claim about arbitrary triangulations or historical novelty follows.

## Files and release

The two candidate proofs, two team controllers and their certificate files are under `backgroundMaterial/planemap-structural/longtable/audit/team-a-*` and `team-b-*`. Root certificates are in `belt-strategy-replay-results.json`. `belt-parallel-review.sha256` freezes these files, this review, and the handoff message. No n=14 enumeration, new census, or Lean work was run. All changes belong to the audit; Long Table's joined proof and the Navigator files were left to their owners.
