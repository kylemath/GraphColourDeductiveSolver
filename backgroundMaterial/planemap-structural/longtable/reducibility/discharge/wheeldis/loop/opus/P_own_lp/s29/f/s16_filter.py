"""Stage 16 A' private filter (Opus). Forbidden set = round-44 RSST 582 (rsst_verdicts.txt verdict D2 or C2cons) +
every twoeng k3x name at 09d8ac38 (k3x_D / k3x_C files given), read as configurations from their kc lines (glob loop/k*/*),
exactly as explore's census50.py (3b08eef3). Containment = grow.embeddings (k42, unchanged): exact degrees, induced,
interior triangles onto faces.
LOCAL test at one link vertex w_j of a receiver u: u's 3-ball structure (rings.Layered) where only the window
w_{j-2..j+2} (letters), s_{j-2..j+1} (variables) and w_j's privates (variables) may hold interior vertices; every other
vertex (outside link / apexes / other privates, and u itself when U = 9) has degree 99 (never exact). A private value
is killed when an embedding needs only window letters plus that one private.
usage: python3 s16_filter.py EXDIR TD TC OUT [wj=6] [U=7,8,9] [one=a,b,e,f]"""
import sys, os, re, glob, itertools, collections, json, time
EX, TD, TC, OUT = sys.argv[1:5]
OPTS = dict(a.split('=') for a in sys.argv[5:])
LOOP = os.path.join(EX, 'backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop')
sys.path.insert(0, os.path.join(LOOP, 'k42'))
import grow
from rings import Layered
LET = (5, 6, 7, 8, 9); NEVER = 99
def registry():
    K44 = os.path.join(LOOP, 'k44')
    ok = {l.split()[0] for l in open(os.path.join(K44, 'rsst_verdicts.txt')) if not l.startswith('#') and
          ('verdict=D2' in l.split() or 'verdict=C2cons' in l.split())}
    assert len(ok) == 582
    kcn = [l.split()[0] for l in open(os.path.join(K44, 'rsst.txt')) if l.strip()]
    C = [(n,) + tuple(c[1:]) for n, c in zip(kcn, grow.rsst()) if n in ok]
    want = {l.split()[0] for l in open(TD) if re.match(r'^[epf]\d+_', l)} | \
           {l.split()[0] for l in open(TC) if re.match(r'^[epf]\d+_\S+ r=\d+ ', l)}
    got = {}; pat = re.compile(r'^([epf]\d+_\S+) (\d+) (\d+) (\S+) (\S+)$')
    for fn in sorted(glob.glob(os.path.join(LOOP, 'k[0-9]*', '*'))):
        if not os.path.isfile(fn): continue
        try:
            for l in open(fn):
                m = pat.match(l.rstrip('\n'))
                if m and m.group(1) in want and m.group(1) not in got: got[m.group(1)] = grow.kcline(l, 'explore')
        except UnicodeDecodeError: continue
    assert len(got) == len(want), (len(got), len(want))
    return C + list(got.values())
def build(D, LK):
    L = Layered(D); L.add_ring(list(LK))
    Wr = L.rings[1]; Z = L.ring(); adj = {}
    for a, b, c in L.tris:
        for x, y in ((a, b), (b, c), (c, a)): adj.setdefault(x, set()).add(y); adj.setdefault(y, set()).add(x)
    name = {0: ('u',)}
    for i, w in enumerate(Wr): name[w] = ('w', i)
    Wi = {w: i for i, w in enumerate(Wr)}; cnt = {}
    for z in Z:
        ws = sorted(Wi[x] for x in adj[z] if x in Wi)
        if len(ws) == 2:
            i, j = ws; name[z] = ('s', j if (i, j) == (0, D - 1) else i)
        else:
            i = ws[0]; cnt[i] = cnt.get(i, 0) + 1; name[z] = ('p', i, cnt[i])
    L.add_ring([9 for z in Z])
    adj = {}
    for a, b, c in L.tris:
        for x, y in ((a, b), (b, c), (c, a)): adj.setdefault(x, set()).add(y); adj.setdefault(y, set()).add(x)
    inv = {v: x for x, v in name.items()}
    pa = {x: {name[y] for y in adj[inv[x]] if y in name} for x in inv}
    pf = {frozenset(name[y] for y in f) for f in L.tris if all(y in name for y in f)}
    return list(inv), pa, pf
