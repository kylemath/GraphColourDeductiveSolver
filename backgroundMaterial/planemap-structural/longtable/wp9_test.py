"""WP9: local determinacy of the mass-macro good-root property (see WP9-local-determinacy-declaration.md).

Discovery stage only: orders 12-18.  Reads the published outcomes; computes rooted-ball codes
from the rotations.  Facts only; no status claims.
"""
import argparse
import hashlib
import json
from collections import defaultdict, deque

from mass_core import FIXTURES, HERE, parse_ascii


def ball(rot, r, k):
    dist = {r: 0}
    q = deque([r])
    while q:
        v = q.popleft()
        if dist[v] == k:
            continue
        for w in rot[v]:
            if w not in dist:
                dist[w] = dist[v] + 1
                q.append(w)
    return set(dist)


def code_from(rot, S, r, w0, sign):
    label, order, parent = {r: 0}, [r], {r: None}
    q = deque([r])
    rec = []
    while q:
        v = q.popleft()
        ns = rot[v]
        d = len(ns)
        start = ns.index(w0) if v == r else (ns.index(parent[v]) + sign) % d
        seq = [ns[(start + sign * i) % d] for i in range(d)]
        seq = [w for w in seq if w in S]
        out = []
        for w in seq:
            if w not in label:
                label[w] = len(label)
                parent[w] = v
                order.append(w)
                q.append(w)
            out.append(label[w])
        rec.append((len(rot[v]), tuple(out)))
    return tuple(rec)


def ball_code(rot, r, k):
    S = ball(rot, r, k)
    return min(code_from(rot, S, r, w0, s) for w0 in rot[r] for s in (1, -1))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--orders", default="12-18")
    args = ap.parse_args()
    lo, hi = map(int, args.orders.split("-"))
    table = json.loads((FIXTURES / "mass-macro-results.json").read_text())
    roots = []
    for o in table["orders"]:
        if not lo <= o["order"] <= hi:
            continue
        for g in o["graphs_checked"]:
            rot = parse_ascii(g["ascii"])
            for rr in g["roots"]:
                roots.append((o["order"], g["graph_index"], rr["root"], rr["outcome"] == "passes", rot))
    out = {"scope": f"WP9 local-determinacy test on orders {lo}-{hi}; finite evidence, no status claims.",
           "orders": f"{lo}-{hi}", "roots": len(roots), "failing_roots": sum(not x[3] for x in roots), "radii": {}}
    for k in (1, 2, 3):
        classes = defaultdict(list)
        for order, gi, r, good, rot in roots:
            classes[ball_code(rot, r, k)].append((order, gi, r, good))
        mixed = [v for v in classes.values() if len({x[3] for x in v}) == 2]
        fail_info = []
        for v in classes.values():
            for x in v:
                if not x[3]:
                    fail_info.append({"root": x[:3], "class_size": len(v),
                                      "passing_roots_sharing_code": sum(y[3] for y in v)})
        out["radii"][k] = {
            "distinct_codes": len(classes), "mixed_codes": len(mixed),
            "LD_survives": not mixed,
            "mixed_examples": [[list(map(lambda y: list(y[:3]) + [y[3]], v))[:6]] for v in mixed[:3]],
            "failing_roots": fail_info,
            "failing_roots_sharing_code_with_another_root": sum(f["class_size"] > 1 for f in fail_info)}
        r_ = out["radii"][k]
        print(f"k={k}: codes {r_['distinct_codes']}, mixed {r_['mixed_codes']}, LD {'survives' if r_['LD_survives'] else 'KILLED'}; "
              f"failing roots sharing a code with another root: {r_['failing_roots_sharing_code_with_another_root']}/{len(fail_info)}")
        if mixed:
            v = mixed[0]
            print("   first mixed class:", [(y[0], y[1], y[2], 'pass' if y[3] else 'FAIL') for y in v][:8])
    out["checkers"] = {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                       for p in (HERE / "wp9_test.py", HERE / "WP9-local-determinacy-declaration.md")}
    out["inputs"] = {"mass-macro-results.json": hashlib.sha256((FIXTURES / "mass-macro-results.json").read_bytes()).hexdigest()}
    (HERE / f"wp9-orders-{lo}-{hi}.json").write_text(json.dumps(out, indent=1) + "\n")


if __name__ == "__main__":
    main()
