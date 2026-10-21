"""[s53c copy of s45/l3qtabV.py: D-only V tables via s30t s16_filter donly=1 (as s33z/ccover/l3qtab_noC.py).] s45 l3q payee mask table for payee letter V (RELAY_SPEC_s45 45.3) = s28q/s33z l3qtab.py with the link length D and the
centre degree as parameters.  V = 7: D = 7, centre 7 (reproduces l3qtab.py).  V = 8: D = 8, centre 8.  V = 9: D = 9, centre
99 (never exact: no embedding may use the centre; sound for every d >= 9).  Payer u = w_0 = 7, side sg.  Known: u, w_0,
w_{sg..4sg} (= c, w2, w3, w4), a = s_0 / s_{D-1}, o = the other apex.  Free: w_0's private adjacent to a.  Unknown: all else
(99, strict: an embedding touching one is no match).  A letter is killed only by an embedding that uses a2 (reading (A)).
usage: python3 l3qtabV.py EXDIR TD TC OUT.json sg V [exname=FILE] [keys=FILE (lines 'sg cw2w3w4 ao')]"""
import sys, json, time, itertools
EX, TD, TC, OUTF, SG, V = sys.argv[1:7]; SG = int(SG); V = int(V)
XO = dict(a.split('=', 1) for a in sys.argv[7:])
F = '/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s30t/f/'
sys.argv = [sys.argv[0], EX, TD, TC, 'unused', 'donly=1']   # s53c: RSST D2 verdicts only (s30t s16_filter donly=1)
exec(open(F + 's16_filter.py').read().replace("if __name__ == '__main__':", "if False:"))
D = V; CEN = V if V < 9 else NEVER
def one(C, sg, c, w2, w3, w4, a, o):
    LK = [9] * D; LK[0] = 7
    for k, l in zip((1, 2, 3, 4), (c, w2, w3, w4)): LK[(k * sg) % D] = l
    P, pa, pf = build(D, LK)
    sa, so = (('s', 0), ('s', D - 1)) if sg == 1 else (('s', D - 1), ('s', 0))
    slot = [x for x in P if x[0] == 'p' and x[1] == 0 and sa in pa[x]]; assert len(slot) == 1; slot = slot[0]
    known = {('u',): CEN, ('w', 0): 7, sa: a, so: o}
    for k, l in zip((1, 2, 3, 4), (c, w2, w3, w4)): known[('w', (k * sg) % D)] = l
    fd = {}; UNKV = set()
    for x in P:
        if x == slot: continue
        if x in known: fd[x] = known[x] if known[x] < 9 else NEVER
        else: fd[x] = NEVER; UNKV.add(x)
    kill = {}
    for cf in C:
        for e_ in grow.embeddings(cf, P, pa, pf, fd):
            if any(v in UNKV for u, v in e_): continue
            req = dict((v, cf[3][u]) for u, v in e_ if v not in fd)
            if slot in req: kill.setdefault(req[slot], set()).add(cf[0])
    m = 31
    for val in kill: m &= ~(1 << LET.index(val))
    return m, {str(k): sorted(v)[:3] for k, v in kill.items()}
if __name__ == '__main__' or True:
    C = registry(); n0 = len(C)
    if 'exname' in XO:
        EXN = set(l.split()[0] for l in open(XO['exname']) if l.strip() and not l.startswith('#'))
        C = [cf for cf in C if cf[0] not in EXN]
    print('V', V, 'D', D, 'centre', CEN, 'forbidden', n0, 'after exname', len(C), flush=True)
    if 'keys' in XO:
        todo = []
        for l in open(XO['keys']):
            s_, wd, ao = l.split()
            if int(s_) == SG: todo.append(tuple(int(ch) for ch in wd) + tuple(int(ch) for ch in ao))
        todo = sorted(set(todo))
    else:
        todo = [(c, w2, w3, w4, a, o) for c, a in itertools.product((5, 6), repeat=2) for w2, w3, w4, o in itertools.product(LET, repeat=4)]
    out = {}; t0 = time.time(); n = 0
    for c, w2, w3, w4, a, o in todo:
        m, why = one(C, SG, c, w2, w3, w4, a, o); n += 1
        out['%+d %d%d%d%d %d%d' % (SG, c, w2, w3, w4, a, o)] = [m, why]
        if n % 250 == 0: print('  %d %.0fs' % (n, time.time() - t0), flush=True)
    json.dump(out, open(OUTF, 'w')); print('done', n, '%.0fs' % (time.time() - t0))
