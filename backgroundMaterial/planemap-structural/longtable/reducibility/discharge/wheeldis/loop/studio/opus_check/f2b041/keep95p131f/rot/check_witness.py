"""ROT (Studio): CHECK a rule against a GIVEN witness configuration with the rotation-preserving test.
A rule PASSES for the witness iff for EVERY structure Z consistent with the rule (as f2b_rulecheck CHECK) the witness has a
rotation-preserving embedding that uses the target private at degree p and needs nothing the rule does not fix.
Also reports the face-set-only outcome.  usage: check_witness.py IN.tsv(group side rule ... witness at column W) WCOL OUT.tsv"""
import sys, os, json, itertools, collections, multiprocessing as mp
TSV, WCOL, OUT = sys.argv[1], int(sys.argv[2]), sys.argv[3]
_ARGV = list(sys.argv); sys.argv = ['f2b_rulecheck.py', 'x', 'y']; os.environ['DERIVE_ROT'] = '1'
M = {'__name__': 'cw', '__file__': os.path.abspath('out/job31/f2b_rulecheck.py')}
exec(open('out/job31/f2b_rulecheck.py').read(), M); sys.argv = _ARGV   # restore (spawned workers re-read it)
G, RC, ROTK = M['G'], M['RC'], M['ROTK']; FB = {c[0]: c for c in M['FORB']}
rows = [l.rstrip('\n').split('\t') for l in open(TSV) if l.strip() and not l.startswith('#')]
def one(row):
    g, side, rule_s = row[0], int(row[1]), row[2]; wits = row[WCOL].split(','); d = int(g[1]); w0 = int(g[4])
    p, wq, sq = json.loads(rule_s); wd = {o % d: set(al) for o, al in wq}; sd = {o % d: v for o, v in sq}
    opts = []
    for k in range(1, d):
        al = wd.get(k)
        opts.append((0, 1) if al is None or (5 in al and len(al) > 1) else ((1,) if al == {5} else (0,)))
    badF, badR = [], []
    for bits in itertools.product(*opts):
        Z = sum(b << (k + 1) for k, b in enumerate(bits)); pa, pf = M['frame'](d, w0, Z)
        P = ([('u',)] if d in (7, 8) else []) + [('w', k) for k in range(d)] + [('s', k) for k in range(d)] + sorted(x for x in pa if x[0] == 'p' and x[1] == 0)
        fd = {('w', 0): w0}
        if d in (7, 8): fd[('u',)] = d
        Ps = set(P); pa2 = {x: pa[x] & Ps for x in P}; pf2 = {f for f in pf if f <= Ps}
        tgt = tuple(M['targets'](d, w0, pa)[0 if w0 == 6 else side]); okF = okR = False
        for nm in wits:
            if nm not in FB: continue
            cfg = FB[nm]
            for e in G['embeddings'](cfg, P, pa2, pf2, fd):
                r = tuple(sorted((v, cfg[3][u]) for u, v in e if v not in fd)); rd = dict(r)
                if rd.get(tgt) != p: continue
                if not all((v[0] == 'w' and wd.get(v[1]) == {gg}) or (v[0] == 's' and sd.get(v[1]) == gg) for v, gg in r if v != tgt): continue
                if any(v[0] == 'w' and v[1] >= 1 and (gg == 5) != bool((Z >> v[1]) & 1) for v, gg in r): continue   # ZCONS: requirement letters agree with Z
                okF = True
                lk = [w0] + [rd.get(('w', k), 5 if (Z >> k) & 1 else 6) for k in range(1, d)]
                frm = RC.frame_rotation(G, d, lk, {}, {v: g_ for v, g_ in r if v[0] in ('s', 'p')})
                if RC.rot_ok({u: frm[2][v] for u, v in e}, ROTK[nm], frm): okR = True; break
            if okR: break
        if not okF: badF.append(Z)
        if not okR: badR.append(Z)
    return row, badF, badR, [n for n in wits if n not in FB]
if __name__ == '__main__':
    with mp.Pool(int(os.environ.get('NPROC', '4'))) as pool: R = list(pool.imap(one, rows))
    c = collections.Counter()
    with open(OUT, 'w') as f:
        f.write('# group\tside\trule\twitness\tface-set result\trotation-preserving result\tstructures failing (rotation)\n')
        for row, bF, bR, miss in R:
            st = 'PASS' if not bR else 'FAIL'; c[st] += 1
            f.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % (row[0], row[1], row[2], row[WCOL] + (' (not in forbidden set: %s)' % miss if miss else ''), 'PASS' if not bF else 'FAIL %s' % bF[:8], st, bR[:8]))
    print('rows', len(R), dict(c))
