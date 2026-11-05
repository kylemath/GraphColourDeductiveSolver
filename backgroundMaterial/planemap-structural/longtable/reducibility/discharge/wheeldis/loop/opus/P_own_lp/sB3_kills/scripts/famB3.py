# B3 family generator for extended-stack receiver rows (d = 7).
# usage: python3 famB3.py ROWS RMAX OUT.tsv FAMS [KT.npy] [L3T+1.json,L3T-1.json]
#   ROWS: lines "weight LK SV" (weight = any number used for coverage ranking; '#' comments)
#   FAMS: letters among F (plain u-centred 2-ball windows: f-name route), A (kill6: private of a link 6, window inside
#         the kill6 key), L (l3q: private a2 of a link 7 next to apex a, c = w_{j+s} <= 6, a <= 6, window inside the l3q
#         payee window), P (extra fives at privates / ring-3 next to a five, singles; cell route).
# Letter-9 vertices (>= 9) never enter a window (strict rule: an exact degree never matches letter 9).
# writes OUT.tsv: code ring m n5 family name kcline nrows weight rows(';'-joined, first 20)
import sys, json, collections, time, itertools
import numpy as np
from gen3 import build, windows, ring3_candidates
LET = (5, 6, 7, 8, 9)
ROWS = []
for l in open(sys.argv[1]):
    if not l.strip() or l.startswith('#'): continue
    f = l.split(); ROWS.append((float(f[0]), f[1], f[2]))
RMAX = int(sys.argv[2]); OUT = sys.argv[3]; FAMS = sys.argv[4]
KTF = sys.argv[5] if len(sys.argv) > 5 else '/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s77_k6patch/tab/kill/kill6_U7.npy'
L3F = sys.argv[6] if len(sys.argv) > 6 else '/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s77_k6patch/tab/tab_1.json,/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s77_k6patch/tab/tab_-1.json'
KT = np.load(KTF)
L3T = {}
for fn in L3F.split(','):
    for k, v in json.load(open(fn)).items():
        sg, wd, ao = k.split(); L3T[(int(sg),) + tuple(int(c) for c in wd) + tuple(int(c) for c in ao)] = v[0]
out = {}; cover = collections.defaultdict(dict)
def add(fam, ws, rid, wt):
    for code, v in ws:
        if code not in out: out[code] = (v[0], v[1], v[4], fam, v[2], v[3])
        cover[code][rid] = wt
def canonkey(a, b, e, f, s0, s1, s2, s3): return min((a, b, e, f, s0, s1, s2, s3), (f, e, b, a, s3, s2, s1, s0))
famseen = {}
t0 = time.time()
for rid, (wt, LK, SV) in enumerate(ROWS):
    n = len(LK); assert n == 7
    w = [int(c) for c in LK]; s = [int(c) for c in SV]
    adj, rot, name, deg, Z3, inv = build(LK, SV)
    small = {k for k, v in deg.items() if v <= 8}
    rtag = '%s/%s' % (LK, SV)
    if 'F' in FAMS:
        add('F:%s' % rtag, windows(LK, SV, RMAX=RMAX, allowed=small), rid, wt)
    if 'A' in FAMS:
        for j in range(n):
            if w[j] != 6: continue
            key = (w[(j - 2) % n], w[(j - 1) % n], w[(j + 1) % n], w[(j + 2) % n], s[(j - 2) % n], s[(j - 1) % n], s[j], s[(j + 1) % n])
            ck = canonkey(*key); m = 31 & ~int(KT[tuple(x - 5 for x in key)])
            p = ('p', j, 1)
            allowed = ({('u',), p} | {('w', (j + o) % n) for o in range(-2, 3)} | {('s', (j + o) % n) for o in range(-2, 2)})
            allowed = {x for x in allowed if x == p or x in small}
            for L in (5, 6):
                if not (m >> LET.index(L)) & 1: continue
                tag = 'A:%s:%d' % (''.join(map(str, ck)), L)
                if tag in famseen:   # same key: windows identical up to symmetry; only record coverage
                    for code in famseen[tag]: cover[code][rid] = wt
                    continue
                ws = windows(LK, SV, pdeg={p: L}, RMAX=RMAX, must=[p], allowed=allowed | {p})
                famseen[tag] = [c for c, _ in ws]; add(tag, ws, rid, wt)
    if 'L' in FAMS:
        for j in range(n):
            if w[j] != 7: continue
            for sg in (1, -1):
                c = w[(j + sg) % n]; w2, w3, w4 = (w[(j + k * sg) % n] for k in (2, 3, 4))
                ap, o = (s[j], s[(j - 1) % n]) if sg == 1 else (s[(j - 1) % n], s[j])
                if c > 6 or ap > 6: continue
                m = L3T[(sg, c, w2, w3, w4, ap, o)]
                a2 = ('p', j, 2) if sg == 1 else ('p', j, 1)
                apn = ('s', j) if sg == 1 else ('s', (j - 1) % n); on = ('s', (j - 1) % n) if sg == 1 else ('s', j)
                assert inv[apn] in adj[inv[a2]], (LK, SV, j, sg)
                allowed = {('u',), ('w', j), apn, on} | {('w', (j + k * sg) % n) for k in (1, 2, 3, 4)}
                allowed = {x for x in allowed if x in small}
                for L in (5, 6):
                    if not (m >> LET.index(L)) & 1: continue
                    fk = (c, w2, w3, w4, ap, o)   # sigma-free family key (the table is mirror-symmetric in sigma)
                    tag = 'L:%s:%d' % (''.join(map(str, fk)), L)
                    if tag in famseen:
                        for code in famseen[tag]: cover[code][rid] = wt
                        continue
                    ws = windows(LK, SV, pdeg={a2: L}, RMAX=RMAX, must=[a2], allowed=allowed | {a2})
                    famseen[tag] = [cc for cc, _ in ws]; add(tag, ws, rid, wt)
    if 'P' in FAMS:
        ps = [v for v in name.values() if v[0] == 'p' and any(deg.get(name.get(y)) == 5 for y in adj[inv[v]])]
        for p in ps:
            if w[p[1]] == 6 and 'A' in FAMS: continue
            tag = 'P:%s:%s=5' % (rtag, ''.join(map(str, p)))
            try: ws = windows(LK, SV, pdeg={p: 5}, RMAX=RMAX, must=[p], allowed=small | {p})
            except (AssertionError, ValueError): continue
            add(tag, ws, rid, wt)
    if rid % 50 == 0: print(rid, rtag, len(out), '%.0fs' % (time.time() - t0), flush=True)
with open(OUT, 'w') as f:
    for code, v in sorted(out.items(), key=lambda kv: (kv[1][0], -sum(cover[kv[0]].values()))):
        cv = cover[code]
        f.write('%s\t%d\t%d\t%d\t%s\t%s\t%s\t%d\t%.6f\t%s\n' % ((code,) + v + (len(cv), sum(cv.values()), ';'.join(str(r) for r in sorted(cv)[:20]))))
print(OUT, len(out), sorted(collections.Counter(v[0] for v in out.values()).items()))
print('families', collections.Counter(v[3].split(':')[0] for v in out.values()))
