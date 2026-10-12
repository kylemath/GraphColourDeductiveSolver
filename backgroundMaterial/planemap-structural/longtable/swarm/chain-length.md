# Chain length after a vacancy landing

**Verdict: KILL.** The worst chain is order 20, graph 7, failing root 7, stuck orbit 180. The lexicographically shortest vacancy path is $1 \to 0$, landing at root 0 on a descending orbit with $q=252$ and $R=2653$. The slowest greedy rule takes 6 macros there. The first macro drops $R$ by 43. The peak $R$ is 2653. The walk revisits canonical colouring 183. On macro 3 the first swap reaches $p=0$ at colouring 24 with $R=188$, and the second swap leaves it for colouring 194 with $p=1$ and $R=2597$.

The kill is that repeated colouring. The same 21 landings, under the smallest-index rule, all reach $p=0$ in at most 3 macros, and the revisited flag is no on every one of them. Landing $q$ runs from 111 to 252 while the macro counts run from 1 to 6, and $p$ hits 0 while $q$ is still in the hundreds, so the length is a small integer beside $q$.

## Census

Recomputed from `mass-macro-results.json` and `mass_core.RootState`, using the vacancy slide in `inquiry_slide.py`. The published table has 12 failing roots. They carry 21 orbits with $p=1$ whose `descent(i, 2)` witness is present. Each has a vacancy path of length at most 2 that lands on a descending orbit at a passing root. Fifteen shortest paths have length 1 and six have length 2. Every chosen landing still has $p=1$.

Among paths of that minimum length, the row below uses the lexicographically smallest tuple of slide vertices. A slide places the deleted root on the colour of a neighbour of unique boundary colour, then deletes that neighbour.

$R=(6n^2+1)\,p+q$. The scale is 1735 on 17 vertices and 2401 on 20 vertices. The first drop is the fall in $R$ from the landing colouring to the endpoint of the first macro. The peak is the largest $R$ on the walk, including the intermediate colouring of a length-2 macro. The revisited flag is yes when a canonical colouring index occurs twice on that walk.

Smallest-index rule. Among length-1 macros that lower $R$, take the least successor index. If no length-1 macro lowers $R$, among length-2 macros that lower $R$, take the lexicographically least pair of successor indices.

Slowest greedy rule. Among length-1 and length-2 macros that lower $R$, take an endpoint of largest $R$. Ties break by the least endpoint index, then the shorter macro, then the lexicographically least successor pair.

A swap that returns the same canonical colouring is skipped. Selecting the length-2 macro by its position in the move list, instead of by successor indices, leaves the macro counts, the first drops, and the revisited flags unchanged. On two chains the peak falls from 1890 to 1878, because the intermediate colouring of the last macro is different. The maximum length stays 3.

## The 21 chains

Orbit is the canonical colouring index at the failing root. Path is the vacancy slide. Landing is the root where the macros run, and $q$ is the mass at that landing colouring.

