"""Long Table core: independent stdlib implementation of the mass-macro contract.

Contract (JointMassMacroExecutionPlan.md): T is a simple spherical triangulation with
minimum degree five and n vertices; r is a degree-five root; B = N_T(r).  For a proper
four-colouring c of T - r,
    p(c) = max(0, number of colours on B - 3)
    q(c) = sum over the six colour pairs and every bichromatic component K meeting B of |K minus B|^2
    R(c) = (6 n^2 + 1) p(c) + q(c).
A move exchanges the two colours on one whole bichromatic component (components missing B
included).  Good(T, r): every deletion colouring with p = 1 has a sequence of at most two
moves, components recomputed after the first, ending at a strictly smaller R.

Colourings are enumerated modulo global colour renaming (first-occurrence canonical form in
vertex order).  This is an exponential test harness for a polynomially evaluable formula,
not a solver.  No status word is asserted by any output of this module.
"""
import itertools
import json
from pathlib import Path

PAIRS = list(itertools.combinations(range(4), 2))
HERE = Path(__file__).resolve().parent
FIXTURES = HERE.parent


# ---------------------------------------------------------------- graphs

def parse_ascii(line):
    """Plantri ASCII rotation -> list of neighbour lists, validated as a triangulation."""
    n, code = line.strip().split(" ", 1)
    rot = [[ord(ch) - 97 for ch in row] for row in code.split(",")]
    assert len(rot) == int(n)
    validate_triangulation(rot)
    return rot


def rotation_from_fixture(path):
    data = json.loads(Path(path).read_text())
    rot = [list(data["rotation"][str(v)]) for v in sorted(data["vertices"])]
    validate_triangulation(rot)
    return rot


def validate_triangulation(rot):
    n = len(rot)
    for v, ns in enumerate(rot):
        assert len(set(ns)) == len(ns) and v not in ns and len(ns) >= 5, v
        assert all(v in rot[w] for w in ns), v
    edges = sum(len(ns) for ns in rot) // 2
    assert edges == 3 * n - 6
    seen, faces = set(), 0
    for v, ns in enumerate(rot):
        for w in ns:
            if (v, w) in seen:
                continue
            dart, length = (v, w), 0
            while dart not in seen:
                seen.add(dart)
                length += 1
                a, b = dart
                dart = (b, rot[b][(rot[b].index(a) + 1) % len(rot[b])])
            assert dart == (v, w) and length == 3
            faces += 1
    assert n - edges + faces == 2


def relabel(rot, perm):
    """Rotation of the isomorphic copy in which vertex v is renamed perm[v]."""
    out = [None] * len(rot)
    for v, ns in enumerate(rot):
        out[perm[v]] = [perm[w] for w in ns]
    return out


def degree_five(rot):
    return [v for v, ns in enumerate(rot) if len(ns) == 5]


# ---------------------------------------------------------------- colourings

def canon(colours):
    seen = {}
    return tuple(seen.setdefault(x, len(seen)) for x in colours)


def deletion_colourings(rot, r):
    """All proper 4-colourings of T - r modulo colour renaming, as tuples over vertex_order."""
    V = [v for v in range(len(rot)) if v != r]
    pos = {v: i for i, v in enumerate(V)}
    earlier = [[pos[w] for w in rot[v] if w != r and pos[w] < i] for i, v in enumerate(V)]
    out, cur = [], [0] * len(V)

    def go(i, top):
        if i == len(V):
            out.append(tuple(cur))
            return
        blocked = {cur[j] for j in earlier[i]}
        for a in range(min(3, top + 1) + 1):
            if a not in blocked:
                cur[i] = a
                go(i + 1, max(top, a))

    go(0, -1)
    return V, out


# ---------------------------------------------------------------- mass formula and moves

