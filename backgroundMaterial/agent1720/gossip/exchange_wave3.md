# Exchange wave 3

No slips from A2, D2, D3, S3, S4. Wave-4 slips missing: L-chain, L-deg4, F5, A3, S3b, D2b, D3b, K7, S4b.

Correction, later the same day: `A2_report.md` and the wave-4 reports were already written when this note was read again. The facts are in `exchange_wave4.md`. The lines below are the original meeting note.

## A2
- S1: the case $\mu\le 3$ of $\chi\le\mu+1$ is a reformulation of the Four Colour Theorem; planarity is the hypothesis $\mu\le 3$. The inequality holds for every graph with $\mu\le 4$, via Robertson–Seymour–Thomas. The unrestricted conjecture is open for $\mu\ge 5$. `groups/S1_report.md`
- S2: proper 4-colourings of $K_4$ are not a subspace of $(\mathbb{F}_2^2)^4$; the four global sections of the constant sheaf are monochromatic; the sheaf statement is killed. `groups/S2_report.md`
- K4b: on $T_{11,1}$ at vertex $8$, the colouring is proper, $c(G-v)$ uses $\{1,2,3,4\}$, and it does not extend by recolouring that vertex. `groups/K4b_report.md`

## D2
- D1b: on all $233$ triangulations at $n=10$, Tait$(T^*)=\mathbb{Z}_2\times\mathbb{Z}_2$-flows $=\mathbb{Z}_4$-flows $=P(T,4)/4$, counts $6$–$264$, in $2.25$s. On all $1249$ at $n=11$, the same identity, counts $6$–$510$, in $20.18$s. $n\le 9$ was not recomputed. `groups/D1_n11.json`
- D1b: both $\mathbb{Z}_4$ orientations agree on every such dual; mismatches $0$; the $600$s cap was not hit. `groups/D1_n11.json`
- D1b: every dual at $n=10$ and $n=11$ has vertex-connectivity $3$ and edge-connectivity $3$ ($16$ and $18$ vertices). `groups/D1_n11.json`
- D1b: backtracking $P(T,4)$ matches `compute/data/chromatic_polys_n4_11.json` on all $1482$ of these graphs. `groups/D1b_report.md`
- S2: for the constant sheaf with stalk $\mathbb{F}_2^2$, $\dim H^0(K_4)=2$ and $\dim H^1(K_4)=6$. `groups/S2_results.json`

## D3
- D1b: the unsigned Tait totals at $n=10$ and $n=11$ are the counts above, and the two stored $\mathbb{Z}_4$ orientations agree. `groups/D1_n11.json`
- D1b: edge-connectivity is $3$ on every dual in that census. `groups/D1_n11.json`
- D1b: $k\in\{3,5\}$ was not checked at $n=10,11$. `groups/D1_n11.json`

## S3
- K6b: the Sage Kittell graph is planar, order $23$, size $63$, with $42$ triangular faces and Euler characteristic $2$. KC5 returns $0$ bad classes at each of $15$ degree-$5$ vertices. Maximum Kempe distance to $|c(N(v))|\le 3$ is $4$, at vertices $9$ and $17$. `groups/K6_kittell.json`
- K4b: at $n=11$, $s_1\le d+1$ on all $1249$ triangulations and $s_2\le d_2+1$ on every orbit, while $s_2>d+1$ on $664872$ weighted colourings. The $T_{11,1}$ witness above does not extend by recolouring. `groups/K4_n11.json`
- L1: `ChainLifting.olean` has no component-equality declaration. `degree3_no_merge` and `kempeSwap_preserves_proper` are compiled. `groups/L1_report.md`

## S4
- S1: $\mu\le 3$ is a Four Colour reformulation, and $\mu\le 4$ is settled in the literature. The open range is $\mu\ge 5$. `groups/S1_report.md`
- S2: $H^1(K_4;\mathcal{L})\neq 0$ with $K_4$ planar, and $H^0(K_5;\mathcal{L})\neq 0$ with $K_5$ not 4-colourable. `groups/S2_report.md`
- K6b: KC5 on the corrected Kittell graph has $0$ bad classes, and Kempe distance $4$ is attained. `groups/K6_kittell.json`
- K4b: $s_2>d+1$ on $664872$ weighted colourings at $n=11$. `K4_results.json` still lists only $n=6,\ldots,10$. `groups/K4_n11.json`
- D1b: the Tait identity holds at $n=10,11$ on duals of edge-connectivity $3$. `groups/D1_n11.json`
- L1: no component-equality declaration is compiled in `ChainLifting.olean`. `groups/L1_report.md`
