# groups string from kcf family D ("g0,g1R4,...": interior j -> group label, optional rim pin)
# -> cfast --fixed X (every edge inside each merged set) and whether any group is pinned.
import sys
line, groups = open(sys.argv[1]).readline().split(), sys.argv[2]
r, m, rp, ip = int(line[1]), int(line[2]), line[3].split(';'), line[4].split(';')
toks = groups.split(','); lab = {}; pin = {}
for j, t in enumerate(toks):
    g, _, p = t.partition('R'); lab[j] = int(g)
    if p: pin[int(g)] = int(p)
key = lambda j: ('R', pin[lab[j]]) if lab[j] in pin else ('G', lab[j])
X = []
for j in range(m):
    for i in ip[j].split(','):
        if i and int(i) > j and key(j) == key(int(i)): X.append(f"I{j}-I{i}")
    if rp[j] not in ('-', ''):
        for k in rp[j].split(','):
            if key(j) == ('R', int(k)): X.append(f"R{k}-I{j}")
print("pinned" if pin else "interior-only", "|X|=%d" % len(X), ",".join(X))
