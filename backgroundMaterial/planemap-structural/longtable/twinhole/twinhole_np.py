"""Vectorised twin-hole BFS (same model as twinhole.py): joint states are an S x S grid (side-1 colouring i, side-2
colouring j, both with the glued face coloured (0,1,2)). One BFS level:
  interior moves on side 1:  row i -> row a  for each interior move i -> a
  interior moves on side 2:  column j -> column b
  face moves (6 colour pairs): (i, j) -> (T_p[i], T_p[j]); T_p is an involution, so new |= F[T_p][:, T_p].
Usage: python3 twinhole_np.py MAP.json [far|near]  -> one JSON line."""
import sys, json, time, collections
import numpy as np
import twinhole as th


def spread_rows(F, src, dst, S):
    """out[a, :] |= F[i, :] for every edge i -> a, restricted to frontier rows"""
    out = np.zeros_like(F)
    live = F.any(axis=1)
    keep = live[src]
    s, d = src[keep], dst[keep]
    order = np.argsort(d, kind='stable'); s, d = s[order], d[order]
    for k in range(0, len(s), 4096):
        ss, dd = s[k:k + 4096], d[k:k + 4096]
        np.logical_or.at(out, dd, F[ss])
    return out


def main(path, which='far'):
    name, rot, hole = th.load(path)
    n = len(rot); adj = [set(r) for r in rot]; link = rot[hole]
    hd = [-1] * n; hd[hole] = 0; q = collections.deque([hole])
    while q:
        u = q.popleft()
        for w in adj[u]:
            if hd[w] < 0: hd[w] = hd[u] + 1; q.append(w)
    fs = [f for f in th.faces(rot) if len(f) == 3 and hole not in f]
    D = max(fs, key=lambda f: (min(hd[u] for u in f), sum(hd[u] for u in f))) if which == 'far' else \
        min(fs, key=lambda f: (sum(hd[u] for u in f), f))
    t0 = time.time()
    cols = th.colourings(adj, hole, D); S = len(cols)
    inner, T, filled = th.side_tables(adj, hole, D, link, cols)
    dG = np.array(th.bfs(S, lambda i: inner[i] + T[i], [i for i in range(S) if filled[i]]), dtype=np.int16)
    src = np.array([i for i in range(S) for a in inner[i]], dtype=np.int64)
    dst = np.array([a for i in range(S) for a in inner[i]], dtype=np.int64)
    Tp = np.array(T, dtype=np.int64).T            # 6 x S
    fl = np.array(filled)
    dist = np.full((S, S), -1, dtype=np.int16)
    F = np.outer(fl, fl); dist[F] = 0; seen = F.copy(); level = 0
    while F.any():
        new = spread_rows(F, src, dst, S)
        new |= spread_rows(F.T.copy(), src, dst, S).T
        for p in range(6):
            new |= F[Tp[p]][:, Tp[p]]
        new &= ~seen
        level += 1; dist[new] = level; seen |= new; F = new
        print('level', level, int(new.sum()), round(time.time() - t0, 1), file=sys.stderr, flush=True)
    # sequential rule: fill a hole as soon as its rim is down to 3 (free action), then the other. Once a hole is filled
    # its side is a full triangulation glued at a triangle, so (projection lemma) the rest costs exactly dG of the other
    # side. dS(i, j) = min over reachable (i', j') of path length + terminal cost; bucket BFS from the terminal costs.
    BIG = np.int16(30000)
    term = np.full((S, S), BIG, dtype=np.int16)
    term[fl, :] = np.minimum(term[fl, :], dG[None, :])
    term[:, fl] = np.minimum(term[:, fl], dG[:, None])
    dS = term.copy(); k = 0
    while True:
        F = dS == k
        if not F.any() and k > int(dG.max()) + 1: break
        new = spread_rows(F, src, dst, S)
        new |= spread_rows(F.T.copy(), src, dst, S).T
        for p in range(6):
            new |= F[Tp[p]][:, Tp[p]]
        upd = new & (dS > k + 1)
        dS[upd] = k + 1; k += 1
        if k > 60: break
    histS = collections.Counter(dS.ravel().tolist())
    hist = collections.Counter(dist.ravel().tolist())
    big = np.maximum.outer(dG, dG)
    exc = collections.Counter((dist - big)[dist >= 0].ravel().tolist())
    sym = dist[np.arange(S), np.arange(S)]
    deep = np.argwhere(dist == dist.max())[:5].tolist()
    print(json.dumps(dict(map=name, n=n, face=which, D=D, S=S, joint=S * S, secs=round(time.time() - t0, 1),
        maxG=int(dG.max()), maxJ=int(dist.max()), unfillJ=int((dist < 0).sum()), histJ=dict(sorted(hist.items())),
        excess_over_maxside=dict(sorted(exc.items())),
        sym_vs_dG=dict(sorted(collections.Counter(zip(dG.tolist(), sym.tolist())).items())) and
                  {f'{a}->{b}': c for (a, b), c in sorted(collections.Counter(zip(dG.tolist(), sym.tolist())).items())},
        deepest_pairs=[[i, j, int(dG[i]), int(dG[j])] for i, j in deep],
        maxSeq=int(dS.max()), histSeq=dict(sorted(histS.items())),
        seq_le_joint=bool((dS <= np.where(dist < 0, BIG, dist)).all()), seq_ne_joint=int((dS != dist).sum()),
        deepest_seq=[[int(i), int(j), int(dG[i]), int(dG[j]), int(dist[i, j])] for i, j in np.argwhere(dS == dS.max())[:5]])))


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else 'far')
