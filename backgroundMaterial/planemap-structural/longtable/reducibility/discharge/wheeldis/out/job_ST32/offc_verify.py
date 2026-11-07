"""ST-32 (Studio, 7 Nov): independent verifier of an OFFC (s86) off-centre kill file, written from OFFC_SPEC.md alone
(sections 1, 2, R, U, F). No Opus code is read or run.

usage: python3 offc_verify.py KILLFILE OUT.tsv [--mutate]
Per line: (0) source: FILE exists, md5 prefix matches, NAME is in it with D=true (D) or C-REDUCIBLE (C), r= m= read from that line;
(1) K rebuilt from NAME (section 2); (2) section R; (3) phi injective, u>u forbidden (section U), x>u only if deg_K(x)=d, other images carry
deg_K(x); (4) induced on the section 1 window, s_{i-1}s_i pairs with w_i not an image -> letter condition 5 / N on w_i; (5) every triangle of K
onto a face; (6) LINK/SWORD equal exactly the image letters plus those w_i conditions. C lines additionally: the entry's kc line (first match
in loop/k*/) has an interior graph isomorphic (degrees kept) to K, and every X edge is an interior edge of it."""
import sys, os, re, glob, hashlib, itertools, collections
WD = os.getcwd()
K3XDIR = '/tmp/swarm-W17/pat/A97/'

def parse_name(nm):
    """'<letter><d0>_LINK_SWORD[_extra]' -> d0, LINK, SWORD (the spec's window of the entry); extra blocks ignored"""
    m = re.match(r'^[a-z](\d+)_([^_]+)_([^_]+)(?:_.*)?$', nm)
    if not m: return None
    d0 = int(m[1]); L, S = m[2], m[3]
    if len(L) != d0 or len(S) != d0: return None
    return d0, L, S

def ex_slots(d0, L, S):
    ex = {}
    for i, ch in enumerate(L):
        if ch in '5678': ex[('w', i)] = int(ch)
    for i, ch in enumerate(S):
        if ch in '5678': ex[('s', i)] = int(ch)
    return ex

def window_adj(d, a, b, wlet):
    """section 1 adjacency of known vertices a, b in the degree-d window; wlet(i) -> letter of w_i or None (unknown); returns True/False/None"""
    if a == b: return False
    ka, kb = a[0], b[0]
    if ka == 'u' or kb == 'u':
        o = b if ka == 'u' else a
        return o[0] == 'w'
    if ka == 'w' and kb == 'w': return (a[1] - b[1]) % d in (1, d - 1)
    if ka == 's' and kb == 'w': a, b = b, a
    if a[0] == 'w' and b[0] == 's': return b[1] == a[1] or b[1] == (a[1] - 1) % d
    i, j = a[1], b[1]   # both s
    if (j - i) % d == 1: wi = j
    elif (i - j) % d == 1: wi = i
    else: return False
    if d == 2: return None
    let = wlet(wi)
    return None if let is None else (let == 5)

def build_K(nm, r, m):
    """section 2 -> (K vertices with degrees, edge set) or (None, reason)"""
    p = parse_name(nm)
    if p is None: return None, 'name not parsable'
    d0, L, S = p
    ex = ex_slots(d0, L, S)
    for i in range(d0):   # ambiguity
        if ('s', (i - 1) % d0) in ex and ('s', i) in ex and ('w', i) not in ex: return None, 'ambiguous s-s pair at w%d' % i
    V = dict(ex); V[('u',)] = d0
    wl = lambda i: ex.get(('w', i))
    E = set()
    for a, b in itertools.combinations(sorted(V), 2):
        ad = window_adj(d0, a, b, wl)
        if ad is None: return None, 'undetermined adjacency %s %s' % (a, b)
        if ad: E.add(frozenset((a, b)))
    def conn(Vs, Es):
        Vs = list(Vs)
        if not Vs: return False
        seen = {Vs[0]}; st = [Vs[0]]
        while st:
            x = st.pop()
            for e in Es:
                if x in e:
                    y = next(iter(e - {x}))
                    if y not in seen: seen.add(y); st.append(y)
        return len(seen) == len(Vs)
    rr = lambda Vs, Es: sum(V[x] for x in Vs) - len(Es) - 3 * len(Vs) + 3
    if m == len(ex) + 1 and conn(V, E) and rr(V, E) == r: return (V, E, d0, 'Ku'), None
    V0 = {x: g for x, g in V.items() if x != ('u',)}; E0 = {e for e in E if ('u',) not in e}
    if m == len(ex) and conn(V0, E0) and rr(V0, E0) == r: return (V0, E0, d0, 'K0'), None
    return None, '(r, m) not reproduced (|EX|=%d, r(Ku)=%d, r(K0)=%d)' % (len(ex), rr(V, E), rr(V0, E0))

