#!/usr/bin/env python3
"""[exploratory] Decisive test of NightThetaAttempt.md section 6 (two-curve meander case).
usage: s6.py ORDER  -> writes out-ORDER.json (summary) and prints it.
Ground truth (DL, R+3, DD) comes from the vertex engine (common/kempe_py.py, Space); the Tait/meander data is
computed independently from the dual cubic graph and compared with the truth."""
import sys, os, json
from collections import defaultdict
H = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(H, "..", "common"))
from kempe_py import Space, gentri_rotation, adj_from_rot

GEN = os.path.join(H, "..", "..", "..", "studiointel", "gentri")


class Dual:
    """Dual cubic graph of T - v with five stubs."""
    def __init__(s, rot, v):
        s.rot = rot; s.v = v; s.link = list(rot[v]); n = len(rot)
        nxt = lambda w, u: rot[w][(rot[w].index(u) + 1) % len(rot[w])]
        s.face_of = {}
        faces = {}
        for u in range(n):
            for w in rot[u]:
                z = nxt(w, u)
                assert nxt(z, w) == u and nxt(u, z) == w
                tri = (u, w, z); k = min(tri[i:] + tri[:i] for i in range(3))
                s.face_of[(u, w)] = k; faces[k] = 1
        s.faces = [f for f in faces if v not in f]
        s.fedges = {}          # face -> cyclic list of 3 undirected edges (frozenset)
        for f in s.faces:
            s.fedges[f] = [frozenset((f[i], f[(i + 1) % 3])) for i in range(3)]
        s.stubface = {}        # link edge index i (x_i x_{i+1}) -> face
        for i in range(5):
            a, b = s.link[i], s.link[(i + 1) % 5]
            for d in ((a, b), (b, a)):
                if v not in s.face_of[d]: s.stubface[i] = s.face_of[d]
        s.stubedge = {i: frozenset((s.link[i], s.link[(i + 1) % 5])) for i in range(5)}
        s.edge2stub = {e: i for i, e in s.stubedge.items()}
        s.edge_faces = defaultdict(list)
        for f in s.faces:
            for e in s.fedges[f]: s.edge_faces[e].append(f)

    def other_face(s, e, f):
        L = s.edge_faces[e]
        if len(L) == 1: return None   # stub
        return L[0] if L[1] == f else L[1]

    def trace(s, start_stub, cols, tc):
        """alternating chain from stub; returns (edges, faces, end_stub). tc: edge->tait colour."""
        e = s.stubedge[start_stub]; f = s.stubface[start_stub]
        edges = [e]; faces = []
        while True:
            faces.append(f)
            want = cols[0] if tc[e] == cols[1] else cols[1]
            nxt = [x for x in s.fedges[f] if x != e and tc[x] == want]
            assert len(nxt) == 1, "not a chain"
            e = nxt[0]; edges.append(e)
            g = s.other_face(e, f)
            if g is None: return edges, faces, s.edge2stub[e]
            f = g

    def comps(s, cols, tc):
        """component id of each face in the (cols)-subgraph."""
        cid = {}; n = 0
        for f in s.faces:
            if f in cid: continue
            cid[f] = n; st = [f]
            while st:
                g = st.pop()
                for e in s.fedges[g]:
                    if tc[e] in cols:
                        h = s.other_face(e, g)
                        if h is not None and h not in cid: cid[h] = n; st.append(h)
            n += 1
        return cid

    def side(s, f, ein, eout):
        E = s.fedges[f]; i, j = E.index(ein), E.index(eout)
        return 1 if (j - i) % 3 == 1 else -1   # third edge is on the side given by cyclic orientation


def link_info(col, linki):
    c = [col[i] for i in linki]
    if len(set(c)) != 4: return None
    for j in range(5):
        if c[j] == c[(j + 2) % 5]: break
    else: return None
    return j, c[j], c[(j + 1) % 5], c[(j + 3) % 5], c[(j + 4) % 5]   # j, alpha, mu, A, B


