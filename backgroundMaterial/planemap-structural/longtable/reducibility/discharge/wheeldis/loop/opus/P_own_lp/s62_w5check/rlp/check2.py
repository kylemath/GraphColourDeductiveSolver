# Second method.  (a) strict K1: for each of the 3 keys, engine q7sig/q7keys at every cert slot, then the privates the key
# forces there and the engine masks.  (b) K2 by edge-overlap consistency (no completion enumeration), compared with price77.
import itertools, collections
import price77 as P
ns = P.ns; q7sig = ns['q7sig']; q7keys = ns['q7keys']
KEYS3 = [(7, 6, 6, 5, 5, 5, 7), (7, 5, 5, 5, 6, 6, 7), (7, 5, 7, 5, 5, 6, 6)]
print('(a) strict K1, engine q7keys + masks')
for K in KEYS3:
    hits = []
    for b, j in P.SL:
        w, s = P.rows[b]; n = 7
        sg = q7sig(7, w[(j + 1) % n], s[j], s[(j - 1) % n], w[(j - 1) % n])
        if tuple(K) not in q7keys(sg): continue
        # orientation(s) in which slot reads K: L = (7, w[j+1], s[j], p1, p2, s[j-1], w[j-1])
        for L in (K, (K[0],) + tuple(reversed(K[1:]))):
            if (L[1], L[2], L[5], L[6]) == (w[(j + 1) % n], s[j], s[(j - 1) % n], w[(j - 1) % n]):
                m1, m2 = P.mask(w, s, j, 1), P.mask(w, s, j, -1)
                ok = (m1 is None or L[3] in m1) and (m2 is None or L[4] in m2)
                hits.append((P.names[b], j, 'p1=%d p2=%d' % (L[3], L[4]), 'mask+', m1, 'mask-', m2, 'ALLOWED' if ok else 'excluded'))
    print(' key', ''.join(map(str, K)), 'lenient-compatible slots:', len(hits))
    for h in hits: print('    ', *h)
print('(b) K2 by overlap consistency')
def overlap_ok(a, i, b, j, strict):
    (wa, sa), (wb, sb) = P.rows[a], P.rows[b]; n = 7
    A = lambda k: wa[(i + k) % n]; AS = lambda k: sa[(i + k) % n]; B = lambda k: wb[(j + k) % n]; BS = lambda k: sb[(j + k) % n]
    for o in (1, -1):    # o = +1: A's +1 side faces B's +1 side
        Ao = lambda k: A(o * k); ASo = lambda k: AS(k) if o == 1 else AS(-k - 1)
        if A(0) != 7 or B(0) != 7: return False   # B's letter in A's link and A's letter in B's link (both degree 7)
        c = [Ao(1) == B(1), Ao(-1) == B(-1), Ao(2) == BS(0), Ao(-2) == BS(-1), ASo(0) == B(2), ASo(-1) == B(-2)]
        if B(1) == 5: c.append(ASo(1) == BS(1))
        if B(-1) == 5: c.append(ASo(-2) == BS(-2))
        if strict:
            m1, m2 = P.mask(wb, sb, j, 1), P.mask(wb, sb, j, -1)
            c.append(m1 is None or Ao(3) in m1); c.append(m2 is None or Ao(-3) in m2)
        if all(c): return True
    return False
for mode in ('lenient', 'strict'):
    P.MODE = mode; opts, adj, mt = P.match(2)
    agree = 0; dis = []
    for e, (a, i, k1, k2) in enumerate(P.EM):
        s1 = set(adj[e]); s2 = {sl for sl in P.SL if overlap_ok(a, i, sl[0], sl[1], mode == 'strict')}
        if s1 == s2: agree += 1
        else: dis.append((P.names[a], i, s1, s2))
    print(' ', mode, 'K2 compatible-slot sets agree for %d of %d emissions; matched %d' % (agree, len(P.EM), len(mt)), dis[:3])
