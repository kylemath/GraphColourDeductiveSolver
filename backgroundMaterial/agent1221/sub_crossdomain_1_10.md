# Cross-Domain Analysis: 10 Cutting-Edge Mathematical Areas and the Four Colour Theorem

**Agent:** 1221  
**Date:** 17 February 2026  
**Project:** Graph Colouring  
**Scope:** Cross-domain feasibility analysis (Areas 1–10)

---

## Preamble

The Four Colour Theorem (4CT) states that every planar graph $G$ satisfies $\chi(G) \leq 4$. The only known proofs proceed by (i) discharging arguments showing that any minimal counterexample must contain one of $N$ configurations from an unavoidable set, and (ii) computer-verified reducibility of each configuration. No human-readable deductive proof exists. The key mathematical objects in play are: Euler's formula ($V - E + F = 2$ and the corollary $E \leq 3V - 6$), Kempe chains (maximal bichromatic connected subgraphs whose colour-swap preserves validity), chromatic polynomials ($P(G,k)$ counting proper $k$-colourings), nowhere-zero flows (Tutte's dual formulation), and the planar separator theorem (every $n$-vertex planar graph has a separator of size $O(\sqrt{n})$).

This report examines 10 areas from modern mathematics and mathematical machine learning, evaluating each for genuine technical bridges to the 4CT. The analysis is intentionally rigorous: speculative connections are flagged as such, and areas with no credible pathway are honestly assessed.

---

## 1. Geometric Deep Learning

### Core Ideas

Geometric deep learning (GDL) is a unifying framework for designing neural network architectures that respect the symmetry structure of their input domains. The central principle is **equivariance**: if a symmetry group $\mathcal{G}$ acts on the input space $\mathcal{X}$, then a layer $f: \mathcal{X} \to \mathcal{Y}$ should satisfy $f(g \cdot x) = g \cdot f(x)$ for all $g \in \mathcal{G}$. This generalises convolutional neural networks (translation-equivariance on grids) to arbitrary domains: graphs, manifolds, point clouds, and meshes. Key architectures include message-passing neural networks (MPNNs), where each vertex aggregates information from its neighbours in learnable rounds, and higher-order architectures like $k$-WL networks that track $k$-tuples of vertices and are aligned with the $k$-dimensional Weisfeiler-Leman graph isomorphism hierarchy.

The mathematical foundation draws on representation theory (decomposing feature spaces into irreducible representations of the symmetry group), differential geometry (defining convolutions on Riemannian manifolds via the Laplace-Beltrami operator), and combinatorial topology (simplicial and cellular complexes as higher-order generalisations of graphs).

### Connection to 4CT

The connection is surprisingly concrete through two channels:

**Channel 1 — Expressivity and the WL hierarchy.** MPNNs are known to be bounded in expressivity by the 1-WL (colour refinement) algorithm. The 1-WL test cannot distinguish all non-isomorphic graphs, and in particular it cannot detect planarity. However, 3-WL and higher can distinguish all planar graphs (since planar graphs have bounded tree-width in a local sense). A GDL architecture with provably sufficient expressivity could, in principle, learn to verify 4-colourability of planar graphs — not as a proof, but as a computational oracle that might reveal structural patterns.

**Channel 2 — Equivariant colouring.** A proper vertex colouring can be viewed as a function $c: V \to \{1,2,3,4\}$ that is constrained by the graph structure. GDL provides a natural language for studying such functions: the automorphism group $\text{Aut}(G)$ acts on the set of colourings, and an equivariant network could learn to produce colourings that are "canonical" in some symmetry-respecting sense. This is related to the concept of a **canonical form** for colourings under graph automorphisms.

### Specific Technical Bridge

The most transferable result is the **Equivariant Polynomial Theorem** (Maron et al., 2019): any permutation-equivariant polynomial function on $k$-tensors over graphs can be expressed in terms of a specific basis of equivariant operators. For $k = 2$, these operators include adjacency multiplication and trace operations — precisely the linear-algebraic operations that appear in the theory of chromatic polynomials and Tutte polynomials. An equivariant network operating on the adjacency tensor of a planar graph could, in principle, learn to compute (or approximate) the chromatic polynomial $P(G, 4)$ and certify that it is positive.

Additionally, **spectral graph networks** that use the eigenvalues of the graph Laplacian $L = D - A$ connect to Hoffman's bound $\chi(G) \geq 1 - \lambda_{\max}/\lambda_{\min}$. If a GDL architecture could learn tighter spectral bounds specific to planar graphs, it would provide a new computational route to 4-colourability.

### Feasibility

**Speculative.** GDL is a powerful computational framework, but the 4CT is a theorem requiring proof, not prediction. A neural network that correctly 4-colours every planar graph it encounters provides no mathematical guarantee. The value of GDL here is as a **discovery tool** — it might reveal structural invariants or colouring patterns that a human mathematician could then prove. As a direct proof method, it is not viable.

### Concrete Research Direction

Train a 3-WL-equivalent GDL architecture on the task of producing 4-colourings of random planar graphs (generated via random planar triangulations up to $n = 10{,}000$ vertices). Analyse the learned representations to determine whether the network implicitly computes Kempe chain structures or chromatic polynomial features. Specifically, extract the attention weights or message-passing coefficients and test whether they correlate with known reducibility indicators (e.g., whether the network assigns special intermediate representations to Birkhoff diamonds or other classically reducible configurations). If such correlations emerge, they would suggest new reducibility criteria that could shrink the unavoidable set.

---

## 2. Information Geometry

### Core Ideas

