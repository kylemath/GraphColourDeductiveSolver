"""EXPLORE round 60 (coordinator 05:39Z/05:42Z): the pair census of the "Formal problem statement" thread asked from our side,
by containment only.  For a receiver row LK/SV (u, link and apexes closed; an apex letter 9 = >= 9 stays open) and a
link 7 w_k (a link or apex letter 9 = >= 9 stays open), its two privates p_k_1 (next to s_k) and p_k_2 (next to s_(k-1)) get letters a, b in 5..9 (9 = >= 9, left
open), the names of that thread's census (priv<a><b>).  Reported per (k, a, b): a configuration of the registry (RSST
582 + twoeng names of TD/TC) or of the 2026 set (XKC) inside the closed vertices, if any; else the share of the open
fillings of the boundary (each slot above its disc degree, as sat59.py) that the registry, then registry + 2026 set,
covers.
usage: python3 pair60.py TD TC XKC [ROW ...]   (ROW = LK/SV, default the three rows of that census) -> k60/pair60.txt
(or k60/$PAIROUT)"""
import sys, os, itertools, time
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(H, '..', 'k59'))
TD, TC, XKC = sys.argv[1:4]
ROWS = sys.argv[4:] or ['7766556/6567566', '7665566/6675676', '7766655/6567659']
sys.argv = sys.argv[:1]
import chain59 as C
import grow

def frame(LK, SV):
    d = len(LK); D = C.Disc(); u, W = D.wheel(d, 'u')
    for i in range(d):
        D.lab[W[i]] = 'w%d' % i
        if LK[i] != 9: assert D.close(W[i], LK[i])
    S = []
    for i in range(d):
        s = [x for x in D.adj[W[i]] & D.adj[W[(i + 1) % d]] if x != u]; assert len(s) == 1; S.append(s[0]); D.lab[s[0]] = 's%d' % i
    for i in range(d):
        if SV[i] != 9: assert D.close(S[i], SV[i]), i
    return D, u, W, S

def privates(D, W, S, k):
    d = len(W); pk = [x for x in D.adj[W[k]] if x not in D.deg and x not in S and x not in W]
    assert len(pk) == 2, pk
    p1 = [x for x in pk if S[k] in D.adj[x]]; p2 = [x for x in pk if S[k - 1] in D.adj[x]]
    assert len(p1) == len(p2) == 1 and p1 != p2
    D.lab[p1[0]] = 'p%d_1' % k; D.lab[p2[0]] = 'p%d_2' % k
    return p1[0], p2[0]

def cyls(E, lets, CONF):
    P = list(range(E.n)); pa = {v: set(E.adj[v]) for v in P}; pf = set(E.tris); fd = dict(E.deg); out = []; inside = []
    for c in CONF:
        if len(c[2]) > len(P): continue
        for e in grow.embeddings(c, P, pa, pf, fd):
            req = {v: c[3][x] for x, v in e if v not in fd}
            if not req: inside.append(c[0])
            if all(req[v] in lets[v] for v in req): out.append(req)
    return C.minimal(out), sorted(set(inside))

def main():
    REG, miss = C.F.registry(TD, TC)
    XR = [grow.kcline(l, 'xreg') for l in open(XKC) if l.strip()]
    out = open(os.path.join(H, os.environ.get('PAIROUT', 'pair60.txt')), 'w')
    def say(*a):
        s = ' '.join(map(str, a)); print(s, flush=True); out.write(s + '\n'); out.flush()
    say('# pair60 %s: registry %d (%d names not found), 2026 set %d; letters a = p_k_1 (next to s_k), b = p_k_2 (next to s_(k-1)), 9 = >= 9 open' % (
        time.strftime('%H:%MZ', time.gmtime()), len(REG), miss, len(XR)))
    for row in ROWS:
        lk, sv = row.split('/'); LK = [int(c) for c in lk]; SV = [int(c) for c in sv]
        for k in range(len(LK)):
            if LK[k] != 7: continue
            dead = 0
            for a, b in itertools.product((5, 6, 7, 8, 9), repeat=2):
                t0 = time.time(); D, u, W, S = frame(LK, SV); p1, p2 = privates(D, W, S, k); ok = True
                for x, l in ((p1, a), (p2, b)):
                    if l <= 8 and not D.close(x, l): ok = False
                if not ok: say('%s w%d priv%d%d: impossible' % (row, k, a, b)); continue
                lets, allp = C.open_lets(D)
                for x, l in ((p1, a), (p2, b)):
                    if l == 9: lets[x] = (9,)
                for i in range(len(SV)):
                    if SV[i] == 9: lets[S[i]] = (9,)
                    if LK[i] == 9: lets[W[i]] = (9,)
                SL = sorted(lets); tot = C.prod(len(lets[x]) for x in SL)
                cr, ir = cyls(D, lets, REG)
                if ir:
                    dead += 1; say('%s w%d priv%d%d: DEAD, registry inside: %s' % (row, k, a, b, ' '.join(ir[:4]))); continue
                cx, ix = cyls(D, lets, XR)
                if ix:
                    dead += 1; say('%s w%d priv%d%d: DEAD, 2026 set inside: %s (registry %.2f%%)' % (row, k, a, b, ' '.join(ix[:4]),
                                                                                             100.0 * C.count(cr, SL, lets) / tot)); continue
                say('%s w%d priv%d%d: open, %d slots; registry covers %.2f%%, with the 2026 set %.2f%% of the open fillings (%.0fs)' % (
                    row, k, a, b, len(SL), 100.0 * C.count(cr, SL, lets) / tot, 100.0 * C.count(cr + cx, SL, lets) / tot, time.time() - t0))
            say('# %s w%d: %d of 25 letter pairs dead by containment' % (row, k, dead))

if __name__ == '__main__':
    main()
