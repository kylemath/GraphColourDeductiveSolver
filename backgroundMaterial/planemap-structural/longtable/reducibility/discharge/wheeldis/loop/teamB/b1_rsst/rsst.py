"""Team B round B1: RSST's 32 discharge rules in Gonthier's encoding (fourcolor/theories/proof/discharge.v), ported to
Python and evaluated on explicit planar rotation systems.  Own code; semantics taken from part.v (fitp, mirror_part,
rot_part) and discharge.v (base_drules, symmetrize_drules, dscore).

A part is a list of subparts (spoke, hat, fans); ranges are (lo, hi) with hi = 99 for "M+" / "*".  Degree 9 stands
for "9 or more" everywhere (Pr99 = >= 9 in Gonthier).  A part fitting exactly at dart j of vertex v (deg v = size)
moves one unit (RSST units, initial charge 10 (6 - deg)) from v to the spoke of subpart 2.

Geometry (part.v subpart_loc_move): spoke k = k-th neighbour from the dart, in the face (rotation) order of v.  Around
spoke S = w_k, in the same rotation sense, the neighbours read v, w_{k-1}, hat_k, fan1, fan2, ..., i.e. the hat is the
common neighbour of w_{k-1} and w_k other than v, and the fans follow it going away from v."""

RANGES = {}


def rng(tok):
    if tok == '*':
        return (5, 99)
    if tok.endswith('+'):
        return (int(tok[:-1]), 99)
    if tok.endswith('-'):
        return (5, int(tok[:-1]))
    if '?' in tok:
        a, b = tok.split('?')
        return (int(a), int(b))
    m = int(tok)
    return (m, 99) if m == 9 else (m, m)


def parse(s):
    """Gonthier Part syntax -> list of dicts {s, h, f: [..]}."""
    s = s.strip()
    assert s.startswith('$') and s.endswith('$')
    out = []
    i = 0
    while True:
        assert s[i] == '$'
        i += 1
        while i < len(s) and s[i] == ' ':
            i += 1
        if i >= len(s):
            break
        if s[i] == '[':
            j = s.index(']', i)
            inner = s[i + 1:j].split()
            i = j + 1
        else:
            inner = None
        while s[i] == ' ':
            i += 1
        j = i
        while s[j] != ' ' and s[j] != '$':
            j += 1
        spk = s[i:j]
        i = j
        while s[i] == ' ':
            i += 1
        if inner is None:
            out.append({'s': rng(spk), 'h': (5, 99), 'f': []})
        elif len(inner) == 1:
            out.append({'s': rng(spk), 'h': rng(inner[0]), 'f': []})
        else:
            n = int(spk)
            assert len(inner) == n - 4, (s, inner, spk)     # hat + (n - 5) fans
            out.append({'s': (n, n), 'h': rng(inner[0]), 'f': [rng(t) for t in inner[1:]]})
    return out


