"""EXPLORATORY. Rigidity of locked classes: in a locked class, is every chain {c(y),k} through y
equal to ALL vertices of the two colours (plus x)?  And what are the colour-class sizes?
Usage: python3 lock_rigid.py PLANTRI GRAPH_INDEX"""
import subprocess, sys
from collections import Counter
import tilley_apex as TA, vhphi_explore as E, lock_anatomy as LA

plantri, gi = sys.argv[1], int(sys.argv[2])
line = subprocess.run([plantri, "-m5", "17", "-a"], capture_output=True, text=True).stdout.splitlines()[gi]
rot = TA.parse(line); n = len(rot); adj = [set(r) for r in rot]
tally = Counter(); sizes = Counter(); total = 0; allmembers = 0; rigid_members = 0
for x in range(n):
    if len(rot[x]) != 5: continue
    legal = {f[0] for f in E.legal_fans(rot, x, adj)}
    for i, y in enumerate(rot[x]):
        if i not in legal: continue
        G = [set(a) for a in adj]; G[x].discard(y); G[y].discard(x)
        allc, comp = LA.classes(G, n)
        sep = {comp[c] for c in allc if c[x] != c[y]}
        locked = {comp[c] for c in allc if c[x] == c[y]} - sep
        for k in locked:
            total += 1
            for c in (c for c in allc if comp[c] == k):
                allmembers += 1
                full = []
                for o in set(range(4)) - {c[y]}:
                    chain = LA.chain(G, c, y, o)
                    want = {w for w in range(n) if c[w] in (c[y], o)}
                    full.append(chain == want)
                rigid_members += all(full)
                if c is not None:
                    sizes[tuple(sorted(Counter(c[w] for w in range(n) if w != x).values()))] += 1
print("graph 17:%d: locked classes %d, members %d, members with all three chains = full colour pairs: %d"
      % (gi, total, allmembers, rigid_members))
print("colour class sizes in T - x over all locked members:", dict(sizes))
