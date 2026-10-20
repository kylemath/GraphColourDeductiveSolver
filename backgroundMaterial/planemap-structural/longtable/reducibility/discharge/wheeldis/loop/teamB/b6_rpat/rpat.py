"""Team B round B6: configuration oracle for receiver arrangements.
Given a receiver of exact degree d with link word w and second-ring word s (letters 5..9, 9 = 9+), look for an RSST
configuration (the 633, all D/C-reducible on Team B's kc and cfast, round B2) whose inner vertices map onto u, the link
and the second ring only (privates never inner), with equal degrees (9+ never matched; u's degree d is exact), the same
cyclic neighbour order (either orientation) and an induced inner subgraph.  Such an embedding does not depend on the
privates or the third ring, so it kills every arrangement that agrees on the slots it reads:
  - the letter of every mapped w_i / s_i (singleton mask),
  - for every mapped s_i, whether w_i and w_{i+1} are 5 (s_i touches s_{i-1} / s_{i+1} exactly when they are):
    mask {5} or {6,7,8,9}.
Output pattern format = sepb's: 'd n slot mask ...' with slot w_i = i, s_i = d + i, mask bit k = letter 5 + k."""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
DIS = os.path.abspath(os.path.join(HERE, '../../../..'))
sys.path.insert(0, os.path.join(DIS, 'b8b'))
sys.path.insert(0, DIS)
sys.path.insert(0, os.path.join(HERE, '..', 'b1_rsst'))
sys.path.insert(0, os.path.join(HERE, '..', 'b5_lt7'))
from rings import Layered
from rstar import disc_rot
import contain

CONFS = list(contain.CONFS)


def load_nl(cdir):
    """the 2026 set (github.com/near-linear-4ct/reducible-configurations, MIT): all 8,200 D on both of our engines
    (explore round 54d + Studio nl54d/nl54e).  .conf: blank, 'n r', then 'v deg nbrs' per interior vertex, cyclic order."""
    out = []
    for fn in sorted(os.listdir(cdir)):
        if not fn.endswith('.conf'):
            continue
        L = [l.split() for l in open(os.path.join(cdir, fn)) if l.strip()]
        n, r = int(L[0][0]), int(L[0][1])
        adj = {int(f[0]): [int(x) for x in f[2:]] for f in L[1:]}
        assert sorted(adj) == list(range(r + 1, n + 1)) and all(int(f[1]) == len(f) - 2 for f in L[1:]), fn
        out.append((fn[:-5], r, adj))
    return out


if os.environ.get('RPAT_NL'):
    CONFS += load_nl(os.environ['RPAT_NL'])


def degsig(adj):
    c = {}
    for a in adj:
        c[len(adj[a])] = c.get(len(adj[a]), 0) + 1
    return c


SIGS = [degsig(c[2]) for c in CONFS]
FULL = 31
NOT5 = 30


def disc(d, link, sword):
    """explicit disc: u = 0, link, second ring with the given s letters, privates of degree 9 (never inner)."""
    L = Layered(d)
    w = L.rings[1]
    L.add_ring(list(link))
    R2 = L.rings[2]
    adj = {}
    for a, b, c in L.tris:
        for x, y in ((a, b), (b, c), (c, a)):
            adj.setdefault(x, set()).add(y)
            adj.setdefault(y, set()).add(x)
    S = []
    for i in range(d):
        c = [z for z in R2 if w[i] in adj[z] and w[(i + 1) % d] in adj[z]]
        assert len(c) == 1
        S.append(c[0])
    deg = {0: d}
    for i in range(d):
        deg[w[i]] = link[i]
        deg[S[i]] = sword[i]
    for z in R2:
        if z not in deg:
            deg[z] = 9
    L.add_ring([deg[z] for z in R2])
    rot = disc_rot(L)
    slot = {w[i]: i for i in range(d)}
    slot.update({S[i]: d + i for i in range(d)})
    known = {x for x in slot if deg[x] <= 8 and len(rot[x]) == deg[x]}
    if len(rot[0]) == d:
        known.add(0)
    return rot, deg, known, slot


def degok(dc, x, deg):
    if x == 0:
        return dc == deg[0]
    return deg[x] <= 8 and dc == deg[x]


def embed_map(conf, rot, deg, known):
    name, r, adj = conf
    inner = list(adj)
    a0 = max(inner, key=lambda a: len(adj[a]))
    for x0 in known:
        if not degok(len(adj[a0]), x0, deg):
            continue
        for orient in (1, -1):
            for off in range(len(adj[a0])):
                m = {a0: x0}
                used = {x0}
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
                        if b not in adj:
                            continue
                        if b in m:
                            if m[b] != y:
                                ok = False
                                break
                            continue
                        if y not in known or not degok(len(adj[b]), y, deg) or y in used:
                            ok = False
                            break
                        db = len(adj[b])
                        m[b] = y
                        used.add(y)
                        align[b] = ((rot[y].index(x) - s * adj[b].index(a)) % db, s)
                        stack.append(b)
                if ok and len(m) == len(inner):
                    if all((m[b] in rot[m[a]]) == (b in adj[a]) for a in inner for b in inner if a < b):
                        return m
    return None


def pattern(d, link, sword, m, slot):
    sm = {}
    for x in m.values():
        if x == 0:
            continue
        sl = slot[x]
        let = link[sl] if sl < d else sword[sl - d]
        sm[sl] = 1 << (let - 5)
    for x in list(m.values()):
        if x == 0 or slot[x] < d:
            continue
        i = slot[x] - d
        for j in (i, (i + 1) % d):
            if j not in sm:
                sm[j] = 1 if link[j] == 5 else NOT5
    return sorted(sm.items())


def kill(d, link, sword):
    """first configuration (in RSST order) appearing in the arrangement for every privates / third ring:
    returns (name, pattern) or None."""
    rot, deg, known, slot = disc(d, link, sword)
    have = {}
    for x in known:
        have[deg[x]] = have.get(deg[x], 0) + 1
    for c, sg in zip(CONFS, SIGS):
        if any(have.get(k, 0) < v for k, v in sg.items()):
            continue
        m = embed_map(c, rot, deg, known)
        if m is not None:
            return c[0], pattern(d, link, sword, m, slot)
    return None


def fmt(d, pat):
    return '%d %d %s' % (d, len(pat), ' '.join('%d %d' % q for q in pat))


if __name__ == '__main__':
    for a in sys.argv[1:]:
        ww, ss = a.split('/')
        link = [int(c) for c in ww]
        sw = [int(c) for c in ss]
        print(a, kill(len(link), link, sw))
