"""RELAY_SPEC section 21.4 (s28q, 321660a8): Studio's l3q payee mask tables, built from the spec text alone on explore's
grow.py (build2, embeddings), no Opus code. Window at the payee v (degree 7), u = w_0 (7), side sigma:
  known: v, u, c = w_{sigma}, w2 = w_{2 sigma}, w3 = w_{3 sigma}, w4 = w_{4 sigma} (= w_{-3 sigma}), a = the apex across
         (u, c) (s_0 for +, s_6 for -), o = u's other apex (s_6 for +, s_0 for -);
  free:  a2 = u's private adjacent to a;   unknown (strict, never in the target set): everything else.
Forbidden set: the registry of the solve: RSST D2 / C2cons (loop/k44/rsst_verdicts.txt, 582) + the kc lines of every
k3x name (D and C) at the given registry commit. A letter of a2 is killed when some embedding into the known vertices plus
a2 uses a2 at that letter (reading A, as section 14'); reading B (an embedding avoiding a2 kills every letter) is also
counted. Letter 9 is never an exact degree (grow.embeddings: free slots take 5..8; a known letter 9 matches nothing).
Table: sigma in (+1, -1), c, a in {5, 6}, w2, w3, w4, o in 5..9: 5,000 masks (bit k = letter 5 + k not killed).
Usage: [L3QV=8] python3 out/job31/l3q_masks.py K3X_D K3X_C OUTDIR
L3QV=8 (RELAY_SPEC s45.3 / s47 R9): the V = 8 table T_8: payee centre degree exactly 8, link length 8 (w4 = the antipode);
everything else as above (the default L3QV=7 is the section 21.4 table, unchanged)."""
import os, sys, re, glob, json, itertools, collections, hashlib
HERE = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
KD, KC, OUT = sys.argv[1], sys.argv[2], sys.argv[3]; os.makedirs(OUT, exist_ok=True)
G = {'__file__': os.path.join(HERE, 'loop', 'k42', 'grow.py'), '__name__': 'grow'}
exec(open(G['__file__']).read(), G)
ver = {}
for l in open(os.path.join(HERE, 'loop', 'k44', 'rsst_verdicts.txt')):
    if l.startswith('#') or not l.strip(): continue
    f = l.split(); v = [x for x in f if x.startswith('verdict=')]; ver[f[0].split('_')[0]] = v[0][8:] if v else None
R = [c for c in G['rsst']() if ver.get(c[0]) in ('D2', 'C2cons')]
if os.environ.get('RSSTC_KEEP'):   # s52c cover check: keep the RSST C2cons entries named in this file only (D2 all kept)
    _kp = {l.split()[0].split('_')[0] for l in open(os.environ['RSSTC_KEEP']) if l.strip() and not l.startswith('#') and l.startswith('rsst')}
    R = [c for c in R if ver.get(c[0]) == 'D2' or c[0] in _kp]; print('RSSTC_KEEP: %d RSST C2cons kept (%s)' % (sum(ver.get(c[0]) == 'C2cons' for c in R), sorted(_kp)), flush=True)
names = []
for fn in (KD, KC):
    for l in open(fn):
        if re.match(r'^[epf]\d+_\S+ r=\d+ ', l): names.append(l.split()[0])
names = list(dict.fromkeys(names)); want = set(names); kc = {}
for fn in sorted(glob.glob(os.path.join(HERE, 'loop', 'k[0-9]*', '*'))):
    if not os.path.isfile(fn): continue
    try: lines = open(fn).read().splitlines()
    except UnicodeDecodeError: continue
    for l in lines:
        f = l.split()
        if len(f) == 5 and f[0] in want and f[0] not in kc and f[1].isdigit() and f[2].isdigit() and ';' in f[3] + f[4]:
            kc[f[0]] = G['kcline'](l, 'k3x')
missing = [n for n in names if n not in kc]; assert not missing, ('no kc line', len(missing), missing[:5])
FORB = R + [kc[n] for n in names]
print('forbidden set: %d RSST + %d k3x (%s, %s) = %d configurations' % (len(R), len(names), os.path.basename(KD), os.path.basename(KC), len(FORB)), flush=True)
D = int(os.environ.get('L3QV', '7'))   # RELAY_SPEC s45.3: V = 8 -> link length 8, centre degree exactly 8 (V = 7 default unchanged)
assert D in (7, 8), 'V = 9 (centre never exact, excluded from embeddings) is not built here'
def frame(lk_fill, sv_fill):
    LK = [7] + [lk_fill] * 4 + [9] * (D - 5)   # u = w_0 = 7; w_1..w_4 placeholders; w_5..w_{D-1} placeholders (unknown for +)
    G['D'] = D; G['LK'] = LK; G['SV'] = {i: sv_fill for i in range(D)}
    adj, name, faces = G['build2']({('s', j): sv_fill for j in range(D)})
    pa = {x: {name[y] for y in adj[v] if y in name} for v, x in name.items()}
    pf = {frozenset(name[y] for y in f) for f in faces if all(y in name for y in f)}
    return pa, pf
