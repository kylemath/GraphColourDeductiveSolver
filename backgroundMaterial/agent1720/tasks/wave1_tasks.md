# Agent 1720 — Wave 1 task cards

**Issued by:** main planning distributor, 27 September 2026.
**Rules:** `backgroundMaterial/agent1720/OPERATING.md`.
**Gate:** critic meeting with the main planning team. No navigator node changes before it.

Why this wave: Agent 1701 worked only Track 1 at the specification level and killed two universal BFS-avoidance conjectures. Tracks 2–7 and the Foundation were never started. This wave starts every track that can run on this machine, and asks one group (S4) to look for routes the roadmap does not list.

---

## M-Kempe (Track 1)

### K4 — Safe paths of length BFS distance + 1, all small triangulations
- **Navigator:** new node `t1-safe-plus1` under `track1`.
- **Statement to test:** for every triangulation $G$ on $n \le 10$ vertices, every vertex $v$ with $\deg v \in \{4,5\}$, and every proper 5-colouring $c$ of $G$ with $c(v)=5$, there is a K1-safe path in $\mathcal{R}(G-v,5)$ of length at most $d(c)+1$ to a colouring of $G-v$ with at most four colours, where $d(c)$ is the BFS distance. Definitions: `backgroundMaterial/agent1701/groups/K3_weaker_spec.md` §1.
- **Output:** smallest failing instance (graph, vertex, colouring, $d$, least safe length) or the counted range where it holds. Also report whether a K1-safe path to a four-colouring of $G-v$ actually yields a 4-colouring of $G$ (i.e. whether $N(v)$ ends on at most 3 colours); if not, state the stronger target that does.
- **Kill:** one instance with no safe path of length $\le d+1$.

### K5 — Kempe reducibility 5→4 and monotone reduction
- **Navigator:** `t1-1`, new node `t1-monotone`.
- **Part A:** for every triangulation $n \le 10$ (extend to 11 if under ten minutes), check $\mathcal{R}(G,5)$ is connected (Meyniel 1978 predicts this for all planar graphs) and that each class contains a 4-colouring.
- **Part B (literature):** Meyniel 1978, Las Vergnas–Meyniel 1981, Mohar 2006, Bonamy–Bousquet–Feghali–Johnson 2019. State precisely: given Meyniel, “every 5-colouring Kempe-reduces to a 4-colouring” is equivalent to the Four Colour Theorem. Label Track 1's root statement as a reformulation if that holds.
- **Part C (new conjecture):** *monotone reduction* — from every proper 5-colouring there is a Kempe sequence along which $|c^{-1}(5)|$ never increases and reaches 0. Test $n \le 10$. Kill: one colouring where it fails.

