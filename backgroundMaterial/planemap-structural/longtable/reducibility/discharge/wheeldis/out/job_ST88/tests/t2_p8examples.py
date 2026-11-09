# ST-88 T2: W6b's p8_test.json "E" examples (row label, key, value_A, value_B) through code_gk8/gkfam.py (receiver d >= 8 rows:
# gkwin IN - OUT). A payer SET {8, 9} is the sum of its single-letter keys (PAYER8SPEC 1). pmask: the patched298 kill stack
# (kill6_U*.npy, the K3l5j stack of T6), and, to show whether an answer depends on the stack, pmask = all letters and = none.
import sys, ast, json, collections, numpy as np
C = sys.argv[1] if len(sys.argv) > 1 else '/tmp/swarm-W17/code_gk8'; sys.path.insert(0, C)
import gkfam as G
J = sys.argv[2] if len(sys.argv) > 2 else '.'
KD = '/tmp/swarm-W17/kill/patched298'
KA = {U: np.load('%s/kill6_U%d.npy' % (KD, U)) for U in (7, 8, 9)}
PM = {'patched298': lambda U, *a: int(~KA[U][tuple(x - 5 for x in a)]) & 31, 'all': lambda U, *a: 31, 'none': lambda U, *a: 0}
E = json.load(open(J + '/in/p8_test.json'))['E']
def mask(fs): return sum(1 << (l - 5) for l in fs)
tot = collections.Counter(); out = []
for ctl, blk in E.items():
    for ex in blk['examples']:
        row, kstr, va, vb = ast.literal_eval(ex)
        Pset, Qset, cd = eval(kstr, {'__builtins__': {}}, {'frozenset': frozenset})
        lab, rest = row.split(' '); d = int(lab[1:]); lk, ap = rest.split('/'); w = [int(c) for c in lk]; s = [int(c) for c in ap]
        assert lab[0] == 'R' and len(w) == d == len(s)
        conds = ' '.join('%s=%s' % (p, G.msym(mask(m))) for p, m in sorted(cd.items()))
        parts = [mask({u}) for u in sorted(Pset)] if (Pset & {8, 9}) else [mask(Pset)]   # a payer set with 8 / 9 = sum of single-letter keys
        cdm = tuple(sorted((G.EPOS.index(p), mask(m)) for p, m in cd.items()))
        keys = [('k%d' % n, U_, mask(Qset), cdm) for n, U_ in enumerate(parts)]   # raw tuples: the matcher, not the parser
        refused = []
        for (kn, U_, V_, cd_) in keys:
            try: G.parse_key('%s EDGE(%s->%s)[%s]' % (kn, G.msym(U_), G.msym(V_), conds))
            except ValueError as e_: refused.append(str(e_).split(': ', 1)[1])
        res = {}
        for pn, pm in PM.items():
            ct = G.Win(G.Engine(keys), pm).row(d, w, s); res[pn] = sum(ct[k[0]] for k in keys)
        mine = res['patched298']
        which = 'A' if mine == va else 'B' if mine == vb else 'neither'
        dep = '' if len(set(res.values())) == 1 else ' (pmask-dependent: %s)' % res
        tot[(ctl, which)] += 1
        out.append('%-9s %-28s EDGE(%s->%s)[%s]: listed (A %d, B %d); code_gk8 %d -> %s%s%s' % (ctl, row, G.msym(mask(Pset)), G.msym(mask(Qset)), conds, va, vb, mine, which, dep,
                   ('; production parser refuses: ' + refused[0]) if refused else ''))
print('\n'.join(out))
print('T2 summary: %s' % dict(sorted(tot.items())))