def setup(sig, pa):
    W = lambda k: ('w', k % D); S = lambda k: ('s', k % D)
    a = S(0) if sig == 1 else S(-1); o = S(-1) if sig == 1 else S(0)
    priv = [x for x in pa if x[0] == 'p' and x[1] == 0]
    a2 = [x for x in priv if a in pa[x]]; assert len(a2) == 1, (sig, priv, a2)
    var = {'c': W(sig), 'w2': W(2 * sig), 'w3': W(3 * sig), 'w4': W(4 * sig), 'a': a, 'o': o, 'a2': a2[0]}
    return var
def reqs(P, pa, pf, fd):
    Ps = set(P); pa2 = {x: pa[x] & Ps for x in P}; pf2 = {f for f in pf if f <= Ps}; out = set()
    for cfg in FORB:
        for e in G['embeddings'](cfg, P, pa2, pf2, fd):
            out.add(tuple(sorted((v, cfg[3][u]) for u, v in e if v not in fd)))
    return out
TAB = {}; stats = collections.Counter(); REQ = {}
for sig in (1, -1):
    refs = []
    for lf, sf in ((6, 6), (5, 7), (8, 5)):   # placeholder letters: the known-vertex structure must not depend on them
        pa, pf = frame(lf, sf); var = setup(sig, pa)
        P = [('u',), ('w', 0)] + list(var.values()); fd = {('u',): D, ('w', 0): 7}
        Ps = set(P); refs.append(({x: pa[x] & Ps for x in P}, {f for f in pf if f <= Ps}))
    assert all(r == refs[0] for r in refs), 'known-vertex structure depends on placeholder letters'
    pa, pf = frame(6, 6); var = setup(sig, pa); inv = {v: k for k, v in var.items()}
    P = [('u',), ('w', 0)] + list(var.values()); fd = {('u',): D, ('w', 0): 7}
    rs = reqs(P, pa, pf, fd); REQ[sig] = [{inv[v]: g for v, g in r} for r in rs]
    print('sigma %+d: a2 = %s, a = %s, o = %s; %d requirement sets (%d use a2, %d avoid a2)' % (sig, var['a2'], var['a'], var['o'], len(rs),
          sum('a2' in r for r in REQ[sig]), sum('a2' not in r for r in REQ[sig])), flush=True)
    for c_, a_ in itertools.product((5, 6), repeat=2):
        for w2, w3, w4, o_ in itertools.product((5, 6, 7, 8, 9), repeat=4):
            ent = {'c': c_, 'a': a_, 'w2': w2, 'w3': w3, 'w4': w4, 'o': o_}
            killA = set(); killB = False
            for r in REQ[sig]:
                if all(ent[k] == v for k, v in r.items() if k != 'a2'):
                    if 'a2' in r: killA.add(r['a2'])
                    else: killB = True
            mA = sum(1 << (L - 5) for L in (5, 6, 7, 8, 9) if L not in killA)
            TAB[(sig, c_, a_, w2, w3, w4, o_)] = (mA, 0 if killB else mA)
            stats[(sig, mA)] += 1; stats[('B', sig, 0 if killB else mA)] += 1
print('reading A (kill only through a2): masks by side %s' % {k: v for k, v in sorted(stats.items(), key=str) if k[0] != 'B'})
print('reading B (an a2-free embedding kills all): %s' % {k: v for k, v in sorted(stats.items(), key=str) if k[0] == 'B'})
for sig in (1, -1):
    rows = [[c_, a_, w2, w3, w4, o_, TAB[(sig, c_, a_, w2, w3, w4, o_)][0]] for c_, a_ in itertools.product((5, 6), repeat=2) for w2, w3, w4, o_ in itertools.product((5, 6, 7, 8, 9), repeat=4)]
    fn = os.path.join(OUT, ('studio_l3qtab_%+d.json' if D == 7 else 'studio_l3qtabV%d_%%+d.json' % D) % sig); json.dump(rows, open(fn, 'w'))
    print('%s: md5 %s; killed letters: %s' % (os.path.basename(fn), hashlib.md5(open(fn, 'rb').read()).hexdigest(),
          dict(collections.Counter(tuple(L for L in range(5, 10) if not (r[6] >> (L - 5)) & 1) for r in rows))))
json.dump({str(s): [{k: v for k, v in r.items()} for r in REQ[s]] for s in REQ}, open(os.path.join(OUT, 'studio_l3q_reqs.json' if D == 7 else 'studio_l3qV%d_reqs.json' % D), 'w'))
