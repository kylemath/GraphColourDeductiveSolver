"""Stage 16 A' private filter (RELAY_SPEC section 14', 3b972410), built by Studio from the spec alone on explore's
grow.py / rings.py (the tools the spec names); no Opus code.
Forbidden set (spec 14'): the 582 RSST configurations with verdict D2 or C2cons in loop/k44/rsst_verdicts.txt (read by
grow.rsst() from unavoidable.conf), plus the 1,427 twoeng names of k3x_D/C at 09d8ac38 read as configurations from their
kc lines (first match over loop/k[0-9]*/*; every name must have one).
Containment: grow.embeddings (exact degrees, induced, interior triangles onto faces) into the named vertices of u's
3-ball (grow.build2). A configuration vertex may land only on a *known* vertex (strict rule): unknown vertices, and any
fixed vertex with letter 9 (= degree >= 9, never exact), are left out of the target set entirely; variable slots take
5..8 only.
1) check 4 full test: binder 7665566/6675666, each private slot alone variable, the other privates unknown.
2) LP test kill tables K_U (U = 7, 8, 9): a value of p is killed only by an embedding that uses p. Known = u
   (degree U for U = 7; unknown, never matched, for U = 8 and 9: the fcdd458e fix), w_{j-2..j+2} with w_j = 6,
   s_{j-2..j+1}, and w_j's private p; all else unknown. Indexed [w_{j-2}, w_{j-1}, w_{j+1}, w_{j+2}, s_{j-2}, s_{j-1},
   s_j, s_{j+1}, p] (letters 5..9 -> 0..4), True = p killed.
3) check 4 LP projection (survivors and md5), mirror symmetry, U8 == U9, and the unknown-code variants (unknown link
   letters 5 or 7 in the frame) under the strict rule; also the non-strict code-5 variant as the spec's control.
Usage: python3 out/job31/st16_filter.py OUTDIR"""
import os, sys, re, glob, json, itertools, collections, hashlib
import numpy as np
HERE = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'out', 'job31', 'st16')
os.makedirs(OUT, exist_ok=True)
G = {'__file__': os.path.join(HERE, 'loop', 'k42', 'grow.py'), '__name__': 'grow'}
exec(open(G['__file__']).read(), G)
LET = (5, 6, 7, 8, 9)

# ---- forbidden set ----
ver = {}
for l in open(os.path.join(HERE, 'loop', 'k44', 'rsst_verdicts.txt')):
    if l.startswith('#') or not l.strip(): continue
    f = l.split(); v = [x for x in f if x.startswith('verdict=')]
    ver[f[0].split('_')[0]] = v[0][8:] if v else None
R = [c for c in G['rsst']() if ver.get(c[0]) in ('D2', 'C2cons')]
names = []
K3X = os.environ.get('K3X')   # 'D_FILE,C_FILE' (s33z: the solve's registry); default the 09d8ac38 pair
for fn in (K3X.split(',') if K3X else (os.path.join(HERE, 'loop', 'studio', 'opus_check', 'k3x_D_09d8ac38.out'), os.path.join(HERE, 'loop', 'studio', 'opus_check', 'k3x_C_09d8ac38.cfast'))):
    for l in open(fn if os.path.isabs(fn) else os.path.join(HERE, fn)):
        if re.match(r'^[epf]\d+_\S+ r=\d+ ', l): names.append(l.split()[0])
names = list(dict.fromkeys(names))
want = set(names); kc = {}
for fn in sorted(glob.glob(os.path.join(HERE, 'loop', 'k[0-9]*', '*'))):
    if not os.path.isfile(fn): continue
    try: lines = open(fn).read().splitlines()
    except UnicodeDecodeError: continue
    for l in lines:
        f = l.split()
        if len(f) == 5 and f[0] in want and f[0] not in kc and f[1].isdigit() and f[2].isdigit() and ';' in f[3] + f[4]:
            kc[f[0]] = G['kcline'](l, 'twoeng')
