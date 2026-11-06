"""For given sides: which semantics/registry variants kill the slot letter 5?  variants: rsst633 (all RSST), nonstrict (other privates free)."""
import sys, json, time, collections, os
ROOT = os.environ.get('F2B7_AUDIT_ROOT') or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # package root
SC = ROOT + '/tree'  # was '/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad'
P = ROOT + '/tree/P_own_lp'  # was '/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp'
EX = SC + '/ex_A97'; TD = P + '/s33z/reg_A97/k3x_D_A97.out'; TC = P + '/s33z/reg_A97/k3x_C_A97.cfast'
EXN = P + '/s77_k6patch/tab/exname_keep95p131f.txt'; NL51 = P + '/s39o/k57/nl51_kc.txt'
rows = sys.argv[1:]
sys.argv = ['s16', EX, TD, TC, 'unused', 'donly=0']
exec(open(P + '/s30t/f/s16_filter.py').read().replace("if __name__ == '__main__':", "if False:"))
C = registry(); have = {c[0] for c in C}
for l in open(NL51).read().splitlines():
    f = l.split()
    if len(f) == 5 and f[1].isdigit() and f[2].isdigit() and ';' in f[3] + f[4] and f[0] not in have:
        C.append(grow.kcline(l, 'nl51')); have.add(f[0])
X = set(l.split()[0] for l in open(EXN) if l.strip() and not l.startswith('#'))
Cx = [cf for cf in C if cf[0] in X]
C = [cf for cf in C if cf[0] not in X]
K44 = os.path.join(LOOP, 'k44')
ver = {}
for l in open(os.path.join(K44, 'rsst_verdicts.txt')):
    if l.startswith('#') or not l.strip(): continue
    f = l.split(); v = [x for x in f if x.startswith('verdict=')]; ver[f[0]] = v[0][8:] if v else None
kcn = [l.split()[0] for l in open(os.path.join(K44, 'rsst.txt')) if l.strip()]
R51 = [(n,) + tuple(c[1:]) for n, c in zip(kcn, grow.rsst()) if ver.get(n) == 'none']
print('broad', len(C), 'exname-held configs in registry', len(Cx), 'rsst none-verdict', len(R51), flush=True)
def test(D, w, s, j, sg, CC, strict=True, ufree=False):
    Pv, pa, pf = build(D, list(w))
    sa = ('s', j) if sg == 1 else ('s', (j - 1) % D)
    slot = [x for x in Pv if x[0] == 'p' and x[1] == j and sa in pa[x]][0]
    fd = {} if ufree else {('u',): D}
    for i in range(D): fd[('w', i)] = w[i] if w[i] < 9 else NEVER; fd[('s', i)] = s[i] if s[i] < 9 else NEVER
    for x in Pv:
        if x == slot or x in fd or x == ('u',): continue
        if strict: fd[x] = NEVER
    kill = {}
    for cf in CC:
        for e_ in grow.embeddings(cf, Pv, pa, pf, fd):
            req = dict((v, cf[3][u]) for u, v in e_ if v not in fd)
            if slot in req: kill.setdefault(req[slot], []).append((cf[0], sorted((str(v), l) for v, l in req.items() if v != slot)))
    return kill
for a in rows:
    lk, ap, j, sg = a.split(','); w = [int(c) for c in lk]; s = [int(c) for c in ap]; D = len(w)
    print('ROW', lk, ap, j, sg)
    for nm, CC, st in (('broad strict', C, True), ('exname-held strict', Cx, True), ('rsst-none strict', R51, True), ('broad NONSTRICT', C, False)):
        k = test(D, w, s, int(j), int(sg), CC, st)
        print('   %-20s kills5: %s' % (nm, (k.get(5) or [])[:3]))
