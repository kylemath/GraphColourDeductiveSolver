"""Second engine for Job 7: the Python reference (4square kempe_engine.HoleGame, as in boundary/ring_levels.py) on census
holes, with the same regions as bnd.cpp.  Prints one JSON line per hole in bnd's format (aggregates per region kind).
usage: ref_check.py CENSUSFILE [max_lines] [--hole h]"""
import sys, os, json, collections
sys.path.insert(0, os.path.expanduser('~/4square'))
from kempe_engine import HoleGame

def regions(rot, h):
    n = len(rot); d = [-1] * n; d[h] = 0; q = collections.deque([h])
    while q:
        u = q.popleft()
        for w in rot[u]:
            if d[w] < 0: d[w] = d[u] + 1; q.append(w)
    dmax = max(d); F = set()
    for u in range(n):
        r = rot[u]
        for i in range(len(r)): F.add(tuple(sorted((u, r[i], r[(i + 1) % len(r)]))))
    fd = {f: min(d[x] for x in f) for f in F}; fmax = max(fd.values()); out = []
    for f in sorted(F):
        if fd[f] == fmax: out.append(('faceMax', set(f)))
        elif fd[f] >= 3: out.append(('face3', set(f)))
    out.append(('shell1', {v for v in range(n) if d[v] == dmax})); out.append(('shell2', {v for v in range(n) if d[v] >= dmax - 1}))
    s3 = {v for v in range(n) if d[v] >= 3}
    if s3: out.append(('dist3', s3))
    return out, dmax, fmax

def run(name, rot, h):
    n = len(rot); H = HoleGame(n, [list(r) for r in rot], h, rot[h])
    regs, dmax, fmax = regions(rot, h)
    agg = {}
    chains = [H.chains(c) for c in H.states]
    for kind, R in regs:
        nb = [[] for _ in range(H.S)]
        for k, c in enumerate(H.states):
            for K in chains[k]:
                if K['web'] or not (K['set'] & R): continue
                nb[k].append(H.index[H.canon(H.flip(c, K))])
        dist = [0 if f else -1 for f in H.filled]; q = collections.deque(k for k in range(H.S) if H.filled[k])
        while q:
            k = q.popleft()
            for t in nb[k]:
                if dist[t] < 0: dist[t] = dist[k] + 1; q.append(t)
        fail = sum(1 for k in range(H.S) if not H.filled[k] and H.dF[k] >= 0 and dist[k] < 0)
        ok = [k for k in range(H.S) if not H.filled[k] and dist[k] >= 0]
        mdr = max([dist[k] for k in ok], default=0); ext = max([dist[k] - H.dF[k] for k in ok], default=0)
        a = agg.setdefault(kind, [0, 0, 0, 0, 0]); a[0] += 1; a[1] += bool(fail); a[2] = max(a[2], fail); a[3] = max(a[3], mdr); a[4] = max(a[4], ext)
    unf = [k for k in range(H.S) if not H.filled[k]]
    return dict(name=name, hole=h, n=n, S=H.S, unfilled=len(unf), unreachF=sum(1 for k in unf if H.dF[k] < 0),
                dFmax=max([H.dF[k] for k in unf if H.dF[k] >= 0], default=0), dmax=dmax, fmax=fmax, **agg)

if __name__ == '__main__':
    lim = int(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[2].isdigit() else 10 ** 9
    oh = int(sys.argv[sys.argv.index('--hole') + 1]) if '--hole' in sys.argv else None
    for i, l in enumerate(open(sys.argv[1])):
        if i >= lim: break
        p = l.split(); rot = [[int(x) for x in r.split(',')] for r in p[2].split(';')]
        for h in range(len(rot)):
            if len(rot[h]) == 5 and (oh is None or h == oh): print(json.dumps(run(p[0], rot, h)), flush=True)
