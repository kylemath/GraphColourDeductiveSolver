# Physical Energy Functionals for Kempe Chain Reconfiguration

**Paper:** *Physical Energy Functionals for Kempe Chain Reconfiguration: Spin Glasses, Magic Gems, and the Four Colour Theorem*

**Author:** Kyle Elliott Mathewson

## Abstract

We introduce eight energy functionals for the Kempe chain reconfiguration graph of planar triangulations, drawing on anti-ferromagnetic Potts models, polyhedral covariance (Magic Gems), electrostatic charge flow, and protein folding energy landscapes. By embedding the four colors at the vertices of a regular tetrahedron in $\mathbb{R}^3$, each Kempe swap becomes a 180-degree rotation in SO(3), linking the constructive Four Colour Theorem to topological quantum field theory.

Three principal findings emerge from evaluation on the first known counterexamples to BFS-optimal avoidance at $n = 9$:

1. **Local entropy** cleanly discriminates safe from unsafe reconfiguration paths
2. **Magic Gem energy trajectories** expose kinetic trap structure analogous to protein misfolding
3. **Surface tension rigidity** provides a combinatorial signature of merge-prone configurations (subsequently falsified at $n \geq 10$)

## Repository Structure

```
├── paper/                  LaTeX source for the paper
│   ├── main.tex            Main document
│   ├── sections/           Section files (01-introduction through 06-conclusion)
│   ├── figures/            Generated figures
│   ├── references.bib      Bibliography
│   ├── build.sh            Build script (pdflatex + bibtex)
│   ├── preamble.tex        Package imports and macros
│   └── coverpage.tex       Title, abstract, metadata
│
├── compute/kempe/          Python computational pipeline (reproduces all paper results)
│   ├── kempe_ops.py        Core: Kempe chain operations, swaps, coloring enumeration
│   ├── triangulation_db.py Planar triangulation generation (n ≤ 12)
│   ├── reconfiguration_graph.py  Build and analyze R(G,k)
│   ├── reduction_search.py BFS reduction from 5-coloring to 4-coloring
│   ├── physical_analogies.py     The 8 energy functionals from the paper
│   ├── generate_energy_figures.py Figure generation for the paper
│   ├── merge_analysis.py   Chain merge characterization by degree
│   ├── noncrossing_verifier.py   Theorem A (non-interleaving) verification
│   ├── fisk_homology.py    Fisk equivalence classes for 4-colorings
│   ├── all_paths_analysis.py     Exhaustive path census
│   ├── ...                 Additional analysis scripts
│   └── tests/
│       ├── test_plan2.py           31 tests covering core functionality
│       └── test_physical_analogies.py  Energy functional tests
```

## Quick Start

### Build the paper

```bash
cd paper
chmod +x build.sh
./build.sh
# Output: paper/main.pdf
```

Requires a LaTeX distribution with `pdflatex` and `bibtex`.

### Run the computational pipeline

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

cd compute/kempe
python tests/test_plan2.py          # ~4 minutes, 31 tests
python tests/test_physical_analogies.py  # Energy functional tests
```

### Reproduce the paper figures

```bash
source .venv/bin/activate
cd compute/kempe
python generate_energy_figures.py
# Figures written to paper/figures/
```

## Key Modules

| Module | Description |
|--------|-------------|
| `kempe_ops.py` | Kempe chain extraction, swaps, proper coloring enumeration |
| `triangulation_db.py` | Generate all planar triangulations up to isomorphism |
| `reconfiguration_graph.py` | Build reconfiguration graph $\mathcal{R}(G, k)$, compute BFS distances |
| `reduction_search.py` | BFS search for 5-to-4-coloring reduction paths |
| `physical_analogies.py` | All 8 energy functionals: Magic Gem, Potts, electrostatic, surface tension, entropy, ruggedness, defect interaction |
| `merge_analysis.py` | Characterize chain merges by vertex degree |
| `noncrossing_verifier.py` | Verify the non-interleaving theorem for disjoint color pairs |

## Data Types

```python
Colouring = Dict[int, int]           # vertex -> colour (1..5)
CanonicalColouring = Tuple[int, ...]  # hashable form, sorted by vertex
```

## Computational Scope

| $n$ | Triangulations | Colorings tested | Runtime (single core) |
|-----|----------------|------------------|-----------------------|
| 4-8 | 23 | ~43,000 | < 1 min |
| 9 | 50 | ~282,300 | ~4 min |
| 10 | 233 | ~2,000,000 | ~2 hrs |

## Requirements

- Python 3.8+
- NetworkX
- NumPy
- SciPy
- Matplotlib (for figure generation)

## Citation

```bibtex
@misc{mathewson2026energy,
  author       = {Mathewson, Kyle Elliott},
  title        = {Physical Energy Functionals for {Kempe} Chain
                  Reconfiguration: Spin Glasses, Magic Gems, and the
                  {Four Colour Theorem}},
  year         = {2026},
}
```

## License

MIT License. See [LICENSE](LICENSE).
