"""Q2 (defect patches): classify the ring of every receiver-centred (rc, B free) and B-fixed (bf) set at every 7
of K <= 4 defect candidates.  Usage: q2_defects.py STRIDE OFFSET OUT"""
import sys, gzip, re, collections, itertools, json, time
from ringlib import *
STRIDE, OFF, OUT = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
SRC = '../../out/defect_K4_candidates_checked.txt.gz'
def ball(adj, src, r):
    d = {s: 0 for s in src}; q = collections.deque(src)
    while q:
        x = q.popleft()
        if d[x] < r:
            for y in adj[x]:
                if y not in d: d[y] = d[x] + 1; q.append(y)
    return d
tally = collections.Counter(); ex = {}; t0 = time.time(); n = 0; sepsig = 0
for li, line in enumerate(gzip.open(SRC, 'rt')):
    if li % STRIDE != OFF: continue
    m = re.search(r'sig=(\S+)', line)
    if not m: continue
    sig = m.group(1); L, adj, nxt = patch(sig); deg = L.deg; outer = set(L.ring()); n += 1
    far = ball(adj, outer, 2)
    seps = None
    for u in sorted(adj):
        if u in outer or deg[u] != 7: continue
        lk = rotf(nxt, u); d = len(lk); snd = [i for i in range(d) if deg[lk[i]] == 5]
        for k in range(2, len(snd) + 1):
            for S in itertools.combinations(snd, k):
                Sv = {lk[i] for i in S}
                Irc = {u} | Sv
                for s in Sv: Irc |= {y for y in adj[s] if deg[y] <= 6}
                Ibf = {u} | Sv
                for s in Sv: Ibf |= adj[s]
                for kind, I in (('rc', Irc), ('bf', Ibf)):
                    cl = classify(adj, nxt, I); ok = extract_cfg(adj, I)
                    if cl['lab'] == 'simple' and ok: tally[(kind, 'simple', 'simple', '-', '-')] += 1; continue
                    fill = (not ok) and code_fill(adj, I)
                    code = 'simple' if ok else ('fill-ok' if fill else 'NOSIMPLE')
                    w = witness(adj, I, cl)
                    if seps is None:
                        seps = short_sep_cycles(adj, nxt, [v for v in adj if v not in far], deg)
                        if seps: sepsig += 1
                    near = ball(adj, I, 1)
                    sn = sum(all(x in near for x in c) for c in seps)
                    key = (kind, cl['lab'], code, 'w%s' % w, 'sep' if sn else 'nosep')
                    tally[key] += 1
                    if key not in ex:
                        ex[key] = dict(sig=sig, u=u, word=''.join(str(deg[x]) for x in lk), S=S,
                                       walks=[[(v, deg[v]) for v, _ in wk] for wk in cl['walks']],
                                       rep=[(r, deg[r]) for r in cl['rep']], chords=cl['chords'],
                                       enclosed=sorted(cl['enclosed']), double=cl['double'])
with open(OUT, 'w') as f:
    f.write('candidates %d (stride %d offset %d), %.0fs; candidates with any separating <=5-cycle in patch interior: %d\n'
            % (n, STRIDE, OFF, time.time() - t0, sepsig))
    for k, v in sorted(tally.items()): f.write('tally %s %d\n' % (' '.join(k), v))
    for k, v in sorted(ex.items()): f.write('example %s %s\n' % (' '.join(k), json.dumps(v)))
print(open(OUT).read()[:3000])
