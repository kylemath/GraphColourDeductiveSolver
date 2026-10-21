"""EXPLORE round 59s (Long Table 05:13Z, doc "Capacity transport rule"): saturation census for capacity transport on a
face row, stage 1 = equal split (each 5 splits its unit over its neighbours of degree >= 7).
The row's 2-ball is closed (u, link LK, apexes SV all exact).  The privates of the two link bigs PAY (default w0, w1) are
each 5..9; a private at 5..8 is closed and its neighbours become slots; every other boundary vertex is a slot 5..9
(9 = degree >= 9, never exact).  Open fillings only (each slot above its disc degree; closing fillings counted apart),
as chain59.py.  Loads: L(v) = (6 - deg v) + sum over v's 5-neighbours x of 1/l(x), l(x) = number of x's neighbours of
degree >= 7; kappa = max(-L, 0).  u's surplus sigma = L(u) (from the closed 2-ball).  Stage 2 saturates u iff k >= 1
and kappa(v)/m(v) >= sigma/k for each of the k payees v with spare; m(v) = number of v's big neighbours with surplus:
m_lo counts u and the other payee if it is overloaded; m_hi adds v's big privates (loads outside the window).  The
short form (Long Table 05:13Z): kappa(v) >= sigma/2 for both payees.  A filling is dead when the registry (fam51:
RSST 582 + twoeng names of TD/TC) holds a configuration in the window or u is saturated; the 2026 set (XKC) is matched
apart, on the completions with survivors only.
usage: python3 sat59.py TD TC XKC [LK SV PAY]   (defaults 7766556 6567566 0,1) -> sat59_<LK>_<SV>.txt"""
import sys, os, itertools, collections, time
from fractions import Fraction as Q
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, H)
TD, TC, XKC = sys.argv[1:4]
LK = [int(c) for c in (sys.argv[4] if len(sys.argv) > 4 else '7766556')]
SV = [int(c) for c in (sys.argv[5] if len(sys.argv) > 5 else '6567566')]
PAY = [int(c) for c in (sys.argv[6] if len(sys.argv) > 6 else '0,1').split(',')]
sys.argv = sys.argv[:1]
import chain59 as C
import grow
d = len(LK)

def frame():
    D = C.Disc(); u, W = D.wheel(d, 'u')
    for i in range(d):
        assert D.close(W[i], LK[i]); D.lab[W[i]] = 'w%d' % i
    S = []
    for i in range(d):
        s = [x for x in D.adj[W[i]] & D.adj[W[(i + 1) % d]] if x != u]; assert len(s) == 1; S.append(s[0]); D.lab[s[0]] = 's%d' % i
    for i in range(d): assert D.close(S[i], SV[i]), i
    PR = {}
    for j in PAY:
        pj = [x for x in D.adj[W[j]] if x not in D.deg]
        assert len(pj) == LK[j] - 5, (j, pj)
        for x in pj: D.lab[x] = 'p%d%s' % (j, 'a' if S[0] in D.adj[x] else ('b' if S[j] in D.adj[x] or S[j - 1] in D.adj[x] else 'm'))
        PR[j] = sorted(pj, key=lambda x: D.lab[x])
    return D, u, W, S, PR

def minimal(cyl):
    cs = sorted({frozenset(c.items()) for c in cyl}, key=len); keep = []
    for c in cs:
        if not any(m <= c for m in keep): keep.append(c)
    return [dict(c) for c in keep]

def cylinders(E, lets, CONF):
    P = list(range(E.n)); pa = {v: set(E.adj[v]) for v in P}; pf = set(E.tris); fd = dict(E.deg); out = []; who = {}
    for c in CONF:
        if len(c[2]) > len(P): continue
        for e in grow.embeddings(c, P, pa, pf, fd):
            req = {v: c[3][x] for x, v in e if v not in fd}
            if all(req[v] in lets[v] for v in req):
                out.append(req); who.setdefault(frozenset(req.items()), c[0])
    m = minimal(out)
    return m, {frozenset(c.items()): who[frozenset(c.items())] for c in m}