def triangles(V, E):
    return [frozenset(t) for t in itertools.combinations(sorted(V), 3) if all(frozenset(p) in E for p in itertools.combinations(t, 2))]

def section_R(V, E):
    T = triangles(V, E)
    for e in E:
        k = sum(1 for t in T if e <= t)
        if k == 0: return 'R1: edge %s in no triangle' % sorted(e)
        if k >= 3: return 'R2: edge %s in %d triangles' % (sorted(e), k)
    if T:
        seen = {T[0]}; st = [T[0]]
        while st:
            t = st.pop()
            for t2 in T:
                if t2 not in seen and len(t & t2) == 2: seen.add(t2); st.append(t2)
        if len(seen) != len(T): return 'R3: triangles not edge-connected'
    for v in V:
        Tv = [t for t in T if v in t]
        if Tv:
            seen = {Tv[0]}; st = [Tv[0]]
            while st:
                t = st.pop()
                for t2 in Tv:
                    if t2 not in seen and len(t & t2) == 2: seen.add(t2); st.append(t2)
            if len(seen) != len(Tv): return 'R4: two fans at %s' % (v,)
    if len(V) - len(E) + len(T) != 1: return 'R5: V-E+T = %d' % (len(V) - len(E) + len(T))
    return None

def slot(s):
    if s == 'u': return ('u',)
    return (s[0], int(s[1:]))

