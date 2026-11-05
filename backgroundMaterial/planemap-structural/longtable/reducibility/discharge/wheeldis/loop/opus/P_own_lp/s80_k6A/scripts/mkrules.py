"""s80 Team E: B3 routes A' (configs_D_kill6wide.txt) and L' (configs_D_l3qrow.txt) -> extra f2b rules (same JSON format as
Studio's rules_studio_keep95p131f.json), with an independent soundness check of every rule.

Rule (f2b semantics, eng/f2b.py): (p, w_req, s_req) in group dD_w6 (spoke w_i = 6, d = D) or dD_w7[sg] (spoke w_i = 7, l3q side sg);
fires at spoke i iff w[(i+o) % d] in allowed for every (o, allowed) in w_req and s[(i+o) % d] == v for every (o, v) in s_req;
a firing rule removes letter p from the private mask of that spoke (w6: the filt16 amask of the M term; w7 side sg: the l3q mask
of the payee side, a = s_i (sg = +1) or s_{i-1} (sg = -1), c = w_{i+sg}; also the q7m payer mask of that side).

Source of each rule: the entry's q-name (PRIVCELL grammar, parsed by eng/privcell.py pc_parse): every constrained link / apex slot
other than the parent becomes a requirement at its offset from the parent; the single constrained private gives p and the side
(exact 7 parent: L1 = next to s_{j-1} -> sg = -1, L2 = next to s_j -> sg = +1).  Both orientations are emitted (mirror:
w offset o -> -o, s offset o -> -o-1, sg -> -sg).  Offsets are written mod d (as Studio's rules).
A `u` name acts only at d = its D; a centre-free name at every D' in 7..9 (w6) / 7..8 (w7) where PRIVCELL 1.4 places it.

Soundness check (independent of B3's naming code): for every rule, for every structural variant of the row (each link slot the
rule leaves free is 5, 6 or 7, i.e. 0, 1, >= 2 privates; each slot the rule allows several letters takes each of them), the
2-ball is built with k42/grow.py build2 and the entry's kc-line configuration must embed (grow.embeddings: exact degrees,
induced, interior triangles onto faces) into the vertices the rule pins (u, the pinned w / s, the parent and the killed private
at the killed letter), with the killed private in the image.  Then every row the rule matches contains the configuration
whenever the private has that letter.
Also checks the q-name against B3's route-entry text (key letters, side, extra slots).
usage: python3 mkrules.py GROW_PY PRIVCELL_PY OUTDIR CONFIG_FILE...   (writes OUTDIR/rules_{Ap,Lp,ApLp}.json, OUTDIR/rules_AL.tsv)"""
import sys, os, re, json, itertools, collections
GROW, PCPY, OUT = sys.argv[1:4]; CFGS = sys.argv[4:]
G = {'__file__': GROW, '__name__': 'grow'}; exec(open(GROW).read(), G)
PC = {'__name__': 'pc'}; exec(open(PCPY).read().split("if __name__ == '__main__':")[0], PC)

def offs(N, j, i, dd):
    """offset of link position i from the parent j, mod dd (centred name: mod N.d; centre-free: along its arc)"""
    if N.cu or dd == N.d: return (i - j) % dd
    a0, ln = PC['pc_arc'](N); return (((i - a0) % N.d) - ((j - a0) % N.d)) % dd

def mkrule(N, j, dd):
    wr = {}; sr = {}
    for i in range(N.d):
        if N.W[i] is not None and i != j:
            o = offs(N, j, i, dd); assert o not in wr; wr[o] = sorted(N.W[i])
        if N.S[i] is not None:
            assert len(N.S[i]) == 1, 'apex set not exact'
            o = offs(N, j, i, dd); assert o not in sr; sr[o] = next(iter(N.S[i]))
    return wr, sr

def mirror(wr, sr, dd): return {(-o) % dd: v for o, v in wr.items()}, {(-o - 1) % dd: v for o, v in sr.items()}

