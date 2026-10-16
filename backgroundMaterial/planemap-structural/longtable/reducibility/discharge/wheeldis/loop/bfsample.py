"""Round 1 probe P1: collect B-fixed receiver-centred configs (u=7, S = subset of its 5-neighbours, |S|>=2, all links of S
at exact degree) from R_opt-free patches; write unique ones by |S| and ring size."""
import sys, os, hashlib, itertools, collections, random
W = sys.argv[1]; sys.path.insert(0, W)
sys.argv = ['defect_check2.py', '/dev/null', '/dev/null']
src = open(os.path.join(W, 'defect_check2.py')).read(); __file__ = os.path.join(W, 'defect_check2.py')
exec(src[:src.index("if __name__ == '__main__':")])
out = collections.defaultdict(dict); fives = collections.Counter()
for fn in sys.argv_files if False else os.environ['PATCHES'].split(','):
    for line in open(fn):
        sig = line.split('sig=')[1].split()[0]
        L, adj, nxt = patch(sig); deg = L.deg; outer = set(L.ring())
        for u in adj:
            if u in outer or deg.get(u) != 7: continue
            lk = rotf(nxt, u); snd = [x for x in lk if deg[x] == 5]
            # only if every vertex of the B-fixed set lies well inside the patch
            for k in range(2, len(snd) + 1):
                for S in itertools.combinations(snd, k):
                    Ib = {u} | set(S)
                    for s in S: Ib |= adj[s]
                    if any(x in outer for x in Ib): continue
                    cb = extract_cfg(adj, deg, Ib)
                    if cb is None: continue
                    kb = 'b' + hashlib.sha1(cb.encode()).hexdigest()[:16]
                    out[(len(snd), k)][kb] = cb
for (n5, k), d in sorted(out.items()):
    rs = collections.Counter(int(c.split()[0]) for c in d.values())
    print('u has %d fives, |S|=%d: %d unique, rings %s' % (n5, k, len(d), dict(sorted(rs.items()))))
    with open('bf_n%d_k%d.txt' % (n5, k), 'w') as f:
        for kb, cb in d.items(): f.write('%s %s\n' % (kb, cb))
