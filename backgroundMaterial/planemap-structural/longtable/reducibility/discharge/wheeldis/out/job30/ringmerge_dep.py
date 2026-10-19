"""Ring-merge hold (Long Table 19:27Z, CGLUE-SCOPE a7557788): does any LP pattern depend only on the 3 held C entries?
For each held entry H (d = 7): every receiver arrangement (w_0..w_6, s_0..s_6 in letters 5..9) that H matches in its
own frame is tested against every other entry the Studio loader (wlp3.py, exec'd up to the sep tables, read-only)
loads from ARGSFILE, under all 14 dihedral images (matchtest.py's independent matcher semantics, fullparse slots).
An arrangement matched by H and by no other entry depends only on H.
Usage: WLP_SEPF=1 python3 out/job30/ringmerge_dep.py ARGSFILE"""
import sys, os, itertools, numpy as np
HERE = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
HELD = ['f7_..56757_...5...', 'f7_..65757_..55...', 'f7_..65757_..65...']
args = open(sys.argv[1]).read().split()
src = open(os.path.join(HERE, 'wlp3.py')).read().replace('os.path.abspath(__file__)', repr(os.path.join(HERE, 'wlp3.py')), 1)
sys.argv = ['wlp3'] + args; os.chdir(HERE)
G = {'__name__': 'wlp3_loader'}; exec(src[:src.index('# static tables for sep')], G)
names = sorted(G['SEEN']); print('loader names %d; held present: %s' % (len(names), [h in G['SEEN'] for h in HELD]))
SETS = {'5': {5}, '6': {6}, '7': {7}, '8': {8}, 'B': {7, 8, 9}}
def slots(nm):
    f = nm.split('_'); d = int(f[0][1:]); out = {}
    for word, off in ((f[1], 0), (f[2], d)):
        for i, ch in enumerate(word):
            if ch == '.' or (f[0][0] == 'p' and ((off == 0 and ch == '9') or (off and ch == '0'))): continue
            out[off + i] = SETS[ch]
    return d, out
def image(d, sl, refl, r):
    out = {}
    for k, v in sl.items():
        isS = k >= d; i = k - d if isS else k
        j = ((2 * d - i - 1) % d if isS else (d - i) % d) if refl else i
        out[(d + (j + r) % d) if isS else ((j + r) % d)] = v
    return out
D = 7; others = [n for n in names if n not in HELD and slots(n)[0] == D]
imgs = []; _seen = set()
for n in others:
    _, sl = slots(n)
    for refl in (0, 1):
        for r in range(D):
            im = tuple(sorted((k, sum(1 << (x - 5) for x in v)) for k, v in image(D, sl, refl, r).items()))
            if im not in _seen: _seen.add(im); imgs.append((n, im))
print('other d=7 entries %d (%d distinct images)' % (len(others), len(imgs)))
for h in HELD:
    _, sl = slots(h); free = [k for k in range(2 * D) if k not in sl]
    fixed = {k: sorted(v) for k, v in sl.items()}
    choices = [fixed[k] if k in fixed else [5, 6, 7, 8, 9] for k in range(2 * D)]
    A = np.array(list(itertools.product(*choices)), dtype=np.int8); Bt = (1 << (A - 5)).astype(np.uint8)
    unc = np.ones(len(A), bool); who = {}; idx = np.arange(len(A)); Bi = Bt
    for t, (n, im) in enumerate(imgs):
        if not len(idx): break
        ok = np.ones(len(idx), bool)
        for k, m in im: ok &= (Bi[:, k] & m) != 0
        if ok.any():
            unc[idx[ok]] = False; who[n] = who.get(n, 0) + int(ok.sum()); idx = idx[~ok]; Bi = Bi[~ok]
    print('%s: %d arrangements matched; covered by other entries %d; matched by %s alone: %d%s' % (
        h, len(A), int((~unc).sum()), h, int(unc.sum()),
        ('' if not unc.any() else '; e.g. ' + ' '.join(''.join(map(str, a[:D])) + '/' + ''.join(map(str, a[D:])) for a in A[unc][:3]))))
