"""Job 29 (exploratory): pattern dependencies of a wlp3x solution.

The LP solution (y, x, z9, t) is feasible because every arrangement that would violate it is forbidden by some
pattern. This script lists those arrangements and the patterns that cover them:
- It takes the solution JSON dumped by wlp3x.py and that run's pattern arguments.
- Pattern-free separation (bin/sep3x_new, SEP_NODELIMIT=0, exhaustive) finds every violating arrangement at
  d = 7..DMAXP. Rows for d > DMAXP use no patterns.
- Each arrangement is matched against every loaded pattern, using all dihedral images (as sep3x does).
- A greedy set cover picks the windows the solution needs. Windows are reported per source file, with names
  listed for the files whose second engine is only dfast18 or dfast16.
- Any violating arrangement that no pattern covers is printed loudly: that would mean the solution is infeasible.

Usage: python3 certdeps.py SOLUTION.json [many=1000000]"""
import sys, os, re, json, subprocess, collections
HERE = os.path.dirname(os.path.abspath(__file__))
SOLF = sys.argv[1]; SOL = json.load(open(SOLF))
MANY = int(next((a[5:] for a in sys.argv[2:] if a.startswith('many=')), '1000000'))
ARGS = SOL['args']; PATARGS = [a for a in ARGS if a.startswith(('pat=', 'cpat='))]
# pattern-free static input: wlp3 prologue with only w7plus (RBIG kept)
src = open(os.path.join(HERE, 'wlp3.py')).read().replace('os.path.abspath(__file__)', repr(os.path.join(HERE, 'wlp3.py')), 1)
sys.argv = ['wlp3', 'tag=deps_nopat'] + (['w7plus'] if 'w7plus' in ARGS else [])
exec(src[:src.index('A_ub, b_ub = [], []')])
SEP.stdin.close(); SEP.wait()
env = dict(os.environ, SEP_NODELIMIT='0')
SX = subprocess.Popen([os.path.join(HERE, 'bin', 'sep3x_new'), SF], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True, env=env)
yv = [0.0] * len(roots)
for k, v in SOL['y'].items():
    u, rest = k.split('|'); yv[ix[(int(u),) + tuple(int(c) for c in rest)]] = v
xs = [(int(k), v) for k, v in SOL['x'].items()]
t = SOL['t']
def sepx(d, thr, many):
    SX.stdin.write('q %d %.12f %d %d\n%s\nX %d %s\n' % (d, thr, many, 0, ' '.join('%.12f' % x for x in yv),
                   len(xs), ' '.join('%d %.12f' % kv for kv in xs))); SX.stdin.flush(); out = []
    while True:
        f = SX.stdout.readline().split()
        if f[0] == 'END': return out, f
        out.append((float(f[1]), f[2], f[3]))
# --- patterns with their source and name ---
LI = {5: 0, 6: 1, 7: 2, 8: 3, 9: 4}
SETS = {5: (5,), 6: (6,), 7: (7,), 8: (8,), 'B': (7, 8, 9)}
def mask(slots): return sum(sum(1 << (5 * t_ + LI[x]) for x in SETS[v]) for t_, v in enumerate(slots))
def parsep(name):
    f = name.split('_'); d = int(f[0][1:]); lk, sv = f[1], f[2]; k0 = f[0][0]
    def L(ch, kind):
        if ch == '.' or (k0 == 'p' and ((kind == 'w' and ch == '9') or (kind == 's' and ch == '0'))): return None
        return 'B' if ch == 'B' else int(ch)
    w = [L(c, 'w') for c in lk]; s = [L(c, 's') for c in sv]; P = []
    for i in range(d):
        if w[i] != 5: continue
        r = (w[(i + 1) % d], s[i], s[(i - 1) % d], w[(i - 1) % d])
        if None in r: continue
        P.append((i, mask(r)))
    return d, P
