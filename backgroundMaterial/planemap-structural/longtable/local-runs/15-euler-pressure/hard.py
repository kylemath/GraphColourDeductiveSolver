#!/usr/bin/env python3
"""[exploratory] Euler-slack features for the hard examples.
(a) the four radius-5 certificate states (91a307d1 hole 22, 8a23ee3e hole 23, 62661a3f hole 23, 80b930d1 hole 23; studiointel/run-C-2026-10-06/cert),
    plus every state within 3 swaps of each (exact radius of each by BFS, cap 400k states per BFS);
(b) the order-22 F-cycle graph (studiointel/fcycle/fcycle_order22.json, hole 15): ALL states of T - hole (Space enumeration).
usage: hard.py > hard.json"""
import os, sys, json, itertools
from collections import deque
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(H, "..", "common")); sys.path.insert(0, H)
from kempe_py import Space
from euler_features import features, FEATURES
SI = os.path.join(H, "..", "..", "..", "studiointel")
CERT = os.path.join(SI, "run-C-2026-10-06", "cert")
CAP = 400000


def build(faces, hole):
    adj = {}
    for a, b, c in faces:
        for x, y in ((a, b), (b, c), (a, c)): adj.setdefault(x, set()).add(y); adj.setdefault(y, set()).add(x)
    nb = {}
    for f in faces:
        if hole in f:
            o = [x for x in f if x != hole]; nb.setdefault(o[0], []).append(o[1]); nb.setdefault(o[1], []).append(o[0])
    link = [min(nb)]; prev = None
    while len(link) < len(nb):
        nxt = [y for y in nb[link[-1]] if y != prev][0] if prev is not None else nb[link[-1]][0]
        prev = link[-1]; link.append(nxt)
    assert len(link) == 5 and all(link[(i + 1) % 5] in adj[link[i]] for i in range(5)), link
    return adj, link


class Local:
    def __init__(self, faces, hole):
        adj, link = build(faces, hole)
        V = sorted(v for v in adj if v != hole); self.idx = {v: i for i, v in enumerate(V)}; self.V = V
        self.adj = [[self.idx[w] for w in sorted(adj[v]) if w != hole] for v in V]
        self.link = [self.idx[x] for x in link]; self.N = len(V)

    def canon(self, c):
        mp = {}; return tuple(mp.setdefault(x, len(mp)) for x in c)

    def filled(self, s): return len({s[i] for i in self.link}) <= 3

    def nbrs(self, s):
        out = set()
        for p, q in itertools.combinations(range(4), 2):
            seen = set()
            for st in range(self.N):
                if s[st] not in (p, q) or st in seen: continue
                comp = [st]; seen.add(st); stk = [st]
                while stk:
                    x = stk.pop()
                    for y in self.adj[x]:
                        if s[y] in (p, q) and y not in seen: seen.add(y); stk.append(y); comp.append(y)
                d = list(s)
                for x in comp: d[x] = q if s[x] == p else p
                t = self.canon(d)
                if t != s: out.add(t)
        return out

    def radius(self, s0):
        if self.filled(s0): return 0
        seen = {s0}; fr = [s0]; d = 0
        while fr:
            d += 1; nx = []
            for s in fr:
                for t in self.nbrs(s):
                    if t in seen: continue
                    if self.filled(t): return d
                    seen.add(t); nx.append(t)
            if len(seen) > CAP: return None
            fr = nx
        return -1

    def ball(self, s0, R):
        dist = {s0: 0}; fr = [s0]
        for d in range(1, R + 1):
            nx = []
            for s in fr:
                for t in self.nbrs(s):
                    if t not in dist: dist[t] = d; nx.append(t)
            fr = nx
        return dist

    def feat(self, s):
        f, fr = features(self.adj, list(s), self.link)
        return {k: f[k] for k in ["N", "min_sl", "sl_mu", "sl_alpha", "Uv", "Ue", "Urank", "Uslack", "Fv", "Fe", "Fslack", "ky_tot", "pen_tot", "ky_pen", "DL"]}


def certs():
    out = []
    for gid, hole in (("91a307d1852a1764", 22), ("8a23ee3ec7b2bb33", 23), ("62661a3f304f4caa", 23), ("80b930d1540e4ee3", 23)):
        faces = json.load(open(os.path.join(CERT, gid + ".graph.json")))["faces"]
        st = json.load(open(os.path.join(CERT, "%s.hole%d.state.json" % (gid, hole))))
        L = Local(faces, hole)
        s0 = L.canon([st[str(v)] for v in L.V])
        r0 = L.radius(s0)
        ball = L.ball(s0, 3)
        rows = []
        for s, d in sorted(ball.items(), key=lambda kv: kv[1]):
            f = L.feat(s); f["dist_from_cert"] = d; f["radius"] = L.radius(s); rows.append(f)
        out.append({"graph": gid, "hole": hole, "order": L.N + 1, "cert_radius_bfs": r0, "cert": L.feat(s0), "ball3": rows})
        print(gid, hole, "radius", r0, "ball3 size", len(rows), "all DL:", all(r["DL"] == 1 for r in rows), file=sys.stderr)
    return out


def fcycle():
    d = json.load(open(os.path.join(SI, "fcycle", "fcycle_order22.json")))
    faces = d["faces"]; hole = d["hole"]
    adj, link = build(faces, hole)
    sp = Space({v: set(w) for v, w in adj.items()}, hole, link=d["link"])
    sp.build_graph(); sp.classes(); sp.dist_to_filled()
    N = sp.N; A = [[j for j in range(N) if sp.nbm[i] >> j & 1] for i in range(N)]
    rows = []
    for k, s in enumerate(sp.states):
        f, fr = features(A, list(s), sp.linki)
        rows.append({"filled": int(sp.filled(k)), "radius": sp.dist[k], "cls": sp.cl[k], **{x: f[x] for x in ["min_sl", "sl_mu", "sl_alpha", "Uv", "Ue", "Urank", "Uslack", "Fv", "Fe", "Fslack", "ky_tot", "pen_tot", "ky_pen", "DL"]}})
    return {"graph": d["graph"], "hole": hole, "order": N + 1, "n_states": len(rows), "n_classes": sp.ncl, "rows": rows}


if __name__ == "__main__":
    json.dump({"certs": certs(), "fcycle22": fcycle()}, sys.stdout, indent=0)
