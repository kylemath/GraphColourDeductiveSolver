"""EXPLORE round 59s, every possible filling: sat59.py's census without the open-fillings restriction.  A slot whose
letter equals its disc degree closes off (an edge between its two boundary neighbours), so the fillings are split into
parts with a fixed structure, recursively (as cen53's parts); letters below a slot's disc degree are impossible.
NOREG=1 drops the registry (control: what saturation alone kills).  Same loads, criteria and output as sat59.py, one line
per (private letters, part) with survivors, one line per private letters otherwise.
usage: python3 sat59b.py TD TC XKC [LK SV PAY]   -> sat59b_<LK>_<SV>[_noreg].txt"""
import sys, os, itertools, collections, time
from fractions import Fraction as Q
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, H)
ARGS = list(sys.argv)
import sat59 as S                      # parses its own argv; frame() and cylinders() are reused
C = S.C; grow = S.grow; LK, SV, PAY, d = S.LK, S.SV, S.PAY, S.d
TD, TC, XKC = ARGS[1:4]
NOREG = os.environ.get('NOREG') == '1'

def parts(E, lets):
    """[(disc, lets)] covering every possible filling once, each with a fixed structure."""
    out = []
    def rec(E, lets):
        lets = {x: tuple(l for l in ls if l == 9 or l >= len(E.adj[x])) for x, ls in lets.items() if x in E.B}
        if any(not ls for ls in lets.values()): return
        for x in E.B:
            k = len(E.adj[x])
            if k <= 8 and k in lets[x]:
                F = E.copy()
                if F.close(x, k):
                    l2 = dict(lets); del l2[x]; rec(F, l2)
                l3 = dict(lets); l3[x] = tuple(l for l in lets[x] if l != k); rec(E, l3)
                return
        out.append((E, lets))
    rec(E, lets)
    return out

