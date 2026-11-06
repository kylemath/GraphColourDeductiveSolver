import sys, json, glob
argv = sys.argv[1:]
sys.argv = ['x']
exec(open('variants.py').read().split("for a in rows:")[0])
KP = [grow.kcline(l, 'kpriv') for l in open(P + '/s49/kpriv_kc.txt').read().splitlines() if l.strip() and len(l.split()) == 5]
try: E12 = grow.explore_kills()
except Exception as e: print('explore_kills failed', e); E12 = []
ALL = C + Cx + R51 + KP + [c for c in E12 if c[0] not in have]
print('extended registry', len(ALL), 'kpriv', len(KP), 'explore', len(E12), flush=True)
def strict(D, w, s, j, sgi, CC):
    Pv, pa, pf = build(D, list(w))
    sa = ('s', j) if sgi == 1 else ('s', (j - 1) % D)
    slot = [x for x in Pv if x[0] == 'p' and x[1] == j and sa in pa[x]][0]
    fd = {('u',): D}
    for i in range(D): fd[('w', i)] = w[i] if w[i] < 9 else NEVER; fd[('s', i)] = s[i] if s[i] < 9 else NEVER
    for x in Pv:
        if x != slot and x not in fd: fd[x] = NEVER
    res = {}
    for cf in CC:
        for e_ in grow.embeddings(cf, Pv, pa, pf, fd):
            req = dict((v, cf[3][u]) for u, v in e_ if v not in fd)
            if slot in req: res.setdefault(req[slot], cf[0])
    return res
mode = argv[0]
if mode == 'rules':
    D, SG = int(argv[1]), argv[2]
    U = []
    for fn in sorted(glob.glob('rejust_rules_d%d_%s_*_4.json' % (D, SG))): U += [o for o in json.load(open(fn)) if not o['justified']]
    n = 0
    for o in U:
        r = strict(D, [int(c) for c in o['test_link']], [int(c) for c in o['test_apex']], 0, int(SG), ALL)
        if o['p'] in r: n += 1; print('  now justified by', r[o['p']], o['w_req'], o['s_req'])
    print('D', D, 'sg', SG, 'unjustified', len(U), 'justified by extended registry', n)
else:
    U = json.load(open('unjustified_sides.json')); n = 0
    for x in U:
        wgt, lk, ap, j, sg = x[:5]
        r = strict(len(lk), [int(c) for c in lk], [int(c) for c in ap], j, sg, ALL)
        if 5 in r: n += 1; print('  side now justified by', r[5], lk, ap, j, sg)
    print('sides unjustified', len(U), 'justified by extended registry', n)
