# Task B: exact insertion width k*(L) = max over level pairs (a,b) of min_pi (dist(a, pi b) - 1) on the straight
# degree-6 cylinder, via exact BFS on the full row graph (bfs.c).  Measures: old (tm.tau<=1, some base point) and
# intrinsic strip half-width tau_strip (ic.py convention), with and without the cap |t|<=2.
import sys, math, json, subprocess, collections, time, itertools
sys.path.insert(0, '/mnt/project-files/multiscale/bandfill'); sys.path.insert(0, '/mnt/project-files/multiscale/closing/round2')
from lev import gen_level, rot, PERMS
from tm import rows, tau, walk, n2
BFS = '/tmp/claude-0/-home-claude/6412a0d0-5a16-5792-8fcd-75c860b4d69c/scratchpad/bfs'
S3 = math.sqrt(3)
E = lambda p: ((p[0]-p[1]/2)/2, p[1]*S3/4)
def tau_strip(r):
    H = walk(r); t = (H[-1][0]-H[0][0], H[-1][1]-H[0][1])
    if t == (0, 0): return round(tau(r)[0], 3), 0.0
    tx, ty = E(t); nt = math.hypot(tx, ty); nx, ny = -ty/nt, tx/nt
    pr = [E(h)[0]*nx+E(h)[1]*ny for h in H]
    return round((max(pr)-min(pr))/2, 3), round(math.sqrt(n2(t)), 3)
def canon(r): return min(tuple(p[c] for c in rot(r, k)) for p in PERMS for k in range(len(r)))
def kstar(L, lev, maxd=12):
    lev = sorted(set(lev)); can = sorted(set(canon(r) for r in lev))
    inp = f"{L} {maxd} {len(can)} {len(lev)}\n" + "\n".join("".join(map(str, r)) for r in can) + "\n" + "\n".join("".join(map(str, r)) for r in lev) + "\n"
    out = subprocess.run([BFS], input=inp, capture_output=True, text=True).stdout.split()
    hist = collections.Counter(); worst = []
    for a, line in zip(can, out):
        for j, ch in enumerate(line):
            k = 'inf' if ch == 'x' else ord(ch)-ord('0')-1
            hist[k] += 1
        mx = max((ord(c)-49 if c != 'x' else 99) for c in line)
        worst.append((mx, a, lev[max(range(len(line)), key=lambda j: (ord(line[j]) if line[j] != 'x' else 999))]))
    worst.sort(reverse=True)
    fin = [k for k in hist if k != 'inf']
    return dict(nlevel=len(lev), ncanon=len(can), hist={str(k): v for k, v in sorted(hist.items(), key=lambda x: (x[0] == 'inf', x[0] if x[0] != 'inf' else 0))},
                kstar_finite=max(fin) if fin else None, n_inf=hist.get('inf', 0), worst=[(w[0], ''.join(map(str, w[1])), ''.join(map(str, w[2]))) for w in worst[:3]])
if __name__ == '__main__':
    L = int(sys.argv[1]); modes = sys.argv[2].split(',')
    t0 = time.time()
    if 'old' in modes:
        r = kstar(L, gen_level(L)); r.update(L=L, mode='old tau<=1', sec=round(time.time()-t0, 1)); print(json.dumps(r), flush=True)
    if 'strip' in modes:
        R = rows(L); ts = {r: tau_strip(r) for r in R}
        tmin = min(v[0] for v in ts.values()); cap = [v[0] for v in ts.values() if v[1] <= 2.001]; tminc = min(cap)
        print(json.dumps(dict(L=L, tmin=tmin, tmin_cap2=tminc, tdist=sorted(collections.Counter(v for v in ts.values() if v[0] <= 1.001).items())[:30])), flush=True)
        for name, T, c in [('strip T=Tmin', tmin, 99), ('strip T=Tmin_cap, |t|<=2', tminc, 2.001), ('strip T=1, |t|<=2', 1.0, 2.001), ('strip T=1, no cap', 1.0, 99)]:
            lev = [r for r in R if ts[r][0] <= T+1e-6 and ts[r][1] <= c]
            t1 = time.time(); r = kstar(L, lev); r.update(L=L, mode=name, T=T, sec=round(time.time()-t1, 1)); print(json.dumps(r), flush=True)