def main():
    REG, miss = C.F.registry(TD, TC)
    if NOREG: REG = []
    XR = [grow.kcline(l, 'xreg') for l in open(XKC) if l.strip()]
    D0, u, W, Sv, PR = S.frame()
    big = lambda g: g >= 7
    sigma = Q(6 - d) + sum(Q(1, sum(big(D0.deg[y]) for y in D0.adj[x])) for x in D0.adj[u] if D0.deg.get(x) == 5)
    tag = '_noreg' if NOREG else ''
    out = open(os.path.join(H, 'sat59b_%s_%s%s.txt' % (''.join(map(str, LK)), ''.join(map(str, SV)), tag)), 'w')
    def say(*a):
        s = ' '.join(map(str, a)); print(s, flush=True); out.write(s + '\n'); out.flush()
    privs = [x for j in PAY for x in PR[j]]
    say('# sat59b %s: row d%d %s/%s, payees %s, sigma(u) = %s; registry %d%s, 2026 set %d; privates %s; every possible filling' % (
        time.strftime('%H:%MZ', time.gmtime()), d, ''.join(map(str, LK)), ''.join(map(str, SV)), ','.join('w%d' % j for j in PAY),
        sigma, len(REG), ' (NOREG control)' if NOREG else '', len(XR), ' '.join(D0.lab[x] for x in privs)))
    TOT = collections.Counter(); SURV = collections.Counter(); SURVX = collections.Counter(); bad = 0; npart = 0
    for A in itertools.product((5, 6, 7, 8, 9), repeat=len(privs)):
        t0 = time.time(); E0 = D0.copy(); ok = True
        for x, l in zip(privs, A):
            if l <= 8 and not E0.close(x, l): ok = False; break
        if not ok: bad += 1; continue
        pd = {x: l for x, l in zip(privs, A)}
        lets0 = {x: ((9,) if pd.get(x) == 9 else (5, 6, 7, 8, 9)) for x in E0.B}
        PT = parts(E0, lets0); npart += len(PT)
        asv = collections.Counter(); atot = 0; acov = 0; notes = []
        for pi, (E, lets) in enumerate(PT):
            SL = sorted(lets)
            def g(y, cls):
                if y in E.deg: return E.deg[y]
                if y in pd: return pd[y]
                return cls[y]
            fives = {j: [x for x in E.adj[W[j]] if E.deg.get(x) == 5] for j in PAY}
            R = sorted({y for j in PAY for x in fives[j] for y in E.adj[x] if y not in E.deg and y not in pd})
            cyl, who = S.cylinders(E, lets, REG)
            tot = C.prod(len(lets[x]) for x in SL); cov = C.count(cyl, SL, lets); atot += tot; acov += cov
            sv = collections.Counter(); svc = []; memo = {}
            for cls in itertools.product((0, 1), repeat=len(R)):
                l2 = dict(lets)
                for y, c in zip(R, cls): l2[y] = tuple(l for l in lets[y] if big(l) == bool(c))
                if any(not l2[y] for y in R): continue
                cl = {y: (7 if c else 5) for y, c in zip(R, cls)}
                Lv = {j: Q(6 - LK[j]) + sum(Q(1, sum(big(g(y, cl)) for y in E.adj[x])) for x in fives[j]) for j in PAY}
                kap = {j: max(-Lv[j], 0) for j in PAY}; K = [j for j in PAY if kap[j] > 0]
                def sat(hi):
                    if not K: return False
                    for j in K:
                        m = 1 + sum(1 for i in PAY if i != j and Lv[i] > 0 and W[i] in E.adj[W[j]])
                        if hi: m += sum(1 for x in PR[j] if big(pd[x]))
                        if kap[j] / m < sigma / len(K): return False
                    return True
                crit = {'lo': sat(False), 'hi': sat(True), 'short': all(kap[j] >= sigma / len(PAY) for j in PAY)}
                n = C.prod(len(l2[x]) for x in SL); unc = n - C.count(cyl, SL, l2, memo)
                for k, v in crit.items():
                    if not v: sv[k] += unc
                if not crit['lo'] and unc: svc.append((cls, unc, Lv))
            asv.update(sv)
            if sv['lo'] or sv['short']:
                cx, _ = S.cylinders(E, lets, XR); sx = 0
                for cls, unc, Lv in svc:
                    l2 = dict(lets)
                    for y, c in zip(R, cls): l2[y] = tuple(l for l in lets[y] if big(l) == bool(c))
                    sx += C.prod(len(l2[x]) for x in SL) - C.count(cyl + cx, SL, l2)
                SURVX['lo'] += sx
                closed = sorted(E.lab[x] + '=%d' % E.deg[x] for x in E.deg if x not in E0.deg)
                ex = svc[0] if svc else None
                notes.append('part %d (closed %s): %d fillings, survivors lo %d hi %d short %d, lo with 2026 %d%s' % (
                    pi, ' '.join(closed) or '-', tot, sv['lo'], sv['hi'], sv['short'], sx,
                    (' | e.g. %s, L %s' % (' '.join('%s:%s' % (E.lab[y], 'big' if c else 'small') for y, c in zip(R, ex[0])) or 'no R',
                                            ' '.join('w%d=%s' % (j, ex[2][j]) for j in PAY))) if ex else ''))
        TOT['possible'] += atot; TOT['registry'] += acov; SURV.update(asv)
        say('A %s | %d parts, %d fillings, registry %.3f%% | survivors lo %d hi %d short %d | %.0fs' % (
            ' '.join('%s=%d' % (D0.lab[x], l) for x, l in zip(privs, A)), len(PT), atot, 100.0 * acov / atot if atot else 100,
            asv['lo'], asv['hi'], asv['short'], time.time() - t0))
        for n_ in notes: say('   ', n_)
    say('# total: %d assignments impossible, %d parts; %d possible fillings; registry covers %.4f%%; survivors (not registry, u not saturated): m_lo %d, m_hi %d, short form %d; m_lo with the 2026 set %d' % (
        bad, npart, TOT['possible'], 100.0 * TOT['registry'] / TOT['possible'] if TOT['possible'] else 100,
        SURV['lo'], SURV['hi'], SURV['short'], SURVX['lo']))

if __name__ == '__main__':
    main()