Information geometry applies Riemannian differential geometry to the space of probability distributions. Given a parametric family $\{p_\theta : \theta \in \Theta\}$, the **Fisher information matrix** $g_{ij}(\theta) = \mathbb{E}_{p_\theta}\left[\frac{\partial \log p_\theta}{\partial \theta_i} \frac{\partial \log p_\theta}{\partial \theta_j}\right]$ defines a Riemannian metric on $\Theta$, making the parameter space a Riemannian manifold. The resulting geometry is invariant under reparametrisation and encodes the statistical distinguishability of nearby distributions. Key structures include the **$\alpha$-connections** (a one-parameter family of affine connections, with $\alpha = 1$ giving the exponential connection and $\alpha = -1$ the mixture connection), **geodesics** (curves of minimal Fisher-Rao distance), and **dually flat structures** (the exponential family admits a pair of dual coordinate systems — natural and expectation parameters — with respect to which the manifold is flat).

### Connection to 4CT

The connection requires constructing a probability distribution from a graph colouring problem, which is actually quite natural:

**The Gibbs/Potts distribution.** Given a graph $G = (V, E)$ and an inverse temperature $\beta$, the **Potts model** assigns probability $p_\beta(\sigma) \propto \exp\left(-\beta \sum_{(u,v) \in E} \mathbf{1}[\sigma(u) = \sigma(v)]\right)$ to each assignment $\sigma: V \to \{1, \ldots, q\}$. The partition function is $Z_G(q, \beta) = \sum_\sigma \exp\left(-\beta \sum_{(u,v) \in E} \mathbf{1}[\sigma(u) = \sigma(v)]\right)$. At $\beta \to \infty$, only proper colourings survive, and $Z_G(q, \infty) = P(G, q)$, the chromatic polynomial. The 4CT is equivalent to $Z_G(4, \infty) > 0$ for all planar $G$.

The information geometry of the $q$-state Potts model on planar graphs is a well-defined Riemannian manifold parametrised by $(\beta, q)$ (with analytic continuation of $q$ to real values). The **phase transitions** of the Potts model on planar lattices — the points where the Fisher information metric degenerates — are known to relate to the zeros of $Z_G$ in the complex $q$-plane. The Beraha conjecture places the accumulation points of chromatic polynomial zeros at $B_n = 4\cos^2(\pi/n)$, with $B_\infty = 4$ being the critical value.

### Specific Technical Bridge

The **natural gradient** on the Potts model manifold provides a geometrically natural flow in parameter space. In the $(\beta, q)$-plane, the Fisher-Rao metric diverges at phase transitions, creating geometric singularities. For planar graphs, the structure of these singularities near $q = 4$ is directly related to the 4CT: the theorem implies that $q = 4$ is never a zero of the chromatic polynomial (since $P(G, 4) > 0$), which means the Potts model at $q = 4$ should have a specific geometric regularity.

The **Amari-Chentsov theorem** guarantees that the Fisher metric is the unique (up to scale) Riemannian metric invariant under sufficient statistics. This universality could constrain the possible behaviour of $Z_G(q, \beta)$ near $q = 4$ in ways that are not visible from purely combinatorial analysis.

### Feasibility

**Highly Speculative.** While the Potts model connection is mathematically legitimate, information geometry adds a layer of geometric abstraction that has not yet produced results about chromatic polynomials. The machinery is powerful but the gap between "the Fisher metric has interesting structure near $q = 4$" and "this proves $P(G, 4) > 0$" is vast. The main value is conceptual: information geometry provides a different lens through which to view the chromatic polynomial, and this change of perspective occasionally leads to breakthroughs.

### Concrete Research Direction

Compute the Fisher information matrix of the $q$-state Potts model on small planar triangulations ($n \leq 20$) as a function of $q$ and $\beta$, and study its spectral properties (eigenvalues as functions of $q$) near $q = 4$. Determine whether the condition $P(G, 4) > 0$ (i.e., the 4CT) manifests as a specific geometric property — for instance, positive definiteness of the Fisher matrix along the $\beta \to \infty$ limit at $q = 4$. If a clean geometric characterisation emerges, attempt to prove it holds for all planar graphs using the structural properties of planar embeddings (e.g., the fact that every planar graph is the medial graph of a surface triangulation).

---

## 3. Topological Data Analysis (TDA)

### Core Ideas

Topological Data Analysis uses tools from algebraic topology — primarily **persistent homology** — to extract qualitative structural features from data. Given a point cloud or a filtered simplicial complex, persistent homology tracks the birth and death of topological features (connected components, loops, voids) across a range of scale parameters. The output is a **persistence diagram** or **barcode**: a multiset of intervals $[b_i, d_i)$ representing the lifetime of each feature. Long-lived features (large $d_i - b_i$) are considered genuine topological signal; short-lived features are noise. The theory is grounded in the **stability theorem** (Chazal et al.), which guarantees that small perturbations of the input produce small changes in the persistence diagram (in the bottleneck or Wasserstein distance).

Beyond persistent homology, TDA includes **Mapper** (a tool for constructing simplified topological summaries of high-dimensional data), **persistent cohomology** (dual to homology, with ring structure), and connections to sheaf theory and derived categories.

### Connection to 4CT

The connection is indirect but substantive through two pathways:

**Pathway 1 — The topology of the colouring space.** For a graph $G$ and $k$ colours, the set of proper $k$-colourings forms a discrete set $\mathcal{C}(G, k) \subseteq \{1, \ldots, k\}^V$. One can define a graph on $\mathcal{C}(G, k)$ where two colourings are adjacent if they differ at exactly one vertex — this is the **reconfiguration graph** or **Kempe graph**. The topology (specifically, the connectivity) of this reconfiguration graph is deeply studied: Cereceda, van den Heuvel, and Johnson showed that for $k \geq \text{col}(G) + 2$ (where col is the colouring number), the reconfiguration graph is connected. For $k = 4$ and planar graphs, the reconfiguration graph's structure is intimately tied to the 4CT.

One can build a **Vietoris-Rips complex** on $\mathcal{C}(G, k)$ (using Hamming distance) and compute its persistent homology. The homological features of this complex encode structural information about the space of colourings: $H_0$ gives the number of connected components (reconfiguration classes), $H_1$ detects "colouring cycles" (sequences of Kempe swaps that return to the starting colouring via a non-trivial loop), and higher homology detects more complex structure.

