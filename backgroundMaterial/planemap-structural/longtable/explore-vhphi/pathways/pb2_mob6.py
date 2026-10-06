"""[exploratory] Line A: k-mobility at degree-5 and degree-6 holes; failure patterns; radius by hole degree.
k-mobility: from hole h, reach hole y (chosen neighbour) by <= k Kempe swaps in G-h then one slide (y's colour a
singleton on N(h)), or meet a fill on the way. Exact over all canonical states on T4, order 14, A_3;
pentakis (order 32, all deg-5 holes are (6^5)) sampled by random Kempe walks from one colouring."""
import sys, time, random
from collections import Counter, defaultdict
from pb2_lib import *
t0 = time.process_time()

def cyc_link(adj, h):
    L = sorted(adj[h]); out = [L[0]]; prev = None
    while len(out) < len(L):
        cur = out[-1]
        nxt = [w for w in adj[cur] & adj[h] if w != prev and w not in out]
        prev = cur; out.append(min(nxt))
    return out

def pattern(col, link, y):
    i = link.index(y); w = [col[link[(i + j) % len(link)]] for j in range(len(link))]
    # canonical up to colour renaming and reflection fixing y
    best = None
    for ww in (w, [w[0]] + w[1:][::-1]):
        mp = {}; s = ''.join('abcd'[mp.setdefault(c, len(mp))] for c in ww)
        best = s if best is None or s < best else best
    return best

def run(name, adj, sample=None):
    deg = {u: len(adj[u]) for u in adj}
    print(f"== {name}: n={len(adj)}, degree counts {dict(Counter(deg.values()))}")
    for d in sorted(set(deg.values())):
        holes = [h for h in adj if deg[h] == d]
        hist = defaultdict(Counter); pat = defaultdict(Counter); radmax = {}
        for h in holes:
            if sample is None:
                dist, idx, nb = radius_table(adj, h); cols = list(idx.values())
                radmax[h] = max(dist.values())
            else:
                cols = sample(adj, h); dist = None
            link = cyc_link(adj, h)
            for c in cols:
                if free(adj, c, h): continue
                for y in adj[h]:
                    r = move_cost(adj, c, h, y, 2)
                    tag = 'none<=2' if r is None else f"{r[0]}{r[1]}"
                    hist[deg[y]][tag] += 1
                    if d == 6:
                        p = pattern(c, link, y)
                        pat[p]['ok<=1' if (r is not None and r[1] <= 1) else ('ok2' if r is not None else 'none<=2')] += 1
        print(f"  holes of degree {d}: {len(holes)}" + (f"; max pure radius per hole {sorted(Counter(radmax.values()).items())} (radius:#holes)" if radmax else ''))
        for dy in sorted(hist):
            tot = sum(hist[dy].values())
            print(f"    neighbour degree {dy}: {tot} (state,neighbour) pairs; cost hist {dict(sorted(hist[dy].items()))}")
        if d == 6 and pat:
            print("    deg-6 link patterns (y first; a=y's colour), outcome counts:")
            for p, cnt in sorted(pat.items()):
                print(f"      {p}: {dict(cnt)}")
    return

def sample_states(n_samples=150, seed=1):
    def f(adj, h):
        rnd = random.Random(seed + h)
        # start from one colouring of G-h: greedy via colourings_H is too big; use DSATUR-ish backtrack on G-h
        vs = sorted(u for u in adj if u != h); col = {}
        def rec(i):
            if i == len(vs): return True
            u = vs[i]
            for c in range(4):
                if all(col.get(w) != c for w in adj[u]):
                    col[u] = c
                    if rec(i + 1): return True
                    del col[u]
            return False
        assert rec(0)
        out = {}; c = dict(col)
        for _ in range(n_samples * 5):
            cs = comps_H(adj, c, {h}); a, b, K = rnd.choice(cs); c = swap(c, a, b, K)
            k = key(canon(c)); out.setdefault(k, canon(c))
            if len(out) >= n_samples: break
        return list(out.values())
    return f

if __name__ == '__main__':
    for name, adj in graphs(): run(name, adj)
    print("cpu so far", round(time.process_time() - t0, 1))
    P = pentakis()
    run('pentakis (32), SAMPLED <=150 distinct states per hole by random Kempe walk', P, sample=sample_states())
    print("cpu", round(time.process_time() - t0, 1))
