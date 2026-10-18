"""C_kc_ring17: per (s1,s4) filling coverage of R from results2/results3 (kc) and xD*_dfast.out (dfast second engine).
Writes ../fillings_opus.txt: 's1s4 status window ring' (9 = >= 9; D2 = kc and dfast D, D1 = kc only, open)."""
import re, glob
kc, ring = {}, {}
for fn in ('results2.txt', 'results3.txt'):
    try:
        for l in open(fn):
            f = l.split(); nm = f[1]; ring[nm] = int(f[2][2:])
            kc[nm] = 'D' if 'D=true' in l else ('notD' if 'D=false' in l else 'budget')
    except FileNotFoundError: pass
df = {}
for fn in glob.glob('*_dfast.out'):
    for l in open(fn):
        f = l.split()
        if f and 'D=' in l: df[f[0]] = 'D' if 'D=true' in l else 'notD'
out = []; ran = {}
for a in '6789':
    for b in '6789':
        app = [nm for nm in kc if nm[12 + 1] in ('.', a) and nm[12 + 4] in ('.', b) and nm[13] != '5' and nm[16] != '5']
        D = sorted([nm for nm in app if kc[nm] == 'D'], key=lambda n: (df.get(n) != 'D', ring[n]))
        ran[a + b] = len(app)
        if D: out.append('%s%s %s %s ring=%d' % (a, b, 'D2' if df.get(D[0]) == 'D' else 'D1', D[0], ring[D[0]]))
        else: out.append('%s%s open - (%d windows run not D, max ring %d)' % (a, b, len(app), max([ring[n] for n in app] or [0])))
hdr = '# C_kc_ring17 (opus), R = d7 link 5675765, s0=6 s2=7 s3=7 s5=7 s6=5; windows = connected subsets of R\'s fixed vertices (u, w, s; s1/s4 at the filling), not u+all-link; kc [E], dfast second engine at ring <= 16\n'
open('../fillings_opus.txt', 'w').write(hdr + '\n'.join(out) + '\n'); print(hdr + '\n'.join(out))
