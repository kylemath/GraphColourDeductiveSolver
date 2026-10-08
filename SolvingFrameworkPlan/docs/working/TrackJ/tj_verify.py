#!/usr/bin/env python3
"""Track J: independent verification of a near-rigid closed class with the TrackH pure-Python engine (read-only import)
and TrackI's primal chain count.  For each graph line (hole 0 unless given): every Kempe class that is a union of
all-DL pi-cycles with N <= 9 everywhere; the N-profile along each cycle; the chain-parity law at each step; Kempe
neighbourhoods; the role pair of the extra chain at N = 9 states and its link-free swap partner; filled states elsewhere
(G 4-colourable); simple graph facts (edges, triangles-per-edge, H3 counts).
usage: tj_verify.py FILE [hole]  (FILE lines 'name n adj;...' or a .jsonl with 'graph')"""
import sys, os, json
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'TrackH')); sys.path.insert(0, os.path.join(HERE, '..', 'TrackI'))
from th_engine import Hole
from ti_chains import nchains

ROLEP = lambda r: {'am': (r[0], r[1]), 'AB': (r[2], r[3]), 'aA': (r[0], r[2]), 'mB': (r[1], r[3]), 'aB': (r[0], r[3]), 'mA': (r[1], r[2])}


def counts(H, col, roles):
    out = {}
    for k, (p, q) in ROLEP(roles).items():
        left = {v for v in H.V if col[v] in (p, q)}; c = 0
        while left:
            s = next(iter(left)); left -= H.comp(col, s, (p, q)); c += 1
        out[k] = c
    return out


def verify(line, h=0):
    p = line.split(); rot = [list(map(int, r.split(','))) for r in p[2].split(';')]
    n = len(rot); E = sum(len(r) for r in rot) // 2
    S = [set(r) for r in rot]
    notri = sum(1 for u in range(n) for v in rot[u] if v > u and u != h and v != h and not (S[u] & S[v]))
    H = Hole(rot, h).build(); info = H.info; Ns = [nchains(H, H.col(i)) for i in range(len(H.states))]
    filled = sum(1 for r in info if r['kind'] == 'F')
    oncyc = set(); cycs = H.allDL_cycles()
    for c in cycs: oncyc.update(c)
    res = dict(name=p[0], n=n, edges=E, edges_not_in_triangle=notri, states=len(H.states), filled_states=filled, cycles=[len(c) for c in cycs])
    found = []
    for root in set(H.cls):
        mem = [i for i in range(len(H.states)) if H.cls[i] == root]
        if not all(i in oncyc and Ns[i] <= 9 for i in mem): continue
        rep = dict(size=len(mem), filled=sum(info[i]['kind'] == 'F' for i in mem), N=Counter(Ns[i] for i in mem))
        law = Counter(); nb = Counter(); extra = Counter(); zp = Counter(); h3 = Counter()
        for i in mem:
            r = info[i]; t = r['pi']
            law[((Ns[t] - Ns[i]) % 2 == (1 if info[t]['kind'] == 'DL' else 0))] += 1
            col = H.col(i); cn = counts(H, col, r['roles'])
            tg = {m[4] for m in H.moves[i] if m[4] != i}; nb[(Ns[i], len(tg))] += 1
            # H3 counts
            al, mu, A, B = r['roles']; P = [0, 0, 0]
            for u in H.V:
                for w in H.adj[u]:
                    if w > u:
                        s = {col[u], col[w]}
                        P[0 if s in ({al, mu}, {A, B}) else (1 if s in ({al, A}, {mu, B}) else 2)] += 1
            h3[(P[0] == P[1] + 1 == P[2] + 1)] += 1
            if Ns[i] == 9:
                ex = [k for k, v in cn.items() if v > {'am': 1, 'AB': 1, 'aA': 2, 'mB': 1, 'aB': 2, 'mA': 1}[k]]
                extra[tuple(ex)] += 1
                for m in H.moves[i]:
                    if not m[2] and m[4] != i:
                        zp[(Ns[m[4]], info[m[4]]['kind'], m[4] in mem)] += 1
        rep.update(law_ok=dict(law), N_and_Kdeg=dict((str(k), v) for k, v in nb.items()), extra_pair_at_N9=dict((str(k), v) for k, v in extra.items()),
                   linkfree_move_targets=dict((str(k), v) for k, v in zp.items()), H3_ok=dict(h3),
                   cycles_in_class=[[Ns[i] for i in c] for c in cycs if c[0] in mem])
        found.append(rep)
    res['near_rigid_closed_classes'] = found
    return res


if __name__ == '__main__':
    f = sys.argv[1]; h = int(sys.argv[2]) if len(sys.argv) > 2 else 0; k = 0
    for l in open(f):
        if l.startswith('{'):
            d = json.loads(l)
            if d.get('ev') != 'example': continue
            l = d['graph']
        if len(l.split()) < 3: continue
        print(json.dumps(verify(l, h)), flush=True); k += 1
        if k >= int(os.environ.get('TJ_MAXV', '5')): break
