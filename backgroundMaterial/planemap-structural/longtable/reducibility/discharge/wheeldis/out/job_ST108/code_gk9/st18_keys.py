"""Stage 18 hat channel H5 (RELAY_SPEC section 15, 8f71209b): Studio's key reader, written from the spec alone, and the
both-ends consistency test on random triangulations (no Opus code).
K = min(side(x) + side(y), side(y) + side(x)) for a five v, consecutive spokes x, y, and big hat b of v between them:
  side(z) = (5, c2(Z1), letter(Z2)) if z = 5;  (6, c2(Z1), c2(Zo)) if z = 6;  (z,) if z >= 7;  c2: 5,6 -> 0, big -> 1.
Three readings of the same diamond are compared:
  (P) physical: from rotation systems, z's rotation read as (v, other spoke, b, Z1, Z2) / (v, other spoke, b, Z1, Zo, Z2);
  (S) sender-row formula (spec 15 table): from v's link w, hat classes H and fan classes F, z = w_k, other spoke w_{k+1};
  (R) receiver-row formula: from b's link w and apexes s, z = w_i, other spoke w_{i+1}, s_i = v.
Frames: explore's grow.py build2 (u = b; random link letters 5..9, random second-ring letters, U = d in 7..9), every
apex five s_i of u is a test diamond; (S) uses both orientations of v's rotation.
Usage: python3 out/job31/st18_keys.py [N=3000 frames]"""
import os, sys, random, collections
HERE = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
def c2(l): return 1 if l >= 7 else 0

def side(z, a, bq):
    """z's letter, then (Z1, Z2) for a five or (Z1, Zo) for a six, as letters; returns the spec side tuple."""
    if z == 5: return (5, c2(a), bq)
    if z == 6: return (6, c2(a), c2(bq))
    return (z,)
def K_of(sx, sy): return min(sx + sy, sy + sx)

def key_sender(w, H, F, k):
    """sender-row formula: five with link w (5 letters), hat classes H[0..4] (H[m] between w_m and w_{m+1}), fan classes
    F[m] for six spokes; hat b at k (between w_k and w_{k+1})."""
    x, y = w[k], w[(k + 1) % 5]
    if x == 5: sx = (5, H[(k - 1) % 5], w[(k - 1) % 5])
    elif x == 6: sx = (6, F[k], H[(k - 1) % 5])
    else: sx = (x,)
    if y == 5: sy = (5, H[(k + 1) % 5], w[(k + 2) % 5])
    elif y == 6: sy = (6, F[(k + 1) % 5], H[(k + 1) % 5])
    else: sy = (y,)
    return K_of(sx, sy)
def key_receiver(w, s, i):
    """receiver-row formula: big with link w, apexes s (s_i between w_i and w_{i+1}), apex five s_i."""
    d = len(w); W = lambda q: w[q % d]; S = lambda q: s[q % d]
    x, y = W(i), W(i + 1)
    sx = (5, c2(W(i - 1)), S(i - 1)) if x == 5 else (6, c2(W(i - 1)), c2(S(i - 1))) if x == 6 else (x,)
    sy = (5, c2(W(i + 2)), S(i + 1)) if y == 5 else (6, c2(W(i + 2)), c2(S(i + 1))) if y == 6 else (y,)
    return K_of(sx, sy)