def run_hole(rot, v, stats):
    adj = adj_from_rot(rot)
    sp = Space(adj, hole=v, link=rot[v])
    D = Dual(rot, v)
    idx, linki = sp.idx, sp.linki
    lk = sp.link

    def comp_has(col, cm, p, q, x, y):
        K = sp.flood(1 << idx[x], cm[p] | cm[q]); return bool(K >> idx[y] & 1)

    def cm_of(col):
        cm = [0, 0, 0, 0]
        for i, x in enumerate(col): cm[x] |= 1 << i
        return cm

    def dl(col):
        li = link_info(col, linki)
        if li is None: return None
        j, al, mu, A, B = li; cm = cm_of(col)
        m, a, b = lk[(j + 1) % 5], lk[(j + 3) % 5], lk[(j + 4) % 5]
        return j, comp_has(col, cm, mu, A, m, a) and comp_has(col, cm, mu, B, m, b)

    recs = []
    for s in sp.states:
        r = dl(s)
        if r is None or not r[1]: continue
        j = r[0]; _, al, mu, A, B = link_info(s, linki); cm = cm_of(s)
        x = lambda t: lk[(j + t) % 5]
        K = sp.flood(1 << idx[x(2)], cm[al] | cm[A])
        assert not (K >> idx[x(0)] & 1), "R+3 undefined on DL state"
        s2 = list(s)
        for i in range(sp.N):
            if K >> i & 1: s2[i] = A if s[i] == al else al
        r2 = dl(tuple(s2))
        assert r2 is not None and r2[0] == (j + 3) % 5
        DD = bool(r2[1])
        # --- Tait picture.  Z2^2 labels alpha=0, mu=p=1, A=q=2, B=r=3.
        lab = {al: 0, mu: 1, A: 2, B: 3}; p, q, rr = 1, 2, 3
        tc = {}
        for f in D.faces:
            for e in D.fedges[f]:
                u, w = tuple(e); tc[e] = lab[s[idx[u]]] ^ lab[s[idx[w]]]
        lab2 = lab
        tc2 = {}
        for f in D.faces:
            for e in D.fedges[f]:
                u, w = tuple(e); tc2[e] = lab[s2[idx[u]]] ^ lab[s2[idx[w]]]
        # B1: (p,r)-path from stub e_{j+1}
        Be, Bf, Bend = D.trace((j + 1) % 5, (p, rr), tc)
        assert Bend == (j + 3) % 5, ("B1 end", Bend)
        Ce, Cf, Cend = D.trace((j + 2) % 5, (q, rr), tc)
        assert Cend == (j + 4) % 5, ("C end", Cend)
        # prediction (a): swap B1 only
        tcB = dict(tc)
        for e in Be: tcB[e] = p if tc[e] == rr else rr
        # r-edges of B1 in order, with orientation
        redges = [(k, Be[k]) for k in range(1, len(Be) - 1) if tc[Be[k]] == rr]   # Be[k] joins Bf[k-1] -> Bf[k]
        assert all(tc[Be[0]] == p and tc[Be[-1]] == p for _ in [0])
        def pred(tcx):
            e_, f_, en = D.trace((j + 2) % 5, (q, rr), tcx)
            return en == (j + 3) % 5
        predB = pred(tcB); predK = pred(tc2)
        # chain ids of (q,r)-components
        cid = D.comps((q, rr), tc)
        Cid = cid[Cf[0]]
        extra = len({cid[Bf[k]] for k, e in redges} - {Cid})
        k = len(redges)
        Bset = set(Be)
        bdry = {e for f in D.faces for e in D.fedges[f] if len(e) == 2 and (lambda u, w: bool(K >> idx[u] & 1) != bool(K >> idx[w] & 1))(*tuple(e))}
        pure = bdry <= Bset
        assert Bset - {D.stubedge[(j+1)%5], D.stubedge[(j+3)%5]} >= set() 
        twocurve = (extra == 0)
        key = None
        if twocurve:
            pos = {}
            Cpos = {e: t for t, e in enumerate(Ce)}
            order = [];
            for t, (kk, e) in enumerate(redges):
                assert e in Cpos
                pos[e] = (t, Cpos[e])
            # C visit order and direction: C edge index t_C ; direction of C across the edge: from Cf[t_C-1] -> Cf[t_C]
            visits = sorted(range(k), key=lambda t: pos[redges[t][1]][0 + 1])
            seq = []
            for t in visits:
                kk, e = redges[t]; tcpos = Cpos[e]
                y, z = Bf[kk - 1], Bf[kk]
                cy, cz = Cf[tcpos - 1], Cf[tcpos]
                seq.append((t, 1 if (cy, cz) == (y, z) else -1))
            sides = []
            for t, (kk, e) in enumerate(redges):
                # at y: face Bf[kk-1], incoming Be[kk-1], outgoing Be[kk] ; at z: face Bf[kk], in Be[kk], out Be[kk+1]
                sides.append((D.side(Bf[kk - 1], Be[kk - 1], Be[kk]), D.side(Bf[kk], Be[kk], Be[kk + 1])))
            key = json.dumps([k, seq, sides])
        recs.append((DD, predB, predK, extra, k, key, pure))
    return len(sp.states), recs


