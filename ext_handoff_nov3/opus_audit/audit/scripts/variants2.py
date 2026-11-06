import sys
exec(open('variants.py').read().split("for a in rows:")[0])
for a in rows:
    lk, ap, j, sg = a.split(','); w = [int(c) for c in lk]; s = [int(c) for c in ap]; D = len(w); j = int(j); sg = int(sg)
    print('ROW', lk, ap, j, sg)
    # other side's slot (swapped orientation)
    k = test(D, w, s, j, -sg, C, True)
    print('   other private (side %+d) strict kills: %s' % (-sg, {L: v[:2] for L, v in k.items()}))
    # both privates free, record joint requirement
    Pv, pa, pf = build(D, list(w))
    pr = [x for x in Pv if x[0] == 'p' and x[1] == j]
    fd = {('u',): D}
    for i in range(D): fd[('w', i)] = w[i] if w[i] < 9 else NEVER; fd[('s', i)] = s[i] if s[i] < 9 else NEVER
    for x in Pv:
        if x not in fd and x not in pr: fd[x] = NEVER
    J = {}
    for cf in C:
        for e_ in grow.embeddings(cf, Pv, pa, pf, fd):
            req = tuple(sorted((v, cf[3][u]) for u, v in e_ if v not in fd))
            J.setdefault(req, cf[0])
    sa = ('s', j) if sg == 1 else ('s', (j - 1) % D)
    print('   privates of w_j:', [(x, sorted(pa[x])) for x in pr], 'slot apex', sa)
    print('   joint (both privates of w_j free) requirements:', sorted(J.items())[:8])
