"""EXPLORE round 44 part B (Long Table, 20:00Z): receiver patterns from RSST containment, d = 7..11.
Host = the 1.5-ball the LP's receiver rows describe: u (exact degree d), w_0..w_{d-1}, s_0..s_{d-1} (s_i between w_i and
w_{i+1}).  Edges u-w_i, w_i-w_{i+1}, w_i-s_i, w_{i+1}-s_i always; s_{i-1}-s_i iff w_i = 5 (internal 6-connectivity: no
other edges or identifications among these 2d+1 vertices).  Faces (u,w_i,w_{i+1}), (w_i,w_{i+1},s_i), and
(w_i,s_{i-1},s_i) iff w_i = 5.
Containment as round 42 (RSST appearance): injective map of a configuration's interior into the host, exact degrees
(u = d; w/s slots 5..8, the LP's letter 9 is 'at least 9' and never an exact match), induced, interior triangles onto
faces.  Where the map uses both s_{i-1} and s_i, the configuration's adjacency between them fixes w_i to 5 or to not-5;
that requirement is part of the pattern even when w_i itself is not in the image.
Pattern = (d, {slot: letter set}), slot w_i = i, s_i = d + i, letter set as a 5-bit mask (bit v - 5), i.e. the NF section of
wlp3/sep3xf.  Dihedral images are identified (sep3x stores them all); a pattern implied by another is dropped.
usage: python3 gen44.py [VERDICTS]   (VERDICTS = rsst_verdicts.txt: only configs marked D2 or C2cons are used)
Writes pats44_all.txt (every pattern, with source configs), and with VERDICTS pats44.txt (registry-eligible, minimal)."""
import sys, os, collections
H = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(H, '..', 'k42'))
import grow
DS = range(7, 12)

def host(d):
    P = [('u',)] + [('w', i) for i in range(d)] + [('s', i) for i in range(d)]
    adj = {x: set() for x in P}; cond = {}
    def e(a, b): adj[a].add(b); adj[b].add(a)
    for i in range(d):
        e(('u',), ('w', i)); e(('w', i), ('w', (i + 1) % d)); e(('w', i), ('s', i)); e(('w', (i + 1) % d), ('s', i))
    for i in range(d): cond[frozenset((('s', (i - 1) % d), ('s', i)))] = i
    cadj = {x: set(adj[x]) for x in P}
    for pr in cond:
        a, b = tuple(pr); cadj[a].add(b); cadj[b].add(a)
    faces = set()
    for i in range(d):
        faces.add(frozenset((('u',), ('w', i), ('w', (i + 1) % d)))); faces.add(frozenset((('w', i), ('w', (i + 1) % d), ('s', i))))
    cfaces = {frozenset((('w', i), ('s', (i - 1) % d), ('s', i))): i for i in range(d)}
    return P, adj, cadj, cond, faces, cfaces

def embeddings(c, d, H_):
    """yield (image map, requirement {i: True (w_i = 5) / False (w_i != 5)})"""
    nm, tag, U, g, E, tri = c
    P, adj, cadj, cond, faces, cfaces = H_
    order = [max(U, key=lambda u: (len(E[u]), g[u]))]
    while len(order) < len(U):
        order.append(max((u for u in U if u not in order), key=lambda u: (len(E[u] & set(order)), g[u])))
    def ok(x, v): return g[x] == d if v == ('u',) else 5 <= g[x] <= 8
    phi = {}; used = set(); req = {}; out = []
    def rec(k):
        if k == len(order):
            r = dict(req)
            for x, v in phi.items():
                if v[0] == 'w' and v[1] in r and r[v[1]] != (g[x] == 5): return
            for t in tri:
                im = frozenset(phi[x] for x in t)
                if im in faces: continue
                if im in cfaces and r.get(cfaces[im]) is True: continue
                return
            out.append((dict(phi), r)); return
        x = order[k]; pl = [y for y in order[:k] if y in E[x]]
        cand = set.intersection(*[cadj[phi[y]] for y in pl]) if pl else set(P)
        for v in cand:
            if v in used or not ok(x, v): continue
            new = []; bad = False
            for y in order[:k]:
                pr = frozenset((phi[y], v)); want = y in E[x]
                if pr in cond:
                    i = cond[pr]
                    if i in req:
                        if req[i] != want: bad = True; break
                    else: new.append(i); req[i] = want
                elif (phi[y] in adj[v]) != want: bad = True; break
            if not bad:
                phi[x] = v; used.add(v); rec(k + 1); del phi[x]; used.discard(v)
            for i in new: del req[i]
    if all(any(ok(x, v) for v in P) for x in U): rec(0)
    return out

