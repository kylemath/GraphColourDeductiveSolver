"""EXPLORATORY. Realisable far sides for the order-16 quadrilateral member.

A = the recorded member (T minus edge st, quad face phi = (s, x, t, y)). For every disc
triangulation B bounded by a 4-cycle (plantri -P4 m -a, chordless, m - 4 interior vertices),
and for the two diagonals (k = 0), glue B into phi in all 8 alignments and ask which pairs
(v, fan) with v a degree-5 vertex of A off phi are pure-good in the glued graph (every start
has a pure Kempe fill at v). Reports the pairs good for every far side tried.

Usage: python3 vhphi_farside.py MEMBER_JSON PLANTRI_BIN MAXINTERIOR
"""
import json
import subprocess
import sys

import vhphi_explore as E


def disc_faces(rot):
    n = len(rot)
    pos = [{w: i for i, w in enumerate(r)} for r in rot]
    seen = set()
    faces = []
    for u in range(n):
        for v in rot[u]:
            if (u, v) in seen:
                continue
            f = []
            a, b = u, v
            while (a, b) not in seen:
                seen.add((a, b))
                f.append(a)
                # next edge: at b, the neighbour after a in rotation
                i = pos[b][a]
                c = rot[b][(i + 1) % len(rot[b])]
                a, b = b, c
            faces.append(f)
    return faces


def main():
    member = json.load(open(sys.argv[1]))["member"]
    plantri = sys.argv[2]
    kmax = int(sys.argv[3])
    n = member["n"]
    faces = {tuple(f) for f in member["faces"]}
    adjT = E.adjacency(faces, n)
    rotT = E.rotation(faces, n)
    s, t = member["deleted"]
    em = E.edge_face_map(faces)
    x, y = em[(s, t)], em[(t, s)]
    quad = [s, y, t, x]  # cyclic order around the 4-face (one orientation)
    adjA = [set(a) for a in adjT]
    adjA[s].discard(t)
    adjA[t].discard(s)
    phi = set(quad)
    deg5 = [v for v in range(n) if v not in phi and len(adjA[v]) == 5]
    fans = {v: E.legal_fans(rotT, v, adjA) for v in deg5}  # chords vs A; recheck per glue

    # far sides: list of (interior count, adjacency builder)
    sides = [("diag s-t", [(0, 2)], 0), ("diag x-y", [(1, 3)], 0)]
    for m in range(5, 4 + kmax + 1):
        out = subprocess.run([plantri, "-P4", str(m), "-a"], capture_output=True, text=True).stdout
        for li, line in enumerate(out.splitlines()):
            parts = line.split()
            if len(parts) != 2:
                continue
            rot = [[ord(c) - 97 for c in r] for r in parts[1].split(",")]
            fs = disc_faces(rot)
            outer = [f for f in fs if len(f) == 4]
            if len(outer) != 1:
                continue
            o = outer[0]
            interior = [w for w in range(m) if w not in o]
            edges = {(a, b) for a in range(m) for b in rot[a] if a < b}
            sides.append((f"P4 m={m} #{li}", (o, interior, edges), len(interior)))

    good_all = None
    per_side = []
    for name, data, k in sides:
        for align in range(8):
            adj = [set(a) for a in adjA]
            if k == 0:
                (i, j), = data
                # alignments irrelevant for diagonals; do once
                if align:
                    break
                a, b = quad[i], quad[j]
                adj[a].add(b)
                adj[b].add(a)
            else:
                o, interior, edges = data
                r = align % 4
                order = o[r:] + o[:r]
                if align >= 4:
                    order = order[::-1]
                mp = {order[i]: quad[i] for i in range(4)}
                for w in interior:
                    mp[w] = len(adj)
                    adj.append(set())
                for a, b in edges:
                    A_, B_ = mp[a], mp[b]
                    if A_ in phi and B_ in phi:
                        continue  # boundary edge of Q (already in A)
                    adj[A_].add(B_)
                    adj[B_].add(A_)
            rotlike = [sorted(a) for a in adj]
            good = set()
            for v in deg5:
                R = [sorted(a) for a in adj]
                R[v] = list(rotT[v])
                gfans, _ = E.pure_good_fans(R, adj, v)
                for fi in gfans:
                    good.add((v, fi))
            per_side.append((name, align, len(good)))
            good_all = good if good_all is None else good_all & good
            print(name, "align", align, "good pairs", len(good), "still good for all", len(good_all), flush=True)
    print("PAIRS GOOD FOR EVERY FAR SIDE TRIED:", sorted(good_all))
    json.dump({"pairs_good_all": sorted(good_all), "per_side": per_side},
              open("farside-order16.json", "w"))


if __name__ == "__main__":
    main()
