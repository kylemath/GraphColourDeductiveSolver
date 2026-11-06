# AUDITSPEC: when is one f2b rule justified? (W18, A-1, 6 Nov 2026)

This is the soundness condition the W18 engine (`code/engine.py`) tests for every rule of
`rules_studio_keep95p131f.json` (md5 45a4c6d1). The engine is my own code. It is independent of OP-5's
`rejust.py`, which I have not read, and of the Studio's DERIVE, whose code I read only to explain the failures.

## 1. What a rule says

A rule `(p, w_req, s_req)` in group `d{d}_w{a}`, with side sg (±1 for w7; none for w6), says the following.

Take a receiver row of degree d, with link w_0..w_{d-1} and apexes s_0..s_{d-1} (s_k sits over the edge w_k w_{k+1}).
At a link position j with w_j = a, suppose every listed letter holds:
- for every (off, allowed) in w_req, w_{j+off} is in allowed;
- for every (off, v) in s_req, s_{j+off} = v.

Then **the slot** cannot have degree p.
- For w6, the slot is A = w_j's one private.
- For w7 side +1, it is A's private adjacent to s_j.
- For w7 side -1, it is A's private adjacent to s_{j-1}.

Offsets are taken mod d. Letters are 5..9, and 9 means 9 or more.

## 2. The row's true 2-ball

The engine builds the 2-ball from the rule's pinned letters, with j = 0. It uses these vertices:
- the centre v;
- the link w_k, counter-clockwise;
- the apexes s_k;
- the privates q_{k,1..m} of w_k, where m = deg(w_k) - 5. q_{k,1} is adjacent to s_k and q_{k,m} to s_{k-1}. If w_k = 5 there are none, and s_{k-1} s_k is an edge.

It writes these as one oriented face list:
- v w_k w_{k+1};
- w_{k+1} w_k s_k;
- the fan of w_k over s_{k-1}, q_{k,m}, ..., q_{k,1}, s_k.

Every vertex's rotation (its cyclic order of neighbours) is read from the faces. For a boundary vertex (an apex or a private), the positions its exact degree adds beyond its known neighbours are unknown ring-3 vertices.

**Premise.** The receiver lies in an internally 6-connected triangulation, as everywhere in the stack. So these vertices are distinct and there are no other edges among them; a coincidence would need a separating cycle of length ≤ 5 (REVIEW item 4).

**Check.** On 300 random fully pinned rows, the adjacency and faces match Studio's grow.py `build2` (`code/geomcheck.py`: 0 mismatches).

## 3. Which vertices may be used

A vertex is *usable* only if its degree is exact:

| Vertex | Usable when |
|---|---|
| v | d = 7 or 8. At d = 9 the centre is never exact; this is "9 is never exact", and DERIVE also leaves u out at d = 9. |
| A | always: degree 6 or 7, fixed by the group |
| w_k | w_req[k] is a single letter in 5..8 |
| s_k | s_req[k] is in 5..8 |
| the slot | always, at degree p (the killed letter) |

Every other vertex is unusable:
- unpinned or multi-letter link vertices;
- unpinned apexes;
- letter 9;
- **all other privates, including A's other private (strict rule 14').**

## 4. One completion suffices

A rule fixes the induced structure on the usable vertices whenever it pins w_k each time it pins both s_{k-1} and s_k. Only that w_k decides the edge s_{k-1} s_k.

- **On the file [P]:** 0 rules pin both apexes and leave the link letter between them open (`code/smoke.py`). So 0 rules need a split into "w_k = 5" and "w_k ≠ 5". The engine would split them and require both if any did.
- **Allowed sets in the file:** single letters, and {6,7,8,9} (98 occurrences). A {6,7,8,9} vertex is non-5 and unusable.
- **Splitting it into its completions adds nothing.** The 9-completion is exactly the direct test. A mechanical re-test of all 88 rejects that have such a set confirms it: every one stays unjustified. So the class "justified only after splitting" is empty.
- **Every unpinned letter can be 9.** So the direct test is the worst completion. A rule justified directly is justified in every completion.

## 5. The test

