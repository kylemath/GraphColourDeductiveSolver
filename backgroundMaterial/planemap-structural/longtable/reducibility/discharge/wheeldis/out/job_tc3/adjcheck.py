"""tc3 (Long Table via coordinator 21 Oct 05:36Z): Studio's independent check of each window line `NAME r m RINGNB INTNB`.
Graph: interior 0..m-1, ring R0..R(r-1) with the ring cycle R_t - R_{t+1}. Checks: (a) symmetric interior adjacency, ring
indices in range; (b) near-triangulation with the ring as the outer face: every interior vertex's neighbourhood induces one
cycle (wheel), every ring vertex's neighbourhood induces one path from R_{t-1} to R_{t+1}; (c) Euler: V - E + F = 2 with
F = T + 1, T = 3-cycles, and 3T + r = 2E (no separating triangle); (d) degrees (interior degree = |ring| + |interior|),
the two degree-7 hubs and their links read cyclically against 7766556 / 6567566 up to rotation and reflection."""
import sys, collections
def cyc_words(w):
    n = len(w); out = set()
    for s in (w, w[::-1]):
        for k in range(n): out.add(s[k:] + s[:k])
    return out
for line in open(sys.argv[1]):
    if not line.strip(): continue
    nm, r, m, RN, IN = line.split(); r = int(r); m = int(m)
    rp = [[] if g == '-' else [int(x) for x in g.split(',')] for g in RN.split(';')]
    ip = [[] if g == '-' else [int(x) for x in g.split(',')] for g in IN.split(';')]
    bad = []
    if len(rp) != m or len(ip) != m: bad.append('field lengths %d %d != m' % (len(rp), len(ip)))
    G = collections.defaultdict(set)
    for v in range(m):
        for u in ip[v]:
            if not 0 <= u < m or u == v: bad.append('bad interior nbr %d of %d' % (u, v))
            elif v not in ip[u]: bad.append('asymmetric %d-%d' % (v, u))
            G[('I', v)].add(('I', u))
        for t in rp[v]:
            if not 0 <= t < r: bad.append('ring index %d out of range' % t)
            G[('I', v)].add(('R', t)); G[('R', t)].add(('I', v))
    for t in range(r): G[('R', t)].add(('R', (t + 1) % r)); G[('R', (t + 1) % r)].add(('R', t))
    V = m + r; E = sum(len(s) for s in G.values()) // 2
    T = sum(1 for a in G for b in G[a] for c in G[a] & G[b] if a < b < c)
    if V - E + T + 1 != 2: bad.append('Euler V-E+F = %d' % (V - E + T + 1))
    if 3 * T + r != 2 * E: bad.append('3T+r=%d != 2E=%d' % (3 * T + r, 2 * E))
    for x in G:
        N = G[x]; deg = {y: len(G[y] & N) for y in N}
        if x[0] == 'I':
            ok = all(d == 2 for d in deg.values())
        else:
            ends = {('R', (x[1] - 1) % r), ('R', (x[1] + 1) % r)}
            ok = all(deg[y] == (1 if y in ends else 2) for y in N) and len(N) >= 2
        # connectivity of the link
        if ok:
            st = [next(iter(N))]; seen = set(st)
            while st:
                y = st.pop()
                for z in G[y] & N:
                    if z not in seen: seen.add(z); st.append(z)
            ok = seen == N
        if not ok: bad.append('link of %s%d not a %s' % (x[0], x[1], 'cycle' if x[0] == 'I' else 'ring path'))
    if any(not G[('R', t)] - {('R', (t - 1) % r), ('R', (t + 1) % r)} for t in range(r)): bad.append('ring vertex with no interior nbr')
    deg = [len(G[('I', v)]) for v in range(m)]
    # order each hub's neighbours cyclically and read degrees ('?' for ring vertices)
    hubs = [v for v in range(m) if deg[v] == 7]
    info = []
    for h in hubs:
        N = G[('I', h)]; cyc = [next(iter(sorted(N)))]
        while len(cyc) < len(N):
            nx = [z for z in G[cyc[-1]] & N if z not in cyc]
            if not nx: break
            cyc.append(sorted(nx)[0])
        word = ''.join(str(len(G[z])) if z[0] == 'I' else '?' for z in cyc)
        fit = any(all(a == '?' or a == b for a, b in zip(w, '7766556')) for w in cyc_words(word))
        info.append('hub I%d link %s %s' % (h, word, 'fits 7766556' if fit else 'NOT 7766556'))
    hh = [(a, b) for a in hubs for b in hubs if a < b and ('I', b) in G[('I', a)]]
    print('%s r=%d m=%d V=%d E=%d T=%d deg=%s hubs7=%s 7-7 edges=%s | %s | %s' % (nm, r, m, V, E, T, ''.join(map(str, deg)) if max(deg) < 10 else deg,
          hubs, hh, '; '.join(info), 'OK' if not bad else 'FAIL: ' + '; '.join(bad[:5])))
