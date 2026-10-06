"""[exploratory] Line A, part 2 (T4, order14, A_3; exact):
(1) where the degree-6 move failures (>2 swaps) sit: hole, state radius, link pattern, singleton count;
(2) hole-move graph M_k (one hole-move = <=1 swap then one slide to ANY neighbour; deg5-only variant for comparison):
    from every radius-4 state at a degree-5 hole, least number of hole-moves to a state of pure radius <=2
    (any hole) or a filled state; and whether a radius-greedy walk cycles."""
import time
from collections import Counter, deque
from pb2_lib import *
from pb2_mob6 import cyc_link, pattern
t0 = time.process_time()

def holemoves(adj, c, h, allow):
    out = set()
    cand = [c] + [swap(c, a, b, K) for a, b, K in comps_H(adj, c, {h})]
    for c2 in cand:
        cs = [c2[w] for w in adj[h]]
        for y in adj[h]:
            if len(adj[y]) in allow and cs.count(c2[y]) == 1:
                n = dict(c2); col = n.pop(y); n[h] = col
                out.add((y, key(canon(n))))
    return out

def run(name, adj):
    deg = {u: len(adj[u]) for u in adj}
    R = {}
    for h in adj:
        dist, idx, nb = radius_table(adj, h)
        for k, r in dist.items(): R[(h, k)] = r
        assert len(dist) == len(idx)
    # (1) failures
    fails = Counter()
    for h in adj:
        if deg[h] != 6: continue
        link = cyc_link(adj, h)
        for k in [k for (hh, k) in R if hh == h]:
            c = dict(k)
            if free(adj, c, h): continue
            for y in adj[h]:
                if move_cost(adj, c, h, y, 2) is None:
                    cs = [c[w] for w in link]
                    fails[(h, R[(h, k)], pattern(c, link, y), cs.count(c[y]))] += 1
    hm = {h: max(r for (hh, k), r in R.items() if hh == h) for h in adj}
    print(f"== {name}: per-hole max pure radius {hm}")
    print("  deg-6 move failures (>2 swaps): (hole, state radius, pattern, #y-colour in link) -> count:", dict(fails))
    # (2) walk
    starts = [(h, k) for (h, k), r in R.items() if deg[h] == 5 and r == max(R[(hh, kk)] for (hh, kk) in R if deg[hh] == 5)]
    top = R[starts[0]]
    for allow, lab in [({5}, 'deg5-only'), ({5, 6}, 'deg5+6')]:
        dh = Counter(); greedy = Counter()
        for s in starts:
            # BFS
            seen = {s}; fr = [s]; d = 0; found = None
            while fr and found is None and d <= 6:
                for (h, k) in fr:
                    if R[(h, k)] <= 2: found = d; break
                if found is not None: break
                nf = []
                for (h, k) in fr:
                    for t in holemoves(adj, dict(k), h, allow):
                        if t not in seen: seen.add(t); nf.append(t)
                fr = nf; d += 1
            dh[found] += 1
            # greedy: move to the successor of least radius (ties: smallest key); stop at R<=2; detect cycle
            cur = s; vis = {cur}; steps = 0; res = None
            while res is None:
                if R[cur] <= 2: res = f"ok{steps}"; break
                nx = sorted(holemoves(adj, dict(cur[1]), cur[0], allow), key=lambda t: (R[t], str(t)))
                if not nx: res = 'stuck'; break
                cur = nx[0]; steps += 1
                if cur in vis: res = 'cycle'; break
                vis.add(cur)
        # one more: total elementary cost = hole moves*(<=2) + remaining radius vs top
            greedy[res] += 1
        print(f"  {lab}: {len(starts)} states of radius {top} at deg-5 holes; least #hole-moves to R<=2: {dict(dh)}; R-greedy outcome: {dict(greedy)}")

for name, adj in graphs(): run(name, adj)
print("cpu", round(time.process_time() - t0, 1))
