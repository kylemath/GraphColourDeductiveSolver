"""Which tested B-free receiver-centred configurations (dfast/cfast outputs) are contained in a given d=7 arrangement."""
import sys, re, glob
D = '/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis'
A = {5: 0, 6: 1, 7: 2, 8: 2, 9: 2}
def parse(name):
    f = name.split('_'); d = int(f[0][1:]); lk, sv = f[1], f[2]
    def L(ch, kind):
        if ch == '.' or (f[0][0] == 'p' and ((kind == 'w' and ch == '9') or (kind == 's' and ch == '0'))): return None
        return 'B' if ch == 'B' else int(ch)
    w = [L(c, 'w') for c in lk]; s = [L(c, 's') for c in sv]; P = []
    AB = {5: 0, 6: 1, 'B': 2}
    for i in range(d):
        if w[i] != 5: continue
        r = (w[(i + 1) % d], s[i], s[(i - 1) % d], w[(i - 1) % d])
        if None in r: continue
        P.append((i, tuple(AB[x] for x in r)))
    return d, P
def contains(lk, sv, P, d=7):
    w = [int(c) for c in lk]; s = [int(c) for c in sv]
    for refl in (0, 1):
        ww = w if not refl else [w[-k % d] for k in range(d)]
        ss = s if not refl else [s[(-k - 1) % d] for k in range(d)]
        for r in range(d):
            ok = True; S = []
            for i, c in P:
                j = (i + r) % d
                if ww[j] != 5 or (A[ww[(j + 1) % d]], A[ss[j]], A[ss[j - 1]], A[ww[j - 1]]) != c: ok = False; break
                S.append(j)
            if ok: return sorted(S), refl, r
    return None
lk, sv = sys.argv[1], sys.argv[2]
for fn in sorted(glob.glob(D + '/out/*dfast*.out')) + glob.glob(D + '/job27/*'):
    for line in open(fn):
        m = re.match(r'^([ep]7_\S+)', line)
        if not m: continue
        d, P = parse(m.group(1))
        if len(P) < 2: continue
        hit = contains(lk, sv, P)
        if hit: print(fn.split('/')[-1], m.group(1), 'D=true' in line, 'slots', hit[0], line.split()[1] if len(line.split()) > 1 else '')