The rule is **justified** iff some configuration K in the pool embeds into the usable vertices with the slot in its image. An embedding is a map φ from K's interior into the usable vertices with all of these properties:
- φ is injective;
- γ_K(x) = deg(φ(x)) exactly;
- one global orientation is used (a mirror image of K is allowed);
- **at every interior vertex x, K's rotation at x maps position by position onto T's rotation at φ(x).**
  - Each interior neighbour goes to its image.
  - Each ring position goes to a vertex outside φ(K): an unusable or unknown vertex, or a usable vertex not in the image.

As a result, φ(K) is induced, every interior face goes to a face, and K's free completion maps locally onto T.

K's rotations come from its free completion:
- **RSST:** the rotations in unavoidable.conf.
- **kc lines:** the ring cycle plus the ring and interior adjacency. Every interior vertex's link was checked to be an induced cycle of length γ and consistently oriented; all 13,323 configurations pass.

**Why rotation positions, not only faces.** A reading that only asks for "faces as vertex sets plus induced" is what DERIVE uses through grow.py `embeddings`. It is weaker for a configuration with a cut vertex or a pendant vertex: there it lets a block be re-placed or flipped around the cut vertex.
- The flipped placement is a different configuration with a different ring, and K's reducibility proof does not cover it.
- For a 2-connected K, both readings agree: each vertex has at most one ring gap.
- [P] On all 278 face-set embeddings behind the 274 rejects where they differ, the broken vertex is in a configuration with a cut vertex. There is no case with a 2-connected configuration.

## 6. The pool

Built by `code/pool.py`; 13,323 configurations, all parsed:

| Source | Count | Notes |
|---|---|---|
| RSST unavoidable.conf | 633 | md5 26aeba66; verdicts loop/k44: D2 249, C2cons 333, none 51 |
| k3x D A100 | 3,096 | |
| k3x C A100 | 1,311 | |
| k3x A111-only | 57 | D 29, C 28 |
| nl51 | 8,200 | md5 b9bc6e8b |
| k3p D | 4 | |
| k3p C | 6 | 5 of them are the leaked q7- entries |
| kpriv | 16 | D2 14, C2 2 |

**How the kc lines were found.** k3x kc lines are located the way Studio's f2b_rulecheck.py does it: the first kc line for the name in the sorted `loop/k[0-9]*/*` files. I cite that location rule; the parse is mine. 106 names have more than one distinct kc line, and all 106 are isomorphic (`code/kcalt.py`).

**The keep pool, which is the pool for the verdict, has 12,268 configurations.** It is the keep95p131f DERIVE forbidden set: Studio's keep95p131 set of 12,273 minus the 5 leaked k3p C. Membership:
- RSST: all D2, plus C2cons iff named in keep95p131_C.txt;
- k3x: all D A100, plus C A100 iff in k3x_C_A100_keep95p131.cfast;
- nl51: all;
- k3p: all D, plus the one non-leaked C.

No keep configuration is held out by exname_keep95p131f.

The other configurations are tried only to label a reject:
- **non-keep, non-exname:** RSST none, non-keep C2cons, A100 C outside keep, A111-only, kpriv, the leaked k3p;
- **exname-held:** 721 configurations.

## 7. Verdict classes

| Class | Meaning |
|---|---|
| J_keep | justified: an embedding through the slot from the keep pool. The witness and its embedding are recorded. **Only these are kept in the strict filtered file.** |
| J_nonkeep_only | not justified in the keep pool; justified by a non-keep, non-exname configuration (witness recorded) |
| J_exname_only | justified only by an exname-held configuration (none occur) |
| NJ | not justified in any pool I have |

**Labels for rejects.**
- **Reason**, from the Studio's DERIVE justifiers re-tested in the true 2-ball:
  - `faceset_only`: the justifier embeds only under the face-set reading;
  - `no_embedding_true_2ball`: it does not embed even under that reading.
- **Vacuous:** the pinned letters already contain a keep configuration without the slot. Such a rule is sound but not justified through the slot, and is listed separately.

## 8. What this does not check

- The reducibility of the configurations themselves. That is the stack's premise; W18b (A-2) checks the justifiers.
- That the LP applies the rules with the slot identity of section 1. REVIEW items 1-3 and 6 checked this.
