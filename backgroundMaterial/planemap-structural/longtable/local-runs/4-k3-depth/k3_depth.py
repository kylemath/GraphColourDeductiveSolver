#!/usr/bin/env python3
"""[exploratory] Local compute item 4: K3 at order 26, plantri index 5401, hole 13 (the k = 4 state of k3-summary.jsonl).
Phi = (lock_size, lock_dist), definitions as conjecture-K3/README.md: for an unfilled state with repeat c(x_j) = c(x_{j+2}),
m = x_{j+1}, a = x_{j+3}, b = x_{j+4}: lock_size = |{mu,A}-comp of m| + |{mu,B}-comp of m|; lock_dist = BFS length m -> a
inside the first (0 if a not in it) + the same for m -> b in the second. Filled states (link on <= 3 colours) count as success.
Enumerates EVERY sequence of 1..4 non-trivial swaps (a swap is non-trivial if the image differs from the current state up to
renaming; repeated states along a sequence are allowed) from the stored state, on the concrete colouring. For each depth:
number of sequences, the set of end Phi values (with multiplicity), min lock_size, and the number of sequences whose end is
filled or has Phi < Phi(start) ("lowering"). A sequence is counted as lowering at depth k only if no proper prefix already
lowered (so "first lowering at depth k").  Plain Python, ../common/kempe_py.py; cross-checked with k3.cpp (unchanged).
usage: python3 k3_depth.py > k3-depth-results.json"""
import json, os, sys, itertools, subprocess, tempfile
from collections import Counter
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(H, "..", "common"))
from kempe_py import Space, plantri_ascii, adj_from_rot
K3 = os.path.join(H, "..", "..", "studio-explore", "conjecture-K3")

rec = [json.loads(l) for l in open(os.path.join(K3, "k3-26-counterexample-holes.jsonl"))]
summ = [json.loads(l) for l in open(os.path.join(K3, "k3-summary.jsonl"))]
fc = [s for s in summ if s.get("order") == 26][0]["first_counterexample"]
assert fc["index"] == 5401 and fc["hole"] == 13
line = fc.get("graph") or "26 bcdef,afghic,abijd,acjke,adklf,aelmgb,bfmnh,bgnoi,bhopjc,cipqrkd,djrsle,ekstumf,flung,gmuoh,hnuvwxpi,ioxqj,jpxyr,jqyzsk,krztl,lszvu,ltvonm,outzw,ovzyx,owyqp,qxwzr,rywvts"
rot = plantri_ascii(line); hole = 13; adj = adj_from_rot(rot); link = list(rot[hole])
col0 = {int(k): v for k, v in fc["colouring"].items()}
S = Space(adj, hole, link=link); S.build_graph(); dist = S.dist_to_filled()


def phi(c):
    lc = [c[x] for x in link]
    if len(set(lc)) <= 3: return None  # filled
    j = [j for j in range(5) if lc[j] == lc[(j + 2) % 5]][0]
    m, a, b = link[(j + 1) % 5], link[(j + 3) % 5], link[(j + 4) % 5]
    size = dd = 0
    for t in (a, b):
        cols = (c[m], c[t]); seen = {m: 0}; q = [m]
        for x in q:
            for y in adj[x]:
                if y != hole and c[y] in cols and y not in seen: seen[y] = seen[x] + 1; q.append(y)
        size += len(seen); dd += seen.get(t, 0)
    return (size, dd)


def comps(c):
    out = []
    for p, q in itertools.combinations(range(4), 2):
        Vs = {u for u in c if c[u] in (p, q)}; sn = set()
        for s in sorted(Vs):
            if s in sn: continue
            K = {s}; st = [s]; sn.add(s)
            while st:
                x = st.pop()
                for y in adj[x]:
                    if y in Vs and y not in sn: sn.add(y); K.add(y); st.append(y)
            if len(K) < len(Vs): out.append(((p, q), sorted(K)))  # whole-pair swaps are renamings (trivial)
    return out


def apply(c, pq, K):
    p, q = pq; d = dict(c)
    for u in K: d[u] = q if c[u] == p else p
    return d


phi0 = phi(col0); s0 = S.state_of(col0)
res = {"graph": line, "hole": hole, "link": link, "start_phi": phi0, "start_dist": dist[s0], "states": len(S.states), "rho": max(dist)}
frontier = [((), col0)]; depth = {}; example = None; first_lower_depth = None
allseq = open(os.path.join(H, "k3-depth-sequences-1to3.jsonl"), "w")  # every sequence of length 1..3 with its end Phi
for k in range(1, 5):
    nxt = []; phis = Counter(); lowering = 0; nseq = 0; minsize = None; filled_n = 0
    for seq, c in frontier:
        for pq, K in comps(c):
            d = apply(c, pq, K); f = phi(d); nseq += 1
            low = f is None or f < phi0
            if f is None: filled_n += 1; phis["filled"] += 1
            else: phis[str(f)] += 1; minsize = f[0] if minsize is None else min(minsize, f[0])
            step = {"pair": list(pq), "component": K, "phi_after": f if f is not None else "filled"}
            if k <= 3: allseq.write(json.dumps({"depth": k, "end_phi": step["phi_after"], "lowering": f is None or f < phi0, "seq": list(seq) + [step]}) + "\n")
            if low:
                lowering += 1
                if example is None: example = list(seq) + [step]
            else: nxt.append((seq + (step,), d))
    depth[k] = {"sequences": nseq, "sequences_first_lowering_here": lowering, "end_filled": filled_n,
                "min_lock_size_among_nonfilled_ends": minsize, "end_phi_histogram": dict(sorted(phis.items())),
                "distinct_states_at_end": len({S.state_of(c) for _, c in nxt})}
    if lowering and first_lower_depth is None: first_lower_depth = k
    frontier = nxt
allseq.close(); res["by_depth"] = depth; res["least_k_by_enumeration"] = first_lower_depth; res["one_lowering_sequence"] = example
# check the example
c = dict(col0)
for st in example: c = apply(c, st["pair"], st["component"])
assert all(c[u] != c[w] for u in c for w in adj[u] if w != hole)
res["example_end_phi"] = phi(c); res["example_end_dist"] = dist[S.state_of(c)]
# cross-check with k3.cpp (unchanged studio code), compiled at ../common/k3
seen, F = set(), []
for v, nb in enumerate(rot):
    for i in range(len(nb)):
        f = (v, nb[(i + 1) % len(nb)], nb[i]); kk = min((f, f[1:] + f[:1], f[2:] + f[:2]))
        if kk not in seen: seen.add(kk); F.append(f)
with tempfile.NamedTemporaryFile("w", suffix=".tri", delete=False) as fh:
    fh.write("%d %d\n" % (len(rot), len(F)) + "".join("%d %d %d\n" % f for f in F)); p = fh.name
res["k3cpp"] = json.loads(subprocess.run([os.path.join(H, "..", "common", "k3"), p, str(hole), "4"], capture_output=True, text=True).stdout)
os.unlink(p)
print(json.dumps(res, indent=1))
