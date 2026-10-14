"""B8b (exploratory): sphere triangulations from layered rings around a centre vertex u.

A layered disc is given by the centre degree d and, ring by ring, the degree of each ring vertex.  The in-count of a
ring vertex (edges to the previous ring) is determined by the previous strip; out = deg - in - 2.  The strip between
ring k and ring k+1 is the word  prod_j ('O' * (out_j - 1) + 'I')  (O-triangles with apex v_j, then the I-triangle
on edge v_j v_{j+1}); ring k+1 has length sum_j (out_j - 1).  A ring whose vertices all have out = 1 is closed by a
fan to one last vertex.  Faces are oriented consistently, so rot[] is a planar rotation system (ball.py format).

close(...) finishes a disc by a randomised shrinking schedule (5s spread evenly, degrees 5..7), retried until
ball.class_check passes.  Used by lone8.py for the explicit patches."""
import sys, os, random
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
import ball


class Layered:
    def __init__(self, d):
        self.n = 1; self.tris = []; self.rings = [[0]]; self.deg = {0: d}
        z = list(range(1, d + 1)); self.n += d
        for t in range(d): self.tris.append((z[(t + 1) % d], z[t], 0))
        self.rings.append(z); self.inn = {x: 1 for x in z}

    def ring(self): return self.rings[-1]

    def add_ring(self, degs):
        """degs: degree of each vertex of the current outer ring (same order)."""
        R = self.ring(); a = len(R)
        out = [degs[j] - self.inn[R[j]] - 2 for j in range(a)]
        assert all(o >= 1 for o in out), ('out < 1', degs, [self.inn[x] for x in R])
        for j in range(a): self.deg[R[j]] = degs[j]
        b = sum(o - 1 for o in out)
        if b == 0:                                  # fan to one vertex
            c = self.n; self.n += 1
            for j in range(a): self.tris.append((R[j], R[(j + 1) % a], c))
            self.deg[c] = a; self.rings.append([c]); return
        Z = list(range(self.n, self.n + b)); self.n += b
        inn = {z: 1 for z in Z}; t = 0
        for j in range(a):
            for _ in range(out[j] - 1):
                self.tris.append((Z[(t + 1) % b], Z[t], R[j])); t += 1
            self.tris.append((R[j], R[(j + 1) % a], Z[t % b])); inn[Z[t % b]] += 1
        # the I-triangle on v_j v_{j+1} has apex Z[t]; the first apex z_0 also gets the last I: counted above
        # in-count correction: each z counted 1 (own) + I-triangles with apex z; but z_t gets +1 for every I with
        # apex z_t, and inn initialised to 1 already counts one edge too many when z has no I: recompute exactly.
        self.rings.append(Z)
        self.inn = self._inn(R, Z)

    def _inn(self, R, Z):
        Rs = set(R); adj = {z: set() for z in Z}
        for tr in self.tris:
            for x in tr:
                if x in adj:
                    for y in tr:
                        if y in Rs: adj[x].add(y)
        return {z: len(adj[z]) for z in Z}

    def rot(self):
        nxt = [dict() for _ in range(self.n)]
        for a, b, c in self.tris:
            nxt[a][b] = c; nxt[b][c] = a; nxt[c][a] = b
        rot = []
        for x in range(self.n):
            s = next(iter(nxt[x])); r = [s]; y = nxt[x][s]
            while y != s: r.append(y); y = nxt[x][y]
            assert len(r) == len(nxt[x])
            rot.append(r)
        return rot


def close(L, rng, maxtries=2000, deg_fn=None):
    """Finish layered disc L (outer ring open) into a sphere; returns rot or None.  Strategy per ring: choose the
    number of 5s so the ring shrinks by about 6, spread them evenly; when the ring is short, fan."""
    import copy
    for _ in range(maxtries):
        M = copy.deepcopy(L); ok = True
        while True:
            R = M.ring(); a = len(R); inn = [M.inn[x] for x in R]
            if all(i >= 2 for i in inn) and 5 <= a <= 7 and rng.random() < 0.7:
                M.add_ring([i + 3 for i in inn]); break
            base = [i + 4 for i in inn]                     # out = 2 -> contributes in==1:+1? (out-1 = 1)
            # out_j - 1 = deg - in - 3; base gives 1 each -> next length a; want a - k
            k = min(a - 5, max(1, int(round(a / 6.0 + rng.uniform(-1, 1)))) + 3)
            if a <= 9: k = a - rng.choice([5, 6, 7])
            k = max(0, min(k, a))
            cand = [j for j in range(a) if inn[j] >= 2]
            if len(cand) < k: k = len(cand)
            rng.shuffle(cand); step = []
            # spread: pick every (len/k)-th candidate after sorting
            cand.sort(); off = rng.randrange(max(1, len(cand)))
            if k > 0:
                sel = set(cand[(off + int(i * len(cand) / k)) % len(cand)] for i in range(k))
            else: sel = set()
            degs = [base[j] - (1 if j in sel else 0) for j in range(a)]
            if any(dg < 5 for dg in degs) or any(dg > 7 for dg in degs): ok = False; break
            try: M.add_ring(degs)
            except AssertionError: ok = False; break
            if len(M.ring()) == 1: break
            if len(M.rings) > 60: ok = False; break
        if not ok: continue
        rot = M.rot()
        if min(len(r) for r in rot) < 5: continue
        cc = ball.class_check(rot)
        if cc['in_class']: return rot, M
    return None
