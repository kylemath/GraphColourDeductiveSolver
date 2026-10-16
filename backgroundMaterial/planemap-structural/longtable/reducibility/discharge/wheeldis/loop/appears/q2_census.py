"""Q2 (census): every frame-class triangulation (plantri -m5 -c4 + frame filter; no separating triangle), every u of
degree 7..9, every S (|S| >= 2) of its degree-5 neighbours: classify the ring of the B-fixed set u + S + N(S).
Usage: q2_census.py OUT FILE [FILE ...]"""
import sys, collections, itertools, json, time
from ringlib import *
OUT = sys.argv[1]; FILES = sys.argv[2:]
tally = collections.Counter(); ex = {}; t0 = time.time(); ng = 0; nu = 0; gsep = collections.Counter()
for fn in FILES:
    for line in open(fn):
        f = line.split()
        if len(f) < 3: continue
        name = f[0]; rot = [list(map(int, x.split(','))) for x in f[2].split(';')]
        adj, nxt = sphere(rot); deg = {v: len(r) for v, r in enumerate(rot)}; ng += 1
        assert sum(len(nxt[v]) for v in nxt) == 2 * sum(deg.values()) // 2
        seps = None
        for u in range(len(rot)):
            if not 7 <= deg[u] <= 9: continue
            lk = rotf(nxt, u); snd = [i for i in range(len(lk)) if deg[lk[i]] == 5]
            if len(snd) >= 2: nu += 1
            for k in range(2, len(snd) + 1):
                for S in itertools.combinations(snd, k):
                    Sv = {lk[i] for i in S}; I = {u} | Sv
                    for s in Sv: I |= adj[s]
                    cl = classify(adj, nxt, I)
                    lab = cl['lab'] if cl['walks'] else 'nowalk'
                    ok = extract_cfg(adj, I) if cl['RS'] else False
                    if lab == 'simple' and ok: tally[('d%d' % deg[u], 'simple', 'simple', '-', '-', '-')] += 1; continue
                    fill = (not ok) and bool(cl['RS']) and code_fill(adj, I)
                    code = 'simple' if ok else ('fill-ok' if fill else 'NOSIMPLE')
                    w = witness(adj, I, cl)
                    if seps is None:
                        seps = short_sep_cycles(adj, nxt, list(adj), deg)
                        for c in seps: gsep[len(c)] += 1
                    near = set(I) | cl['RS']
                    sn = sum(all(x in near for x in c) for c in seps)
                    rest = set(adj) - set(I) - cl['RS']; comps = []
                    while rest:
                        st = [rest.pop()]; c = 1
                        while st:
                            x = st.pop()
                            for y in adj[x]:
                                if y in rest: rest.discard(y); st.append(y); c += 1
                        comps.append(c)
                    comps.sort(reverse=True)
                    deep = 'deep' if len(comps) >= 2 else 'shallow'
                    key = ('d%d' % deg[u], lab, code, 'w%s' % w, 'sepN1' if sn else ('sepG' if seps else 'nosep'), deep)
                    tally[key] += 1
                    if key not in ex:
                        ex[key] = dict(g=name, n=len(rot), u=u, word=''.join(str(deg[x]) for x in lk), S=S, I=len(I),
                                       RS=len(cl['RS']), walks=[[(v, deg[v]) for v, _ in wk] for wk in cl['walks']],
                                       rep=cl['rep'], chords=cl['chords'], enclosed=sorted(cl['enclosed']),
                                       double=cl['double'], comps=comps, seps=[c for c in seps if all(x in near for x in c)][:3])
    print(fn, ng, '%.0fs' % (time.time() - t0), flush=True)
with open(OUT, 'w') as fo:
    fo.write('graphs %d, (u,|five-nbrs|>=2) pairs %d, %.0fs; separating short cycles counted per graph where needed: %s\n'
             % (ng, nu, time.time() - t0, dict(gsep)))
    for k, v in sorted(tally.items()): fo.write('tally %s %d\n' % (' '.join(k), v))
    for k, v in sorted(ex.items()): fo.write('example %s %s\n' % (' '.join(k), json.dumps(v)))
