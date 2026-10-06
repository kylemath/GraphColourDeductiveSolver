#!/usr/bin/env python3
"""Independent census of rigid labelled discs, to validate Math's disc_gen/disc_gen2.

Audit code. It imports and reads no Math or Long Table code. The definitions come from
MathNDiscSearch/README.md and d1-hand-attack.md (Prop 3), as stated there:

  object  = (T, x, ring labelling u0..u4, proper 4-colouring c of T - x), where
            T is a min-degree-5 spherical triangulation, x has degree 5, u0..u4 is the
            rotation at x (either direction, any start), and c has ring word
            D a D b g, i.e. c(u0..u4) = (0,1,0,2,3);
  rigid   = all six bichromatic subgraphs of T - x are forests, with component counts
            (Da,Db,Dg,ab,ag,bg) = (1,2,2,1,1,1);
  legal   = no ring chord u_i u_{i+2} (the generator forbids these).

Canonical form: the labelled ring fixes the starting dart (x -> u0) and an orientation (u0 -> u1
around x), so a breadth-first planar code from that dart is canonical. Mirror images coincide,
because the orientation is taken from the ring labels, not from the input embedding.
"mirror-identified" additionally identifies an object with its reversed labelling
(u0' = u2, u1' = u1, u2' = u0, u3' = u4, u4' = u3, with colours b and g exchanged).

usage:
  rigid_census.py plantri FILE      census from plantri -a output (a triangulation per line)
  rigid_census.py discs FILE...     canonicalise Math's DISC lines, re-verifying each
Both print JSON: counts, and canonical codes with multiplicities.
"""
import json, sys, hashlib
from itertools import combinations

PAIRS = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]   # D=0, a=1, b=2, g=3
TARGET = (1, 2, 2, 1, 1, 1)
RING = (0, 1, 0, 2, 3)


def parse_plantri(line):
    n, rest = line.split()[0], line.split()[1]
    rot = [[ord(ch) - 97 for ch in part] for part in rest.split(',')]
    assert len(rot) == int(n)
    return rot


# ---------- triangulation checks and orientation from an edge list ----------

def faces_of(adj, n):
    """Faces of a triangulation = triangles whose removal leaves the graph connected."""
    faces = []
    for a in range(n):
        for b in adj[a]:
            if b <= a: continue
            for c in adj[a] & adj[b]:
                if c <= b: continue
                rem = set(range(n)) - {a, b, c}
                s = next(iter(rem)); seen = {s}; st = [s]
                while st:
                    v = st.pop()
                    for w in adj[v]:
                        if w in rem and w not in seen:
                            seen.add(w); st.append(w)
                if len(seen) == len(rem):
                    faces.append((a, b, c))
    return faces


def rotation_from_edges(adj, n, x, ring):
    """Oriented rotation system with ring[0] -> ring[1] consecutive around x.
    Returns nxt[v][a] = neighbour following a around v. Checks T is a triangulation."""
    faces = faces_of(adj, n)
    m = sum(len(s) for s in adj) // 2
    if len(faces) != 2 * n - 4 or m != 3 * n - 6:
        raise ValueError('not a triangulation')
    edge_faces = {}
    for f in faces:
        for e in ((f[0], f[1]), (f[1], f[2]), (f[0], f[2])):
            edge_faces.setdefault(frozenset(e), []).append(f)
    if any(len(v) != 2 for v in edge_faces.values()):
        raise ValueError('edge not in exactly two faces')
    # orient faces consistently: an oriented face is a cyclic triple; darts used are (p,q),(q,r),(r,p)
    start = next(f for f in faces if set(f) == {x, ring[0], ring[1]})
    oriented = {frozenset(start): (x, ring[0], ring[1])}
    queue = [(x, ring[0], ring[1])]
    while queue:
        p, q, r = queue.pop()
        for (s, t) in ((p, q), (q, r), (r, p)):
            for g in edge_faces[frozenset((s, t))]:
                key = frozenset(g)
                third = (set(g) - {s, t}).pop()
                want = (t, s, third)                       # opposite traversal of edge s-t
                if key in oriented:
                    o = oriented[key]
                    darts = {(o[0], o[1]), (o[1], o[2]), (o[2], o[0])}
                    if key != frozenset((p, q, r)) and (t, s) not in darts:
                        raise ValueError('non-orientable / inconsistent')
                else:
                    oriented[key] = want; queue.append(want)
    nxt = [dict() for _ in range(n)]
    for (p, q, r) in oriented.values():
        nxt[p][q] = r; nxt[q][r] = p; nxt[r][p] = q
    for v in range(n):
        if len(nxt[v]) != len(adj[v]):
            raise ValueError('rotation incomplete')
    return nxt


