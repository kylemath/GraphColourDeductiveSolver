"""RELAY_SPEC_s39o 39.2 / 39.6 (rpatN3), Studio's own build from the spec text alone (no Opus code): u-centred
whole-window raw patterns from kc lines `NAME r m RINGNB INTNB` (degree = |ring| + |interior|).
Window of degree d (39.1): u, w_0..w_{d-1}, s_0..s_{d-1}; edges u-w_i, w_i-w_{i+1}, w_i-s_i, w_{i+1}-s_i, and s_{i-1}-s_i
iff w_i = 5; faces u w_i w_{i+1}, w_i w_{i+1} s_i, and w_i s_{i-1} s_i iff w_i = 5 (every 3-cycle of the window is a face,
so "interior 3-cliques land on faces" follows from the induced condition and is still checked).
For each configuration vertex c with 7 <= deg(c) <= 17: every embedding with c -> u in the degree-deg(c) window,
injective, every other image an exact letter 5..8 equal to its degree (a 9 is never exact), induced (configuration edges
= window edges among the images), interior 3-cliques onto faces. c's configuration neighbours go to w slots, the rest to
s slots. Pattern: image slots get their letters; a non-image w_i between image s_{i-1}, s_i gets 5 (configuration edge
s_{i-1}-s_i) or N (no edge); everything else '.'. Patterns deduped up to the 2d rotations / reflections
(w_i -> w_{i+r}, s_i -> s_{i+r}; w_i -> w_{-i}, s_i -> s_{-i-1}); canonical form = min of LINK + SWORD.
Usage: python3 out/job31/rpatN_studio.py KCFILE OUT  (writes 'd LINK SWORD # name c=v' lines, one per pattern)"""
import sys, collections

def parse(line):
    f = line.split(); nm, r, m = f[0], int(f[1]), int(f[2]); rp, ip = f[3].split(';'), f[4].split(';')
    E = {u: set() if ip[u] == '-' else {int(x) for x in ip[u].split(',')} for u in range(m)}
    g = {u: len(E[u]) + (0 if rp[u] == '-' else len(rp[u].split(','))) for u in range(m)}
    tri = {frozenset((a, b, c)) for a in range(m) for b in E[a] for c in E[a] & E[b] if a < b < c}
    return nm, m, g, E, tri

def canon(d, L, S):
    best = None
    for refl in (False, True):
        for r in range(d):
            if refl: L2 = [L[(r - i) % d] for i in range(d)]; S2 = [S[(r - i - 1) % d] for i in range(d)]
            else: L2 = [L[(i + r) % d] for i in range(d)]; S2 = [S[(i + r) % d] for i in range(d)]
            k = ''.join(L2) + ' ' + ''.join(S2)
            if best is None or k < best: best = k
    return best

