"""Find occurrences (Occ) of the generated configurations in the library icosahedron.
Usage: python3 -I ico_occ.py <Icosahedron.lean> <PlaneMap module dir/>"""
import re, sys
L = open(sys.argv[1]).read()
def table(name):
    s = L.split('def %s' % name)[1].split(':=', 1)[1].split('def ')[0]
    nums = [int(x) for x in re.findall(r'\d+', s)]
    return [nums[12*i:12*i+12] for i in range(12)]
nxt = table('nextTable'); prv = table('prevTable')
E = re.findall(r'\((\d+), ?(\d+)\)', L.split('def endpoints')[1].split('def graph')[0])
adj = {(int(a), int(b)) for a, b in E} | {(int(b), int(a)) for a, b in E}
P = sys.argv[2]
def parse(t):
    m = re.match(r'(ring|int) (\d+)', t.strip('() ')); return (m.group(1), int(m.group(2)))
for ns in ['DiamondM', 'DiamondP', 'C2122M', 'C2122P']:
    src = open(P + ns + 'Occ.lean').read()
    occ = src.split('structure Occ')[1].split('theorem')[0]
    facts = [tuple(parse(x) for x in re.findall(r'\((?:ring|int) \d+\)', l)) for l in occ.splitlines() if ': Nx T' in l]
    degs = [int(x) for x in re.search(r'deg : .*?!\[([\d, ]+)\]', occ).group(1).split(',')]
    R = 1 + max(i for f in facts for k, i in f if k == 'ring'); I = len(degs)
    found = None
    for i0 in range(12):
        for i1 in range(12):
            if (i0, i1) not in adj: continue
            asg = {('int', 0): i0, ('int', 1): i1}
            ch = True
            while ch:
                ch = False
                for (x, y, z) in facts:
                    if x in asg and y in asg and z not in asg and (asg[x], asg[y]) in adj: asg[z] = nxt[asg[x]][asg[y]]; ch = True
                    if x in asg and z in asg and y not in asg and (asg[x], asg[z]) in adj: asg[y] = prv[asg[x]][asg[z]]; ch = True
            if len(asg) < R + I: continue
            ok = all((asg[x], asg[y]) in adj and nxt[asg[x]][asg[y]] == asg[z] for x, y, z in facts)
            vals = list(asg.values())
            if ok and len(set(vals)) == len(vals) and all(d == 5 for d in degs):
                found = ([asg[('ring', t)] for t in range(R)], [asg[('int', a)] for a in range(I)]); break
        if found: break
    print(ns, 'degrees', degs, 'ring', R, '->', found)