def canon_code(nxt, x, u0, label):
    """BFS planar code from dart x->u0 following nxt; vertices carry label[v]."""
    num = {x: 0}; order = [x]; code = []
    first = {x: u0}
    i = 0
    while i < len(order):
        v = order[i]; i += 1
        a = first[v]; w = a; row = []
        while True:
            if w not in num:
                num[w] = len(order); order.append(w); first[w] = v
            row.append(num[w])
            w = nxt[v][w]
            if w == a: break
        code.append((label[v], tuple(row)))
    return repr(code)


# ---------- rigid test on a labelled, coloured T - x ----------

def pair_stats(adj, col, verts):
    out = []
    for (p, q) in PAIRS:
        vs = [v for v in verts if col[v] in (p, q)]
        par = {v: v for v in vs}
        def f(v):
            while par[v] != v:
                par[v] = par[par[v]]; v = par[v]
            return v
        comps = len(vs); forest = True
        for v in vs:
            for w in adj[v]:
                if w > v and w in par:
                    a, b = f(v), f(w)
                    if a == b: forest = False
                    else: par[a] = b; comps -= 1
        out.append((comps, forest))
    return out


def object_code(adj, n, x, ring, col):
    """ring = (u0..u4) in labelled order; col on T - x. Returns (code, mirror_code)."""
    nxt = rotation_from_edges(adj, n, x, ring)
    lab = {v: ('c', col[v]) for v in range(n) if v != x}
    lab[x] = ('x',)
    for k, u in enumerate(ring): lab[u] = ('u', k, col[u])
    code = canon_code(nxt, x, ring[0], lab)
    # reversed labelling: u0'=u2, u1'=u1, u2'=u0, u3'=u4, u4'=u3; colours b<->g
    r2 = (ring[2], ring[1], ring[0], ring[4], ring[3])
    swap = {0: 0, 1: 1, 2: 3, 3: 2}
    col2 = {v: swap[col[v]] for v in col}
    nxt2 = rotation_from_edges(adj, n, x, r2)
    lab2 = {v: ('c', col2[v]) for v in range(n) if v != x}
    lab2[x] = ('x',)
    for k, u in enumerate(r2): lab2[u] = ('u', k, col2[u])
    code2 = canon_code(nxt2, x, r2[0], lab2)
    return code, min(code, code2)


def h(s): return hashlib.sha256(s.encode()).hexdigest()[:20]


# ---------- census from plantri ----------

def census_graph(rot):
    n = len(rot)
    adj = [set(r) for r in rot]
    found = []
    for x in range(n):
        if len(rot[x]) != 5: continue
        r = rot[x]
        others = [v for v in range(n) if v != x]
        for j in range(5):
            for d in (1, -1):
                ring = tuple(r[(j + d * k) % 5] for k in range(5))
                legal = all(ring[(k + 2) % 5] not in adj[ring[k]] for k in range(5))
                col = {ring[k]: RING[k] for k in range(5)}
                # proper on ring (ring edges u_k u_{k+1} have distinct colours by RING); chords
                if any(col.get(a) is not None and col.get(b) is not None and col[a] == col[b]
                       for a in ring for b in adj[a] if b in col and b != x):
                    continue
                # backtracking over the remaining vertices in BFS order from the ring
                rest = []; seen = set(ring) | {x}; q = list(ring)
                while q:
                    v = q.pop(0)
                    for w in rot[v]:
                        if w not in seen: seen.add(w); rest.append(w); q.append(w)
                assert len(rest) == n - 6
                for c in extend(adj, col, rest, 0, x):
                    st = pair_stats(adj, c, others)
                    if all(fo for _, fo in st) and tuple(cm for cm, _ in st) == TARGET:
                        found.append((x, ring, dict(c), legal))
    return adj, found


