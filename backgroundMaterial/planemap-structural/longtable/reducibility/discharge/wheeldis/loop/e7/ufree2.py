"""EXPLORE round 13 (exploratory): ufree.py with S allowed to hold fives whose non-u neighbours include link bigs
(letters 7/8 at exact degree; 9 = free big is excluded since the window must be exact).  Everything else as ufree:
EXPLORE round 7 (exploratory): receiver-FREE configurations of lone fives.
For an arrangement (d, link, s) and a set S of its lone fives (a five whose neighbours other than u all have degree
<= 6) lying in one short arc of the link, the configuration is S + every neighbour of S except u, all at exact degree;
u stays on the ring with its degree free.  It does not depend on d, so if it is reducible it forbids the same window
at every receiver degree at once.  Built with gen.py's builder (u is built at degree d and then left out of I).
Writes OUT.txt (dfast lines, ring <= RMAX, new names only) and OUT.pat (the window as an f<d>_ pattern for every
d = 7..DMAX, one line per (name, d), read by wlp3/lone.py as 'pat=' once its verdict is known: see mkpat below).
Names: z_<link window>_<s window>, dihedral minimum; '.' = position not in the configuration.
Usage: python3 loop/e7/ufree2.py OUT RMAX MAXARC ARRFILE [ARRFILE ...]
       python3 loop/e7/ufree2.py mkpat DFAST_OUT PATOUT [DMAX=17]   (patterns for every D=true z_ name)"""
import sys, os, itertools, re
HERE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if sys.argv[1] == 'mkpat':
    src_, dst = sys.argv[2], sys.argv[3]; DMAX = int(sys.argv[4]) if len(sys.argv) > 4 else 17; out = []
    for line in open(src_):
        f = line.split()
        if not f or not f[0].startswith('z_') or 'D=true' not in line: continue
        _, lw, sw = f[0].split('_'); k = len(lw)
        for d in range(max(7, k + 2), DMAX + 1):
            out.append('f%d_%s_%s D=true via %s' % (d, lw + '.' * (d - k), sw + '.' * (d - k + 1), f[0]))
    open(dst, 'w').write('\n'.join(out) + '\n'); print(len(out), 'pattern lines'); sys.exit()
UOUT, URMAX, MAXARC, UFILES = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4:]   # U*: gen28's header sets OUT/RMAX/FILES
src = open(os.path.join(HERE, 'gen28.py')).read(); src = src[:src.rindex('arrs = []')]
sys.argv = ['gen28.py', '/dev/null', str(URMAX)]; __file__ = os.path.join(HERE, 'gen28.py'); exec(src)
def lone(d, lk, sv, i):   # here: any five whose non-u neighbours have exact letters 5..8
    return lk[i] == '5' and lk[(i - 1) % d] in '5678' and lk[(i + 1) % d] in '5678' and sv[i] in '5678' and sv[(i - 1) % d] in '5678'
def zname(d, lk, sv, wl, sl):
    """window name: the arc from the first to the last link position used, as link letters and s letters (s_j between
    w_j and w_j+1, so the s window is one shorter); dihedral minimum (reflection reverses both and shifts s by one)."""
    best = None
    for st in range(d):
        arc = [(st + t) % d for t in range(d)]
        used = [t for t, j in enumerate(arc) if j in wl]
        if not used or used[0] != 0: continue
        k = used[-1] + 1
        lw = ''.join(lk[arc[t]] if arc[t] in wl else '.' for t in range(k))
        sw = ''.join(sv[arc[t]] if arc[t] in sl else '.' for t in range(k - 1))
        for cand in ((lw, sw), (lw[::-1], sw[::-1])):
            if best is None or (len(cand[0]), cand) < (len(best[0]), best): best = cand
    return 'z_%s_%s' % best
lines = {}; seen = 0
for fn in UFILES:
    for line in open(fn):
        m = re.search(r'receiver d=(\d+) link (\d+) s (\d+)', line)
        if not m: continue
        d, lk, sv = int(m.group(1)), m.group(2), m.group(3); seen += 1
        Lp = [i for i in range(d) if lone(d, lk, sv, i)]
        for k in range(2, 5):
            for S in itertools.combinations(Lp, k):
                # S must fit in an arc of MAXARC consecutive link positions
                if not any(all((i - st) % d < MAXARC for i in S) for st in range(d)): continue
                wl = {(i + e) % d for i in S for e in (-1, 0, 1)}; sl = {(i + e) % d for i in S for e in (-1, 0)}
                nm = zname(d, lk, sv, wl, sl)
                if nm in lines: continue
                link = [int(lk[j]) if j in wl else 9 for j in range(d)]
                adj, name = build(d, link, {('s', j): int(sv[j]) for j in sl})
                inv = {v: x for x, v in name.items()}
                I = [inv[('w', j)] for j in wl] + [inv[('s', j)] for j in sl]
                deg = {inv[('w', j)]: int(lk[j]) for j in wl}; deg.update({inv[('s', j)]: int(sv[j]) for j in sl})
                c = extract(adj, I, deg)
                if c is None: lines[nm] = None; continue
                if c[0] > URMAX: lines[nm] = None; continue
                lines[nm] = '%s %d %d %s %s' % ((nm,) + c)
good = sorted((l for l in lines.values() if l), key=lambda x: (int(x.split()[1]), x))
open(UOUT, 'w').write(''.join(l + '\n' for l in good))
print('arrangements', seen, 'windows', len(lines), 'written (ring <= %d)' % URMAX, len(good))