BASE_SRC = """
drule1 := $ * $ * $ 6+ $ * $ * $
drule2  := $ * $ 5 $ 7+ $ * $ * $
drule2' := $ * $ 5 $ 7+ $ * $ * $ * $
drule3  := $ 5 $ 6- $ 6+ $ * $ * $
drule3' := $ 5 $ 6- $ 6+ $ * $ * $ * $
drule4  := $ 6- $[5] 5 $ 6+ $ * $ * $ * $
drule4' := $ 6- $[5] 6 $ 6+ $ * $ * $ * $
drule5 := $ 6 $[6- 5] 6 $ 6+ $ * $ * $ * $
drule6 := $ 6 $[6-] 5 $[5] 7+ $ * $ * $ * $
drule7 := $ 6 $[6 6-] 6 $[5] 7+ $ * $ * $ * $
drule8 := $ 5 $ 6- $ 7+ $ * $ * $ * $ * $
drule9 := $ 6- $ 6- $ 7+ $ * $ * $ * $ 5 $
drule10  := $ 5 $ 5 $ 7+ $ 5 $ 6+ $ * $ * $
drule10' := $ 5 $ 5 $ 7+ $ 5 $ 5 $ * $ * $
drule11 := $ 6 $[5] 5 $ 7+ $ 5 $ 6+ $ * $ * $
drule12 := $ 5 $[5] 5 $ 7+ $ 5 $[5] 5 $ * $ * $
drule13 := $ 6 $[5] 5 $[5] 8+ $ 5 $ 5 $ * $ * $
drule14 := $ 5 $[5] 6 $ 7+ $ 5 $ * $ * $ * $
drule15 := $ 5 $ 6 $ 7+ $ 5 $ 7+ $ 5 $ 6 $
drule16 := $ 6 $ 6 $ 7+ $ 5 $ 5 $ 5 $ 6 $
drule17 := $ 5 $[6] 6 $ 7+ $ 5 $ 5 $ 7+ $ 5 $
drule18 := $ 6 $[5] 5 $[5] 7 $ 6+ $ * $ * $ 5 $
drule19 := $ 6 $ 6+ $ 8+ $[5] 5 $[5] 6 $ 5 $ 6 $
drule20 := $ 5 $ 6 $ 7+ $ 6 $ 6 $ 5 $ 5 $
drule21 := $ 6- $ 6 $[5] 7 $ 6+ $ * $ 5 $ 5 $
drule22 := $ 5 $ 6 $[5] 7 $ 6+ $ * $ 5 $ 6 $
drule23 := $ 5 $[5] 7 $ 7+ $ 5 $ * $ * $ * $
drule24 := $ 5 $ 5 $[5] 7 $ 7+ $ 6 $ 6 $ 5 $
drule25 := $ 5 $ 5 $ 7+ $[* * 5] 7 $[6] 5 $ 5 $ * $
drule26 := $ 6 $ 6 $[5] 7 $ 7+ $ 5 $ 5 $ 6 $
drule27 := $ 7+ $ 6 $[6 5 6+] 7 $ 7 $[5] 6- $ * $ * $
drule28 := $ 5 $ 5 $ 7+ $ 5 $ 5 $ * $ * $ 5 $
drule29 := $ 5 $[5] 5 $ 7+ $ 5 $ * $ * $ 5 $ 5 $
drule30 := $ 5 $ 5 $ 7+ $ 5 $[5] 6 $ 5 $ * $ * $
drule31  := $ 5 $[5] 5 $ 7+ $ 5 $[6+] 5 $ 6+ $ * $ 6+ $
drule31' := $ 5 $[5] 5 $ 7+ $ 5 $[5] 5 $ 6+ $ * $ 6+ $
drule32 := $ 5 $ 6 $[5] 7 $ 7+ $ 6 $ 5 $ 5 $ 5 $
"""
NAMES, SRC = [], {}
for line in BASE_SRC.strip().splitlines():
    nm, body = line.split(':=')
    nm = nm.strip()
    NAMES.append(nm)
    SRC[nm] = body.strip()
ORDER = ['drule1', 'drule1', 'drule2', "drule2'", 'drule3', "drule3'", 'drule4', "drule4'", 'drule5', 'drule6',
         'drule7', 'drule8', 'drule9', 'drule10', "drule10'", 'drule11', 'drule12', 'drule13', 'drule14', 'drule15',
         'drule16', 'drule17', 'drule18', 'drule19', 'drule20', 'drule21', 'drule22', 'drule23', 'drule24', 'drule25',
         'drule26', 'drule27', 'drule28', 'drule29', 'drule30', 'drule31', "drule31'", 'drule32']
assert len(ORDER) == 38


def mirror_part(p):
    """part.v mirror_part: reversed list; each subpart takes the next subpart's hat (cyclically wrapping to the
    first hat), and its fans reversed."""
    n = len(p)
    out = []
    for k in range(n):
        nh = p[k + 1]['h'] if k + 1 < n else p[0]['h']
        out.append({'s': p[k]['s'], 'h': nh, 'f': list(reversed(p[k]['f']))})
    return list(reversed(out))


def rot_part(n, p):
    return p[n:] + p[:n]


def sym_image(p):
    q = mirror_part(p)
    for _ in range(5):
        q = rot_part(len(q) - 1, q)
    return q


def subset(p, q):
    """p's set of fitting maps contained in q's (same size), componentwise."""
    if len(p) != len(q):
        return False
    for a, b in zip(p, q):
        if len(a['f']) != len(b['f']) and b['f']:
            # q constrains fans that p does not fix
            return False
        for x, y in [(a['s'], b['s']), (a['h'], b['h'])] + list(zip(a['f'], b['f'])):
            if not (y[0] <= x[0] and x[1] <= y[1]):
                return False
    return True


