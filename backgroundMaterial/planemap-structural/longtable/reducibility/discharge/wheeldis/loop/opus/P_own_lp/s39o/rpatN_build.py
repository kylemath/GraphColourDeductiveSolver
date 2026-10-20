"""s39o rpatN builder (Opus P_own_lp, round s39o).  From a kc file (explore's round-55 row55_hits_kc.txt: the 35 configurations
of the 2026 set that sit wholly inside 27 of the 45 A67 binders, each two-engine D in loop/k53/N54_res.txt / N54_kcc.out / N54_df.out)
build u-centred whole-window patterns for the stacked engine (option rpatN=FILE, OFFC_SPEC.md section 3).

kc line: NAME r m RINGNB INTNB ; vertex v = 0..m-1, RINGNB[v] = its ring neighbours (';'-separated, '-' none), INTNB[v] = its
interior neighbours.  deg(v) = |ring nb| + |interior nb|.  Interior triangles = 3-cliques of the interior graph.

Window of a row of degree d (OFFC_SPEC section 1): u; w_0..w_{d-1}; s_0..s_{d-1}; edges u-w_i, w_i-w_{i+1}, w_i-s_i, w_{i+1}-s_i,
s_{i-1}-s_i iff w_i = 5; faces u w_i w_{i+1}, w_i w_{i+1} s_i, w_i s_{i-1} s_i (w_i = 5).  An embedding (round-42/44 matcher, as
explore's grow.embeddings): injective, every image exact with degree = the configuration degree (letter 9 never exact), induced
(adjacent iff adjacent) among the images, every interior triangle onto a face.

For every configuration and every vertex c of degree d in 7..DMAX, every embedding with c -> u is enumerated; it becomes the pattern
{image slot: {its letter}} plus, for every w_i with both s_{i-1}, s_i images and w_i not an image, w_i in {5} (configuration edge) or
{6,7,8,9} (configuration non-edge; written N).  Every other slot is free.  Output: one line per distinct pattern:
  d LINK SWORD # NAME c=v      (LINK/SWORD chars: 5 6 7 8 exact, N = not 5, . = free)
usage: python3 rpatN_build.py KCFILE OUT [dmax=17]"""
import sys, itertools, collections

def kc(line):
    f = line.split(); m = int(f[2]); rp = f[3].split(';'); ip = f[4].split(';')
    assert len(rp) == m and len(ip) == m, f[0]
    E = {v: (set() if ip[v] == '-' else {int(x) for x in ip[v].split(',')}) for v in range(m)}
    for v in E:
        for x in E[v]: assert v in E[x], (f[0], v, x)
    g = {v: len(E[v]) + (0 if rp[v] == '-' else len(rp[v].split(','))) for v in range(m)}
    tri = {frozenset((a, b, c)) for a in range(m) for b in E[a] for c in E[a] & E[b] if a < b < c}
    return f[0], m, E, g, tri

def wadj(d, x, y, wl):
    """window adjacency of slots x, y given w letters wl (dict i -> letter or None = not an image).  Returns True/False, or
    ('w', i) when it is s_{i-1}-s_i with w_i not an image (adjacent iff w_i = 5)."""
    if x > y: x, y = y, x
    if x == ('u',) or y == ('u',):
        o = y if x == ('u',) else x
        return o[0] == 'w'
    if x[0] == 'w' and y[0] == 'w': return (x[1] - y[1]) % d in (1, d - 1)
    if x[0] == 's' and y[0] == 's':
        if (x[1] - y[1]) % d == 1: i = x[1]
        elif (y[1] - x[1]) % d == 1: i = y[1]
        else: return False
        L = wl.get(i)                     # s_{i-1}-s_i shares w_i
        return ('w', i) if L is None else (L == 5)
    w, s = (x, y) if x[0] == 'w' else (y, x)
    return s[1] in (w[1], (w[1] - 1) % d)