class RootState:
    """Everything needed to evaluate the contract at one root, with complete move lists."""

    def __init__(self, rot, r):
        assert len(rot[r]) == 5
        self.rot, self.r, self.n = rot, r, len(rot)
        self.V, self.C = deletion_colourings(rot, r)
        self.pos = {v: i for i, v in enumerate(self.V)}
        self.adj = [[self.pos[w] for w in rot[v] if w != r] for v in self.V]
        self.B = [self.pos[w] for w in rot[r]]
        self.Bset = set(self.B)
        self.index = {c: i for i, c in enumerate(self.C)}
        self.scale = 6 * self.n * self.n + 1
        self.info = [self._analyse(c) for c in self.C]

    def _analyse(self, c):
        q, moves = 0, []
        for a, b in PAIRS:
            pending = {i for i, x in enumerate(c) if x in (a, b)}
            while pending:
                seed = min(pending)
                pending.discard(seed)
                comp, stack = {seed}, [seed]
                while stack:
                    i = stack.pop()
                    for j in self.adj[i]:
                        if j in pending:
                            pending.discard(j)
                            comp.add(j)
                            stack.append(j)
                if comp & self.Bset:
                    q += len(comp - self.Bset) ** 2
                swapped = canon([b if (i in comp and x == a) else a if (i in comp and x == b) else x
                                 for i, x in enumerate(c)])
                moves.append(((a, b), tuple(sorted(self.V[i] for i in comp)), self.index[swapped]))
        p = max(0, len({c[i] for i in self.B}) - 3)
        assert q <= 6 * self.n * self.n
        return {"p": p, "q": q, "R": self.scale * p + q, "moves": moves}

    def check_closure(self):
        """Properness, move closure and reversibility of the enumerated quotient."""
        for c in self.C:
            assert all(c[i] != c[j] for i in range(len(c)) for j in self.adj[i])
        for i, info in enumerate(self.info):
            for _, _, t in info["moves"]:
                assert any(u == i for _, _, u in self.info[t]["moves"]), (i, t)

    def rank(self, i):
        return (self.info[i]["p"], self.info[i]["q"])

    def descent(self, i, macro=2):
        """Return None if a <= macro decreasing sequence exists from state i, else a full witness."""
        start = self.info[i]["R"]
        for m1, k1, t in self.info[i]["moves"]:
            if self.info[t]["R"] < start:
                return None
        if macro >= 2:
            for m1, k1, t in self.info[i]["moves"]:
                for m2, k2, u in self.info[t]["moves"]:
                    if self.info[u]["R"] < start:
                        return None
        return self.witness(i, macro)

    def witness(self, i, macro):
        info = self.info[i]
        one = [{"pair": m, "component": k, "successor": self.C[t], "rank": self.rank(t)}
               for m, k, t in info["moves"]]
        out = {"vertex_order": self.V, "coloring": self.C[i], "rank": self.rank(i),
               "integer_rank": info["R"], "one_step": one}
        if macro >= 2:
            out["two_step_rank_sets"] = [
                {"first_pair": m, "first_component": k,
                 "second_ranks": sorted({self.rank(u) for _, _, u in self.info[t]["moves"]})}
                for m, k, t in info["moves"]]
        return out

    def first_decreasing_macro(self, i):
        start = self.info[i]["R"]
        for m1, k1, t in self.info[i]["moves"]:
            if self.info[t]["R"] < start:
                return [(m1, k1, self.C[t], self.rank(t))]
        for m1, k1, t in self.info[i]["moves"]:
            for m2, k2, u in self.info[t]["moves"]:
                if self.info[u]["R"] < start:
                    return [(m1, k1, self.C[t], self.rank(t)), (m2, k2, self.C[u], self.rank(u))]
        return None

    def target_distance_max(self):
        """Full-state BFS distance to p = 0 (diagnostic only; never used as a rank)."""
        dist = {i: 0 for i, info in enumerate(self.info) if info["p"] == 0}
        frontier = list(dist)
        while frontier:
            nxt = []
            for i in frontier:
                for _, _, t in self.info[i]["moves"]:
                    if t not in dist:
                        dist[t] = dist[i] + 1
                        nxt.append(t)
            frontier = nxt
        return None if len(dist) < len(self.C) else max(dist.values())

    def mass_summary(self, keep_witness=True):
        non_target = [i for i, info in enumerate(self.info) if info["p"] == 1]
        one = [i for i in non_target if self.descent(i, 1) is not None]
        two = [i for i in non_target if self.descent(i, 2) is not None]
        out = {"root": self.r, "boundary_cyclic_order": list(self.rot[self.r]),
               "coloring_orbits": len(self.C), "non_target": len(non_target),
               "empty_family": len(self.C) == 0, "vacuous_non_target": len(non_target) == 0,
               "one_swap_stuck": len(one), "two_swap_stuck": len(two),
               "good_macro2": len(two) == 0}
        if keep_witness:
            if one:
                out["one_swap_first_stuck"] = self.witness(one[0], 1)
                out["one_swap_stuck_colorings"] = [self.C[i] for i in one]
                out["one_swap_stuck_escapes"] = [self.first_decreasing_macro(i) for i in one]
            if two:
                out["two_swap_first_stuck"] = self.witness(two[0], 2)
        return out


