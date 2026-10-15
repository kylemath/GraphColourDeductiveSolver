"""LP-guided receiver-centred configurations (README §6, exploratory).
Reads the dual certificate of an out/wlp2_<tag>.txt run.  For every receiver arrangement in it (link word w_0..,
s word s_i between w_i and w_i+1), every sender set S (|S| >= 2) of its degree-5 link vertices gives a configuration of
the pairs2.py type: u (exact degree d) + S + the links of S, with letters 7/8/9 left free (B, ring vertices).  Ring size
by the Euler formula (checked against every pairs/pairs2 build), then built with pairs.py's builder and written in
dfast format if ring <= RMAX and not already tested (registry = every *_dfast.out / *.out listed in TESTED).
Greedy mode (default): an arrangement is killed when one of its sender sets is tested D; for every arrangement not
killed, only its cheapest (smallest ring) untested sender set is written.  Arrangements whose sender sets with ring
<= RMAX are all tested and none is D are listed as HARD (they survive every ring <= RMAX configuration of this type).
Usage: python3 gen.py OUTFILE RMAX wlp2_out [wlp2_out ...] [all]  (OUTFILE gets the dfast input lines)"""
import sys, os, glob, itertools, re
HERE = os.path.dirname(os.path.abspath(__file__)); DIS = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(DIS, 'b8b')); sys.path.insert(0, DIS)
from rings import Layered
ALL = 'all' in sys.argv; OUT, RMAX, FILES = sys.argv[1], int(sys.argv[2]), [a for a in sys.argv[3:] if a != 'all']

def canon_key(d, lk, sv):
    """lk, sv: strings over 5,6,B,'.'; min over the dihedral group (s_i sits between w_i and w_i+1)."""
    best = None
    for refl in (0, 1):
        if refl: l2 = lk[::-1]; s2 = ''.join(sv[(-i - 2) % d] for i in range(d))
        else: l2, s2 = lk, sv
        for k in range(d):
            c = (l2[k:] + l2[:k], s2[k:] + s2[:k])
            if best is None or c < best: best = c
    return (d,) + best
def key_of_name(nm):
    f = nm.split('_'); d = int(f[0][1:]); lk, sv = f[1], f[2]
    if f[0][0] == 'p': lk = lk.replace('9', '.'); sv = sv.replace('0', '.')
    return canon_key(d, lk, sv)
TESTED = {}; PENDC = set()     # PENDC: the not-D equal-split overloads at a 7 (Studio Job 27 cfast, pending)
for fn in glob.glob(os.path.join(HERE, 'out', '*.out')):
    for line in open(fn):
        f = line.split()
        if not f or not re.match(r'^[ep]\d+_', f[0]): continue
        TESTED[key_of_name(f[0])] = 'D' if 'D=true' in line else 'notD'
        if os.path.basename(fn) == 'eq_D7_dfast.out' and 'D=true' not in line: PENDC.add(key_of_name(f[0]))

def ringf(d, w, s):
    tot = d
    for j in range(d):
        if w[j] is not None:
            tot += w[j] - 4
            if w[(j + 1) % d] is not None: tot -= 1
            if s[j] is not None: tot -= 1
            if s[(j - 1) % d] is not None: tot -= 1
            if w[j] == 5 and s[j] is not None and s[(j - 1) % d] is not None: tot -= 1
        if s[j] is not None: tot += s[j] - 3
    return tot

def build(D, link, r2):
    L = Layered(D); L.add_ring(list(link))
    W = L.rings[1]; Z = L.ring(); adj = {}
    for a, b, c in L.tris:
        for x, y in ((a, b), (b, c), (c, a)): adj.setdefault(x, set()).add(y); adj.setdefault(y, set()).add(x)
    name = {0: ('u',)}
    for i, w in enumerate(W): name[w] = ('w', i)
    Wi = {w: i for i, w in enumerate(W)}; cnt = {}
    for z in Z:
        ws = sorted(Wi[x] for x in adj[z] if x in Wi)
        if len(ws) == 2:
            i, j = ws; name[z] = ('s', j if (i, j) == (0, D - 1) else i)
        else:
            i = ws[0]; cnt[i] = cnt.get(i, 0) + 1; name[z] = ('p', i, cnt[i])
    L.add_ring([r2.get(name[z], 9) for z in Z])
    adj = {}
    for a, b, c in L.tris:
        for x, y in ((a, b), (b, c), (c, a)): adj.setdefault(x, set()).add(y); adj.setdefault(y, set()).add(x)
    return adj, name
