"""For VROW lines in an upper log: which C patterns (cpat files of an args file) match the arrangement.
usage: python3 cmatch.py LOG ARGS ROOT [nsample]"""
import sys, os, re, collections, random
LOG, ARGS, ROOT = sys.argv[1:4]; NS = int(sys.argv[4]) if len(sys.argv) > 4 else 40
LET = (5, 6, 7, 8, 9); LI = {l: i for i, l in enumerate(LET)}
SETS = {'5': (5,), '6': (6,), '7': (7,), '8': (8,), 'B': (7, 8, 9)}
def pname(name):
    f = name.split('_'); kind = f[0][0]; d = int(f[0][1:]); lk, sv = f[1], f[2]; out = []
    for typ, word in (('w', lk), ('s', sv)):
        for i, ch in enumerate(word):
            if ch == '.': continue
            if kind == 'p' and ((typ == 'w' and ch == '9') or (typ == 's' and ch == '0')): continue
            out.append(((typ, i), frozenset(SETS[ch])))
    return d, tuple(sorted(out))
def insts(d, P):
    out = set()
    for r in range(d):
        for refl in (False, True):
            m = {}
            for (typ, i), S in P:
                j = (i + r) % d if not refl else ((r - i) % d if typ == 'w' else (r - i - 1) % d)
                sl = 2 * j + (0 if typ == 'w' else 1); m[sl] = m.get(sl, 31) & sum(1 << LI[x] for x in S)
            out.add(tuple(sorted(m.items())))
    return out
C = collections.defaultdict(list)   # d -> [(name, file, insts)]
for a in open(ARGS).read().split():
    if not a.startswith('cpat='): continue
    fn = a.split('=', 1)[1]; fn = fn[:-4] if fn.endswith(':all') else fn; p = fn if os.path.isabs(fn) else os.path.join(ROOT, fn)
    if not os.path.exists(p): continue
    cur = None
    for line in open(p):
        if ' r=' in line and not line.startswith(' '): cur = line.split()[0]
        elif 'C-REDUCIBLE' in line and cur and re.match(r'^[epf]\d+_', cur):
            d, P = pname(cur); C[d].append((cur, os.path.basename(p), insts(d, P)))
rows = []
for l in open(LOG):
    m = re.match(r'\s*VROW d=(\d+) load (\S+) excess (\S+) link (\S+) sv (\S+)', l)
    if m: rows.append((int(m.group(1)), float(m.group(3)), m.group(4), m.group(5)))
print('VROW rows: %d; by d %s' % (len(rows), dict(collections.Counter(r[0] for r in rows))))
if rows: print('worst excess %.9f' % max(r[1] for r in rows))
def letters(lk, sv):
    a = {}
    for i, c in enumerate(lk): a[2 * i] = int(c)
    for i, c in enumerate(sv): a[2 * i + 1] = int(c)
    return a
tot = collections.Counter(); nonec = 0
for d, ex, lk, sv in rows:
    a = letters(lk, sv); hit = set()
    for nm, fb, I in C.get(d, ()):
        if any(all((m >> LI[a[s]]) & 1 for s, m in inst) for inst in I): hit.add((nm, fb))
    for h in hit: tot[h] += 1
    if not hit: nonec += 1
rs = sorted(rows, key=lambda r: -r[1])
print('rows matched by no cpat C pattern (repaired elsewhere: kill tables / wheels): %d' % nonec)
print('C patterns by #rows repaired (top 40):')
for (nm, fb), c in tot.most_common(40): print('  %6d  %s  [%s]' % (c, nm, fb))
print('sample (worst first):')
for d, ex, lk, sv in rs[:NS]:
    a = letters(lk, sv); hit = sorted(nm + '[' + fb + ']' for nm, fb, I in C.get(d, ()) if any(all((m >> LI[a[s]]) & 1 for s, m in inst) for inst in I))
    print('  d=%d %s/%s excess %.6f : %s' % (d, lk, sv, ex, ' '.join(hit[:6]) + (' ...+%d' % (len(hit) - 6) if len(hit) > 6 else '') if hit else '(no cpat C)'))
