"""Cache the output of ``generate_triangulations`` as JSON edge lists.

Index ``i`` under key ``n`` in the cache is ``generate_triangulations(max_n)[n][i]``,
so names such as ``T_9_35`` keep their meaning.
"""

import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from triangulation_db import generate_triangulations  # noqa: E402

KNOWN_COUNTS = {4: 1, 5: 1, 6: 2, 7: 5, 8: 14, 9: 50, 10: 233, 11: 1249, 12: 7595}


def main(max_n: int = 11) -> None:
    """Generate triangulations up to ``max_n`` vertices and write the cache."""
    start = time.time()
    tris = generate_triangulations(max_n)
    out = {
        "max_n": max_n,
        "elapsed_seconds": time.time() - start,
        "known_counts_plantri": {str(k): v for k, v in KNOWN_COUNTS.items() if k <= max_n},
        "graphs": {
            str(n): [sorted([min(u, v), max(u, v)] for u, v in G.edges()) for G in gs]
            for n, gs in tris.items()
        },
    }
    for n, gs in tris.items():
        assert len(gs) == KNOWN_COUNTS[n], (n, len(gs))
    path = Path(__file__).resolve().parents[1] / "data" / f"triangulations_n4_{max_n}.json"
    path.parent.mkdir(exist_ok=True)
    path.write_text(json.dumps(out))
    print(f"wrote {path} in {out['elapsed_seconds']:.1f}s")


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 11)
