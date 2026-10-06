#!/usr/bin/env python3
"""WP20 independent audit recomputation (third implementation).

Written from WP20-D1-declaration.md and WP20-output-format.md only. It imports and reads neither
d1_confirm.py nor d1_check.py. Plan: longtable/audit/WP20-P1-audit-replay-plan.md (commit 003c289).

For one graph it recomputes every per-vertex field of the output schema:
  unfilled_total, states, no_legal_fan, sep_bad, depth{1,2,3,>3}, filled_neighbour_for_bad,
  d1_kills, p_kills, p_capped, locked_classes, legal_fans, status,
and it lists sep_bad / d1 / p kill states in the canonical state encoding.

Colourings are bitmask-based: a colouring is a tuple of 4 vertex masks.
usage:
  wp20_audit.py graph PLANTRI_FILE INDEX...      print JSON per graph
  wp20_audit.py time PLANTRI_FILE INDEX...       timing only
"""
import sys, json, time
from collections import deque

PCAP = 200_000


def parse(line):
    n, rest = line.split()
    rot = [[ord(ch) - 97 for ch in part] for part in rest.split(',')]
    assert len(rot) == int(n)
    return rot


class Graph:
    def __init__(self, rot):
        self.n = len(rot); self.rot = rot
        self.nb = [0] * self.n
        for v, r in enumerate(rot):
            for w in r: self.nb[v] |= 1 << w


def bits(m):
    while m:
        b = m & -m; yield b.bit_length() - 1; m ^= b


def comp_mask(nb, allowed, start):
    """Component of start inside vertex mask `allowed` (start in allowed)."""
    seen = 1 << start; frontier = seen
    while frontier:
        new = 0
        for v in bits(frontier): new |= nb[v]
        new &= allowed & ~seen
        seen |= new; frontier = new
    return seen


def components(nb, allowed):
    out = []; rest = allowed
    while rest:
        s = (rest & -rest).bit_length() - 1
        c = comp_mask(nb, allowed, s); out.append(c); rest &= ~c
    return out


PAIRS = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]


def canon(masks, order):
    """Canonical tuple: colour classes renamed by first occurrence over `order` (list of vertices)."""
    owner = {}
    for c in range(4):
        for v in bits(masks[c]): owner[v] = c
    ren = {}; out = []
    for v in order:
        out.append(ren.setdefault(owner[v], len(ren)))
    return tuple(out)


def masks_from(tup, order):
    m = [0, 0, 0, 0]
    for v, c in zip(order, tup): m[c] |= 1 << v
    return m


def swaps(nb, masks, domain):
    """All single whole-component Kempe swaps of the colouring restricted to `domain` mask."""
    for (p, q) in PAIRS:
        allowed = (masks[p] | masks[q]) & domain
        for K in components(nb, allowed):
            m = list(masks)
            m[p] = (masks[p] & ~K) | (masks[q] & K)
            m[q] = (masks[q] & ~K) | (masks[p] & K)
            yield m


def enum_colourings(G, verts_order, extra_nb=None):
    """All proper 4-colourings of the subgraph on verts_order, canonical by first occurrence in
    verts_order (symmetry breaking: new colour only = number used so far)."""
    pos = {v: i for i, v in enumerate(verts_order)}
    prev = [[w for w in G.rot[v] if w in pos and pos[w] < pos[v]] for v in verts_order]
    if extra_nb:
        for v, ws in extra_nb.items():
            prev[pos[v]] = [w for w in prev[pos[v]] if w not in ws]
    col = [0] * len(verts_order); out = []
    vid = {v: i for i, v in enumerate(verts_order)}
    def rec(i, used):
        if i == len(verts_order):
            out.append(tuple(col)); return
        forb = {col[vid[w]] for w in prev[i]}
        for c in range(min(used + 1, 4)):
            if c not in forb:
                col[i] = c; rec(i + 1, max(used, c + 1))
    rec(0, 0)
    return out