def embeddings_c(conf, c, d):
    nm, m, E, g, tri = conf
    slots = [('w', i) for i in range(d)] + [('s', i) for i in range(d)]
    order = [c]
    while len(order) < m:
        order.append(max((v for v in range(m) if v not in order), key=lambda v: (len(E[v] & set(order)), g[v], -v)))
    phi = {c: ('u',)}; out = []
    def wl():
        return {s_[1]: g[v] for v, s_ in phi.items() if s_[0] == 'w'}
    def rec(k):
        if k == m:
            L = wl(); cons = {}
            vs = list(phi)
            for a, b in itertools.combinations(vs, 2):
                r = wadj(d, phi[a], phi[b], L)
                want = b in E[a]
                if isinstance(r, tuple):
                    cons[r] = frozenset((5,)) if want else frozenset((6, 7, 8, 9))
                elif r != want: return
            for t in tri:   # every interior triangle onto a face
                im = sorted(phi[v] for v in t)
                if not face(d, im, L, cons): return
            out.append((dict(phi), cons)); return
        v = order[k]
        for s_ in slots:
            if s_ in phi.values(): continue
            if not (5 <= g[v] <= 8): return          # an image is exact: letter 9 never exact, w/s letters 5..9
            # induced against already placed: decided pairs only (s-s via a non-image w is settled at the end)
            L = {s2[1]: g[x] for x, s2 in phi.items() if s2[0] == 'w'}
            if s_[0] == 'w': L[s_[1]] = g[v]
            bad = False
            for x, sx in phi.items():
                r = wadj(d, s_, sx, L)
                if isinstance(r, tuple): continue
                if r != (x in E[v]): bad = True; break
            if bad: continue
            phi[v] = s_; rec(k + 1); del phi[v]
    rec(1)
    return out

def face(d, im, L, cons):
    S = set(im)
    if ('u',) in S:
        ws = sorted(x[1] for x in S if x[0] == 'w')
        return len(ws) == 2 and (ws[0] - ws[1]) % d in (1, d - 1)
    ws = [x[1] for x in S if x[0] == 'w']; ss = [x[1] for x in S if x[0] == 's']
    if len(ws) == 2 and len(ss) == 1:
        a, b = ws
        if (a - b) % d == 1: a, b = b, a
        return (b - a) % d == 1 and ss[0] == a
    if len(ws) == 1 and len(ss) == 2:
        i = ws[0]; return set(ss) == {(i - 1) % d, i} and L.get(i) == 5
    return False

def pattern(d, phi, cons, g):
    lk = ['.'] * d; sv = ['.'] * d
    for v, s_ in phi.items():
        if s_[0] == 'w': lk[s_[1]] = str(g[v])
        elif s_[0] == 's': sv[s_[1]] = str(g[v])
    for (_, i), S in cons.items():
        assert lk[i] == '.'
        lk[i] = '5' if S == frozenset((5,)) else 'N'
    return ''.join(lk), ''.join(sv)

if __name__ == '__main__':
    KC, OUT = sys.argv[1], sys.argv[2]
    DM = int(dict(a.split('=') for a in sys.argv[3:]).get('dmax', '17'))
    lines = [l.rstrip('\n') for l in open(KC) if l.strip()]
    out = []; seen = set(); stat = collections.Counter()
    for l in lines:
        conf = kc(l); nm, m, E, g, tri = conf
        for c in range(m):
            d = g[c]
            if d < 7 or d > DM: continue
            stat['centres'] += 1
            es = embeddings_c(conf, c, d)
            for phi, cons in es:
                lk, sv = pattern(d, phi, cons, g)
                stat['N/5 constrained w'] += len(cons)
                # canonical up to the 2d rotations / reflections (w_i -> w_{-i}, s_i -> s_{-i-1}) so the file is small
                cands = []
                for r in range(d):
                    for refl in (0, 1):
                        L2 = [lk[(r - i) % d] if refl else lk[(i + r) % d] for i in range(d)]
                        S2 = [sv[(r - i - 1) % d] if refl else sv[(i + r) % d] for i in range(d)]
                        cands.append((''.join(L2), ''.join(S2)))
                key = (d, min(cands))
                if key in seen: continue
                seen.add(key); out.append('%d %s %s # %s c=%d' % (d, key[1][0], key[1][1], nm, c))
            stat['embeddings'] += len(es)
    with open(OUT, 'w') as f:
        f.write('# rpatN (s39o): u-centred whole-window patterns from %s (%d configurations); d LINK SWORD, 5-8 exact, N = not 5, . free\n' % (KC.split('/')[-1], len(lines)))
        f.write('\n'.join(out) + '\n')
    print('rpatN: %d configurations, %s, %d distinct patterns (up to rotation/reflection) -> %s' % (len(lines), dict(stat), len(out), OUT))
