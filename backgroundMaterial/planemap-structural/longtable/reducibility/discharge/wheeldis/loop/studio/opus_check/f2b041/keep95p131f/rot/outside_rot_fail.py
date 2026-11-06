"""ROT step: for each outside-rule (full2ball_extra_rules.json) CHECK failure under DERIVE_ROT, list the face-set justifying
configurations at each failing structure Z and the rotcheck condition that rejects them (nodeg / shift / ring, per sign).
Our code only: f2b_rulecheck's preamble (frame, targets, embeddings) + rot/rotcheck.py.  usage: outside_rot_fail.py FAILJSON OUT.tsv"""
import sys, os, json, re, collections, multiprocessing as mp
FJ, OUT = sys.argv[1], sys.argv[2]
_ARGV = list(sys.argv); sys.argv = ['f2b_rulecheck.py', 'x', 'y']; os.environ['DERIVE_ROT'] = '1'
M = {'__name__': 'orf', '__file__': os.path.abspath('out/job31/f2b_rulecheck.py')}
exec(open('out/job31/f2b_rulecheck.py').read(), M); sys.argv = _ARGV   # restore (spawned workers re-read it)
G, RC, ROTK = M['G'], M['RC'], M['ROTK']
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'diag_rot.py')).read().split('rows = [l.rstrip')[0].split("exec(open('out/job31/f2b_rulecheck.py').read(), M)")[1].split('G, RC, ROTK')[1].split('\n', 1)[1])   # brings why()
GR = {'d7_w6': (7, 6), 'd8_w6': (8, 6), 'd9_w6': (9, 6), 'd7_w7': (7, 7), 'd8_w7': (8, 7)}
FAIL = json.load(open(FJ))['fail']
need = collections.defaultdict(list)
for i, (g, sg, n_, why_, rule) in enumerate(FAIL):
    for Z in map(int, re.findall(r'\d+', why_.split('[', 1)[1])): need[(GR[g][0], GR[g][1], Z)].append(i)
def work(key):
    d, w0, Z = key; pa, pf = M['frame'](d, w0, Z)
    P = ([('u',)] if d in (7, 8) else []) + [('w', k) for k in range(d)] + [('s', k) for k in range(d)] + sorted(x for x in pa if x[0] == 'p' and x[1] == 0)
    fd = {('w', 0): w0}
    if d in (7, 8): fd[('u',)] = d
    Ps = set(P); pa2 = {x: pa[x] & Ps for x in P}; pf2 = {f for f in pf if f <= Ps}; T = M['targets'](d, w0, pa)
    res = []
    for i in need[key]:
        g, sg, n_, _, (p, wq, sq) = FAIL[i]; tgt = tuple(T[0 if w0 == 6 else sg])
        wd = {o % d: set(al) for o, al in wq}; sd = {o % d: v for o, v in sq}; hits = collections.Counter(); names = set()
        for cfg in M['FORB']:
            for e in G['embeddings'](cfg, P, pa2, pf2, fd):
                r = tuple(sorted((v, cfg[3][u]) for u, v in e if v not in fd)); rd = dict(r)
                if rd.get(tgt) != p: continue
                if not all((v[0] == 'w' and wd.get(v[1]) == {gg}) or (v[0] == 's' and sd.get(v[1]) == gg) for v, gg in r if v != tgt): continue
                lk = [w0] + [rd.get(('w', k), 5 if (Z >> k) & 1 else 6) for k in range(1, d)]
                frm = RC.frame_rotation(G, d, lk, {}, {v: g_ for v, g_ in r if v[0] in ('s', 'p')})
                rs = why({u: frm[2][v] for u, v in e}, ROTK[cfg[0]], frm)
                names.add(cfg[0]); hits['%s/%s' % (rs[1], rs[-1])] += 1
        res.append((i, Z, sorted(names), dict(hits)))
    return res
if __name__ == '__main__':
    with mp.Pool(int(os.environ.get('NPROC', '6'))) as pool:
        R = [x for rs in pool.imap_unordered(work, sorted(need), chunksize=1) for x in rs]
    by = collections.defaultdict(list)
    for i, Z, nm, h in R: by[i].append((Z, nm, h))
    with open(OUT, 'w') as f:
        f.write('# group\tside\trule\tnamed justifiers (face-set CHECK, at the failing structures)\tfailed rotcheck condition (per emitting embedding: sign+1/sign-1 -> count)\tfailing structures Z\n')
        tot = collections.Counter()
        for i, (g, sg, n_, why_, rule) in enumerate(FAIL):
            nm = sorted({x for _, n, _ in by[i] for x in n}); h = collections.Counter()
            for _, _, hh in by[i]: h.update(hh)
            tot.update(h)
            f.write('%s\t%s\t%s\t%s\t%s\t%s\n' % (g, sg, json.dumps(rule), ','.join(nm) or '-', ';'.join('%s:%d' % kv for kv in sorted(h.items())), ','.join(str(Z) for Z, _, _ in sorted(by[i]))))
    print('rules', len(FAIL), 'condition totals', dict(tot))
