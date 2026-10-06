"""Route B: larger candidate configurations around a (6^5) hole, for the vacancy game.

UNTESTED.  Math research worker, 6 October 2026, EXPLORE MODE.  Written by hand on the MacBook;
it has NOT been run, not even imported.  Run it on the Mac Studio from this directory with
Python 3.9 and one core.  Write-up: ../MathRouteBSixFive.md.

Every configuration is the 2-ball of a (6^5) hole v (family.config_from_degrees((6,)*5)) plus a
sequence of "closings".  close(x, d) takes a ring vertex x, gives it total degree d, and makes it
an interior vertex:
  * k = d - (current degree of x inside K) new vertices y_1..y_k are added outside x,
    with faces (x, a, y_1), (x, y_i, y_i+1), (x, y_k, b), where a, b are x's ring neighbours;
    x is replaced on the ring by y_1..y_k;
  * if k = 0 the face (a, x, b) closes x, with a new ring edge a-b;
  * k < 0 raises (the right structure would identify two apexes; the builders below avoid this
    by closing degree-5 vertices first).
Genericity assumption [hand]: new vertices are distinct from all old ones (simple ring).  For the
small configurations here this follows from the absence of nontrivial separating cycles of length
<= 5 in a minimal counterexample; it is not checked for the larger ones.

Ring-2 positions: cfg['ring'] of the 2-ball is [w_4, m_0, w_0, m_1, ..., w_3, m_4]:
position p even = w-type (common to two link vertices), p odd = m-type (middle).
Symmetry group of the positions (dihedral of order 10): p -> +-p + 2k (mod 10).

Usage:
  python3 route_b_candidates.py census            # no game; counts words and ring sizes (seconds)
  python3 route_b_candidates.py 0                 # sanity checks (about 1 min)
  python3 route_b_candidates.py 1                 # ring 10-11 candidates (about 5-10 min)
  python3 route_b_candidates.py 2                 # ring 12 candidates (about 30-90 min, < 8 GB)
  python3 route_b_candidates.py 3                 # ring 13-14 (opt-in; hours, may abort)
  python3 route_b_candidates.py 4                 # flat 3-ball F_3, ring 15 (expected to abort)
  python3 route_b_candidates.py 2 Pw Pm           # only the named candidates of a stage
One JSON line per configuration on stdout, flushed; redirect to route_b_stageN_log.txt.
"""
import sys, time, json, itertools
import family, vdred, vdred_joint

POS = list(range(10))
WPOS = [0, 2, 4, 6, 8]
MPOS = [1, 3, 5, 7, 9]


# ----------------------------------------------------------------------------------------------
# disc builder
# ----------------------------------------------------------------------------------------------
class Disc:
    def __init__(self):
        cfg = family.config_from_degrees((6,) * 5)
        self.v = cfg['v']                       # 0
        self.link = list(cfg['link'])           # x_0..x_4 = 1..5
        self.ring = list(cfg['ring'])
        self.R2 = list(cfg['ring'])             # position p -> vertex
        self.E = set(tuple(sorted(e)) for e in cfg['edges'])
        self.nxt = max(cfg['verts']) + 1
        self.closed = {x: 6 for x in self.link}
        self.closed[self.v] = 5

    def kdeg(self, x):
        d = sum(1 for e in self.E if x in e)
        return d + (1 if x in self.link else 0)

    def close(self, x, d):
        if x not in self.ring:
            raise ValueError(f"vertex {x} is not on the ring")
        n = len(self.ring)
        i = self.ring.index(x)
        a, b = self.ring[i - 1], self.ring[(i + 1) % n]
        k = d - self.kdeg(x)
        if k < 0:
            raise ValueError(f"close({x},{d}): already degree {self.kdeg(x)} (apex identification needed)")
        if k == 0:
            e = tuple(sorted((a, b)))
            if e in self.E or n <= 4:
                raise ValueError(f"close({x},{d}) with k=0 would duplicate edge {e}")
            self.E.add(e)
            self.ring.pop(i)
            new = []
        else:
            new = list(range(self.nxt, self.nxt + k))
            self.nxt += k
            path = [a] + new + [b]
            for y in new:
                self.E.add(tuple(sorted((x, y))))
            for p, q in zip(path, path[1:]):
                self.E.add(tuple(sorted((p, q))))
            self.ring[i:i + 1] = new
        self.closed[x] = d
        return new

    def cp(self, p, d):
        """close ring-2 position p."""
        return self.close(self.R2[p], d)

    def cfg(self):
        verts = sorted({a for e in self.E for a in e})
        assert len(set(self.ring)) == len(self.ring)
        return dict(link=list(self.link), ring=list(self.ring), verts=verts,
                    edges=sorted(self.E), v=self.v, r=None)

    def cfg_at(self, x):
        """Same disc, vacancy game played at another closed degree-5 vertex x."""
        if x == self.v:
            return self.cfg()
        assert x in self.closed and x not in self.ring and self.closed[x] == 5
        full = set(self.E) | {tuple(sorted((self.v, u))) for u in self.link}
        nb = {y for e in full if x in e for y in e if y != x}
        adjN = {y: [z for z in nb if tuple(sorted((y, z))) in full] for y in nb}
        assert all(len(l) == 2 for l in adjN.values()), "link of new centre not an induced cycle"
        start = min(nb)
        order, prev, cur = [start], None, start
        while True:
            nx = [z for z in adjN[cur] if z != prev][0]
            if nx == start:
                break
            order.append(nx)
            prev, cur = cur, nx
        assert len(order) == len(nb)
        verts = sorted({y for e in full for y in e} - {x})
        edges = sorted(e for e in full if x not in e)
        return dict(link=order, ring=list(self.ring), verts=verts, edges=edges, v=x, r=None)


