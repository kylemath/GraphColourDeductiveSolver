# Discharging Lemma for the 5/6/7 Sub-World at $t = 0$

> **Verification & Reproducibility Note**: Every row count, distinct-row count, tightest-row label, maximum final charge, and exact rational slack in this document is verified in exact ` fractions.Fraction` arithmetic against [`primal_t0_exact.json`](file:///Users/kylemathewson/GraphColouringNov/pack/W6-rule-grammar/round7/primal_t0_exact.json) and [`dual_t0_exact.json`](file:///Users/kylemathewson/GraphColouringNov/pack/W6-rule-grammar/round7/dual_t0_exact.json) by [`phase0_check.py`](file:///Users/kylemathewson/GraphColouringNov/phase0_check.py) and exported in machine-readable form in [`case_tables.json`](file:///Users/kylemathewson/GraphColouringNov/agents/agent4_lemma/case_tables.json).

---

## 1. The 5/6/7 Sub-World and the Discharging Schemas

### 1.1 The Sub-World and Admissibility Frontier

Let $G = (V, E, F)$ be an internally 6-connected planar (or toroidal) triangulation with minimum degree $\delta(G) \ge 5$ that contains no reducible configuration from the Studio-full / A97 reducibility set $\mathcal{R}$. Following the classical Euler discharging method, we assign to every vertex $v \in V$ the initial charge
$$\text{ch}_0(v) = 6 - d(v),$$
so that $\sum_{v \in V} \text{ch}_0(v) = 6|V| - 2|E| = 6\chi(\Sigma)$ equals $+12$ on the sphere $\mathbb{S}^2$ and $0$ on the torus $\mathbb{T}^2$. Specifically:
- **Degree-5 vertices (Senders, $S$)** start with initial charge $\text{ch}_0(v) = +1$ and must discharge at least $1$ unit of net outflow ($\text{outflow}(v) \ge 1$, so $\text{ch}_{\text{final}}(v) = 1 - \text{outflow}(v) \le 0$).
- **Degree-6 vertices (Relay / Conservation, $C$)** start with initial charge $\text{ch}_0(v) = 0$ and must be net-conservative ($\text{inflow}(v) - \text{outflow}(v) \le 0$, so $\text{ch}_{\text{final}}(v) \le 0$).
- **Degree-7 vertices (Receivers, $R_7$)** start with initial charge $\text{ch}_0(v) = -1$ and can absorb at most $1$ unit of net inflow ($\text{net\_inflow}(v) \le 1 - t$ at target margin $t$; at $t = 0$, $\text{net\_inflow}(v) \le 1$, so $\text{ch}_{\text{final}}(v) = -1 + \text{net\_inflow}(v) \le 0$).

The **5/6/7 sub-world** isolates the core regime where the local neighbourhood around every receiver consists exclusively of vertices of degrees $\{5, 6, 7\}$:
1. **Receivers ($d = 7$)**: A degree-7 vertex $v$ is described by its cyclic 1-ball $(w, s) \in \{5,6,7\}^7 \times \{5,6,7\}^7$ up to dihedral symmetry $D_7$, where $w = (w_0,\dots,w_6)$ is the cyclic sequence of neighbour degrees in $N(v)$ and $s = (s_0,\dots,s_6)$ is the cyclic sequence of outer apex degrees of the 7 triangles Sharing two consecutive neighbours $(w_i, w_{i+1})$ with $v$. After pruning configurations killed by local reducibility rules (`R5`, `R6`, `RBIG`, `adj_ok`, `wheel_ok`, and Studio-full / A97 $d \le 7$ subsets in [`tables_bundle.zlib`](file:///Users/kylemathewson/GraphColouringNov/tables_bundle.zlib)), there are exactly **$110,087$** admissible degree-7 receiver labels (`109,592` distinct linear inequalities).
2. **Senders ($d = 5$)**: A degree-5 vertex $u$ is described by its cyclic neighbour word $w = (w_0,\dots,w_4)$, its binary hat vector $H = (H_0,\dots,H_4) \in \{0,1\}^5$ (where $H_k = 1$ indicates that the outer apex $s_k$ of the face $(u, w_k, w_{k+1})$ has degree $5$, and $H_k = 0$ indicates $s_k \in \{6,7,8,9\}$), and for each $k$ with $w_k = 6$, its binary far-private bit $F_k \in \{0,1\}$ (indicating whether the private neighbour of the degree-6 vertex $w_k$ opposite $u$ has degree $5$ or $\ge 6$). Because `R5` kills every 5-wheel whose neighbours all have degree $\le 6$, every admissible sender has $b = n_{\text{big}}(w) = |\{k : w_k \ge 7\}| \in \{1, 2, 3, 4, 5\}$.
   - Across the full alphabet $w \in \{5,6,7,8,9\}^5$, there are **$342$** non-`R5` canonical 5-words, generating **$26,280$** admissible `(w, H, F)` sender labels (**$22,514$** distinct rows).
   - Restricted to $w \in \{5,6,7\}^5$, there are **$24$** non-`R5` canonical 5-words, generating **$2,840$** raw `(w, H, F)` labels, which base-deduplicate to the **$2,020$** sender labels stored in [`world_567_7_std.pkl`](file:///Users/kylemathewson/GraphColouringNov/pack/W16-zero-euler/data/world_567_7_std.pkl) (**$2,038$** distinct rows when the 87 2-ball `EDGE` keys are included).
3. **Degree-6 Relay (`cons2`, $d = 6$)**: A degree-6 vertex $v$ is described by its cyclic neighbour word $L = (L_0,\dots,L_5)$ (non-`R6`) and its coarsened apex-class word $s \in \{5, 7\}^6$ up to dihedral symmetry $D_6$ (where $5$ denotes $s_i = 5$ and $7$ denotes $s_i \ge 6$).
   - Across $L \in \{5,6,7,8,9\}^6$, there are **$1,424$** non-`R6` canonical 6-words, generating **$81,136$** `(L, s)` labels, of which **$81,135$** are non-empty (only `C 666666/555555` has a identically zero row $0 \le 0$) and **$80,148$** are distinct non-empty rows.
   - Restricted to $L \in \{5,6,7\}^6$, there are **$61$** non-`R6` canonical 6-words (`48` with at least one $5$ or $7$ where base variables are active), generating **$2,838$** raw `(L, s)` labels (**$2,837$** non-empty; **$2,803$** distinct rows), which base-deduplicate to the **$1,984$** `cons2` labels in [`world_567_7_std.pkl`](file:///Users/kylemathewson/GraphColouringNov/pack/W16-zero-euler/data/world_567_7_std.pkl).

---

### 1.2 The Base Discharging Variables and `mrow` Closure

In the base discharging system (implemented in [`phase0_check.py`](file:///Users/kylemathewson/GraphColouringNov/phase0_check.py#L267-L407)), charge is transferred between adjacent vertices and across triangles via eight families of non-negative primal variables:

| Variable Family | Role & Transfer Channel | Sender / Relay / Mrow Appearance | Receiver ($d = 7$) Appearance |
| :--- | :--- | :--- | :--- |
| `y`, `z`, `zr` | **Direct $5 \to 7$ edge transfer**: net transfer along a $(5, 7)$ edge with local 5-link root `rootw` and hat bits $(h_r, h_l)$ is $T_{5\to 7} = y(\text{root}) + z(zk) - zr(zk)$. | In $S$ (`sender_row`): $+y + z - zr$ for each $w_j \ge 7$. | In $R_7$ (`recv_row`): $+y + z - zr$ for each $w_i = 5$. |
| `r`, `rr` | **Hat transfer ($5 \leftrightarrow \text{apex } 5$)**: net transfer between a central vertex and an outer triangle apex $s_i = 5$ across edge $(w_i, w_{i+1})$ is $r(hk) - rr(hk)$. | In $S$: $+r(hk) - rr(hk)$ for each $k$ with $H_k = 1$ ($s_k = 5$). | In $R_7$: $+r(hk) - rr(hk)$ for each $i$ with $s_i = 5$. |
| `g` | **First-hop relay ($5 \to 6$)**: charge sent from a degree-5 vertex to a degree-6 neighbour $w_k = 6$, indexed by the coarsened 6-wheel signature `g2_raw`. | In $S$: $+g$ for each $w_k = 6$. In $C$ (`cons2_row`): $+g$ for each $L_i = 5$. | Does not appear in $R_7$. |
| `h`, `M` | **Second-hop relay ($6 \to 7$)**: charge sent from a degree-6 vertex to a degree-7 neighbour (`h`), received at $R_7$ via the masked credit variable `M` (which knows only the admissible bitmask `mk` of the 6-vertex's private neighbour). | In $C$: $-h(hk)$ for each $L_i \ge 7$. In `mrowR2`: $+h(hk) - M(sg) \le 0$ for each $hk \in \text{cand2}(sg)$. | In $R_7$: $+M(sg)$ for each $w_i = 6$. |
| `x` | **Antisymmetric $7 \leftrightarrow 7$ edge transfer**: across a $(7, 7)$ edge, the oriented pair $(\tau_{\text{in}}, \tau_{\text{out}})$ transfers $x(\tau_{\text{in}}) - x(\tau_{\text{out}})$. | Does not appear in $S$ or $C$. | In $R_7$: $+x(\tau_{\text{in}}) - x(\tau_{\text{out}})$ for each $w_i = 7$. |
| `q`, `Q7` | **Masked $7 \to 7$ wheel-credit transfer**: a 7-vertex pays $q(qk)$ to each 7-neighbour based on its own full 7-wheel $qk$, and receives $Q_7(sg_7)$ from each 7-neighbour based on the masked signature $sg_7$ (with private-degree bitmasks $m_1, m_2 \subseteq \{5,6,7,8,9\}$ computed from `MASK` and `f2b_extra`). | In `mrowQ`: $+q(qk) - Q_7(sg_7) \le 0$ for each $qk \in \text{q7cands}(sg_7)$. | In $R_7$: $-q(qk) + Q_7(sg_7)$ for each $w_i = 7$. |
| `lq`, `lQ` | **Masked $7 \to 7$ half-side credit transfer**: for each $w_j = 7$ and each orientation $\sigma \in \{+1, -1\}$ with $(w_{j+\sigma}, w_{j+2\sigma}) \in \{5,6\}^2$, $R_7$ pays $lq(w_{j+\sigma}, w_{j+2\sigma}, w_{j+3\sigma})$ and receives $lQ(c, a, m_7)$ whenever $(c, a) = (w_{j+\sigma}, s_{j,\sigma}) \in \{5,6\}^2$. | In `mrowL`: $+lq(c, a, a_2) - lQ(c, a, m_7) \le 0$ for each $a_2 \in m_7$. | In $R_7$: $-lq + lQ$ for each $w_j = 7, \sigma \in \{\pm 1\}$. |

The three **masked-credit closure (`mrow`)** families enforce conservation across information loss: because a receiver $R_7$ inspecting a neighbour $w_i \in \{6, 7\}$ only sees the neighbour's shared link/apex degrees and a reducibility bitmask of its hidden private degrees, the credit received at $R_7$ ($M$, $Q_7$, or $lQ$) cannot exceed the minimum payment ($h$, $q$, or $lq$) over all admissible completions of that bitmask:
$$M(sg) \le \min_{hk \in \text{cand2}(sg)} h(hk), \qquad Q_7(sg_7) \le \min_{qk \in \text{q7cands}(sg_7)} q(qk), \qquad lQ(c,a,m) \le \min_{a_2 \in m} lq(c,a,a_2).$$
Across all keys active in the 5/6/7 world, `mrow_closure` generates **$3,401$** inequalities: **$1,496$** `mrowR2` rows, **$1,856$** `mrowQ` rows, and **$49$** `mrowL` rows.

---

### 1.3 The 2-Ball `EDGE` Rule Grammar and Sure-Out / Possible-In Conservation

As established in [`W16-zero-euler/REPORT.md`](file:///Users/kylemathewson/GraphColouringNov/pack/W16-zero-euler/REPORT.md) and [`W6-rule-grammar/round7/REPORT_B2.md`](file:///Users/kylemathewson/GraphColouringNov/pack/W6-rule-grammar/round7/REPORT_B2.md), the base 1-ball discharging LP (even with `Q7` and `lQ` masked credits) has a strictly positive dual floor $t^* = -0.025279716$ (equivalently $D = +0.025279716 > 0$ in [`x567SO_all_summary.json`](file:///Users/kylemathewson/GraphColouringNov/pack/W16-zero-euler/certs/x567SO_all_summary.json)) because 1-ball rules cannot see enough of the 2-ball across an edge to distinguish bottleneck configurations from benign ones.

To reach $t = 0$, [`primal_t0_exact.json`](file:///Users/kylemathewson/GraphColouringNov/pack/W6-rule-grammar/round7/primal_t0_exact.json) augments the base variables with **$87$** non-negative 2-ball edge-transfer variables $E_{\text{nm}} \ge 0$ (`A1, KS, N1`, and `gk00_*` through `gk04_*`), specified in [`KEYSPEC.md`](file:///Users/kylemathewson/GraphColouringNov/pack/W6-rule-grammar/round7/KEYSPEC.md). Each rule has the syntax
$$\texttt{EDGE}(P \to Q)\big[\text{pred}_1\ \text{pred}_2\ \dots\big],$$
representing a directed transfer of magnitude $E_{\text{nm}} \ge 0$ along an oriented edge $(u \to v, \sigma)$ from payer $u$ (with $d(u) \in P$) to payee $v$ (with $d(v) \in Q$) with side orientation $\sigma \in \{+1, -1\}$, conditioned on up to 10 relative 2-ball positions:
- `S.L+1, S.L+2, S.L+3, S.L-1, S.L-2, S.L-3` (degrees on the payer's link relative to $v$),
- `S.A+1, S.A-1` (outer triangle apexes on the payer's side), and
- `R.L+2, R.L-2` (degrees on the payee's link two steps from $u$).

Because each row of the LP knows only the local picture of a single vertex ($S$, $C$, or $R_7$), every position in an outgoing or incoming slot carries a 5-bit mask $m \subseteq \{5,6,7,8,9\}$ of *admissible* degrees. To guarantee that charge is conserved on every concrete triangulation without introducing additional `mrow` rows, every `EDGE` rule is evaluated under the **sure-out / possible-in** rule ([`phase0_check.py`](file:///Users/kylemathewson/GraphColouringNov/phase0_check.py#L613-L622)):
1. **Payer (`OUT` slot — sure match)**: An outgoing half-edge slot $(u \to w_i, \sigma)$ pays $E_{\text{nm}}$ if and only if for every predicate `(pos, mask)` in the rule, the slot's admissible mask at `pos` is a **subset** of `mask` ($\text{slot}[\text{pos}] \subseteq \text{mask}$). Thus, if $u$ pays in the LP, $u$ is *guaranteed* to match the rule in every valid triangulation extending $u$'s picture.
2. **Payee (`IN` slot — possible match)**: An incoming half-edge slot $(w_i \to v, \sigma)$ receives $E_{\text{nm}}$ whenever for every predicate `(pos, mask)` in the rule, the slot's admissible mask at `pos` **intersects** `mask` ($\text{slot}[\text{pos}] \cap \text{mask} \ne \emptyset$). Thus, if $w_i$ can *possibly* pay $v$ in any valid triangulation extending $v$'s picture, $v$ is charged with receiving $E_{\text{nm}}$ in the LP.

Consequently, on any concrete edge $(u \to v, \sigma)$ of a valid triangulation $G$, if the true 2-ball matches the rule, then $\text{slot}_u[\text{pos}] \ni \text{deg}_{\text{true}}(\text{pos}) \in \text{mask}$ and $\text{slot}_v[\text{pos}] \ni \text{deg}_{\text{true}}(\text{pos}) \in \text{mask}$. If $u$ is credited as paying ($1_{\text{sure}}(u) = 1$), then $\text{deg}_{\text{true}}(\text{pos}) \in \text{slot}_u[\text{pos}] \subseteq \text{mask}$ for all positions, so $\text{slot}_v[\text{pos}] \cap \text{mask} \ne \emptyset$ and $v$ is必ず debited as receiving ($1_{\text{poss}}(v) = 1$):
$$1_{\text{sure}}(u \to v, \sigma) \le 1_{\text{true}}(u \to v, \sigma) \le 1_{\text{poss}}(u \to v, \sigma).$$
Since $E_{\text{nm}} \ge 0$, total charge received across all edges in the LP upper-bounds total charge paid, making the LP relaxation strictly conservative. In terms of the net counts $\text{pay}(v) = \sum_{\text{out}} 1_{\text{sure}}$ and $\text{get}(v) = \sum_{\text{in}} 1_{\text{poss}}$, the coefficient of $E_{\text{nm}}$ is $\text{pay}(v) - \text{get}(v)$ in a sender row ($\ge 1$) and $\text{get}(v) - \text{pay}(v)$ in a `cons2` ($\le 0$) or receiver ($\le 1$) row.

---

## 2. Plain-Language Account: Why Charge from 5s Can Always Escape, and Which Four Structures Make It Tight

### 2.1 Why Charge from 5s Can Always Escape in the 5/6/7 World

At first sight, discharging the 5/6/7 world looks like a game of musical chairs with no spare capacity:
- Every degree-5 vertex starts with $+1$ excess charge that it must shed.
- Every degree-6 vertex has $0$ capacity: it can act as a bridge, but every unit of charge it accepts from 5-neighbours must be passed on to 7-neighbours.
- Every degree-7 vertex starts at $-1$ and can absorb at most $+1$ net charge before overflowing ($-1 + \text{inflow} \le 0$).
- Unlike degree-8 or degree-9 vertices (which have $-2$ and $-3$ Euler deficits and act as deep sinks), degree-7 vertices have the smallest possible negative Euler charge ($-1$) while potentially having up to five degree-5 neighbours!

Why, then, can the $+1$ charge on every 5 *always* escape to 7s without overflowing any 7? Three structural mechanisms work together:

1. **Reducibility kills isolated clusters of 5s and over-saturated 7s (`R5` and `RBIG`)**:
   - On the sender side, `R5` eliminates every degree-5 vertex whose link consists solely of 5s and 6s. Thus **every 5 has at least one big neighbour ($w_j \ge 7$)**, and if it has only one ($b = 1$, such as `55667`, `56667`, `66667`), it is flanked by two to four degree-6 vertices that are not `R6` and therefore border additional 7s at distance 2.
   - On the receiver side, `RBIG` eliminates every degree-7 wheel with $n_5 \ge 6$ degree-5 neighbours, every wheel with four consecutive 5s ($5555$), and every wheel with the pattern $55565$. Thus **every 7 has at most $n_5 \le 5$ degree-5 neighbours**, and the only admissible 7-link with $n_5 = 5$ is `5557557` (where the two 7-neighbours break the five 5s into a run of three and a run of two).

2. **Multi-channel routing splits the load of a 5 across its 1-ball and 2-ball**:
   - A degree-5 sender $u$ does not dump $1/b$ blindly onto each of its $b$ degree-7 neighbours. Instead, $u$ inspects the degrees around each $7$-neighbour via `y` and `zr` (which depend on the entire 5-link $w$ and the two adjacent triangle apexes $H_j, H_{j-1}$).
   - If a 7-neighbour $v$ is flanked on $u$'s link by other 7s (e.g., $w = 55777$ or $57777$), the common neighbours between $u$ and $v$ are themselves 7s (`s_i = 7` on $v$'s wheel), which means $v$ has fewer 5-neighbours on its link and can absorb more direct charge (`y - zr` up to $\approx 1.80$ in scaled LP units, or $\approx 0.60$ of a unit of Euler charge).
   - Conversely, if $u$ shares a $5\text{--}5$ edge with another 5 across a triangle whose apex on $v$'s link is 5 (`H_k = 1`), the hat transfer `r - rr` redistributes charge between the central vertex and the triangle apex, while degree-6 neighbours ($w_k = 6$) absorb charge via `g` and pipe it through `cons2` (`h/M`) to degree-7 vertices at distance 2 from $u$.

3. **Lateral $7 \leftrightarrow 7$ redistribution drains crowded 7s into adjacent 7s**:
   - Even when a degree-7 receiver $v$ has four or five degree-5 neighbours (`5575577` or `5557557`), its remaining two or three link neighbours are necessarily 7s (or 6s).
   - Through the antisymmetric $7 \leftrightarrow 7$ transfer `x`, the wheel-credit `q/Q7`, the half-side credit `lq/lQ`, and the 2-ball `EDGE(7->7)` / `EDGE(7->5)` / `EDGE(7->6)` keys, a heavily loaded 7-vertex exports its surplus charge across its $(7, 7)$ edges to adjacent 7-vertices that sit in more benign neighbourhoods (such as 7s whose own links contain fewer 5s or whose apexes are 7s).

---

### 2.2 Which Four Structures Make the 5/6/7 World Tight

Why does the 5/6/7 world have **zero spare global margin** ($t^* = 0$), and why did the pre-key discharging LP fail with a positive floor $D = +0.025279716 > 0$? Because four specific geometric configurations push the discharging capacity to its absolute limit:

#### Structure I: The 5/7 Mesh (Pure $\{5, 7\}$ Triangulations Around Crowded 7s)
- **Key rows**:
  - `R7 5575577/5775777` ($\text{slack} = 0$, **tight in `dual_t0_exact.json`** with dual weight $1/4$),
  - `R7 5757777/5555755` ($\text{slack} = 0$, **tight in `dual_t0_exact.json`** with dual weight $1/4$),
  - `R7 5575577/5775757` ($\text{slack} = 66026263 / 10^{12} \approx 6.60 \times 10^{-5}$),
  - `R7 5677757/7656555` ($\text{slack} = 33013131 / 5 \times 10^{11} = 66026262 / 10^{12} \approx 6.60 \times 10^{-5}$),
  - `R7 5557557/5766777` ($\text{slack} = 132052523 / 2 \times 10^{12} \approx 6.60 \times 10^{-5}$) and `R7 5557557/5777777` ($\text{slack} = 132052529 / 2 \times 10^{12} \approx 6.60 \times 10^{-5}$),
  - `R7 5757577/5577567` ($\text{slack} = 4439980267 / 5 \times 10^{11} \approx 0.008880$) and `R7 5557557/5776777` ($\text{slack} = 49684062011 / 4 \times 10^{11} \approx 0.124210$).
- **Why it is tight**: In a pure 5/7 mesh, there are no degree-6 vertices at all; every vertex has degree 5 (charge $+1$) or degree 7 (charge $-1$). By Euler's formula on the torus, if a periodic patch has equal numbers of 5s and 7s (ratio $1:1$), the average Euler charge per vertex is $\frac{1}{2}(+1) + \frac{1}{2}(-1) = 0$.
  In `R7 5575577/5775777` ($R_a$), the central 7 has **four** 5-neighbours (arranged as two $5\text{--}5$ pairs, each capped by an outer apex $s_i = 5$, forming two $5\text{--}5\text{--}5$ triangles!) and three 7-neighbours. Under [`primal_t0_exact.json`](file:///Users/kylemathewson/GraphColouringNov/pack/W6-rule-grammar/round7/primal_t0_exact.json):
  - The four 5-neighbours send a massive direct edge charge of $4 y(7,5,5,7,7) - 2 zr(7,5,5,7,7,1,0) - 2 zr(7,5,5,7,7,1,1) = +19.004463 - 11.934320 = +7.070143$ to $R_a$, while the two $s_i = 5$ hat apexes contribute $2 r(5,1,7,5,1,7) - 2 rr(5,1,7,5,1,7) = -0.114530$.
  - To survive (`LHS = 1`), $R_a$ **must export** $-5.961123$ units across its three $(7,7)$ edges via the antisymmetric transfer `x`: specifically $-1 \cdot x(252) = -3.000000$ across its $(7,7)$ edge flanked by 7s, and $-2 \cdot x(302) = -2.961123$ across its two $(7,7)$ edges flanked by $(5,7)$.
  - Where does that $+5.961123$ of exported `x`-charge go? Straight into `R7 5757777/5555755` ($R_b$), whose three $(7,7)$ edges have the exact opposite `x`-orientations ($+1 \cdot x(252) + 2 \cdot x(302) = +5.961123$)! Although $R_b$ has only two 5-neighbours on its link (`5757777`), five of its seven outer triangle apexes are 5s (`s = 5555755`), giving $+0.362432$ from hats `r - rr` and $-5.393271$ from `y - zr`. When combined with the 2-ball `EDGE` keys (`A1`, `gk00_10`, `gk01_18`, `gk02_24`, `gk02_26`) and `Q7/q/lQ/lq` credits, **both $R_a$ and $R_b$ land at $\text{LHS} = 1$ with exact slack $0$**.
  - Similarly, in the $n_5 = 5$ receiver `R7 5557557/5777777` (five 5-neighbours!), the five 5s send $y - zr = +22.132421 - 14.877529 = +7.254892$, which is offset by exporting $-2 \cdot x(252) = -6.000000$ across its two $(7,7)$ edges, $-0.179977$ via `q(7,5,5,5,7,5,5)`, and $-0.050873$ via the 2-ball `EDGE` keys (`gk04_41`, `gk03_35`, `A1`, `gk02_26`), leaving a razor-thin positive slack of $132052529 / 2000000000000 \approx 6.602626 \times 10^{-5}$.

#### Structure II: A 7 Carrying a Triangle of Three 5s (`5-5-5` Face) Inside the 5–6–7 Relay
- **Key rows**:
  - `R7 5556677/7576757` ($\text{slack} = 66026261 / 10^{12} \approx 6.60 \times 10^{-5}$),
  - `R7 5556676/5777767` ($\text{slack} = 33013131 / 5 \times 10^{11} = 66026262 / 10^{12} \approx 6.60 \times 10^{-5}$),
  - `R7 5757677/5556657` ($\text{slack} = 33013131 / 5 \times 10^{11} = 66026262 / 10^{12} \approx 6.60 \times 10^{-5}$),
  - `R7 5556677/7576577` ($\text{slack} = 2362697031 / 5 \times 10^{11} \approx 0.004725$),
  - `R7 5556667/7576677` ($\text{slack} = 15479943939 / 5 \times 10^{11} \approx 0.030960$).
- **Why it is tight**: In these configurations, a degree-7 receiver $v$ has a contiguous run of three degree-5 neighbours $(w_0, w_1, w_2) = (5, 5, 5)$ where the middle triangle $(v, w_1, w_2)$ has outer apex $s_1 = 5$ (so $(w_1, w_2, s_1)$ is a $5\text{--}5\text{--}5$ triangle!), AND this $5\text{--}5\text{--}5$ cluster is immediately bordered by a pair of degree-6 relay vertices $(w_3, w_4) = (6, 6)$ before reaching the remaining 7-neighbours.
  - Because $w_3 = w_4 = 6$, the receiver $v$ cannot use $7 \leftrightarrow 7$ `x`-transfers along those two edges; instead, $v$ *receives* relay inflow $+M$ from the 6s while simultaneously absorbing direct $5 \to 7$ inflow from the three 5s ($y - zr = +11.593913 - 8.842377 = +2.751536$ in `R7 5556677/7576757`).
  - Even worse, in `R7 5556677/7576577`, the $(7,6)$ edge at $w_4 = 6, w_5 = 7$ has apex $s_4 = 5$, which triggers the huge half-side credit $lQ(6, 5, 30) = +1.594500$ (coupled to `lq(6, 5, 7) = +1.594434` on `R7 5677757/7656555` and `lq(6, 5, 5) = +1.594434` on `R7 5556676/5777767`).
  - In the pre-key LP ([`W16-zero-euler/round7/REPORT.md`](file:///Users/kylemathewson/GraphColouringNov/pack/W16-zero-euler/round7/REPORT.md)), `R7 5556677/7576577` carried the **largest dual weight ($0.1146$)** in the positive-floor obstruction because no 1-ball variable could drain it without starving `R7 5677757/7656555`.
  - In [`primal_t0_exact.json`](file:///Users/kylemathewson/GraphColouringNov/pack/W6-rule-grammar/round7/primal_t0_exact.json), this bottleneck is broken by **K\*** (`KS = EDGE(7->7)[S.L+1=B S.L-1=S S.L-2=5 S.L-3=5 S.A-1=B]`, value $0.034115$) together with `gk00_50` ($0.043987$), `gk00_7` ($0.045860$), `gk03_35` ($2 \times 0.025046$), and `gk01_69` ($0.022625$), which recognize the $5\text{--}5$ run (`S.L-2=5 S.L-3=5`) on the 7-payer's link and export net `EDGE` charge $-0.167245$ (on `5556677/7576757`), $-0.179229$ (on `5556677/7576577`), and $-0.211797$ (on `5556676/5777767`), bringing all of them below $1$!

#### Structure III: Degree-5 Senders with 2 to 4 Big Neighbours Paying 7s That Are Already Full
- **Key rows**:
  - `S 55777 H11011 F-----` and its mirror twin `S 55777 H11101 F-----` ($\text{slack} = 0$, **tight in `dual_t0_exact.json`** with dual weight $1/2$),
  - `S 57777 H00100 F-----` ($\text{slack} = 66026259 / 10^{12} \approx 6.60 \times 10^{-5}$) and `S 57777 H00010 F-----` ($\text{slack} = 66026261 / 10^{12}$),
  - `S 55767 H01001 F---1-` ($\text{slack} = 66026259 / 10^{12}$), `S 56677 H00010 F-11--` ($\text{slack} = 66026259 / 10^{12}$),
  - `S 56777 H01110 F-0---` ($\text{slack} = 3301313 / 5 \times 10^{10} = 66026260 / 10^{12}$), `S 57577 H00010 F-----` ($\text{slack} = 66026260 / 10^{12}$),
  - `S 55677 H11011 F--0--` ($\text{slack} = 5282101 / 8 \times 10^{10} = 66026262.5 / 10^{12}$), `S 55757 H10010 F-----` ($\text{slack} = 66026261 / 10^{12}$).
- **Why it is tight**: Intuitively, one might expect a degree-5 sender with only *one* 7-neighbour ($b = 1$, like `55667`) to be the hardest to discharge, and a sender with *three or four* 7-neighbours (`55777`, `56777`, `57777`) to be easy. In fact, the **only tight sender in the entire 5/6/7 world** is `S 55777 H11011 F-----` ($b = 3$)!
  Why? Because in `S 55777 H11011 F-----`, the two 5-neighbours ($w_0 = 5, w_1 = 5$) have hat $H_0 = 1$ (forming a $5\text{--}5\text{--}5$ triangle of three `S 55777` vertices), and the three 7-neighbours ($w_2 = 7, w_3 = 7, w_4 = 7$) have hats $H_1 = 1, H_2 = 0, H_3 = 1, H_4 = 1$, which means those 7-neighbours are **precisely the full 5/7-mesh receivers $R_a$ (`5575577/5775777`) and $R_b$ (`5757777/5555755`)**!
  Specifically, under [`primal_t0_exact.json`](file:///Users/kylemathewson/GraphColouringNov/pack/W6-rule-grammar/round7/primal_t0_exact.json), `S 55777 H11011 F-----` discharges:
  - Direct $5 \to 7$ edge transfers to its two outer 7s ($w_2, w_4$, which are $R_a$ vertices): $2 y(7,5,5,7,7) - zr(7,5,5,7,7,1,0) - zr(7,5,5,7,7,1,1) = +9.502231 - 2.967160 - 3.000000 = +3.535071$.
  - Direct $5 \to 7$ edge transfer to its middle 7 ($w_3$, which is an $R_b$ vertex): $y(7,7,5,5,7) - zr(7,7,5,5,7,0,1) = +0.219732 - 2.916368 = -2.696636$ (net *reverse* flow from $R_b$ back to $S$, so total $y - zr = +0.838436$!).
  - Four hat transfers ($H_0 = H_1 = H_3 = H_4 = 1$): $2(r - rr)(5,1,5,7) + (r - rr)(5,1,7,5,1,7) + (r - rr)(7,7) = +0.069519 - 0.057265 + 0.111697 = +0.123951$.
  - Two 2-ball `EDGE` keys: $+2 E_{\text{gk01\_18}} - 1 E_{\text{gk02\_26}} = +0.042455 - 0.004841 = +0.037613$.
  - Summing the three channels gives $\text{outflow} = +0.838436 + 0.123951 + 0.037613 = 1.000000$ **with exact slack $0$**.

#### Structure IV: The Tight 6-Relay Bridges (`cons2` Bottlenecks)
- **Key rows**:
  - `C 666666/777777` ($\text{slack} = 4126641 / 62500000000 = 66026256 / 10^{12} \approx 6.60 \times 10^{-5}$, tightest `cons2` row overall),
  - `C 575757/555555` ($\text{slack} = 66026259 / 10^{12} \approx 6.60 \times 10^{-5}$),
  - `C 576767/577775`, `C 556676/577557`, `C 557667/555555`, `C 556777/575557`, `C 557777/557575`, `C 557557/555577` (all at $\text{slack} = 3301313 / 5 \times 10^{10} = 66026260 / 10^{12}$),
  - `C 576677/575577` and `C 576777/575555` ($\text{slack} = 66026261 / 10^{12} \approx 6.60 \times 10^{-5}$),
  - `C 566767/555575` ($\text{slack} = 66026263 / 10^{12} \approx 6.60 \times 10^{-5}$),
  - `C 556676/575757` ($\text{slack} = 202061763 / 10^{12} \approx 0.000202$).
- **Why it is tight**: A degree-6 vertex $v$ must satisfy $\text{inflow}(v) - \text{outflow}(v) \le 0$. In the base system, $v$ receives $g$ from each 5-neighbour on its 6-link $L$ and pays $h$ to each 7-neighbour on $L$. Why can't $h$ simply be made arbitrarily large to satisfy `cons2`? Because `mrowR2` forces $M(sg) \le h(hk)$, and $M(sg)$ is added directly to the inflow of every degree-7 receiver $R_7$ that borders $v$!
  For example, in `C 576677/575577` (one 5-neighbour, two 6-neighbours, three 7-neighbours) and `C 576777/575555` (one 5-neighbour, one 6-neighbour, four 7-neighbours):
  - In `C 576677/575577`, the single 5-neighbour sends $g(7,0,0,1,7,5,7) = +0.034769$, while the three 7-neighbours only absorb $-h(7,5,7,6,6,7,7,7) - h(7,6,6,7,5,7,5,7) = -0.022058 - 0.019157 = -0.041216$ (the third 7-neighbour has $h = 0$ because its receiver-side $M$ is capped at $0$ by crowded 7s!). Together with $+0.006381$ from 2-ball `EDGE` keys (`gk00_61`, `gk00_5`, `gk01_14`, `gk03_32`), the net balance is $\text{LHS} = -66026261 / 10^{12} < 0$.
  - Likewise, in `C 566767/555575`, the single 5-neighbour sends $g(6,0,1,0,7,5,5) = +0.175890$ (the exact `g`-channel used by the $b=1$ sender `S 55667 H01001 F--11-`!), and the two 7-neighbours absorb $-h(7,6,6,5,7,6,5,5) - h(7,5,6,6,7,6,5,7) = -0.151669 - 0.027572 = -0.179240$, plus $+0.003284$ from `EDGE` keys, leaving $\text{LHS} = -66026263 / 10^{12} < 0$.
  - Thus, **zero** non-empty `cons2` rows are tight at $0$: every single non-empty `cons2` row has strictly negative final charge $\text{ch}_{\text{final}}(v) \le -4126641 / 62500000000 = -6.6026256 \times 10^{-5} < 0$.

---

## 3. The Exact Tight Dual at $t = 0$ (`dual_t0_exact.json`) and Its Periodic Torus Realization

### 3.1 Algebraic Structure of the 9-Row Zero-Euler Certificate

In [`dual_t0_exact.json`](file:///Users/kylemathewson/GraphColouringNov/pack/W6-rule-grammar/round7/dual_t0_exact.json), the dual LP at $t = 0$ is solved in exact rational arithmetic by a sparse certificate supported on **only 9 rows** of the 220,903-row system:

| # | Row Type | Row Label / Key Signature | Dual Weight $\alpha_i$ | RHS $b_i$ (Sign-Normalized) | Weighted Euler Contribution $\alpha_i b_i$ |
| :-: | :--- | :--- | :-: | :-: | :-: |
| 1 | Receiver ($R_a$) | `R7 5575577/5775777` | $1/4$ | $-1$ ($-\text{inflow} \ge -1$) | $-1/4$ |
| 2 | Receiver ($R_b$) | `R7 5757777/5555755` | $1/4$ | $-1$ ($-\text{inflow} \ge -1$) | $-1/4$ |
| 3 | Sender ($S$) | `S 55777 H11011 F-----` | $1/2$ | $+1$ ($\text{outflow} \ge +1$) | $+1/2$ |
| 4 | `mrowQ` ($Q_{7,1}$) | `Q7(7,5,5,5,5,30,30) >= q(7,5,5,7,7,5,5)` | $1/4$ | $0$ | $0$ |
| 5 | `mrowQ` ($Q_{7,2}$) | `Q7(7,5,5,5,7,30,31) >= q(7,5,5,7,5,5,7)` | $1/2$ | $0$ | $0$ |
| 6 | `mrowQ` ($Q_{7,3}$) | `Q7(7,5,7,7,5,31,31) >= q(7,5,7,7,7,7,5)` | $1/4$ | $0$ | $0$ |
| 7 | `mrowQ` ($Q_{7,4}$) | `Q7(7,5,7,7,7,31,31) >= q(7,5,7,5,7,7,7)` | $1/2$ | $0$ | $0$ |
| 8 | `mrowQ` ($Q_{7,5}$) | `Q7(7,7,5,7,7,31,31) >= q(7,7,5,7,5,7,7)` | $1/2$ | $0$ | $0$ |
| 9 | `mrowL` ($lQ_1$) | `lQ(5,5,30) >= lq(5,5,7)` | $1$ | $0$ | $0$ |
| **Total** | | **9 Active Rows** | $\sum \alpha_i = 7/2$ | | **$\sum \alpha_i b_i = 0$** |

When we orient all 9 inequalities in the $\ge$ direction — namely $\text{outflow}(S) \ge 1$ with weight $+1/2$, $-\text{inflow}(R_a) \ge -1$ with weight $+1/4$, $-\text{inflow}(R_b) \ge -1$ with weight $+1/4$, and $\text{credit} - \text{payment} \ge 0$ for the 6 `mrow` rows — **every single one of the 35 active primal columns cancels identically to zero**:

| Column Family | Variable Key | Coef in $S$ ($\times \frac{1}{2}$) | Coef in $-R_a$ ($\times \frac{1}{4}$) | Coef in $-R_b$ ($\times \frac{1}{4}$) | Coef in $-\text{mrow}$ | Weighted Sum $\gamma_k$ |
| :--- | :--- | :-: | :-: | :-: | :-: | :-: |
| **Direct $5\to 7$ (`y`)** | `('y', (7, 5, 5, 7, 7))` | $+2$ | $-4$ | $0$ | $0$ | $\frac{1}{2}(2) + \frac{1}{4}(-4) = 0$ |
| | `('y', (7, 7, 5, 5, 7))` | $+1$ | $0$ | $-2$ | $0$ | $\frac{1}{2}(1) + \frac{1}{4}(-2) = 0$ |
| **Direct $5\to 7$ (`z`, `zr`)** | `('z', (7, 5, 5, 7, 7, 1, 0))` / `zr` | $\pm 1$ | $\mp 2$ | $0$ | $0$ | $\frac{1}{2}(\pm 1) + \frac{1}{4}(\mp 2) = 0$ |
| | `('z', (7, 5, 5, 7, 7, 1, 1))` / `zr` | $\pm 1$ | $\mp 2$ | $0$ | $0$ | $\frac{1}{2}(\pm 1) + \frac{1}{4}(\mp 2) = 0$ |
| | `('z', (7, 7, 5, 5, 7, 0, 1))` / `zr` | $\pm 1$ | $0$ | $\mp 2$ | $0$ | $\frac{1}{2}(\pm 1) + \frac{1}{4}(\mp 2) = 0$ |
| **Hat (`r`, `rr`)** | `('r', (5, 1, 5, 7))` / `rr` | $\pm 2$ | $0$ | $\mp 4$ | $0$ | $\frac{1}{2}(\pm 2) + \frac{1}{4}(\mp 4) = 0$ |
| | `('r', (5, 1, 7, 5, 1, 7))` / `rr` | $\pm 1$ | $\mp 2$ | $0$ | $0$ | $\frac{1}{2}(\pm 1) + \frac{1}{4}(\mp 2) = 0$ |
| | `('r', (7, 7))` / `rr` | $\pm 1$ | $0$ | $\mp 2$ | $0$ | $\frac{1}{2}(\pm 1) + \frac{1}{4}(\mp 2) = 0$ |
| **$7\leftrightarrow 7$ (`x`)** | `('x', 252)` | $0$ | $+1$ | $-1$ | $0$ | $\frac{1}{4}(+1) + \frac{1}{4}(-1) = 0$ |
| | `('x', 302)` | $0$ | $+2$ | $-2$ | $0$ | $\frac{1}{4}(+2) + \frac{1}{4}(-2) = 0$ |
| **Wheel (`q`, `Q7`)** | `q(7,5,5,7,7,5,5)` & `Q7(7,5,5,5,5,30,30)` | $0$ | $+1_q$ | $-1_{Q7}$ | $-1_q + 1_{Q7}$ ($\times \frac{1}{4}$) | $\frac{1}{4}(1 - 1) = 0$ |
| | `q(7,5,5,7,5,5,7)` & `Q7(7,5,5,5,7,30,31)` | $0$ | $+2_q$ | $-2_{Q7}$ | $-1_q + 1_{Q7}$ ($\times \frac{1}{2}$) | $\frac{1}{4}(2) - \frac{1}{2}(1) = 0$ |
| | `q(7,5,7,7,7,7,5)` & `Q7(7,5,7,7,5,31,31)` | $0$ | $-1_{Q7}$ | $+1_q$ | $-1_q + 1_{Q7}$ ($\times \frac{1}{4}$) | $\frac{1}{4}(-1 + 1) = 0$ |
| | `q(7,5,7,5,7,7,7)` & `Q7(7,5,7,7,7,31,31)` | $0$ | $-2_{Q7}$ | $+2_q$ | $-1_q + 1_{Q7}$ ($\times \frac{1}{2}$) | $-\frac{1}{2} + \frac{1}{2} = 0$ |
| | `q(7,7,5,7,5,7,7)` & `Q7(7,7,5,7,7,31,31)` | $0$ | $0$ | $+2_q - 2_{Q7}$ | $-1_q + 1_{Q7}$ ($\times \frac{1}{2}$) | $\frac{1}{4}(2) - \frac{1}{2}(1) = 0$ |
| **Half-side (`lq`, `lQ`)** | `lq(5,5,7)` & `lQ(5,5,30)` | $0$ | $+4_{lq}$ | $-4_{lQ}$ | $-1_{lq} + 1_{lQ}$ ($\times 1$) | $\frac{1}{4}(4) - 1 = 0$ |
| **2-Ball `EDGE` Keys** | `('E', 'A1')` | $0$ | $+4$ | $-4$ | $0$ | $\frac{1}{4}(4) + \frac{1}{4}(-4) = 0$ |
| | `('E', 'gk00_10')` | $0$ | $+2$ | $-2$ | $0$ | $\frac{1}{4}(2) + \frac{1}{4}(-2) = 0$ |
| | `('E', 'gk01_18')` | $+2$ | $-4$ | $0$ | $0$ | $\frac{1}{2}(2) + \frac{1}{4}(-4) = 0$ |
| | `('E', 'gk02_24')` | $0$ | $-2$ | $+2$ | $0$ | $\frac{1}{4}(-2) + \frac{1}{4}(2) = 0$ |
| | `('E', 'gk02_26')` | $-1$ | $+2$ | $0$ | $0$ | $\frac{1}{2}(-1) + \frac{1}{4}(2) = 0$ |

Because $\gamma_k = 0$ for every column $k$, taking the inner product of this dual vector $\alpha \ge 0$ with any primal solution $x$ yields:
$$0 = \sum_{k} \gamma_k x_k = \frac{1}{2}\,\text{outflow}(S) - \frac{1}{4}\,\text{inflow}(R_a) - \frac{1}{4}\,\text{inflow}(R_b) + \sum_{j=1}^{6} \alpha_{\text{mrow},j}\big(\text{credit}_j - \text{payment}_j\big).$$
Since $\text{outflow}(S) = 1 + \text{slack}(S)$, $\text{inflow}(R_a) = 1 - \text{slack}(R_a)$, $\text{inflow}(R_b) = 1 - \text{slack}(R_b)$, and $\text{payment}_j - \text{credit}_j = \text{slack}(\text{mrow}_j)$, this identity simplifies to:
$$\frac{1}{2}\,\text{slack}(S) + \frac{1}{4}\,\text{slack}(R_a) + \frac{1}{4}\,\text{slack}(R_b) + \sum_{j=1}^{6} \alpha_{\text{mrow},j}\,\text{slack}(\text{mrow}_j) = 0.$$
Since every primal slack is non-negative, **every single one of these 9 rows must have $\text{slack} = 0$ in every feasible $t = 0$ primal solution**, and no discharging rule using this column space can ever achieve $t > 0$!

---

### 3.2 Explicit Realization as a 12-Vertex Periodic Torus Triangulation $\mathcal{T}_{12}$

Why do all 35 columns — including the five 2-ball `EDGE` keys (`A1`, `gk00_10`, `gk01_18`, `gk02_24`, `gk02_26`) under the asymmetric sure-out / possible-in rule — cancel with zero loss? Because the 9-row dual certificate is **not an artifact of LP relaxation**: it is the exact incidence matrix of a **12-vertex, 36-edge, 24-face simple simplicial triangulation of the torus**, $\mathcal{T}_{12}$ (and more generally an infinite family $\mathcal{T}_{12m^2}$ on $\mathbb{Z}_m \times \mathbb{Z}_m$ with $p3$ threefold rotational symmetry), constructed and verified in [`construct_exact_57_torus.py`](file:///Users/kylemathewson/GraphColouringNov/agents/agent4_lemma/construct_exact_57_torus.py).

```
                 T_5^{(1)} = (6, 7, 8)      T_5^{(2)} = (9, 10, 11)
                 [three S: 55777 H11011]    [three S: 55777 H11011]
                          \                    /
                           \                  /
                 R_a = {3, 4, 5}: three 7-vertices (5575577 / 5775777)
                 [each borders two T_5 edges (w0,w1) and (w3,w4)]
                                   |
                                   |  (6 edges between R_a and R_b)
                                   v
                 R_b = {0, 1, 2}: triangle T_mid = (0, 1, 2)
                 [three 7-vertices (5757777 / 5555755)]
```

#### Explicit Vertex, Cyclic Link, and Face Specification of $\mathcal{T}_{12}$
The 12 vertices of $\mathcal{T}_{12}$ partition into three orbits under $\mathbb{Z}_3$ ($i \in \{0, 1, 2\}$, indices mod $3$ within each block):
1. **Three $R_b$ vertices $\{0, 1, 2\}$ (`R7 5757777/5555755`, weight $3/12 = 1/4$)**:
   - They form a central 7-7-7 triangle $T_{\text{mid}} = (0, 1, 2)$, whose outer triangles on its three edges are $(1, 0, 5)$, $(2, 1, 3)$, and $(0, 2, 4)$ capped by the three $R_a$ vertices $\{3, 4, 5\}$.
   - Their cyclic 7-links $(w_0,\dots,w_6)$ with degree sequence `(5, 7, 5, 7, 7, 7, 7)` and apex sequence `(5, 5, 5, 5, 7, 5, 5)` are:
     - $v = 0$: `(6, 3, 9, 5, 1, 2, 4)`
     - $v = 1$: `(7, 4, 10, 3, 2, 0, 5)`
     - $v = 2$: `(8, 5, 11, 4, 0, 1, 3)`
2. **Three $R_a$ vertices $\{3, 4, 5\}$ (`R7 5575577/5775777`, weight $3/12 = 1/4$)**:
   - Each $A_i = i + 3$ is adjacent to two $5\text{--}5$ edges — $(9+i, 9+(i+1))$ from $T_5^{(2)}$ and $(6+i, 6+(i+1))$ from $T_5^{(1)}$ — and to all three $R_b$ vertices $\{0, 1, 2\}$.
   - Their cyclic 7-links $(w_0,\dots,w_6)$ with degree sequence `(5, 5, 7, 5, 5, 7, 7)` and apex sequence `(5, 7, 7, 5, 7, 7, 7)` are:
     - $v = 3$: `(10, 9, 0, 6, 8, 2, 1)`
     - $v = 4$: `(11, 10, 1, 7, 6, 0, 2)`
     - $v = 5$: `(9, 11, 2, 8, 7, 1, 0)`
3. **Six $S$ vertices $\{6, 7, 8\}$ and $\{9, 10, 11\}$ (`S 55777 H11011 F-----`, weight $6/12 = 1/2$)**:
   - $\{6, 7, 8\}$ form a $5\text{--}5\text{--}5$ triangle $T_5^{(1)} = (6, 7, 8)$, and $\{9, 10, 11\}$ form a second $5\text{--}5\text{--}5$ triangle $T_5^{(2)} = (9, 10, 11)$.
   - Their cyclic 5-links $(w_0,\dots,w_4)$ with degree sequence `(5, 5, 7, 7, 7)` and hat bits `H = (1, 1, 0, 1, 1)` (outer apex degrees `(5, 5, 7, 5, 5)`) are:
     - $v = 6$: `(7, 8, 3, 0, 4)`, $v = 7$: `(8, 6, 4, 1, 5)`, $v = 8$: `(6, 7, 5, 2, 3)`
     - $v = 9$: `(10, 11, 5, 0, 3)`, $v = 10$: `(11, 9, 3, 1, 4)`, $v = 11$: `(9, 10, 4, 2, 5)`

The **24 triangular faces** of $\mathcal{T}_{12}$ are:
```
(0,1,2), (0,2,4), (0,3,9), (0,4,6), (0,5,1), (0,6,3), (0,9,5), (1,3,2),
(1,4,10), (1,5,7), (1,7,4), (1,10,3), (2,3,8), (2,5,11), (2,8,5), (2,11,4),
(3,6,8), (3,10,9), (4,7,6), (4,11,10), (5,8,7), (5,9,11), (6,7,8), (9,10,11)
```
Every vertex link is a single cycle of length $d(v) \in \{5, 7\}$, all 36 edges are simple (and for $m \ge 2$, $\mathcal{T}_{12m^2}$ has girth $3$ with no non-contractible 3-cycles), $\chi(\mathcal{T}_{12}) = 12 - 36 + 24 = 0$, every vertex is admissible under Studio-full and A97, and **`payee_kills = 0`**: every hidden private degree in $\mathcal{T}_{12}$ lies inside the `MASK` / `f2b_extra` bitmasks (specifically, $A_i$'s privates opposite $B_i$ have degree $7 \in \{6,7,8,9\} = \text{mask } 30$), so the 5 `mrowQ` rows and 1 `mrowL` row hold with exact equality on $\mathcal{T}_{12}$.

---

## 4. Case-by-Case Partition and Hand-Checkable Argument That Every Row Ends at or Below $0$

To make the verification of the 5/6/7 world completely transparent and machine-reproducible, we partition all **$220,903$** non-empty rows of the $t = 0$ system ([`phase0_check.py`](file:///Users/kylemathewson/GraphColouringNov/phase0_check.py)) into four top-level families (**Senders**, **Cons2**, **Degree-7 Receivers**, and **Mrow Closure**) and a small number of natural combinatorial cases within each family.

For every case, we report both:
- **`std_pkl` (`{5,6,7}` world)**: the base-deduplicated row labels in [`world_567_7_std.pkl`](file:///Users/kylemathewson/GraphColouringNov/pack/W16-zero-euler/data/world_567_7_std.pkl) (`2,020` Senders, `1,984` Cons2, `110,087` Receivers), and
- **`raw` (`build_world_labels`)**: the full enumeration of [`phase0_check.py`](file:///Users/kylemathewson/GraphColouringNov/phase0_check.py#L748-L781) (`2,840` `{5,6,7}` Senders / `26,280` total Senders; `2,837` non-empty `{5,6,7}` Cons2 / `81,135` total non-empty Cons2; `110,087` Receivers; `3,401` Mrow rows), together with the number of **distinct full rows** after deduplicating identical base+key linear forms.

Every single number below is reproduced in exact `Fraction` arithmetic by [`build_case_tables.py`](file:///Users/kylemathewson/GraphColouringNov/agents/agent4_lemma/build_case_tables.py) and stored in [`case_tables.json`](file:///Users/kylemathewson/GraphColouringNov/agents/agent4_lemma/case_tables.json).

---

### 4.1 Case Family A: Degree-5 Senders ($d = 5$, Initial Charge $+1$, Target $\text{ch}_{\text{final}} = 1 - \text{outflow} \le 0$)

We partition degree-5 senders into **5 main cases A1–A5** according to the number of big neighbours $b = n_{\text{big}}(w) = |\{k : w_k \ge 7\}| \in \{1, 2, 3, 4, 5\}$ on the 5-link ($b = 0$ is impossible by `R5`), and within the `{5,6,7}` link alphabet ($b = n_7$) into **14 sub-cases** indexed by $(n_5, n_6, n_7)$ with $n_5 + n_6 + n_7 = 5$.

#### Summary of Main Sender Cases A1–A5 (by $b = n_{\text{big}} \in \{1, 2, 3, 4, 5\}$)

| Case | $b = n_{\text{big}}$ | `{5,6,7}` Words | `{5,6,7}` `std_pkl` (`raw`) | All `{5..9}` Words | All `raw` (`distinct`) | Tight ($\text{slack}=0$) | Min Outflow $v_{\min}$ | Max Final Charge $1 - v_{\min}$ | Exact Rational Min Slack | Tightest Row Label in `{5,6,7}` |
| :--- | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :--- | :--- |
| **A1** | $b = 1$ | $5$ | $816$ ($1,064$) | $15$ | $3,192$ ($2,466$) | $0$ | $1.00006603$ | $-6.602626 \times 10^{-5}$ | `3301313/50000000000` | `S 55667 H01001 F--11-` |
| **A2** | $b = 2$ | $10$ | $828$ ($1,200$) | $72$ | $8,304$ ($7,196$) | $0$ | $1.00006603$ | $-6.602626 \times 10^{-5}$ | `66026259/1000000000000` | `S 55767 H01001 F---1-` |
| **A3** | $b = 3$ | $6$ | $308$ ($448$) | $126$ | $9,216$ ($7,968$) | $1$ ($2$ raw) | **$1.00000000$** | **$0$** | **`0`** (next: `3301313/50000000000`) | **`S 55777 H11011 F-----`** |
| **A4** | $b = 4$ | $2$ | $60$ ($96$) | $90$ | $4,320$ ($3,996$) | $0$ | $1.00006603$ | $-6.602626 \times 10^{-5}$ | `66026259/1000000000000` | `S 57777 H00100 F-----` |
| **A5** | $b = 5$ | $1$ | $8$ ($32$) | $39$ | $1,248$ ($888$) | $0$ | $1.00006603$ | $-6.602626 \times 10^{-5}$ | `33013129/500000000000` | `S 77777 H00101 F-----` |
| **Total** | $1..5$ | **$24$** | **$2,020$ ($2,840$)** | **$342$** | **$26,280$ ($22,514$)** | **$1$ ($2$ raw)** | **$1.00000000$** | **$0$** | **`0`** | **`S 55777 H11011 F-----`** |

#### Detailed Breakdown of the 14 `{5,6,7}` Sender Sub-Cases by $(n_5, n_6, n_7)$

| Sub-Case | $(n_5, n_6, n_7)$ | Canonical 5-Words in `{5,6,7}` | `std_pkl` (`raw`) | Distinct Rows | Tight ($0$) | Exact Rational Min Slack ($\text{outflow} - 1$) | Tightest Row Label | How Charge Escapes (Primary Mechanism) |
| :--- | :-: | :--- | :-: | :-: | :-: | :--- | :--- | :--- |
| **A1.1** | $(2, 2, 1)$ | `55667`, `55676` | $184$ ($240$) | $184$ | $0$ | `3301313/50000000000` ($6.602626 \times 10^{-5}$) | `S 55667 H01001 F--11-` | Single 7 takes $y - zr \approx +3.635$ (in $3\times$ units) + two 6s take $g \approx +0.405$. |
| **A1.2** | $(1, 3, 1)$ | `56667`, `56676` | $424$ ($424$) | $424$ | $0$ | `3301313/50000000000` ($6.602626 \times 10^{-5}$) | `S 56667 H10000 F-011-` | Single 7 takes $y - zr$ + three non-`R6` 6-relays absorb $g$. |
| **A1.3** | $(0, 4, 1)$ | `66667` | $208$ ($400$) | $214$ | $0$ | `3301313/50000000000` ($6.602626 \times 10^{-5}$) | `S 66667 H00000 F1111-` | Single 7 + four 6-relays (all $F_k$ combinations with $\ge 1$ non-`R6` exit). |
| **A2.1** | $(3, 0, 2)$ | `55757` | $20$ ($32$) | $20$ | $0$ | `66026261/1000000000000` ($6.6026261 \times 10^{-5}$) | `S 55757 H10010 F-----` | Two non-adjacent 7s take $2y(7,5,5,7,5) - zr \approx +1.014$ + hats `r - rr`. |
| **A2.2** | $(2, 1, 2)$ | `55677`, `55767`, `56757` | $168$ ($192$) | $168$ | $0$ | `66026259/1000000000000` ($6.6026259 \times 10^{-5}$) | `S 55767 H01001 F---1-` | Two 7s take $y - zr \approx +0.963$ to $+3.854$ + one 6-relay takes $g$. |
| **A2.3** | $(1, 2, 2)$ | `56677`, `56767`, `56776`, `57667` | $380$ ($496$) | $384$ | $0$ | `66026259/1000000000000` ($6.6026259 \times 10^{-5}$) | `S 56677 H00010 F-11--` | Two 7s + two 6-relays share outflow evenly. |
| **A2.4** | $(0, 3, 2)$ | `66677`, `66767` | $260$ ($480$) | $264$ | $0$ | `66026259/1000000000000` ($6.6026259 \times 10^{-5}$) | `S 66677 H01010 F100--` | Two 7s + three 6-relays; no 5-neighbours on link. |
| **A3.1** | $(2, 0, 3)$ | `55777`, `57577` | $40$ ($64$) | $40$ | **$1$ ($2$ raw)** | **`0`** (next: `3301313/50000000000` at `S 57577 H00010 F-----`) | **`S 55777 H11011 F-----`** | **Zero-Euler torus sender**: pays two $R_a$ 7s ($+3.535$), gets $-2.697$ from $R_b$, $+0.124$ hats, $+0.038$ `EDGE`. |
| **A3.2** | $(1, 1, 3)$ | `56777`, `57677` | $128$ ($128$) | $128$ | $0$ | `3301313/50000000000` ($6.602626 \times 10^{-5}$) | `S 56777 H01110 F-0---` | Three 7s take $y - zr \approx +0.999$ + hats `r - rr` + `EDGE(5->6)` `gk02_31`. |
| **A3.3** | $(0, 2, 3)$ | `66777`, `67677` | $140$ ($256$) | $144$ | $0$ | `66026261/1000000000000` ($6.6026261 \times 10^{-5}$) | `S 66777 H00001 F01---` | Three 7s + two 6-relays; no 5-neighbours on link. |
| **A4.1** | $(1, 0, 4)$ | `57777` | $20$ ($32$) | $20$ | $0$ | `66026259/1000000000000` ($6.6026259 \times 10^{-5}$) | `S 57777 H00100 F-----` | Four 7s take $2y(7,5,7,7,7) + 2y(7,7,5,7,7) - zr \approx +0.871$ + `r(7,7)` + `gk00_59`. |
| **A4.2** | $(0, 1, 4)$ | `67777` | $40$ ($64$) | $40$ | $0$ | `3301313/50000000000` ($6.602626 \times 10^{-5}$) | `S 67777 H00101 F0----` | Four 7s + one 6-relay. |
| **A5.1** | $(0, 0, 5)$ | `77777` | $8$ ($32$) | $8$ | $0$ | `33013129/500000000000` ($6.6026258 \times 10^{-5}$) | `S 77777 H00101 F-----` | Five 7-neighbours absorb $5(y - zr) \approx +1.000$ directly. |

---

### 4.2 Case Family B: Degree-6 Relay (`cons2`, $d = 6$, Initial Charge $0$, Target $\text{ch}_{\text{final}} = \text{inflow} - \text{outflow} \le 0$)

We partition degree-6 `cons2` vertices into **5 main cases B0–B4** by the number of degree-5 neighbours $n_5 \in \{0, 1, 2, 3, 4\}$ on the 6-link ($n_5 \ge 5$ is impossible because every 6-link with five or six 5s is reducible by `R6`), and within `{5,6,7}` into **19 sub-cases** indexed by $(n_5, n_6, n_7)$ with $n_5 + n_6 + n_7 = 6$.

#### Summary of Main `cons2` Cases B0–B4 (by $n_5 \in \{0, 1, 2, 3, 4\}$)

| Case | $n_5$ | `{5,6,7}` Words | `{5,6,7}` `std_pkl` (`raw non-empty`) | All `{5..9}` Words | All `raw non-empty` (`distinct`) | Tight ($0$) | Max Final Charge $v_{\max}$ | Exact Rational Min Slack ($-v_{\max}$) | Tightest Row Label in `{5,6,7}` (and Overall) |
| :--- | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :--- | :--- |
| **B0** | $n_5 = 0$ | $13$ | $191$ ($413$ of $414$) | $430$ | $22,667$ ($22,423$) | $0$ | $-6.6026256 \times 10^{-5}$ | `4126641/62500000000` | `C 666666/777777` (overall tightest) |
| **B1** | $n_5 = 1$ | $19$ | $633$ ($1,020$) | $543$ | $32,988$ ($32,847$) | $0$ | $-6.6026260 \times 10^{-5}$ | `3301313/50000000000` (all: `33013129/5e11`) | `C 576767/577775` (all: `C 566866/777777`) |
| **B2** | $n_5 = 2$ | $23$ | $898$ ($1,136$) | $366$ | $20,752$ ($20,650$) | $0$ | $-6.6026260 \times 10^{-5}$ | `3301313/50000000000` (all: `66026259/1e12`) | `C 556676/577557` (all: `C 556686/577557`) |
| **B3** | $n_5 = 3$ | $5$ | $240$ ($244$) | $77$ | $4,476$ ($4,460$) | $0$ | $-6.6026259 \times 10^{-5}$ | `66026259/1000000000000` | `C 575757/555555` |
| **B4** | $n_5 = 4$ | $1$ | $22$ ($24$) | $8$ | $252$ ($252$) | $0$ | $-6.6026260 \times 10^{-5}$ | `3301313/50000000000` | `C 557557/555577` |
| **Total** | $0..4$ | **$61$** | **$1,984$ ($2,837$)** | **$1,424$** | **$81,135$ ($80,148$)** | **$0$** | **$-6.6026256 \times 10^{-5}$** | **`4126641/62500000000`** | **`C 666666/777777`** |

*(Note: The single empty `cons2` label is `C 666666/555555` in Case B0, which has no 5-neighbours, no $\ge 7$ neighbours, and no matching 2-ball `EDGE` keys, giving the trivial identity $0 \le 0$.)*

#### Detailed Breakdown of the 19 `{5,6,7}` `cons2` Sub-Cases by $(n_5, n_6, n_7)$

| Sub-Case | $(n_5, n_6, n_7)$ | Words | `std_pkl` (`raw non-empty`) | Distinct Rows | Tight ($0$) | Exact Rational Min Slack ($\text{outflow} - \text{inflow}$) | Tightest Row Label | Relay Balance Mechanism |
| :--- | :-: | :-: | :-: | :-: | :-: | :--- | :--- | :--- |
| **B0.1** | $(0, 6, 0)$ | $1$ (`666666`) | $0$ ($12$ of $13$) | $10$ | $0$ | `4126641/62500000000` ($6.6026256 \times 10^{-5}$) | `C 666666/777777` | No base `g/h`; `EDGE(6->6)` keys (`gk01_14`, `gk01_65`, `gk03_32`) yield net outflow. |
| **B0.2** | $(0, 5, 1)$ | $1$ (`666667`) | $3$ ($36$) | $34$ | $0$ | `8253283/125000000000` ($6.6026264 \times 10^{-5}$) | `C 666667/555555` | Zero 5-inflow ($g = 0$); single 7-neighbour drains $h$ + `EDGE(6->6/7)`. |
| **B0.3** | $(0, 4, 2)$ | $3$ | $22$ ($100$) | $97$ | $0$ | `33013131/500000000000` ($6.6026262 \times 10^{-5}$) | `C 666677/777555` | Zero 5-inflow; two 7-neighbours drain $h$. |
| **B0.4** | $(0, 3, 3)$ | $3$ | $52$ ($116$) | $114$ | $0$ | `66026261/1000000000000` ($6.6026261 \times 10^{-5}$) | `C 666777/575755` | Zero 5-inflow; three 7-neighbours drain $h$. |
| **B0.5** | $(0, 2, 4)$ | $3$ | $69$ ($100$) | $96$ | $0$ | `3301313/50000000000` ($6.6026260 \times 10^{-5}$) | `C 667777/757575` | Zero 5-inflow; four 7-neighbours drain $h$. |
| **B0.6** | $(0, 1, 5)$ | $1$ (`677777`) | $34$ ($36$) | $34$ | $0$ | `3301313/50000000000` ($6.6026260 \times 10^{-5}$) | `C 677777/575575` | Zero 5-inflow; five 7-neighbours drain $h$. |
| **B0.7** | $(0, 0, 6)$ | $1$ (`777777`) | $11$ ($13$) | $11$ | $0$ | `33013131/500000000000` ($6.6026262 \times 10^{-5}$) | `C 777777/555555` | Zero 5-inflow; six 7-neighbours drain $h$. |
| **B1.1** | $(1, 4, 1)$ | $3$ | $33$ ($164$) | $162$ | $0$ | `66026261/1000000000000` ($6.6026261 \times 10^{-5}$) | `C 566766/575577` | One 5-inflow $g$ matched by single 7-outflow $h$ + `EDGE(6->5/6)` keys. |
| **B1.2** | $(1, 3, 2)$ | $6$ | $152$ ($328$) | $325$ | $0$ | `33013131/500000000000` ($6.6026262 \times 10^{-5}$) | `C 566677/577555` | Includes `C 566767/555575` ($\text{slack} = 66026263/10^{12}$): $g = +0.17589$, $h = -0.17924$. |
| **B1.3** | $(1, 2, 3)$ | $6$ | $252$ ($328$) | $326$ | $0$ | `3301313/50000000000` ($6.6026260 \times 10^{-5}$) | `C 576767/577775` | Includes `C 576677/575577` ($\text{slack} = 66026261/10^{12}$): $g = +0.03477$, $h = -0.04122$. |
| **B1.4** | $(1, 1, 4)$ | $3$ | $162$ ($164$) | $162$ | $0$ | `66026261/1000000000000` ($6.6026261 \times 10^{-5}$) | `C 567777/555555` | Includes `C 576777/575555` ($\text{slack} = 66026261/10^{12}$): $g = +0.07893$, $h = -0.08850$. |
| **B1.5** | $(1, 0, 5)$ | $1$ (`577777`) | $34$ ($36$) | $34$ | $0$ | `66026261/1000000000000` ($6.6026261 \times 10^{-5}$) | `C 577777/557755` | One 5-inflow $g$ drained across five 7-neighbours. |
| **B2.1** | $(2, 3, 1)$ | $4$ | $102$ ($228$) | $228$ | $0$ | `3301313/50000000000` ($6.6026260 \times 10^{-5}$) | `C 556676/577557` | Includes `C 556676/575757`: two 5s send $g = +0.28178$; single 7 takes $h = -0.25606$ + `EDGE` $-0.02591$. |
| **B2.2** | $(2, 2, 2)$ | $10$ | $376$ ($480$) | $478$ | $0$ | `3301313/50000000000` ($6.6026260 \times 10^{-5}$) | `C 557667/555555` | Two 5-inflows $g$ drained by two 7-outflows $h$ + `EDGE(6->5)` keys. |
| **B2.3** | $(2, 1, 3)$ | $6$ | $324$ ($328$) | $328$ | $0$ | `3301313/50000000000` ($6.6026260 \times 10^{-5}$) | `C 556777/575557` | Two 5-inflows $g$ drained by three 7-outflows $h$. |
| **B2.4** | $(2, 0, 4)$ | $3$ | $96$ ($100$) | $96$ | $0$ | `3301313/50000000000` ($6.6026260 \times 10^{-5}$) | `C 557777/557575` | Two 5-inflows $g$ drained by four 7-outflows $h$. |
| **B3.1** | $(3, 1, 2)$ | $3$ | $162$ ($164$) | $164$ | $0$ | `66026261/1000000000000` ($6.6026261 \times 10^{-5}$) | `C 556757/575557` | Three 5-inflows (`556757`, `557567`, `565757`; no `555` by `R6`) drained by two 7s. |
| **B3.2** | $(3, 0, 3)$ | $2$ | $78$ ($80$) | $80$ | $0$ | `66026259/1000000000000` ($6.6026259 \times 10^{-5}$) | `C 575757/555555` | Alternating `575757` and `557577`: three 5s drained by three 7s. |
| **B4.1** | $(4, 0, 2)$ | $1$ (`557557`) | $22$ ($24$) | $24$ | $0$ | `3301313/50000000000` ($6.6026260 \times 10^{-5}$) | `C 557557/555577` | Unique $n_5 = 4$ 6-word (`557557`); four 5s have small $g$ because each borders 7s directly. |

---

### 4.3 Case Family C: Degree-7 Receivers ($d = 7$, Initial Charge $-1$, Target $\text{ch}_{\text{final}} = -1 + \text{inflow} \le 0$)

We partition the **$110,087$** admissible degree-7 receiver labels (`109,592` distinct full rows) into **6 main cases C0–C5** according to the number of degree-5 neighbours $n_5 \in \{0, 1, 2, 3, 4, 5\}$ on the 7-link ($n_5 \ge 6$ is killed by `RBIG`), and into **26 sub-cases** indexed by $(n_5, n_6, n_7)$ with $n_5 + n_6 + n_7 = 7$.

#### Summary of Main Degree-7 Receiver Cases C0–C5 (by $n_5 \in \{0, 1, 2, 3, 4, 5\}$)

| Case | $n_5$ | Link Words | Labels (`std_pkl` = `raw`) | Distinct Rows | Tight ($\text{slack}=0$) | Max Net Inflow $v_{\max}$ | Max Final Charge $-1 + v_{\max}$ | Exact Rational Min Slack ($1 - v_{\max}$) | Tightest Row Label (and Next Tightest if $\text{slack}=0$) |
| :--- | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :--- | :--- |
| **C0** | $n_5 = 0$ | $18$ | $18,964$ | $18,460$ | $0$ | $0.99993397$ | $-6.6026262 \times 10^{-5}$ | `33013131/500000000000` | `R7 6666767/5755657` |
| **C1** | $n_5 = 1$ | $35$ | $48,978$ | $48,732$ | $0$ | $0.99993397$ | $-6.6026260 \times 10^{-5}$ | `3301313/50000000000` | `R7 5676667/6775666` |
| **C2** | $n_5 = 2$ | $54$ | $34,553$ | $34,407$ | **$1$** | **$1.00000000$** | **$0$** | **`0`** (next: `66026259/1000000000000`) | **`R7 5757777/5555755`** (next: `R7 5657677/5576655`) |
| **C3** | $n_5 = 3$ | $28$ | $6,794$ | $6,715$ | $0$ | $0.99993397$ | $-6.6026258 \times 10^{-5}$ | `33013129/500000000000` | `R7 5657567/5576767` |
| **C4** | $n_5 = 4$ | $7$ | $765$ | $762$ | **$1$** | **$1.00000000$** | **$0$** | **`0`** (next: `3301313/50000000000`) | **`R7 5575577/5775777`** (next: `R7 5556757/7576766`) |
| **C5** | $n_5 = 5$ | $1$ (`5557557`) | $33$ | $32$ | $0$ | $0.99993397$ | $-6.60262615 \times 10^{-5}$ | `132052523/2000000000000` | `R7 5557557/5766777` |
| **Total** | $0..5$ | **$143$** | **$110,087$** | **$109,592$** | **$2$** | **$1.00000000$** | **$0$** | **`0`** (next: `33013129/500000000000`) | **`R7 5575577/5775777` & `R7 5757777/5555755`** |

#### Detailed Breakdown of All 26 Degree-7 Receiver Sub-Cases by $(n_5, n_6, n_7)$

| Sub-Case | $(n_5, n_6, n_7)$ | Link Words | Labels | Distinct Rows | Tight ($0$) | Exact Rational Min Slack ($1 - \text{inflow}$) | Tightest Row Label | Discharging & Escape Mechanism |
| :--- | :-: | :-: | :-: | :-: | :-: | :--- | :--- | :--- |
| **C0.1** | $(0, 0, 7)$ | $1$ (`7777777`) | $198$ | $176$ | $0$ | `381216071839/500000000000` ($0.762432$) | `R7 7777777/5656566` | Pure 7-ring: only hat inflow `r - rr` ($\le 3$ apex 5s) + `Q7 - q`; massive slack $> 0.76$. |
| **C0.2** | $(0, 1, 6)$ | $1$ (`6777777`) | $1,134$ | $1,080$ | $0$ | `90149935581/250000000000` ($0.360600$) | `R7 6777777/5656565` | One 6-relay $M$ + hats + lateral $7\leftrightarrow 7$ transfers; slack $> 0.36$. |
| **C0.3** | $(0, 2, 5)$ | $3$ | $3,402$ | $3,303$ | $0$ | `1856007991/25000000000` ($0.074240$) | `R7 6776777/5655665` | Two 6-relays $M$ + hats + lateral $7\leftrightarrow 7$ transfers; slack $> 0.074$. |
| **C0.4** | $(0, 3, 4)$ | $4$ | $5,508$ | $5,364$ | $0$ | `66026263/1000000000000` ($6.6026263 \times 10^{-5}$) | `R7 6677677/5565565` | Three 6-relays $M$ + four 7s importing `x` from crowded 7s. |
| **C0.5** | $(0, 4, 3)$ | $4$ | $5,257$ | $5,162$ | $0$ | `66026263/1000000000000` ($6.6026263 \times 10^{-5}$) | `R7 6676767/6566556` | Four 6-relays $M$ + three 7s importing `x`. |
| **C0.6** | $(0, 5, 2)$ | $3$ | $2,825$ | $2,755$ | $0$ | `33013131/500000000000` ($6.6026262 \times 10^{-5}$) | `R7 6666767/5755657` | Five 6-relays $M$ + two 7s + three apex-5 hats. |
| **C0.7** | $(0, 6, 1)$ | $1$ (`6666667`) | $546$ | $534$ | $0$ | `69746272717/1000000000000` ($0.069746$) | `R7 6666667/5656566` | Six 6-relays (capped by `R6` and `cand2`) + one 7; slack $> 0.069$. |
| **C0.8** | $(0, 7, 0)$ | $1$ (`6666666`) | $94$ | $86$ | $0$ | `66026263/1000000000000` ($6.6026263 \times 10^{-5}$) | `R7 6666666/6676767` | All-6 link: absorbs seven 6-relay $M$ credits + `EDGE(6->7)` keys. |
| **C1.1** | $(1, 0, 6)$ | $1$ (`5777777`) | $1,134$ | $1,086$ | $0$ | `31849526991/125000000000` ($0.254796$) | `R7 5777777/5665665` | Single 5-neighbour + six 7s; large slack $> 0.25$. |
| **C1.2** | $(1, 1, 5)$ | $3$ | $6,561$ | $6,546$ | $0$ | `20285076789/500000000000` ($0.040570$) | `R7 5677777/5576565` | Single 5 + one 6 + five 7s; slack $> 0.040$. |
| **C1.3** | $(1, 2, 4)$ | $9$ | $15,414$ | $15,331$ | $0$ | `3301313/50000000000` ($6.6026260 \times 10^{-5}$) | `R7 5767677/5566566` | Single 5 + two 6s + four 7s absorbing `x` exports from crowded 7s. |
| **C1.4** | $(1, 3, 3)$ | $10$ | $16,429$ | $16,379$ | $0$ | `3301313/50000000000` ($6.6026260 \times 10^{-5}$) | `R7 5676776/5675675` | Single 5 + three 6s + three 7s. |
| **C1.5** | $(1, 4, 2)$ | $9$ | $7,920$ | $7,870$ | $0$ | `3301313/50000000000` ($6.6026260 \times 10^{-5}$) | `R7 5676667/6775666` | Single 5 + four 6s + two 7s. |
| **C1.6** | $(1, 5, 1)$ | $3$ | $1,520$ | $1,520$ | $0$ | `33013131/500000000000` ($6.6026262 \times 10^{-5}$) | `R7 5666766/6776676` | Single 5 + five 6s + one 7. |
| **C2.1** | $(2, 0, 5)$ | $3$ | $2,790$ | $2,740$ | **$1$** | **`0`** (next: `3301313/50000000000` at `R7 5757777/5556666`) | **`R7 5757777/5555755`** | **Zero-Euler torus receiver $R_b$**: absorbs $+5.961123$ `x`-export from $R_a$, $+0.362432$ hats, $+0.069452$ `EDGE`, $-5.393271$ `y-zr`. |
| **C2.2** | $(2, 1, 4)$ | $9$ | $10,668$ | $10,618$ | $0$ | `66026259/1000000000000` ($6.6026259 \times 10^{-5}$) | `R7 5757677/5576566` | Includes `R7 5677757/7656555` and `R7 5757677/5556657` ($\text{slack} = 66026262/10^{12}$). |
| **C2.3** | $(2, 2, 3)$ | $18$ | $13,782$ | $13,752$ | $0$ | `66026259/1000000000000` ($6.6026259 \times 10^{-5}$) | `R7 5657677/5576655` | Two 5s + two 6s + three 7s. |
| **C2.4** | $(2, 3, 2)$ | $17$ | $6,409$ | $6,397$ | $0$ | `3301313/50000000000` ($6.6026260 \times 10^{-5}$) | `R7 5656677/5767765` | Two 5s + three 6s + two 7s. |
| **C2.5** | $(2, 4, 1)$ | $7$ | $904$ | $900$ | $0$ | `66026261/1000000000000` ($6.6026261 \times 10^{-5}$) | `R7 5656667/5767777` | Two 5s + four 6s + one 7. |
| **C3.1** | $(3, 0, 4)$ | $4$ | $1,627$ | $1,598$ | $0$ | `66026259/1000000000000` ($6.6026259 \times 10^{-5}$) | `R7 5557777/5776666` | Includes `R7 5757577/5577567` ($\text{slack} = 0.008880$); exports across four $(7,7)$ edges. |
| **C3.2** | $(3, 1, 3)$ | $9$ | $3,286$ | $3,254$ | $0$ | `66026259/1000000000000` ($6.6026259 \times 10^{-5}$) | `R7 5657577/5577675` | Three 5s + one 6 + three 7s. |
| **C3.3** | $(3, 2, 2)$ | $13$ | $1,737$ | $1,719$ | $0$ | `33013129/500000000000` ($6.6026258 \times 10^{-5}$) | `R7 5657567/5576767` | Includes **Structure II** `R7 5556677/7576757` ($\text{slack} = 66026261/10^{12}$) & `R7 5556677/7576577` ($\text{slack} = 0.004725$), drained by `KS`, `gk00_50`, `gk00_7`, `gk03_35`. |
| **C3.4** | $(3, 3, 1)$ | $2$ (`5556667`, `5556676`) | $144$ | $144$ | $0$ | `66026261/1000000000000` ($6.6026261 \times 10^{-5}$) | `R7 5556667/7576666` | Includes **Structure II** `R7 5556676/5777767` ($\text{slack} = 66026262/10^{12}$, drained by `lq(6,5,5) = -1.594434` & `EDGE` $-0.211797$). |
| **C4.1** | $(4, 0, 3)$ | $3$ (`5557577`, `5575577`, `5575757`) | $431$ | $429$ | **$1$** | **`0`** (next: `132052521/2000000000000` at `R7 5557577/5767577`) | **`R7 5575577/5775777`** | **Zero-Euler torus receiver $R_a$**: receives $+7.070143$ `y-zr` from four 5s, exports $-5.961123$ via `x(252)` and `x(302)` to $R_b$. |
| **C4.2** | $(4, 1, 2)$ | $4$ | $334$ | $333$ | $0$ | `3301313/50000000000` ($6.6026260 \times 10^{-5}$) | `R7 5556757/7576766` | Four 5s + one 6 + two 7s; exports via `x`, `q`, and `EDGE(7->5/7)` keys. |
| **C5.1** | $(5, 0, 2)$ | $1$ (`5557557`) | $33$ | $32$ | $0$ | `132052523/2000000000000` ($6.60262615 \times 10^{-5}$) | `R7 5557557/5766777` | Unique $n_5 = 5$ link word (`5557557`): receives $+7.255$ `y-zr` from five 5s, exports $-6.000$ via `2 x(252)` and $-0.180$ via `2 q(7,5,5,5,7,5,5)`. |

---

### 4.4 Case Family D: Masked Credit Closure (`mrow`, $3,401$ Rows, Target $\text{credit} - \text{payment} \le 0$)

Finally, the **$3,401$** masked-credit closure inequalities partition into three cases **D1–D3** by credit family:

| Case | Closure Family | Row Form | Row Count (`distinct`) | Tight ($\text{slack}=0$) | Max LHS ($\text{payment} - \text{credit} \le 0$) | Exact Rational Min Slack | Tightest Row Label (and Next Tightest if $\text{slack}=0$) |
| :--- | :--- | :--- | :-: | :-: | :-: | :--- | :--- |
| **D1** | `mrowR2` ($6 \to 7$ relay) | $h(hk) - M(sg) \le 0$ | $1,496$ ($1,496$) | $0$ | $-6.6026261 \times 10^{-5}$ | `66026261/1000000000000` | `('mrowR2', (7, 5, 5, 6, 5, 7, 7, 28), (7, 5, 5, 7, 6, 5, 7, 7))` |
| **D2** | `mrowQ` ($7 \to 7$ wheel) | $q(qk) - Q_7(sg_7) \le 0$ | $1,856$ ($1,856$) | **$5$** | **$0$** | **`0`** (next: `66026261/1000000000000`) | The 5 `mrowQ` rows of `dual_t0_exact.json` (next: `('mrowQ', (7, 5, 6, 7, 7, 31, 31), (7, 5, 6, 5, 6, 7, 7))`) |
| **D3** | `mrowL` ($7 \to 7$ half-side) | $lq(c,a,a_2) - lQ(c,a,m) \le 0$ | $49$ ($49$) | **$1$** | **$0$** | **`0`** (next: `33013131/500000000000`) | `('mrowL', (5, 5, 30), (5, 5, 7))` (next: `('mrowL', (5, 5, 28), (5, 5, 7))`) |
| **Total** | **All `mrow`** | | **$3,401$ ($3,401$)** | **$6$** | **$0$** | **`0`** (next: `66026261/1000000000000`) | **6 tight rows of `dual_t0_exact.json`** |

---

### 4.5 Global Synthesis: Every Row of the 5/6/7 World Ends at or Below $0$

Combining Case Families A, B, C, and D yields the complete verification of the 5/6/7 world at $t = 0$:

| Row Family | `{5,6,7}` `std_pkl` Labels | Full Raw Labels (`non-empty`) | Distinct Non-Empty Rows | Tight Rows ($\text{slack} = 0$) | Minimum Positive Slack | Maximum Final Charge $\text{ch}_{\text{final}}$ |
| :--- | :-: | :-: | :-: | :-: | :--- | :-: |
| **A. Senders ($d = 5$)** | $2,020$ | $26,280$ ($2,840$ in `{5,6,7}`) | $22,514$ ($2,038$ in `{5,6,7}`) | $1$ `std_pkl` ($2$ raw: `S 55777 H11011` & `H11101`) | `33013129/500000000000` ($6.6026258 \times 10^{-5}$) | **$0$** |
| **B. Cons2 ($d = 6$)** | $1,984$ | $81,136$ ($81,135$ non-empty) | $80,148$ ($2,803$ in `{5,6,7}`) | $0$ | `4126641/62500000000` ($6.6026256 \times 10^{-5}$) | **$-6.6026256 \times 10^{-5} < 0$** |
| **C. Receivers ($d = 7$)** | $110,087$ | $110,087$ ($110,087$ non-empty) | $109,592$ | $2$ (`R7 5575577/5775777` & `R7 5757777/5555755`) | `33013129/500000000000` ($6.6026258 \times 10^{-5}$) | **$0$** |
| **D. Mrow Closure** | $3,401$ | $3,401$ ($3,401$ non-empty) | $3,401$ | $6$ ($5$ `mrowQ`, $1$ `mrowL`) | `66026261/1000000000000` ($6.6026261 \times 10^{-5}$) | **$0$** |
| **Grand Total** | **$117,492$** | **$220,904$ ($220,903$ non-empty)** | **$215,655$** | **$9$ `std_pkl` ($10$ raw)** | **`4126641/62500000000` ($6.6026256 \times 10^{-5}$)** | **$\le 0$ (Zero Violations)** |

Every single row outside the 9-row support of the periodic torus triangulation $\mathcal{T}_{12}$ (`dual_t0_exact.json`) has strictly positive slack $\ge \frac{4126641}{62500000000} = 6.6026256 \times 10^{-5} > 0$, and the 9 rows of $\mathcal{T}_{12}$ hold with exact equality ($\text{slack} = 0$). Consequently, every row of the 5/6/7 world ends at or below $0$.


---

## 7. Multi-Certificate Slack Comparison, Universal Torus Invariance, and Boundary Tightness Anatomy (`[P]`)

All results in this section are reproduced in standalone pure-Python exact `Fraction` arithmetic by [`agents/agent4_lemma/build_compressed_case_tables.py`](file:///Users/kylemathewson/GraphColouringNov/agents/agent4_lemma/build_compressed_case_tables.py) and stored in [`outside-argon-7nov/certs/case_tables_compressed_exact.json`](file:///Users/kylemathewson/GraphColouringNov/outside-argon-7nov/certs/case_tables_compressed_exact.json) (see also [`agents/agent4_lemma/COMPRESSED_CASE_ANALYSIS.md`](file:///Users/kylemathewson/GraphColouringNov/agents/agent4_lemma/COMPRESSED_CASE_ANALYSIS.md)).

### 7.1 Universal Torus Invariance Across All Compressed $t = 0$ Certificates (`[P]`)

Because the 9-row zero-Euler dual operator $\mathcal{L}_{\mathcal{T}_{12}}$ on the 12-vertex torus $\mathcal{T}_{12}$ cancels every base variable and every legal `EDGE` rule in the `KEYSPEC.md` grammar identically ($\mathcal{L}_{\mathcal{T}_{12}} \equiv 0$), **every feasible $t = 0$ primal certificate under any subset of rules or schemas must satisfy all 9 `std_pkl` rows (`10` raw rows) of $\mathcal{T}_{12}$ with exact equality ($\text{slack} = 0/1$)**.

We verified in exact `Fraction` arithmetic across all 15 certificates (`baseline_87rules`, `compressed_20rules`, `compressed_19rules`, `compressed_17rules_89conds`, `compressed_16rules_84conds`, `compressed_6schemas_22rules`, `compressed_3intschemas_20rules`, `compressed_3intschemas_22rules`, `compressed_2intschemas_22rules`, `compressed_1master_schema_22rules`, `compressed_1master_schema_19rules`, `coupled_6relay_39exc`, `K172_schemas_sparse` at $K_{\text{exact}} = 163$, `extreme_vertex_889vars`, and `extreme_vertex_863vars_17rules`) that:
1. All `220,904` linear constraints (`217,503` world labels + `3,401` `mrow` closure rows) have **zero violations (`total_violations == 0`)**.
2. All 9 `std_pkl` rows (`10` raw rows) of $\mathcal{T}_{12}$ (`R7 5575577/5775777`, `R7 5757777/5555755`, `S 55777 H11011 F-----` and raw twin `S 55777 H11101 F-----`, plus `5 mrowQ` and `1 mrowL`) have **exact rational slack `0` (`universal_torus_invariance_verified == True`)**.

### 7.2 Three Geometric Regimes of the $t = 0$ Polytope Across All 15 Certificates (`[P]`)

| Certificate ID | File (`outside-argon-7nov/certs/`) | Closing Rules | Active Variables | Schemas $k$ | Tight `{5,6,7}` Labels (`std_pkl` / `raw` / `dist`) | Tight `mrow` Rows (`3,401` total) | Global Min Positive Label Slack $\sigma_{\min} > 0$ (`{5,6,7}`) |
|---|---|---:|---:|---:|---:|---:|---|
| `baseline_87rules` | `primal_t0_exact.json` *(pack)* | `87` (`708` conds) | `7,213` | `87` | `3 / 4 / 3` *(Torus only)* | `6` *(Torus only)* | $\frac{4126641}{62500000000} \approx 6.602626 \times 10^{-5}$ (`C 666666/777777`) |
| `compressed_20rules` | `primal_t0_20rules_exact.json` | `20` (`92` conds) | `7,168` | `20` | `3 / 4 / 3` *(Torus only)* | `6` *(Torus only)* | $\frac{2305581}{1000000000000} \approx 2.305581 \times 10^{-6}$ (`R7 5657777/5555756`) |
| `compressed_19rules` | `primal_t0_19rules_exact.json` | `19` (`87` conds) | `7,141` | `19` | **`4 / 5 / 4`** *(Torus + `5757777/5555555`)* | `6` *(Torus only)* | $\frac{39187511}{1000000000000000} \approx 3.918751 \times 10^{-8}$ (`C 567677/555755`) |
| **`compressed_17rules_89conds`** | `primal_t0_17rules_89conds_exact.json` | **`17` (`89` ctx preds)** | `7,155` | **`17`** | **`3 / 4 / 3` *(Torus only)*** | **`6` *(Torus only)*** | **$\frac{8629811429}{1000000000000000} \approx 8.629811 \times 10^{-6}$ (`R7 5676776/5576575`)** |
| **`compressed_16rules_84conds`** | `primal_t0_16rules_84conds_exact.json` | **`16` (`84` ctx preds)** | `7,139` | **`16`** | **`3 / 4 / 3` *(Torus only)*** | **`6` *(Torus only)*** | **$\frac{16777203}{5000000000000} \approx 3.355441 \times 10^{-6}$ (`R7 5577577/7567576`)** |
| `compressed_6schemas_22rules` | `primal_t0_6schemas_22rules_exact.json` | `22` | `7,157` | **`6` equal-wt** | `3 / 4 / 3` *(Torus only)* | `6` *(Torus only)* | $\frac{2146107}{1000000000000} \approx 2.146107 \times 10^{-6}$ (`R7 5767767/7555557`) |
| `compressed_3intschemas_20rules` | `primal_t0_3intschemas_20rules_exact.json` | `20` (`92` conds) | `7,159` | **`3` int-mult** | `3 / 4 / 3` *(Torus only)* | `6` *(Torus only)* | $\frac{4093378211}{2500000000000000} \approx 1.637351 \times 10^{-6}$ (`R7 5667767/7566567`) |
| `compressed_3intschemas_22rules` | `primal_t0_3intschemas_22rules_exact.json` | `22` | `7,159` | **`3` int-mult** | `3 / 4 / 3` *(Torus only)* | `6` *(Torus only)* | $\frac{1034797}{500000000000} \approx 2.069594 \times 10^{-6}$ (`R7 5556776/5775767`) |
| `compressed_2intschemas_22rules` | `primal_t0_2intschemas_exact.json` | `22` | `7,148` | **`2` int-mult** ($M_{\max}=5$) | `3 / 4 / 3` *(Torus only)* | `6` *(Torus only)* | $\frac{4930097073}{5000000000000000} \approx 9.860194 \times 10^{-7}$ (`R7 5667767/5575575`) |
| `compressed_1master_schema_22rules` | `primal_t0_1master_schema_exact.json` | `22` | `7,147` | **`1` master** ($M_{\max}=8$) | `3 / 4 / 3` *(Torus only)* | `6` *(Torus only)* | $\frac{4915942219}{5000000000000000} \approx 9.831884 \times 10^{-7}$ (`R7 5667767/5575575`) |
| `compressed_1master_schema_19rules` | `primal_t0_1master_schema_19rules_exact.json` | `19` (`87` conds) | `7,156` | **`1` master** ($M_{\max}=24$) | `3 / 4 / 3` *(Torus only)* | `6` *(Torus only)* | $\frac{8831208373}{12000000000000000} \approx 7.359340 \times 10^{-7}$ (`R7 5566767/7577756`) |
| `coupled_6relay_39exc` | `primal_t0_coupled_6relay_40exc_exact.json` | `87` | `1,231` | `87` (`99.32%` even-split `h`) | **`1,141 / 1,602 / 1,401`** | **`1,554`** | $\frac{1534377580004393952369303667821}{32802277738268513043588871474890685} \approx 4.677656 \times 10^{-5}$ (`R7 5677577/5675765`) |
| `K172_schemas_sparse` | `primal_t0_Kschemas_sparse_exact.json` | `50` active (of `87`) | `1,078` | **`K = 163` full-LP** | **`523 / 846`** | **`1,714`** | $\frac{7041446818661997}{343034690860602903140399} \approx 2.052692 \times 10^{-8}$ (`C 567757/555577`) |
| `extreme_vertex_889vars` | `primal_t0_sparse_pure567_exact.json` | `38` active (of `87`) | **`889`** (`274` env + `615` rule) | `38` | **`1,542 / 2,112 / 1,833`** | **`1,854`** | $\frac{16346275470503908501}{2799905329921891612176380} \approx 5.838153 \times 10^{-6}$ (`R7 5556677/7576756`) |
| **`extreme_vertex_863vars_17rules`** | `primal_t0_sparse_17rules_pure567_exact.json` | **`17` (`89` ctx preds)** | **`863`** (`271` env + `592` rule) | **`17`** | **`2,069 / 2,923`** | **`1,887`** | **$\frac{96436077090639}{32264766079683912820} \approx 2.988897 \times 10^{-6}$ (`R7 5677776/5555575`)** |

1. **Regime I — The 10 Strictly Relative-Interior Certificates (`baseline_87rules`, `compressed_20rules`, `compressed_17rules_89conds`, `compressed_16rules_84conds`, `compressed_6schemas_22rules`, `compressed_3intschemas_20rules`, `compressed_3intschemas_22rules`, `compressed_2intschemas_22rules`, `compressed_1master_schema_22rules`, and `compressed_1master_schema_19rules`)**: The 9 Torus `std_pkl` rows (`3` label + `6` `mrow`) are the **unique** zero-slack rows in the entire `220,904`-row world; every non-torus row has strictly positive rational slack $\ge \sigma_{\min} > 7.35 \times 10^{-7}$. In particular, **`compressed_16rules_84conds`** (`16` irreducible 1-sentence rules, `84` context predicates, zero `5->5`, `6->*`, or `7->5` rules) achieves strictly relative-interior feasibility with $\sigma_{\min} = \frac{16777203}{5 \times 10^{12}} \approx 3.36 \times 10^{-6} > 0$, **`compressed_17rules_89conds`** achieves $\sigma_{\min} \approx 8.63 \times 10^{-6} > 0$, and `compressed_1master_schema_19rules` achieves strictly relative-interior feasibility using a **single master schema ($k = 1$)** (`interior_8certs_unique_torus_tight_verified == True`).
2. **Regime II — The 19-Rule Boundary-Facet Certificate (`compressed_19rules`)**: In `primal_t0_19rules_exact.json`, one single non-torus row touches $\text{slack} = 0$: **`R7 5757777/5555555`** (the outer-shell $s_4 = 5$ twin of the Torus row `R7 5757777/5555755`), giving `4` `std_pkl` label rows (`5` raw label rows) + `6` `mrow` rows = `10` `std_pkl` (`11` raw) zero-slack rows, while `primal_t0_16rules_84conds_exact.json`, `primal_t0_17rules_89conds_exact.json`, and `primal_t0_1master_schema_19rules_exact.json` restore strict positivity on `R7 5757777/5555555`.
3. **Regime III — Sparse, Coupled-6-Relay, and Extreme-Vertex Boundary Certificates (`coupled_6relay_39exc`, `K172_schemas_sparse` at $K = 163$, `extreme_vertex_889vars`, `extreme_vertex_863vars_17rules`, plus `primal_t0_coupled_6relay_16rules_exact.json` and `primal_t0_sparse_16rules_pure567_exact.json`)**: On all sparse/structural boundary certificates, **100% of all `191` `std_pkl` / `413` raw non-empty $n_5 = 0$ `Cons2` rows (`B0_n5_0`)** are identically tight (`0 - 0 = 0`, because $h = 0$ whenever a 6-vertex has no 5-neighbours), with total tight rows (`std_pkl` / `raw_567` including `mrow`) equal to **`2,695 / 3,156`** on `coupled_6relay_39exc` (`274/355` `S`, `558/938` `C`, `309` `R7`, `1,554` `mrow`), **`2,237 / 2,560`** on `K172_schemas_sparse` at $K_{\text{exact}} = 163$ (`80/108` `S`, `358/653` `C`, `85` `R7`, `1,714` `mrow`), **`3,396 / 3,966`** on `extreme_vertex_889vars` (`330/433` `S`, `921/1,388` `C`, `291` `R7`, `1,854` `mrow`), and **`3,956 / 4,810`** on `extreme_vertex_863vars_17rules` (`605/825` `S`, `1,174/1,808` `C`, `290` `R7`, `1,887` `mrow`).

---

## 8. Unified Master 1-Sentence Closing Architecture & Exact Bridge to the Swarm Full-Stack (`GL5` / `GL6` / `MS3`) (`[P]`)

To connect our `{5,6,7}` and Degree-8 exact $t^* = 0$ certificates directly to the full-stack discharging effort (`2026-11-08 ~17:00Z` handoff report), we established four exact results (`[P]`):

### 8.1 The 5-Tier Unified Master 1-Sentence Closing Rule Set ([`primal_unified_master_closing_set_exact.json`](file:///Users/kylemathewson/GraphColouringNov/outside-argon-7nov/certs/primal_unified_master_closing_set_exact.json))

Using two exact wheel-slot identities across all `629,073` `OUT` slots and `71,377` `IN` slots in `S_all U C_all U R7_5678 U R8_567` — **(i)** on every `EDGE(5->v)` rule, `S.L+3 == S.L-2` and `S.L-3 == S.L+2` bit-for-bit; **(ii)** on every `EDGE(6->v)` rule, `S.L+3 == S.L-3` bit-for-bit — together with domain-bound predicate elimination (`0` slot mismatches across all `700,450` slots), we compressed all five benchmarks into a nested **5-Tier Unified Master 1-Sentence Closing Rule Set**:

| Tier | Benchmark World | Admissible Receivers | Irreducible Rules $M$ | Context Predicates | Certificate (`outside-argon-7nov/certs/`) |
| :---: | :--- | ---: | :---: | :---: | :--- |
| **Tier 1** | `{5,6,7}` World (`R7_567`) | `110,087` | **`16`** (`0` `5->5`, `0` `6->*`, `0` `7->5`) | **`84`** | [`primal_t0_16rules_84conds_exact.json`](file:///Users/kylemathewson/GraphColouringNov/outside-argon-7nov/certs/primal_t0_16rules_84conds_exact.json) (`6628e000`) |
| **Tier 2** | Degree-8 Capped `Studio` (`PAT_std` + `rpatN3_rot`) | `2,298,303` | **`17`** (`Tier 1 + r1s_gk00_5`, or `24` keys) | **`87`** (`143` on `24` keys) | [`primal_d8_studio_17rules_exact.json`](file:///Users/kylemathewson/GraphColouringNov/outside-argon-7nov/certs/primal_d8_studio_17rules_exact.json) (`4cf37c47`) / [`primal_d8_studio_24keys_exact.json`](file:///Users/kylemathewson/GraphColouringNov/outside-argon-7nov/certs/primal_d8_studio_24keys_exact.json) (`2485a8a6`) |
| **Tier 3** | Degree-8 Capped `A97+F` (`PAT_a97f` + `rpatN3_rot`) | `2,306,117` | **`37`** (`20 Studio + 17 A97+F`) | **`232`** (`-69` stripped) | [`primal_d8_a97f_37keys_exact.json`](file:///Users/kylemathewson/GraphColouringNov/outside-argon-7nov/certs/primal_d8_a97f_37keys_exact.json) (`8227aedd`) |
| **Tier 4** | Degree-8 Capped `A100F` (`PAT_a100f` + `rpatN3_rot`) | `2,306,129` | **`51`** (`Tier 3 + 14 Route-F`) | **`312`** (`-98` stripped) | [`primal_d8_a100f_51keys_exact.json`](file:///Users/kylemathewson/GraphColouringNov/outside-argon-7nov/certs/primal_d8_a100f_51keys_exact.json) (`299e6739`) |
| **Tier 5** | `k86L` (`2,749` rows) + `CONS2SHARP` All-Big 6-Wheels | `2,749` + `184` `C` | **`+1` rule** (`cg76_SL1_S`, `1` key alone!) | **`+3`** (`315` w/ Tier 4) | [`k86L_cons2sharp_safe_t0_exact.json`](file:///Users/kylemathewson/GraphColouringNov/outside-argon-7nov/certs/k86L_cons2sharp_safe_t0_exact.json) (`240e1bba`) |

In [`wave4_analysis_exact.json`](file:///Users/kylemathewson/GraphColouringNov/outside-argon-7nov/certs/wave4_analysis_exact.json) (`7e282102`), we proved that $M = 17$ (`87` predicates) on Degree-8 Studio is a **sharp minimum**: dropping `r1s_gk00_5` gives exact dual lower bound $D = \frac{78925705617958660897}{525428904563732685477832} \approx 0.000150212 > 0$, all `16` single-rule replacements (keeping `r1s_gk00_5`) have $t^* \ge 0.000061527 > 0$ even on `{5,6,7}`, and all $\binom{17}{2} = 136$ pairwise bitmask join-merges `(r_i | r_j)` fail with $t^* \ge 0.000059719 > 0$.

### 8.2 Exact Discharging of Swarm Floor Binders (`Row A`, `Row B`, `H05`, `mrowL [6,6,*]`, and `d7 link-8578656`) ([`swarm_rowA_rowB_H05_mrowL66_analysis_exact.json`](file:///Users/kylemathewson/GraphColouringNov/outside-argon-7nov/certs/swarm_rowA_rowB_H05_mrowL66_analysis_exact.json))

1. **Why Row A (`7/7665566/6765776`, canonical `7/5566766/5676677`) and Row B (`7/7666666/6567656`, canonical `7/6666667/5676566`) Form a Two-Row `mrowL [6,6,*]` Cycle on a `7-7` Edge**:
   - At dart $i = 0$ (`7->7` with shared face degrees `(c, a) = (6, 6)`), the antisymmetric base transfer `("x", 3906)` (`tau_x(7, 7, side_x(6,6,6), side_x(6,6,6))`) cancels identically (`+1 - 1 = 0`) on both Row A and Row B.
   - Without `f2b` on `d7_w7` (`m7 = 31` on Row B), Row A emits `-2*lq(6,6,5) + 2*lQ(6,6,30)` and Row B emits `-2*lq(6,6,6) + 2*lQ(6,6,31)`, which combine with `2*mrowL((6,6,30),(6,6,6)) + 2*mrowL((6,6,31),(6,6,5))` to cancel all `lq`/`lQ` terms identically (`0`). With `f2b` (`d7_w7` rules `#1200` and `#752`) active, Row B's `lQ` tightens from `(6,6,31)` to `(6,6,30)`, breaking the `B -> A` leg.
   - In [`primal_t0_16rules_84conds_exact.json`](file:///Users/kylemathewson/GraphColouringNov/outside-argon-7nov/certs/primal_t0_16rules_84conds_exact.json) (which uses **zero `7->5` rules**), the `7->7` rule **`gk00_10`** (`EDGE(7->7)[S.L+1=S S.L-1=S S.A+1=5 S.A-1=5 R.L+2={67} R.L-2={67}]`, $w = 0.016917238$) fires with `coef = -2` (`pay=2, get=0`) on Row B and `coef = 0` on Row A, creating an exact $-0.033834477$ gap that allows $\text{lq}(6,6,5) = 0.251280 < \text{lq}(6,6,6) = \text{lQ}(6,6,30) = 0.268197$ and discharges Row A (`LHS = 0.999996645 <= 1`), Row B (`LHS = 0.605486117 <= 1`), and `H05 = 7/7676655/7657666` (`LHS = 0.821968344 <= 1`) without Kill B or any `7->5` rules. In the 16-rule sparse vertex [`primal_t0_sparse_16rules_pure567_exact.json`](file:///Users/kylemathewson/GraphColouringNov/outside-argon-7nov/certs/primal_t0_sparse_16rules_pure567_exact.json) (`701f0874`), **all 6 `mrowL [6,6,*]` variables are identically `0`**.
2. **Non-`7->5` Pure `7->7` 1-Sentence Keys That Relieve Row A Alone (`coef = -2`, `Row B = 0`, `S_pos = 0`, `cons2_pos = 0`)**:
   - On Row A at dart $i = 0$ (`7->7`), `OUT` has `S.L+3 = 5, S.L-3 = 5, S.A+1 = 7, S.A-1 = 7`, whereas on `IN` (`get`), `tab.MASK[(±1, 6, 6, 6, 5, 5, 6)] = 30 = {6,7,8,9}` **forbids `5` at the neighbour's $L_{\mp 3}$**. Thus **`cand_77_rowA_selfclean_1 = EDGE(7->7)[S.L+1=6 S.L+2=6 S.L+3=5 S.L-1=6 S.L-2=6 S.L-3=5 S.A+1=7 S.A-1=7 R.L+2=6 R.L-2=6]`** (and its 8-condition relaxation `cand_77_rowA_selfclean_2`) achieves **`pay = 2, get = 0` (`coef = -2`) on Row A**, **`coef = 0` on Row B**, and **`0` positive rows on `senders` and `cons2`**.
3. **100%-Coverage 1-Sentence Keys for the Un-Killable `d7 link-8578656` Class (`15,776` `R7_5678` / `1,989` `R7_567` Rows)**:
   - In the 151-key library, `gk00_5` relieves `1,974 / 1,989` (`99.25%`) of the $s \in \{5,6,7\}^7$ rows in `link-8578656`, missing only the `15` rows with `R.L+2 = R.L-2 = 5` at both `6`s. Pure link-level 1-sentence keys such as **`cand_78_link8578656_d0 = EDGE(7->8)[S.L+1=5 S.L+2=7 S.L+3=8 S.L-1=6 S.L-2=5 S.L-3=6]`** and **`cand_76_link8578656_d4 = EDGE(7->6)[S.L+1=5 S.L+2=6 S.L+3=8 S.L-1=8 S.L-2=7 S.L-3=5]`** relieve **100% (`15,776 / 15,776`)** of `link-8578656` with `0` positive rows on `S` and `R7`.

### 8.3 Exact Resolution of `CONS2SHARP` (`C 778979`) on `k86L` ([`k86L_cons2sharp_safe_t0_exact.json`](file:///Users/kylemathewson/GraphColouringNov/outside-argon-7nov/certs/k86L_cons2sharp_safe_t0_exact.json))

- Unrefined `cg12_76_0 = EDGE(7->6)[R.L+2={6789} R.L-2={6789}]` enters `cons2` link `778979` at `+6` (`+2` per 7-neighbour) because on any all-big 6-wheel $L \in \{7,8,9\}^6$ (`5,888` pairs, `184` pure-`E` rows), every vertex has degree $\ge 7$, so `R.L+2` and `R.L-2` always lie in $\{7,8,9\} \subset \{6,7,8,9\}$.
- Adding the single predicate `S.L+1=S` (`{5,6}`) yields **`cg76_SL1_S = EDGE(7->6)[S.L+1=S R.L+2={6789} R.L-2={6789}]`** (`3` predicates), which:
  1. Has **identically `0` coefficient on `C 778979` and on all `5,888` all-big pairs $L \in \{7,8,9\}^6$ (`184` pure-`E` rows)**,
  2. **Closes all `2,749` `k86L` rows to exact $t^* = 0$ (`[P]`)** with unconstrained LP value $t^*_{\text{unc}} = -0.067832013$ (`+161x` the `k86L` dual gap, stronger than unrefined `cg12_76_0`'s `-0.053040159`), and
  3. **Alone as a 1-key rule set (`1` active `E` key total)** closes all `2,749` `k86L` rows + all `184` all-big 6-wheels to exact $t^* = 0$ ($t^*_{\text{unc}} = -0.025271535$), and remains exact $t^* = 0$ across all five `f2b` rule sets (`9,326`, `6,718`, `6,290`, `5,974`, and `0` `f2b` rules).
- Alternatively, under the **Generalized Even-Split 6-Relay Law** $h(L_6, k) = (n_5(L_6) g(L_6) + I_{7\to 6}(L_6)) / n_{\text{big}}(L_6)$ ([`primal_t0_coupled_6relay_16rules_exact.json`](file:///Users/kylemathewson/GraphColouringNov/outside-argon-7nov/certs/primal_t0_coupled_6relay_16rules_exact.json), `b1ec9053`), every `cons2` row with $n_{\text{big}}(L_6) \ge 1$ (including `C 778979` where $n_{\text{big}} = 6$) relays 100% of any $7\to 6$ inflow out across its big neighbours (`LHS = 0`).

### 8.4 Audit of the 6–7 Nov Soundness Fixes (`Z-Consistency` `2db75746` & `rpatN3_rot` `8b90a842`), Exact `[P]` Duals, `129`-Rule MILP Set-Cover, and `KEYSPEC v2` Splitting

1. **`rpatN3_rotation_justified.txt` (`8b90a842`, `2,241` patterns vs `2,287` in `s39o`)**: Adds `0` receivers to `R7_567` / `R7_5678` and `511` degree-8 receivers to `R8_567`. Every existing Degree-8 exact $t^* = 0$ certificate (`17` rules, `24` keys, `37` keys, `51` keys) **already satisfies all `511` newly unexcused `R8_567` receivers with `0` violations (`max_excess <= -6.19`)** ([`zcons_audit_567_d8_exact.json`](file:///Users/kylemathewson/GraphColouringNov/outside-argon-7nov/certs/zcons_audit_567_d8_exact.json)).
2. **Exact Rational `[P]` Dual Certificates of the Z-Consistent (`2db75746`, `6,718` Rules) v1 `{5,6,7}` Floor ([`dual_zcons_6718_567_exact.json`](file:///Users/kylemathewson/GraphColouringNov/outside-argon-7nov/certs/dual_zcons_6718_567_exact.json), `1ac98460`)**:
   - Dropping the `2,608` Z-inconsistent rules (`9,326 -> 6,718` in `2db75746`, which drops `698` `d7_w6` and `381/side` `d7_w7` rules) raises the unsplit v1 `{5,6,7}` floor from $t^* = 0$ to exact rational dual bounds (`0` free variables, `0` violations):
     - **`16` rules (`84` conds)**: $D_{\text{exact}} = \frac{13194218569709583}{1045824282250324993} \approx +0.012616095$ (`643` support rows),
     - **`87` Studio keys**: $D_{\text{exact}} = \frac{8851759538074121175711696972}{793957669790938275263755256507} \approx +0.011148906$ (`792` support rows),
     - **`151` library keys**: $D_{\text{exact}} = \frac{52592746610205114535272128201039028}{4972653642923675975909515615063729463} \approx +0.010576394$ (`808` support rows; `69.18%` of $|\lambda|$ on `mrow` rows, matching the Swarm's `GL2–GL5` dual shape).
3. **`KEYSPEC v2` Private-Letter Splitting & 4-Way `Base`/`Pic` Decomposition ([`keyspec_v2_zcons_567_exact.json`](file:///Users/kylemathewson/GraphColouringNov/outside-argon-7nov/certs/keyspec_v2_zcons_567_exact.json), [`wave4_analysis_exact.json`](file:///Users/kylemathewson/GraphColouringNov/outside-argon-7nov/certs/wave4_analysis_exact.json))**:
   - Splitting `w6` into `{5}, {6}, B` (`v2_w6_56B_w7_diff`) eliminates **99.5%–100% of the `IN`-slot mask-widening penalty** (dropping the `151`-key floor from `0.010776` to `0.009200`, and with `Kill B + H05` from `0.010103` to `0.007424`, matching the `Base=6718, Pic=Orig` floor `0.007411`). The remaining `0.007424` is the exact `mrowR2` (`M(7, ..., 31) >= h(p=5)`) / `mrowL` / `mrowQ` base-row floor because `POS10` `OUT` slots (`c -> w_i`) do not encode the link-6 private letter $p_i$.
4. **Global Minimum MILP Set-Cover of Dropped `d = 7` `f2b` Rules Restoring Exact $t^* = 0$ ([`zcons_audit_567_d8_exact.json`](file:///Users/kylemathewson/GraphColouringNov/outside-argon-7nov/certs/zcons_audit_567_d8_exact.json))**:
   - Out of all `1,079` dropped $d = 7$ rule-families (`698` `d7_w6` + `381/side` `d7_w7`), a **provably global-minimum HiGHS MILP set-cover of just `129` rule-families (`87` `d7_w6` + `42/side` `d7_w7`, or `119` on `primal_d8_studio_17rules_exact.json`)** restores **100% (`0 / 110,087` violations, `[P]`)** of our fixed exact $t^* = 0$ certificate [`primal_t0_16rules_84conds_exact.json`](file:///Users/kylemathewson/GraphColouringNov/outside-argon-7nov/certs/primal_t0_16rules_84conds_exact.json) without re-solving the LP, and just **`51` rule-families (`35` `d7_w6` + `16/side` `d7_w7`)** cover 100% of the active LP-dual `R` rows of `2db75746` (curing `82.7%` of all `2,401` violated receivers).

### 8.5 Exact `KEYSPEC v2` (`v2r_dp` 25-State Realisation Model) Certificates on `GL5`, Full-Stack Upper Bounds, and Z-Consistent `{5,6,7}` (`[P]`)

Implementing the true `KEYSPEC v2` joint realisation model (`eng_v2/v2r.py`, maximizing $\text{base}(\rho) + \text{keys}(\rho)$ over $\rho \in \prod_{j=0}^{d-1} \text{dom}_j$ via exact 25-state cyclic dynamic programming `v2r_dp` rather than independent envelope variables `M`, `Q7`, `lQ` and widened `IN` masks) yields three exact rational (`Fraction`) `[P]` certificates:

1. **Exact $t^* = 0$ (`[P]`) on Full-Stack `GL5` + All `5,888` All-Big `cons2` Rows under `KEYSPEC v2` (`v2r_dp`), Global Minimum $K_{\text{GL5,v2}} = 1$ ([`gl5_keyspec_v2_t0_exact.json`](file:///Users/kylemathewson/GraphColouringNov/outside-argon-7nov/certs/gl5_keyspec_v2_t0_exact.json))**:
   - On the full-stack `GL5` benchmark (`cert_p1_00_def2afcc.json`, `3,035` rows: `692` $d \in \{7,8\}$ receivers evaluated by exact 25-state `v2r_dp`, `42` $d \ge 9$ receivers, `459` `senderR2`, `441` `cons2`, `821` `mrowR2`, `534` `mrowQ`, and `46` `mrowL` rows) augmented with all `184` extreme all-big `cons2` rows (`5,888` all-big pairs $L \in \{7,8,9\}^6 \times \{5,7\}^6$ including `C 778979`), **`Config 3a` (`64` active keys including `cg76_SL1_S`)** achieves unconstrained LP floor **$t^* = -0.173205890 < 0$** (`0` violations across all families at $t = 0$ in exact `Fraction` arithmetic, minimum `v2r_dp` slack $\frac{173205887}{1000000000}$).
   - Moreover, **a single active key (`K_GL5,v2 = 1`: `w6b16f_v01 = EDGE(7->B)[S.L+2=6 S.L-1={5679} S.L-2=S S.L-3=5 S.A-1=7 R.L+2=B]` at exact weight $w = \frac{158141891}{500000000} = 0.316283782$)** closes the entire `GL5` + `5,888` all-big `cons2` benchmark to **exact $t^* = 0$ (`[P]`, unconstrained $t^* = -0.000990275 < 0$, `0` violations across all `692` exact `Fraction` 25-state `v2r_dp` receiver evaluations)**.
2. **Exact `KEYSPEC v2` (`v2r_dp`) Audit and Cutting-Plane Repair of the Full-Stack Upper Bound Points ([`fullstack_v2_upper_repair_exact.json`](file:///Users/kylemathewson/GraphColouringNov/outside-argon-7nov/certs/fullstack_v2_upper_repair_exact.json))**:
   - Evaluating exact `Fraction` 25-state `v2r_dp` across all `102` `ST-75` $d \in \{7,8\}$ binding receiver violators on `sol_k86MS5_in03_tight__K3l5j.json` ($t_{\text{v1}} = 0.018674922$) proves that **5 of the 102 violators drop strictly below $t = 0$ (`v2_t_implied_exact < 0`, from $+0.018675$ to $-0.022386$ and $-0.058315$, drops of $+0.041061$ to $+0.076990$)** because under `v2r_dp` no single private-letter assignment $\rho_j = (x_j, y_j) \in \text{dom}_j$ can simultaneously realize the worst-case `lQ` and `IN`-slot demands across adjacent darts.
   - Because the remaining `97` binding violators have a concrete singleton realisation $\rho^* \in \prod_j \text{dom}_j$ attaining `LHS_v2 = LHS_v1`, we ran an exact `KEYSPEC v2` (`v2r_dp`) cutting-plane repair over the `7,833`-row neighborhood pool (`senders + cons2 + 5,888 all-big cons2 + d7/d8 v2r_dp + d9`) within L$\infty$ box radius $\Delta = 10^{-4}$ and certified three exact `Fraction` (`[P]`) upper-bound repairs (`0` violations across all families at $t_{\text{exact}}$):
     - `sol_k86MS5_in03_tight__K3l5j`: $t_{\text{v1}} = 0.018674922 \to t_{\text{v2r,exact}} = \frac{18447259009}{1000000000000} = 0.018447259$ (`-0.000228`),
     - `sol_repS5MW_02_tight__K3l5j`: $t_{\text{v1}} = 0.018551357 \to t_{\text{v2r,exact}} = \frac{4581656499}{250000000000} = 0.018326626$ (`-0.000225`),
     - `sol_repS5MW_03__K3l5j`: $t_{\text{v1}} = 0.018725086 \to t_{\text{v2r,exact}} = \frac{8886843007}{500000000000} = 0.017773686$ (`-0.000951`).
3. **Exact `KEYSPEC v2` (`v2r_dp`) Comparative Analysis & Exact $t^* = 0$ (`[P]`) Certificate on the Z-Consistent (`2db75746`, `6,718` Rules) `{5,6,7}` World ([`primal_t0_zcons_6718_keyspec_v2_567_exact.json`](file:///Users/kylemathewson/GraphColouringNov/outside-argon-7nov/certs/primal_t0_zcons_6718_keyspec_v2_567_exact.json))**:
   - Across all `110,087` `R7_567` receivers under raw `2db75746` (`6,718` rules), replacing unsplit `KEYSPEC v1` envelope rows by exact `KEYSPEC v2` (`v2r_dp`) reduces $t^*$ by **`-0.003030` to `-0.003472`** across every key set and domain (`0.013303 -> 0.010274` on `16` rules; `0.012363 -> 0.009063` on `16` rules + `KillB+H05+offc_K3g`; `0.009255 -> 0.006026` on `257` master keys; `0.008522 -> 0.005051` on `257` master keys + `KillB+H05+offc_K3g`).
   - Adjoining the global-minimum `129` dropped $d=7$ `f2b` rule-families (`87` `d7_w6` + `42/side` `d7_w7`) yields an exact `Fraction` (`[P]`) $t^* = 0$ primal (`16` rules, `84` predicates, `kill_B_required = False`) with **`0` violations across all `110,087` `R7_567` receivers under both `v1` and exact `Fraction` 25-state `v2r_dp`**, `0` violations across all `2,840` `alive_S`, `2,838` `alive_C`, and `3,338` `mrow_closure` rows, and pointwise dominance $\text{LHS}_{\text{v2r,dom567}}(r) \le \text{LHS}_{\text{v2r,dom56789}}(r) \le \text{LHS}_{\text{v1}}(r) \le 1$ verified identically across all tight receivers.

### 8.6 RSST 32-Rule Translation, `pubrules` + 633-Config Containment Audit, `GL5` Single-Row `p1r` Closure, `repK1MW_08` Ceiling Repair, and 125-State / 3,125-Edge Karp Tail LP Potentials ([`rsst_closure_and_big2big_exact.json`](file:///Users/kylemathewson/GraphColouringNov/outside-argon-7nov/certs/rsst_closure_and_big2big_exact.json), `[P]`)

1. **Exact Classification & Translation of RSST's 32 Discharging Rules (`38` Base Parts in `discharge.v`) into `EDGE(u->v)[...]` and `PAYER8SPEC W5` (`[P]`)**:
   - **28 of the 38 RSST base rules** (`drule1` $\times 2$, `drule2`, `drule2'`, `drule3`, `drule3'`, `drule4`, `drule4'`, `drule6`, `drule8`..`drule24`, `drule26`) are **100% exactly expressible** in our 12-coordinate `EDGE(u->v)[S.L+1..+3 S.L-1..-3 S.A+1 S.A-1 R.L+2 R.L-2]` grammar (`extra = []`, since zero RSST rules ever constrain far hats $\text{hat}_0, \text{hat}_5, \text{hat}_6, \text{hat}_7$).
   - **4 base rules (`drule5`, `drule7`, `drule25`, `drule27`)** read a second-neighborhood fan degree (`fan(j=1,k=1)` in `drule5`/`drule7`, `fan(j=3,k=2)=5` in `drule25`, `fan(j=2,k=1..2)` in `drule27`), and **6 base rules (`drule28`, `drule29`, `drule30`, `drule31`, `drule31'`, `drule32`)** are $d=8$ payer rules (`EDGE(8->{789})` / `EDGE(8->7)`) reading far spokes `S.L+-3` (and antipodal `S.L+4=5` in `drule29`/`drule32`), which project cleanly into `PAYER8SPEC W5` (`S.L+-3` wildcarded, extended to both payers $8$ and $9$, yielding `357` combined keys = `280` `16fikpq` + `24` `w6b16s_p8` + `53` RSST & W5 hat variants).
2. **`pubrules.py` Ledger + RSST 633-Configuration Containment Audit on Top 39 `GL5` Floor Rows and 7 `ST-86`/`ST-89` Ceiling Binder Classes (`[P]`)**:
   - Across the top 39 `receiverR2` rows of `GL5` (`cert_p1_00_def2afcc.json`, skipping rank 22 `7 5677659/5666555` with a `9` in link): **20 end strictly $< 0$**, **16 end at $0.0$**, and **3 (`r05: 6776655/6656658`, `r11: 6776665/6656755`, `r35: 7676655/7756657`)** have fillings at $+0.1$. Exhaustive checking against RSST's 633 configurations (`grow.rsst()`) proves that **100% of positive fillings** on `r05` (`1,024/1,024` for priv $\ge 6$, `34,025/34,025` for priv $\ge 5$, killed by `RSST 2.3701166`, `RSST 2.1551966`, `RSST 2.260517966`), `r11` (`16,384/16,384` for priv $\ge 6$, `270,625/270,625` for priv $\ge 5$, killed by `RSST 2.3711966`), and `r35` (`1,024/1,024` for priv $\ge 6$, `27,500/27,500` for priv $\ge 5$) contain an RSST reducible configuration (**`0` surviving positive fillings**).
   - Across the 7 `ST-86`/`ST-89` ceiling binder classes (`R1..R7`): **1 ends at $-0.1$** (`R3: 7 5566786/5675657`) and **6 end at $0.0$** (`R1, R2` via `drule8, 9, 10'`; `R4..R6` via `drule29m` in RSST / `rule042_1` in NL26; `R7` via `drule28, drule29` in RSST / `rule040, rule043` in NL26).
   - On **Row B (`r02: 7 7666666/6567656`)**, the 4 pure 6-flanked 6-spokes (`j = 2, 3, 4, 5`) carry **`0.649646` (`0.651226`)** of net 6-spoke relay load (and all 6 6-spokes carry `0.870593` of `1.001233`), whereas under RSST `r02` ends in $[-0.6, -0.4]$ because RSST routes charge big-to-big rather than through 6s.
3. **Exact `Fraction` (`[P]`) Single-Row `p1r` $t = 0$ Closure on `GL5 + 8,011` `mrow` Envelope Rows `+ 5,888` All-Big `cons2` Rows Using `220` Baseline Keys + Only `5` RSST Hub-7 `7->7+` Rules**:
   - Whereas `GL5` under single-row `p1r` (`220` keys `16fi`) has floor $t^* = +0.001233311856$, adjoining **only 5 RSST hub-7 `EDGE(7->7+)` rules** (`rsst_drule27` at weight `3`, `rsst_drule23` at weight `3`, `rsst_drule11` at weight `3`, `rsst_drule18` at weight $\frac{1466467362493}{1000000000000}$, and `rsst_drule10p` at weight $\frac{491987567979}{1000000000000}$) drops `GL5` + all `8,011` `(h, M), (q, Q), (lq, lQ)` domain-envelope rows + `5,888` all-big `cons2` rows under **single-row `p1r` (without even needing `v2r_dp` cutting planes, and therefore also closing every `v2r_dp` receiver pointwise via `v2r_dp <= p1r`!)** to **$t^* = -0.019293641762 < 0$** (`0` violations across all families at $t = 0$ in exact `Fraction` arithmetic, minimum `GL5` slack $\frac{9646820879}{500000000000} = 0.019293641758$), and the full 357-key combined pool drops `v2r_dp` to **$-0.232803496$**.
4. **Full-Stack Ceiling Repair on `ST-89`, `MK1_in09_tight`, and `repK1MW_08` (`[P]`)**:
   - Adding the RSST `drule1..32` and `w6b16s_p8` / `w6b16q` keys within L$\infty$ box radius $\Delta = 2 \times 10^{-4}$ over the 141-row ceiling pool (`R1..R7 + ST-86 + ST-89 + ST-91 + ST-75`) + `22,514` `senderR2` + `1,424` canonical 6-links (`cons2`) lowers `ST-89` ($0.015524 \to 0.014864$ with 260 keys $\to \mathbf{0.014437}$ with 357 keys), `MK1_in09_tight` ($0.015332 \to 0.014672 \to \mathbf{0.014263}$), and `repK1MW_08` ($0.015175192 \to 0.014515728 \to \mathbf{0.014130080204}$, certified in exact `Fraction` arithmetic at $t_{\text{exact}} = \frac{3532520051}{250000000000}$ with `R7: 8 55557557/58586788` dropping from `0.015175173` to $\frac{10602439213}{1000000000000} = 0.010602439213$).
5. **Exact `Fraction` (`[P]`) 125-State / 3,125-Edge Karp Tail LP Potential Certificate for $d \ge 9$ Receivers (Recommendation 3)**:
   - By Karp's / Howard's theorem on the 125-state de Bruijn transfer graph $V_{\text{Karp}} = \{5,6,7,8,9\}^3$ ($3,125$ entries, $625$ directed transitions $(w_{i-2}, w_{i-1}, w_i) \to (w_{i-1}, w_i, w_{i+1})$), adjoining 125 LP potential variables $\phi(u) \in \mathbb{Q}^{125}$ and linear constraints $M_{\text{step}}[u, v] + \phi(u) - \phi(v) \le \lambda^*$ telescope identically around every cycle of length $d \ge 9$ to bound $\text{load}(C) \le d \cdot \lambda^*$.
   - We certify exact rational (`Fraction`) potentials $\phi \in \mathbb{Q}^{125}$ across all $3,125$ state pairs on `repK1MW_08` with **$\lambda^* = \frac{583629103}{1000000000} = 0.583629103 < 1$** ($d_0 = \frac{6 - t_{\text{stored}}}{1 - \lambda^*} = \frac{6015174607618}{418462647709} \approx 14.374129$, covering all $d \ge 15$ without row separation) and on `seed_sol_k86GL5_p1` ($\lambda^* = \frac{717523737}{50000000} = 14.350474740$, `38` tight transitions).

6. **Discharging of Bottleneck Ceiling Rows to $t \le 0$ via Extended KEYSPEC Degrees and PAYER8SPEC Conjunctions (`[P]`)**:
   - **Requirement R1 ($d = 9$ Ceiling Row Discharge)**: Extending `KEYSPEC` receiver degrees $T_{\text{deg}}$ from $\{5,6,7,8\}$ to $\{5,6,7,8,9,10\}$ allows degree $d \ge 9$ wheels to participate in realization DP and receive incoming `EDGE` payments. On the bottleneck $d = 9$ ceiling row `9 555555557/666776766` (previously stuck at $t = 0.014130080$), exact rational 25-state cycle realization DP yields $\text{load} = \frac{2462440137771}{1000000000000}$, giving residual charge $t = \text{load} - (9 - 6) = -\frac{537559862229}{1000000000000} \approx -0.537559862229 \le 0$, completely discharging the $d = 9$ ceiling pool (`d9_ceiling_pool_floor_exact` $= -537559862229/1000000000000 \le 0$).
   - **Requirement R2 (R2 Ceiling Class Discharge)**: Incorporating `tabV8` middle/far private letter masks (`P8m`, `P8p`, `eight_m`, `eight_p`) into `_gk_posmasks_w5` under `PAYER8SPEC W5` and enabling 2-spoke conjunction rules (`drule15`–`drule17`, `drule32`) to read an 8-spoke's far private letters (`S.R0`) discharges both realizations of `R2` strictly below zero:
     - `R2_orig: 7 5557557/5778877`: $\text{total\_dp} = \frac{494003747249}{500000000000}$, $t = \text{total\_dp} - 1 = -\frac{5996252751}{500000000000} \approx -0.011992506 \le 0$ (`st87_R1_R7_repaired_exact[1]`).
     - `R2_prompt: 7 5558558/6776677`: $\text{total\_dp} = \frac{799396716003}{1000000000000}$, $t = \text{total\_dp} - 1 = -\frac{200603283997}{1000000000000} \approx -0.200603284 \le 0$ (`r2_prompt_repaired_exact`).
