# s43 control (b): physical test of the fy2 (level-2) z keys, RELAY_SPEC_s43 43.2-43.3.
# An explicit rotation system is built around a receiver u of degree d (link w_i, apexes s_i, privates of the w's, the
# apex s_i's own rotation with fresh vertices, and so the face apex private t_i).  Every hat is read by ONE generic rule
# from a rotation list.  Three things are compared for every link five v of u:
#   (I)  an INDEPENDENT key computed here from the graph (own vis / mask / canonical code, no engine key function);
#   (S)  the engine's sender key: v's word and hat classes canonicalised as SENDERS / R2_sender_rows, fy_sender_key;
#   (R)  the engine's receiver z keys: recv_coef_R2(d, link, sv, xon, tau) of the row read in a random rotation and
#        orientation of u, with tau = the cell of the actual t's (the cell must be one of fy2_cells).
# (R) is compared as a multiset over u's link fives.  Broken controls: (a) the big reads the OTHER apex's neighbour for
# t (s_{i+1}'s letter instead of t_i); (b) independent key with level-1 mask (h2 never read).
#   python3 phys43.py [N]
import sys, random, collections, itertools
NARG = int(sys.argv[1]) if len(sys.argv) > 1 else 100000
sys.path.insert(0, '/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/s43')
B = '/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp'
M = '/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/P/m/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis'
E = B + '/s43/eng'
sys.argv = [E + '/pcheck.py', 'none', 'apexcls', 'hat5', 'fy', 'fy2', 'root=' + M]
src = open(E + '/pcheck.py').read(); last = src.rstrip().rsplit('\n', 1)
G = {'__file__': E + '/pcheck.py', '__name__': 'pcheck_exec'}; exec(compile(last[0], E + '/pcheck.py', 'exec'), G)
assert G['FY2'] and G['FY']
isR5 = G['isR5']

def ind_key(n, hats, level2=True):
    """independent: n = degree letters (u, n1..n4) in v's rotation from u; hats = degree letters of v's 5 hats"""
    cl = [1 if x >= 7 else 0 for x in hats]
    show = [True, n[1] == 5, level2 and ((n[1] == 5 and n[2] == 5) or (n[4] == 5 and n[3] == 5)), n[4] == 5, True]
    m = [cl[k] if show[k] else 2 for k in range(5)]
    fwd = list(n) + m
    bwd = [n[0], n[4], n[3], n[2], n[1]] + m[::-1]
    return tuple(min(fwd, bwd))

def build(rng, d):
    L = lambda: rng.choice((5, 6, 7, 8, 9))
    deg = {}; rot = {}
    U = min(d, 9); deg['u'] = U
    w = [rng.choice((5, 5, 5, 6, 6, 7, 8)) for _ in range(d)]
    s = [rng.choice((5, 5, 6, 7, 8, 9)) for _ in range(d)]
    for _ in range(rng.choice((0, 1, 1, 2))):   # plant faces
        i = rng.randrange(d); w[i] = w[(i + 1) % d] = 5; s[i] = 5
    W_ = ['w%d' % i for i in range(d)]; S_ = ['s%d' % i for i in range(d)]
    for i in range(d): deg[W_[i]] = w[i]; deg[S_[i]] = s[i]
    rot['u'] = list(W_)
    # w_i: u, w_{i+1}, s_i, [privates], s_{i-1}, w_{i-1}
    for i in range(d):
        pv = ['p%d_%d' % (i, k) for k in range(w[i] - 5)]
        for z in pv: deg[z] = L()
        rot[W_[i]] = ['u', W_[(i + 1) % d], S_[i]] + pv + [S_[(i - 1) % d], W_[(i - 1) % d]]
    # s_i: w_i, w_{i+1}, a, fresh..., b ; a = the nbr of w_{i+1} before s_i (s_{i+1} or w_{i+1}'s last private),
    # b = the nbr of w_i after s_i (s_{i-1} or w_i's first private)
    for i in range(d):
        a = rot[W_[(i + 1) % d]][-3]; b = rot[W_[i]][3]
        fr = ['f%d_%d' % (i, k) for k in range(s[i] - 4)]
        for z in fr: deg[z] = L()
        rot[S_[i]] = [W_[i], W_[(i + 1) % d], a] + fr + [b]
    # faces of the edges s_i s_{i+1} (present iff w_{i+1} = 5): the vertex after s_{i+1} in s_i's rotation is the vertex
    # before s_i in s_{i+1}'s rotation -> identify (union-find over fresh names)
    par = {}
    def fd(x):
        while par.get(x, x) != x: x = par[x]
        return x
    for i in range(d):
        if w[(i + 1) % d] == 5:
            x, y = fd(rot[S_[i]][3]), fd(rot[S_[(i + 1) % d]][-2])
            if x != y: par[y] = x
    for k in list(rot): rot[k] = [fd(z) for z in rot[k]]
    return d, w, s, deg, rot

def nb_after(rot, x, y):   # in x's rotation, the neighbour after y
    r = rot[x]; return r[(r.index(y) + 1) % len(r)]
def nb_before(rot, x, y):
    r = rot[x]; return r[(r.index(y) - 1) % len(r)]

