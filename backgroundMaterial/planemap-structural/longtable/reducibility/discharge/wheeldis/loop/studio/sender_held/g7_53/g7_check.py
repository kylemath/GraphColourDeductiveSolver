"""Studio check of explore's round-53 held g7_ set (c9cb6184), from the file's spec header and the data files only
(deliv53.py / cen53's builder not read). Per window:
  engines: kc -C -s 60 -t 600; kc D -> out/job52/dfast18 must give D; kc C-REDUCIBLE X -> studio15 cfast --fixed X
           must give leftover 0. Explore's verdict column is compared with Studio's.
  frame:   (a) the frame lists m vertices and each degree equals the kc line's interior degree (grow.kcline);
           (b) frame letters equal the name's letters: v iff 'u' (degree 7), wI / sI at the name's specified link / s
               positions, slots in the header's slot order;
           (c) adjacencies the spec forces, wherever both ends are in the window: v-wI, wI-w(I+1), sI-wI, sI-w(I+1),
               pIK-wI, ring-2 order s(I-1)-pI1-..-pIk-sI, t(a/b/..)-a, b, ..
  ring-merge: the union-find guard of out/job30/twoeng.py on each C's X.
Usage: python3 loop/studio/sender_held/g7_53/g7_check.py   (writes studio_*.out next to it, prints one line per window)"""
import os, re, subprocess, collections
HERE = os.path.dirname(os.path.abspath(__file__)); WD = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
KC = os.path.join(WD, 'loop', 'kc', 'kc'); DF = os.path.join(WD, 'out', 'job52', 'dfast18'); CF = os.path.join(WD, '..', 'studio15', 'cfast')
G = {'__file__': os.path.join(WD, 'loop', 'k42', 'grow.py'), '__name__': 'grow'}; exec(open(G['__file__']).read(), G)
SLOTS = ['p01', 'p02', 'p11', 'p21', 'p51', 'p61', 'tp21/s2', 'ts2/s3/s4', 'ts4', 'tp51/s4']
D = 7
def ringmerge(x):
    par = {}
    def fd(a):
        while par.setdefault(a, a) != a: a = par[a]
        return a
    for e in x:
        a, b = e.split('-'); par[fd(a)] = fd(b)
    c = collections.Counter(fd(v) for v in par if v.startswith('R'))
    return max(c.values(), default=0) >= 2
rows = [l.rstrip('\n') for l in open(os.path.join(HERE, 'held53_7_7665566_6765766.txt')) if l.strip() and not l.startswith('#')]
fk, fd_, fc = (open(os.path.join(HERE, 'studio_%s' % s), 'w') for s in ('kc.out', 'df.out', 'cf.cfast'))
nbad = 0
for r in rows:
    kcl, fr, ver = [x.strip() for x in r.split('|')[:3]]
    nm = kcl.split()[0]; ring, m = int(kcl.split()[1]), int(kcl.split()[2])
    wf = os.path.join(HERE, 'w.in'); open(wf, 'w').write(kcl + '\n')
    ko = subprocess.run(['nice', '-n', '19', KC, '-C', '-s', '60', '-t', '600', wf], capture_output=True, text=True).stdout; fk.write(ko)
    kD = 'D=true' in ko and 'mode=' in ko; mx = re.search(r'C-REDUCIBLE X=\{([^}]*)\}', ko)
    if kD:
        do = subprocess.run(['nice', '-n', '19', DF, wf], capture_output=True, text=True).stdout; fd_.write(do)
        sv = 'D (kc D + dfast18 %s)' % ('D' if 'D=true' in do else 'notD'); ok = 'D=true' in do; X = None
    elif mx:
        co = subprocess.run(['nice', '-n', '19', CF, wf, '--fixed', mx.group(1)], capture_output=True, text=True).stdout; fc.write(co)
        ok = re.search(r'C-REDUCIBLE, leftover bad classes extending after contraction = 0', co) is not None
        X = {e.strip() for e in mx.group(1).split(',')}; sv = 'C X={%s} (kc X + cfast --fixed %s)' % (mx.group(1), 'leftover 0' if ok else 'FAIL')
    else: ok = False; X = None; sv = 'NEITHER on kc'
    os.remove(wf)
    # frame checks
    c = G['kcline'](kcl, 'g7'); g, E = c[3], c[4]
    fl = [x.split('=') for x in fr.replace('frame', '').strip().split(',')]
    lab = [a for a, _ in fl]; deg = [int(b) for _, b in fl]; pos = {a: i for i, a in enumerate(lab)}
    errs = []
    if len(lab) != m: errs.append('frame has %d vertices, kc m=%d' % (len(lab), m))
    for i, (a, dg) in enumerate(zip(lab, deg)):
        if i < m and g[i] != dg: errs.append('%s degree %d vs kc %d' % (a, dg, g[i]))
    f = nm.split('_'); lk, sw, sl = f[1], f[2], f[3]
    want = {}
    if lk[0] == 'u': want['v'] = D
    for i, ch in enumerate(lk[1:]):
        if ch in '56789': want['w%d' % i] = int(ch)
    for i, ch in enumerate(sw):
        if ch in '56789': want['s%d' % i] = int(ch)
    if len(sl) != len(SLOTS): errs.append('slot string %d chars, header has %d slots' % (len(sl), len(SLOTS)))
    for k, ch in enumerate(sl):
        if ch in '56789': want[SLOTS[k]] = int(ch)
    if want != dict(zip(lab, deg)): errs.append('name letters %s != frame %s' % (sorted(want.items()), sorted(zip(lab, deg))))
    def adj(a, b): return a in pos and b in pos and pos[b] in E[pos[a]]
    need = []
    for I in range(D):
        wI, wJ = 'w%d' % I, 'w%d' % ((I + 1) % D)
        need += [('v', wI), (wI, wJ), ('s%d' % I, wI), ('s%d' % I, wJ)]
        ps = sorted(x for x in lab if re.fullmatch(r'p%d\d' % I, x))
        need += [(p, wI) for p in ps]
        chain = ['s%d' % ((I - 1) % D)] + ['p%d%d' % (I, k) for k in range(1, 3)] + ['s%d' % I]
        chain = [x for x in chain if x in pos or x.startswith('s')]
        need += list(zip(chain, chain[1:]))
    for t in lab:
        if t.startswith('t'): need += [(t, x) for x in t[1:].split('/')]
    miss = [(a, b) for a, b in need if a in pos and b in pos and not adj(a, b)]
    if miss: errs.append('spec adjacencies missing: %s' % miss)
    rm = ('ring-merge HOLD' if ringmerge(X) else 'ring-merge pass') if X else 'ring-merge n/a'
    agree = ('D' if kD else 'C' if mx else '-') == ver[0] and (X is None or ('X={%s}' % ','.join(sorted(X))) .replace(' ', '') in ver.replace(' ', '') or mx.group(1).replace(' ', '') in ver.replace(' ', ''))
    nbad += (not ok) + bool(errs) + (not agree)
    print('%s ring=%d m=%d | Studio %s | frame %s | %s | explore: %s | %s' % (nm, ring, m, sv, 'OK' if not errs else 'FAIL: ' + '; '.join(errs), rm, ver, 'agree' if agree else 'DISAGREE'))
print('# windows %d; problems %d' % (len(rows), nbad))
