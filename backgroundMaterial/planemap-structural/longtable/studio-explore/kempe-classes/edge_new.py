#!/usr/bin/env python3
"""[exploratory] Export every edge deletion that creates a new Kempe class (from km-N.jsonl): graph, edge, endpoint
degrees, kappa(T), kappa(T - e), and for each NEW class (hit by no restriction of a T-colouring) its size and one
representative colouring of T - e (vertex -> colour; the two ends of e always share a colour in such a class).
usage: edge_new.py ORDERS... > edge-new-classes.jsonl"""
import json, os, subprocess, sys
H = os.path.dirname(os.path.abspath(__file__))
for n in [int(x) for x in sys.argv[1:]]:
    for l in open(os.path.join(H, "km-%d.jsonl" % n)):
        r = json.loads(l)
        for e in r["edges"]:
            if not e.get("new_classes"):
                continue
            rot = [[ord(c) - 97 for c in x] for x in e["graph"].split()[1].split(",")]
            E = sorted({tuple(sorted((v, w))) for v, nb in enumerate(rot) for w in nb})
            p = "/tmp/edge_new.edges"
            open(p, "w").write("%d %d\n" % (len(rot), len(E)) + "".join("%d %d\n" % x for x in E))
            o = subprocess.run([os.path.join(H, "kmap"), p, "e", str(e["e"][0]), str(e["e"][1])], capture_output=True, text=True,
                               env={**os.environ, "KMAP_REPS": "1"}).stdout.strip().splitlines()
            m, reps = json.loads(o[0]), json.loads(o[1])["reps"]
            new = [x for x in reps if not x["hit_by_T"]]
            assert len(new) == m["new_classes"]
            assert all(x["colouring"][str(e["e"][0])] == x["colouring"][str(e["e"][1])] for x in new)
            print(json.dumps({"order": n, "plantri_index": r["index"], "plantri_ascii": e["graph"], "edge": e["e"],
                              "endpoint_degrees": e["degs"], "edge_orbit_size": e["orbit_size"], "kappa_T": m["kT"],
                              "kappa_T_minus_e": m["kH"], "new_classes": [{"size": x["class_size"], "colouring": x["colouring"]} for x in new]}))
