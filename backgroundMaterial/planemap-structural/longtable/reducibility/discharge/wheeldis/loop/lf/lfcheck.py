"""EXPLORE round 18 (H-LF): defect_check2 (bf) on defect leaves, reusing every existing verdict.  defect_check2 knows
hash-named (g/b) and e/p verdicts; this adds a bridge for named configurations (f<d>_ from Job 28 and the explore
windows, z_ etc.): their dfast lines (any *.txt under out/ and loop/) are keyed by lemmaA la.ckey, and a configuration
built in the patch with no verdict of its own takes the bridged D / C verdict.  No new dfast or cfast runs.
Usage: python3 lfcheck.py LEAVES OUT  |  python3 lfcheck.py rows PREFIX NROWS MAXPER (per-row early-stop check)"""
import sys, os, re, glob, collections
W = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LEAVES, OUT = sys.argv[1], sys.argv[2]
sys.path.insert(0, os.path.join(W, 'loop', 'lemmaA')); _a = sys.argv; sys.argv = ['x']; import la; sys.argv = _a
DV, CV = {}, set()
for fn in glob.glob(os.path.join(W, 'out', '**', '*.out'), recursive=True) + glob.glob(os.path.join(W, 'loop', '**', '*.out'), recursive=True):
    for line in open(fn):
        f = line.split()
        if f and ('D=true' in line or 'D=false' in line) and DV.get(f[0]) != 'D': DV[f[0]] = 'D' if 'D=true' in line else 'notD'
for fn in glob.glob(os.path.join(W, '**', '*.cfast'), recursive=True):
    cur = None
    for line in open(fn):
        if ' r=' in line and not line.startswith(' '): cur = line.split()[0]
        elif 'C-REDUCIBLE' in line and cur: CV.add(cur)
BR = {}
for fn in glob.glob(os.path.join(W, 'out', '**', '*.txt'), recursive=True) + glob.glob(os.path.join(W, 'loop', '**', '*.txt'), recursive=True):
    try:
        for line in open(fn):
            f = line.split()
            if len(f) == 5 and f[1].isdigit() and f[2].isdigit() and (DV.get(f[0]) == 'D' or f[0] in CV):
                BR.setdefault(la.ckey(' '.join(f[1:])), 'D' if DV.get(f[0]) == 'D' else 'C')
    except (UnicodeDecodeError, ValueError, IndexError):
        pass
print('bridge: %d named D/C configurations keyed' % len(BR), file=sys.stderr)
src = open(os.path.join(W, 'defect_check2.py')).read(); src = src[:src.index("if __name__ == '__main__':")]
reps = [("db = DRES.get(kb); cbv = CRES.get(kb)", "db = DRES.get(kb) or BRV(cb, 'D'); cbv = CRES.get(kb) or BRV(cb, 'C')"),
        ("dv = TESTED.get(key) if not isinstance(key, str) else DRES.get(key)",
         "dv = (TESTED.get(key) if not isinstance(key, str) else DRES.get(key)) or BRV(cfg, 'D')"),
        ("cv = CRES.get(key)", "cv = CRES.get(key) or BRV(cfg, 'C')")]
for a, b in reps:
    assert src.count(a) == 1, a
    src = src.replace(a, b)
NB = collections.Counter()
def BRV(cfg, kind):
    v = BR.get(la.ckey(cfg))
    if v == kind or (kind == 'D' and v == 'C' and False): NB[kind] += 1; return v
    return None
_argv = sys.argv; sys.argv = ['defect_check2.py', '/dev/null', '/dev/null', 'bf']
G = {'__file__': os.path.join(W, 'defect_check2.py'), '__name__': 'dc2', 'BRV': BRV}
exec(src, G); check = G['check']; sys.argv = _argv
def rows(prefix, n, maxper):
    """per row: leaves found, leaves checked (evenly spaced sample of at most maxper, stopping at the first survivor)"""
    res = []
    for i in range(1, n + 1):
        fn = '%s_%d.out' % (prefix, i)
        L = [re.search(r'c=(-?\d+) sig=(\S+)', l) for l in open(fn)] if os.path.exists(fn) else []
        L = [m.group(2) for m in L if m]
        idx = list(range(len(L))) if len(L) <= maxper else sorted({int(j * len(L) / maxper) for j in range(maxper)})
        surv = None; nchk = 0; st_ = collections.Counter()
        for j in idx:
            v, st, need = check(L[j]); nchk += 1; st_[v] += 1
            if v != 'killed': surv = (L[j], v, dict(st)); break
        res.append((i, len(L), nchk, dict(st_), surv))
        print(i, len(L), nchk, dict(st_), surv[1] if surv else '-', surv[0] if surv else '', flush=True)
    return res
if LEAVES == 'rows':
    rows(OUT, int(sys.argv[3]), int(sys.argv[4]))
    print('bridged kills', dict(NB))
else:
    out = []; summ = collections.Counter()
    for line in open(LEAVES):
        m = re.search(r'c=(-?\d+) sig=(\S+)', line)
        if not m: continue
        v, st, need = check(m.group(2)); summ[v] += 1
        out.append('%s c=%s sig=%s %s' % (v, m.group(1), m.group(2), dict(st)))
    open(OUT, 'w').write(''.join(o + '\n' for o in out))
    print(dict(summ), 'bridged kills', dict(NB))