def local(C, U, win, wj, unk=NEVER, strict=True):
    """win = (a, b, e, f) letters of w_{j-2}, w_{j-1}, w_{j+1}, w_{j+2}; w_j = wj. Returns {req tuple over VAR: [names]}"""
    D = U if U < 9 else 10; j = 2
    LK = [9] * D; a, b, e, f = win
    for k, l in ((0, a), (1, b), (2, wj), (3, e), (4, f)): LK[k] = l
    LKs = [l if (k <= 4 or unk == NEVER) else unk for k, l in enumerate(LK)]   # structure letters of unknown link vertices
    P, pa, pf = build(D, LKs)
    UNKV = set()                                                               # unknown vertices: never part of a match
    fd = {('u',): U if U < 9 else NEVER}
    if U >= 9: UNKV.add(('u',))
    for i in range(D):
        fd[('w', i)] = LK[i] if (i <= 4 and LK[i] < 9) else NEVER
        if i > 4: fd[('w', i)] = unk; UNKV.add(('w', i))
    VAR = [('s', 0), ('s', 1), ('s', 2), ('s', 3)] + sorted(x for x in P if x[0] == 'p' and x[1] == j)
    for x in P:
        if x[0] in ('s', 'p') and x not in VAR: fd[x] = unk; UNKV.add(x)
    out = collections.defaultdict(list)
    for c in C:
        for e_ in grow.embeddings(c, P, pa, pf, fd):
            if strict and any(v in UNKV for u, v in e_): continue   # RELAY_SPEC 14': a constrained vertex on an unknown = no match
            req = dict((v, c[3][u]) for u, v in e_ if v not in fd)
            if not any(req.get(x) for x in VAR[4:]): continue      # must use a private of w_j
            if sum(1 for x in VAR[4:] if req.get(x)) > 1: continue   # single-private kills only
            out[tuple(req.get(x, 0) for x in VAR)].append(c[0])
    return VAR, out
if __name__ == '__main__':
    C = registry(); print('forbidden set: %d configurations' % len(C), flush=True)
    wj = int(OPTS.get('wj', '6')); Us = [int(x) for x in OPTS.get('U', '7,8,9').split(',')]
    wins = [tuple(int(x) for x in OPTS['one'].split(','))] if 'one' in OPTS else list(itertools.product(LET, repeat=4))
    res = {}; t0 = time.time(); n = 0
    for U in Us:
        for win in wins:
            VAR, out = local(C, U, win, wj, unk=int(OPTS.get('unk', '99')), strict=OPTS.get('strict', '1') == '1'); n += 1
            if out: res['%d %s' % (U, ''.join(map(str, win)))] = {''.join(str(k) for k in key): sorted(set(v))[:6] for key, v in out.items()}
            if n % 100 == 0: print('  %d windows %.0fs' % (n, time.time() - t0), flush=True)
    json.dump({'wj': wj, 'VAR': [list(map(str, x)) for x in VAR], 'kills': res}, open(OUT, 'w'))
    print('done %d windows, %d with kills, %.0fs' % (n, len(res), time.time() - t0))
def fullrow(C, D, LK, SV):
    """FULL 3-ball test on one receiver row (census50's structure: u, whole link LK, all apexes SV fixed; ring 2 = privates).
    Each private slot is tested on its own: that slot is the only free vertex, every other private has degree 99.
    Returns {(j, k): {value: [names]}}."""
    P, pa, pf = build(D, LK)
    base = {('u',): D}
    for i in range(D): base[('w', i)] = LK[i]; base[('s', i)] = SV[i]
    slots = sorted(x for x in P if x[0] == 'p'); out = {}
    for sl in slots:
        fd = dict(base)
        for x in slots:
            if x != sl: fd[x] = NEVER
        for c in C:
            for e_ in grow.embeddings(c, P, pa, pf, fd):
                req = dict((v, c[3][u]) for u, v in e_ if v not in fd)
                if req: out.setdefault(sl[1:], {}).setdefault(req[sl], set()).add(c[0])
    return out