def pattern(d, c, phi, r):
    g = c[3]; F = {}
    for x, v in phi.items():
        if v == ('u',): continue
        F[v[1] if v[0] == 'w' else d + v[1]] = 1 << (g[x] - 5)
    for i, five in r.items():
        if i not in F: F[i] = 1 if five else 30
    return tuple(sorted(F.items()))

def images(d, F):
    out = []
    for refl in (0, 1):
        for rr in range(d):
            Q = []
            for sl, m in F:
                isS = sl >= d; i = sl - d if isS else sl
                j = ((2 * d - i - 1) % d if isS else (d - i) % d) if refl else i
                j = (j + rr) % d; Q.append((d + j if isS else j, m))
            out.append(tuple(sorted(Q)))
    return out
def canon(d, F): return min(images(d, F))
def implies(B, A, d):
    """every row matching B matches some image of A"""
    Bd = dict(B)
    return any(all(sl in Bd and (Bd[sl] & ~m) == 0 for sl, m in Q) for Q in images(d, A))
def minimal(d, Fs):
    Fs = sorted(set(Fs), key=lambda F: (len(F), F)); keep = []
    for F in Fs:
        if not any(implies(F, A, d) for A in keep): keep.append(F)
    return keep

def matches(d, F, lk, sv):
    """row (link word, s word; letters 5..9) contains pattern F"""
    let = [int(ch) for ch in lk] + [int(ch) for ch in sv]
    return any(all((m >> (let[sl] - 5)) & 1 for sl, m in Q) for Q in images(d, F))

def fmt(d, F): return '%d %d %s' % (d, len(F), ' '.join('%d %d' % sm for sm in F))
def word(d, F):
    """readable form: link_s with letters, '.' free, 'n' = not 5, '[..]' other sets"""
    Fd = dict(F); out = []
    for off in (0, d):
        s = ''
        for i in range(d):
            m = Fd.get(off + i)
            if m is None: s += '.'
            elif m == 30: s += 'n'
            elif bin(m).count('1') == 1: s += str(5 + m.bit_length() - 1)
            else: s += '[' + ''.join(str(5 + b) for b in range(5) if (m >> b) & 1) + ']'
        out.append(s)
    return '_'.join(out)

if __name__ == '__main__':
    C = grow.rsst(); assert len(C) == 633
    kcn = [l.split()[0] for l in open(os.path.join(H, 'rsst.txt')) if l.strip()]
    assert all(n.startswith(c[0] + '_') for n, c in zip(kcn, C))
    C = [(n,) + tuple(c[1:]) for n, c in zip(kcn, C)]
    allp = collections.defaultdict(set)        # (d, canon F) -> {config}
    per = collections.Counter()
    for d in DS:
        H_ = host(d)
        for c in C:
            for phi, r in embeddings(c, d, H_):
                allp[(d, canon(d, pattern(d, c, phi, r)))].add(c[0]); per[(c[0], d)] += 1
    with open(os.path.join(H, 'pats44_all.txt'), 'w') as o:
        o.write('# every RSST containment pattern in the d-receiver 1.5-ball, d = 7..11: NF line | readable | configs\n')
        for (d, F) in sorted(allp, key=lambda k: (k[0], len(k[1]), k[1])):
            o.write('%s | %s | %s\n' % (fmt(d, F), word(d, F), ' '.join(sorted(allp[(d, F)]))))
    print('patterns (all configs): %s' % {d: sum(1 for k in allp if k[0] == d) for d in DS})
    print('configs with an embedding: %d' % len({c for c, d in per}))
    if len(sys.argv) > 1:
        ok = {l.split()[0] for l in open(sys.argv[1]) if not l.startswith('#') and ('verdict=D2' in l.split() or 'verdict=C2cons' in l.split())}
        assert ok, 'no eligible configurations read from ' + sys.argv[1]
        with open(os.path.join(H, 'pats44.txt'), 'w') as o:
            o.write('# RSST containment patterns, d = 7..11, from configurations verified on two engines (D, or C with a shared\n'
                    '# conservative X); inclusion-minimal up to dihedral images.  NF line (d k slot mask ...) | readable | configs\n')
            tot = 0
            for d in DS:
                Fs = [F for (dd, F), cs in allp.items() if dd == d and cs & ok]
                keep = minimal(d, Fs); tot += len(keep)
                for F in keep:
                    o.write('%s | %s | %s\n' % (fmt(d, F), word(d, F), ' '.join(sorted(allp[(d, F)] & ok))))
                print('d=%d: %d eligible patterns, %d minimal' % (d, len(Fs), len(keep)))