def check_line(line, srcs):
    f = line.split('#', 1); pat, meta = f[0].split(), f[1].split()
    d, LINK, SWORD = int(pat[0]), pat[1], pat[2]
    src, nm = meta[0], meta[1]; kv = dict(x.split('=', 1) for x in meta[2:])
    d0, fn, md5, phis = int(kv['d0']), kv['file'], kv['md5'], kv['phi']
    if len(LINK) != d or len(SWORD) != d: return 'bad LINK/SWORD length'
    # (0) source
    ent, why = srcs.lookup(fn, md5, nm, src)
    if ent is None: return 'source: ' + why
    r, m, X = ent
    # (1) K
    K, why = build_K(nm, r, m)
    if K is None: return 'K: ' + why
    V, E, kd0, kind = K
    if kd0 != d0: return 'd0 mismatch'
    # (2) R
    why = section_R(V, E)
    if why: return 'section R: ' + why
    # (3) phi
    phi = {}
    for t in phis.split(','):
        a, b = t.split('>'); phi[slot(a)] = slot(b)
    if set(phi) != set(V): return 'phi domain %s != V(K) %s' % (sorted(phi), sorted(V))
    if len(set(phi.values())) != len(phi): return 'phi not injective'
    for x, y in phi.items():
        if y[0] != 'u' and not (0 <= y[1] < d): return 'phi image out of range %s' % (y,)
        if x == ('u',) and y == ('u',): return 'section U: u>u'
        if y == ('u',) and V[x] != d: return 'x>u with deg %d != d' % V[x]
    # expected letters
    exp_L = ['.'] * d; exp_S = ['.'] * d
    for x, y in phi.items():
        if y == ('u',): continue
        if V[x] not in (5, 6, 7, 8): return 'image degree %d not exact' % V[x]
        (exp_L if y[0] == 'w' else exp_S)[y[1]] = str(V[x])
    inv = {y: x for x, y in phi.items()}
    for i in range(d):   # w_i conditions
        a, b = ('s', (i - 1) % d), ('s', i)
        if ('w', i) not in inv and a in inv and b in inv:
            exp_L[i] = '5' if frozenset((inv[a], inv[b])) in E else 'N'
    wlet = lambda i: (V[inv[('w', i)]] if ('w', i) in inv else (5 if exp_L[i] == '5' else (6 if exp_L[i] == 'N' else None)))
    # (4) induced
    for x1, x2 in itertools.combinations(sorted(phi), 2):
        ad = window_adj(d, phi[x1], phi[x2], wlet)
        if ad is None: return 'undetermined window adjacency %s %s' % (phi[x1], phi[x2])
        if ad != (frozenset((x1, x2)) in E): return 'not induced: %s %s (K %s, window %s)' % (x1, x2, frozenset((x1, x2)) in E, ad)
    # (5) faces
    for t in triangles(V, E):
        im = sorted(phi[x] for x in t); ws = [y for y in im if y[0] == 'w']; ss = [y for y in im if y[0] == 's']; uu = [y for y in im if y[0] == 'u']
        ok = False
        if len(uu) == 1 and len(ws) == 2: ok = (ws[0][1] - ws[1][1]) % d in (1, d - 1)
        elif len(ws) == 2 and len(ss) == 1: i = ss[0][1]; ok = {ws[0][1], ws[1][1]} == {i, (i + 1) % d}
        elif len(ws) == 1 and len(ss) == 2: i = ws[0][1]; ok = {ss[0][1], ss[1][1]} == {(i - 1) % d, i} and wlet(i) == 5
        if not ok: return 'triangle %s not onto a face' % [phi[x] for x in t]
    # (6) exact letters
    if ''.join(exp_L) != LINK or ''.join(exp_S) != SWORD: return 'LINK/SWORD %s %s != expected %s %s' % (LINK, SWORD, ''.join(exp_L), ''.join(exp_S))
    # C: X edges in K via the entry's kc line
    if src == 'C':
        why = srcs.check_C(nm, V, E, X)
        if why: return 'C: ' + why
        if srcs.rim: return 'NOTE-RIM ' + ','.join(srcs.rim)
    return None

