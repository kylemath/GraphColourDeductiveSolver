#!/usr/bin/env python3
"""Track N: annealing search for Q-e.  Looks for a graph G (non-planar allowed) with a degree-5 hole h = 0 (link = induced
5-cycle 1..5) having a pi-cycle of DL states with N <= 9 inside the constraint set S_f (see tn_lib):
  f = 1 (control): + chain-parity law at every pi-step
  f = 2          : + Lemma E sphere constants Sigma chi = (2,3,3) at every cycle state  (no law)
  f = 3 (Q-e)    : + law + (2,3,3)
Options (env):
  TN_TRI=1     soft penalty 1 per edge of G - h in no triangle; an example then also needs 0 such edges
  TN_CLS=w     penalty w * (# states of the run's / cycle's Kempe class violating Lemma E); example needs 0 (class variant)
  TN_MOVES     move weights 'swap:flip:toggle:stack:unstack:exch' (default 1:2:0:1:1:6).  exch = forest exchange at a
               reference colouring c* (a random state of the current best window): delete an edge uv with colours {p,q} and
               add a {p,q}-coloured non-edge xy that reconnects the two sides (or any {p,q} non-edge if uv was on a cycle),
               so every pair graph of c* keeps its component count, N(c*) and dev(c*).  swap = delete one edge of G - h (not a
               link-cycle edge) and add one non-edge (edge count preserved); flip = sphere-style diagonal flip of an edge in
               >= 2 triangles; toggle = add or delete one edge; stack = new degree-3 vertex on a triangle of G - h;
               unstack = delete a degree-3 non-link vertex.  Min degree 3 off the link; link stays induced; n <= 52.
  TN_TLIM      seconds
  TN_CYCONLY=1 score = 25 - P_f(best all-DL cycle) only (keeps an existing cycle; for seeds that already have one)
  TN_MINDEG    minimum degree of G - h vertices counted in G (default 3)
Score = max(20 - Win_f, 25 - P_f(best all-DL cycle)) (30 at an example) + 0.01 run_0 - penalties; P_f = sum max(0,N-9) + [E] sum dev
+ [law] fails over the cycle; Win_f = same over the best window of 10 consecutive DL states on a pi-path (3 per missing state).
usage: tn_search.py F SEED WALKS STEPS OUTPREFIX SEEDFILE [SEEDFILE ...]
"""
import sys, json, random, time, hashlib, os
from tn_lib import Engine, adjof, to_line, notri, load_seeds


