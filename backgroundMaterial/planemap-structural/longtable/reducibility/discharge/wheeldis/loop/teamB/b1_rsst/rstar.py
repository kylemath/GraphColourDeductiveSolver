"""Round B1: RSST score of u at R* (link 5675765, s = 6,s1,7,7,s4,7,5), per filling and private assignment.
Ring-3 degrees are free in {5..9}; each neighbour's inflow to u is maximised / minimised over the ring-3 vertices it
reads (independently per neighbour: an upper / lower bound on u's score)."""
import sys, os, itertools
HERE = os.path.dirname(os.path.abspath(__file__))
DIS = os.path.abspath(os.path.join(HERE, '../../../..'))
sys.path.insert(0, os.path.join(DIS, 'b8b'))
sys.path.insert(0, DIS)
sys.path.insert(0, HERE)
from rings import Layered
import rsst

LINK = [5, 6, 7, 5, 7, 6, 5]


def build(s1, s4, priv):
    """priv = (p1, p2a, p2b, p4a, p4b, p5).  Returns (Map, u, w[], s[], ring3 list)."""
    L = Layered(7)
    w = L.rings[1]
    L.add_ring(LINK)
    R2 = L.rings[2]
    tris = L.tris
    adj = {}
    for a, b, c in tris:
        for x, y in ((a, b), (b, c), (c, a)):
            adj.setdefault(x, set()).add(y)
            adj.setdefault(y, set()).add(x)
    S = [None] * 7
    for i in range(7):
        c = [z for z in R2 if w[i] in adj[z] and w[(i + 1) % 7] in adj[z]]
        assert len(c) == 1
        S[i] = c[0]
    sdeg = [6, s1, 7, 7, s4, 7, 5]
    deg = {}
    for i in range(7):
        deg[S[i]] = sdeg[i]
    p1, p2a, p2b, p4a, p4b, p5 = priv

    def privs(i):
        return [z for z in R2 if w[i] in adj[z] and z not in S]
    P1 = privs(1); P5 = privs(5); P2 = privs(2); P4 = privs(4)
    assert len(P1) == 1 and len(P5) == 1 and len(P2) == 2 and len(P4) == 2
    deg[P1[0]] = p1
    deg[P5[0]] = p5
    # p2a is next to s1, p2b next to s2 (both privates of w2 are adjacent to each other)
    a2 = [z for z in P2 if S[1] in adj[z]]
    b2 = [z for z in P2 if S[2] in adj[z]]
    assert len(a2) == 1 and len(b2) == 1 and a2 != b2
    deg[a2[0]] = p2a
    deg[b2[0]] = p2b
    a4 = [z for z in P4 if S[3] in adj[z]]
    b4 = [z for z in P4 if S[4] in adj[z]]
    assert len(a4) == 1 and len(b4) == 1 and a4 != b4
    deg[a4[0]] = p4a
    deg[b4[0]] = p4b
    assert len(deg) == len(R2), (len(deg), len(R2))
    L.add_ring([deg[z] for z in R2])
    R3 = L.rings[3]
    deg[0] = 7
    for i in range(7):
        deg[w[i]] = LINK[i]
    for z in R3:
        deg[z] = None
    rot = disc_rot(L)
    return rot, deg, w, S, R3


def disc_rot(L):
    """rotation lists; complete for interior vertices, a path for boundary ones (never used as hub or spoke)."""
    nxt = [dict() for _ in range(L.n)]
    for a, b, c in L.tris:
        nxt[a][b] = c; nxt[b][c] = a; nxt[c][a] = b
    rot = []
    for x in range(L.n):
        succ = nxt[x]
        if not succ:
            rot.append([]); continue
        starts = set(succ) - set(succ.values())
        s = next(iter(starts)) if starts else next(iter(succ))
        r = [s]; y = succ.get(s)
        while y is not None and y != s:
            r.append(y); y = succ.get(y)
        rot.append(r)
    return rot


def second_nbhd(rot, v):
    out = set()
    for x in rot[v]:
        out.update(rot[x])
        out.add(x)
    out.discard(v)
    return out


def score_bounds(s1, s4, priv, detail=False):
    rot, deg, w, S, R3 = build(s1, s4, priv)
    M = rsst.Map(rot, dict(deg))
    out_u = M.sends(0)
    hi = lo = -10 - len(out_u)
    per = []
    free = set(R3)
    for i, x in enumerate(w):
        a, b, arg = rsst.inflow_range(M, x, 0, free)
        hi += b
        lo += a
        per.append((i, LINK[i], a, b, arg))
    if detail:
        return hi, lo, out_u, per
    return hi, lo


if __name__ == '__main__':
    hi, lo, out_u, per = score_bounds(6, 6, (7, 6, 6, 6, 6, 6), detail=True)
    print('u out', out_u)
    for row in per:
        print(row)
    print('score bounds', lo, hi)