class Sources:
    def __init__(self):
        self.cache = {}; self.kc = None
    def path(self, fn):
        if fn.startswith('/home/claude/'):
            return K3XDIR + 'loop__opus__P_own_lp__s33z__reg_A97__' + os.path.basename(fn)
        return fn
    def lookup(self, fn, md5, nm, src):
        p = self.path(fn)
        if not os.path.exists(p): return None, 'file missing %s' % p
        if p not in self.cache:
            self.cache[p] = (hashlib.md5(open(p, 'rb').read()).hexdigest(), open(p, errors='ignore').read().splitlines())
        h, lines = self.cache[p]
        if not h.startswith(md5): return None, 'md5 %s != %s' % (h[:8], md5)
        for k, l in enumerate(lines):
            if l.startswith(nm + ' '):
                mm = re.search(r' r=(\d+) m=(\d+)', l)
                if not mm: continue
                r, m = int(mm[1]), int(mm[2])
                if src == 'D':
                    if 'D=true' in l: return (r, m, None), None
                    continue
                for l2 in lines[k + 1:]:
                    if not l2.startswith(' '): break
                    mx = re.search(r'X=\{([^}]*)\}.*C-REDUCIBLE', l2) or re.search(r'C-REDUCIBLE.*X=\{([^}]*)\}', l2)
                    if mx and ('leftover bad classes extending after contraction = 0' in l2 or 'C-REDUCIBLE X=' in l2): return (r, m, mx[1]), None
        return None, '%s not found with %s evidence in %s' % (nm, 'D=true' if src == 'D' else 'C-REDUCIBLE', fn)
    def kcline(self, nm):
        if self.kc is None:
            self.kc = {}
            for f in sorted(glob.glob('loop/k[0-9]*/*')):
                if not os.path.isfile(f): continue
                try: ls = open(f).read().splitlines()
                except UnicodeDecodeError: continue
                for l in ls:
                    g = l.split()
                    if len(g) == 5 and g[1].isdigit() and g[2].isdigit() and ';' in g[3] + g[4]: self.kc.setdefault(g[0], l)
        return self.kc.get(nm)
    def check_C(self, nm, V, E, X):
        l = self.kcline(nm)
        if l is None: return 'no kc line for %s in loop/k*/' % nm
        g = l.split(); m = int(g[2]); rp = g[3].split(';'); ip = g[4].split(';')
        IE = {u: (set() if ip[u] == '-' else {int(x) for x in ip[u].split(',')}) for u in range(m)}
        deg = {u: len(IE[u]) + (0 if rp[u] == '-' else len(rp[u].split(','))) for u in range(m)}
        RN = {u: (set() if rp[u] == '-' else {int(x) for x in rp[u].split(',')}) for u in range(m)}
        self.rim = []
        for e in X.split(','):
            a, b = e.split('-')
            if a[0] == 'I' and b[0] == 'I':
                if int(b[1:]) not in IE[int(a[1:])]: return 'X edge %s not an interior edge of the kc configuration' % e
            else:   # rim-pinned edge R-I: the I end is a K vertex and R one of its ring neighbours (the ring vertex is not in K)
                rr_, ii = (a, b) if a[0] == 'R' else (b, a)
                if rr_[0] != 'R' or ii[0] != 'I' or int(rr_[1:]) not in RN[int(ii[1:])]: return 'X edge %s is neither interior nor a ring edge of its I end' % e
                self.rim.append(e)
        if len(V) != m: return 'kc m=%d != |K|=%d' % (m, len(V))
        Kv = sorted(V); Kadj = {x: {y for y in Kv if frozenset((x, y)) in E} for x in Kv}
        order = sorted(range(m), key=lambda u: -len(IE[u]))
        def rec(i, mp):
            if i == m: return True
            u = order[i]
            for x in Kv:
                if x in mp.values() or V[x] != deg[u] or len(Kadj[x]) != len(IE[u]): continue
                if any((w in IE[u]) != (mp[w] in Kadj[x]) for w in mp): continue
                mp[u] = x
                if rec(i + 1, mp): return True
                del mp[u]
            return False
        return None if rec(0, {}) else 'kc interior graph not isomorphic to K'

if __name__ == '__main__':
    KF, OUT = sys.argv[1], sys.argv[2]
    srcs = Sources(); res = []; byd = collections.Counter(); bad = collections.Counter()
    for l in open(KF):
        if l.startswith('#') or not l.strip(): continue
        why = check_line(l.rstrip('\n'), srcs); d = int(l.split()[0]); note = None
        if why and why.startswith('NOTE-RIM'): note, why = why, None
        res.append((l.rstrip('\n'), why or note)); byd[(d, 'PASS' if why is None else 'FAIL')] += 1
        if why: bad[why.split(':')[0]] += 1
    ok = lambda w: w is None or w.startswith('NOTE-RIM')
    with open(OUT, 'w') as f:
        f.write('# verdict\treason\tline\n')
        for l, why in res: f.write('%s\t%s\t%s\n' % ('PASS' if ok(why) else 'FAIL', why or '-', l))
    print('lines', len(res), 'PASS', sum(1 for _, w in res if ok(w)), 'FAIL', sum(1 for _, w in res if not ok(w)), '| rim-pinned C notes', sum(1 for _, w in res if w and w.startswith('NOTE-RIM')))
    print('by d:', dict(sorted(byd.items())))
    if bad: print('fail reasons:', dict(bad))
