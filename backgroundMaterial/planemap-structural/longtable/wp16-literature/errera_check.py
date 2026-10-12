"""WP16 literature scout: identify order-17 corpus graphs against the Errera graph.

Read-only. Uses mass-macro-results.json and the Errera adjacency stored in
compute/kempe/a1720_k6_named.py (reconstructed there from SageMath ErreraGraph()).
Run from the repo root:  .venv/bin/python backgroundMaterial/planemap-structural/longtable/wp16-literature/errera_check.py
"""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "backgroundMaterial/planemap-structural/longtable"))
sys.path.insert(0, str(ROOT / "compute/kempe"))
import networkx as nx
from mass_core import parse_ascii, FIXTURES
from a1720_k6_named import ERRERA

Ge = nx.Graph([(a, b) for a, bs in ERRERA.items() for b in bs])
table = json.loads((FIXTURES / "mass-macro-results.json").read_text())
for o in table["orders"]:
    if o["order"] != 17:
        continue
    for g in o["graphs_checked"]:
        rot = parse_ascii(g["ascii"])
        G = nx.Graph([(v, w) for v in range(len(rot)) for w in rot[v]])
        aut = sum(1 for _ in nx.isomorphism.GraphMatcher(G, G).isomorphisms_iter())
        iso = nx.is_isomorphic(G, Ge)
        types = {r: sorted(len(rot[w]) for w in rot[r]) for r in range(len(rot)) if len(rot[r]) == 5}
        print(f"order 17 graph {g['graph_index']}: |Aut|={aut} errera={iso}")
        for r, t in types.items():
            print(f"   root {r}: neighbour degrees {t}")
        if iso:
            m = next(nx.isomorphism.GraphMatcher(G, Ge).isomorphisms_iter())
            print("   corpus->Errera vertex map:", dict(sorted(m.items())))
