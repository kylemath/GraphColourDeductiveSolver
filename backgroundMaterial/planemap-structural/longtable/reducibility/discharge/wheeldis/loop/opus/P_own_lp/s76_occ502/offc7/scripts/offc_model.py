"""Python model of OffcLemma.lean's OffcOK (HOFFC7). Reads an offc rpatN file, rebuilds K from the
entry's own degree-d0 window (OFFC_SPEC sec 1-2, K's vertex set = phi's domain), builds K's rotation
in the RotOcc convention (Nx T (a) (rot a)[k+1] (rot a)[k]) from the own window's oriented faces,
and checks OffcOK(d, rot, phi, pat, eps) for eps in (+1, -1)."""
import sys, re, collections

def slot_parse(x):
    if x == 'u': return ('u', 0)
    return (x[0], int(x[1:]))

def wadj(d, five, x, y):
    """sec 1 adjacency on slots; five(i) -> bool or None (undetermined)."""
    (kx, i), (ky, j) = x, y
    if x == y: return False
    if kx == 'u' or ky == 'u':
        return (kx, ky) in (('u', 'w'), ('w', 'u'))
    if kx == 'w' and ky == 'w':
        return j == (i + 1) % d or i == (j + 1) % d
    if kx == 's' and ky == 'w': (kx, i), (ky, j) = y, x
    if kx == 'w' and ky == 's':   # w_i, s_j adjacent iff j = i or j + 1 = i
        return j == i or (j + 1) % d == i
    # s_i, s_j
    if j == (i + 1) % d: return five(j)
    if i == (j + 1) % d: return five(i)
    return False

def face0(d, five, x, y, z):
    (a, i), (b, j), (c, k) = x, y, z
    if (a, b, c) == ('u', 'w', 'w'): return k == (j + 1) % d
    if (a, b, c) == ('w', 'w', 's'): return i == (j + 1) % d and k == j
    if (a, b, c) == ('w', 's', 's'): return (j + 1) % d == i and k == i and five(i) is True
    return False

def face(d, five, x, y, z):
    return face0(d, five, x, y, z) or face0(d, five, y, z, x) or face0(d, five, z, x, y)

def letters_of_name(name):
    m = re.fullmatch(r'([a-z])(\d+)_([^_]+)_([^_]+)(?:_[01]+)?', name)
    assert m, name
    d0 = int(m.group(2)); L, S = m.group(3), m.group(4)
    assert len(L) == d0 and len(S) == d0, name
    return d0, L, S

def own_rot(name, verts):
    """K's rotation (RotOcc convention, ring slots as ('R',None)) from the own window, + degrees."""
    d0, L, S = letters_of_name(name)
    def letter(x):
        k, i = x
        if k == 'u': return d0
        c = (L if k == 'w' else S)[i]
        assert c in '5678', (name, x, c)
        return int(c)
    def five(i):
        return L[i] == '5' and ('w', i) in verts   # a w_i not in EX never gives an s-s edge
    deg = {x: letter(x) for x in verts}
    V = list(verts)
    adj = {x: set(y for y in V if wadj(d0, five, x, y)) for x in V}
    tris = set()
    for a in V:
        for b in adj[a]:
            for c in adj[a] & adj[b]:
                tris.add(frozenset((a, b, c)))
    # orient each triangle as a positive own-window face
    succ = {x: {} for x in V}   # T-rotation at a: b -> c
    for t in tris:
        a, b, c = list(t)
        if face(d0, five, a, b, c): o = (a, b, c)
        elif face(d0, five, a, c, b): o = (a, c, b)
        else: raise ValueError('%s: triangle %s is not an own-window face' % (name, sorted(t)))
        x, y, z = o
        for (p, q, r) in ((x, y, z), (y, z, x), (z, x, y)):
            assert q not in succ[p], (name, p, q)
            succ[p][q] = r
    rot = {}
    for a in V:
        nb = adj[a]; s = succ[a]
        assert set(s) <= nb and set(s.values()) <= nb
        starts = [b for b in nb if b not in s.values()]
        if not starts:   # full cycle
            b0 = sorted(nb)[0]; seq = [b0]
            while s[seq[-1]] != b0: seq.append(s[seq[-1]])
            assert len(seq) == len(nb) == deg[a], (name, a, seq, deg[a])
        else:
            assert len(starts) == 1, (name, a, 'fans', starts)
            seq = [starts[0]]
            while seq[-1] in s: seq.append(s[seq[-1]])
            assert len(seq) == len(nb), (name, a, 'edge in no triangle?')
            assert deg[a] > len(seq), (name, a)
            seq = seq + [('R', None)] * (deg[a] - len(seq))
        rot[a] = list(reversed(seq))   # RotOcc: Nx a rot[k+1] rot[k]
    return rot, deg, adj