| order | graph | root | orbit | path | landing | $q$ | macros | first drop | peak $R$ | revisited? | slow macros | slow first drop | slow peak $R$ | slow revisited? |
| ---: | ---: | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: | ---: | --- |
| 17 | 0 | 4 | 25 | $3 \to 2$ | 2 | 143 | 3 | 12 | 1878 | no | 3 | 12 | 1878 | no |
| 17 | 0 | 6 | 27 | $5 \to 0$ | 0 | 155 | 2 | 29 | 1890 | no | 6 | 1 | 1890 | yes |
| 17 | 0 | 9 | 18 | $3 \to 2$ | 2 | 143 | 2 | 68 | 1890 | no | 4 | 32 | 1878 | yes |
| 17 | 0 | 14 | 21 | $7 \to 2$ | 2 | 143 | 2 | 68 | 1890 | no | 4 | 32 | 1878 | yes |
| 17 | 3 | 3 | 44 | $0$ | 0 | 111 | 1 | 1692 | 1900 | no | 1 | 1692 | 1900 | no |
| 17 | 3 | 3 | 47 | $2$ | 2 | 111 | 1 | 1692 | 1900 | no | 1 | 1692 | 1900 | no |
| 17 | 3 | 3 | 77 | $0$ | 0 | 123 | 1 | 1723 | 1890 | no | 1 | 1723 | 1890 | no |
| 17 | 3 | 3 | 91 | $2$ | 2 | 123 | 1 | 1723 | 1890 | no | 1 | 1723 | 1890 | no |
| 17 | 3 | 3 | 93 | $0$ | 0 | 111 | 1 | 1692 | 1900 | no | 1 | 1692 | 1900 | no |
| 17 | 3 | 13 | 19 | $6$ | 6 | 111 | 1 | 1692 | 1900 | no | 1 | 1692 | 1900 | no |
| 17 | 3 | 13 | 29 | $7$ | 7 | 111 | 1 | 1692 | 1900 | no | 1 | 1692 | 1900 | no |
| 17 | 3 | 13 | 52 | $6$ | 6 | 123 | 1 | 1723 | 1890 | no | 1 | 1723 | 1890 | no |
| 17 | 3 | 13 | 76 | $7$ | 7 | 123 | 1 | 1723 | 1890 | no | 1 | 1723 | 1890 | no |
| 17 | 3 | 13 | 96 | $6$ | 6 | 111 | 1 | 1692 | 1900 | no | 1 | 1692 | 1900 | no |
| 20 | 7 | 7 | 180 | $1 \to 0$ | 0 | 252 | 2 | 52 | 2653 | no | 6 | 43 | 2653 | yes |
| 20 | 7 | 11 | 18 | $10 \to 9$ | 9 | 252 | 2 | 52 | 2653 | no | 6 | 43 | 2653 | yes |
| 20 | 60 | 3 | 93 | $2$ | 2 | 177 | 2 | 6 | 2665 | no | 2 | 6 | 2584 | no |
| 20 | 60 | 3 | 169 | $0$ | 0 | 192 | 1 | 2365 | 2653 | no | 2 | 6 | 2616 | no |
| 20 | 62 | 15 | 83 | $8$ | 8 | 164 | 1 | 2324 | 2659 | no | 1 | 2324 | 2659 | no |
| 20 | 63 | 3 | 189 | $0$ | 0 | 164 | 1 | 2324 | 2659 | no | 1 | 2324 | 2659 | no |
| 20 | 63 | 15 | 197 | $6$ | 6 | 164 | 1 | 2324 | 2659 | no | 1 | 2324 | 2659 | no |

Smallest-index lengths: 14 chains of 1 macro, 6 of 2, and 1 of 3. Maximum 3. Slowest-greedy lengths: 13 of 1, 2 of 2, 1 of 3, 2 of 4, and 3 of 6. Maximum 6. Every other shortest vacancy landing, followed by the smallest-index rule, also finishes in at most 3 macros with the revisited flag no.

## The five repeated colourings

Each macro endpoint has strictly smaller $R$ than the previous endpoint, so the endpoints are distinct. The repeated index is a colouring that already appeared inside a length-2 macro.

- Order 17, graph 0, root 6, orbit 27, landing 0. Six macros, first drop 1, peak $R=1890$. Colouring 36 is the intermediate of macro 1 and the endpoint of macro 5. The $q$ trace of the endpoints is $155, 154, 143, 142, 134, 126, 167$.
- Order 17, graph 0, root 9, orbit 18, landing 2. Four macros, first drop 32. Colouring 53 is the intermediate of macro 1 and the endpoint of macro 3.
- Order 17, graph 0, root 14, orbit 21, landing 2. Four macros, first drop 32. Same return, to colouring 53 at that landing root.
- Order 20, graph 7, root 7, orbit 180, landing 0. Six macros, first drop 43, peak $R=2653$. Macro 3 is the swap pair $63 \to 24 \to 194$: colouring 24 has $p=0$ and $R=188$, then colouring 194 has $p=1$ and $R=2597$. Macro 5 then returns to colouring 183, the intermediate of macro 4. Endpoint $q$ runs $252, 209, 204, 196, 175, 168, 249$.
- Order 20, graph 7, root 11, orbit 18, landing 9. Six macros, first drop 43, peak $R=2653$. Colouring 25 is an intermediate of macros 3 and 4 and the endpoint of macro 5.

The length-2 macro is allowed to do this because the rule scores the endpoint. $R=2597$ at $p=1$ is larger than $R=188$ at $p=0$, so the slowest greedy keeps the second swap.

## Bound against $q$

The longest smallest-index chain, order 17 graph 0 root 4 orbit 25, has endpoint $q$ trace $143, 131, 115, 159$. The longest slow chains still have $q$ above 100 at every $p=1$ state, and the successful state has $q=249$ or $q=167$. A landing with $q=164$ finishes in one macro under both rules. A landing with $q=143$ takes three under the smallest-index rule. Spearman rank correlation of landing $q$ with macro count is 0.52 for the smallest-index rule and 0.65 for the slowest greedy rule.

Feasibility of a short rescue that accepts an arbitrary lowering macro: **Low**.

Next step: name the macro. On these 21 orbits the smallest-index rule reaches $p=0$ in at most 3 macros, with the revisited flag no. That is the only rescue-shaped statement this census supports.