def verify(kc, dd, par, sg, p, wr, sr):
    """soundness check of one rule placed at spoke 0 of a d = dd row; sg = 0 for a 6 parent.  -> (ok, n variants, detail)"""
    cfg = G['kcline'](kc, 'B3'); i0 = 0
    free = [q for q in range(dd) if q != i0 and q not in wr]
    fixed = [q for q in range(dd) if q in wr]
    nv = 0; bad = []
    for fv in itertools.product((5, 6, 7), repeat=len(free)):
        for xv in itertools.product(*[wr[q] for q in fixed]):
            LK = [0] * dd; LK[i0] = par
            for q, v in zip(free, fv): LK[q] = v
            for q, v in zip(fixed, xv): LK[q] = v
            G['D'] = dd; G['LK'] = LK; G['SV'] = {}
            adj, name, faces = G['build2']({})
            inv = {v: x for x, v in name.items()}
            # the killed private: the private of w_0 next to s_{-1} (sg = -1 or 6-parent) or next to s_0 (sg = +1)
            sa = ('s', i0 if sg == 1 else (i0 - 1) % dd)
            pv = [x for x in adj[inv[sa]] if x in name and name[x][0] == 'p' and name[x][1] == i0]
            if len(pv) != 1: bad.append(('no unique private', LK)); continue
            pn = name[pv[0]]
            P = [('u',), ('w', i0)] + [('w', q) for q in fixed] + [('s', q) for q in sr] + [pn]
            fd = {('u',): dd, ('w', i0): par, pn: p}
            for q, v in zip(fixed, xv): fd[('w', q)] = v
            for q, v in sr.items(): fd[('s', q)] = v
            Ps = set(P)
            pa = {x: {name[y] for y in adj[inv[x]] if y in name and name[y] in Ps} for x in P}
            pf = {frozenset(name[y] for y in f) for f in faces if all(y in name and name[y] in Ps for y in f)}
            E = G['embeddings'](cfg, P, pa, pf, fd); nv += 1
            if not any(pn in {v for _, v in e} for e in E): bad.append(('no embedding', ''.join(map(str, LK))));
    return (not bad), nv, bad[:3]

def check_text(route, extra, N, j, sg):
    """B3's route-entry / extra-slot text vs the q-name; returns list of mismatches"""
    d = N.d; L = lambda S: '.' if S is None else str(next(iter(S))) if len(S) == 1 else '?'
    mm = []; slots = {}
    for i in range(d):
        if N.W[i] is not None and i != j: slots[('w', i)] = L(N.W[i])
        if N.S[i] is not None: slots[('s', i)] = L(N.S[i])
    seen = set()
    m = re.search(r'kill6 U=(\d+) w\(j-2,j-1,j\+1,j\+2\)=(\S{4}) s\(j-2,j-1,j,j\+1\)=(\S{4}) private=(\d)', route)
    if m:
        for k, o in enumerate((-2, -1, 1, 2)):
            x = ('w', (j + o) % d); seen.add(x)
            if m.group(2)[k] != slots.get(x, '.'): mm.append('key %s' % (x,))
        for k, o in enumerate((-2, -1, 0, 1)):
            x = ('s', (j + o) % d); seen.add(x)
            if m.group(3)[k] != slots.get(x, '.'): mm.append('key %s' % (x,))
    m = re.search(r'l3q side \(sigma=([+-]1), c,w2,w3,w4=(\S{4}), a=(\S), o=(\S)\)', route)
    if m:
        s_ = int(m.group(1))
        if s_ != sg: mm.append('sigma %d vs %d' % (s_, sg))
        for k in range(4):
            x = ('w', (j + (k + 1) * s_) % d); seen.add(x)
            if m.group(2)[k] != slots.get(x, '.'): mm.append('l3q %s' % (x,))
        xa = ('s', j if s_ == 1 else (j - 1) % d); xo = ('s', (j - 1) % d if s_ == 1 else j); seen |= {xa, xo}
        if m.group(3) != slots.get(xa, '.'): mm.append('a')
        if m.group(4) != slots.get(xo, '.'): mm.append('o')
    ex = {}
    for it in re.findall(r'([ws])(\d+)=(\d)', extra.split(':', 1)[1] if ':' in extra else ''): ex[(it[0], int(it[1]))] = it[2]
    for x, v in slots.items():
        if x in seen: continue
        if ex.get(x) != v: mm.append('extra %s=%s not listed' % (x, v))
    for x, v in ex.items():
        if slots.get(x) != v: mm.append('listed extra %s=%s not in name' % (x, v))
    return mm

