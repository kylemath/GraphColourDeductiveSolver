# WP20 output format and conventions

Part of the WP20 declaration (`WP20-D1-declaration.md`). The producer writes one JSON file per phase; the independent checker recomputes from the plantri input and compares.

## Conventions (fixed)

- A **state** is a tuple of $n$ integers, one per vertex $0..n-1$ of $T$ in plantri label order. Entry $x$ (the hole) is `4`. Every other entry is a colour in $\{0,1,2,3\}$, **canonical**: colours are renamed in order of first occurrence over the vertices $0,1,\dots,n-1$ with $x$ skipped (so the first non-hole vertex has colour $0$, and so on).
- A **colouring of $G=T-xr_j$** is a tuple of $n$ integers in $\{0,..,3\}$, canonical in the same way **with $x$ included** (vertex order $0..n-1$, nothing skipped).
- Vertex labels are the plantri letters `a=0, b=1, ...`; the rotation at a vertex lists its neighbours in plantri order. Graph indices are 0-based in plantri output order. The ring of $x$ is the rotation at $x$.
- `depth` of a SEP-bad state: breadth-first search over all states of $T-x$ (filled or not) joined by pure Kempe swaps; the depth is the least $k\in\{1,2,3\}$ such that a state at pure distance $k$ is **good** (unfilled, with a legal admitting fan, and separable for some admitting legal fan); otherwise `">3"`.
- `states` counts unfilled states with at least one legal admitting fan. `no_legal_fan` counts unfilled states with none. `unfilled_total = states + no_legal_fan`.
- P is evaluated for every unfilled state, including the `no_legal_fan` ones, using connected components of the pure Kempe graph on all states of $T-x$ (filled and unfilled). A component with no filled state kills P for all its unfilled states. A component of more than 200,000 states is `capped`.
- `locked_classes`: the number of pairs (legal fan $j$, Kempe class of colourings of $G=T-xr_j$) such that the class contains at least one colouring and every colouring in it has $c(x)=c(r_j)$.

## File schema

```
{
 "wp": "WP20", "phase": "P1", "order": 25,
 "declaration_sha256": "...", "input_sha256": "...",
 "producer_sha256": {"d1_confirm.py": "..."},
 "graphs": [
   {"index": 0, "ascii": "25 bcdef,...", "status": "complete" | "interrupted",
    "vertices": [
      {"x": 3, "status": "complete" | "interrupted" | "capped",
       "unfilled_total": N, "states": N, "no_legal_fan": N,
       "sep_bad": N,
       "depth": {"1": N, "2": N, "3": N, ">3": N},
       "filled_neighbour_for_bad": N,
       "d1_kills": N, "p_kills": N, "p_capped": N,
       "locked_classes": N,
       "legal_fans": [j, ...]}
    ]}
 ],
 "witnesses": {
   "sep_bad": [{"index": i, "x": v, "state": [n ints], "depth": 1 | 2 | 3 | ">3"}],
   "d1_kills": [{"index": i, "x": v, "state": [n ints]}],
   "p_kills": [{"index": i, "x": v, "state": [n ints]}]
 },
 "truncated": false
}
```

`filled_neighbour_for_bad` counts SEP-bad states that have at least one filled pure neighbour (recorded, not good). `depth` counts only SEP-bad states. Vertices of degree other than 5 are omitted.
