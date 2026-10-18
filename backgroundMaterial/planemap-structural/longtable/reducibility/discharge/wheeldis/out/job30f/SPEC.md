# Job 30 F: Rule T option F, sender-side letters (Studio proposal, 18 Oct ~12:30Z; for Opus review before F runs)

## Built and validated already: full z letters (the mechanical part of F)
- `wlp3xt.py tfull` with `bin/sep3xt` ("TF" table) implements G_ruleT_lp option F:
  - Y[r, z_a, z_e] and T[r, z_a, z_e, side], with z the letter (5..9) of the vertex beyond a 6-spoke; T exists only for
    z ≥ 7.
  - Sender rows run over every z-letter assignment, coupled through each 6-spoke's wheel (non-R6 for some q).
  - The inflow T is keyed by the receiver's own letter.
- Counts: 3,048 Y, 2,007 T, 19,626 sender rows. Set-equal to Opus's tcount.py enumeration with the physical side
  carried (loop/studio/tc/tdiffF.py).
- Bijection: every T is receivable at its z and vice versa (TCHECK).
- Separator weights equal the Python row values to 5e-10, both on random weights and on inflow-heavy weights where all
  160 rows have inflow (TSELF).
- T = 0 with flags merged: byte-identical to sep3xf (regress.py MODE=TF). B's mode is unchanged (same counts, same
  self-checks, MODE=T identical).

## Proposal: sender-side letters (the kills that cannot be receiver windows)
**Inputs:** the 10 k42 hits that leave both the w2 and w4 frames, and RSST 2.3701166 (D). See out/job30b/RUNLOG.md:
122.126, 3.3700806, 2.3711966, 122.1031 ×2, 126.61686 ×2, 2.211701966, 2.504980 ×2, plus 2.3701166.

### 1. The five's 2-ball model (what a sender row describes)
- v = the five; its link a_0..a_4, with exact letters from the sender word. t_k = the second-ring vertex on the link
  edge (a_k, a_{k+1}): the other common neighbour of a_k and a_{k+1}.
- Private vertices of a_k: a_k has d_k − 5 privates, strictly between t_{k−1} and t_k around a_k. A 6-spoke has one
  private, the wheel's q.
- Edges, from the triangulation with no separating ≤ 4-cycle and no non-trivial separating 5-cycle (the same
  assumption as the receiver model and Opus's rsst_rows):
  - v–a_k, a_k–a_{k+1};
  - t_k–a_k and t_k–a_{k+1};
  - the privates of a_k form a path t_{k−1}, q_1, …, q_{d_k−5}, t_k, each adjacent to a_k;
  - t_{k−1}–t_k iff a_k = 5 (no privates).
  - No other edges among these vertices. All triangles among them are faces.
- **Letters 5..8 are exact degrees; 9 means ≥ 9 and never hosts an interior vertex.** A link vertex lettered 9 has an
  unknown number of privates, so its privates are not modelled (they cannot host).
- In today's option F, the only lettered second-ring vertices are the z's, i.e. t_k on the {big root, 6} edges.

### 2. Which slots get letters (principle 2: only what a kill reads)
- Run each kill configuration K through all its embeddings into the model, with every non-link slot as a wildcard
  (5..8).
- A slot is *read* if some embedding of some K maps an interior vertex to it. Only read slots are lettered, and only
  in the sender words where such an embedding exists.
- Expected read slots, from the k42 images seen from R*'s fives (w0, w3, w6), all within distance 2 of the five:
  - t_k: e.g. u's s1 is the q of w1's wheel seen from w0;
  - the 6-wheel q;
  - privates of big link vertices (e.g. p1 is w0's t on edge (w1, s0)).
- Nothing outside the five's 2-ball is lettered. A kill whose images all need distance 3 is reported and not used.

### 3. Kill rule (principle 1: a row is deleted only when every filling contains K)
- A sender row is (five word, z letters, letters on read slots, wildcards elsewhere).
- K **deletes** the row if K has an embedding (exact degrees, induced, triangles onto faces) that uses **only lettered
  vertices** with letters equal to K's degrees. Every filling of the unlettered slots then contains K, because the
  embedding and the model edges among lettered vertices do not depend on the fillings.
- A **partial match**, an embedding that also needs some unlettered read slots, **splits** the row. Those slots
  become lettered, one sub-row per letter 5..9 (the coupling filter applies to each).
  - Sub-rows where K now embeds on lettered vertices are deleted. The others stay.
  - The row itself is never deleted on a partial match.
- Induced condition: if K's embedding uses t_{k−1} and t_k, it needs a_k's letter. a_k is a link vertex, so it is
  always lettered. No unlettered vertex decides an adjacency among lettered ones.
- Variables are unchanged. Y and T stay keyed by (r, z_a, z_e[, side]): the rule class does not read the new
  letters. Only the sender-row family changes (split, then filtered). A deleted row is a five neighbourhood that
  contains a reducible configuration, so it cannot occur in a minimal counterexample.

### 4. Matcher discipline (principle 3)
- An independent networkx check builds the five's lettered 2-ball as a graph from §1. For each of the 11 configurations
  and every sender row (or sub-row), it decides "K embeds on lettered vertices" by induced subgraph isomorphism with
  degree labels and a triangle check.
- The sender-row filter (Python, in wlp3xt) must agree with it on every row: 0 mismatches. A random sample of deleted
  and kept rows is also printed for hand checking.
- The two receiver/sender consistency checks of B (TCHECK bijection, TSELF weights) are rerun with the split family.

### 5. Verdicts
- The 10 C hits are C under kc's conservative X with cfast --fixed agreeing (k42/cut_kcc.out, cut_fixedkc.cfast).
- 2.3701166 is D on dfast and kc (k42/cut_dfast.out, cut_kcc.out).
- The verdicts are on the cut configuration K itself, so the sender kill needs only K ⊂ the lettered 2-ball.

### 6. Run plan and kill line (to be copied into job30/RUNLOG.md before F runs)
- A+F: A's registry + B's 12 receiver windows + this sender filter.
- H30F: t*(A+F) < t*(A+B). Kill line: equal, with F FEASIBLE (feascheckt in tfull mode, sender rows evaluated over the
  split family).

### Open questions for Opus
- (a) Is the "no other edges among the five's 2-ball vertices" assumption right at distance 2, for a five whose link
  has two bigs? It is the receiver model's assumption mirrored. A short separating cycle through two privates is
  excluded by B2.
- (b) Is the split depth bounded? Each split letters one read slot, and an embedding uses at most |K| slots, so it is
  at most |K| per row. Expected small, since K has ≤ 8 interior vertices.
- (c) Rows whose read slot is a private of a link vertex lettered 9 cannot be split, since the private count is
  unknown. Proposal: leave them unsplit (sound, just weaker).
