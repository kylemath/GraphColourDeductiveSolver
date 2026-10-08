"""Item 1: independent check of TrackH/lp_general_min.txt (and optionally other cex files).
Usage: python3 rv_cex.py FILE [FILE...]"""
import sys
from collections import Counter, defaultdict
import rv_core as R


def check(line):
    name, adj = R.parse_line(line)
    n = len(adj)
    h = 0
    x = adj[0]
    print(f"== {name}: n={n}, edges={sum(map(len, adj)) // 2}")
    print("  simple-graph errors:", R.validate_simple(adj))
    li = R.link_info(adj, h, x)
    print("  Pent (link = adj[0] in cyclic order):", li['pent'], " chords x_i x_{i+2}:", li['chords'],
          " (induced 5-cycle)" if not li['chords'] else " (NOT induced)")
    print("  link degrees:", [len(adj[v]) for v in x], " deg(h)=", len(adj[h]))
    # triangle data (relevant to (F1)-(F3)): faces at h exist iff link edges exist
    S = [set(a) for a in adj]
    tri_per_edge = Counter()
    for u in range(n):
        for v in adj[u]:
            if u < v:
                tri_per_edge[len(S[u] & S[v])] += 1
    print("  edges by #triangles containing them:", dict(sorted(tri_per_edge.items())))

    cols = R.colourings(adj, h)
    print("  proper 4-colourings of G-h (absolute):", len(cols))
    idx = {c: i for i, c in enumerate(cols)}
    # union-find over Kempe steps
    par = list(range(len(cols)))

    def f(i):
        while par[i] != i:
            par[i] = par[par[i]]
            i = par[i]
        return i
    kdeg = {}
    for i, c in enumerate(cols):
        nb = R.kempe_neighbours(adj, h, c)
        imgs = set()
        for _, _, d in nb:
            assert d in idx, "Kempe image not proper?!"
            par[f(i)] = f(idx[d])
            if R.canon(d) != R.canon(c):
                imgs.add(R.canon(d))
        kdeg[R.canon(c)] = len(imgs)
    classes = defaultdict(list)
    for i in range(len(cols)):
        classes[f(i)].append(cols[i])
    print("  Kempe classes (absolute sizes):", sorted(len(v) for v in classes.values()))
    result = {}
    for root, cl in classes.items():
        reps = sorted({R.canon(c) for c in cl})
        nf = sum(1 for c in cl if R.filled(c, x))
        closed_under_renaming = len(cl) == 24 * len(reps)
        tally = Counter()
        infos = {}
        for c in reps:
            inf = R.state_info(adj, h, x, c)
            infos[c] = inf
            if inf is None:
                tally['filled'] += 1
                continue
            for k in ('DL', 'D1', 'D2', 'P1', 'P2', 'P3', 'LP1', 'LP2', 'LP1odd', 'LP2odd',
                      'handshakeA', 'handshakeB', 'handshakeM', 'inA', 'inB'):
                tally[k] += bool(inf[k])
            tally['counts=' + str(R.pair_counts(adj, h, x, c, inf))] += 1
            tally['rigid'] += R.is_rigid(adj, h, x, c, inf)
        # pi orbit structure up to renaming
        pimg = {}
        for c in reps:
            inf = infos[c]
            p = R.pi_map(adj, h, x, c, inf) if inf else None
            pimg[c] = R.canon(p) if p is not None else None
        repset = set(reps)
        cyc_lens = []
        seen = set()
        for c in reps:
            if c in seen:
                continue
            # walk
            path = [c]
            cur = pimg[c]
            while cur is not None and cur not in path and cur in repset:
                path.append(cur)
                cur = pimg[cur]
            if cur == c:
                cyc_lens.append(len(path))
                seen.update(path)
        print(f"  class: abs={len(cl)} reps={len(reps)} closed-under-renaming={closed_under_renaming} "
              f"filled(abs)={nf}")
        print("    tallies over reps:", dict(tally))
        print("    pi-cycles (lengths, up to renaming) fully inside class:", cyc_lens,
              " pi undefined at:", sum(1 for c in reps if pimg[c] is None),
              " pi leaves class:", sum(1 for c in reps if pimg[c] is not None and pimg[c] not in repset))
        print("    Kempe degree (distinct non-renaming images, up to renaming):",
              dict(Counter(kdeg[c] for c in reps)))
        # sigma: swap K_{alpha mu}(x_{j+2}); is it a pure renaming?
        sig = Counter()
        for c in reps:
            inf = infos[c]
            if inf is None:
                continue
            al, mu, A, B = inf['roles']
            X = [x[(inf['j'] + k) % 5] for k in range(5)]
            K = R.comp_of(adj, h, c, al, mu, X[2])
            sig['sigma_is_renaming' if R.canon(R.swap(c, al, mu, K)) == c else 'sigma_nontrivial'] += 1
        print("    sigma:", dict(sig))
        result[root] = (len(cl), len(reps), nf, cyc_lens, dict(tally))
    return result


if __name__ == '__main__':
    for fn in sys.argv[1:]:
        for line in open(fn):
            if line.strip():
                check(line)
