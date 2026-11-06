"""ROT diagnosis (Studio): for rules dropped by DERIVE_ROT, replay DERIVE's emission (ZCONS-consistent Z only) for each
zcons justifier and report which rotcheck condition rejects each emitting embedding:
  nodeg  = an image has no full rotation or a different degree;  shift = no shift matches the interior neighbours (both signs);
  ring   = shifts exist for both... but ring-vertex images are inconsistent;  pass = rotation-preserving.
Also re-runs with ring consistency off (shift-only) and reports per-sign failures.  usage: diag_rot.py RULES.tsv OUT.tsv"""
import sys, os, json, collections
TSV, OUT = sys.argv[1], sys.argv[2]
sys.argv = ['f2b_rulecheck.py', 'x', 'y']; os.environ['DERIVE_ROT'] = '1'
M = {'__name__': 'diag', '__file__': os.path.abspath('out/job31/f2b_rulecheck.py')}
exec(open('out/job31/f2b_rulecheck.py').read(), M)
G, RC, ROTK = M['G'], M['RC'], M['ROTK']; FB = {c[0]: c for c in M['FORB']}
def why(phi, rotK, frm):
    adj, name, inv, rotF = frm; res = {}
    for sg in (1, -1):
        ring = {}; st = 'pass'
        order = sorted(phi, key=lambda u: -sum(x[0] == 'I' for x in rotK[u]))
        for u in order:
            rc = rotK[u]; v = phi[u]
            if v not in rotF or len(rotF[v]) != len(rc): st = 'nodeg'; break
            rf = rotF[v]; g = len(rc); intr = [(i, x[1]) for i, x in enumerate(rc) if x[0] == 'I']
            shifts = [(rf.index(phi[intr[0][1]]) - sg * intr[0][0]) % g] if intr and phi[intr[0][1]] in rf else ([] if intr else range(g))
            okshift = [t for t in shifts if not any(rf[(t + sg * i) % g] != phi[w] for i, w in intr)]
            if not okshift: st = 'shift'; break
            good = None
            for t in okshift:
                cand = {x[1]: rf[(t + sg * i) % g] for i, x in enumerate(rc) if x[0] == 'R'}
                if all(ring.get(j, fv) == fv for j, fv in cand.items()): good = cand; break
            if good is None: st = 'ring'; break
            ring.update(good)
        res[sg] = st
    return res
rows = [l.rstrip('\n').split('\t') for l in open(TSV) if not l.startswith('#')]
out = open(OUT, 'w'); out.write('# group\tside\trule\tjustifier\tZ\treasons(sign+1/sign-1) per emitting embedding\n'); tot = collections.Counter()
for grp, side, rule_s, just in rows:
    rule = json.loads(rule_s); d = int(grp[1]); w0 = int(grp[4]); sg = int(side)
    want = (rule[0], tuple(sorted((k, tuple(al)) for k, al in rule[1])), tuple(sorted((k, v) for k, v in rule[2])))
    for nm in just.split(','):
        cfg = FB[nm]; rk = ROTK[nm]
        for Z in range(0, 1 << d, 2):
            pa, pf = M['frame'](d, w0, Z)
            P = ([('u',)] if d in (7, 8) else []) + [('w', k) for k in range(d)] + [('s', k) for k in range(d)] + sorted(x for x in pa if x[0] == 'p' and x[1] == 0)
            fd = {('w', 0): w0}
            if d in (7, 8): fd[('u',)] = d
            Ps = set(P); pa2 = {x: pa[x] & Ps for x in P}; pf2 = {f for f in pf if f <= Ps}
            T = M['targets'](d, w0, pa); tt = tuple(T[0 if w0 == 6 else sg])
            for e in G['embeddings'](cfg, P, pa2, pf2, fd):
                r = tuple(sorted((v, cfg[3][u]) for u, v in e if v not in fd)); rd = dict(r)
                if tt not in rd or any(v[0] == 'p' and v != tt for v in rd): continue
                if any(v[0] == 'w' and v[1] >= 1 and (g == 5) != bool((Z >> v[1]) & 1) for v, g in r): continue
                wq = {v[1]: (g,) for v, g in r if v[0] == 'w'}; sq = {v[1]: g for v, g in r if v[0] == 's'}
                for k in range(1, d):
                    if (k - 1) in sq and k in sq and k not in wq: wq[k] = (5,) if (Z >> k) & 1 else (6, 7, 8, 9)
                if (rd[tt], tuple(sorted(wq.items())), tuple(sorted(sq.items()))) != want: continue
                lk = [w0] + [rd.get(('w', k), 5 if (Z >> k) & 1 else 6) for k in range(1, d)]
                frm = RC.frame_rotation(G, d, lk, {}, {v: g_ for v, g_ in r if v[0] in ('s', 'p')})
                rs = why({u: frm[2][v] for u, v in e}, rk, frm)
                tot[(rs[1], rs[-1])] += 1
                out.write('%s\t%s\t%s\t%s\t%d\t%s/%s\n' % (grp, side, rule_s, nm, Z, rs[1], rs[-1]))
out.close(); print('emitting embeddings by (sign +1, sign -1) outcome:', dict(tot))
