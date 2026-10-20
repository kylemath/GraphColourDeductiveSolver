"""EXPLORE round 55 (Opus 06:30Z): the hit sites of row55's hits.  For each row with a hit, each configuration that sits
inside its 1.5-ball (exact vertices only, letter 9 never exact) with every embedding: configuration vertex -> row
vertex (degree), and whether the embedding uses u (Opus's engine and rpatD only match configurations through u).
usage: python3 sites55.py TD TC XKC ROW55OUT ROWS -> sites55_<rows>.txt"""
import sys, os, importlib, collections
TD, TC, XKC, R55, ROWS = sys.argv[1:6]
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(H, '..', 'k53'))
os.environ.update({'RING3': '0', 'J3S': '', 'FOCUS': ''})
rows = [l.split() for l in open(ROWS) if l.strip() and not l.startswith('#')]
sys.argv = ['cen54.py', rows[0][1], rows[0][2], rows[0][3]]
import cen54, grow
REG, miss = cen54.F.registry(TD, TC)
XR = [grow.kcline(l, 'xreg') for l in open(XKC) if l.strip()]
ALL = {c[0]: c for c in REG + XR}
hit = {}
for l in open(R55):
    if l.startswith('#'): continue
    f = l.split('|'); key = f[0].split()[2]
    nm = [x.split(':')[0] for x in f[2].split()[2:] if ':' in x]
    hit[key] = nm
def vn(v): return v[0] + ''.join(map(str, v[1:]))
out = []; tally = collections.Counter()
for w, d, lk, sv in rows:
    key = '%s/%s' % (lk, sv); sys.argv = ['cen54.py', d, lk, sv]; importlib.reload(cen54)
    P, pa, pf = cen54.structure(dict(cen54.EX), [], {})
    names = list(hit.get(key, []))
    if int(d) >= 12 or not names:     # registry hits are listed for rows the registry hits (row55 shows only the d12 row)
        names += [c[0] for c in REG if grow.embeddings(c, P, pa, pf, cen54.EX)]
    if not names: continue
    anyu = False; lines = []
    for nm in names:
        c = ALL[nm]; es = sorted(grow.embeddings(c, P, pa, pf, cen54.EX), key=repr)
        uu = [any(v == ('u',) for _, v in e) for e in es]; anyu |= any(uu)
        lines.append('  %s (%s, %d vertices, degrees %s): %d embeddings, %d through u' % (nm, 'registry' if c[1] != 'xreg' else '2026 set D',
                     len(c[2]), ''.join(str(c[3][u]) for u in c[2]), len(es), sum(uu)))
        for e, u_ in zip(es, uu):
            lines.append('    %s %s' % ('u ' if u_ else '- ', ' '.join('%d->%s(%d)' % (a, vn(v), c[3][a]) for a, v in sorted(e))))
    tally['rows'] += 1; tally['some hit through u' if anyu else 'only hits avoiding u'] += 1
    out.append('%s d%s %s: %s' % (w, d, key, 'a hit runs through u' if anyu else 'every hit avoids u'))
    out += lines
hdr = '# %s; rows from %s, hits from %s; embedding lines: u = uses u, - = avoids u' % (dict(tally), os.path.basename(ROWS), os.path.basename(R55))
open(os.path.join(H, 'sites55_%s' % os.path.basename(ROWS)), 'w').write(hdr + '\n' + '\n'.join(out) + '\n'); print(hdr)
