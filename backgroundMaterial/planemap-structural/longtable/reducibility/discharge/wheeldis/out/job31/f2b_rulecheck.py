"""f2b041 job 3 (Studio, 3 Nov): per-rule soundness of the full2ball rules, on Studio's l3q_masks machinery (explore's grow.py
build2 + induced embeddings). No outside or Opus code is run.

Claim of a rule (p, w_req, s_req) in group (d, w0[, side]): in every receiver arrangement of degree d whose spoke i has w_i = w0 and
satisfies w_req / s_req (offsets mod d from i), the private-letter slot of the group (w0 = 6: w0's private; w0 = 7, side +1 / -1:
w0's private adjacent to s_i / s_{i-1}, i.e. the l3q a2 of that side, as l3q_masks.setup) cannot have degree p, because some
forbidden configuration embeds in the 2-ball using that private at degree p (reading A).

Check: the 2-ball frame (u, w_0..w_{d-1}, s_0..s_{d-1}, w_0's privates) depends on the letters only through which w_k are 5
(w_k = 5 makes s_{k-1} s_k adjacent). For each such structure Z (bit k: w_k = 5) all embeddings of the forbidden set into the frame
with u (d = 7, 8; never at d = 9, the d >= 9 class) and w_0 at fixed degree are enumerated once (requirement sets, as l3q_masks.reqs).
A rule PASSES iff for EVERY structure Z consistent with it (w_k = 5 iff its allowed set is {5}; non-5 iff it is inside {6..9}; both
otherwise, including unconstrained k) some requirement set uses the target private at degree p and needs nothing the rule does not
fix: every other vertex it uses is a w_k with allowed set exactly {its degree} or an s_k with s_req = its degree.
usage: python3 out/job31/f2b_rulecheck.py RULES.json OUT.json  (env as the f2bA tables: EXTRA_KC, K3X D,C files; NPROC)"""
import os, sys, re, glob, json, itertools, collections, multiprocessing as mp
HERE = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
RULES, OUTF = sys.argv[1], sys.argv[2]
G = {'__file__': os.path.join(HERE, 'loop', 'k42', 'grow.py'), '__name__': 'grow'}
exec(open(G['__file__']).read(), G)
# ---- forbidden set: exactly as out/job31/l3q_masks.py (RSST D2 / C2cons + k3x D, C kc lines + EXTRA_KC raw kc lines) ----
ver = {}
for l in open(os.path.join(HERE, 'loop', 'k44', 'rsst_verdicts.txt')):
    if l.startswith('#') or not l.strip(): continue
    f = l.split(); v = [x for x in f if x.startswith('verdict=')]; ver[f[0].split('_')[0]] = v[0][8:] if v else None
FORB = [c for c in G['rsst']() if ver.get(c[0]) in ('D2', 'C2cons')]
if os.environ.get('RSSTC_KEEP'):   # job 2 keep-only: RSST C2cons only if named (as l3q_masks.py / st16_filter.py); D2 all kept
    _kp = {l.split()[0].split('_')[0] for l in open(os.environ['RSSTC_KEEP']) if l.strip() and not l.startswith('#') and l.startswith('rsst')}
    FORB = [c for c in FORB if ver.get(c[0]) == 'D2' or c[0] in _kp]
KD, KC = os.environ['K3X'].split(',')
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
assert not [n for n in names if n not in kc]
FORB += [kc[n] for n in names]; _seen = {c[0] for c in FORB}
for _fn in os.environ.get('EXTRA_KC', '').split(','):
    if not _fn: continue
    for _l in open(_fn):
        if not _l.strip() or _l[0].isspace() or _l.startswith('#'): continue
        _f = _l.split()
        if len(_f) >= 5 and _f[1].isdigit() and _f[2].isdigit() and ';' in _f[3] + _f[4]:
            _c = G['kcline'](_l, 'extra')
            if _c[0] not in _seen: _seen.add(_c[0]); FORB.append(_c)
print('forbidden set %d configurations' % len(FORB), flush=True)

def frame(d, w0, Z):
    G['D'] = d; G['LK'] = [w0] + [5 if (Z >> k) & 1 else 6 for k in range(1, d)]; G['SV'] = {}
    adj, name, faces = G['build2']({})
    pa = {x: {name[y] for y in adj[v] if y in name} for v, x in name.items()}
    pf = {frozenset(name[y] for y in f) for f in faces if all(y in name for y in f)}
    return pa, pf
def targets(d, w0, pa):
    pr = sorted(x for x in pa if x[0] == 'p' and x[1] == 0)
    if w0 == 6: assert len(pr) == 1; return {0: pr[0]}
    t = {}
    for sg, a in ((1, ('s', 0)), (-1, ('s', d - 1))):
        q = [x for x in pr if a in pa[x]]; assert len(q) == 1, (d, sg, pr, q); t[sg] = q[0]
    return t
def job(arg):
    d, w0, Z = arg
    pa, pf = frame(d, w0, Z)
    P = ([('u',)] if d in (7, 8) else []) + [('w', k) for k in range(d)] + [('s', k) for k in range(d)] + sorted(x for x in pa if x[0] == 'p' and x[1] == 0)
    fd = {('w', 0): w0}
    if d in (7, 8): fd[('u',)] = d
    Ps = set(P); pa2 = {x: pa[x] & Ps for x in P}; pf2 = {f for f in pf if f <= Ps}
    T = targets(d, w0, pa); tset = set(T.values()); out = set()
    for cfg in FORB:
        for e in G['embeddings'](cfg, P, pa2, pf2, fd):
            r = tuple(sorted((v, cfg[3][u]) for u, v in e if v not in fd))
            if any(v in tset for v, _ in r): out.add(r)
    for k in range(1, d):   # structure sanity: s_{k-1} s_k adjacent iff w_k = 5
        assert ((('s', k) in pa[('s', k - 1)]) == bool((Z >> k) & 1)), (d, Z, k)
    return (d, w0, Z), {str(sg): v for sg, v in T.items()}, sorted(out)

