"""Joint-outside refinement of the vacancy-D-reducibility game.

[computed, exploratory] Math worker, 2026-10-06.  See REFINEMENT.md.  vdred.py is untouched;
this file imports its Config / canon / map_split / swapcol / nc_matchings.

Knowledge is a partial triple K = (K_1, K_2, K_3), each entry None or a non-crossing matching
of that split's transitional ring edges.  One real outside O is fixed throughout, so all
known entries are the true matchings of O under the current colouring.

  * Reveal: the player picks th with K_th unknown; the adversary picks M_th such that
    K + {th: M_th} is contained in an allowed triple for the current ring colouring.
      adversary='full'      : allowed = all triples (independent matchings; SOUND superset)
      adversary='witnessed' : allowed = triples realised by explicit outsides in a sample
                              (SUBSET of the realisable ones: only a non-reducibility
                              verdict transfers to the exact joint game)
  * Move: swap one th-component C (cost 1).  M_th is always kept (a th-swap fixes the
    th-transitions).  If C contains no ring vertex, C is a whole component of T - v inside
    K - R, the ring colouring and the outside colouring are unchanged, so EVERY known entry
    is kept.  Otherwise only K_th is kept.
  * Win: link uses <= 3 colours.

V(c,K) = 0 if filled, else min_th [ K_th known ? A(c,K,th) : max_M A(c,K+M,th) ]
A(c,K,th) = 1 + min_C V(result).   Value iteration from +inf on the reachable node set.
Knowledge only restricts the adversary, so V <= the vdred.py value on every state.
"""
import sys, time
import vdred
from vdred import INF, canon, map_split, swapcol, nc_matchings


def solve_joint(cfg, adversary='full', allowed=None, verbose=True, max_nodes=3_000_000):
    """allowed: for adversary='witnessed', dict canonical ring colouring -> set of triples."""
    t0 = time.process_time()
    C = vdred.Config(cfg)
    ringset = set(C.ring)
    cols = C.colourings()
    unf = [c for c in cols if not C.filled(c)]

    comp_cache = {}
    def moves(c, th, M):
        key = (c, th, M)
        r = comp_cache.get(key)
        if r is None:
            T = C.trans(c, th)
            r = []
            for comp in C.components(c, th, T, M):
                c2 = list(c)
                for x in comp:
                    c2[x] = swapcol(c2[x], th)
                cc, sig = canon(c2)
                ringfree = not (set(comp) & ringset)
                perm = {t: map_split(t, sig) for t in (1, 2, 3)}
                r.append((cc, perm, ringfree, C.filled(cc)))
            comp_cache[key] = r
        return r

    def ring_kappa(c):
        return canon(tuple(c[i] for i in C.ring))

    def options(c, K, th):
        T = C.trans(c, th)
        allM = nc_matchings(len(T))
        if adversary == 'full':
            return allM
        kap, sig = ring_kappa(c)
        trip = allowed.get(kap, set())
        out = []
        for M in allM:
            KK = list(K); KK[th - 1] = M
            # translate to canonical-ring labelling of splits
            ok = False
            for tr in trip:
                if all(KK[t - 1] is None or tr[map_split(t, sig) - 1] == KK[t - 1] for t in (1, 2, 3)):
                    ok = True; break
            if ok:
                out.append(M)
        return out

    D = {}        # (c, K) -> id
    Dlist = []
    Dopts = []    # per D: list over th of list (adversary options) of Mv ids
    Mv = {}       # (c, K, th) -> id
    Mlist = []
    Msucc = []    # per Mv: list of D ids (-1 = filled)
    empty = (None, None, None)

    def did(c, K):
        k = (c, K)
        i = D.get(k)
        if i is None:
            i = len(Dlist); D[k] = i; Dlist.append(k); Dopts.append(None)
        return i

    def mid(c, K, th):
        k = (c, K, th)
        i = Mv.get(k)
        if i is None:
            i = len(Mlist); Mv[k] = i; Mlist.append(k); Msucc.append(None)
        return i

    for c in unf:
        did(c, empty)
    di = mi = 0
    while di < len(Dlist) or mi < len(Mlist):
        while di < len(Dlist):
            c, K = Dlist[di]
            opts = []
            for th in (1, 2, 3):
                if K[th - 1] is not None:
                    opts.append([mid(c, K, th)])
                else:
                    lst = []
                    for M in options(c, K, th):
                        KK = list(K); KK[th - 1] = M
                        lst.append(mid(c, tuple(KK), th))
                    opts.append(lst)
            Dopts[di] = opts
            di += 1
        while mi < len(Mlist):
            c, K, th = Mlist[mi]
            s = set()
            for (cc, perm, ringfree, filled) in moves(c, th, K[th - 1]):
                if filled:
                    s.add(-1); continue
                KK = [None, None, None]
                if ringfree:
                    for t in (1, 2, 3):
                        KK[perm[t] - 1] = K[t - 1]
                else:
                    KK[perm[th] - 1] = K[th - 1]
                s.add(did(cc, tuple(KK)))
            Msucc[mi] = tuple(s)
            mi += 1
        if len(Dlist) + len(Mlist) > max_nodes:
            return dict(aborted=True, dnodes=len(Dlist), mvnodes=len(Mlist))
    t1 = time.process_time()
    if verbose:
        print(f"  K - v: {C.n} vertices, ring {C.m}; unfilled {len(unf)}; D-nodes {len(Dlist)}, "
              f"move-nodes {len(Mlist)}; build {t1 - t0:.1f}s", flush=True)
    V = [INF] * len(Dlist)
    rounds = 0
    while True:
        rounds += 1
        A = [1 + min((0 if j < 0 else V[j]) for j in s) if s else INF for s in Msucc]
        Vn = []
        for opts in Dopts:
            best = INF
            for lst in opts:
                if not lst:
                    # adversary has no legal reveal (only possible for 'witnessed'):
                    # count it as an immediate player win, so the witnessed adversary
                    # stays weaker than the exact joint adversary
                    best = 0; continue
                best = min(best, max(A[i] for i in lst))
            Vn.append(min(best, INF))
        if Vn == V:
            break
        V = Vn
    t2 = time.process_time()
    U = {c: V[D[(c, empty)]] for c in unf}
    hist = {}
    for x in U.values():
        hist[x] = hist.get(x, 0) + 1
    red = all(x < INF for x in U.values())
    return dict(unfilled=len(unf), dnodes=len(Dlist), mvnodes=len(Mlist), reducible=red,
                depth=max(U.values()) if red else None,
                hist={('inf' if k >= INF else k): v for k, v in sorted(hist.items())},
                cpu_build=round(t1 - t0, 2), cpu_solve=round(t2 - t1, 2), rounds=rounds,
                _U=U, _C=C)


if __name__ == '__main__':
    import graphs
    which = sys.argv[1:] or ['T4', 'A3', 'pentakis']
    for w in which:
        w, _, rr = w.partition(':')
        rr = int(rr or 2)
        if w == 'T4':
            F, v = graphs.T4(), 4
        elif w.startswith('A'):
            F, v = graphs.A(int(w[1:])), 0
        elif w == 'pentakis':
            F, v = graphs.pentakis(), 0
        cfg = graphs.ball_config(F, v, rr)
        print(w, 'r =', rr, flush=True)
        r = solve_joint(cfg)
        print('  ', {k: x for k, x in r.items() if not k.startswith('_')}, flush=True)
