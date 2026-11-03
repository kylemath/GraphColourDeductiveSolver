"""f2b041 job 2 (Studio): which DROPPED C configurations justify what the keep set loses. Same frame and embeddings as
f2b_rulecheck.py, forbidden set = only the C configurations of the full Tier A set that are not in KEEP (RSST C2cons, k3x C, k3p C).
Reports, by configuration name: (1) the outside rules that fail on the keep set (KEEPCHECK json 'fail' list) and the
configurations that justify each; (2) the V8 mask kills lost (full table vs keep table) and the configurations that justify each.
usage: (env as f2b_rulecheck full Tier A) KEEP=keep.txt KEEPCHECK=rulecheck_keep.json V8FULL=tab%s V8KEEP=tab%s python3 f2b_dropnames.py OUT.json"""
import os, sys, json, re, itertools, collections, multiprocessing as mp
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'f2b_rulecheck.py')).read()
pre = src[:src.index("def frame(d, w0, Z):")]; body = src[src.index("def frame(d, w0, Z):"):src.index("if __name__ == '__main__':")]
sys.argv = [sys.argv[0], 'x', sys.argv[1]]; OUTF = sys.argv[2]
G0 = {'__file__': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'f2b_rulecheck.py'), '__name__': 'x'}
exec(pre, G0); FORB = G0['FORB']; ver = G0['ver']; G = G0['G']
kp = {l.split()[0] for l in open(os.environ['KEEP']) if l.strip() and not l.startswith('#')}; kpr = {x.split('_')[0] for x in kp if x.startswith('rsst')}
cset = set()
for fn in [os.environ['K3X'].split(',')[1]] + [f for f in os.environ.get('EXTRA_KC', '').split(',') if f.endswith('.cfast')]:
    for l in open(fn):
        m = re.match(r'^([A-Za-z]\w*_\S+) ', l)
        if m and not l[0].isspace(): cset.add(m.group(1))
DROP = [c for c in FORB if (ver.get(c[0]) == 'C2cons' and c[0].split('_')[0] not in kpr) or (c[0] in cset and c[0] not in kp)]
print('dropped C configurations: %d' % len(DROP), flush=True)
G0['FORB'] = DROP; exec(body, G0)
def job(arg):
    d, w0, Z = arg
    pa, pf = G0['frame'](d, w0, Z)
    P = ([('u',)] if d in (7, 8) else []) + [('w', k) for k in range(d)] + [('s', k) for k in range(d)] + sorted(x for x in pa if x[0] == 'p' and x[1] == 0)
    fd = {('w', 0): w0}
    if d in (7, 8): fd[('u',)] = d
    Ps = set(P); pa2 = {x: pa[x] & Ps for x in P}; pf2 = {f for f in pf if f <= Ps}
    T = G0['targets'](d, w0, pa); tset = set(T.values()); out = collections.defaultdict(set)
    for cfg in DROP:
        for e in G['embeddings'](cfg, P, pa2, pf2, fd):
            r = tuple(sorted((v, cfg[3][u]) for u, v in e if v not in fd))
            if any(v in tset for v, _ in r): out[r].add(cfg[0])
    return (d, w0, Z), {str(sg): v for sg, v in T.items()}, dict(out)
if __name__ == '__main__':
    groups = [(7, 6), (8, 6), (9, 6), (7, 7), (8, 7)]
    jobs = [(d, w0, Z) for d, w0 in groups for Z in range(0, 1 << d, 2)]
    RES = {}; TG = {}
    with mp.Pool(int(os.environ.get('NPROC', '6'))) as pool:
        for key, tg, rs in pool.imap_unordered(job, jobs): RES[key] = rs; TG[key[:2]] = tg
    rep = {'dropped': len(DROP), 'rules': [], 'v8': [], 'by_config': collections.Counter()}
    RJ = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'loop', 'studio', 'opus_check', 'f2b041', 'in', 'gc', 'kill_upgraded', 'tierA', 'full2ball_extra_rules.json')))
    for gname, sg, n_, why, rule in json.load(open(os.environ['KEEPCHECK']))['fail']:
        p, wq, sq = rule; d = int(gname[1]); w0 = int(gname[-1]); tgt = tuple(TG[(d, w0)][str(sg if w0 == 7 else 0)])
        wd = {o % d: set(al) for o, al in wq}; sd = {o % d: v for o, v in sq}; who = set()
        opts = [((0, 1) if (k not in wd or (5 in wd[k] and len(wd[k]) > 1)) else ((1,) if wd[k] == {5} else (0,))) for k in range(1, d)]
        for bits in itertools.product(*opts):
            Z = sum(b << (k + 1) for k, b in enumerate(bits))
            for r, nms in RES[(d, w0, Z)].items():
                rd = dict(r)
                if rd.get(tgt) == p and all((v[0] == 'w' and wd.get(v[1]) == {g}) or (v[0] == 's' and sd.get(v[1]) == g) for v, g in r if v != tgt): who |= nms
        rep['rules'].append([gname, sg, n_, sorted(who)]); rep['by_config'].update(who)
    def mt(p):
        M = {}
        for sg_, f in ((1, p % '+1'), (-1, p % '-1')):
            for r in json.load(open(f)): M[(sg_,) + tuple(r[:6])] = r[6]
        return M
    MF, MK = mt(os.environ['V8FULL']), mt(os.environ['V8KEEP']); d, w0 = 8, 7
    for key, mf in MF.items():
        lost = (MK[key] & ~mf) & 31
        if not lost: continue
        sg, c_, a_, w2, w3, w4, o_ = key; tgt = tuple(TG[(8, 7)][str(sg)])
        known = {('w', sg % 8): c_, ('w', (2 * sg) % 8): w2, ('w', (3 * sg) % 8): w3, ('w', (4 * sg) % 8): w4,
                 ('s', 0 if sg == 1 else 7): a_, ('s', 7 if sg == 1 else 0): o_}
        Z = sum(1 << k for k in range(1, 8) if known.get(('w', k)) == 5)
        for L in range(5, 10):
            if not (lost >> (L - 5)) & 1: continue
            who = set()
            for r, nms in RES[(8, 7, Z)].items():
                rd = dict(r)
                if rd.get(tgt) == L and all(v == tgt or known.get(v) == g for v, g in r): who |= nms
            rep['v8'].append([list(key), L, sorted(who)]); rep['by_config'].update(who)
    rep['by_config'] = rep['by_config'].most_common()
    json.dump(rep, open(OUTF, 'w'), indent=0)
    print('rules: %d failing, %d with a dropped justifying configuration; V8 lost kills %d, %d justified; distinct configurations %d' % (
        len(rep['rules']), sum(1 for x in rep['rules'] if x[3]), len(rep['v8']), sum(1 for x in rep['v8'] if x[2]), len(rep['by_config'])), flush=True)
    for nm, n in rep['by_config'][:30]: print('  %4d %s' % (n, nm))