### K6 — Four-colour Kempe classes at a degree-5 vertex (Kempe's own induction)
- **Navigator:** new node `t1-kempe-class-d5`.
- **Statement to test:** for every triangulation $G$ with $n \le 11$ and every degree-5 vertex $v$, every Kempe class of proper 4-colourings of $G-v$ that contains a colouring using 4 colours on $N(v)$ also contains one using at most 3 on $N(v)$. (If true for all planar $G$, this plus the degree ≤4 cases gives an inductive 4CT proof; it is Kempe's argument with unrestricted swap sequences.)
- **Literature:** Heawood 1890, Errera 1921, Kittell 1935, Tilley 2018 (“Kempe-locking configurations”). Is the statement known false for some larger $G$? Give the smallest known counterexample if any, and verify it computationally if it is small enough.
- **Kill:** one written instance.

---

## M-Algebra (Track 2, Track 7 database)

### A1 — Chromatic polynomial database and roots
- **Navigator:** `t2-2`, `t7-1`, `t7-2`.
- Compute $P(G,k)$ exactly for every triangulation $n \le 11$ (restrict to $n \le 10$ if $n = 11$ exceeds the budget). Record $P(G,4)$, all real roots, the largest real root below 4, and verify Tutte's golden identity $P(T,\varphi+2) = (\varphi+2)\varphi^{3n-10}P(T,\varphi+1)^2$ numerically on each.
- **Literature:** Birkhoff–Lewis 1946 (no real roots $\ge 5$), Woodall, Jackson 1993 (no roots in $(1,32/27]$), Royle 2008 (planar triangulations with real roots arbitrarily close to 4). Track 2's kill criterion says a real root in $(3,4)$ kills the root-bounding approach: decide from the computation and the citation whether that criterion is already met.

### A2 — Deductive positivity results for restricted families
- **Navigator:** `t2-3`, `t2-4`, new node `t2-degenerate`.
- Write complete proofs: $P(G,k) > 0$ for every integer $k \ge d+1$ when $G$ is $d$-degenerate; hence outerplanar and series-parallel graphs have $P(G,4) > 0$; planar graphs have $P(G,k) > 0$ for integers $k \ge 6$ (and $k=5$ via the Five Colour Theorem). Check against A1's data where they overlap. Say plainly which of these are classical and that none reaches $k=4$ for all planar graphs.
- Then look for the strongest *non-trivial* positivity statement at $k=4$ that is provable here (e.g. for planar graphs with some structural restriction) and prove it or record why not.

---

## M-Duality (Tracks 3 and 4)

### D1 — Tait colourings and nowhere-zero 4-flows
- **Navigator:** `t3-1`, `t3-2`, new node `t3-tait`.
- For the dual cubic graph $T^*$ of every triangulation $n \le 10$: count 3-edge-colourings (Tait), nowhere-zero $\mathbb{Z}_2^2$-flows, and nowhere-zero $\mathbb{Z}_4$-flows; check the identities $\#\text{Tait}(T^*) = \#\{\text{nowhere-zero } \mathbb{Z}_2^2\text{-flows}\} = F(T^*,4) = P(T,4)/4$ (labelled colours), and that the $\mathbb{Z}_4$-flow count equals the $\mathbb{Z}_2^2$ count (Tutte: the count depends only on group order). Write the proof of planar Tutte duality ($k$-colourings ↔ nowhere-zero $k$-flows of the dual) in the report, citing the textbook source.
- Write Jaeger's 8-flow theorem proof sketch (two spanning trees / 4-edge-connectivity route) with citation; mark Seymour's 6-flow theorem as literature.

### D2 — Penrose evaluation
- **Navigator:** `t4-1`, `t4-2`, `t4-3`.
- Run and audit `compute/topology/penrose_eval.py`. On every $T^*$ from $n \le 10$ (cubic planar, 16 or fewer vertices), check that the Penrose evaluation equals the Tait count. Then look at the state sum's terms (t4-3): report the distribution of signs of individual terms and whether cancellation occurs; this decides if any positivity mechanism is visible.
- **Literature:** Penrose 1971, Kauffman 1990 (vector cross product), Kauffman–Saleur, Fendley–Krushkal (golden identity via TQFT). Label Track 4's statement as a reformulation if that is what it is.

### D3 — Algebraic edge-colouring (Alon–Tarsi, Nullstellensatz)
- **Navigator:** new node `t3-alon-tarsi`.
- Literature: Alon–Tarsi 1992, Ellingham–Goddyn 1996 (planar cubic 3-edge-colourable graphs are 3-edge-choosable), Jaeger, Matiyasevich's polynomial reformulations, Onn. For small cubic planar graphs compute the relevant graph-polynomial coefficient (or the sign-weighted Tait count) and test whether a sign-invariant identity holds that would give a deductive proof of non-vanishing. State what would be needed.

---

## M-Foundation (Lean 4)

### L1 — Lean toolchain and compile the existing Kempe development
- **Navigator:** `f-spec-lean`, `f1`, `f4`.
- Install `elan` in the user home (not system-wide), toolchain `leanprover/lean4:v4.15.0` per `lean4/KempeReconfiguration/lean-toolchain`, fetch Mathlib with `lake exe cache get`, and run `lake build` in `lean4/KempeReconfiguration`. Time every step. Record errors and `sorry` warnings exactly.
- If the build works, fix compile errors that are local and obvious; do not weaken statements.
- **Blocker rule:** if a download step exceeds ten minutes, record command and elapsed time and stop that step.

### L2 — Foundation files F1–F3
- **Navigator:** `f1`, `f2`, `f3`.
- Write `lean4/FourColor/Foundation/F1_ColoringBasics.lean` (K4 is 4-colourable, not 3-colourable, using Mathlib `SimpleGraph.Coloring`), and a design note for F2 (planarity: which definition, what Mathlib v4.15 has) and F3 (Euler). Survey what Mathlib and the literature already formalize (Gonthier's Coq 4CT, any Lean planarity work) with citations. If L1's toolchain is ready, compile F1; otherwise record that it is unchecked.

---

## M-Frontier (Tracks 5, 6, new)

### S1 — Colin de Verdière (Track 5)
- **Navigator:** `t5-1`, `track5`.
- Literature: Colin de Verdière 1990, van der Holst–Lovász–Schrijver survey; state which cases of $\chi \le \mu + 1$ are known and whether the $\mu \le 3$ case requires the 4CT. Compute a certificate that $\mu(G) \ge 3$ for small planar triangulations with cvxpy or numpy (a Colin de Verdière matrix with corank 3), and test $\chi \le \mu+1$ where both are computable. Decide whether Track 5 is a reformulation.

### S2 — Sheaf cohomology (Track 6)
- **Navigator:** `t6-1`, `track6`.
- Define a precise candidate sheaf (e.g. cellular sheaf of $\mathbb{F}_2$- or $\mathbb{F}_4$-vector spaces whose global sections relate to 4-colourings, or the non-abelian set-valued sheaf with Čech $H^1$). Compute $H^0$, $H^1$ on small planar and non-planar graphs. Kill test: does $H^1$ vanish on some non-4-colourable graph or fail to vanish on a planar one? Colourings are not a linear condition; say what that forces.

### S3 — Discharging and unavoidability audit (new Track 8)
- **Navigator:** new node `track8` "Track 8: Discharging and reducibility".
- Audit `compute/discharging/` and `SolvingFrameworkPlan/Plan1_RefinedDischarging.md`. Run the scripts that exist. Report what they compute, what is claimed, and whether any reducibility check (D- or C-reducibility of the Birkhoff diamond at least) is implemented correctly. Implement a D-reducibility check for the Birkhoff diamond if absent and verify the classical result.

### S4 — New deductive routes survey
- **Navigator:** new nodes under `4ct` for each route that passes the critic.
- Survey reformulations and partial deductive routes not in the roadmap: Tait's Hamiltonian approach (Tutte's counterexample), Hadwiger $K_5$-minor form (Wagner), Kauffman's vector cross product / Spencer-Brown, Birkhoff–Lewis equations, Eliahou's signed colourings, Matiyasevich's probabilistic reformulations, Hajós/Ore, edge-3-colouring via perfect matchings (Petersen / 4CT ↔ every bridgeless planar cubic graph has a perfect matching whose complement is a union of even cycles), the Robertson–Sanders–Seymour–Thomas simplification, and Gonthier's formalization. For each: exact statement, what is known, what would count as progress here, feasibility. Recommend at most three new tracks.
