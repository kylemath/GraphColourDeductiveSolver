"""Q1: ring structure of every receiver-centred (rc) and B-fixed (bf) set in a defect patch (default D1)."""
import sys, collections, itertools
from ringlib import *
sig = sys.argv[1] if len(sys.argv) > 1 else '5|55667|767666675|765757557756665|66666666666666666666'
L, adj, nxt = patch(sig); deg = L.deg; outer = set(L.ring())
def ball(src, r):
    d = {s: 0 for s in src}; q = collections.deque(src)
    while q:
        x = q.popleft()
        if d[x] < r:
            for y in adj[x]:
                if y not in d: d[y] = d[x] + 1; q.append(y)
    return d
Y = [v for v in adj if v not in outer and deg[v] != 6]
far = ball(outer, 2)
inner = [v for v in adj if v not in far]
seps = short_sep_cycles(adj, nxt, inner, deg)
print('sig', sig, '| patch vertices', len(adj), '| non-6 vertices', len(Y))
print('separating triangles / chordless 4-cycles / nontrivial chordless 5-cycles in the whole patch interior:',
      sum(len(c) == 3 for c in seps), sum(len(c) == 4 for c in seps), sum(len(c) == 5 for c in seps))
tally = collections.Counter()
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
                cl = classify(adj, nxt, I); ok = extract_cfg(adj, I); fill = (not ok) and code_fill(adj, I)
                code = 'simple' if ok else ('fill-ok' if fill else 'NOSIMPLE')
                tally[(kind, cl['lab'], code)] += 1
                if cl['lab'] != 'simple' or not ok:
                    w = witness(adj, I, cl)
                    near = ball(I, 1)
                    sn = [c for c in seps if all(x in near for x in c)]
                    print('%s u=%d (word %s) S=%s |I|=%d ring|RS|=%d walks=%s lab=%s code=%s rep=%s chords=%s enclosed=%s double=%s '
                          'witness_cycle_len=%s sep<=5_within_N1(I)=%d' % (
                        kind, u, ''.join(str(deg[x]) for x in lk), S, len(I), len(cl['RS']),
                        [len(w_) for w_ in cl['walks']], cl['lab'], code,
                        [(r, deg[r]) for r in cl['rep']], [(a, b) for a, b in cl['chords']],
                        sorted(cl['enclosed']), cl['double'], w, len(sn)))
                    if cl['lab'] == 'pinch':
                        for wk in cl['walks']:
                            print('    walk (vertex:deg):', ' '.join('%d:%d' % (v, deg[v]) for v, _ in wk))
for k, v in sorted(tally.items()): print('tally', k, v)
