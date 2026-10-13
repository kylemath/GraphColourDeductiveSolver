"""faceconst.py -- read planecount outputs (SIG lines) and extract the sharp face constants.
For each class and each face signature (multiset of face sizes >= 4) we have min P(G,4) over all
embedded graphs with n <= N. Reports
  * min of (P/24) / 2^miss  (miss = sum (|f|-3))  -> is the 2^miss bound sharp/valid per class
  * for pure signatures (j faces all of size k): min P/24, compare to 2^{j(k-3)}
  * best uniform base alpha: min over signatures of (P/24)^(1/miss)
  * LP-free check of per-face constants c_k: smallest (P/24)/prod 2^{|f|-3}
Usage: python3 faceconst.py pc-4.txt ... pc-9.txt"""
import sys, re, collections
best = {}
for fn in sys.argv[1:]:
    n = int(re.search(r'(?:pc|out)-(\d+)', fn).group(1))
    for line in open(fn):
        if not line.startswith('SIG'): continue
        m = re.match(r'SIG cls=(\d) faces>=4:([\d ]*)\| minP=(\d+) count=(\d+) witness tri=(\d+) edges:(.*)', line)
        cls = int(m.group(1)); faces = tuple(int(x) for x in m.group(2).split()); P = int(m.group(3))
        key = (cls, faces)
        if key not in best or P < best[key][0]: best[key] = (P, n, int(m.group(5)), m.group(6).strip())
names = {1: 'connected', 2: '2-connected', 3: '2-conn, all 2-cuts are edges', 4: '3-connected'}
for cls in (1, 2, 3, 4):
    items = [(faces, v) for (c, faces), v in best.items() if c == cls]
    if not items: continue
    print(f"=== class {cls} ({names[cls]}): {len(items)} face signatures")
    r = min(((v[0] / 24) / 2 ** sum(k - 3 for k in f), f, v) for f, v in items)
    print(f"  min (P/24)/2^miss = {r[0]:.4f} at faces {r[1]} n={r[2][1]} P={r[2][0]}")
    worst = sorted(((v[0] / 24) / 2 ** sum(k - 3 for k in f), f, v[1], v[0]) for f, v in items)[:8]
    for w in worst: print(f"    ratio {w[0]:.4f} faces {w[1]} n={w[2]} P={w[3]}")
    # pure signatures
    pure = collections.defaultdict(dict)
    for f, v in items:
        if f and len(set(f)) == 1: pure[f[0]][len(f)] = v
    for k in sorted(pure):
        row = '  '.join(f"j={j}: P/24={pure[k][j][0]/24:g} (2^(j(k-3))={2**(j*(k-3))}, n={pure[k][j][1]})" for j in sorted(pure[k]))
        print(f"  pure k={k}: {row}")
    # per face size: best constant if only one non-triangular face
    print("  single-face constant c_k = min P/24 with exactly one face of size k (others triangles):",
          {k: pure[k][1][0] / 24 for k in sorted(pure) if 1 in pure[k]})
    # tight signatures (ratio exactly 1)
    tight = sorted(f for f, v in items if v[0] == 24 * 2 ** sum(k - 3 for k in f))
    print(f"  signatures attaining equality P = 24*2^miss: {len(tight)}; e.g. {tight[:12]}")
    # minimal ratio per number of non-triangular faces j and per face size present
    bymax = collections.defaultdict(lambda: 9e9)
    for f, v in items:
        if f: bymax[max(f)] = min(bymax[max(f)], (v[0] / 24) / 2 ** sum(k - 3 for k in f))
    print("  min ratio by largest face size:", {k: round(x, 4) for k, x in sorted(bymax.items())})
