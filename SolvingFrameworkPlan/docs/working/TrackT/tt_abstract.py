#!/usr/bin/env python3
"""Track T: search for NRC-M cycles (and long NRC-M runs) in ABSTRACT graphs: one vertex v of degree 5 with an
arbitrary cyclic labelling f0..f4, all other vertices cubic, no embedding (generally non-planar).

Score of a graph = max over Hamiltonian DL-type starts of the NRC-M run length (k(H) = 1 at alternate states,
E - M_t connected DL-type at every state); a closed run counts as +1000.
Local search: degree-preserving double-edge swaps (keeping v's degree), simulated annealing.
usage: tt_abstract.py SEED N MINUTES [mode]   mode 'rand' = independent random graphs; 'anneal' = local search"""
import sys, random, time, json
from tt_lib import G5, ham_states, run_from, run_back
from tt_runs import nrcm_len


def random_graph(n, rnd):
    while True:
        stubs = [0] * 5 + [x for x in range(1, n) for _ in range(3)]
        rnd.shuffle(stubs)
        edges = [(stubs[2 * i], stubs[2 * i + 1]) for i in range(len(stubs) // 2)]
        if any(a == b for a, b in edges): continue
        if not connected(n, edges): continue
        return edges


def connected(n, edges):
    adj = [[] for _ in range(n)]
    for a, b in edges: adj[a].append(b); adj[b].append(a)
    seen = {0}; st = [0]
    while st:
        x = st.pop()
        for y in adj[x]:
            if y not in seen: seen.add(y); st.append(y)
    return len(seen) == n


def build(n, edges, rot):
    ve = [k for k, (a, b) in enumerate(edges) if 0 in (a, b)]
    fv = [ve[i] for i in rot]
    return G5(n, edges, fv)


RMODE = False


def rrun_len(word):
    """longest stretch of the word alternating exactly 1,2,1,2,... (R-run in Tait form with the law)"""
    best = 0; cur = 0; prev = None
    for x in word:
        if x in (1, 2) and (prev is None or prev + x == 3):
            cur += 1
        elif x in (1, 2):
            cur = 1
        else:
            cur = 0
        prev = x if x in (1, 2) else None
        best = max(best, cur)
    return best


LMODE = False


def lawrun_len(word):
    """longest stretch of consecutive states with k(H) parity alternating (Tait form of the chain-parity law)
    and containing at least one Hamiltonian state (k = 1); stretches without a 1 score half"""
    best = 0; i = 0; L = len(word)
    while i < L:
        j = i
        while j + 1 < L and (word[j + 1] - word[j]) % 2 == 1: j += 1
        seg = word[i:j + 1]; sc = len(seg) if 1 in seg else len(seg) // 2
        best = max(best, sc); i = j + 1
    return best


def score(g, maxham=20000):
    hs = ham_states(g, limit=maxham)
    best = (0, None); seen = set(); closed_any = []
    for P, M in hs:
        if (P, M) in seen or g.dl_info(P, M) is None: continue
        fw, closed = run_from(g, P, M, maxlen=200)
        if not closed and g.dl_info(*fw[-1]) is None: fw = fw[:-1]
        bw = run_back(g, P, M, maxlen=200)
        states = list(reversed(bw))[:-1] + fw
        for s in states: seen.add(s)
        word = [g.kH(*s) for s in states]
        if closed is True:
            w = [g.kH(*s) for s in fw]
            closed_any.append(''.join(str(min(x, 9)) for x in w))
            L = len(w)
            law = all((w[i] - w[(i + 1) % L]) % 2 == 1 for i in range(L))
            ok = L % 2 == 0 and (all(w[i] == 1 for i in range(0, L, 2)) or all(w[i] == 1 for i in range(1, L, 2)))
            sc = (10000 if (law and ok) else 1000 if law else 500 if ok else 100) + L
            if RMODE and not (law and ok):
                sc = min(rrun_len(w + w), L)
            if LMODE:
                sc = (20000 + L if 1 in w else 10000 + L) if law else min(lawrun_len(w + w), L)
        else:
            sc = lawrun_len(word) if LMODE else rrun_len(word) if RMODE else nrcm_len(word)
        if sc > best[0]: best = (sc, ''.join(str(min(x, 9)) for x in word))
    return best, closed_any


def main():
    seed, n, minutes = int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3])
    mode = sys.argv[4] if len(sys.argv) > 4 else 'rand'
    global RMODE
    RMODE = len(sys.argv) > 5 and sys.argv[5] == 'R'
    global LMODE
    LMODE = len(sys.argv) > 5 and sys.argv[5] == 'L'
    rnd = random.Random(seed); t0 = time.time(); cnt = 0; rec = 0
    if len(sys.argv) > 6 and sys.argv[6] == 'jseed':     # seed = best record of an earlier tt_abstract log
        best = None
        for l in open(sys.argv[7]):
            d = json.loads(l)
            if d['event'] == 'record' and (best is None or d['sc'] > best['sc']): best = d
        n = best['n']; edges = [tuple(e) for e in best['edges']]; rot = list(best['rot'])
    elif len(sys.argv) > 6:          # seed graph: GRAPHFILE name:hole (Tait dual of a sphere hole)
        from tt_lib import load_graphs, tait_dual
        nm, hh = sys.argv[7].rsplit(':', 1)
        g0 = tait_dual(load_graphs(sys.argv[6], {nm})[nm], int(hh))
        n = g0.n; edges = list(g0.E)
        ve = [k for k, (a, b) in enumerate(edges) if 0 in (a, b)]
        rot = [ve.index(e) for e in g0.fv]
    else:
        edges = random_graph(n, rnd); rot = list(range(5)); rnd.shuffle(rot)
    cur = score(build(n, edges, rot))[0][0]; T = 1.0
    while time.time() - t0 < minutes * 60:
        if mode == 'rand':
            e2 = random_graph(n, rnd); r2 = list(range(5)); rnd.shuffle(r2)
        else:
            e2 = list(edges); r2 = list(rot)
            if rnd.random() < 0.1:
                rnd.shuffle(r2)
            else:
                for _ in range(rnd.choice([1, 1, 2])):
                    i, j = rnd.sample(range(len(e2)), 2)
                    (a, b), (c, d) = e2[i], e2[j]
                    if rnd.random() < 0.5: c, d = d, c
                    e2[i], e2[j] = (a, d), (c, b)
                if any(a == b for a, b in e2) or not connected(n, e2): continue
        try:
            g = build(n, e2, r2)
        except AssertionError:
            continue
        (sc, word), closed = score(g); cnt += 1
        if closed:
            print(json.dumps(dict(event='closed', n=n, edges=e2, rot=r2, words=closed, sc=sc)), flush=True)
        if sc > rec:
            rec = sc
            print(json.dumps(dict(event='record', cnt=cnt, n=n, sc=sc, word=word, edges=e2, rot=r2,
                                  t=round(time.time() - t0))), flush=True)
        if mode != 'rand':
            if sc >= cur or rnd.random() < 2.718 ** ((sc - cur) / T):
                edges, rot, cur = e2, r2, sc
            T = max(0.3, T * 0.9995)
    print(json.dumps(dict(event='done', cnt=cnt, rec=rec)), flush=True)


if __name__ == '__main__':
    main()