def the_drules():
    base = [(nm, parse(SRC[nm])) for nm in ORDER]
    out = []
    # symmetrize_drules: p :: (sym rest), with p' prepended when p is not a subset of p'
    for nm, p in base:
        pp = sym_image(p)
        if subset(p, pp):
            out.append((nm, p))
        else:
            out.append((nm + 'm', pp))
            out.append((nm, p))
    return out


RULES = the_drules()


def inr(r, d):
    return r[0] <= d <= r[1]


class Map:
    """rot[v]: neighbours of v in a consistent rotation order (complete for every vertex we evaluate at);
    deg[v]: degree label (9 = 9 or more).  Vertices whose rotation is incomplete may appear as hats/fans only."""

    def __init__(self, rot, deg):
        self.rot = rot
        self.deg = deg
        self.pos = [{y: i for i, y in enumerate(r)} for r in rot]

    def around(self, s, v, prev):
        """neighbours of s read from v in the sense where the next one is prev; returns list starting at v."""
        r = self.rot[s]
        n = len(r)
        i = self.pos[s][v]
        if r[(i + 1) % n] == prev:
            return [r[(i + t) % n] for t in range(n)]
        assert r[(i - 1) % n] == prev, ('not adjacent around spoke', s, v, prev)
        return [r[(i - t) % n] for t in range(n)]

    def fits(self, v, j, p):
        r = self.rot[v]
        d = len(r)
        if d != len(p):
            return False
        for k, sp in enumerate(p):
            w = r[(j + k) % d]
            if not inr(sp['s'], self.deg[w]):
                return False
            if sp['h'] != (5, 99) or sp['f']:
                ar = self.around(w, v, r[(j + k - 1) % d])
                # ar = [v, w_{k-1}, hat, fan1, ...]
                if not inr(sp['h'], self.deg[ar[2]]):
                    return False
                for t, fr in enumerate(sp['f']):
                    if not inr(fr, self.deg[ar[3 + t]]):
                        return False
        return True

    def sends(self, v):
        """list of (target, rule name) units sent by v."""
        out = []
        r = self.rot[v]
        d = len(r)
        for j in range(d):
            for nm, p in RULES:
                if len(p) == d and self.fits(v, j, p):
                    out.append((r[(j + 2) % d], nm))
        return out


if __name__ == '__main__':
    for nm, p in RULES:
        print(nm, len(p), p)
    print(len(RULES), 'rules after symmetrization')


def constraints(M, v, j, p):
    """the (vertex, range) conjunction for part p at dart j of v (p's size must equal deg v), or None."""
    r = M.rot[v]
    d = len(r)
    if d != len(p):
        return None
    cs = []
    for k, sp in enumerate(p):
        w = r[(j + k) % d]
        cs.append((w, sp['s']))
        if sp['h'] != (5, 99) or sp['f']:
            ar = M.around(w, v, r[(j + k - 1) % d])
            cs.append((ar[2], sp['h']))
            for t, fr in enumerate(sp['f']):
                cs.append((ar[3 + t], fr))
    return cs


def inflow_range(M, x, target, free):
    """min and max number of rule units x sends to target, over degrees in {5..9} of the vertices in `free`
    (all other degrees fixed in M.deg).  Returns (lo, hi, rules at hi)."""
    r = M.rot[x]
    d = len(r)
    js = [j for j in range(d) if r[(j + 2) % d] == target]
    cand = []
    for j in js:
        for nm, p in RULES:
            cs = constraints(M, x, j, p)
            if cs is None:
                continue
            ok = True
            fc = []
            for z, rg in cs:
                if z in free:
                    fc.append((z, rg))
                elif not inr(rg, M.deg[z]):
                    ok = False
                    break
            if ok:
                cand.append((nm, fc))
    fv = sorted({z for _, fc in cand for z, _ in fc})
    import itertools
    lo, hi, arg = 10 ** 9, -1, None
    for vals in itertools.product([5, 6, 7, 8, 9], repeat=len(fv)):
        a = dict(zip(fv, vals))
        got = [nm for nm, fc in cand if all(inr(rg, a[z]) for z, rg in fc)]
        if len(got) > hi:
            hi, arg = len(got), got
        lo = min(lo, len(got))
    return lo, hi, arg