if __name__ == '__main__':
    RJ = json.load(open(RULES))
    groups = [('d7_w6', 7, 6, 0), ('d8_w6', 8, 6, 0), ('d9_w6', 9, 6, 0), ('d7_w7', 7, 7, 1), ('d7_w7', 7, 7, -1), ('d8_w7', 8, 7, 1), ('d8_w7', 8, 7, -1)]
    jobs = sorted({(d, w0, Z) for _, d, w0, _ in groups for Z in range(0, 1 << d, 2)})   # bit 0 (w_0) unused
    print('structures to enumerate: %d' % len(jobs), flush=True)
    with mp.Pool(int(os.environ.get('NPROC', '8'))) as pool:
        RES = {}; TG = {}
        for n_, (key, tg, rs) in enumerate(pool.imap_unordered(job, jobs, chunksize=1)):
            RES[key] = rs; TG[key[:2]] = tg
            if n_ % 50 == 0: print('  %d / %d structures' % (n_, len(jobs)), flush=True)
    if os.environ.get('DERIVE'):   # job 2: Studio's own rule set from the same requirement sets (rules JSON format, offsets 0..d-1)
        DR = {'d7_w6': set(), 'd8_w6': set(), 'd9_w6': set(), 'd7_w7': {'1': set(), '-1': set()}, 'd8_w7': {'1': set(), '-1': set()}}
        for (d, w0, Z), rs in RES.items():
            for sgs, t in TG[(d, w0)].items():
                tt = tuple(t)
                for r in rs:
                    rd = dict(r)
                    if tt not in rd or any(v[0] == 'p' and v != tt for v in rd): continue
                    wq = {v[1]: (g,) for v, g in r if v[0] == 'w'}; sq = {v[1]: g for v, g in r if v[0] == 's'}
                    for k in range(1, d):
                        if (k - 1) in sq and k in sq and k not in wq: wq[k] = (5,) if (Z >> k) & 1 else (6, 7, 8, 9)
                    rule = (rd[tt], tuple(sorted((k, al) for k, al in wq.items())), tuple(sorted(sq.items())))
                    (DR['d%d_w6' % d] if w0 == 6 else DR['d%d_w7' % d][sgs]).add(rule)
        enc = lambda S: [[p, [[k, list(al)] for k, al in wq], [[k, v] for k, v in sq]] for p, wq, sq in sorted(S)]
        J = {g: (enc(v) if isinstance(v, set) else {sg: enc(x) for sg, x in v.items()}) for g, v in DR.items()}
        json.dump(J, open(os.environ['DERIVE'], 'w'))
        print('DERIVE: %s -> %s' % ({g: (len(v) if isinstance(v, set) else {k: len(x) for k, x in v.items()}) for g, v in DR.items()}, os.environ['DERIVE']), flush=True)
    rep = {'targets': {'%d_%d' % k: v for k, v in TG.items()}, 'groups': {}, 'fail': []}
    CTRL = os.environ.get('CONTROL', '')   # negative controls: 'swap' = w7 rules checked against the other side's private; 'pshift' = killed letter p -> p+1 (9 -> 5)
    for gname, d, w0, sg in groups:
        rl = RJ[gname] if w0 == 6 else RJ[gname][str(sg)]
        tgt = tuple(TG[(d, w0)][str(sg if CTRL != 'swap' or w0 == 6 else -sg)])
        if CTRL == 'pshift': rl = [[5 if p == 9 else p + 1, wq, sq] for p, wq, sq in rl]
        cnt = collections.Counter()
        for n_, (p, wq, sq) in enumerate(rl):
            wd = {o % d: set(al) for o, al in wq}; sd = {o % d: v for o, v in sq}
            if len(wd) != len(wq) or len(sd) != len(sq) or 0 in wd: cnt['malformed'] += 1; rep['fail'].append([gname, sg, n_, 'malformed', [p, wq, sq]]); continue
            opts = []
            for k in range(1, d):
                al = wd.get(k)
                if al is None or (5 in al and len(al) > 1): opts.append((0, 1))
                elif al == {5}: opts.append((1,))
                else: opts.append((0,))
            badZ = []
            for bits in itertools.product(*opts):
                Z = sum(b << (k + 1) for k, b in enumerate(bits)); ok = False
                for r in RES[(d, w0, Z)]:
                    rd = dict(r)
                    if rd.get(tgt) != p: continue
                    if all((v[0] == 'w' and wd.get(v[1]) == {g}) or (v[0] == 's' and sd.get(v[1]) == g) for v, g in r if v != tgt): ok = True; break
                if not ok: badZ.append(Z)
            if badZ: cnt['FAIL'] += 1; rep['fail'].append([gname, sg, n_, 'no embedding for structures %s' % badZ[:8], [p, wq, sq]])
            else: cnt['PASS'] += 1
            cnt['structures_checked'] += len(list(itertools.product(*opts)))
        rep['groups']['%s%s' % (gname, '' if w0 == 6 else ('_%+d' % sg))] = dict(cnt)
        print('%s side %s: %d rules, target %s: %s' % (gname, sg, len(rl), tgt, dict(cnt)), flush=True)
    json.dump(rep, open(OUTF, 'w'), indent=1)
    print('TOTAL%s: PASS %d FAIL %d' % (' (CONTROL=%s)' % CTRL if CTRL else '', sum(g.get('PASS', 0) for g in rep['groups'].values()), len(rep['fail'])), flush=True)
