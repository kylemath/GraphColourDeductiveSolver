"""Is the charge a rule set moves along an edge a function of the two END neighbourhoods only
(hub's ring + receiver's ring), i.e. expressible as amount = TABLE[type(sender), type(receiver)]?
For each edge: key = (hub link read from the receiver, receiver's own ring: two hats and its fans).
Report how often the amount is constant within a key, per rule kind."""
import pickle, sys, collections as C
sys.path.insert(0, '../code')
from behav import npriv
rows = []
for f in ('all1.pkl', 'all2.pkl', 'all3.pkl', 'all4.pkl'): rows += pickle.load(open(f, 'rb'))
def keys(r, i):
    d, link, asg = r['d'], r['link'], r['asg']
    hub = tuple(link[(i + o) % d] for o in range(d))
    rec = (asg[100 + (i - 1) % d],) + tuple(asg[200 + 3 * i + t] for t in range(npriv(link[i]))) + (asg[100 + i],)
    return (d, hub), rec
for kind in ('dr', 'sp', 'st'):
    for name, sel in (('random balls', lambda r: r['src'] == 'random'), ('all balls', lambda r: True)):
        full = C.defaultdict(C.Counter); hubonly = C.defaultdict(C.Counter)
        for r in rows:
            if not sel(r): continue
            for i in range(r['d']):
                h, rc = keys(r, i); a = r[kind][i]
                full[(h, rc)][a] += 1; hubonly[h][a] += 1
        def stat(G):
            n = sum(sum(c.values()) for c in G.values()); bad = sum(sum(c.values()) - max(c.values()) for c in G.values())
            multi = sum(1 for c in G.values() if sum(c.values()) > 1); amb = sum(1 for c in G.values() if len(c) > 1)
            return n, bad / n, multi, amb
        n, b1, m1, a1 = stat(hubonly); _, b2, m2, a2 = stat(full)
        nz = sum(c[a] for G in (full,) for c in G.values() for a in c if a != 0)
        print('%-3s %-12s edges %6d (charged %5d) | hub ring only: unexplained %.4f, keys seen twice %5d of which ambiguous %5d | both rings: unexplained %.4f, keys seen twice %5d ambiguous %4d' % (kind, name, n, nz, b1, m1, a1, b2, m2, a2))