missing = [n for n in names if n not in kc]
assert not missing, ('no kc line', missing[:5])
FORB = R + [kc[n] for n in names]
print('forbidden set: %d RSST (D2 %d, C2cons %d) + %d twoeng = %d' % (len(R), sum(ver.get(c[0]) == 'D2' for c in R),
      sum(ver.get(c[0]) == 'C2cons' for c in R), len(names), len(FORB)), flush=True)

def frame(D, LK, SV):
    G['D'] = D; G['LK'] = LK; G['SV'] = dict(SV)
    r2 = {('s', j): v for j, v in SV.items()}
    adj, name, faces = G['build2'](r2)
    nm = {v: x for v, x in name.items()}
    pa = {x: {name[y] for y in adj[v] if y in name} for v, x in nm.items()}
    pf = {frozenset(name[y] for y in f) for f in faces if all(y in name for y in f)}
    return pa, pf
def reqs(P, pa, pf, fd):
    """requirement dicts {variable name: degree} of every embedding of every forbidden configuration into P."""
    Ps = set(P); pa2 = {x: pa[x] & Ps for x in P}; pf2 = {f for f in pf if f <= Ps}; out = set(); who = collections.defaultdict(set)
    for c in FORB:
        for e in G['embeddings'](c, P, pa2, pf2, fd):
            r = tuple(sorted((v, c[3][u]) for u, v in e if v not in fd))
            out.add(r); who[r].add(c[0])
    return out, who

# ---- 1) check 4, full test ----
D, LK, SW = 7, [7, 6, 6, 5, 5, 6, 6], [6, 6, 7, 5, 6, 6, 6]
pa, pf = frame(D, LK, {i: SW[i] for i in range(D)})
PRIV = [('p', i, k) for i in range(D) for k in range(1, LK[i] - 4)]
fixed = {('u',): D}
for i in range(D): fixed[('w', i)] = LK[i]; fixed[('s', i)] = SW[i]
kills_full = {}
for slot in PRIV:
    P = list(fixed) + [slot]
    rs, who = reqs(P, pa, pf, dict(fixed))
    kills_full[slot] = {dict(r)[slot]: sorted(who[r]) for r in rs if r}   # value -> configurations
    for r in rs: assert r and r[0][0] == slot
print('check 4 full test, per-slot kills: %s' % {'p%d%d' % (s[1], s[2]): {v: w for v, w in sorted(kills_full[s].items())} for s in PRIV})
surv_full = [pv for pv in itertools.product(LET, repeat=6) if all(pv[k] not in kills_full[s] for k, s in enumerate(PRIV))]
print('check 4 full test: %d survivors (spec 3,072)' % len(surv_full), flush=True)

# ---- 2) LP test kill tables ----
J = 2
KN_W = [('w', J - 2), ('w', J - 1), ('w', J + 1), ('w', J + 2)]
KN_S = [('s', J - 2), ('s', J - 1), ('s', J), ('s', J + 1)]
SLOTS = KN_W + KN_S + [('p', J, 1)]
def table(U, unk=6, strict=True, unkdeg=None):
    """kill table for receiver letter U; unk = letter given to unknown link vertices in the frame; strict leaves unknown
    vertices out of the target set (non-strict: they join it with fixed degree unkdeg)."""
    Dd = U if U in (7, 8) else 9
    K = np.zeros((5,) * 9, dtype=bool)
    for c1, c2 in itertools.product((5, 6), repeat=2):          # w_{j-1}, w_{j+1}: 5 or not (only that changes the structure)
        LKf = [unk] * Dd; LKf[J] = 6; LKf[J - 1] = c1; LKf[J + 1] = c2; LKf[J - 2] = 6; LKf[J + 2] = 6
        SVf = {i: 6 for i in range(Dd)}
        pa, pf = frame(Dd, LKf, SVf)
        known = ([('u',)] if U == 7 else []) + [('w', J)] + SLOTS
        fd = {('w', J): 6}
        if U == 7: fd[('u',)] = U
        P = list(known)
        if not strict:
            extra = [x for x in pa if x not in known and x[0] in ('u', 'w', 's', 'p')]
            P += extra
            for x in extra: fd[x] = unkdeg
        rs, _ = reqs(P, pa, pf, fd)
        for r in rs:
            rd = dict(r)
            if ('p', J, 1) not in rd: continue   # spec 14': a value is killed when some configuration embeds *using it*
            w1, w2 = rd.get(('w', J - 1)), rd.get(('w', J + 1))
            if w1 is not None and (w1 == 5) != (c1 == 5): continue
            if w2 is not None and (w2 == 5) != (c2 == 5): continue
            idx = []
            for k, sl in enumerate(SLOTS):
                if sl in rd: idx.append(rd[sl] - 5)
                elif k == 1: idx.append(slice(0, 1) if c1 == 5 else slice(1, 5))
                elif k == 2: idx.append(slice(0, 1) if c2 == 5 else slice(1, 5))
                else: idx.append(slice(None))
            K[tuple(idx)] = True
    return K
