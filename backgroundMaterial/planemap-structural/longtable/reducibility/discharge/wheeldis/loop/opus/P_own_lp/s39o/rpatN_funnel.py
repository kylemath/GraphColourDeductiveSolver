"""s39o: why rpatN3 has 2,287 patterns from 8,200 configurations (funnel over the rpatN_build rule).  usage: python3 rpatN_funnel.py KC"""
import sys, collections
import rpatN_build as B
st = collections.Counter(); owners = collections.defaultdict(set); maxdeg = collections.Counter(); first = {}
for l in open(sys.argv[1]):
    if not l.strip(): continue
    conf = B.kc(l); nm, m, E, g, tri = conf
    cs = [c for c in range(m) if 7 <= g[c] <= 17]
    maxdeg[max(g.values()) if isinstance(g, dict) else max(g)] += 1
    if not cs: st['A no vertex of degree >= 7 (no centre)'] += 1; continue
    keys = set(); ne = 0
    for c in cs:
        d = g[c]
        for phi, cons in B.embeddings_c(conf, c, d):
            ne += 1; lk, sv = B.pattern(d, phi, cons, g)
            cands = [(''.join(lk[(r - i) % d] if f else lk[(i + r) % d] for i in range(d)), ''.join(sv[(r - i - 1) % d] if f else sv[(i + r) % d] for i in range(d))) for r in range(d) for f in (0, 1)]
            keys.add((d, min(cands)))
    st['centres'] += len(cs); st['embeddings'] += ne
    if not ne: st['B has a centre but no embedding with it at u (not inside one 1.5-ball window)'] += 1; continue
    st['C has >= 1 u-centred embedding'] += 1; st['distinct (config, pattern) pairs'] += len(keys)
    for k in keys: owners[k].add(nm)
print('configurations by max degree:', dict(sorted(maxdeg.items())))
for k, v in sorted(st.items()): print('%-80s %d' % (k, v))
print('distinct patterns:', len(owners), ' shared by >= 2 configurations:', sum(len(v) > 1 for v in owners.values()),
      ' configurations sharing max:', max(len(v) for v in owners.values()))
print('patterns by number of owning configurations:', dict(sorted(collections.Counter(len(v) for v in owners.values()).items())[:10]))
