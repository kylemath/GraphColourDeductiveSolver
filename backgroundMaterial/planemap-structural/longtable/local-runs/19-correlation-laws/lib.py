"""[exploratory] Item 19 shared code: link-pattern sequences of the d-cycle, dihedral action, class loading."""
import itertools, json, os
H = os.path.dirname(os.path.abspath(__file__))

def canon(w):
    mp = {}; return tuple(mp.setdefault(x, len(mp)) for x in w)

def sequences(d):
    """all proper colourings of the d-cycle with colours 0..3, canonical by first occurrence (colour renaming removed)"""
    out = []
    for w in itertools.product(range(4), repeat=d):
        if canon(w) == w and all(w[i] != w[(i + 1) % d] for i in range(d)): out.append(w)
    return out

def dihedral(d):
    """list of (r, s): position t of the new word reads old position (r + s*t) mod d"""
    return [(r, s) for r in range(d) for s in (1, -1)]

def act(w, g):
    d = len(w); r, s = g
    return canon([w[(r + s * t) % d] for t in range(d)])

def is_filled(w): return len(set(w)) <= 3

class Deg:
    def __init__(self, d):
        self.d = d; self.seqs = sequences(d); self.idx = {w: i for i, w in enumerate(self.seqs)}
        self.G = dihedral(d)
        # perm[g][i] = index of act(seqs[i], g)
        self.perm = [[self.idx[act(w, g)] for w in self.seqs] for g in self.G]
        self.filled = [i for i, w in enumerate(self.seqs) if is_filled(w)]
        self.unfilled = [i for i, w in enumerate(self.seqs) if not is_filled(w)]
        # dihedral orbits
        seen = {}; self.orbits = []
        for i in range(len(self.seqs)):
            if i in seen: continue
            orb = sorted({p[i] for p in self.perm}); k = len(self.orbits); self.orbits.append(orb)
            for j in orb: seen[j] = k
        self.orbit_of = seen

def load(path_list, degs=(5, 6, 7), maxorder=99, minorder=0):
    """yield (deg, order, gentri_index, hole, size, {pattern string: count})"""
    for fn in path_list:
        for l in open(fn):
            o = json.loads(l)
            if o["deg"] not in degs or not (minorder <= o["order"] <= maxorder): continue
            for size, pc in o["classes"]: yield o["deg"], o["order"], o["gentri_index"], o["hole"], size, pc