# ----------------------------------------------------------------------------------------------
# words on ring 2 (symbols 5, 6, 7, ...; 0 = not closed / degree >= 7 left on the ring)
# ----------------------------------------------------------------------------------------------
def group():
    gs = []
    for k in range(5):
        gs.append(lambda p, k=k: (p + 2 * k) % 10)
        gs.append(lambda p, k=k: (-p + 2 * k) % 10)
    return gs

GROUP = group()

def canon_word(w):
    best = None
    for g in GROUP:
        t = [None] * 10
        for p in POS:
            t[g(p)] = w[p]
        t = tuple(t)
        if best is None or t < best:
            best = t
    return best

def disc_from_word(w):
    """close every position with w[p] != 0, degree-5 positions first (avoids apex merges)."""
    D = Disc()
    for p in POS:
        if w[p] == 5:
            D.cp(p, 5)
    for p in POS:
        if w[p] not in (0, 5):
            D.cp(p, w[p])
    return D

def five_words():
    """{5,6}-words with no two cyclically adjacent 5s, up to symmetry (Burnside, hand: 24)."""
    seen = {}
    for w in itertools.product((5, 6), repeat=10):
        if any(w[p] == 5 and w[(p + 1) % 10] == 5 for p in POS):
            continue
        seen.setdefault(canon_word(w), w)
    return sorted(seen)

def goldberg_words(max_stars=6):
    """Goldberg-like class: a 5 on ring 2 is a hole, so its ring neighbours are 6.
    0 stands for degree >= 7 (left on the ring).  Discharging lemma: <= 6 such vertices."""
    seen = set()
    for w in itertools.product((0, 5, 6), repeat=10):
        if sum(1 for x in w if x == 0) > max_stars:
            continue
        if any(w[p] == 5 and (w[(p + 1) % 10] != 6 or w[p - 1] != 6) for p in POS):
            continue
        seen.add(canon_word(w))
    return sorted(seen)


# ----------------------------------------------------------------------------------------------
# named candidates
# ----------------------------------------------------------------------------------------------
def B2():
    return Disc()

def W(J):
    """(6^5) hole with degree-5 vertices at w-positions J (subset of WPOS); ring 10, |H| 15+|J|."""
    D = Disc()
    for p in J:
        D.cp(p, 5)
    return D

def W_classes():
    seen = {}
    for r in range(1, 6):
        for J in itertools.combinations(WPOS, r):
            w = tuple(5 if p in J else 0 for p in POS)
            seen.setdefault(canon_word(w), J)
    return [seen[k] for k in sorted(seen)]

def M1():
    """degree-5 vertex at m_0 only (p=1); ring 11, |H| 17."""
    D = Disc(); D.cp(1, 5); return D

def Dw6():
    """w_0 (p=2) prescribed degree 6; ring 11, |H| 17."""
    D = Disc(); D.cp(2, 6); return D