**Pathway 2 — Filtrations on the graph itself.** Given a planar graph $G$, one can construct filtrations based on degree, centrality, or embedding coordinates, and compute the persistent homology of the resulting filtered complexes. The clique complex of $G$ has homology that encodes information about its chromatic number: specifically, the **Lovász bound** $\chi(G) \geq 1 + \text{conn}(\text{Hom}(K_2, G))$ relates the chromatic number to the topological connectivity of the Hom complex. While this bound is not tight for planar graphs (it does not prove the 4CT), TDA-style persistence computations on Hom complexes might reveal patterns specific to planar graphs.

### Specific Technical Bridge

The most concrete bridge is through the **neighbourhood complex** $\mathcal{N}(G)$ and Lovász's theorem: $\chi(G) \geq \text{conn}(\mathcal{N}(G)) + 3$. For Kneser graphs, this bound is tight, yielding one of the most celebrated applications of topology to combinatorics. For planar graphs, $\text{conn}(\mathcal{N}(G)) \leq 1$ is required by the 4CT. Computing the persistent homology of $\mathcal{N}(G)$ for families of planar graphs could reveal whether the connectivity bound can be tightened or whether additional topological invariants (e.g., torsion in homology, cup product structure in cohomology) provide additional constraints.

### Feasibility

**Speculative.** The topological lower bounds on chromatic number ($\chi(G) \geq \text{conn}(\mathcal{N}(G)) + 3$) are powerful for specific graph families (Kneser graphs) but known to be weak for planar graphs. TDA adds computational muscle to topology but does not change the fundamental bound. The most promising direction is the analysis of reconfiguration spaces, where TDA could reveal structural features not visible to purely combinatorial methods — but this remains exploratory.

### Concrete Research Direction

Compute the persistent homology of the reconfiguration graph $\mathcal{R}(G, 4)$ for all planar triangulations on $n \leq 12$ vertices. Classify the resulting persistence diagrams and look for patterns: Do all planar graphs produce trivial $H_0$ (i.e., connected reconfiguration graphs)? If non-trivial $H_1$ features appear, do they correspond to known obstructions like Kempe-locked configurations? Compare with the persistence diagrams of $\mathcal{R}(G, 5)$ (which should always be connected by the Cereceda-van den Heuvel-Johnson theorem) to isolate phenomena specific to $k = 4$.

---

## 4. Mathematical Theory of Transformers/LLMs

### Core Ideas

The mathematical theory of transformer architectures seeks to understand, rigorously, the computational and statistical properties of attention-based neural networks. Key results include: universality theorems showing that transformers with sufficient depth and width can approximate any sequence-to-sequence function (Yun et al., 2020); the characterisation of transformers as performing iterative refinement in a residual stream (Elhage et al., 2021); connections between attention and kernel methods (Tsai et al., 2019); and the identification of in-context learning as implicit Bayesian inference or gradient descent in function space (Akyürek et al., 2023; von Oswald et al., 2023). Emergent abilities — capabilities that appear abruptly at scale — remain poorly understood theoretically, with proposed explanations ranging from phase transitions in loss landscapes to artefacts of evaluation metrics.

### Connection to 4CT

The connection is weak as a proof method but potentially interesting as a discovery and verification tool:

**Transformers as proof search engines.** Recent work on using LLMs for mathematical reasoning (e.g., AlphaProof, DeepMind's collaboration with IMO 2024) demonstrates that transformer-based systems can perform non-trivial proof search. A transformer trained on the formal proof library (including Gonthier's Coq formalisation of the 4CT) could potentially discover novel proof strategies — for instance, identifying that certain groups of the 633 RSST reducibility cases can be collapsed into parameterised lemmas, effectively compressing the proof.

**Attention as combinatorial search.** The self-attention mechanism computes pairwise affinities between tokens. If the "tokens" are vertices of a graph and the "attention pattern" reflects adjacency, then a transformer layer performs a form of message-passing. In fact, the connection between transformers and MPNNs is well-established. A multi-head attention mechanism with positional encodings can simulate Kempe chain identification: one head attends to colour-$a$ neighbours, another to colour-$b$ neighbours, and the composition identifies the bichromatic chain.

### Specific Technical Bridge

The most relevant technical result is the **Turing completeness of transformers** (Pérez et al., 2021): transformers with hard attention and positional encoding can simulate arbitrary Turing machines. This means, in principle, a transformer can verify reducibility of any configuration — but so can any Turing-complete system, so this is not a useful bridge.

More interesting is the **circuit complexity** perspective: the 4CT reducibility check for each configuration can be expressed as a bounded-depth Boolean circuit. If transformer computation corresponds to bounded-depth circuit classes (as suggested by Merrill and Sabharwal, 2023), then the question becomes whether the 4CT reducibility check lies in a circuit class that transformers can efficiently represent. This connects to the broader question of whether the 4CT has a proof in a specific logical fragment (e.g., bounded arithmetic).

### Feasibility

**Highly Speculative.** Transformer theory is about understanding neural network computation, not about proving combinatorial theorems. The connection to the 4CT is purely instrumental: transformers might assist in proof search or proof compression, but the mathematical theory of transformers itself does not provide new tools for graph colouring. The circuit complexity connection is intriguing but undeveloped.

### Concrete Research Direction

Fine-tune a transformer-based proof assistant (e.g., built on the Lean or Coq proof corpus) on the specific task of verifying D-reducibility of graph configurations. Measure whether the model can generalise from the 633 RSST configurations to correctly predict reducibility of novel configurations not in the training set. If it can, analyse the model's internal representations to identify what features it uses — this could reveal new sufficient conditions for reducibility that simplify the proof. If it cannot generalise, this itself is informative: it suggests the 633 configurations are not instances of a simple pattern.

---

## 5. Mean-Field Game Theory & Agentic AI

### Core Ideas

