# B3 coordinator targets (18:10Z): C link family and B pattern supersets.
#  C = link class 5575757 (row 5757575/7755777 in canonical orientation 5575757/7775577); near-tight apex sets
#      [6789][6789][78]55[78][6789].  Family-wide windows read only u, the link and s3 = s4 = 5 (fixed in every near-tight row);
#      s2, s5 in {7,8} enter as a case split (one SV variant per value); s0, s1, s6 are never read, except s1 = 6 for the
#      l3q side of w2 (rows with s1 = 6 only).
#      CF  : F route (no private): kills every row of the class (or of the s2/s5 case).
#      CQ  : a2 of an l3q side of w4 (c = 5, a = 5; L3T key fixed in the class) at 5 or 6: plain L / L' entry valid class-wide.
#      CQ2 : a2 of the w2 side with apex s1 = 6 (c = w1 = 5), rows with s1 = 6.
#  B = rows 7577575/7555755 and 7577575/7565755: windows that contain Studio's A111 C pattern f7_..57575_...55.. (r11; in row
#      coordinates u, w4 w5 w6 w0 w1, s5 s6; f7_.575757_..55... r13 is the same plus w2).
#      BF  : F route supersets (whole-row kill).   BP : supersets plus one private of a 7 at 5 or 6 (mask kill).
# usage: python3 famCB.py RMAX OUT.tsv [C][B]
import sys, collections
from gen3 import build, windows
RMAX, OUT, WHICH = int(sys.argv[1]), sys.argv[2], (sys.argv[3] if len(sys.argv) > 3 else 'CB')
L3T = {}
import json
P = '/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s77_k6patch/tab/'
for fn in (P + 'tab_1.json', P + 'tab_-1.json'):
    for k, v in json.load(open(fn)).items():
        sg, wd, ao = k.split(); L3T[(int(sg),) + tuple(int(c) for c in wd) + tuple(int(c) for c in ao)] = v[0]
out = {}; cover = collections.defaultdict(dict)
def add(fam, ws, rtag, keep=None):
    n = 0
    for code, v in ws:
        if keep is not None and not keep(v[2]): continue
        if code not in out: out[code] = (v[0], v[1], v[4], fam, v[2], v[3]); n += 1
        cover[code][rtag] = 1
    print(fam, rtag, 'new', n, flush=True)
def mask(LK, SV, j, sg):
    w = [int(c) for c in LK]; s = [int(c) for c in SV]; n = len(w)
    c = w[(j + sg) % n]; w2, w3, w4 = (w[(j + k * sg) % n] for k in (2, 3, 4))
    ap, o = (s[j], s[(j - 1) % n]) if sg == 1 else (s[(j - 1) % n], s[j])
    return L3T[(sg, c, w2, w3, w4, ap, o)], (sg, c, w2, w3, w4, ap, o)
if 'C' in WHICH:
    LK = '5575757'
    fixed = {('u',)} | {('w', j) for j in range(7)} | {('s', 3), ('s', 4)}
    for x in '78':
        for y in '78':
            SV = '77%s55%s7' % (x, y); rt = '%s/%s' % (LK, SV)
            if x == y == '7':
                add('CF:%s' % LK, windows(LK, SV, RMAX=RMAX, allowed=fixed), rt)
            add('CF:%s:s2=%s,s5=%s' % (LK, x, y), windows(LK, SV, RMAX=RMAX, allowed=fixed | {('s', 2), ('s', 5)}), rt,
                keep=lambda nm: nm.split('_')[2][2] != '.' or nm.split('_')[2][5] != '.')
            m, key = mask(LK, SV, 4, 1)   # a2 = p(4,2), next to s4 (the w4 sides are mirror images)
            for L in (5, 6):
                if not (m >> (L - 5)) & 1: continue
                a2 = ('p', 4, 2)
                if x == y == '7':
                    add('CQ:%s:p42=%d' % (LK, L), windows(LK, SV, pdeg={a2: L}, RMAX=RMAX, must=[a2], allowed=fixed | {a2}), rt)
                add('CQ:%s:p42=%d:s2=%s,s5=%s' % (LK, L, x, y), windows(LK, SV, pdeg={a2: L}, RMAX=RMAX, must=[a2], allowed=fixed | {a2, ('s', 2), ('s', 5)}), rt,
                    keep=lambda nm: nm.split('_')[2][2] != '.' or nm.split('_')[2][5] != '.')
    for x in '78':
        SV = '76%s55%s7' % (x, x); rt = '%s/%s' % (LK, SV)   # s1 = 6: l3q side of w2 with sigma = -1 (c = w1, a = s1)
        m, key = mask(LK, SV, 2, -1)
        for L in (5, 6):
            if not (m >> (L - 5)) & 1: continue
            a2 = ('p', 2, 1)
            add('CQ2:%s:p21=%d:s1=6,s2=%s' % (LK, L, x), windows(LK, SV, pdeg={a2: L}, RMAX=RMAX, must=[a2, ('s', 1)], allowed=fixed | {a2, ('s', 1), ('s', 2)}), rt)
if 'B' in WHICH:
    pat = [('u',), ('w', 4), ('w', 5), ('w', 6), ('w', 0), ('w', 1), ('s', 5), ('s', 6)]
    for LK, SV in (('7577575', '7555755'), ('7577575', '7565755')):
        rt = '%s/%s' % (LK, SV)
        adj, rot, name, deg, Z3, inv = build(LK, SV)
        small = {k for k, v in deg.items() if v <= 8}
        ws = [(c, v) for c, v in windows(LK, SV, RMAX=RMAX, must=pat, allowed=small) if v[1] > len(pat)]
        add('BF:%s' % rt, ws, rt)
        ps = [v for v in name.values() if v[0] == 'p' and int(LK[v[1]]) <= 8]
        for p in ps:
            if not any(inv[x] in adj[inv[p]] for x in pat + [('w', 2), ('w', 3)] + [('s', j) for j in range(7)]): continue
            for L in (5, 6):
                ws = windows(LK, SV, pdeg={p: L}, RMAX=RMAX, must=pat + [p], allowed=small | {p})
                add('BP:%s:%s=%d' % (rt, ''.join(map(str, p)), L), ws, rt)
with open(OUT, 'w') as f:
    for code, v in sorted(out.items(), key=lambda kv: (kv[1][0], -kv[1][1])):
        cv = cover[code]
        f.write('%s\t%d\t%d\t%d\t%s\t%s\t%s\t%d\t%.6f\t%s\n' % ((code,) + v + (len(cv), float(len(cv)), ';'.join(sorted(cv)))))
print(OUT, len(out), sorted(collections.Counter(v[0] for v in out.values()).items()))
print(sorted(collections.Counter((v[3].split(':')[0], v[0]) for v in out.values()).items()))
