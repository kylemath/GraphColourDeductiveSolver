"""EXPLORE round 19: canonical-key registry of every existing D/C verdict that has a dfast line.
Verdicts: D from any *.out (dfast), C from any *.cfast (C-REDUCIBLE).  Lines: any 'name r m ra ia' line in *.txt, *.d,
*.c, *.txt.gz under wheeldis.  Keyed by lemmaA la.ckey; cached in bridge.pkl.  Usage: python3 bridge.py"""
import sys, os, re, glob, gzip, pickle, collections
W = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(W, 'loop', 'lemmaA')); _a = sys.argv; sys.argv = ['x']; import la; sys.argv = _a
def load():
    DV, CV = set(), set()
    for fn in glob.glob(os.path.join(W, '**', '*.out'), recursive=True):
        for line in open(fn, errors='replace'):
            if 'D=true' in line: DV.add(line.split()[0])
    for fn in glob.glob(os.path.join(W, '**', '*.cfast'), recursive=True):
        cur = None
        for line in open(fn, errors='replace'):
            if ' r=' in line and not line.startswith(' '): cur = line.split()[0]
            elif 'C-REDUCIBLE' in line and cur: CV.add(cur)
    BR = {}; src = collections.Counter()
    files = [f for e in ('txt', 'd', 'c') for f in glob.glob(os.path.join(W, '**', '*.' + e), recursive=True)]
    files += glob.glob(os.path.join(W, '**', '*.txt.gz'), recursive=True)
    for fn in files:
        op = gzip.open if fn.endswith('.gz') else open
        try:
            for line in op(fn, 'rt', errors='replace'):
                f = line.split()
                if len(f) != 5 or not f[1].isdigit() or not f[2].isdigit(): continue
                if f[0] in DV or f[0] in CV:
                    k = la.ckey(' '.join(f[1:]))
                    if k not in BR: BR[k] = ('D' if f[0] in DV else 'C', f[0]); src[os.path.basename(fn)] += 1
        except Exception as e:
            print('skip', fn, e, file=sys.stderr)
    return BR, src
if __name__ == '__main__':
    BR, src = load()
    pickle.dump(BR, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'bridge.pkl'), 'wb'))
    print(len(BR), 'keys;', collections.Counter(v[0] for v in BR.values()), 'top sources', src.most_common(8))
