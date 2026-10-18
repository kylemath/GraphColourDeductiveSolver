"""Team B round B5: does a published RSST configuration appear in the disc of each non-zero case?
Own containment test: an injective map of the configuration's inner vertices to disc vertices of known degree that
preserves degree and the cyclic order of neighbours (one of the two orientations), so the inner near-triangulation and
its ring attachments are reproduced, and the inner vertices span an induced copy; only u, its link and the second ring are used (third ring degrees unknown), so a
hit holds for every third ring. A disc degree 9 means 9+, so it matches a configuration degree only in mode 'nine'
(degree exactly 9); the strict mode never matches it."""
import sys, os, itertools
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, '..', 'b2_rsst633'))
import score
import conv


def load_confs():
    blocks, cur = [], []
    for line in open(conv.CONF):
        if line.strip() == '':
            if cur:
                blocks.append(cur); cur = []
        else:
            cur.append(line.split())
    if cur:
        blocks.append(cur)
    out = []
    for b in blocks:
        name = b[0][0]
        n, r = int(b[1][0]), int(b[1][1])
        adj = {}
        for row in b[3:3 + n]:
            adj[int(row[0])] = [int(x) for x in row[2:]]
        inner = list(range(r + 1, n + 1))
        out.append((name, r, {a: adj[a] for a in inner}))
    return out


CONFS = load_confs()


def disc(priv):
    L, w, S, P, owner = score.layout()
    deg = {0: 7}
    for i in range(7):
        deg[w[i]] = score.LINK[i]
        deg[S[i]] = score.SWORD[i]
    for z, p in zip(P, priv):
        deg[z] = p
    L.add_ring([deg[z] for z in L.rings[2]])
    rot = score.disc_rot(L)
    known = {x for x in deg if deg[x] is not None and len(rot[x]) == deg[x]}
    return rot, deg, known


def degok(dc, dd, mode):
    if dd == 9:
        return mode == 'nine' and dc == 9
    return dc == dd


def embed(conf, rot, deg, known, mode):
    name, r, adj = conf
    inner = list(adj)
    a0 = max(inner, key=lambda a: len(adj[a]))
    for x0 in known:
        if not degok(len(adj[a0]), deg[x0], mode):
            continue
        for orient in (1, -1):
            for off in range(len(adj[a0])):
                m = {a0: x0}
                align = {a0: (off, orient)}
                stack = [a0]
                ok = True
                while stack and ok:
                    a = stack.pop()
                    x = m[a]
                    o, s = align[a]
                    da = len(adj[a])
                    for k in range(da):
                        b = adj[a][k]
                        y = rot[x][(o + s * k) % da]
                        if b not in adj:          # ring vertex of the configuration: no constraint
                            continue
                        if b in m:
                            if m[b] != y:
                                ok = False; break
                            continue
                        if y not in known or not degok(len(adj[b]), deg[y], mode) or y in m.values():
                            ok = False; break
                        # alignment of b: position of x in rot[y] must correspond to position of a in adj[b]
                        db = len(adj[b])
                        ia = adj[b].index(a)
                        jx = rot[y].index(x)
                        # rot[y][(ob + s * ia) % db] == x  ->  ob = jx - s * ia
                        m[b] = y
                        align[b] = ((jx - s * ia) % db, s)
                        stack.append(b)
                if ok and len(m) == len(inner):
                    # induced: inner vertices adjacent in the disc must be adjacent in the configuration
                    if all((m[b] in rot[m[a]]) == (b in adj[a]) for a in inner for b in inner if a < b):
                        return True
    return False


def job(line):
    f = line.split()
    priv = tuple(int(c) for c in f[0])
    rot, deg, known = disc(priv)
    res = []
    for mode in ('strict', 'nine'):
        hit = None
        for conf in CONFS:
            if embed(conf, rot, deg, known, mode):
                hit = conf[0]
                break
        res.append(hit or '-')
    return '%s %s %s %s %s' % (f[0], f[1], f[2], res[0], res[1])


if __name__ == '__main__':
    lines = [l for l in open(os.path.join(HERE, 'sweep.out')) if l.split()[2] != '0']
    if len(sys.argv) > 1:
        lines = lines[:int(sys.argv[1])]
    with Pool(2) as pool, open(os.path.join(HERE, 'contain.out'), 'w') as fo:
        for s in pool.imap(job, lines, chunksize=20):
            fo.write(s + '\n')
