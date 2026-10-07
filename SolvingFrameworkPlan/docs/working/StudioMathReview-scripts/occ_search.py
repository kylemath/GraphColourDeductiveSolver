"""Find Occ instances of generated configurations in an oriented triangulation (faces).
Usage: python3 -I occ_search.py <faces.json> <PlaneMap module dir/> <NS> [<NS> ...]"""
import json, re, sys
J = json.load(open(sys.argv[1])); faces = J['faces'] if isinstance(J, dict) else J
P = sys.argv[2]
nxt = {}; adj = set()
for (a, b, c) in faces:
    nxt[(b, a)] = c; nxt[(c, b)] = a; nxt[(a, c)] = b
    adj |= {(a, b), (b, a), (b, c), (c, b), (a, c), (c, a)}
prv = {(u, w): v for (u, v), w in nxt.items()}
N = 1 + max(max(f) for f in faces); deg = [sum(1 for (u, v) in adj if u == x) for x in range(N)]
def parse(t): m = re.match(r'(ring|int) (\d+)', t.strip('() ')); return (m.group(1), int(m.group(2)))
for ns in sys.argv[3:]:
    occ = open(P + ns + 'Occ.lean').read().split('structure Occ')[1].split('\ntheorem')[0]
    facts = [tuple(parse(x) for x in re.findall(r'\((?:ring|int) \d+\)', l)) for l in occ.splitlines() if ': Nx T' in l]
    degs = [int(x) for x in re.search(r'!\[([\d, ]+)\]', occ.split('deg :')[1]).group(1).split(',')]
    R = 1 + max(i for f in facts for k, i in f if k == 'ring'); I = len(degs)
    found = []
    for i0 in range(N):
        for i1 in range(N):
            if (i0, i1) not in adj: continue
            asg = {('int', 0): i0, ('int', 1): i1}; ch = True
            while ch:
                ch = False
                for (x, y, z) in facts:
                    if x in asg and y in asg and z not in asg and (asg[x], asg[y]) in adj: asg[z] = nxt[(asg[x], asg[y])]; ch = True
                    if x in asg and z in asg and y not in asg and (asg[x], asg[z]) in adj: asg[y] = prv[(asg[x], asg[z])]; ch = True
            if len(asg) < R + I: continue
            if not all((asg[x], asg[y]) in adj and nxt[(asg[x], asg[y])] == asg[z] for x, y, z in facts): continue
            vals = list(asg.values())
            if len(set(vals)) == len(vals) and all(deg[asg[('int', a)]] == degs[a] for a in range(I)):
                found.append(([asg[('ring', t)] for t in range(R)], [asg[('int', a)] for a in range(I)]))
    print(ns, len(found), found[:3])