groups = {k: collections.OrderedDict() for k in ('Ap', 'Lp')}   # (group, sg) -> {rule json string: entry ids}
tsv = []; nent = 0; summary = collections.Counter()
for cf in CFGS:
    route_kind = 'Lp' if 'l3qrow' in cf else 'Ap'
    for l in open(cf):
        if l.startswith('#') or not l.strip(): continue
        f = [x.strip() for x in l.rstrip('\n').split('|')]
        kc, route, extra, qn = f[0], f[1], f[2], f[3]; wname = kc.split()[0]; nent += 1
        N = PC['pc_parse'](qn)
        assert len(N.P) == 1 and not N.T, qn
        (j, side, k), = N.P.keys(); pset = N.P[(j, side, k)]; assert len(pset) == 1; p = next(iter(pset))
        par = PC['pc_exact'](N.W[j]); assert par in (6, 7), (qn, par)
        if route_kind == 'Ap': assert par == 6; sg = 0
        else:
            assert par == 7 and side == 'L' and k in (1, 2); sg = -1 if k == 1 else 1
        mm = check_text(route, extra, N, j, sg)
        okd = PC['pc_degrees'](N)
        Ds = [dd for dd in ((7, 8, 9) if par == 6 else (7, 8)) if okd(dd)]
        if not Ds:
            tsv.append([route_kind, wname, qn, '-', '-', '-', 'NOT PLACED (d=%d; f2b groups stop at d=9 / d=8)' % N.d, ';'.join(mm) or 'text ok']); summary['not placed'] += 1; continue
        for dd in Ds:
            wr, sr = mkrule(N, j, dd)
            for orient in (0, 1):
                w_, s_ = (wr, sr) if orient == 0 else mirror(wr, sr, dd); g_ = sg if orient == 0 else -sg
                ok, nv, bad = verify(kc, dd, par, g_, p, w_, s_)
                grp = ('d%d_w6' % dd) if par == 6 else ('d%d_w7' % dd)
                rule = [p, [[o, v] for o, v in sorted(w_.items())], [[o, v] for o, v in sorted(s_.items())]]
                key = (grp, g_); rs = json.dumps(rule)
                tsv.append([route_kind, wname, qn, dd, grp + ('' if par == 6 else '[%+d]' % g_), 'mirror' if orient else 'as named', rs,
                            ('VERIFIED (%d variants)' % nv) if ok else ('FAILED %s' % bad), ';'.join(mm) or 'text ok'])
                summary['verified' if ok else 'FAILED'] += 1
                if ok: groups[route_kind].setdefault(key, collections.OrderedDict()).setdefault(rs, []).append(wname)
def emit(kinds, fn):
    R = {'d7_w6': [], 'd8_w6': [], 'd9_w6': [], 'd7_w7': {'1': [], '-1': []}, 'd8_w7': {'1': [], '-1': []}}; n = 0
    for kd in kinds:
        for (grp, g_), rules in groups[kd].items():
            for rs in rules:
                r = json.loads(rs)
                tgt = R[grp] if g_ == 0 else R[grp]['%d' % g_]
                if r not in tgt: tgt.append(r); n += 1
    json.dump(R, open(fn, 'w'), indent=0); return n
os.makedirs(OUT, exist_ok=True)
nA = emit(['Ap'], os.path.join(OUT, 'rules_Ap.json')); nL = emit(['Lp'], os.path.join(OUT, 'rules_Lp.json')); nAL = emit(['Ap', 'Lp'], os.path.join(OUT, 'rules_ApLp.json'))
with open(os.path.join(OUT, 'rules_AL.tsv'), 'w') as o:
    o.write('# route\twindow\tq-name\td\tgroup[side]\torientation\trule [p, w_req, s_req] (offsets mod d)\tsoundness check\tq-name vs B3 text\n')
    for r in tsv: o.write('\t'.join(map(str, r)) + '\n')
print('entries %d; placements %s; distinct rules: A\' %d, L\' %d, together %d' % (nent, dict(summary), nA, nL, nAL))
for r in tsv:
    if 'FAILED' in str(r[7]) or (len(r) > 8 and r[8] != 'text ok') or 'NOT PLACED' in str(r[6]): print('  NOTE', r)
