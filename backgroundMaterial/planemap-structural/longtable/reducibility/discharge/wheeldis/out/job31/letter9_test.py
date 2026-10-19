"""Letter-9 rule test (Long Table 19 Oct 08:45Z; rule in loop/studio/opus_check/letter9_rule.md).
Windows are cut exactly as explore's win45.py does (its build / extract, exec'd without its __main__): every lettered
window vertex is an interior vertex at its exact degree. For rows whose link or s word holds a 9, every window whose
interior contains a 9-lettered vertex is generated, and two frames are compared per window:
  name frame: slot -> letter, read from the a/f-name (Studio's explicit reader parse9 below: '9' = exact degree 9);
  kc frame:   slot -> degree, read from the kc line itself (interior degree = interior + ring adjacencies, as grow.kcline,
              the line dfast / cfast / kc all take).
It also records what Studio's LP name parser (wlp3.parse / fullparse) does with each name: it must refuse it, since its
letter 9 means degree >= 9 and the window proves the kill only at degree exactly 9.
Usage: python3 out/job31/letter9_test.py > loop/studio/opus_check/letter9_test.out"""
import os, sys, itertools, collections, hashlib
HERE = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
src = open(os.path.join(HERE, 'loop', 'k47', 'win45.py')).read()
pre = src[:src.index("D, LK, SV = int(sys.argv[2])")]; body = src[src.index('def build(r2):'):src.index("if __name__ == '__main__':")]
G = {'__file__': os.path.join(HERE, 'loop', 'k47', 'win45.py'), '__name__': 'win45_lib'}
exec(pre, G); exec(body, G)
G2 = {'__file__': os.path.join(HERE, 'loop', 'k42', 'grow.py'), '__name__': 'grow'}
exec(open(G2['__file__']).read(), G2)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from letter9 import parse9 as parse9_mod, lp_reading
W3 = open(os.path.join(HERE, 'wlp3.py')).read()
NS = {}; exec("import collections\nLI = {5: 0, 6: 1, 7: 2, 8: 3, 9: 4}\n" + W3[W3.index('SETS = {'):W3.index('def dropped(')], NS)

def parse9(name):
    """explicit reader: a/f-name -> {('u',): d or None, ('w', j): letter, ('s', j): letter}; '9' read as exact degree 9."""
    f = name.split('_'); d = int(f[0][1:]); lk, sv = f[1], f[2]; out = {}
    if lk[0] == 'u': out[('u',)] = d; lk = lk[1:]
    elif lk[0] == '-': lk = lk[1:]
    for j, ch in enumerate(lk):
        if ch in '56789': out[('w', j)] = int(ch)
    for j, ch in enumerate(sv):
        if ch in '56789': out[('s', j)] = int(ch)
    return out

ROWS = [(9, '655665556', '666559575'),       # explore's next row (Long Table 08:45Z)
        (7, '7665566', '6695666'), (7, '9665566', '6675666'), (8, '96565665', '66956665'), (7, '5965655', '6669665'),
        (9, '965565565', '665569566'), (9, '765556565', '566956665')]   # synthetic, and the r9f binder (9 in s)
RMAX = 12; lines = []; tot = collections.Counter()
for D, LK, SV in ROWS:
    G['D'], G['LK'], G['SV'] = D, LK, SV
    r2 = {('s', j): int(SV[j]) for j in range(D)}
    adj, name, faces = G['build'](r2); inv = {v: x for x, v in name.items()}
    V = [('u',)] + [('w', j) for j in range(D)] + [('s', j) for j in range(D)]
    deg = {('u',): D}; deg.update({('w', j): int(LK[j]) for j in range(D)}); deg.update({('s', j): int(SV[j]) for j in range(D)})
    nine = [x for x in V if deg[x] == 9]
    nb = {x: {name[y] for y in adj[inv[x]] if name.get(y) in deg} for x in V}
    seen = set(); nwin = 0
    def grow(S, ext):
        global nwin
        key = frozenset(S)
        if key in seen or len(seen) > 60000: return
        seen.add(key)
        if len(S) >= 2 and any(x in S for x in nine):
            r = G['ringsize']([inv[x] for x in S], adj)
            if r <= RMAX:
                c = G['extract'](adj, [inv[x] for x in S], {inv[x]: deg[x] for x in S})
                if c is not None:
                    nm = 'a%d_%s%s_%s' % (D, 'u' if ('u',) in S else '-', ''.join(LK[j] if ('w', j) in S else '.' for j in range(D)),
                                          ''.join(SV[j] if ('s', j) in S else '.' for j in range(D)))
                    kc = '%s %d %d %s %s' % ((nm,) + c)
                    cfg = G2['kcline'](kc, 'test')                     # (name, tag, U, g, E, tri)
                    Il = sorted(inv[x] for x in S); kdeg = {name[v]: cfg[3][k] for k, v in enumerate(Il)}
                    fnm = 'f%d_%s_%s' % (D, nm.split('_')[1][1:], nm.split('_')[2])   # registry f-name form: no u marker
                    nf = parse9(nm); assert nf == parse9_mod(nm)
                    lpr = lp_reading(fnm); tot['l9_' + lpr] += 1
                    same = nf == kdeg
                    try: NS['parse'](fnm); lp = 'parsed'
                    except Exception as e: lp = 'refused:%s' % type(e).__name__
                    try: NS['fullparse'](fnm); lpf = 'parsed'
                    except Exception as e: lpf = 'refused:%s' % type(e).__name__
                    nwin += 1; tot['windows'] += 1; tot['frame_equal' if same else 'frame_DIFFERENT'] += 1; tot['lp_' + lp.split(':')[0]] += 1; tot['lpfull_' + lpf.split(':')[0]] += 1
                    nine_in = [x for x in S if deg[x] == 9]
                    lines.append('%s ring=%d interior=%d nine_at=%s kc_degree_of_nine=%s frames_equal=%s lp_parse=%s lp_fullparse=%s letter9=%s' % (
                        nm, c[0], c[1], ','.join(''.join(map(str, x)) for x in nine_in), ','.join(str(kdeg[x]) for x in nine_in), same, lp, lpf, lpr))
        if len(S) >= 7: return
        for y in sorted(ext, key=str):
            grow(S | {y}, (ext | nb[y]) - S - {y})
    for x in nine:
        grow({x}, set(nb[x]))
    tot['rows'] += 1
    lines.append('# row d=%d %s/%s: %d windows with an interior 9 (ring <= %d, interior <= 7)' % (D, LK, SV, nwin, RMAX))
out = '\n'.join(sorted(l for l in lines if not l.startswith('#')) + [l for l in lines if l.startswith('#')]) + '\n'
out += '# TOTAL %s\n' % dict(sorted(tot.items()))
sys.stdout.write(out)
sys.stderr.write('md5 of this output: %s\n' % hashlib.md5(out.encode()).hexdigest())