if __name__ == '__main__':
    N = int(next((a[2:] for a in sys.argv[1:] if a.startswith('N=')), '3000'))
    G = {'__file__': os.path.join(HERE, 'loop', 'k42', 'grow.py'), '__name__': 'grow'}
    exec(open(G['__file__']).read(), G)
    random.seed(18)
    def rotation(adj, tri, h):
        nb = adj[h]; nxt = collections.defaultdict(set)
        for t in tri:
            if h in t:
                a, b = sorted(t - {h}); nxt[a].add(b); nxt[b].add(a)
        if any(len(nxt[x]) != 2 for x in nb): return None
        cyc = [min(nb)]; prev = None
        while True:
            c = sorted(nxt[cyc[-1]] - ({prev} if prev is not None else set()))
            c = [y for y in c if y not in cyc[1:]] or c
            if c[0] == cyc[0]: break
            prev = cyc[-1]; cyc.append(c[0])
            if len(cyc) > len(nb): return None
        return cyc if len(cyc) == len(nb) else None
    def apex(adj, tri, c, p, q):
        z = [x for x in adj[p] & adj[q] if x != c and frozenset((p, q, x)) in tri]
        return z[0] if len(z) == 1 else None
    tested = mm_SR = mm_SP = mm_RP = mm_refl = skipped = 0; byshape = collections.Counter()
    for _ in range(N):
        d = random.choice((7, 8, 9)); LK = [random.choice((5, 5, 6, 6, 6, 7, 8, 9)) for _ in range(d)]
        SV = {i: random.choice((5, 5, 6, 6, 7, 8, 9)) for i in range(d)}
        G['D'] = d; G['LK'] = LK; G['SV'] = SV
        r2 = {('s', i): SV[i] for i in range(d)}
        priv = {}
        adj, name, faces = G['build2'](r2)
        inv = {x: v for v, x in name.items()}
        let = {}
        for v_, x in name.items():
            if x == ('u',): let[v_] = d
            elif x[0] == 'w': let[v_] = LK[x[1]]
            elif x[0] == 's': let[v_] = SV[x[1]]
            elif x[0] == 'p': let[v_] = random.choice((5, 6, 7, 8, 9))
        for v_ in adj:   # ring-3 vertices (unnamed): random letters, as any frame vertex
            if v_ not in let: let[v_] = random.choice((5, 6, 7, 8, 9))
        tri = set(faces)
        u = inv[('u',)]
        for i in range(d):
            if SV[i] != 5: continue
            v = inv[('s', i)]; x, y = inv[('w', i)], inv[('w', (i + 1) % d)]
            rv = rotation(adj, tri, v)
            if rv is None or len(rv) != 5 or any(q not in let for q in rv): skipped += 1; continue
            # (R) receiver formula from u's arrangement
            Kr = key_receiver(LK, [SV[q] for q in range(d)], i)
            # (P) physical: read each spoke z's rotation starting at v, then the other spoke, then b = u
            def phys_side(z, other):
                rz = rotation(adj, tri, z)
                if rz is None: return None
                n = len(rz); j = rz.index(v)
                for step in (1, -1):
                    seq = [rz[(j + step * t) % n] for t in range(n)]
                    if seq[1] == other and seq[2] == u: break
                else: return None
                if any(q not in let for q in seq): return None
                lz = let[z]
                if lz == 5: return side(5, let[seq[3]], let[seq[4]])          # (v, other, b, Z1, Z2)
                if lz == 6: return side(6, let[seq[3]], let[seq[4]])          # (v, other, b, Z1, Zo, Z2)
                return (lz,)
            sx, sy = phys_side(x, y), phys_side(y, x)
            if sx is None or sy is None: skipped += 1; continue
            Kp = K_of(sx, sy)
            # (S) sender formula from v's own link / hats / fans, both orientations of v's rotation
            Ks = []
            for orient in (rv, rv[::-1]):
                w5 = [let[q] for q in orient]
                H = [c2(let[apex(adj, tri, v, orient[m], orient[(m + 1) % 5])]) if apex(adj, tri, v, orient[m], orient[(m + 1) % 5]) in let else None for m in range(5)]
                F = [None] * 5
                for m in range(5):
                    if w5[m] == 6:   # fan: in spoke l_m's wheel (v, l_{m+1}, h_m, f_m, h_{m-1}, l_{m-1}), the vertex opposite v
                        rz = rotation(adj, tri, orient[m]); jj = rz.index(v) if rz else None
                        F[m] = c2(let[rz[(jj + 3) % 6]]) if rz and len(rz) == 6 and rz[(jj + 3) % 6] in let else None
                kk = next(m for m in range(5) if {orient[m], orient[(m + 1) % 5]} == {x, y})
                if None in (H[(kk - 1) % 5], H[(kk + 1) % 5]) or (w5[kk] == 6 and F[kk] is None) or (w5[(kk + 1) % 5] == 6 and F[(kk + 1) % 5] is None):
                    Ks.append(None); continue
                Ks.append(key_sender(w5, H, F, kk))
            if None in Ks: skipped += 1; continue
            tested += 1; byshape[(LK[i], LK[(i + 1) % d])] += 1
            mm_refl += Ks[0] != Ks[1]; mm_SR += Ks[0] != Kr; mm_SP += Ks[0] != Kp; mm_RP += Kr != Kp
    print('both-ends key test: %d diamonds from %d random frames (skipped %d with a needed vertex outside the built ball)' % (tested, N, skipped))
    print('  spoke shapes tested (x, y letters): %d kinds, e.g. %s' % (len(byshape), dict(list(sorted(byshape.items()))[:8])))
    print('  mismatches: sender vs receiver %d, sender vs physical %d, receiver vs physical %d, sender orientation (reflection) %d'
          % (mm_SR, mm_SP, mm_RP, mm_refl))
    # broken-key control: receiver reads s_{i+1} where it should read s_{i-1}
    bad = 0; tot = 0
    random.seed(19)
    for _ in range(20000):
        d = random.choice((7, 8, 9)); w = [random.choice((5, 6, 7, 8, 9)) for _ in range(d)]; s = [random.choice((5, 6, 7, 8, 9)) for _ in range(d)]
        for i in range(d):
            if s[i] != 5: continue
            s2 = list(s); s2[(i - 1) % d], s2[(i + 1) % d] = s[(i + 1) % d], s[(i - 1) % d]
            tot += 1; bad += key_receiver(w, s, i) != key_receiver(w, s2, i)
    print('  broken-key control (s_{i-1} and s_{i+1} swapped at the receiver): %d of %d keys change' % (bad, tot))
