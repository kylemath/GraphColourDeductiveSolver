"""Round 54d count check: duplicates in the 2026 set under a canonical form (BFS code over interior darts, both
orientations). usage: python3 -I dup54.py CONFDIR"""
import sys, os, glob, collections
def parse(fn):
    L = open(fn).read().split('\n'); n, r = map(int, L[1].split()[:2]); nb = {}
    for l in L[2:]:
        f = l.split()
        if f: nb[int(f[0])] = [int(x) for x in f[2:]]
    return r, nb
def code(r, nb, u0, j0, d):
    lab = {u0: 0}; order = [u0]; ref = {u0: nb[u0][j0]}; out = []; k = 0
    while k < len(order):
        v = order[k]; k += 1
        if v <= r: continue
        rot = nb[v]; i = rot.index(ref[v]); m = len(rot); row = [m]
        for t in range(m):
            w = rot[(i + d * t) % m]
            if w not in lab:
                lab[w] = len(lab); order.append(w)
                if w > r: ref[w] = v
            row.append((lab[w], w <= r))
        out.append(tuple(row))
    return tuple(out)
def canon(r, nb, refl):
    best = None
    for u in nb:
        for j in range(len(nb[u])):
            for d in ((1, -1) if refl else (1,)):
                c = code(r, nb, u, j, d)
                if best is None or c < best: best = c
    return best
fs = sorted(glob.glob(os.path.join(sys.argv[1], '*.conf')))
for refl in (False, True):
    seen = collections.defaultdict(list)
    for fn in fs:
        r, nb = parse(fn); seen[canon(r, nb, refl)].append(os.path.basename(fn))
    dups = [v for v in seen.values() if len(v) > 1]
    print('reflections %s: %d files, %d distinct, %d duplicate groups %s' % (refl, len(fs), len(seen), len(dups), dups[:10]))