def five_view(st, i):
    """v = w_i: its rotation from u, hats by the generic rule (common nbr of consecutive spokes other than v)"""
    d, w, s, deg, rot = st; v = 'w%d' % i
    sp = rot[v]                          # u, w_{i+1}, s_i, s_{i-1}, w_{i-1}
    assert len(sp) == 5
    hats = []
    for k in range(5):
        x, y = sp[k], sp[(k + 1) % 5]
        # common neighbour of x and y other than v: read from a rotation that contains both
        hs = set()
        for a, b in ((x, y), (y, x)):
            if a in rot and b in rot[a]:
                r = rot[a]; j = r.index(b); c1, c2_ = r[(j - 1) % len(r)], r[(j + 1) % len(r)]
                assert v in (c1, c2_); hs.add(c2_ if c1 == v else c1)
        assert len(hs) == 1, ('inconsistent rotations', hs)
        h = hs.pop()
        hats.append(h)
    return sp, hats

def run(N, seed=43):
    rng = random.Random(seed); stats = collections.Counter()
    for _ in range(N):
        d = rng.choice((7, 7, 8, 9, 10)); st = build(rng, d)
        d, w, s, deg, rot = st; U = min(d, 9)
        faces = [i for i in range(d) if w[i] == 5 and w[(i + 1) % d] == 5 and s[i] == 5]
        if any((i + 1) % d in faces for i in faces): stats['skip two faces'] += 1; continue
        if any(w[i] == 5 and isR5((U, w[(i + 1) % d], s[i], s[(i - 1) % d], w[(i - 1) % d])) for i in range(d)): stats['skip R5 five'] += 1; continue
        if any(isR5([deg[z] for z in rot['s%d' % i]]) for i in faces): stats['skip R5 apex'] += 1; continue
        ind = collections.Counter(); ind1 = collections.Counter()
        for i in range(d):
            if w[i] != 5: continue
            sp, hats = five_view(st, i)
            n = [deg[z] for z in sp]; hl = [deg[z] for z in hats]
            # the t of a face five must be the apex's own 4th neighbour (Lemma 2)
            for f in faces:
                if i == f: assert hats[2] == rot['s%d' % f][3], 'lemma 2 (w_i)'; stats['lemma2'] += 1
                if i == (f + 1) % d: assert hats[2] == rot['s%d' % f][3], 'lemma 2 (w_i+1)'; stats['lemma2'] += 1
            K = ind_key(n, hl); ind[K] += 1; ind1[ind_key(n, hl, False)] += 1
            # (S) engine sender key from the canonical five word
            x = n; H = [1 if z >= 7 else 0 for z in hl]
            if isR5(x) or max(x) < 7: continue
            wc = min(min(tuple(x[(r + m) % 5] for m in range(5)), tuple(x[(r - m) % 5] for m in range(5))) for r in range(5))
            ks = set()
            for refl in (False, True):
                for r in range(5):
                    idx = [(r + m) % 5 for m in range(5)] if not refl else [(r - m) % 5 for m in range(5)]
                    if tuple(x[j] for j in idx) != wc: continue
                    HH = [H[idx[m]] for m in range(5)] if not refl else [H[(idx[m] - 1) % 5] for m in range(5)]
                    ks.add(G['fy_sender_key'](list(wc), HH, idx.index(0)))
            stats['sender pairs'] += 1
            if ks != {K}: stats['SENDER MISMATCH'] += 1
        # (R) engine receiver row in a random rotation / orientation, cell from the actual t's
        rr = rng.randrange(d); refl = rng.random() < 0.5
        wl = [None] * d; sl = [None] * d; sid = [None] * d
        for i in range(d):
            j = (i + rr) % d if not refl else (rr - i) % d; wl[j] = w[i]
            j2 = (i + rr) % d if not refl else (rr - i - 1) % d; sl[j2] = s[i]; sid[j2] = i
        lk = ''.join(map(str, wl)); sv = ''.join(map(str, sl))
        cells = dict(G['fy2_cells'](d, wl, sl))
        for broken in (False, True):
            tau = {}
            for j in range(d):
                if wl[j] == 5 and wl[(j + 1) % d] == 5 and sl[j] == 5:
                    t_ = rot['s%d' % sid[j]][3]; tl = deg[t_]
                    if broken: tl = deg[rot['s%d' % sid[j]][2]]   # control: s_{i+1}'s letter read as t
                    tau[j] = 1 if tl >= 7 else 0
            lab = ','.join('%d:%d' % (j, tau[j]) for j in sorted(tau))
            if lab not in cells:
                stats['broken cell not allowed' if broken else 'CELL NOT ALLOWED'] += 1; continue
            cf = G['recv_coef_R2'](d, lk, sv, False, cells[lab])
            rz = collections.Counter({k[1]: v for k, v in cf.items() if k[0] == 'z' and v})
            if broken: stats['broken rows'] += 1; stats['broken mismatches'] += rz != ind
            else:
                stats['rows'] += 1; stats['face rows'] += bool(faces); stats['five keys'] += sum(ind.values())
                if rz != ind: stats['RECEIVER MISMATCH'] += 1
                if ind1 != ind: stats['level-1 control differs'] += 1
    return stats
N = NARG
st = run(N)
for k in sorted(st): print('%-28s %d' % (k, st[k]))
ok = st['SENDER MISMATCH'] == 0 and st['RECEIVER MISMATCH'] == 0 and st['CELL NOT ALLOWED'] == 0
print('PHYS43:', 'PASS' if ok else 'FAIL', '(broken t control: %d of %d rows mismatch; level-1 mask differs on %d rows)' % (st['broken mismatches'], st['broken rows'], st['level-1 control differs']))
