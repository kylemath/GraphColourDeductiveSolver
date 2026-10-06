"""EXPLORATORY. Shortest pure escape from each locked class (hole x fixed, swaps in T - x),
and what the first chord-breaking swap looks like. Usage: python3 lock_escape.py PLANTRI GRAPH_INDEX"""
import subprocess, sys
from collections import Counter, deque
import tilley_apex as TA, vhphi_explore as E, lock_anatomy as LA

def main():
    plantri, gi = sys.argv[1], int(sys.argv[2])
    order = int(sys.argv[3]) if len(sys.argv) > 3 else 17
    line = subprocess.run([plantri, "-m5", str(order), "-a"], capture_output=True, text=True).stdout.splitlines()[gi]
    rot = TA.parse(line); n = len(rot); adj = [set(r) for r in rot]
    lens = Counter(); firsts = Counter(); n_pairs = 0; exits = Counter()
    for x in range(n):
        if len(rot[x]) != 5: continue
        legal = {f[0] for f in E.legal_fans(rot, x, adj)}
        for i, y in enumerate(rot[x]):
            if i not in legal: continue
            G = [set(a) for a in adj]; G[x].discard(y); G[y].discard(x)
            allc, comp = LA.classes(G, n)
            sep = {comp[c] for c in allc if c[x] != c[y]}
            locked = {comp[c] for c in allc if c[x] == c[y]} - sep
            if not locked: continue
            ring = rot[x]
            far = (ring[(i+2) % 5], ring[(i+3) % 5])      # chord ends of the apex fan with apex y
            for k in sorted(locked):
                n_pairs += 1
                members = {c for c in allc if comp[c] == k}
                best = None
                for c0 in members:
                    st = list(c0); st[x] = E.HOLE; st = tuple(st)
                    par = {st: None}; q = deque([st]); hit = None
                    while q and hit is None:
                        u = q.popleft()
                        if E.filled(rot, u): hit = u; break
                        for d in E.kempe_moves(rot, u):
                            if d not in par: par[d] = u; q.append(d); 
                    if hit is None: continue
                    path = []; u = hit
                    while u is not None: path.append(u); u = par[u]
                    path = path[::-1]
                    if best is None or len(path) < len(best): best = path
                L = len(best) - 1; lens[L] += 1
                # first state on the path where a chord of the fan is monochromatic or colouring leaves S
                lt = None
                for t, u in enumerate(best):
                    mono = [u[a] == u[b] for a, b in ((y, far[0]), (y, far[1]))]
                    if any(mono): lt = (t, tuple(mono)); break
                firsts[lt] += 1
    print("locked classes:", n_pairs)
    print("shortest pure escape length (swaps at hole x), over locked classes:", dict(sorted(lens.items())))
    print("first step at which a fan chord becomes monochromatic (step index, (chord1,chord2)):", dict(firsts))

if __name__ == "__main__":
    main()
