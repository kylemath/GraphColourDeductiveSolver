"""Job 30: sep3xf's whole-arrangement matcher against an independent Python matcher, for every pattern that loads
through the NF section. For each pattern: N random frames per dihedral image, built so that half match it and half
differ in one constrained slot. A frame is 'newly forbidden' if sep `c` rejects it with the pattern and accepts it
without. That must equal the Python verdict on every frame the base registry allows.
Usage: python3 out/job30/matchtest.py NAME ... [n=6]"""
import sys, os, random, subprocess
HERE = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
S = os.environ.get('TMPDIR', '/tmp'); random.seed(11)
args = [a for a in sys.argv[1:] if not a.startswith('n=')]; N = int(next((a[2:] for a in sys.argv[1:] if a.startswith('n=')), '6'))
SETS = {'5': {5}, '6': {6}, '7': {7}, '8': {8}, 'B': {7, 8, 9}}
base = open(os.path.join(HERE, 'bin', 'sep3_j29_dump.in')).read().rstrip('\n')
def slots(nm):
    f = nm.split('_'); d = int(f[0][1:]); out = {}
    for word, off in ((f[1], 0), (f[2], d)):
        for i, ch in enumerate(word):
            if ch != '.': out[off + i] = SETS[ch]
    return d, out
def image(d, sl, refl, r):
    out = {}
    for k, v in sl.items():
        isS = k >= d; i = k - d if isS else k
        j = ((2 * d - i - 1) % d if isS else (d - i) % d) if refl else i
        out[(d + (j + r) % d) if isS else ((j + r) % d)] = v
    return out
def pymatch(d, sl, w, s):
    for refl in (0, 1):
        for r in range(d):
            im = image(d, sl, refl, r)
            if all((w[k] if k < d else s[k - d]) in v for k, v in im.items()): return True
    return False
tot = bad = 0
for nm in args:
    d, sl = slots(nm); mask = lambda v: sum(1 << (x - 5) for x in v)
    open(S + '/mt1.in', 'w').write(base + '\n1\n%d %d %s\n' % (d, len(sl), ' '.join('%d %d' % (k, mask(v)) for k, v in sorted(sl.items()))))
    open(S + '/mt0.in', 'w').write(base + '\n0\n')
    frames = []
    for refl in (0, 1):
        for r in range(d):
            im = image(d, sl, refl, r)
            for k in range(N):
                w = [random.choice((5, 6, 7, 8, 9)) for _ in range(d)]; s = [random.choice((5, 6, 7, 8, 9)) for _ in range(d)]
                for q, v in im.items():
                    x = random.choice(sorted(v))
                    if q < d: w[q] = x
                    else: s[q - d] = x
                if k % 2:   # break one constrained slot
                    q = random.choice(sorted(im)); alt = [x for x in (5, 6, 7, 8, 9) if x not in im[q]]
                    if alt:
                        if q < d: w[q] = random.choice(alt)
                        else: s[q - d] = random.choice(alt)
                frames.append((w, s))
    Q = ''.join('c %d %s %s\n' % (d, ''.join(map(str, w)), ''.join(map(str, s))) for w, s in frames)
    run = lambda f: [l == '1' for l in subprocess.run([os.path.join(HERE, 'bin', 'sep3xf'), f], input=Q, capture_output=True, text=True).stdout.split()]
    a0, a1 = run(S + '/mt0.in'), run(S + '/mt1.in')
    n = m = 0
    for i, (w, s) in enumerate(frames):
        if not a0[i]: continue
        n += 1; m += ((not a1[i]) != pymatch(d, sl, w, s))
    nf = sum(1 for i in range(len(frames)) if a0[i] and not a1[i])
    print('%-22s frames %d, allowed by the base %d, newly forbidden %d, mismatches %d' % (nm, len(frames), n, nf, m))
    tot += n; bad += m
print('TOTAL frames checked %d, mismatches %d' % (tot, bad))