def revmask(m): return sum(((m >> (5 * t_)) & 31) << (5 * (3 - t_)) for t_ in range(4))
def matches(m, c): return all((m >> (5 * t_ + (c // (125, 25, 5, 1)[t_] % 5))) & 1 for t_ in range(4))
PATS = []; seen = set()
for a in PATARGS:
    kind, fn = a.split('=', 1); allf = fn.endswith(':all'); fn = fn[:-4] if allf else fn
    path = fn if os.path.isabs(fn) else os.path.join(HERE, fn)
    if not os.path.exists(path): continue
    if kind == 'pat':
        for line in open(path):
            if line.strip() and (allf or 'D=true' in line) and re.match(r'^[epf]\d+_', line):
                nm = line.split()[0]
                if nm not in seen: seen.add(nm); PATS.append((nm, fn, 'D'))
    else:
        cur = None
        for line in open(path):
            if ' r=' in line and not line.startswith(' '): cur = line.split()[0]
            elif 'C-REDUCIBLE' in line and cur and re.match(r'^[epf]\d+_', cur) and cur not in seen:
                seen.add(cur); PATS.append((cur, fn, 'C'))
IDX = collections.defaultdict(list)   # (d, pos, code) -> list of (pattern index, rest images)
for pi, (nm, fn, kd) in enumerate(PATS):
    d, P = parsep(nm)
    imgs = set()
    for refl in (0, 1):
        for r in range(d):
            Q = tuple(sorted(((((d - p) % d if refl else p) + r) % d, revmask(m) if refl else m) for p, m in P))
            imgs.add(Q)
    for Q in imgs:
        q0, m0 = Q[0]
        for c in range(625):
            if matches(m0, c): IDX[(d, q0, c)].append((pi, Q[1:]))
print('patterns loaded', len(PATS), 'index keys', len(IDX), flush=True)
def codes(d, lk, sv):
    w = [int(c) for c in lk]; s = [int(c) for c in sv]; C = {}
    for p in range(d):
        if w[p] == 5: C[p] = LI[w[(p + 1) % d]] * 125 + LI[s[p]] * 25 + LI[s[(p - 1) % d]] * 5 + LI[w[(p - 1) % d]]
    return C
cover = {}; uncovered = []; nviol = collections.Counter()
for d in range(7, DMAXP + 1):
    out, end = sepx(d, d - 6 + t + 1e-9, MANY)
    nviol[d] = len(out)
    if len(end) > 3 and int(end[3]): print('WARNING d=%d separation aborted' % d)
    for wgt, lk, sv in out:
        C = codes(d, lk, sv); hit = set()
        for p, c in C.items():
            for pi, rest in IDX.get((d, p, c), ()):
                if all(q in C and matches(m, C[q]) for q, m in rest): hit.add(pi)
        if not hit: uncovered.append((d, lk, sv, wgt))
        cover[(d, lk, sv)] = hit
    print('d=%d violating arrangements %d' % (d, len(out)), flush=True)
SX.stdin.close(); SX.wait()
# greedy set cover
need = {k for k, v in cover.items() if v}; chosen = []
inv = collections.defaultdict(set)
for k, v in cover.items():
    for pi in v: inv[pi].add(k)
while need:
    pi = max(inv, key=lambda q: len(inv[q] & need)); got = inv[pi] & need
    if not got: break
    chosen.append(pi); need -= got
byfile = collections.Counter(PATS[pi][1] for pi in chosen)
out = ['# certdeps %s: t = %.6f; violating arrangements without patterns: %s; uncovered: %d; windows in greedy cover: %d' % (
    SOLF, t, dict(nviol), len(uncovered), len(chosen))]
for u in uncovered[:20]: out.append('UNCOVERED d=%d link %s s %s weight %.6f' % u)
out.append('windows per file (greedy cover):')
for fn, k in byfile.most_common(): out.append('  %-48s %d' % (fn, k))
out.append('windows used (name, file, D/C):')
for pi in chosen: out.append('  %s %s %s' % PATS[pi])
open(SOLF.replace('_sol.json', '_deps.txt'), 'w').write('\n'.join(out) + '\n')
print('\n'.join(out[:40]))
