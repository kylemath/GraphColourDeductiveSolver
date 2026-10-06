"""EXPLORATORY. Fan switching at a locked class (hole x fixed). Long Table 2026-10-05.
For each locked class (apex y), take its shortest pure escape, look at the state after the
FIRST swap. Which fans at x admit it (chords proper)? For each such fan j (apex y_j) is that
state Tilley-separable for fan j (class of the colouring of T - x y_j with x := c(y_j) contains
a colouring with c(x) != c(y_j))?  Usage: python3 fan_switch.py PLANTRI GRAPH_INDEX [ORDER]"""
import subprocess, sys
from collections import Counter, deque
import tilley_apex as TA, vhphi_explore as E, lock_anatomy as LA

def sep_set(G, n):
    allc = [TA.canon(c) for c in TA.colourings(G, n)]
    good = {c for c in allc if True}
    sepc = {c for c in allc if c[0] is not None}  # placeholder, replaced below
    return allc

def main():
    plantri, gi = sys.argv[1], int(sys.argv[2])
    order = int(sys.argv[3]) if len(sys.argv) > 3 else 17
    line = subprocess.run([plantri, "-m5", str(order), "-a"], capture_output=True, text=True).stdout.splitlines()[gi]
    rot = TA.parse(line); n = len(rot); adj = [set(r) for r in rot]
    cache = {}
    def sep_colourings(x, y):
        if (x, y) in cache: return cache[(x, y)]
        G = [set(a) for a in adj]; G[x].discard(y); G[y].discard(x)
        allc = [TA.canon(c) for c in TA.colourings(G, n)]
        good = {c for c in allc if c[x] != c[y]}
        q = deque(good)
        while q:
            c = q.popleft()
            for d in TA.kempe_nbrs(G, c):
                if d not in good: good.add(d); q.append(d)
        cache[(x, y)] = good
        return good
    tally = Counter(); detail = Counter(); total = 0
    for x in range(n):
        if len(rot[x]) != 5: continue
        ring = rot[x]
        legal = {f[0] for f in E.legal_fans(rot, x, adj)}
        for i, y in enumerate(ring):
            if i not in legal: continue
            G = [set(a) for a in adj]; G[x].discard(y); G[y].discard(x)
            allc, comp = LA.classes(G, n)
            sep = {comp[c] for c in allc if c[x] != c[y]}
            locked = {comp[c] for c in allc if c[x] == c[y]} - sep
            for k in sorted(locked):
                members = {c for c in allc if comp[c] == k}
                best = None
                for c0 in members:
                    st = list(c0); st[x] = E.HOLE; st = tuple(st)
                    par = {st: None}; q = deque([st]); hit = None
                    while q and hit is None:
                        u = q.popleft()
                        if E.filled(rot, u): hit = u; break
                        for d in E.kempe_moves(rot, u):
                            if d not in par: par[d] = u; q.append(d)
                    if hit is None: continue
                    path = []; u = hit
                    while u is not None: path.append(u); u = par[u]
                    path = path[::-1]
                    if best is None or len(path) < len(best): best = path
                total += 1
                u1 = best[1]
                admitting = []; separable = []
                for j in range(5):
                    if j not in legal: continue
                    a0 = ring[j]; far = (ring[(j+2) % 5], ring[(j+3) % 5])
                    if u1[a0] != u1[far[0]] and u1[a0] != u1[far[1]]:
                        admitting.append(j)
                        st = list(u1); st[x] = u1[a0]
                        if TA.canon(st) in sep_colourings(x, a0): separable.append(j)
                tally[(len(admitting), len(separable))] += 1
                detail["state after swap 1 is admitted by >=1 other fan"] += bool(admitting)
                detail["... and separable for at least one admitting fan"] += bool(separable)
    print("locked classes:", total)
    print({k: v for k, v in detail.items()})
    print("(#admitting fans, #of those separable) -> count:", dict(sorted(tally.items())))

if __name__ == "__main__":
    main()
