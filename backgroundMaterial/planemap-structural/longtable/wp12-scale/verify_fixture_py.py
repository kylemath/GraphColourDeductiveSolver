"""Independent pure-Python recheck of the engine's state counts and hard-state count at one root.

Uses mass_core.deletion_colourings (state set), wp11_cert.components / wp11_cert.swap (moves) and
wp11_cert.features (p). For every p = 1 state it searches the complete 1- and 2-move endpoint list
for a p = 0 endpoint (early exit). A state with none is "hard" and gets the full rank test for the
listed weights via wp11_cert.endpoints / features. Usage: verify_fixture_py.py F32|F42 [root].
"""
import json
import sys
import time
from multiprocessing import Pool
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mass_core import deletion_colourings  # noqa: E402
from wp11_cert import components, endpoints, features, swap  # noqa: E402

G = {}


def init(rot, r):
    G["adj"] = {v: [w for w in rot[v] if w != r] for v in range(len(rot)) if v != r}
    G["B"] = list(rot[r])


def pB(col):
    return max(0, len({col[v] for v in G["B"]}) - 3)


def work(chunk):
    V, cs = chunk
    adj, B = G["adj"], G["B"]
    nt = one = hard = 0
    hard_list = []
    for c in cs:
        col = dict(zip(V, c))
        if pB(col) != 1:
            continue
        nt += 1
        found = 0
        firsts = [swap(col, pr, K) for pr, K in components(adj, col)]
        if any(pB(c1) == 0 for c1 in firsts):
            one += 1
            continue
        for c1 in firsts:
            if any(pB(swap(c1, pr, K)) == 0 for pr, K in components(adj, c1)):
                found = 1
                break
        if not found:
            hard += 1
            p, f = features(adj, B, col)
            stuck = {}
            for name in ("q", "lin"):
                stuck[name] = not any(features(adj, B, c2)[1][name] < f[name] for *_, c2 in endpoints(adj, col))
            hard_list.append({"coloring": list(c), "stuck": stuck})
    return nt, one, hard, hard_list


def main():
    name = sys.argv[1]
    fx = json.loads((HERE / "fixtures.json").read_text())["fixtures"][name]
    rot = fx["rotation"]
    r = int(sys.argv[2]) if len(sys.argv) > 2 else fx["degree_five_roots"][0]
    t = time.time()
    V, C = deletion_colourings(rot, r)
    te = time.time() - t
    chunks = [(V, C[i:i + 500]) for i in range(0, len(C), 500)]
    with Pool(12, initializer=init, initargs=(rot, r)) as pool:
        res = pool.map(work, chunks)
    out = {"fixture": name, "root": r, "coloring_orbits": len(C), "non_target": sum(x[0] for x in res),
           "one_move_target": sum(x[1] for x in res), "hard": sum(x[2] for x in res),
           "hard_states": [h for x in res for h in x[3]],
           "seconds_enumerate": te, "seconds_total_12proc": time.time() - t}
    print(json.dumps({k: v for k, v in out.items() if k != "hard_states"}))
    (HERE / f"verify-py-{name}-r{r}.json").write_text(json.dumps(out, indent=1) + "\n")


if __name__ == "__main__":
    main()
