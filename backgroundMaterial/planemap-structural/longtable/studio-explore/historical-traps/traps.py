#!/usr/bin/env python3
"""[exploratory] Run 6: the historical traps (Errera 1921, Kittell 1935, Poussin) through the standard pipeline.
Edge lists are parsed as data from Sage's smallgraphs.py (sha256 9f9b3404...cdd9); Sage code is not executed (Poussin's
construction is re-typed from its listing). For each graph: edge count, triangulation check (faces = non-separating
triangles; every edge in exactly 2 faces), min degree, separating triangles (core class = min degree 5 and none);
then at every degree-5 vertex v: kmap (kappa(T), kappa(T - v), new classes), kreach (depth to a filled state),
and Studio intel's kempe.cpp (rho, unreached DL states) on consistently oriented faces."""
import ast, itertools, json, os, subprocess
C = os.path.expanduser("~/studio-scratch/census")
src = open(os.path.expanduser("~/studio-scratch/ext/sage/smallgraphs.py")).read()


def dict_after(name, marker):
    i = src.index("def %s" % name); j = src.index(marker, i); k = j + len(marker) - 1
    depth = 0
    for t in range(k, len(src)):
        depth += {"{": 1, "}": -1}.get(src[t], 0)
        if depth == 0:
            return ast.literal_eval(src[k:t + 1])


def edges_from_dict(d):
    return {tuple(sorted((a, b))) for a, l in d.items() for b in l}


def poussin():
    E = edges_from_dict({2: [7, 8, 3, 4], 1: [7, 6], 0: [6, 5, 4], 3: [5]})
    cyc = lambda L: {tuple(sorted((L[i], L[(i + 1) % len(L)]))) for i in range(len(L))}
    path = lambda L: {tuple(sorted((L[i], L[i + 1]))) for i in range(len(L) - 1)}
    E |= cyc(list(range(3))) | cyc(list(range(3, 9))) | cyc(list(range(9, 14)))
    E |= path([8, 12, 7, 11, 6, 10, 5, 9, 3, 13, 8, 12])
    E |= {(i, 14) for i in range(9, 14)}
    return E


GRAPHS = {"Errera": edges_from_dict(dict_after("ErreraGraph", "edge_dict = {")),
          "Kittell": edges_from_dict(dict_after("KittellGraph", "g = Graph({")),
          "Poussin": poussin()}


def analyse(name, E):
    V = sorted({x for e in E for x in e}); adj = {v: set() for v in V}
    for a, b in E: adj[a].add(b); adj[b].add(a)

    def connected(rem):
        S = [v for v in V if v not in rem]; seen = {S[0]}; st = [S[0]]
        while st:
            x = st.pop()
            for y in adj[x]:
                if y not in rem and y not in seen: seen.add(y); st.append(y)
        return len(seen) == len(S)
    tri = [t for t in itertools.combinations(V, 3) if t[1] in adj[t[0]] and t[2] in adj[t[0]] and t[2] in adj[t[1]]]
    faces = [t for t in tri if connected(set(t))]; sep = [t for t in tri if not connected(set(t))]
    every2 = all(sum(1 for f in faces if a in f and b in f) == 2 for a, b in E)
    info = {"graph": name, "V": len(V), "E": len(E), "triangulation": len(E) == 3 * len(V) - 6 and every2 and len(faces) == 2 * len(V) - 4,
            "min_degree": min(len(adj[v]) for v in V), "degrees": sorted(len(adj[v]) for v in V), "separating_triangles": sep}
    info["core_class"] = info["triangulation"] and info["min_degree"] >= 5 and not sep
    if not info["triangulation"]:
        return info
    # orient faces consistently (BFS over faces, an edge must appear in opposite directions)
    of = {faces[0]: faces[0]}; todo = [faces[0]]
    while todo:
        f = of[todo.pop()]
        darts = {(f[i], f[(i + 1) % 3]) for i in range(3)}
        for g in faces:
            if g in of: continue
            for a, b in darts:
                if a in g and b in g:
                    c = [x for x in g if x not in (a, b)][0]; of[g] = (b, a, c); todo.append(g); break
    oriented = list(of.values())
    assert len({(f[i], f[(i + 1) % 3]) for f in oriented for i in range(3)}) == 2 * len(E)
    pf = "/tmp/trap_%s.tri" % name; pe = "/tmp/trap_%s.edges" % name
    open(pf, "w").write("%d %d\n" % (len(V), len(oriented)) + "".join("%d %d %d\n" % f for f in oriented))
    open(pe, "w").write("%d %d\n" % (len(V), len(E)) + "".join("%d %d\n" % e for e in sorted(E)))
    info["holes"] = []
    for v in V:
        if len(adj[v]) != 5: continue
        km = json.loads(subprocess.run([os.path.join(C, "kmap"), pe, "v", str(v)], capture_output=True, text=True).stdout.splitlines()[0])
        kr = json.loads(subprocess.run([os.path.join(C, "kreach"), pe, str(v)], capture_output=True, text=True).stdout)
        ke = json.loads(subprocess.run([os.path.join(C, "kempe"), pf, str(v)], capture_output=True, text=True).stdout)
        info["holes"].append({"v": v, "link_degrees": sorted(len(adj[w]) for w in adj[v]), "kappa_T": km["kT"], "kappa_T_minus_v": km["kH"],
                              "new_classes": km["new_classes"], "targetless": kr["targetless_classes"], "depth": kr["depth"],
                              "rho": ke.get("rho"), "unreached_DL": ke.get("unreached_DL")})
    info["faces_ccw"] = oriented
    return info


if __name__ == "__main__":
    for name, E in GRAPHS.items():
        r = analyse(name, E)
        json.dump(r, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "%s.json" % name), "w"))
        h = r.get("holes", [])
        print(json.dumps({k: r[k] for k in ("graph", "V", "E", "triangulation", "min_degree", "core_class")},),
              "sep", len(r["separating_triangles"]), "deg5 holes", len(h),
              "kappa_T", sorted({x["kappa_T"] for x in h}), "kappa_T-v", dict(__import__("collections").Counter(x["kappa_T_minus_v"] for x in h)),
              "targetless", sum(x["targetless"] for x in h), "new", sum(x["new_classes"] for x in h),
              "rho", dict(__import__("collections").Counter(x["rho"] for x in h)), "depth", dict(__import__("collections").Counter(x["depth"] for x in h)))