Mean-field game (MFG) theory, introduced by Lasry-Lions (2006–2007) and Huang-Malhamé-Caines (2006), studies strategic interactions among a continuum (or large finite number) of rational agents, each infinitesimally small. The key insight is that in the limit of infinitely many agents, each agent's optimal strategy depends on the population only through its **distribution** (the mean field), not through individual interactions. The resulting system couples a **Hamilton-Jacobi-Bellman equation** (for individual optimality) with a **Fokker-Planck equation** (for population evolution):

$$-\partial_t u + H(x, \nabla u) = F(x, m(t)), \quad \partial_t m - \nabla \cdot (m \nabla_p H(x, \nabla u)) = 0,$$

where $u$ is the value function, $m$ is the population density, $H$ is the Hamiltonian, and $F$ encodes the interaction cost. MFG theory has been extended to finite-state spaces (where the Fokker-Planck equation becomes a master equation on a finite set), multi-population games, and games on networks.

### Connection to 4CT

The connection is tenuous but can be articulated as follows:

**Graph colouring as a coordination game.** Consider each vertex of $G$ as an autonomous agent choosing a colour from $\{1, 2, 3, 4\}$. The payoff for each vertex-agent is $-\sum_{(v,w) \in E} \mathbf{1}[c(v) = c(w)]$ — agents are penalised for matching their neighbours. A proper 4-colouring is a **Nash equilibrium** of this game (no vertex can improve by changing colour, since it already has no conflicts). The question "does a proper 4-colouring exist?" becomes "does this game have a Nash equilibrium with zero total penalty?"

In the mean-field limit, if the graph is a large regular lattice (or a random planar graph with some regularity), each vertex sees approximately the same neighbourhood distribution, and the mean-field approximation replaces the graph structure with a distributional interaction. The MFG equilibrium condition then becomes a fixed-point equation for the distribution of colours in the population.

**The problem:** The mean-field approximation discards the specific graph structure, replacing it with a distributional summary. But the 4CT is precisely about the specific structure of planar graphs — it fails for general graphs (e.g., $K_5$ requires 5 colours). The mean-field limit is too coarse to distinguish planar from non-planar graphs.

### Specific Technical Bridge

The most relevant structure is the **MFG on a graph** (Caines and Huang, 2018), where the mean field is not a single global distribution but a local distribution on each vertex's neighbourhood. For a planar graph, the degree constraint ($\Delta \leq 5$ for some vertex, by Euler) provides structural control on the local mean field. If one could show that the local MFG equilibrium on a planar graph always admits a solution with support on 4 colours, this would prove the 4CT.

However, this essentially reduces to proving the 4CT by other means — the MFG machinery adds formalism but not leverage. The Hamilton-Jacobi-Bellman / Fokker-Planck coupling does not simplify the combinatorial problem.

### Feasibility

**Highly Speculative.** The mean-field approximation is fundamentally at odds with the graph-structure-dependent nature of the 4CT. While the game-theoretic formulation of graph colouring is valid, MFG theory provides no tools that improve upon direct combinatorial or algebraic approaches. The local MFG variant is closer to the mark but reduces to a restatement of the problem rather than a solution.

### Concrete Research Direction