# ---------------------------------------------------------------- (sigma, beta) robust game

def sigma_beta(rot, r):
    """The fixed one-bit robust boundary-action game, reimplemented from BitSearchReport.md.

    Label-sensitive by design: the boundary is rotated to start at its minimum label, colours
    are canonicalised boundary-first, and beta asks whether the minimum remaining label lies
    in the canonical {1,3} component meeting the boundary.
    """
    V, C = deletion_colourings(rot, r)
    pos = {v: i for i, v in enumerate(V)}
    adj = [[pos[w] for w in rot[v] if w != r] for v in V]
    B = list(rot[r])
    B = B[B.index(min(B)):] + B[:B.index(min(B))]
    Bi = [pos[v] for v in B]
    order = Bi + [i for i in range(len(V)) if i not in set(Bi)]
    index = {c: i for i, c in enumerate(C)}
    keys, actions = [], []
    minv = pos[min(V)]
    for c in C:
        mp = {}
        for i in order:
            mp.setdefault(c[i], len(mp))
        cc = [mp[x] for x in c]
        parts, acts, bit = [], {}, False
        for a, b in PAIRS:
            pending = {i for i, x in enumerate(cc) if x in (a, b)}
            part = []
            while pending:
                seed = min(pending)
                pending.discard(seed)
                comp, stack = {seed}, [seed]
                while stack:
                    i = stack.pop()
                    for j in adj[i]:
                        if j in pending:
                            pending.discard(j)
                            comp.add(j)
                            stack.append(j)
                hit = tuple(k for k, i in enumerate(Bi) if i in comp)
                if hit:
                    if (a, b) == (1, 3) and minv in comp:
                        bit = True
                    part.append(hit)
                    t = canon([b if (i in comp and x == a) else a if (i in comp and x == b) else x
                               for i, x in enumerate(cc)])
                    acts[(a, b, hit)] = index[t]
            parts.append(tuple(sorted(part)))
        keys.append(((tuple(cc[i] for i in Bi), tuple(parts)), bit))
        actions.append(acts)
    groups = {}
    for i, k in enumerate(keys):
        groups.setdefault(k, []).append(i)
    winning = {k for k in groups if len(set(k[0][0])) <= 3}
    rounds = 0
    while True:
        new = set()
        for k, ids in groups.items():
            if k in winning:
                continue
            common = set(actions[ids[0]])
            for i in ids[1:]:
                common &= actions[i].keys()
            if any(all(keys[actions[i][act]] in winning for i in ids) for act in common):
                new.add(k)
        if not new:
            break
        winning |= new
        rounds += 1
    return {"root": r, "boundary": B, "coloring_orbits": len(C), "groups": len(groups),
            "losing_groups": len(groups) - len(winning), "winning_rounds": rounds}