def main():
    f, seed, walks, steps, pref = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
    seeds = []
    for sf in sys.argv[6:]: seeds += load_seeds(sf)
    rng = random.Random(seed); eng = Engine(maxstates=60000, reff=f)
    TRI = os.environ.get('TN_TRI') == '1'; CLS = float(os.environ.get('TN_CLS', '0'))
    W = list(map(float, os.environ.get('TN_MOVES', '1:2:0:1:1:6').split(':')))
    tlim = float(os.environ.get('TN_TLIM', '1e9')); MINDEG = int(os.environ.get('TN_MINDEG', '3')); CYCONLY = os.environ.get('TN_CYCONLY') == '1'
    log = open(pref + '.jsonl', 'a'); seen = set(); nev = nex = 0; t0 = time.time()
    hist = {}

    def valid(E, n):
        adj = adjof(E, n)
        if any(len(adj[v]) < MINDEG for v in range(1, n)): return None
        return adj

    def evaluate(E, n, name):
        adj = valid(E, n)
        if adj is None: return None
        line = to_line(name, adj)
        js, tn, _ = eng.run(line)
        if tn is None: return None
        run = tn['run'][f]; cyc = tn['cyc'][f]
        base = 20 - tn['win'][f] if tn['win'][f] >= 0 else -10
        if 'bc' in tn: base = max(base, 25 - tn['bc'][f][0])
        if CYCONLY: base = (25 - tn['bc'][f][0]) if 'bc' in tn else -1000 + base
        if cyc: base = 30
        clsv = tn.get('cls%d' % f, [0, 0, 0, 0])[3]
        nt = notri(adj) if TRI else 0
        sc = base + 0.01 * tn['run'][0] - nt - CLS * clsv
        ex = bool(cyc) and nt == 0 and (CLS == 0 or clsv == 0)
        return sc, dict(js=js, tn=tn, nt=nt, clsv=clsv, line=line, ex=ex, run=run, cyc=cyc)

    def exch(E, n, refs):
        if not refs: return E, n
        c = refs[rng.randrange(len(refs))]; c = [int(x) if x != '-' else -1 for x in c]
        if len(c) != n: return E, n
        cand = [e for e in E if not (min(e) >= 1 and max(e) <= 5)]
        for _ in range(20):
            e = rng.choice(cand); u, v = tuple(e); p, q = c[u], c[v]
            P = {x for x in range(1, n) if c[x] in (p, q)}
            adj = {}
            for f2 in E:
                if f2 == e: continue
                a, b = tuple(f2)
                if a in P and b in P: adj.setdefault(a, []).append(b); adj.setdefault(b, []).append(a)
            comp = {u}; st = [u]
            while st:
                x = st.pop()
                for y in adj.get(x, ()):
                    if y not in comp: comp.add(y); st.append(y)
            if v in comp: pairs = [(x, y) for x in P for y in P if x < y and c[x] != c[y]]
            else:
                compv = {v}; st = [v]
                while st:
                    x = st.pop()
                    for y in adj.get(x, ()):
                        if y not in compv: compv.add(y); st.append(y)
                pairs = [(x, y) for x in comp for y in compv if c[x] != c[y]]
            pairs = [(x, y) for (x, y) in pairs if frozenset((x, y)) != e and frozenset((x, y)) not in E and not (1 <= x <= 5 and 1 <= y <= 5)]
            if not pairs: continue
            x, y = rng.choice(pairs); E2 = set(E); E2.discard(e); E2.add(frozenset((x, y))); return E2, n
        return E, n

    def move(E, n, refs=None):
        E = set(E); k = rng.choices(range(len(W)), weights=W)[0]
        if k == 5: return exch(E, n, refs)
        adjs = {}
        for e in E:
            u, v = tuple(e); adjs.setdefault(u, set()).add(v); adjs.setdefault(v, set()).add(u)
        nonlink = lambda e: not (min(e) >= 1 and max(e) <= 5)
        if k == 0 or k == 2:
            dele = (k == 0) or rng.random() < 0.5
            if dele:
                rem = [e for e in E if nonlink(e)]
                E.discard(rng.choice(rem))
            if k == 0 or not dele:
                for _ in range(50):
                    u, v = rng.randrange(1, n), rng.randrange(1, n)
                    if u != v and nonlink((u, v)) and frozenset((u, v)) not in E: E.add(frozenset((u, v))); break
        elif k == 1:
            for _ in range(30):
                e = rng.choice(list(E)); u, v = tuple(e)
                if not nonlink(e): continue
                com = list(adjs[u] & adjs[v] - {0})
                if len(com) < 2: continue
                x, y = rng.sample(com, 2)
                if x == y or y in adjs[x] or (1 <= x <= 5 and 1 <= y <= 5): continue
                E.discard(e); E.add(frozenset((x, y))); break
        elif k == 3:
            if n >= 52: return E, n
            tris = [(a, b, c) for a in adjs for b in adjs[a] if b > a for c in adjs[a] & adjs[b] if c > b]
            if not tris: return E, n
            a, b, c = rng.choice(tris); E |= {frozenset((n, a)), frozenset((n, b)), frozenset((n, c))}; n += 1
        else:
            d3 = [v for v in range(6, n) if len(adjs.get(v, ())) == 3]
            if not d3: return E, n
            v = rng.choice(d3); E = {e for e in E if v not in e}
            # relabel n-1 -> v
            if v != n - 1:
                E = {frozenset(v if x == n - 1 else x for x in e) for e in E}
            n -= 1
        return E, n

    for w in range(walks):
        if time.time() - t0 > tlim: break
        nm, n, E = seeds[w % len(seeds)]; E = set(E)
        r = evaluate(E, n, 'seed'); nev += 1
        if r is None: continue
        cur, info = r; wbest = cur; T = 1.0
        s = -1; lastimp = 0
        while True:
            s += 1
            if s >= steps and (s - lastimp > 800 or s >= 8 * steps or wbest < 15): break
            if time.time() - t0 > tlim: break
            refs = info['tn'].get('ref')
            E2, n2 = move(E, n, refs)
            if rng.random() < 0.3: E2, n2 = move(E2, n2, refs if n2 == n else None)
            r = evaluate(E2, n2, f'n{f}_{seed}_{w}_{s}'); nev += 1
            if r is None: continue
            sc, inf2 = r
            if inf2['ex']:
                key = hashlib.md5(str(sorted(tuple(sorted(e)) for e in E2)).encode()).hexdigest()
                if key not in seen:
                    seen.add(key); nex += 1
                    log.write(json.dumps(dict(ev='example', f=f, seed=seed, walk=w, step=s, src=nm, n=n2, nedge=inf2['tn']['nedge'],
                                              tn=inf2['tn'], notri=inf2['nt'], states=inf2['js']['states'], filled=inf2['js']['filled'], graph=inf2['line'])) + '\n'); log.flush()
            if sc > wbest + 1e-9:
                wbest = sc; lastimp = s
                if inf2['run'] >= 8 or sc >= 16 or (CYCONLY and sc >= -10):
                    log.write(json.dumps(dict(ev='wbest', f=f, walk=w, step=s, src=nm, sc=round(sc, 3), n=n2, nedge=inf2['tn']['nedge'], tn=inf2['tn'],
                                              notri=inf2['nt'], clsv=inf2['clsv'], graph=inf2['line'])) + '\n'); log.flush()
            if sc >= cur or rng.random() < pow(2.718, (sc - cur) / T):
                E, n, cur, info = E2, n2, sc, inf2
            T = max(0.2, T * 0.999)
        b = int(wbest); hist[b] = hist.get(b, 0) + 1
        print(json.dumps(dict(walk=w, src=nm, n=n, best=round(wbest, 3), cur=round(cur, 3), nev=nev, nex=nex, secs=round(time.time() - t0))), flush=True)
    print('DONE', json.dumps(dict(f=f, seed=seed, nev=nev, examples=nex, best_hist=dict(sorted(hist.items())), secs=round(time.time() - t0))), flush=True)
    eng.close()


if __name__ == '__main__':
    main()
