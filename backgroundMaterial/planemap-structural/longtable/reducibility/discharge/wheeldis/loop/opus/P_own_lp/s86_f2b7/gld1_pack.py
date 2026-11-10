# s86 (10 Nov 03:00Z, Lead 02:42Z): summarise the k86GLD1 phase-1 certificate (t1 = -2/11 on K3gB5n + 357 keys + p1r, eng_p8ld lextcertall)
# usage: python3 -I gld1_pack.py <cert_p1.json> <sol_p1.json> <keys file> <out SUMMARY.md>
import json, sys, collections, re
cert = json.load(open(sys.argv[1])); sol = json.load(open(sys.argv[2])); keys = {}
for l in open(sys.argv[3]):
    if l.strip() and not l.startswith('#'): n, sp = l.split(None, 1); keys[n] = sp.split('#')[0].strip()
o = open(sys.argv[4], 'w'); P = lambda *a: o.write(' '.join(str(x) for x in a) + '\n')
P('# k86GLD1 phase-1 certificate summary'); P(''); P('t1 = %.15f (sol_p1)' % sol['t']); P('')
by = collections.defaultdict(lambda: [0, 0.0]); 
for e in cert: k = e['row'][0]; by[k][0] += 1; by[k][1] += abs(e['w'])
P('## Rows with nonzero dual, by kind (count, sum |w|)'); P('')
for k, (n, s) in sorted(by.items(), key=lambda kv: -kv[1][1]): P('- %s: %d rows, sum |w| %.6g' % (k, n, s))
P(''); P('## Top 40 rows by |w|'); P(''); P('```')
for e in sorted(cert, key=lambda e: -abs(e['w']))[:40]: P('%+.6g  %s' % (e['w'], json.dumps(e['row'])))
P('```'); P('')
recv = collections.Counter(); sw = collections.defaultdict(float)
for e in cert:
    r = e['row']
    if r[0] in ('receiverR2', 'receiver'): recv[r[1]] += 1; sw[r[1]] += abs(e['w'])
P('## receiver rows by degree (count, sum |w|)'); P('')
for d in sorted(recv): P('- d=%s: %d, %.6g' % (d, recv[d], sw[d]))
P(''); P('## Generic keys at nonzero amount in the phase-1 point (ks)'); P('')
ks = sorted([e for e in sol.get('ks', []) if abs(e[1]) > 1e-9], key=lambda e: -e[1])
for n, v in ks: P('- %s = %.6g   %s' % (n, v, keys.get(n, '(not a generic key: %s)' % n)))
P(''); P('payer of each nonzero key: %s' % dict(collections.Counter((re.match(r'EDGE\((\d)', keys.get(n, '')) or [None, '?'])[1] for n, v in ks)))
g = sorted(sol.get('g', []), key=lambda e: -e[1])[:20]
P(''); P('## top 20 g columns (old cg grammar) in the phase-1 point'); P(''); P('```')
for e in g: P('%.6g  %s' % (e[1], e[0]))
P('```')
xs = sol.get('x', {}); P(''); P('x (xcap 3) at nonzero: %d; at cap (>= 2.999): %s' % (sum(1 for v in xs.values() if v > 1e-9), [k for k, v in xs.items() if v >= 2.999]))
o.close(); print('summary written', sys.argv[4])