def creates_cycle(adj, col, v, cv, x):
    """Would colouring v with cv close a cycle in some pair graph (cv, d) of coloured vertices?
    True iff two d-coloured neighbours of v are already joined in that pair graph."""
    for d in range(4):
        if d == cv: continue
        nb = [w for w in adj[v] if w != x and col.get(w) == d]
        if len(nb) < 2: continue
        compid = {}
        for k, s in enumerate(nb):
            if s in compid: return True
            stack = [s]; compid[s] = k
            while stack:
                a = stack.pop()
                for b in adj[a]:
                    if b != x and b not in compid and col.get(b) in (cv, d):
                        compid[b] = k; stack.append(b)
    return False


def extend(adj, col, rest, i, x):
    if i == len(rest):
        yield col; return
    v = rest[i]
    used = {col[w] for w in adj[v] if w in col}
    for cv in range(4):
        if cv in used: continue
        if creates_cycle(adj, col, v, cv, x): continue
        col[v] = cv
        yield from extend(adj, col, rest, i + 1, x)
        del col[v]


def run_plantri(path):
    codes, mcodes = {}, {}
    raw = 0; legal_raw = 0; graphs = 0
    for line in open(path):
        if not line.strip(): continue
        graphs += 1
        rot = parse_plantri(line)
        adj, found = census_graph(rot)
        for (x, ring, col, legal) in found:
            raw += 1
            if not legal: continue
            legal_raw += 1
            c, mc = object_code(adj, len(rot), x, ring, col)
            codes[h(c)] = codes.get(h(c), 0) + 1
            mcodes[h(mc)] = mcodes.get(h(mc), 0) + 1
    return dict(source=path, graphs=graphs, rigid_labelled_raw=raw, rigid_labelled_legal=legal_raw,
                classes=len(codes), classes_mirror_identified=len(mcodes),
                codes=codes, mirror_codes=mcodes)


# ---------- Math's DISC lines ----------

def run_discs(paths):
    codes, mcodes = {}, {}
    lines = 0; bad = []
    for path in paths:
        for ln, line in enumerate(open(path), 1):
            if not line.startswith('DISC'): continue
            lines += 1
            parts = line[4:].split(';')
            cols = list(map(int, parts[1].split()))
            m = len(cols); n = m + 1; x = m
            adj = [set() for _ in range(n)]
            for e in parts[2].split():
                a, b = map(int, e.split('-')); adj[a].add(b); adj[b].add(a)
            for k in range(5): adj[x].add(k); adj[k].add(x)
            col = {v: cols[v] for v in range(m)}
            ring = (0, 1, 2, 3, 4)
            why = []
            if tuple(cols[:5]) != RING: why.append('ring word')
            if any(cols[a] == cols[b] for a in range(m) for b in adj[a] if b < m): why.append('improper')
            if min(len(s) for s in adj) < 5: why.append('min degree')
            if any(ring[(k + 2) % 5] in adj[ring[k]] for k in range(5)): why.append('ring chord')
            st = pair_stats(adj, col, list(range(m)))
            if not (all(fo for _, fo in st) and tuple(cm for cm, _ in st) == TARGET): why.append('not rigid')
            try:
                c, mc = object_code(adj, n, x, ring, col)
            except ValueError as e:
                why.append(str(e)); c = mc = None
            if why:
                bad.append((path, ln, why)); continue
            codes[h(c)] = codes.get(h(c), 0) + 1
            mcodes[h(mc)] = mcodes.get(h(mc), 0) + 1
    return dict(source=paths, disc_lines=lines, rejected=bad, classes=len(codes),
                classes_mirror_identified=len(mcodes), codes=codes, mirror_codes=mcodes)


if __name__ == '__main__':
    mode = sys.argv[1]
    res = run_plantri(sys.argv[2]) if mode == 'plantri' else run_discs(sys.argv[2:])
    json.dump(res, sys.stdout, indent=1); print()
