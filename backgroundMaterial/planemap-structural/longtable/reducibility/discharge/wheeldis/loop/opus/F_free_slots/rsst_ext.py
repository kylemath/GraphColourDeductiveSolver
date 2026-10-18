"""RSST 633 in the binder's filled patch extended by w's private neighbours (the rest of u's 2-ball).
Patch: u (7), w0..w6 = 5675765, s0..s6 = 6577575 with (s1, s4) = filling.  w_i of degree k has k-5 privates
p(i,1..k-5) on the path s_{i-1} - p(i,1) - .. - p(i,k-5) - s_i (if w_i = 5, s_{i-1} ~ s_i).  Ring 2 = the 13-cycle
of s's and privates; ring-3 vertices are only ring vertices of K (not hosts), as B's relaxed mode does for s.
Privates: letter free in {5,6,7,8} (a 9 is never interior).  Hosts: u, w, exact s (<= 8), privates.
For each hit, print the letters it puts on the privates.  Assumes generic adjacency (no chords on rings 1-2) [I]."""
import sys, os, collections
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'B_rsst_rows'))
import rsst_rows as R
d = 7; w = [int(c) for c in '5675765']; s0 = [int(c) for c in '6577575']
def target(s, plet=frozenset({5, 6, 7, 8})):
    host = {'u': {d}}; adj = collections.defaultdict(set)
    def e(a, b):
        if a in host and b in host: adj[a].add(b); adj[b].add(a)
    for i in range(d):
        host[('w', i)] = {w[i]}
        if s[i] <= 8: host[('s', i)] = {s[i]}
        for k in range(1, w[i] - 4): host[('p', i, k)] = set(plet)
    for i in range(d):
        j = (i + 1) % d
        e('u', ('w', i)); e(('w', i), ('w', j)); e(('s', i), ('w', i)); e(('s', i), ('w', j))
        chain = [('s', (i - 1) % d)] + [('p', i, k) for k in range(1, w[i] - 4)] + [('s', i)]
        for a, b in zip(chain, chain[1:]): e(a, b)
        for k in range(1, w[i] - 4): e(('w', i), ('p', i, k))
    for v in host: adj[v]
    return host, dict(adj)
FILL = [(a, b) for a in range(6, 10) for b in range(6, 10)]
mode = sys.argv[1] if len(sys.argv) > 1 else 'ext'
for a, b in FILL:
    s = list(s0); s[1], s[4] = a, b
    host, adj = target(s)
    res = []
    for i, p in enumerate(R.P):
        if len(p['deg']) > len(host): continue
        if not R.contains(host, adj, p): continue
        embs = R.allemb(host, adj, p, cap=200)
        lets = sorted({' '.join('p%d.%d=%d' % (t[1], t[2], dg) for t, dg in sorted(e.values(), key=str) if t[0] == 'p') or 'none'
                       for e in embs})
        res.append('%s(r%d,%s)[%s]' % (p['name'], p['ring'], p['kind'], '; '.join(lets[:6]) + (' ...' if len(lets) > 6 else '')))
    print('s1=%s s4=%s: %d hits %s' % (a if a < 9 else '9+', b if b < 9 else '9+', len(res), ' | '.join(res)), flush=True)