def analyse_vertex(G, x, deadline=None):
    n = G.n; ring = G.rot[x]
    order = [v for v in range(n) if v != x]                 # canonical order skips x
    domain = ((1 << n) - 1) & ~(1 << x)
    nbT = list(G.nb)                                        # T - x: domain excludes x
    legal = [j for j in range(5)
             if not (G.nb[ring[j]] >> ring[(j + 2) % 5] & 1) and not (G.nb[ring[j]] >> ring[(j + 3) % 5] & 1)]
    states = enum_colourings(G, order)
    idx = {s: i for i, s in enumerate(states)}
    pos = {v: i for i, v in enumerate(order)}
    ringpos = [pos[r] for r in ring]

    def ringcols(s): return [s[p] for p in ringpos]
    def filled(s): return len(set(ringcols(s))) <= 3
    def admitting(s):
        rc = ringcols(s); return [j for j in range(5) if rc.count(rc[j]) == 1]

    # pure Kempe graph on all states of T - x
    adjS = [None] * len(states)
    for i, s in enumerate(states):
        m = masks_from(s, order)
        nbrs = set()
        for m2 in swaps(nbT, m, domain):
            nbrs.add(idx[canon(m2, order)])
        adjS[i] = nbrs

    # components of the pure graph (for P)
    compid = [-1] * len(states); comps = []
    for i in range(len(states)):
        if compid[i] >= 0: continue
        cid = len(comps); stack = [i]; compid[i] = cid; members = [i]
        while stack:
            a = stack.pop()
            for b in adjS[a]:
                if compid[b] < 0: compid[b] = cid; stack.append(b); members.append(b)
        comps.append(members)
    comp_has_filled = [any(filled(states[i]) for i in mem) for mem in comps]
    comp_size = [len(mem) for mem in comps]

    # fans: G_j = T - x r_j, x included. Colourings of G_j canonical over order_x = 0..n-1 (x included).
    order_x = list(range(n))
    sep_ok = {}            # (state index, j) -> separable?
    locked_classes = 0
    for j in legal:
        rj = ring[j]
        nbG = list(G.nb); nbG[x] &= ~(1 << rj); nbG[rj] &= ~(1 << x)
        domG = (1 << n) - 1
        # all colourings of G_j: extend each state of T - x by a colour for x avoiding the other 4 ring vertices
        gstates = {}
        for s in states:
            rc = ringcols(s); others = {rc[k] for k in range(5) if k != j}
            m = masks_from(s, order)
            for cx in range(4):
                if cx in others: continue
                m2 = list(m); m2[cx] |= 1 << x
                gstates.setdefault(canon(m2, order_x), None)
        glist = list(gstates); gidx = {g: i for i, g in enumerate(glist)}
        par = list(range(len(glist)))
        def f(a):
            while par[a] != a: par[a] = par[par[a]]; a = par[a]
            return a
        for i, g in enumerate(glist):
            m = masks_from(g, order_x)
            for m2 in swaps(nbG, m, domG):
                k = gidx[canon(m2, order_x)]
                a, b = f(i), f(k)
                if a != b: par[a] = b
        sepclass = {}
        for i, g in enumerate(glist):
            r = f(i); sepclass.setdefault(r, False)
            if g[x] != g[rj]: sepclass[r] = True
        locked_classes += sum(1 for r in sepclass if not sepclass[r])
        # separability of each state admitted by fan j: x coloured c(r_j)
        for si, s in enumerate(states):
            if filled(s) or j not in admitting(s): continue
            m = masks_from(s, order)
            owner_rj = next(c for c in range(4) if m[c] >> rj & 1)
            m2 = list(m); m2[owner_rj] |= 1 << x
            sep_ok[(si, j)] = sepclass[f(gidx[canon(m2, order_x)])]

    rec = dict(x=x, legal_fans=legal, unfilled_total=0, states=0, no_legal_fan=0, sep_bad=0,
               depth={'1': 0, '2': 0, '3': 0, '>3': 0}, filled_neighbour_for_bad=0,
               d1_kills=0, p_kills=0, p_capped=0, locked_classes=locked_classes, status='complete')
    wit = dict(sep_bad=[], d1_kills=[], p_kills=[])

    def state_enc(s):
        out = []; k = 0
        for v in range(n):
            if v == x: out.append(4)
            else: out.append(s[k]); k += 1
        return out

    def good(i):
        s = states[i]
        if filled(s): return False
        la = [j for j in admitting(s) if j in legal]
        return any(sep_ok.get((i, j), False) for j in la)

    for i, s in enumerate(states):
        if filled(s): continue
        rec['unfilled_total'] += 1
        la = [j for j in admitting(s) if j in legal]
        cid = compid[i]
        if comp_size[cid] > PCAP: rec['p_capped'] += 1
        elif not comp_has_filled[cid]:
            rec['p_kills'] += 1; wit['p_kills'].append(state_enc(s))
        if not la:
            rec['no_legal_fan'] += 1; continue
        rec['states'] += 1
        if any(sep_ok[(i, j)] for j in la): continue
        rec['sep_bad'] += 1
        if any(filled(states[k]) for k in adjS[i]): rec['filled_neighbour_for_bad'] += 1
        # depth: BFS over all states (filled traversed), least distance to a good state, cap 3
        dist = {i: 0}; q = deque([i]); d = '>3'
        while q:
            a = q.popleft()
            if dist[a] >= 3: continue
            hit = False
            for b in adjS[a]:
                if b not in dist:
                    dist[b] = dist[a] + 1
                    if good(b): d = str(dist[b]); hit = True; break
                    q.append(b)
            if hit: break
        rec['depth'][d] += 1
        wit['sep_bad'].append(dict(state=state_enc(s), depth=d))
        if d != '1':
            rec['d1_kills'] += 1; wit['d1_kills'].append(state_enc(s))
    if rec['p_capped']: rec['status'] = 'capped'
    return rec, wit


def analyse_graph(rot):
    G = Graph(rot)
    verts = [analyse_vertex(G, x) for x in range(G.n) if len(rot[x]) == 5]
    return [r for r, _ in verts], [w for _, w in verts]


if __name__ == '__main__':
    mode, path = sys.argv[1], sys.argv[2]
    lines = [l for l in open(path) if l.strip()]
    for a in sys.argv[3:]:
        i = int(a); t = time.time()
        recs, wits = analyse_graph(parse(lines[i]))
        if mode == 'time':
            print(i, f'{time.time() - t:.1f}s', len(recs), flush=True)
        else:
            print(json.dumps(dict(index=i, vertices=recs, witnesses=wits)), flush=True)