Study the **finite-agent** (non-mean-field) version: model the graph colouring game as a potential game and analyse the convergence of best-response dynamics (each vertex iteratively switches to its best colour given its neighbours' current colours). On planar graphs, does best-response dynamics always converge to a 4-colouring? This is essentially the study of the Kempe chain dynamics as a game — and the answer is known to be subtle (Kempe chain swaps do not always converge; there exist frozen colourings). Characterising the convergence landscape of colouring dynamics on planar graphs is a legitimate research problem, though it is better framed in terms of combinatorial reconfiguration than MFG theory.

---

## 6. Quantum-Inspired Classical Algorithms

### Core Ideas

Quantum-inspired classical algorithms are classical algorithms whose design is motivated by quantum computing techniques — particularly quantum walks, amplitude amplification, and the structure of quantum states — but which run on classical hardware. Key examples include: Tang's (2019) dequantisation of quantum recommendation systems, achieving $\text{polylog}(mn)$ time for low-rank matrix tasks using $\ell^2$-norm sampling; quantum-inspired algorithms for semidefinite programming (SDP) that exploit low-rank structure; and classical algorithms based on the simulation of variational quantum eigensolvers (VQE) for combinatorial optimisation.

The central idea is that quantum algorithms gain their advantage from working in high-dimensional Hilbert spaces with superposition and interference. When the input data has low-rank or sparse structure, a classical algorithm can simulate these quantum effects using random sampling, achieving comparable performance without a quantum computer.

### Connection to 4CT

**Channel 1 — SDP relaxations of chromatic number.** The Lovász theta function $\vartheta(\bar{G})$ is an SDP relaxation of the chromatic number: $\chi(G) \geq \vartheta(\bar{G})$ (where $\bar{G}$ is the complement). Computing $\vartheta$ via SDP is polynomial-time, and quantum-inspired algorithms for SDP could potentially compute it faster for large graphs. However, $\vartheta$ does not distinguish 4-colourable planar graphs from non-4-colourable general graphs (it is a bound, not an exact value), so this does not directly help with the 4CT.

**Channel 2 — Quantum walks and graph structure.** Quantum walks on graphs (and their classical simulations) can detect structural properties like bipartiteness, expansion, and the existence of specific subgraphs. A quantum walk on a planar graph, dequantised to a classical algorithm, might detect properties related to 4-colourability. The **Grover-like search** framework provides quadratic speedups for unstructured search; applied to the search for a proper 4-colouring, this would reduce the search from $4^n$ to $2^n$ — significant but not qualitatively new.

**Channel 3 — Tensor network methods.** Tensor networks, originally from quantum many-body physics, provide efficient representations of high-dimensional tensors with bounded entanglement. The chromatic polynomial $P(G, q)$ can be expressed as a **contraction of a tensor network** whose structure mirrors the graph $G$. For planar graphs, the tensor network is planar and can be contracted in polynomial time using the **planar tensor network contraction algorithm** (based on nested dissection). This is a genuinely interesting connection: it means $P(G, 4)$ can be computed exactly in polynomial time for planar graphs using tensor network methods, providing an alternative proof that 4-colourability is decidable in polynomial time (which is already known, since 4-colourability of planar graphs is guaranteed).

### Specific Technical Bridge

The tensor network contraction approach is the most concrete bridge. The chromatic polynomial $P(G, q)$ for a graph $G$ with $n$ vertices and $m$ edges can be written as the contraction of a tensor network where each edge contributes a tensor $T_{ij} = q \cdot \delta_{ij} - 1$ (or variants depending on the formulation). For planar graphs, the tree-width is $O(\sqrt{n})$ by the planar separator theorem, so the contraction can be performed in time $\exp(O(\sqrt{n}))$. Quantum-inspired improvements to tensor network contraction (e.g., using randomised SVD for low-rank approximations within the contraction) could further reduce the constant factors, making it practical to compute $P(G, 4)$ for moderately large planar graphs.

More speculatively, the **MERA** (multiscale entanglement renormalisation ansatz) tensor network architecture, which has a hierarchical structure matching the recursive structure of planar separators, could provide a natural framework for a hierarchical proof of the 4CT: prove that each level of the MERA hierarchy preserves 4-colourability.

### Feasibility

**Plausible** (for tensor network methods); **Speculative** (for quantum walk dequantisation). The tensor network approach to computing chromatic polynomials is mathematically sound and practically feasible. It does not provide a new proof of the 4CT, but it provides efficient computational tools for studying chromatic polynomials of planar graphs, which could support the algebraic proof strategy (showing $P(G, 4) > 0$ for all planar $G$ by studying the structure of $P$ as computed by tensor contraction).

### Concrete Research Direction

Implement the planar tensor network contraction algorithm for the chromatic polynomial and compute $P(G, 4)$ for all planar triangulations up to $n = 30$ vertices. Study the structure of the intermediate tensors in the contraction: do they exhibit low-rank structure or other regularities at $q = 4$ that do not appear at $q = 3$? If so, this would suggest a structural explanation for why $P(G, 4) > 0$ — an explanation that might be provable by induction on the tree-decomposition, yielding a new proof strategy.

---

## 7. Scientific Machine Learning (SciML)

### Core Ideas

Scientific machine learning combines domain knowledge — typically in the form of partial differential equations (PDEs) — with neural network architectures to create hybrid models for scientific simulation. Key paradigms include: **physics-informed neural networks** (PINNs), which embed PDE residuals as soft constraints in the loss function; **neural operators** (e.g., Fourier Neural Operator, DeepONet), which learn mappings between function spaces; and **differentiable simulators**, which embed traditional numerical solvers inside autodiff frameworks. The mathematical foundation draws on approximation theory (universal approximation in Sobolev spaces), PDE theory (well-posedness, regularity), and numerical analysis (convergence, stability).

### Connection to 4CT

The connection requires interpreting graph colouring as a continuous problem amenable to PDE-like analysis:

**The heat equation on graphs.** The graph Laplacian $L = D - A$ generates a discrete heat equation $\dot{u} = -Lu$ on the vertices. The eigenvalues of $L$ for a planar graph are constrained by planarity (e.g., the Fiedler value satisfies bounds related to the genus). A "colouring field" $u: V \to \mathbb{R}^4$ (with each vertex assigned a 4-dimensional vector representing colour probabilities) evolves under a nonlinear diffusion equation that penalises adjacent vertices with similar colour vectors. The steady states of this diffusion are related to proper colourings.

**PDE on the dual surface.** A planar graph defines a cell decomposition of the sphere. One can define a PDE on this cell complex — for instance, an Allen-Cahn equation with a multi-well potential whose wells correspond to the four colours. The steady-state solutions of this PDE are "approximate colourings," and the question is whether a proper colouring (an exact steady state) always exists. This connects to the theory of phase-field models and interface dynamics.

### Specific Technical Bridge

The most concrete bridge is through **spectral methods**. The eigenfunctions of the graph Laplacian provide a Fourier-like basis for functions on the graph. A proper $k$-colouring, viewed as a function $c: V \to \{e_1, \ldots, e_k\} \subset \mathbb{R}^k$ (where $e_i$ are standard basis vectors), can be expanded in this basis. The constraint that $c$ is a proper colouring translates to conditions on the Fourier coefficients — specifically, the coefficient of each eigenfunction must be such that adjacent vertices are mapped to different basis vectors.

For planar graphs, the spectrum of $L$ has specific structure (e.g., the multiplicity of eigenvalues is bounded, and the eigenfunctions have bounded support in a certain sense). SciML tools — specifically, neural operators trained on graph Laplacian spectra — could learn the mapping from spectral data to colourability, potentially identifying spectral certificates for 4-colourability.

### Feasibility

**Highly Speculative.** SciML is designed for continuous physical systems, and graph colouring is fundamentally discrete and combinatorial. The continuous relaxations (heat equation, Allen-Cahn) lose the essential combinatorial structure: a smooth approximate colouring is not a proper colouring, and rounding introduces errors that cannot be controlled in general. The spectral approach is more promising but reduces to spectral graph theory, which has been studied extensively without producing a proof of the 4CT. SciML adds computational tools but not new mathematical insight.

### Concrete Research Direction

Use a neural operator (e.g., a graph-adapted DeepONet) to learn the mapping from the spectral data $(\lambda_1, \ldots, \lambda_n, \phi_1, \ldots, \phi_n)$ of a planar graph's Laplacian to a proper 4-colouring. Train on random planar graphs up to $n = 1{,}000$ vertices. If the operator generalises successfully, analyse which spectral features it relies on. If the operator consistently uses the eigengap at specific eigenvalue thresholds, this would suggest a new spectral bound on the chromatic number of planar graphs — a bound that could then be proved rigorously.

---

## 8. Fourth-Order Nonlinear Chaos Theory

### Core Ideas

Fourth-order nonlinear chaos theory studies dynamical systems governed by ODEs of the form $x^{(4)} = f(x, \dot{x}, \ddot{x}, \dddot{x})$, where $f$ is nonlinear. Such systems arise in beam mechanics (the Euler-Bernoulli equation with nonlinear restoring forces), fluid dynamics (the Kuramoto-Sivashinsky equation $u_t + u_{xxxx} + u_{xx} + u u_x = 0$), and certain control systems. The presence of the fourth derivative creates a rich dynamical landscape: the system has a 4-dimensional phase space, allowing for chaotic attractors, hyperchaos (multiple positive Lyapunov exponents), and complex bifurcation structures. Key analytical tools include Lyapunov exponent computation, Poincaré sections, bifurcation diagrams, and Melnikov analysis for homoclinic orbits.

### Connection to 4CT

The connection is not obvious but becomes interesting when one considers **Kempe chain dynamics as a dynamical system.**

Define the following discrete dynamical system on the space of 4-colourings of a planar graph $G$:

- **State space:** $\mathcal{C}(G, 4) = \{c: V \to \{1,2,3,4\} \mid c \text{ is a proper colouring}\}$.
- **Dynamics:** At each step, select a random vertex $v$ and a random pair of colours $(a, b)$; perform a Kempe chain swap on the $(a,b)$-Kempe chain containing $v$ (if $v$ has colour $a$ or $b$). This defines a Markov chain on $\mathcal{C}(G, 4)$.

This Markov chain is the **Glauber dynamics** of the Potts model at zero temperature. Its mixing properties — whether it rapidly converges to a uniform distribution over colourings — are a central question in statistical physics and combinatorics. Vigoda (2000) showed that for $k \geq 11\Delta/6$, the Glauber dynamics mixes in $O(n \log n)$ steps. For $k = 4$ and planar graphs ($\Delta$ unbounded), mixing is not guaranteed and the dynamics can exhibit **frozen configurations** (colourings from which no single Kempe swap can reach other colourings).

The question "does the Kempe chain dynamics have chaotic or regular behaviour?" is a legitimate dynamical systems question. If one embeds the discrete state space into a continuous one (e.g., by interpolating between colourings using a soft-assignment representation), the resulting continuous dynamics could exhibit chaos, periodic orbits, or convergence to fixed points.

### Specific Technical Bridge

The most concrete bridge is through the **Lyapunov exponent** of the Kempe chain Markov chain. Define a distance metric on $\mathcal{C}(G, 4)$ (e.g., Hamming distance) and compute the rate of divergence of two initially close colourings under Kempe chain dynamics. If the maximal Lyapunov exponent is positive (exponential divergence), the dynamics is chaotic, suggesting that the colouring space has a complex structure. If it is negative (convergence), the dynamics is regular, and the space of colourings has a simpler structure.

For planar graphs, the 4CT guarantees that $\mathcal{C}(G, 4) \neq \emptyset$. The ergodic properties of the Kempe chain dynamics on this non-empty set — particularly whether the dynamics is ergodic (i.e., the reconfiguration graph is connected) — are related to the question of whether all 4-colourings of a planar graph are Kempe-equivalent. This is currently an open problem.

Fourth-order systems specifically could arise if one models the dynamics of a "colouring energy" functional $E(c) = \sum_{(u,v) \in E} \phi(c(u) - c(v))$ on a continuous relaxation, where $\phi$ is a fourth-order potential. The resulting gradient flow would be a fourth-order PDE whose steady states correspond to proper colourings.

### Feasibility

**Speculative.** The dynamical systems perspective on Kempe chain reconfiguration is legitimate and understudied. However, fourth-order chaos theory specifically adds little: the dynamics of Kempe chains is naturally discrete and combinatorial, and the connection to continuous fourth-order ODEs is artificial. The Lyapunov exponent analysis of the Kempe chain Markov chain is a reasonable project but belongs more naturally to the theory of Markov chain mixing than to chaos theory.

### Concrete Research Direction

Compute the mixing time and spectral gap of the Kempe chain Markov chain on $\mathcal{C}(G, 4)$ for all planar triangulations up to $n = 15$ vertices. Classify the resulting dynamics: Is the chain always ergodic (connected reconfiguration graph)? What is the typical mixing time as a function of $n$? Does the dynamics exhibit metastability (long trapping times in certain regions of the colouring space)? If metastable states exist, do they correspond to specific graph structures (e.g., large cliques or dense subgraphs)? This analysis would inform both the theoretical question of Kempe equivalence and the practical design of colouring algorithms.

---

## 9. Optimal Transport Theory

### Core Ideas

Optimal transport (OT) theory studies the problem of moving one probability distribution to another at minimum cost. Given distributions $\mu, \nu$ on spaces $\mathcal{X}, \mathcal{Y}$ and a cost function $c: \mathcal{X} \times \mathcal{Y} \to \mathbb{R}_{\geq 0}$, the **Monge problem** seeks a transport map $T: \mathcal{X} \to \mathcal{Y}$ minimising $\int c(x, T(x)) \, d\mu(x)$ subject to $T_\# \mu = \nu$. The **Kantorovich relaxation** replaces the map with a coupling (joint distribution) $\pi \in \Pi(\mu, \nu)$, yielding the **Wasserstein distance** $W_p(\mu, \nu) = \left(\inf_{\pi \in \Pi(\mu,\nu)} \int c(x,y)^p \, d\pi(x,y)\right)^{1/p}$. Key results include Brenier's theorem (the optimal map is the gradient of a convex function for quadratic cost), the Benamou-Brenier formulation (OT as a fluid dynamics problem), and entropic regularisation leading to the Sinkhorn algorithm.

### Connection to 4CT

**The colour redistribution perspective.** A proper 4-colouring assigns to each vertex a colour; equivalently, it partitions $V$ into 4 independent sets $I_1, I_2, I_3, I_4$. Given two proper 4-colourings $c_1, c_2$, one can define a transport plan $\pi$ that maps the "colour distribution" of $c_1$ to that of $c_2$. The cost of this transport, measured in terms of the graph distance, quantifies how "different" the two colourings are.

More precisely, let $\mu_i = \frac{1}{|V|} \sum_{v: c_i(v) = k} \delta_v$ for $k = 1,\ldots,4$ be the empirical distribution of colour $k$ under colouring $c_i$. The Wasserstein distance $W_1(\mu_1^{(k)}, \mu_2^{(k)})$ between the distributions of colour $k$ in the two colourings measures the spatial rearrangement required. The total transport cost $\sum_{k=1}^4 W_1(\mu_1^{(k)}, \mu_2^{(k)})$ provides a metric on the space of colourings that is more refined than Hamming distance.

**Barycentres and interpolation.** The Wasserstein barycenter of multiple colourings provides a notion of "average colouring" that respects the graph geometry. If the barycenter of all 4-colourings of a planar graph has a specific structural property (e.g., it always corresponds to a colouring where each colour class is close to an independent set), this would provide geometric insight into why 4 colours suffice.

### Specific Technical Bridge

The most promising technical bridge uses the **Kantorovich duality**: the Wasserstein distance equals $\sup_{f: \text{Lip}(f) \leq 1} \int f \, d(\mu - \nu)$, where the supremum is over 1-Lipschitz functions. On a graph, 1-Lipschitz functions are precisely functions $f: V \to \mathbb{R}$ with $|f(u) - f(v)| \leq 1$ for all edges $(u,v)$. This connects OT to the theory of graph homomorphisms and, more specifically, to the study of **graph cuts**: a partition of $V$ into colour classes defines a multi-cut, and the OT cost of transporting between colour classes is related to the cut weight.

For planar graphs, the **max-flow min-cut theorem** (and its dual, the shortest-path structure on the dual graph) provides strong structural control on cuts. Combining OT duality with planar duality might yield new inequalities constraining the possible distributions of colours in a proper 4-colouring.

### Feasibility

**Speculative.** Optimal transport provides a beautiful metric framework for comparing colourings, but it does not obviously address the existence question (does a 4-colouring exist?). The machinery is best suited for studying the *structure* of the space of colourings assuming they exist, rather than proving existence. The Kantorovich duality / planar duality connection is intriguing but unexplored.

### Concrete Research Direction

For each planar triangulation on $n \leq 14$ vertices, enumerate all proper 4-colourings and compute the pairwise Wasserstein-1 distances (using graph shortest-path as the ground metric). Analyse the resulting distance matrix: What is the diameter of the colouring space in Wasserstein distance? Is it bounded independently of $n$? Compute the Wasserstein barycenter of all colourings and determine whether it has a combinatorial interpretation (e.g., does it always place roughly $n/4$ vertices in each colour class?). If structural regularities emerge, investigate whether they can be proved for all planar graphs using the planar separator theorem and OT duality.

---

## 10. Hypergraph Theory & Network Analysis

### Core Ideas

Hypergraph theory generalises graph theory by allowing edges (**hyperedges**) to connect arbitrary subsets of vertices, not just pairs. A hypergraph $\mathcal{H} = (V, \mathcal{E})$ where $\mathcal{E} \subseteq 2^V$ captures multi-way relationships that pairwise graphs cannot represent. Key concepts include: **hypergraph colouring** (assigning colours to vertices so that no hyperedge is monochromatic — the "rainbow" condition — or so that no hyperedge has all vertices the same colour — the "proper" condition); **hypergraph duality** (transposing the incidence matrix); **fractional chromatic number** (the LP relaxation of the chromatic number); and **Turán-type problems** for hypergraphs (extremal questions about how many hyperedges force a specific substructure).

In network analysis, hypergraphs model systems with group interactions: co-authorship networks (a paper is a hyperedge connecting all authors), chemical reactions (a reaction is a hyperedge connecting reactants and products), and higher-order neural interactions.

### Connection to 4CT

This is the most natural connection among all 10 areas, because the 4CT can be directly reformulated in hypergraph-theoretic terms:

**Reformulation 1 — The face hypergraph.** Given a planar graph $G$ embedded in the plane, define a hypergraph $\mathcal{H}_G$ on the same vertex set $V$, where each face of the embedding defines a hyperedge (the set of vertices on its boundary). A proper vertex colouring of $G$ (the 4CT) is equivalent to a colouring of $\mathcal{H}_G$ in which no hyperedge of size 2 is monochromatic (this is just the edge constraint) and in which the colouring restricted to each face boundary satisfies additional constraints from the face structure.

**Reformulation 2 — The independent set hypergraph.** The 4CT is equivalent to: the vertex set of every planar graph can be partitioned into 4 independent sets. This is a hypergraph colouring problem on the **edge hypergraph** (which is just the graph itself, viewed as a 2-uniform hypergraph) with 4 colours. More interesting is the **clique hypergraph**: define hyperedges as the maximal cliques of $G$. For a planar graph, the maximal cliques have size at most 4 (since $K_5$ is not planar). The 4CT is then equivalent to: the clique hypergraph of every planar graph has chromatic number at most 4.

**Reformulation 3 — The deficiency version.** Lovász (1966) showed that $\chi(G) \leq \lceil(n + \omega(G))/2\rceil$ where $\omega$ is the clique number. For planar graphs, $\omega \leq 4$, giving $\chi \leq \lceil(n+4)/2\rceil$ — weak, but hypergraph colouring bounds (particularly those using the **Lovász Local Lemma** for hypergraphs) can potentially improve this. The LLL states that if each vertex's "bad event" (having the same colour as a neighbour) has probability $p$ and depends on at most $d$ other events, and $ep(d+1) \leq 1$, then a proper colouring exists. For a random 4-colouring of a planar graph with maximum degree $\Delta$, $p = 1/4$ for each edge and $d \leq 2\Delta - 2$. The LLL condition $e \cdot (1/4) \cdot (2\Delta - 1) \leq 1$ gives $\Delta \leq 1 + 2/e \approx 1.74$, which is useless for general planar graphs. Sharper versions of the LLL (the Lopsided LLL, the cluster expansion) improve the bound but not to the point of proving the 4CT.

### Specific Technical Bridge

The most promising bridge is through **list colouring** and its hypergraph generalisation. Thomassen (1994) proved that every planar graph is **5-list-colourable** (every vertex has a list of 5 colours, and a proper colouring can be chosen from the lists). The 4-list-colouring version (Hadwiger's conjecture for list colouring) is false for planar graphs in general — Voigt (1993) constructed a planar graph that is not 4-list-colourable. However, the **correspondence colouring** (DP-colouring) framework of Dvořák and Postle (2018), which generalises list colouring using a "correspondence" hypergraph structure, provides new tools. In DP-colouring, each edge carries a matching between the colour lists of its endpoints, and the colouring must avoid the matched pairs. This is naturally a hypergraph colouring problem, and the DP-chromatic number $\chi_{DP}(G)$ satisfies $\chi_{DP}(G) \geq \chi_\ell(G) \geq \chi(G)$.

For planar graphs, $\chi_{DP}(G) \leq 5$ (Dvořák and Postle). A proof that $\chi_{DP}(G) \leq 4$ for planar graphs would imply the 4CT and would be a strictly stronger result. While this is unlikely to be true in full generality (it would imply 4-list-colourability, which is false), DP-colouring with restricted correspondence structures (e.g., planar correspondences) might yield the 4CT as a special case.

### Feasibility

**Promising.** Hypergraph theory is the closest of the 10 areas to the 4CT, and the connections are not speculative — they are well-established and actively studied. The DP-colouring framework, the Lovász Local Lemma approach, and the hypergraph reformulations of the 4CT all represent genuine research directions with recent progress. The main challenge is that the known hypergraph colouring tools are not quite strong enough: the LLL gives weaker bounds, and DP-colouring generalises list colouring which is already known to be harder than ordinary colouring for planar graphs.

### Concrete Research Direction

Study the **fractional chromatic number** $\chi_f(G)$ of planar graphs via the LP relaxation of the hypergraph colouring problem on the clique hypergraph. It is known that $\chi_f(G) \leq 4$ for planar graphs (this follows from the 4CT, but can it be proved independently?). A direct proof that $\chi_f(G) \leq 4$ for all planar graphs — using only the LP duality and the structural properties of planar clique hypergraphs — would be a significant step toward an algebraic proof of the 4CT. The first step is to formulate the LP dual explicitly for planar triangulations, identify the dual variables with faces of the embedding, and attempt to construct a feasible dual solution using the planarity constraints (Euler's formula, the handshaking lemma for faces).

---

## Summary Table

| # | Area | Connection Strength | Feasibility Rating | Key Bridge Object |
|---|------|--------------------|--------------------|-------------------|
| 1 | Geometric Deep Learning | Moderate | Speculative | WL hierarchy; equivariant colouring functions |
| 2 | Information Geometry | Weak | Highly Speculative | Fisher metric of Potts model near $q = 4$ |
| 3 | Topological Data Analysis | Moderate | Speculative | Persistent homology of reconfiguration spaces |
| 4 | Transformer/LLM Theory | Weak | Highly Speculative | Proof compression; circuit complexity of reducibility |
| 5 | Mean-Field Game Theory | Very Weak | Highly Speculative | Colouring as coordination game (reduces to restatement) |
| 6 | Quantum-Inspired Algorithms | Moderate | Plausible | Tensor network contraction for chromatic polynomial |
| 7 | Scientific ML (SciML) | Weak | Highly Speculative | Spectral methods on graph Laplacian |
| 8 | Fourth-Order Chaos Theory | Weak-Moderate | Speculative | Lyapunov analysis of Kempe chain dynamics |
| 9 | Optimal Transport | Weak-Moderate | Speculative | Wasserstein metric on colouring space; OT-planar duality |
| 10 | Hypergraph Theory | Strong | Promising | DP-colouring; LLL; fractional chromatic number via clique hypergraph |

### Overall Assessment

Of the 10 areas, **Hypergraph Theory** (Area 10) has by far the strongest and most natural connection to the 4CT, with active research programmes and well-defined open problems. **Quantum-Inspired Classical Algorithms** (Area 6), via tensor network methods for chromatic polynomial computation, offers a plausible computational tool that could support algebraic proof strategies. **Geometric Deep Learning** (Area 1) and **Topological Data Analysis** (Area 3) offer moderate-strength connections through the WL hierarchy and reconfiguration space topology, respectively, though both are more useful as discovery tools than as proof methods.

The remaining areas (Information Geometry, Transformer Theory, Mean-Field Games, SciML, Chaos Theory, Optimal Transport) have connections that range from tenuous to nonexistent as direct proof strategies for the 4CT. However, several offer interesting computational or conceptual frameworks for studying the *structure* of graph colourings (e.g., the Potts model connection in Information Geometry, the dynamical systems perspective in Chaos Theory, the Wasserstein metric on colourings in Optimal Transport). These are better understood as tools for generating conjectures or computational evidence than as pathways to proof.

The most actionable research programme emerging from this analysis is: **use tensor network contraction (Area 6) to compute chromatic polynomials of planar graphs efficiently, feed the results into a GDL architecture (Area 1) to identify structural patterns, and formalise any discovered patterns using the hypergraph/DP-colouring framework (Area 10).** This pipeline combines the computational strengths of Areas 1 and 6 with the mathematical rigour of Area 10.

---

*Agent 1221 — Graph Colouring Project*  
*17 February 2026*