def Dm6():
    """m_0 (p=1) prescribed degree 6; ring 12, |H| 18."""
    D = Disc(); D.cp(1, 6); return D

def C4():
    """B2(v) u B2(x_0): close w_4, m_0, w_0 (p=0,1,2) at degree 6; ring 12, |H| 20."""
    D = Disc()
    for p in (0, 1, 2):
        D.cp(p, 6)
    return D

def Pw():
    """two holes at distance 2, w-position: x = w_0 (p=2) degree 5, its link all degree 6.
    = B2(v) u B2(x); ring 12, |H| 21.  Symmetric under v <-> x."""
    D = Disc()
    (z,) = D.cp(2, 5)
    D.cp(1, 6); D.cp(3, 6)
    D.close(z, 6)
    D.hole2 = D.R2[2]
    return D

def Pm():
    """two holes at distance 2, m-position: x = m_0 (p=1) degree 5, its link all degree 6.
    = B2(v) u B2(x); ring 12, |H| 22."""
    D = Disc()
    n1, n2 = D.cp(1, 5)
    D.cp(0, 6); D.cp(2, 6)
    D.close(n1, 6); D.close(n2, 6)
    D.hole2 = D.R2[1]
    return D

def Pair3w():
    """two holes at distance 3: a = ring-3 vertex shared by w_0 and m_0, degree 5, with
    w_0, m_0 and a's other three neighbours all degree 6.  ring 14, |H| 25."""
    D = Disc()
    a, b = D.cp(2, 6)            # path m_0 - a - b - m_1
    d, e = D.close(a, 5)         # path m_0 - d - e - b
    D.cp(1, 6)
    D.close(b, 6); D.close(d, 6); D.close(e, 6)
    D.hole2 = a
    return D

def flat_arc(L):
    """partial flat 3-ball: positions 2, 3, ..., 2+L-1 (w_0 m_1 w_1 ...) closed at degree 6.
    ring = 11, 12, 12, 13, 13, 14, 14, ... for L = 1, 2, 3, ..."""
    D = Disc()
    for j in range(L):
        D.cp((2 + j) % 10, 6)
    return D

def F3():
    return disc_from_word((6,) * 10)

def pentakis3():
    return disc_from_word(tuple(5 if p in WPOS else 6 for p in POS))


# ----------------------------------------------------------------------------------------------
# running
# ----------------------------------------------------------------------------------------------
def count_colourings(cfg, limit):
    """number of canonical proper colourings of K - v, aborting above limit (returns None)."""
    C = vdred.Config(cfg)
    n, nbr = C.n, C.nbr
    c = [-1] * n
    cnt = [0]
    class Stop(Exception):
        pass
    def rec(i, mx):
        if i == n:
            cnt[0] += 1
            if cnt[0] > limit:
                raise Stop
            return
        used = {c[j] for j in nbr[i] if c[j] >= 0}
        for col in range(min(mx + 2, 4)):
            if col not in used:
                c[i] = col
                rec(i + 1, max(mx, col))
        c[i] = -1
    try:
        rec(0, -1)
    except Stop:
        return None
    return cnt[0]

def run(name, cfg, col_limit, max_nodes, also_vdred=False):
    t0 = time.process_time()
    out = dict(name=name, ring=len(cfg['ring']), H=len(cfg['verts']), centre=cfg['v'])
    nc = count_colourings(cfg, col_limit)
    out['colourings'] = nc if nc is not None else f'>{col_limit} (skipped)'
    if nc is not None:
        r = vdred_joint.solve_joint(cfg, verbose=False, max_nodes=max_nodes)
        out.update({k: x for k, x in r.items() if not k.startswith('_')})
        if also_vdred:
            a = vdred.solve(cfg, verbose=False)
            out['vdred'] = dict(reducible=a['reducible'], depth=a['depth'], hist=a['hist'])
    out['cpu'] = round(time.process_time() - t0, 1)
    print(json.dumps(out, default=str), flush=True)
    return out