def main():
    REG, miss = C.F.registry(TD, TC)
    XR = [grow.kcline(l, 'xreg') for l in open(XKC) if l.strip()]
    D0, u, W, S, PR = frame()
    big = lambda g: g >= 7
    def sig_u():
        L = Q(6 - d)
        for x in D0.adj[u]:
            if D0.deg.get(x) == 5: L += Q(1, sum(big(D0.deg[y]) for y in D0.adj[x]))
        return L
    sigma = sig_u()
    out = open(os.path.join(H, 'sat59_%s_%s.txt' % (''.join(map(str, LK)), ''.join(map(str, SV)))), 'w')
    def say(*a):
        s = ' '.join(map(str, a)); print(s, flush=True); out.write(s + '\n'); out.flush()
    privs = [x for j in PAY for x in PR[j]]
    say('# sat59 %s: row d%d %s/%s, payees %s, sigma(u) = %s; registry %d (%d names not found), 2026 set %d; privates %s' % (
        time.strftime('%H:%MZ', time.gmtime()), d, ''.join(map(str, LK)), ''.join(map(str, SV)), ','.join('w%d' % j for j in PAY),
        sigma, len(REG), miss, len(XR), ' '.join(D0.lab[x] for x in privs)))
    TOT = collections.Counter(); SURV = collections.Counter(); SURVX = collections.Counter(); bad = 0
    for A in itertools.product((5, 6, 7, 8, 9), repeat=len(privs)):
        t0 = time.time(); E = D0.copy(); ok = True
        for x, l in zip(privs, A):
            if l <= 8 and not E.close(x, l): ok = False; break
        if not ok: bad += 1; continue
        lets = {x: tuple(l for l in (5, 6, 7, 8, 9) if l > len(E.adj[x]) or (l == 9 and len(E.adj[x]) >= 9)) for x in E.B}
        allp = C.prod(len([l for l in (5, 6, 7, 8, 9) if l >= len(E.adj[x]) or l == 9]) for x in E.B)
        for x, l in zip(privs, A):
            if l == 9: lets[x] = (9,) if 9 in lets[x] else ()
        if any(not v for v in lets.values()): bad += 1; continue
        SL = sorted(lets); pd = {x: l for x, l in zip(privs, A)}
        def g(y, cls):
            if y in E.deg: return E.deg[y]
            if y in pd: return pd[y]
            return cls[y]
        # slots that decide some l(x): neighbours of the payees' 5-neighbours
        fives = {j: [x for x in E.adj[W[j]] if E.deg.get(x) == 5] for j in PAY}
        R = sorted({y for j in PAY for x in fives[j] for y in E.adj[x] if y not in E.deg and y not in pd})
        cyl, who = cylinders(E, lets, REG)
        tot = C.prod(len(lets[x]) for x in SL); covall = C.count(cyl, SL, lets)
        TOT['open'] += tot; TOT['possible'] += allp; TOT['registry'] += covall
        sv = collections.Counter(); svc = []; LR = {j: set() for j in PAY}; memo = {}
        for cls in itertools.product((0, 1), repeat=len(R)):
            l2 = dict(lets)
            for y, c in zip(R, cls): l2[y] = tuple(l for l in lets[y] if big(l) == bool(c))
            if any(not l2[y] for y in R): continue
            cl = {y: (7 if c else 5) for y, c in zip(R, cls)}
            Lv = {}
            for j in PAY:
                L = Q(6 - LK[j])
                for x in fives[j]: L += Q(1, sum(big(g(y, cl)) for y in E.adj[x]))
                Lv[j] = L; LR[j].add(L)
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
            if not crit['hi'] and unc: svc.append((cls, unc, Lv, crit))
        SURV.update(sv)
        line = 'A %s | slots %d, open %d (%.1f%% of %d), registry %.3f%% | L %s | survivors lo %d hi %d short %d | %.0fs' % (
            ' '.join('%s=%d' % (E.lab[x], l) for x, l in zip(privs, A)), len(SL), tot, 100.0 * tot / allp, allp, 100.0 * covall / tot,
            ' '.join('w%d %s..%s' % (j, min(LR[j]), max(LR[j])) for j in PAY), sv['lo'], sv['hi'], sv['short'], time.time() - t0)
        if sv['hi']:
            cx, wx = cylinders(E, lets, XR)
            sx = 0
            for cls, unc, Lv, crit in svc:
                l2 = dict(lets)
                for y, c in zip(R, cls): l2[y] = tuple(l for l in lets[y] if big(l) == bool(c))
                n = C.prod(len(l2[x]) for x in SL); sx += n - C.count(cyl + cx, SL, l2)
            SURVX['hi'] += sx
            line += ' | hi with 2026 %d' % sx
            ex = svc[0]
            line += ' | e.g. %s L %s' % (' '.join('%s:%s' % (E.lab[y], 'big' if c else 'small') for y, c in zip(R, ex[0])) or 'no R slots',
                                         ' '.join('w%d=%s' % (j, ex[2][j]) for j in PAY))
        say(line)
    say('# total: %d assignments impossible; open fillings %d of %d possible (%.1f%%); registry covers %.4f%%; survivors (not registry, u not saturated): m_lo %d, m_hi %d, short form %d; m_hi with the 2026 set %d' % (
        bad, TOT['open'], TOT['possible'], 100.0 * TOT['open'] / TOT['possible'], 100.0 * TOT['registry'] / TOT['open'],
        SURV['lo'], SURV['hi'], SURV['short'], SURVX['hi']))

if __name__ == '__main__':
    main()
