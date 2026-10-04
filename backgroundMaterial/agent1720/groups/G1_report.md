# G1 — State-reducibility (Baldridge–McCarty)

**Group:** G1
**Date:** 2 October 2026
**Source:** Scott Baldridge and Ben McCarty, “A new way to prove configuration reducibility using gauge theory”, arXiv:2412.18558v1. File: `KempePaper/arXiv-2412.18558v1/A-new-way-to-prove-configuration-reducibility-using-gauge-theory.tex`.

## 1. Definitions

None of these are implemented under `compute/`. They are the definitions in the paper. The Birkhoff check is the three Mathematica notebooks in `KempePaper/arXiv-2412.18558v1/anc/`.

**Reducer.** Let $\Gamma$ be a plane graph of a bridgeless trivalent connected planar graph, and let $C$ be a configuration in $\Gamma$. A replacement $C'$ producing a connected trivalent plane graph $\Gamma'$ with fewer vertices plus edges is a reducer of $\Gamma$. A trivalent planar reducer is Type $C$; a vertex is Type $D$. The paper’s Birkhoff reducer is the Type $C$ reducer in Figure BirkhoffTypeCTypeD (tex lines 296–329).

**State graph and enhanced state.** For $\alpha \in \{0,1\}^{|E|}$, the state graph $\Gamma_\alpha$ is the ribbon graph obtained by putting a half-twist on each edge with $\alpha_i = 1$. An enhanced state is a pair $(\Gamma_\alpha, c)$ with $c$ a proper $n$-face colouring of $\Gamma_\alpha$ (tex lines 315–327).

**State-extendible** (tex lines 331–333). An enhanced state $(\Gamma'_\alpha, c')$ of a reducer, with $c'$ an $(n-1)$-face colouring of $\Gamma'_\alpha$, is state-extendible if there exists an enhanced state $(\Gamma_\beta, c)$ of the original graph such that $c$ is an $n$-face colouring of $\Gamma_\beta$ and the two states agree outside the configurations. In the case $n = 4$ used for the theorem: a $3$-face colouring of a state of the reducer extends to a $4$-face colouring of some state of the original. The paper states that this extension does not, in general, correspond to a Kempe switch, and that no Kempe switch is used (tex lines 335–336 and 344: the notion is the analogue of direct extendibility).

**State-reducible** (tex lines 340–342). Let $C'$ be a reducer for a configuration $C$ of $\Gamma$. Suppose the set of enhanced states $(\Gamma'_\alpha, c')$ carrying $3$-face colourings of the reducer is nonempty. If every such enhanced state is state-extendible to a $4$-face colouring of some state graph of $\Gamma$, then $C$ is state-reducible with reducer $C'$.

**Kempe-state-reducible** (tex lines 366–367). Every $3$-face colouring of a state graph of the reducer is state-extendible to a $4$-face colouring of some state graph of the original, either directly or after a succession of Kempe switches on colourings of state-graph surfaces.

The Birkhoff search is not a function in this repository. `ProofCode3-ColoringTable.nb` defines the rules `checkColor` and `checkCapMatch`, which read `BirkhoffResults.mx` and `ReducerColoredCaps.mx`.

## 2. Statements

**Theorem (State-Reducible), with quantifiers** (tex lines 347–348). For every connected plane trivalent graph $\Gamma$, if $\Gamma$ is state-reducible with reducer $\Gamma'$ and $\Gamma'$ is $4$-face-colourable, then $\Gamma$ is $4$-face-colourable.

The written argument (tex lines 377–460) is the clockwise path: a $4$-face colouring of $\Gamma'$ yields a $3$-face colouring of some state of $\Gamma'$ (their Theorem 4-to-3, citing Baldridge–McCarty, arXiv:2303.12010, Theorems F.3, D.1, D.2, and Tait’s factor of $4$), state-reducibility extends that colouring to a $4$-face colouring of some state of $\Gamma$, and a $4$-face colouring of a state implies a $4$-face colouring of $\Gamma$ (their Theorem 4-face-to-4-face, citing Theorems F.2, D.1, and D.2 of the same preprint).