def pat_of(link, sword):
    def pat(x):
        k, i = x
        if k == 'u': return 'free'
        c = (link if k == 'w' else sword)[i]
        if c in '5678': return ('exact', int(c))
        if c == 'N': return 'big'
        assert c == '.', c
        return 'free'
    return pat

def pfive(l):
    if l == 'free': return None
    if l == 'big': return False
    return l[1] == 5

def offc_ok(d, rot, phi, pat, eps):
    """OffcOK; returns list of failure strings (empty = pass)."""
    fails = []
    V = list(rot)
    fiveP = lambda i: pfive(pat(('w', i))) is True
    def padj(x, y):
        if x[0] == 's' and y[0] == 's':
            i, j = x[1], y[1]
            if j == (i + 1) % d: return pfive(pat(('w', j)))
            if i == (j + 1) % d: return pfive(pat(('w', i)))
            return False
        return wadj(d, lambda i: False, x, y)
    # (1) injective
    if len(set(phi[a] for a in V)) != len(V): fails.append('phi not injective')
    # (2) degrees
    for a in V:
        La = len(rot[a])
        if phi[a] == ('u', 0):
            if La != d: fails.append('deg u')
        elif pat(phi[a]) != ('exact', La): fails.append('letter at %s' % (phi[a],))
    # (3) induced
    for a in V:
        for b in V:
            if a == b: continue
            p = padj(phi[a], phi[b])
            if p is None: fails.append('undetermined pair %s %s' % (phi[a], phi[b])); continue
            if p != (b in rot[a]): fails.append('induced %s %s' % (phi[a], phi[b]))
    # (4) faces with one orientation
    for a in V:
        L = len(rot[a])
        for k in range(L):
            b, c = rot[a][(k + 1) % L], rot[a][k]
            if b[0] == 'R' or c[0] == 'R': continue
            ok = face(d, fiveP, phi[a], phi[b], phi[c]) if eps > 0 else face(d, fiveP, phi[a], phi[c], phi[b])
            if not ok: fails.append('face %s %s %s' % (phi[a], phi[b], phi[c]))
    # (5) one interior block
    for a in V:
        L = len(rot[a]); r = rot[a]
        if not any(x[0] != 'R' for x in r): fails.append('no interior slot')
        tr = sum(1 for k in range(L) if r[k][0] != 'R' and r[(k + 1) % L][0] == 'R')
        if tr > 1: fails.append('blocks at %s' % (a,))
    return fails

def main(path, dsel):
    out = []
    for line in open(path):
        if line.startswith('#') or not line.strip(): continue
        head, _, tail = line.partition(' # ')
        d, link, sword = head.split()
        d = int(d)
        if dsel and d not in dsel: continue
        src, name = tail.split()[:2]
        kv = dict(t.split('=', 1) for t in tail.split()[2:])
        phi = {}
        for pr in kv['phi'].split(','):
            x, y = pr.split('>')
            phi[slot_parse(x)] = slot_parse(y)
        rot, deg, adj = own_rot(name, set(phi))
        pat = pat_of(link, sword)
        res = {e: offc_ok(d, rot, phi, pat, e) for e in (1, -1)}
        good = [e for e in (1, -1) if not res[e]]
        out.append((d, link, sword, src, name, kv['d0'], good, res))
    return out

if __name__ == '__main__':
    path = sys.argv[1]
    dsel = set(int(x) for x in sys.argv[2].split(',')) if len(sys.argv) > 2 else None
    rows = main(path, dsel)
    cnt = collections.Counter()
    for d, link, sword, src, name, d0, good, res in rows:
        key = 'pass' if good else 'FAIL'
        cnt[(d, key, tuple(good))] += 1
        if not good:
            print('FAIL', d, link, sword, name, res[1][:3], res[-1][:3])
    for k in sorted(cnt): print(k, cnt[k])
