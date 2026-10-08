#!/usr/bin/env python3
"""Track U: two-engine verification of closed orbits reported by tu_eng (eval output JSONL).

Engine 1 (TrackT, read-only import): tt_lib.G5 + run_from from the state (M_{L-1}, M_0): the orbit must close with
length L, and the k(H) word is recomputed with G5.kH.
Engine 2 (independent, networkx, written from the T1 statement only): checks (i) E - M_t is a connected
figure-eight whose v-loops pair (f_{k-1} f_{k+1}) and (f_{k+2} f_{k-2}), f_k in M_t; (ii) M_{t+1} subset of
E - M_t, f_{k-2} in M_{t+1}, and M_{t+1} perfect; (iii) k(M_{t-1} u M_t) word; law = parity alternation.
usage: tu_verify.py EVAL.jsonl   (lines from `tu_eng eval`)"""
import sys, os, json
import networkx as nx
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'TrackT'))
from tt_lib import G5, run_from


def eng2(n, E, fv, Ms):
    L = len(Ms); fidx = {e: i for i, e in enumerate(fv)}; ok = True; msgs = []
    for t in range(L):
        M = set(Ms[t])
        deg = [0] * n
        for e in M:
            a, b = E[e]; deg[a] += 1; deg[b] += 1
        if any(d != 1 for d in deg): ok = False; msgs.append('t%d not perfect' % t)
        ks = [fidx[e] for e in M if e in fidx]
        if len(ks) != 1: ok = False; msgs.append('t%d v-edges %s' % (t, ks)); continue
        k = ks[0]
        Q = [e for e in range(len(E)) if e not in M]
        G = nx.MultiGraph(); G.add_nodes_from(range(n))
        for e in Q: G.add_edge(*E[e], key=e)
        if not nx.is_connected(G): ok = False; msgs.append('t%d Q disconnected' % t)
        # walk loops from v
        def walk(e0):
            x = E[e0][1] if E[e0][0] == 0 else E[e0][0]; prev = e0
            while x != 0:
                nxt = [e for e in Q if e != prev and x in E[e]]
                assert len(nxt) == 1
                prev = nxt[0]; a, b = E[prev]; x = b if a == x else a
            return prev
        if walk(fv[(k - 1) % 5]) != fv[(k + 1) % 5] or walk(fv[(k + 2) % 5]) != fv[(k - 2) % 5]:
            ok = False; msgs.append('t%d pairing not DL' % t)
        N = set(Ms[(t + 1) % L])
        if not N <= set(Q): ok = False; msgs.append('t%d M_{t+1} not in E-M_t' % t)
        if fv[(k - 2) % 5] not in N: ok = False; msgs.append('t%d f_{k-2} not in M_{t+1}' % t)
    word = []
    for t in range(L):
        H = nx.MultiGraph(); H.add_nodes_from(range(n))
        for e in set(Ms[t - 1]) | set(Ms[t]): H.add_edge(*E[e], key=e)
        word.append(nx.number_connected_components(H))
    law = all((word[t] - word[(t + 1) % L]) % 2 == 1 for t in range(L))
    t1 = law and L % 2 == 0 and (all(word[t] == 1 for t in range(0, L, 2)) or all(word[t] == 1 for t in range(1, L, 2))) \
        and set(word) == {1, 2}
    return ok, word, law, t1, msgs


def eng1(n, E, fv, Ms):
    g = G5(n, [tuple(e) for e in E], fv)
    m0 = sum(1 << e for e in Ms[0]); p0 = sum(1 << e for e in Ms[-1])
    st, closed = run_from(g, p0, m0, maxlen=1000)
    word = [g.kH(*s) for s in st]
    same = [sum(1 << e for e in M) for M in Ms] == [s[1] for s in st]
    return closed is True and len(st) == len(Ms) and same, word


def main():
    graph = None; out = []
    for l in open(sys.argv[1]):
        d = json.loads(l)
        if d['event'] == 'graph': graph = d; gi = d['gi']
        elif d['event'] == 'cycle':
            n, E, fv, Ms = graph['n'], graph['edges'], graph['fv'], d['M']
            ok1, w1 = eng1(n, E, fv, Ms)
            ok2, w2, law, t1, msgs = eng2(n, E, fv, Ms)
            w0 = list(map(int, d['word'].split()))
            r = dict(gi=gi, n=n, L=len(Ms), eng1_closed=ok1, eng2_ok=ok2, words_agree=(w0 == w1 == w2),
                     word=''.join(map(str, w2)), law=law, T1_violation=t1, msgs=msgs[:3])
            print(json.dumps(r), flush=True)


if __name__ == '__main__':
    main()