def main():
    n = int(sys.argv[1])
    lines = open(os.path.join(GEN, "tri%d.txt" % n)).read().split("\n")
    lines = [l for l in lines if l.strip()]
    tot = defaultdict(int); tot.update(dict(graphs=len(lines), holes=0, DLstates=0, DD=0, nonDD=0, predB_mismatch=0, predK_mismatch=0, predB_mismatch_twocurve=0, predB_mismatch_by_extra=defaultdict(int),
               twocurve_DD=0, twocurve_nonDD=0, extra_hist_DD=defaultdict(int), extra_hist_nonDD=defaultdict(int)))
    keys = defaultdict(lambda: [0, 0]); pkeys = defaultdict(lambda: [0, 0]); per_graph = []
    for gl in lines:
        rot = gentri_rotation(gl)
        for v in range(len(rot)):
            if len(rot[v]) != 5: continue
            tot["holes"] += 1
            ns, recs = run_hole(rot, v, tot)
            for DD, pB, pK, extra, k, key, pure in recs:
                tot['pure_total'] += 1 if pure else 0
                if pure and key is not None: tot['pure_twocurve_DD' if DD else 'pure_twocurve_nonDD'] += 1; pkeys[key][0 if DD else 1] += 1
                if pure and pB != DD: tot['pure_predB_mismatch'] += 1
                tot["DLstates"] += 1
                if DD: tot["DD"] += 1; tot["extra_hist_DD"][extra] += 1
                else: tot["nonDD"] += 1; tot["extra_hist_nonDD"][extra] += 1
                if pB != DD:
                    tot["predB_mismatch"] += 1; tot["predB_mismatch_by_extra"][extra] += 1
                    if key is not None: tot["predB_mismatch_twocurve"] += 1
                if pK != DD: tot["predK_mismatch"] += 1
                if key is not None:
                    tot["twocurve_DD" if DD else "twocurve_nonDD"] += 1
                    keys[key][0 if DD else 1] += 1
    tot["predB_mismatch_by_extra"] = dict(sorted(tot["predB_mismatch_by_extra"].items()))
    tot["extra_hist_DD"] = dict(sorted(tot["extra_hist_DD"].items()))
    tot["extra_hist_nonDD"] = dict(sorted(tot["extra_hist_nonDD"].items()))
    tot["distinct_keys"] = len(keys)
    tot["keys_DD_only"] = sum(1 for a, b in keys.values() if a and not b)
    tot["keys_nonDD_only"] = sum(1 for a, b in keys.values() if b and not a)
    tot["keys_mixed"] = sum(1 for a, b in keys.values() if a and b)
    tot["pure_distinct_keys"] = len(pkeys); tot["pure_keys_mixed"] = sum(1 for a, b in pkeys.values() if a and b)
    tot["pure_keys_DD_only"] = sum(1 for a, b in pkeys.values() if a and not b); tot["pure_keys_nonDD_only"] = sum(1 for a, b in pkeys.values() if b and not a)
    tot["keys_mixed_examples"] = [[k, v] for k, v in keys.items() if v[0] and v[1]][:5]
    json.dump({"summary": tot, "keys": {k: v for k, v in keys.items()}, "pure_keys": dict(pkeys)}, open(os.path.join(H, "out-%d.json" % n), "w"))
    print(json.dumps({k: v for k, v in tot.items()}, indent=1))


main()
