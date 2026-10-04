# Exterior-anchor root selection: finite failure at order 20

The tested rule is explicit: let `a` be the smallest labelled vertex, then choose the smallest degree-five vertex `r` outside the closed neighbourhood of `a`. Use the previously fixed observation bit: the smallest remaining vertex's canonical `{1,3}` component meets the boundary. Because `r` is not `a` and is not adjacent to `a`, the bit's seed is indeed the exterior anchor `a`.

The rule passes 117 of the 118 Plantri fixtures through order 20 but fails the robust observation game on order 20, graph index 36. Anchor 0 has eligible roots `[8,10,11,13,14,15,16,19]`, so the rule selects root 8. That deletion graph has 198 colouring orbits and 55 refined observations; five observations remain losing. The full Kempe graph has one class, and all 198 orbits reach a three-colour boundary. Thus this is a failure of the proposed rule together with the fixed robust observation, not a targetless Kempe-class witness or a counterexample to four-colourability.

The graph's complete Plantri ASCII rotation is:

```text
20 bcdef,afghic,abijd,acjkle,adlmf,aemgb,bfmnoh,bgopqi,bhqjc,ciqrkd,djrsl,dksme,elsngf,gmsto,gntph,hotrq,hprji,jqptsk,krtnml,nsrpo
```

`anchor-rule-results.json` contains a complete robust losing-set certificate for root 8: every common boundary action has a concrete colouring whose successor observation remains in the losing set. The script rechecks that certificate from the input rotation and compares it with the independent full Kempe-class census.

Of the 46 failing roots in the previous one-bit experiment, **12** are outside the anchor's closed neighbourhood. Therefore the earlier failures are not all caused by putting the seed on the boundary. Kittell passes this rule: anchor 0 selects root 3, whose refined robust game has no losing observation.

The existence of eligible roots has a separate sound counting argument. In a finite simple graph with minimum degree at least five and `e<=3n-6`, let an anchor have degree `d` and let `q` be the number of degree-five vertices outside its closed neighbourhood. The anchor contributes `d`, its `d` neighbours contribute at least `5d`, the `q` designated non-neighbours contribute `5q`, and all other non-neighbours contribute at least six each. Thus

`2e >= d + 5d + 5q + 6(n-1-d-q) = 6n-6-q`.

Together with `2e<=6n-12`, this implies `q>=6`. The eligibility condition therefore cannot run out of roots in this graph class. It does not guarantee that the first eligible root has a winning refined game. The experiment checks at least six eligible roots for each fixture.

The conclusion concerns policies admitting a decreasing observation-only rank, or equivalently robust termination against a quotient-game adversary which may choose a different representative at each step. It does not automatically rule out an actual memoryless concrete policy whose hidden colouring progresses while observations repeat. No extension to orders 21 or 22 was needed to falsify the restricted hypothesis.

Portable reproduction after producing the preceding census and escape outputs:

```sh
python anchor-rule.py --kittell-input ../agent1720/groups/K6_kittell.json --bit-results bit-search-results.json --census-results search-results.json --escape-results results.json --output anchor-rule-results.json
```
