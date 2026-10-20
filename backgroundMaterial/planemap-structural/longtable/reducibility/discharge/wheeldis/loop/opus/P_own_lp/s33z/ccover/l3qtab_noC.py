"""[s33z ccover copy: D-only tables.] Stage 28 l3q d = 7 payee mask kill table (Opus s28q, RELAY_SPEC_s21.md 21.4), exhaustive.
Payee v (centre, d = 7), payer u = w_0 = 7, side sg. Known: v, u, w_{sg}, w_{2sg}, w_{3sg}, w_{4sg} (= c, w2, w3, w4),
a = s_0 (sg = +1) / s_6 (sg = -1), o = the other apex of u (s_6 / s_0). Free: u's private adjacent to a.
Unknown (degree 99, strict 14' rule: an embedding touching one is no match): w_{-sg}, w_{-2sg}, the other apexes,
every other private. Letter 9 is never an exact degree. Rows: c, a in {5,6}; w2, w3, w4, o in 5..9.
usage: python3 l3qtab.py EXDIR TD TC OUT.json sg"""
import sys, json, time, itertools
EX, TD, TC, OUTF, SG = sys.argv[1:6]; SG = int(SG)
F = '/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s30t/f/'
sys.argv = [sys.argv[0], EX, TD, TC, 'unused', 'donly=1']   # s33z ccover: RSST D2 verdicts only (s30t s16_filter donly=1)
exec(open(F + 's16_filter.py').read().replace("if __name__ == '__main__':", "if False:"))
D = 7
def one(C, sg, c, w2, w3, w4, a, o):
    LK = [9] * D; LK[0] = 7
    for k, l in zip((1, 2, 3, 4), (c, w2, w3, w4)): LK[(k * sg) % D] = l
    P, pa, pf = build(D, LK)
    sa, so = (('s', 0), ('s', D - 1)) if sg == 1 else (('s', D - 1), ('s', 0))
    slot = [x for x in P if x[0] == 'p' and x[1] == 0 and sa in pa[x]]; assert len(slot) == 1; slot = slot[0]
    known = {('u',): 7, ('w', 0): 7, sa: a, so: o}
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
    C = registry(); print('forbidden', len(C), flush=True); out = {}; t0 = time.time(); n = 0
    for c, a in itertools.product((5, 6), repeat=2):
        for w2, w3, w4, o in itertools.product(LET, repeat=4):
            m, why = one(C, SG, c, w2, w3, w4, a, o); n += 1
            out['%+d %d%d%d%d %d%d' % (SG, c, w2, w3, w4, a, o)] = [m, why]
            if n % 250 == 0: print('  %d %.0fs' % (n, time.time() - t0), flush=True)
    json.dump(out, open(OUTF, 'w')); print('done', n, '%.0fs' % (time.time() - t0))