def extract(adj, I, deg):
    Is = set(I); RS = set(y for x in I for y in adj[x]) - Is
    for y in RS:
        if len(adj[y] & RS) != 2: return None
    start = min(RS); order = [start]; prev = None
    while True:
        cur = order[-1]; nb = sorted(adj[cur] & RS); nxt = nb[0] if nb[0] != prev else nb[1]
        if nxt == start: break
        order.append(nxt); prev = cur
    if len(order) != len(RS): return None
    for x in I: assert len(adj[x]) == deg[x], (x, len(adj[x]), deg[x])
    ri = {y: j for j, y in enumerate(order)}; Il = sorted(I); ii = {x: j for j, x in enumerate(Il)}
    f = lambda Ls: ';'.join(','.join(map(str, v)) if v else '-' for v in Ls)
    ia = [sorted(ii[y] for y in adj[x] if y in Is) for x in Il]
    ra = [sorted(ri[y] for y in adj[x] if y in RS) for x in Il]
    return len(order), len(Il), f(ra), f(ia)

arrs = []
for fn in FILES:
    for line in open(fn):
        m = re.search(r'receiver d=(\d+) link (\d+) s (\d+)', line)
        if m: arrs.append((int(m.group(1)), m.group(2), m.group(3)))
new = {}; stats = {'subsets': 0, 'ring>R': 0, 'tested': 0, 'notext': 0, 'killed': 0, 'hard': 0, 'pending': 0}
hard = []; NOTEXT = set()
def subsets(d, lk, sv):
    snd = [i for i in range(d) if lk[i] == '5']; res_ = []
    for k in range(2, len(snd) + 1):
        for S in itertools.combinations(snd, k):
            wl = {(i + e) % d for i in S for e in (-1, 0, 1)}; sl = {(i + e) % d for i in S for e in (-1, 0)}
            w = [int(lk[j]) if j in wl and lk[j] in '56' else None for j in range(d)]
            s = [int(sv[j]) if j in sl and sv[j] in '56' else None for j in range(d)]
            r = ringf(d, w, s)
            if r > RMAX: continue
            L_ = ''.join(('B' if lk[j] in '789' else lk[j]) if j in wl else '.' for j in range(d))
            S_ = ''.join(('B' if sv[j] in '789' else sv[j]) if j in sl else '.' for j in range(d))
            res_.append((r, k, S, w, s, canon_key(d, L_, S_)))
    return sorted(res_, key=lambda x: (x[0], x[1]))
def make(d, r, S, w, s, key):
    """dfast line for the sender set, or None if its ring is not a simple induced cycle."""
    link = [w[j] if w[j] is not None else 9 for j in range(d)]       # B and unspecified -> 9, not in I
    adj, name = build(d, link, {('s', j): s[j] for j in range(d) if s[j] is not None})
    inv = {v: x for x, v in name.items()}
    I = [inv[('u',)]] + [inv[('w', j)] for j in range(d) if w[j] is not None] + [inv[('s', j)] for j in range(d) if s[j] is not None]
    deg = {inv[('u',)]: d}; deg.update({inv[('w', j)]: w[j] for j in range(d) if w[j] is not None})
    deg.update({inv[('s', j)]: s[j] for j in range(d) if s[j] is not None})
    c = extract(adj, I, deg)
    if c is None: return None
    assert c[0] == r, (d, S, c[0], r)
    nm = 'e%d_%s_%s_%s' % (d, key[1], key[2], ''.join('1' if ch != '.' else '0' for ch in key[1]))
    return '%s %d %d %s %s' % ((nm,) + c)
for d, lk, sv in arrs:
    subs = subsets(d, lk, sv)
    if any(TESTED.get(x[5]) == 'D' for x in subs): stats['killed'] += 1; continue
    un = [x for x in subs if x[5] not in TESTED and x[5] not in NOTEXT]
    if not ALL:
        if any(x[5] in new for x in un): stats['pending'] += 1; continue
    got = False
    for r, k, S, w, s, key in un:
        if key in new: continue
        line = make(d, r, S, w, s, key); stats['subsets'] += 1
        if line is None: stats['notext'] += 1; NOTEXT.add(key); continue
        new[key] = line; got = True
        if not ALL: break
    if got or any(x[5] in new for x in un): stats['pending'] += 1
    else: stats['hard'] += 1; hard.append((d, lk, sv, len(subs), sum(1 for x in subs if x[5] in PENDC)))
lines = sorted(new.values(), key=lambda x: int(x.split()[1]))
open(OUT, 'w').write('\n'.join(lines) + ('\n' if lines else ''))
for h in hard: print('HARD d=%d link %s s %s (%d sender sets with ring <= RMAX, all tested, none D; pendC=%d)' % h)
print('arrangements', len(arrs), stats, 'new configs', len(lines), 'rings', sorted(__import__('collections').Counter(int(x.split()[1]) for x in lines).items()))