def mirror(K): return np.transpose(K, (3, 2, 1, 0, 7, 6, 5, 4, 8))
TAB = {}
for U in (7, 8, 9):
    K = table(U); TAB[U] = K
    np.save(os.path.join(OUT, 'kill_U%d.npy' % U), K)
    A = np.zeros((5,) * 8, dtype=np.uint8)
    for b_ in range(5): A |= (K[..., b_].astype(np.uint8) << b_)
    fnl = os.path.join(OUT, 'kill6_U%d.npy' % U); np.save(fnl, np.ascontiguousarray(A))
    print('K_U%d in the spec layout (uint8 (5,)*8, bit i = letter 5+i killed): file md5 %s, raw-array md5 %s' % (
        U, hashlib.md5(open(fnl, 'rb').read()).hexdigest(), hashlib.md5(A.tobytes()).hexdigest()), flush=True)
    print('K_U%d: %d killed (window, p) of %d; mirror-symmetry exceptions %d; tobytes md5 %s' % (
        U, int(K.sum()), K.size, int((K != mirror(K)).sum()), hashlib.md5(K.tobytes()).hexdigest()), flush=True)
print('U8 == U9: %s' % bool((TAB[8] == TAB[9]).all()))
def lp_survivors(T7):
    W, S = LK, SW; out = []
    vis = {}
    for i in range(D):
        if W[i] != 6: continue
        key = [W[(i - 2) % D], W[(i - 1) % D], W[(i + 1) % D], W[(i + 2) % D], S[(i - 2) % D], S[(i - 1) % D], S[i], S[(i + 1) % D]]
        vis[('p', i, 1)] = {p for p in LET if T7[tuple(x - 5 for x in key) + (p - 5,)]}
    for pv in itertools.product(LET, repeat=6):
        if all(pv[k] not in vis.get(s, ()) for k, s in enumerate(PRIV)): out.append(''.join(map(str, pv)))
    return out, vis
s4, vis = lp_survivors(TAB[7])
for tail in ('\n', ''):
    print('check 4 LP projection: %d survivors (spec 7,500); md5 of sorted lines joined by newline%s: %s' % (
        len(s4), ' + trailing newline' if tail else '', hashlib.md5(('\n'.join(sorted(s4)) + tail).encode()).hexdigest()))
print('LP-visible kills at the binder: %s' % {'p%d%d' % (s[1], s[2]): sorted(v) for s, v in vis.items()}, flush=True)
for code in (5, 7):
    same = all((table(U, unk=code) == TAB[U]).all() for U in (7, 8, 9))
    print('unknown link letters coded %d, strict: tables identical to the default: %s' % (code, same), flush=True)
K5 = table(7, unk=5, strict=False, unkdeg=5); s5, _ = lp_survivors(K5)
print('control, non-strict with unknowns as degree 5: %d survivors (spec 3,072 = the failure the strict rule prevents); md5 %s'
      % (len(s5), hashlib.md5(('\n'.join(sorted(s5)) + '\n').encode()).hexdigest()), flush=True)
json.dump({'kills_full': {'p%d%d' % (s[1], s[2]): {str(v): w for v, w in kills_full[s].items()} for s in PRIV}}, open(os.path.join(OUT, 'check4_full.json'), 'w'), indent=1)
open(os.path.join(OUT, 'check4_lp_survivors.txt'), 'w').write('\n'.join(sorted(s4)) + '\n')
