"""EXPLORE round 53: Studio delivery of the split-census kills of one row as a held set (Studio, 20:34Z): g<D>_ names kept,
kc line, slot spec, frame map per interior vertex (kc-line vertex order), the X of each C, and the ring-merge guard (a C
whose X joins two ring vertices, by union-find over X's edges, is held out).  Every kill in G_res.txt whose name is this
row's is rebuilt from its name exactly as cen53 builds it, and the rebuilt kc line is checked against the cached one.
usage: python3 deliv53.py D LK SV   -> held53_<D>_<LK>_<SV>.txt"""
import sys, os, re
H = os.path.dirname(os.path.abspath(__file__))
sys.argv = [sys.argv[0]] + sys.argv[1:4] + ['16', '2', '600', '0']
exec(open(os.path.join(H, 'cen53.py')).read().replace("if __name__ == '__main__':\n    main()", ''))
pre = 'g%d_' % D
def parse(nm):
    _, l, s, p = nm.split('_')
    S = set([('u',)] if l[0] == 'u' else [])
    S |= {('w', j) for j, c in enumerate(l[1:]) if c.isdigit()}
    S |= {('s', j) for j, c in enumerate(s) if c.isdigit()}
    lets = {x: int(c) for x, c in zip(SLOTS, p) if c.isdigit()}
    assert all(int(c) == LK[j] for j, c in enumerate(l[1:]) if c.isdigit()) and all(int(c) == SV[j] for j, c in enumerate(s) if c.isdigit())
    return frozenset(S | set(lets)), lets
def guard(X):
    par = {}
    def f(a):
        while par.setdefault(a, a) != a: a = par[a]
        return a
    for e in X.split(','):
        a, b = e.split('-'); par[f(a)] = f(b)
    rs = [v for v in par if v.startswith('R')]
    return len(rs) == len({f(v) for v in rs})
want = [l.rstrip('\n').split(' ', 2) for l in open(os.path.join(H, 'G_res.txt'))]
want = [w for w in want if w[0].startswith(pre) and F.kills(w[1]) and w[0].split('_', 1)[1].count('_') == 2]
out = []; spec = ' '.join(sname(x) for x in SLOTS)
for nm, v, line in want:
    S, lets = parse(nm)
    adj, name, _ = build(lets); inv = {y: x for x, y in name.items()}
    deg = {('u',): D}; deg.update({('w', j): LK[j] for j in range(D)}); deg.update({('s', j): SV[j] for j in range(D)}); deg.update(lets)
    I = [inv[x] for x in S]; c = F.extract(adj, I, {inv[x]: deg[x] for x in S})
    assert gname(S, deg) == nm and '%d %d %s %s' % c == line, nm
    fm = [name[y] for y in sorted(I)]
    fr = ','.join(('v' if x == ('u',) else '%s%d' % x if x[0] in 'ws' else sname(x)) + '=%d' % deg[x] for x in fm)
    if v == 'D': ver, g = 'D (kc + dfast)', 'n/a'
    else: X = v[2:-1]; ver, g = 'C X={%s} (kc -C + cfast --fixed)' % X, 'pass' if guard(X) else 'HOLD'
    out.append('%s %s | frame %s | %s | ring-merge guard %s' % (nm, line, fr, ver, g))
hdr = ['# round 53 split-census kills of row %d %s/%s (explore, cen53.py; held set for Studio, not for k3x)' % (D, sys.argv[2], sys.argv[3]),
       '# name g%d_<u|-><w letters, F/N as win45>_<s letters>_<one char per slot, letter or .>; slot order: %s' % (D, spec),
       '# slots: pIK = K-th private of w_I (ring 2, between s_(I-1) and s_I); t(a/b/..) = ring-3 vertex whose ring-2 neighbours are a, b, ..',
       '# frame: each interior vertex in kc-line vertex order, as v (centre), wI, sI or a slot, with its degree']
open(os.path.join(H, 'held53_%d_%s_%s.txt' % (D, sys.argv[2], sys.argv[3])), 'w').write('\n'.join(hdr + out) + '\n')
print(len(out), 'kills;', sum('HOLD' in o for o in out), 'held by the guard')
