import sys, json
argv = sys.argv[1:]
D = int(argv[0]); SG = argv[1]; part = argv[2]
sys.argv = ['x']
exec(open('variants.py').read().split("for a in rows:")[0])
import glob
xt = {}
pk, pn = map(int, part.split('/'))
U = []
for fn in sorted(glob.glob('rejust_rules_d%d_%s_*_4.json' % (D, SG))):
    U += [o for o in json.load(open(fn)) if not o['justified']]
U = U[pk::pn]
def run(D, w, s, j, sgi, CC, free, slot_side):
    Pv, pa, pf = build(D, list(w))
    sa = ('s', j) if slot_side == 1 else ('s', (j - 1) % D)
    slot = [x for x in Pv if x[0] == 'p' and x[1] == j and sa in pa[x]][0]
    fd = {('u',): D}
    for i in range(D): fd[('w', i)] = w[i] if w[i] < 9 else NEVER; fd[('s', i)] = s[i] if s[i] < 9 else NEVER
    for x in Pv:
        if x == slot or x in fd: continue
        if free == 'none': fd[x] = NEVER
        elif free == 'own' and not (x[0] == 'p' and x[1] == j): fd[x] = NEVER
    res = {}
    for cf in CC:
        for e_ in grow.embeddings(cf, Pv, pa, pf, fd):
            req = dict((v, cf[3][u]) for u, v in e_ if v not in fd)
            if slot in req: res.setdefault(req[slot], (cf[0], sorted((str(v), l) for v, l in req.items() if v != slot)))
    return res
import collections
st = collections.Counter(); det = []
for o in U:
    p = o['p']; w = [int(c) for c in o['test_link']]; s = [int(c) for c in o['test_apex']]; sgi = int(SG)
    expl = None
    for nm, CC, free, side in (('H4 exname-held/rsst-none, strict', Cx + R51, 'none', sgi), ('H5 other private, strict', C, 'none', -sgi),
                               ('H1 own other private free', C, 'own', sgi), ('H2 all privates free', C, 'all', sgi)):
        r = run(D, w, s, 0, sgi, CC, free, side)
        if p in r: expl = (nm, r[p]); break
    st[expl[0] if expl else 'UNEXPLAINED'] += 1
    det.append({'rule': [p, o['w_req'], o['s_req']], 'test': [o['test_link'], o['test_apex']], 'expl': expl})
print(D, SG, part, dict(st), flush=True)
json.dump(det, open('hyp_d%d_%s_%d_%d.json' % (D, SG, pk, pn), 'w'))
