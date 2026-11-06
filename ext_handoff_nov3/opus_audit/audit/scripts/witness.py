import sys
ROWS = sys.argv[1:]; sys.argv = ["x"]
exec(open('variants.py').read().split("for a in rows:")[0])
KP = [grow.kcline(l, 'kpriv') for l in open(P + '/s49/kpriv_kc.txt').read().splitlines() if l.strip() and len(l.split()) == 5]
ALL = C + Cx + R51 + KP
for a in ROWS:
    lk, ap, j, sg = a.split(','); w = [int(c) for c in lk]; s = [int(c) for c in ap]; D = len(w); j = int(j); sg = int(sg)
    Pv, pa, pf = build(D, w)
    sa = ('s', j) if sg == 1 else ('s', (j - 1) % D)
    slot = [x for x in Pv if x[0] == 'p' and x[1] == j and sa in pa[x]][0]
    other = [x for x in Pv if x[0] == 'p' and x[1] == j and x != slot][0]
    print('ROW', lk, ap, 'j', j, 'side', sg, 'slot', slot, 'nbrs', sorted(pa[slot]), 'other', other)
    for free_other in (False, True):
        fd = {('u',): D}
        for i in range(D): fd[('w', i)] = w[i] if w[i] < 9 else NEVER; fd[('s', i)] = s[i] if s[i] < 9 else NEVER
        for x in Pv:
            if x == slot or x in fd: continue
            if free_other and x == other: continue
            fd[x] = NEVER
        J = {}
        for cf in ALL:
            for e_ in grow.embeddings(cf, Pv, pa, pf, fd):
                req = tuple(sorted((str(v), cf[3][u]) for u, v in e_ if v not in fd))
                if req not in J: J[req] = (cf[0], sorted(str(v) for u, v in e_))
        print('   %s: %s' % ('slot+other free' if free_other else 'strict (slot only)', {k: v[0] for k, v in J.items()} or 'no embedding'))