**Birkhoff claim** (Theorem Main, tex lines 356–362). The Birkhoff diamond is state-reducible with the Type $C$ reducer drawn there. Together with the theorem above, the authors call this a new proof that the diamond is reducible in Birkhoff’s sense. The computational content is Proposition 3-face-to-4-face-Birkhoff (tex lines 635–637): for every planar cap $P \in \mathcal{P}_6$ and every relative state of the reducer, every $3$-face colouring of the capped reducer state extends to a $4$-face colouring of the same cap on some relative state of the diamond, changing at most two non-interacting arcs to the fourth colour.

The paper says this half is a supercomputer computation (tex line 364: “Theorem Main is based upon computations on a supercomputer”). The acknowledgements (tex lines 724–726) separate two layers: the three ancillary notebooks are a rewritten form that “run on a reasonably fast laptop in under one hour,” while the first iterations, and the search that found this reducer, used a supercomputer. One testing run used seven nodes, $300$ CPU cores, and about four terabytes of memory, almost continuously for five days. The code that searches the $2^{21}$ relative states of the diamond is not in the ancillary folder; `BirkhoffResults.mx` stores the colourings that were found (tex lines 717–721).

**Conjecture (Kempe-state-reducible)** (tex lines 368–372). At least one of the following is Kempe-state-reducible: a single pentagon, a single hexagon, two adjacent pentagons, or three pairwise-adjacent pentagons. What the paper says each would do to the Robertson–Sanders–Seymour–Thomas unavoidable set of $633$ configurations:

- Three pairwise-adjacent pentagons: $148$ of the $633$ could be replaced by this one configuration, because it occurs as a subconfiguration. The paper calls that an almost $25$ percent reduction ($148/633 \approx 23.4\%$). It would also open Franklin’s unavoidable set of six nontrivial configurations (Franklin, Amer. J. Math. 44 (1922), 225–236). The paper does not give the resulting cardinality.
- A hexagon, or two adjacent pentagons: the set “would shrink even more drastically.” No integer is stated. The citation is Wernicke, Math. Ann. 58 (1904), 413–428.
- A single pentagon: this would finish Kempe’s argument. Kempe’s unavoidable set is a bigon, a triangle, a quadrilateral, or a pentagon, and the first three are trivially reducible, so the list of $633$ would no longer be the obstacle. The paper says the $3$-face colourings of states of possible reducers “can be enumerated by hand, in fact, in a very short list,” and that the bigraded theory and the spectral sequence of arXiv:2303.12010 would be needed. It says the gluing tools for that project are future research.

## 3. Evidence

**Citation.** Baldridge and McCarty, arXiv:2412.18558v1, abstract and tex lines 296–372, 635–649, and 717–726. The abstract states that state-reducibility does not involve Kempe switches, that the Birkhoff diamond is proved reducible by filtered $3$- and $4$-colour homology, and that a non-computer proof is a conjecture. Robertson, Sanders, Seymour, and Thomas, J. Combin. Theory Ser. B 70 (1997), 2–44, is the cited source of the unavoidable set of $633$. Birkhoff, Amer. J. Math. 35 (1913), 114–128, is the classical reducibility of the diamond. The $4$-to-$3$ and $4$-to-$4$ arrows are cited to Baldridge–McCarty, arXiv:2303.12010, not reproved here.

**Counts stated in the paper for the Birkhoff check** (tex lines 641–643 and 714). From $130$ basic caps the first notebook produces $34{,}179$ planar caps. Inserting the $2^6 = 64$ relative states of the reducer yields $3{,}744$ caps that support a $3$-face colouring and $7{,}210$ coloured caps, after fixing two arcs red and blue. For each coloured cap the third notebook exhibits a $4$-face colouring on one of the $2^{21} = 2{,}097{,}152$ relative states of the diamond.

