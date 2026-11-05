# canonical code of a kc configuration line (up to rotation/reflection), rotation recovered from the triangulation (ring + hub)
import hashlib
def parse(line):
    f = line.split(); nm, r, m = f[0], int(f[1]), int(f[2])
    ra = [[] if x == '-' else [int(y) for y in x.split(',')] for x in f[3].split(';')]
    ia = [[] if x == '-' else [int(y) for y in x.split(',')] for x in f[4].split(';')]
    return nm, r, m, ra, ia
def sig(line):
    nm, r, m, ra, ia = parse(line)
    return (r, m, tuple(sorted(len(a) + len(b) for a, b in zip(ra, ia))))
def code(line):
    nm, r, m, ra, ia = parse(line)
    N = r + m; H = N; adj = {x: set() for x in range(N + 1)}
    def e(a, b): adj[a].add(b); adj[b].add(a)
    for i in range(r): e(i, (i + 1) % r); e(i, H)
    for j in range(m):
        for x in ra[j]: e(r + j, x)
        for x in ia[j]: e(r + j, r + x)
    # rotation: link cycle of each vertex
    rot = {}
    for x in adj:
        nb = adj[x]
        sub = {y: adj[y] & nb for y in nb}
        if any(len(v) != 2 for v in sub.values()): return None
        s = min(nb); cyc = [s]; prev = None
        while True:
            c = cyc[-1]; a, b = sorted(sub[c]); nx = a if a != prev else b
            if nx == s: break
            cyc.append(nx); prev = c
        if len(cyc) != len(nb): return None
        rot[x] = cyc
    # orient coherently from the hub
    ori = {H: rot[H]}; stack = [H]
    while stack:
        x = stack.pop(); cx = ori[x]; L = len(cx)
        for i, y in enumerate(cx):
            if y in ori: continue
            z = cx[(i + 1) % L]   # rot(x): y -> z  => rot(y): z -> x
            cy = rot[y]; k = cy.index(z)
            if cy[(k + 1) % len(cy)] != x: cy = cy[::-1]
            ori[y] = cy; stack.append(y)
    Is = set(range(r, N)); best = None
    rotn = {x: [y for y in ori[x] if y != H] for x in range(N)}
    for i in range(r):
        for b in ((i + 1) % r, (i - 1) % r):
            for mir in (0, 1):
                lab = {i: 0, b: 1}; seq = [i, b]; ref = {i: b, b: i}; out = []; k = 0
                while k < len(seq):
                    x = seq[k]; nb = rotn[x][::-1] if mir else rotn[x]
                    j = nb.index(ref[x]); nb = nb[j:] + nb[:j]
                    for y in nb:
                        if y not in lab: lab[y] = len(seq); seq.append(y); ref[y] = x
                    out.append((1 if x in Is else 0,) + tuple(lab[y] for y in nb)); k += 1
                c = tuple(out)
                if best is None or c < best: best = c
    return hashlib.md5(repr(best).encode()).hexdigest()[:20]
