# W2 — A longer safe path from one colouring of \(T_{9,35}-6\)

**Date:** 27 September 2026
**Group:** W2
**Colouring:** the colouring of \(T_{9,35}\) already checked in `backgroundMaterial/agent1701/groups/W_path.md`
**Status:** one colouring, one call of `find_safe_nonoptimal_path`. This file does not treat the result as a theorem.

The graph is `generate_triangulations(9)[35]`, named `T_9_35`. Vertex \(6\) has degree \(4\) and neighbours \(0,1,2,5\). \(H = G - 6\). The colouring is

| Vertex | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|--------|---|---|---|---|---|---|---|---|---|
| Colour | 1 | 2 | 3 | 4 | 5 | 3 | 5 | 2 | 5 |

The same run found that this map is a proper \(5\)-colouring of \(G\), and that its restriction to \(H\) is a proper \(5\)-colouring of \(H\). The canonical tuple of \(c|_H\), in vertex order \(0,1,2,3,4,5,7,8\), is \((1,2,3,4,5,3,2,5)\).

---

## 1. Command and time

NumPy is imported by `compute/kempe/counterexample_energy_targeted.py` and was not present in the project virtual environment. It was installed there, and not globally: `numpy==1.26.4`.

```
/Users/fulkanjou/GraphColour/.venv/bin/python -u backgroundMaterial/agent1701/groups/w2_longer_search.py
```

The script calls `find_safe_nonoptimal_path(T, H, 6, col, col_H, opt_dist=2, max_extra=3)`. That window is distances \(3\), \(4\), and \(5\).

| Clock | Seconds |
|---|---|
| `generate_triangulations(9)` | \(1.081\) |
| `find_safe_nonoptimal_path` | \(0.001\) |
| Process wall clock | \(3.725\) |

The search returned before the ten-minute stop. It expanded `all_kempe_neighbours` \(21\) times and returned on the first safe path it classified. It did not continue through distances \(4\) and \(5\).

---

## 2. What “safe” means in this function

`find_safe_nonoptimal_path` does not implement a second predicate. It reconstructs the breadth-first parent path and accepts it when `classify_path_safety` in `compute/kempe/all_paths_analysis.py` sets `path_is_safe`.

That flag is false when some step has `is_unsafe`. For an \((a,5)\)-step, `is_unsafe` is set when at least two neighbours of \(v\) lie in distinct \((a,5)\)-chains and the Kempe chain of a swapped vertex is one of those chains. A chain of a neighbour contains that neighbour, and a Kempe step swaps the whole chain, so this is the same sentence as: the step swaps an \((a,5)\)-chain containing a neighbour of \(v\) while \(v\) bridges two \((a,5)\)-chains.

`is_step_unsafe` in `compute/kempe/verify_counterexamples.py` is the same test, including the same use of the evolving colouring of \(G\) rather than a separately stored colouring of \(H\). K1 §2 names `classify_path_safety` as the reading of that sentence. On the path below, `is_step_unsafe` and `classify_path_safety` are both false at every step, and a direct check on the colourings of \(H\) stored in the path gives the same three answers.

The search is the first parent-pointer path, in breadth-first order, to a colouring with at most four colours at distance greater than \(2\), inside the window of distances \(3\), \(4\), and \(5\). It is not a list of every walk of those lengths.

---

## 3. The path

A safe path was found. Its length is \(3\). The last colouring of \(H\) uses the four colours \(\{1,2,3,5\}\).

Each step below was replayed on \(H\): the swapped set equals the Kempe chain of that colour pair, swapping it reproduces the next colouring, and that colouring is a Kempe neighbour. Every colouring on the path is a proper colouring of \(H\).

### Step 0

| Field | Value |
|---|---|
| Colour pair | \((1,2)\) |
| Swapped vertices | \(\{0,7\}\) |
| \((a,5)\)-step | no |
| K1-unsafe | no |

Neighbour \(0\) is in the swapped set. The pair is not an \((a,5)\)-pair, so the bridge test does not apply. After the swap, \(H\) is coloured

$$
0\mapsto 2,\; 1\mapsto 2,\; 2\mapsto 3,\; 3\mapsto 4,\; 4\mapsto 5,\; 5\mapsto 3,\; 7\mapsto 1,\; 8\mapsto 5.
$$

Vertices \(0\) and \(1\) are both coloured \(2\). They are not adjacent in \(H\).

### Step 1

| Field | Value |
|---|---|
| Colour pair | \((1,5)\) |
| Swapped vertices | \(\{4\}\) |
| Neighbours of \(6\) coloured \(1\) or \(5\) | none |
| Swapped set meets \(N(6)\) | no |
| K1-unsafe | no |

Vertex \(4\) is not a neighbour of \(6\). After the swap,

$$
0\mapsto 2,\; 1\mapsto 2,\; 2\mapsto 3,\; 3\mapsto 4,\; 4\mapsto 1,\; 5\mapsto 3,\; 7\mapsto 1,\; 8\mapsto 5.
$$

### Step 2

| Field | Value |
|---|---|
| Colour pair | \((4,5)\) |
| Swapped vertices | \(\{3\}\) |
| Neighbours of \(6\) coloured \(4\) or \(5\) | none |
| Swapped set meets \(N(6)\) | no |
| K1-unsafe | no |

Vertex \(3\) is not a neighbour of \(6\). After the swap, \(H\) is coloured

$$
0\mapsto 2,\; 1\mapsto 2,\; 2\mapsto 3,\; 3\mapsto 5,\; 4\mapsto 1,\; 5\mapsto 3,\; 7\mapsto 1,\; 8\mapsto 5,
$$

which uses four colours.

This is not the shortest path whose first step is the \((3,5)\)-swap of \(\{2,8\}\). That path has length \(2\). This one has length \(3\) and its three swaps are \((1,2)\) on \(\{0,7\}\), \((1,5)\) on \(\{4\}\), and \((4,5)\) on \(\{3\}\).

---

## 4. Not proved

This is one colouring, not all \(24\), and not a theorem.

The call shows that, for this \(c\) and this \(v\), `find_safe_nonoptimal_path` returns a path of length \(3\) in \(\mathcal{R}(H,5)\) from \(c|_H\) to a \(4\)-colouring, and that path has no K1-unsafe step. It does not show the same for the other colourings of \(T_{9,35}\) at vertex \(6\). It does not show that every path of length greater than \(2\) is safe. Degree-\(4\) BFS avoidance is a statement about shortest paths; a longer safe path does not prove or refute it. Degree-\(5\) BFS avoidance, and the Four Colour Theorem, are untouched.