def embeddings(m, g, E, tri, c):
    """yield (d, LINK list, SWORD list) for every embedding with c -> u"""
    d = g[c]; nb = sorted(E[c]); rest = [v for v in range(m) if v != c and v not in E[c]]
    if any(not 5 <= g[v] <= 8 for v in range(m) if v != c): return
    if len(nb) > d or len(rest) > d: return
    pos = {}   # v -> ('w', i) or ('s', i)
    def adj_window(a, b, wlet):
        """window adjacency of slots a, b given the letters of image w's (wlet: i -> letter); returns True / False / None
        (None = s_{i-1}-s_i with w_i not an image: free, decided by the pattern)"""
        (ka, ia), (kb, ib) = a, b
        if ka == 'w' and kb == 'w': return (ia - ib) % d in (1, d - 1)
        if ka == 's' and kb == 'w': (ka, ia), (kb, ib) = b, a
        if ka == 'w' and kb == 's': return ib == ia or ib == (ia - 1) % d
        # both s
        if (ib - ia) % d == 1: wi = ib
        elif (ia - ib) % d == 1: wi = ia
        else: return False
        if wi in wlet: return wlet[wi] == 5
        return None
    order = nb + rest
    def rec(k, usedw, useds):
        if k == len(order):
            wlet = {pos[v][1]: g[v] for v in nb}
            L = ['.'] * d; S = ['.'] * d
            for v in nb: L[pos[v][1]] = str(g[v])
            for v in rest: S[pos[v][1]] = str(g[v])
            sl = {pos[v][1]: v for v in rest}
            for i in range(d):   # non-image w_i between image s_{i-1}, s_i
                if i not in wlet and (i - 1) % d in sl and i in sl:
                    L[i] = '5' if sl[i] in E[sl[(i - 1) % d]] else 'N'
            # faces: every interior 3-clique must be a window face
            for t in tri:
                if c in t: continue   # u-triangles: u w_i w_{i+1} are faces once induced
                ws = [pos[v][1] for v in t if pos[v][0] == 'w']; ss = [pos[v][1] for v in t if pos[v][0] == 's']
                if len(ws) == 2:   # face w_i w_{i+1} s_i
                    if not (len(ss) == 1 and set(ws) == {ss[0], (ss[0] + 1) % d}): return
                elif len(ws) == 1:   # face w_i s_{i-1} s_i with w_i = 5
                    if not (set(ss) == {(ws[0] - 1) % d, ws[0]} and L[ws[0]] == '5'): return
                else: return
            yield (d, L, S); return
        v = order[k]; isn = v in E[c]
        for i in range(d):
            if (isn and i in usedw) or (not isn and i in useds): continue
            if isn and k == 0 and i != 0: continue   # rotation: the first neighbour sits at w_0 (dedup covers the rest)
            slot = ('w', i) if isn else ('s', i)
            wlet = {pos[x][1]: g[x] for x in pos if pos[x][0] == 'w'}
            if isn: wlet[i] = g[v]
            ok = True
            for x, sx in pos.items():
                a = adj_window(slot, sx, wlet); e = x in E[v]
                if a is None: continue
                if a != e: ok = False; break
            if ok:   # s-s pairs fixed by a newly placed w
                if isn:
                    sl = {pos[x][1]: x for x in pos if pos[x][0] == 's'}
                    if (i - 1) % d in sl and i in sl and ((sl[i] in E[sl[(i - 1) % d]]) != (g[v] == 5)): ok = False
            if not ok: continue
            pos[v] = slot
            (usedw if isn else useds).add(i)
            yield from rec(k + 1, usedw, useds)
            (usedw if isn else useds).discard(i); del pos[v]
    if not nb: return
    yield from rec(0, set(), set())

if __name__ == '__main__':
    KC, OUT = sys.argv[1], sys.argv[2]
    pats = {}; nconf = ncent = nemb = 0; withemb = 0; pairs = set(); nocentre = 0
    for line in open(KC):
        if not line.strip(): continue
        nm, m, g, E, tri = parse(line)
        cents = [c for c in range(m) if 7 <= g[c] <= 17]
        nconf += 1
        if not cents: nocentre += 1; continue
        got = False
        for c in cents:
            ncent += 1
            for d, L, S in embeddings(m, g, E, tri, c):
                nemb += 1; got = True; k = (d, canon(d, L, S)); pairs.add((nm, k))
                pats.setdefault(k, (nm, c))
        withemb += got
    with open(OUT, 'w') as fo:
        fo.write('# rpatN (Studio, RELAY_SPEC_s39o 39.2 / 39.6): u-centred whole-window patterns from %s; d LINK SWORD\n' % KC)
        for (d, k), (nm, c) in sorted(pats.items()):
            fo.write('%d %s # %s c=%d\n' % (d, k, nm, c))
    byd = collections.Counter(d for d, _ in pats)
    print('configurations %d; no centre %d; with >= 1 u-centred embedding %d; centres tried %d; embeddings (first neighbour at w_0) %d; '
          '(configuration, pattern) pairs %d; patterns %d; by d %s' % (nconf, nocentre, withemb, ncent, nemb, len(pairs), len(pats), dict(sorted(byd.items()))))
