#!/usr/bin/env python3
"""ST-120 B5 M1 cross-check: kill yes/no per (state, configuration) at d = 5..8, Lean `containsK` (RSSTKillX.lean)
against RSST-1SHOT's `requirements` / `contained` (rcore.py, spec §7; u is a host at d <= 8 there, as in the errata).
  gen  N seed  -> cases_kill.txt (id;d;link;apex;privs, B2's case format) + expected_kill.txt (id: contained config indices)
  cmp          -> compares lean_kill.txt with expected_kill.txt
usage: python3 -I xcheck_kill.py gen 120 20261110 | cmp"""
import os, sys, random
H = os.path.dirname(os.path.abspath(__file__)); B5 = os.path.normpath(os.path.join(H, '..'))
OUT = os.path.normpath(os.path.join(B5, '..', '..'))
sys.path.insert(0, os.path.join(OUT, 'job_RSST1SHOT', 'code'))

def gen(N, seed, ctrl=''):
    import rcore as R
    if ctrl == 'nouhost':                       # planted control: u not a host (pre-errata reading)
        wh = R.window_hostgraph
        def wh2(W, d9_u_host=None):
            host, adj, var = wh(W); host.pop('u', None); adj.pop('u', None)
            for v in adj: adj[v].discard('u')
            return host, adj, var
        R.window_hostgraph = wh2
    rnd = random.Random(seed)
    P = [5, 5, 5, 5, 6, 6, 7, 8, 9] if seed % 2 == 0 else [5, 5, 5, 5, 5, 6, 6, 6, 7, 8, 9]
    cases, exp = [], []
    # fixed: the spec §10.1 d7/8 argmax fillings with listed containments
    fixed = [(7, '7676766', '6565665', ['55', '9', '55', '9', '55', '5', '5']),
             (7, '7676766', '6565665', ['55', '9', '55', '9', '65', '6', '7']),
             (8, '56765767', '56655555', ['', '9', '55', '9', '', '65', '6', '56']),
             (7, '5566776', '5666657', ['', '', '7', '6', '69', '56', '9'])]
    rows = []
    for d, l, a, pv in fixed: rows.append((d, [int(c) for c in l], [int(c) for c in a], [[int(c) for c in s] for s in pv]))
    for t in range(N):
        d = 5 + t % 4
        link = [rnd.choice(P) for _ in range(d)]; apex = [rnd.choice(P) for _ in range(d)]
        priv = [[(9 if (link[i] >= 9 and j == 1) else rnd.choice(P)) for j in range(R.npriv(link[i]))] for i in range(d)]
        rows.append((d, link, apex, priv))
    for n, (d, link, apex, priv) in enumerate(rows):
        W = R.Window(d, link, apex)
        f = {}
        for i in range(d):
            for j, x in enumerate(priv[i]): f['p%d.%d' % (i, j + 1)] = x
        c = sorted(R.contained(R.requirements(W), f))
        cid = 'k%d' % n
        cases.append('%s;%d;%s;%s;%s' % (cid, d, ''.join(map(str, link)), ''.join(map(str, apex)), ','.join(''.join(map(str, p)) for p in priv)))
        exp.append('%s %s' % (cid, ' '.join(map(str, c))))
    if ctrl: open(os.path.join(B5, 'expected_kill_%s.txt' % ctrl), 'w').write('\n'.join(exp) + '\n'); return
    open(os.path.join(B5, 'cases_kill.txt'), 'w').write('\n'.join(cases) + '\n')
    open(os.path.join(B5, 'expected_kill.txt'), 'w').write('\n'.join(exp) + '\n')
    print('cases', len(rows), 'pairs', 633 * len(rows), 'yes', sum(len(e.split()) - 1 for e in exp))

def cmp(fn='expected_kill.txt'):
    E = {l.split()[0]: set(map(int, l.split()[1:])) for l in open(os.path.join(B5, fn)) if l.strip()}
    L = {}
    bad_wit = 0
    for l in open(os.path.join(B5, 'lean_kill.txt')):
        f = l.split()
        if not f: continue
        L[f[0]] = set(int(x) for x in f[1:] if not x.startswith('!'))
        bad_wit += sum(1 for x in f[1:] if x.startswith('!'))
    pairs = yes = mis = 0; ex = []
    for k, e in E.items():
        g = L.get(k)
        if g is None: print('missing', k); mis += 633; continue
        pairs += 633; yes += len(e)
        d = (e ^ g)
        mis += len(d)
        if d: ex.append((k, sorted(e - g)[:5], sorted(g - e)[:5]))
    print('cases %d pairs %d yes(rcore) %d mismatches %d witnesses-failing-checkEmb %d' % (len(E), pairs, yes, mis, bad_wit))
    for x in ex[:10]: print('  mismatch', x)

if sys.argv[1] == 'gen': gen(int(sys.argv[2]), int(sys.argv[3]), sys.argv[4] if len(sys.argv) > 4 else '')
else: cmp(sys.argv[2] if len(sys.argv) > 2 else 'expected_kill.txt')
