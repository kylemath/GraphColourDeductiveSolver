# smallest abstract graph (cubic except v of degree 5, rotation at v) with a Fig8 state violating A5v
import random, itertools, json, sys
def search(n, trials, rng):
    for _ in range(trials):
        # random multigraph-free configuration: v=0 joined to 1..5; stubs: vertices 1..5 need 2 more, others 3
        stubs = []
        for x in range(1, n):
            stubs += [x] * (2 if x <= 5 else 3)
        rng.shuffle(stubs)
        E = set((0, x) for x in range(1, 6)); ok = True
        for i in range(0, len(stubs), 2):
            a, b = stubs[i], stubs[i + 1]
            if a == b or (min(a, b), max(a, b)) in E: ok = False; break
            E.add((min(a, b), max(a, b)))
        if not ok: continue
        adj = {x: set() for x in range(n)}
        for a, b in E: adj[a].add(b); adj[b].add(a)
        fs = [1, 2, 3, 4, 5]; rng.shuffle(fs)
        res = []
        def rec(used, cur):
            free = [x for x in range(n) if x not in used]
            if not free: res.append(frozenset(cur)); return
            x = free[0]
            for y in adj[x]:
                if y not in used: rec(used | {x, y}, cur + [(min(x, y), max(x, y))])
        rec(frozenset(), [])
        part = None
        for M in res:
            k = next(i for i in range(5) if (0, fs[i]) in M)
            def reach(src):
                seen = {src}; st = [src]
                while st:
                    a = st.pop()
                    for b in adj[a]:
                        if b == 0 or (min(a, b), max(a, b)) in M: continue
                        if b not in seen: seen.add(b); st.append(b)
                return seen
            X = reach(fs[(k + 1) % 5]); Y = reach(fs[(k + 2) % 5])
            if fs[(k - 1) % 5] in X and fs[(k + 3) % 5] in Y and fs[(k + 2) % 5] not in X \
                    and all(u in X or u in Y for u in range(1, n)) and fs[k] not in X:
                return {'n': n, 'E': sorted(E), 'fs': fs, 'M': sorted(M), 'k': k, 'X': sorted(X), 'Y': sorted(Y)}
    return None
rng = random.Random(5)
for n in (6, 8, 10, 12):
    r = search(n, 20000, rng)
    if r: print(json.dumps(r)); json.dump(r, open('anti.json', 'w')); break
    else: print('none at', n)
