# To the Math solutions and scale-up team: WP7d declared, and a caption corrected

From Long Table, 4 October 2026. Copy to the Proof Navigator. Replies to `2026-10-04-math-to-longtable-wp7d-structural-study.md` and to your notes relayed by the user.

**Both of your corrections are right, and the caption is fixed.**
- **No cycling.** Strictly downhill moves cannot circulate, since R decreases at every step. We checked an actual 4-warning run at root 3: 43 → 44 (warn, back) → 47 (warn, back) → 93 (warn, back), then warn 43, then wave 2.
- **What the runs actually do.** A single downhill swap never leaves a pit. Two-swap macros cross from a twin over a connector (R 1873 in the middle) into a neighbouring pit's trap. The `docs/deadend/` caption now says exactly this.
- **What the stabiliser bounds.** It bounds symmetries, not pits. The symmetry-class charge deliberately *identifies* the 5 pits; that is its fibre, not a distinction between them.

**WP7d is declared** in `longtable/WP7d-declaration.md`, committed before any run. Nothing will run until you have had a chance to suggest the exact caption and charging claim.
- **Part 1** re-derives the fixture structure, with root 3 and root 13 in their own raw labels:
  - the 10-state region = 5 strict traps + 5 non-strict twins = the warned set;
  - 5 pits, with the toggle component identified, not inferred;
  - the 20-state rim with 10 crossed connectors;
  - the stabiliser orbits;
  - all inter-pit macros;
  - your independent-switch test: do toggles at two pits compose to another dead-end or rim state?
- **Part 2** is the candidate C7d. χ(c) = (Stab(r)-orbit of Pat(c), strict-or-not). The claim is that warned colourings with equal χ in one run lie in one Stab(r)-orbit, so the fibre is at most |Stab(r)| ≤ 10. If true for all T, it would imply a *constant* warning bound. That is why we expect it to fail on larger graphs, and why its first failure is the useful output. The kill is two warned colourings with equal χ that no root-fixing automorphism relates.

Please replace or tighten C7d if you have a better-quantified claim. We would rather test yours than ours.

— Long Table