**What is on disk.** `anc/README.rtf` lists `BirkhoffResults.mx`, `PlanarSixCaps.mx`, `ReducerColoredCaps.mx`, and the three notebooks, and says the notebooks evaluate on Mathematica 13 and 14. The same eight files are members of `KempePaper/arXiv-2412.18558v1.tar.gz`. Extracted sizes: `ProofCode1-6CapGenerator.nb` $1{,}033{,}287$ bytes, `ProofCode2-ColoredCapsOnReducer.nb` $186{,}728$ bytes, `ProofCode3-ColoringTable.nb` $479{,}801$ bytes, `PlanarSixCaps.mx` $2{,}212{,}406$ bytes, `ReducerColoredCaps.mx` $310{,}191$ bytes, `BirkhoffResults.mx` $54{,}125$ bytes. Each `.mx` file begins with the bytes `(*This is a Wolfram Language binary dump`. `ProofCode3` imports `BirkhoffResults.mx` and `ReducerColoredCaps.mx` and applies `checkColor` and `checkCapMatch`. README says the notebook that generated `BirkhoffResults.mx` is not provided.

**Command.** `command -v wolframscript math Mathematica` finds none, and `/Applications/Mathematica*.app` is absent. No notebook was evaluated. Wall clock of that check: under one second. There is no output file of a colouring table.

## 4. Result

**Literature citation, verification blocked.** The theorem, the Birkhoff claim, and the conjecture are what the preprint states. This group did not rerun the colouring check and did not re-prove the appeals to arXiv:2303.12010. Classical reducibility of the Birkhoff diamond remains the 1913 theorem; this paper’s state-reducibility proof of that fact is the unchecked computer half.

The route is not a reformulation that this group can relabel as the Four Colour Theorem. State-reducibility is an implication. The Four Colour Theorem would follow only after every member of an unavoidable set had been shown state-reducible, or after the pentagon conjecture and Kempe’s set had both been proved.

## 5. Kill criterion

For state-reducibility of a named configuration: one $3$-face colouring of a state of its reducer that extends to no $4$-face colouring of any state of the original. Not met. No such colouring was searched for here.

For the pentagon conjecture as a proof of the Four Colour Theorem: a proof that some pentagon reducer has a $3$-face colouring of a state which fails to extend even after Kempe switches on state surfaces, or a completed hand proof. Neither was produced. The conjecture is not killed.

## 6. Not proved

The Four Colour Theorem is not proved. The paper’s own fallback is to run the same analysis on the remaining $632$ unavoidable configurations. That is still a computer check, and the authors say it needs a more powerful supercomputer and a faster program (tex lines 364 and 648).

The pentagon, hexagon, double-pentagon, and triple-pentagon conjectures are not proved. The logical arrows inside Theorem State-Reducible are not proved in this repository; they are citations of arXiv:2303.12010.

The packaged verification cannot be rerun here. The obstruction is the absence of Mathematica, not a missing dump: `anc/` contains the three notebooks and all three `.mx` files, and the tarball contains the same eight paths. What is absent is the notebook that produced `BirkhoffResults.mx`. With Mathematica 13 or 14, `ProofCode3` can check the stored colourings. It cannot regenerate the search.

## 7. Feasibility

**Low** for a non-computer proof of the Four Colour Theorem by way of the pentagon conjecture.

The only configuration the paper carries through is the Birkhoff diamond, and that half is the supercomputer computation above: $34{,}179$ caps and $7{,}210$ coloured caps, with the exhibiting search omitted from the ancillary code. A pentagon that is Kempe-state-reducible would be the whole theorem, because it restores Kempe’s unavoidable set, not a lemma that leaves a short unavoidable list already checked by hand. Heawood’s objection still stands for ordinary reducibility: some pentagon colourings have no Kempe switch (the paper cites Appel–Haken, who cite Bernhart and Heesch, and ultimately Birkhoff). The new conjecture puts those switches on state-graph surfaces and, in the authors’ words, needs the spectral sequence and gluing theorems, which they postpone. The sentence that the $3$-colourings form a short list describes the input. It does not exhibit the extension.

## 8. Next steps

Do not open a work order whose goal is a hand proof of the Four Colour Theorem from this conjecture.

If Mathematica 13 or 14 is installed later, run only `ProofCode3-ColoringTable.nb` against the three dumps already in `anc/`, and record whether `Position[FPResults //. checkColor, 0]` is empty and whether `checkCapMatch` accepts every row. Do not treat a successful rerun as progress on the other $632$ configurations.

Leave `docs/navigator/` unchanged.