def stage_list(stage):
    L = []
    if stage == 0:
        L.append(('B2_flat_sanity', B2))                 # expect unfilled 550, hist {1:180, inf:370}
        L.append(('pentakis3_by_closing', pentakis3))    # expect colourings 18420, unfilled 7710,
                                                         # reducible, depth <= 7 (vdred depth 7)
    elif stage == 1:
        for J in W_classes():
            L.append((f'W{list(J)}', lambda J=J: W(J)))
        L.append(('M1', M1))
        L.append(('Dw6', Dw6))
        for w in five_words():
            if sum(1 for x in w if x == 5) >= 4:          # ring 10, 11
                L.append(('B3_' + ''.join(map(str, w)), lambda w=w: disc_from_word(w)))
    elif stage == 2:
        L += [('C4', C4), ('Pw', Pw), ('Pm', Pm), ('Dm6', Dm6),
              ('flat_arc3', lambda: flat_arc(3))]
        for w in five_words():
            if sum(1 for x in w if x == 5) == 3:          # ring 12
                L.append(('B3_' + ''.join(map(str, w)), lambda w=w: disc_from_word(w)))
        L.append(('Pw_at_x', Pw))                        # same disc, game at the other hole
    elif stage == 3:
        for w in five_words():
            if sum(1 for x in w if x == 5) == 2:          # ring 13
                L.append(('B3_' + ''.join(map(str, w)), lambda w=w: disc_from_word(w)))
        L += [('flat_arc4', lambda: flat_arc(4)), ('flat_arc5', lambda: flat_arc(5)),
              ('Pair3w', Pair3w), ('Pair3w_at_a', Pair3w)]
    elif stage == 4:
        L.append(('F3_flat', F3))
    return L


LIMITS = {0: (100_000, 3_000_000), 1: (200_000, 6_000_000), 2: (400_000, 10_000_000),
          3: (1_500_000, 25_000_000), 4: (3_000_000, 40_000_000)}


def census():
    print('five_words (expect 24 classes):', len(five_words()), flush=True)
    by = {}
    for w in five_words():
        k = sum(1 for x in w if x == 5)
        c = disc_from_word(w).cfg()
        by.setdefault((k, len(c['ring']), len(c['verts'])), []).append(''.join(map(str, w)))
    for key in sorted(by):
        print('  #5 =', key[0], 'ring', key[1], '|H|', key[2], ':', len(by[key]), by[key], flush=True)
    print('W classes:', W_classes(), flush=True)
    for name, f in [('B2', B2), ('M1', M1), ('Dw6', Dw6), ('Dm6', Dm6), ('C4', C4), ('Pw', Pw),
                    ('Pm', Pm), ('Pair3w', Pair3w), ('F3', F3), ('pentakis3', pentakis3)] + \
                   [(f'flat_arc{L}', lambda L=L: flat_arc(L)) for L in range(1, 9)]:
        c = f().cfg()
        print(f'  {name}: ring {len(c["ring"])}, |H| {len(c["verts"])}', flush=True)
    gw = goldberg_words()
    hist = {}
    for w in gw:
        try:
            c = disc_from_word(w).cfg()
            key = len(c['ring'])
        except ValueError as e:
            key = 'error'
        hist[key] = hist.get(key, 0) + 1
    print('Goldberg-class words (<= 6 stars), classes:', len(gw), 'ring histogram:',
          dict(sorted(hist.items(), key=lambda kv: str(kv[0]))), flush=True)


if __name__ == '__main__':
    import graphs
    if sys.argv[1:2] == ['census']:
        census(); sys.exit()
    stage = int(sys.argv[1])
    only = set(sys.argv[2:])
    col_limit, max_nodes = LIMITS[stage]
    if stage == 0:
        ref = graphs.ball_config(graphs.pentakis(), 0, 3)
        mine = pentakis3().cfg()
        print(json.dumps(dict(check='pentakis3 vs graphs.ball_config',
                              ring=(len(mine['ring']), len(ref['ring'])),
                              H=(len(mine['verts']), len(ref['verts'])),
                              edges=(len(mine['edges']), len(ref['edges'])),
                              colourings=(count_colourings(mine, 10**6),
                                          count_colourings(ref, 10**6)))), flush=True)
    for name, f in stage_list(stage):
        if only and name not in only:
            continue
        D = f()
        if name.endswith('_at_x') or name.endswith('_at_a'):
            cfg = D.cfg_at(D.hole2)
        else:
            cfg = D.cfg()
        run(name, cfg, col_limit, max_nodes, also_vdred=(stage == 0))
