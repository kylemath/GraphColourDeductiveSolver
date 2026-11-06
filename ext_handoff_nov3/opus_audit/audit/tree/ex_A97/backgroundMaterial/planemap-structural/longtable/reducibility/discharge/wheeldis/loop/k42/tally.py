"""Round 42: survivors per filling under the conservative two-engine set (RSST 2.126 = rsst003 and 126.8168 = rsst142
are C only with a broad X on both engines, so they are left out) and under the full set.  usage: python3 tally.py"""
import os, itertools, collections
H = os.path.dirname(os.path.abspath(__file__))
G = {'__file__': os.path.join(H, 'grow.py'), '__name__': 'grow'}; exec(open(G['__file__']).read(), G)
P, pa, pf = G['structure'](); fd = G['fixed_deg'](); VAR, LET = G['VAR'], G['LET']
C = G['rsst']() + G['explore_kills']()
BROAD = {'rsst003', 'rsst142'}
def run(skip):
    pats = set()
    for c in C:
        if c[0] in skip: continue
        for e in G['embeddings'](c, P, pa, pf, fd):
            req = dict((v, c[3][u]) for u, v in e if v not in fd); key = tuple(req.get(x, 0) for x in VAR)
            if key[0] != 5 and key[1] != 5: pats.add(key)
    dead = set()
    for key in pats:
        rng = [[k] if k else ([6, 7, 8, 9] if j < 2 else LET) for j, k in enumerate(key)]
        dead.update(itertools.product(*rng))
    sv = {(a, b): [p for p in itertools.product(LET, repeat=6) if (a, b) + p not in dead] for a in (6, 7, 8, 9) for b in (6, 7, 8, 9)}
    return pats, sv
for lab, skip in (('conservative', BROAD), ('with broad', set())):
    pats, sv = run(skip)
    print('%s: %d patterns; survivors %d of 250000' % (lab, len(pats), sum(len(v) for v in sv.values())))
    print('  ' + ' '.join('%d%d:%d' % (k + (len(v),)) for k, v in sorted(sv.items())))
    if lab == 'conservative':
        with open(os.path.join(H, 'cases_cons.txt'), 'w') as o:
            o.write('# conservative two-engine survivors per filling (s1 s4); privates p1 p2a p2b p4a p4b p5\n')
            for f in sorted(sv):
                o.write('## %d%d %d\n' % (f + (len(sv[f]),)))
                for p in sv[f]: o.write(''.join(map(str, p)) + '\n')
