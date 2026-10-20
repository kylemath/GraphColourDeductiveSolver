"""Generate CXRing.lean (Long Table, 19 Oct 2026): every ring-X C entry of discharge/wheeldis/out/job30/k3x_C.cfast,
with the configuration its C verdict was computed on and one label per X-component.
Source of each configuration: as twoeng.py, the first loop/k*/ cfast block (sorted file order, C2 files and teamB
skipped) with an accepted C line for the name; its input line is read from the sibling .txt/.in (stem without
_cf.cfast/_cf.out/_fixedX.cfast), else from any .txt/.in in that folder, and must match the block header's r and m
exactly once.
Usage: python3 gen_cxring.py CXRing.lean > CXRing.new   (replaces the xrEntries block; header and theorems kept)"""
import os, re, sys, glob
W = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'discharge', 'wheeldis')
XR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..', '..',
                  'SolvingFrameworkPlan', 'docs', 'working', 'CGLUE-XRING-ENTRIES.txt')
names = {}; cur = None
for l in open(os.path.join(W, 'out', 'job30', 'k3x_C.cfast')):
    if not l.startswith(' '): cur = l.split()[0]; hdr = l
    elif 'C-REDUCIBLE' in l:
        m = re.search(r'X=\{([^}]*)\}', l)
        names.setdefault(cur, (m.group(1).split(','), re.search(r' r=(\d+) m=(\d+)', hdr).groups()))
files = sorted(f for f in glob.glob(os.path.join(W, 'loop', 'k[0-9]*', '*')) if os.path.isfile(f))
files = [f for f in files if 'C2' not in os.path.basename(f) and os.sep + 'teamB' not in f]
src = {}
for fn in files:
    cur = None; curkc = False
    try: lines = open(fn).read().splitlines()
    except UnicodeDecodeError: continue
    for line in lines:
        m = re.match(r'^([A-Za-z]\w*_\S+) r=\d+ ', line)
        if m: cur, curkc = m.group(1), 'mode=' in line; continue
        if cur and 'C-REDUCIBLE' in line and not curkc:
            mf = re.search(r'fixed X=(\{[^}]*\}) .*C-REDUCIBLE, leftover bad classes extending after contraction = 0$', line)
            if 'fixed X=' in line and not mf: continue
            if cur in names and cur not in src: src[cur] = fn
def confs_in(p, n):
    out = set()
    for line in open(p, errors='ignore'):
        t = line.split()
        if len(t) == 5 and t[0] == n and t[1].isdigit(): out.add(' '.join(t[1:]))
    return out
def isring(x): return any(e.startswith('R') or '-R' in e for e in x)
listed = [l.split()[0] for l in open(XR) if not l.startswith('#') and l.strip()]
xr = sorted(n for n in names if isring(names[n][0]))
order = listed + [n for n in xr if n not in listed]
def parse(s):
    r, m, ra, ia = s.split(); r = int(r); m = int(m)
    ra = [[] if g == '-' else list(map(int, g.split(','))) for g in ra.split(';')]
    ia = [[] if g == '-' else list(map(int, g.split(','))) for g in ia.split(';')]
    return r, m, ra, ia
arr = lambda L: "#[" + ", ".join("#[" + ", ".join(map(str, g)) + "]" for g in L) + "]"
items = []
for n in order:
    fn = src[n]; d = os.path.dirname(fn)
    stem = re.sub(r'_(cf\.cfast|cf\.out|fixedX\.cfast)$', '', os.path.basename(fn))
    got = set()
    for e in ('.txt', '.in'):
        if os.path.exists(os.path.join(d, stem + e)): got |= confs_in(os.path.join(d, stem + e), n)
    if not got:
        for f in os.listdir(d):
            if f.endswith('.txt') or f.endswith('.in'): got |= confs_in(os.path.join(d, f), n)
    got = sorted(g for g in got if g.split()[:2] == list(names[n][1]))
    assert len(got) == 1, (n, fn, got)
    r, m, ra, ia = parse(got[0])
    par = {}
    def f(x):
        par.setdefault(x, x)
        while par[x] != x: x = par[x]
        return x
    eqR = []; eqI = []
    for e in names[n][0]:
        p, q = e.split('-'); P = (p[0], int(p[1:])); Q = (q[0], int(q[1:]))
        par[f(P)] = f(Q)
        if P[0] == 'R': eqR.append((P[1], Q[1]))
        elif Q[0] == 'R': eqR.append((Q[1], P[1]))
        else: eqI.append((Q[1], P[1]))
    ids = {}
    lab = lambda v: ids.setdefault(f(v), len(ids))
    lbl = [lab(('I', a)) for a in range(m)] + [lab(('R', t)) for t in range(r)]
    items.append('  { name := "%s", src := "%s", X := "%s",\n    cf := {\n      name := "%s", r := %d, m := %d,\n'
                 '      ringAdj := %s,\n      intAdj := %s },\n    eqR := %s, eqI := %s,\n    lbl := %s }' % (
        n, os.path.relpath(fn, W), ','.join(names[n][0]), n, r, m, arr(ra), arr(ia),
        "[" + ", ".join("(%d, %d)" % p for p in eqR) + "]", "[" + ", ".join("(%d, %d)" % p for p in eqI) + "]", lbl))
cur = open(sys.argv[1]).read()
i = cur.rindex("/-- The ", 0, cur.index(" ring-X C entries of `k3x_C.cfast`"))
j = cur.index("/-- **Every ring-X entry")
block = ("/-- The %d ring-X C entries of `k3x_C.cfast` (%d in `CGLUE-XRING-ENTRIES.txt`, then %d admitted since). -/\n"
         "def xrEntries : List XRData := [\n" % (len(items), len(listed), len(items) - len(listed)))
block += ",\n".join(items) + "]\n\n"
sys.stdout.write(cur[:i] + block + cur[j:])
