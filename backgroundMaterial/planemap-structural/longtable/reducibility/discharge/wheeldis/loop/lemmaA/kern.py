"""Greedy minimal D sub-configurations ("kernels") of D hits K(S).  From each hit line of res_*.txt (L s HIT ... S=..)
delete interior vertices one at a time (second-ring vertices first, then link vertices, then S, never u) while the
rest is connected, has a simple induced ring and stays D (dfast, verdicts cached in vcache.txt).  Kernels are grouped
by canonical key and described by roles: u7, w<j>:<deg>(S marks the sender set), s<j>:<deg>.
Usage: python3 kern.py RESFILE MAXRING MAXN  -> kern_<basename>.txt"""
import sys, os, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import la, inst
RES, MAXR, MAXN = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
def connected(I, adj):
    I = set(I); st = [next(iter(I))]; seen = {st[0]}
    while st:
        x = st.pop()
        for y in adj[x] & I:
            if y not in seen: seen.add(y); st.append(y)
    return seen == I
kern = collections.defaultdict(list); n = 0
for line in open(RES):
    f = line.split()
    if f[2] != 'HIT': continue
    r = int(f[3][2:])
    if r > MAXR: continue
    n += 1
    if n > MAXN: break
    L = tuple(map(int, f[0])); s = tuple(map(int, f[1])); S = tuple(int(c) for c in f[5][2:])
    adj, deg, w, sv, known = la.build(L, s)
    I = {0} | {w[j] for j in S}
    for j in S:
        for y in adj[w[j]]:
            if deg.get(y, 9) <= 8: I.add(y)
    role = {0: 'u7'}
    for j in range(7): role[w[j]] = 'w%d:%d%s' % (j, deg[w[j]], 'S' if j in S else '')
    for j in range(7): role.setdefault(sv[j], 's%d:%d' % (j, deg[sv[j]]))
    order = sorted(I - {0}, key=lambda x: (0 if role.get(x, 'x').startswith('s') else 1 if 'S' not in role.get(x, '') else 2, x))
    changed = True
    while changed:
        changed = False
        for x in order:
            if x not in I: continue
            J = I - {x}
            if not connected(J, adj): continue
            cb = la.extract_cfg(adj, J)
            if cb is None: continue
            kb = la.ckey(cb) or ('h' + la.hashlib.sha1(cb.encode()).hexdigest()[:16])
            if inst.dverd(kb, cb, int(cb.split()[0])) == 'D': I = J; changed = True
    cb = la.extract_cfg(adj, I); kb = la.ckey(cb)
    kern[kb].append((' '.join(sorted(role.get(x, '?') for x in I)), cb.split()[0], f[0], f[1]))
with open(os.path.join(la.HERE, 'kern_%s' % os.path.basename(RES)), 'w') as fo:
    for kb, v in sorted(kern.items(), key=lambda x: -len(x[1])):
        fo.write('%s ring=%s n=%d roles=[%s] e.g. %s %s\n' % (kb, v[0][1], len(v), v[0][0], v[0][2], v[0][3]))
print('hits', min(n, MAXN), 'kernels', len(kern))
