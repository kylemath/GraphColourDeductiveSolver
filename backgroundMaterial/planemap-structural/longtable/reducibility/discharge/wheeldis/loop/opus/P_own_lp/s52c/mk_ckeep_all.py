"""s52c (= s46c/mk_ckeep_all.py): every name the engine could keep under ckeep= for A83 (all pat=/cpat= header names of args_A83, C 7-wheels c7_<canon> of
ROOT/out/def_*.cfast, studio17 wheel names). For the ckeep control (all kept + full reg_A83 tables must reproduce upper_base.log).
usage: python3 mk_ckeep_all.py ARGS ROOT DIS OUT"""
import sys, os, glob, re
ARGS, ROOT, DIS, OUT = sys.argv[1:5]
def canon(w):
    w = tuple(w); n = len(w)
    return min(min(s[k:] + s[:k] for k in range(n)) for s in (w, w[::-1]))
N = set()
for a in open(ARGS).read().split():
    if not a.startswith(('pat=', 'cpat=')): continue
    fn = a.split('=', 1)[1]; fn = fn[:-4] if fn.endswith(':all') else fn
    p = fn if os.path.isabs(fn) else os.path.join(ROOT, fn)
    if not os.path.exists(p): continue
    for line in open(p):
        if ' r=' in line and not line.startswith(' '): N.add(line.split()[0])
for fn in glob.glob(os.path.join(ROOT, 'out', 'def_*.cfast')):
    for line in open(fn):
        m = re.match(r'^(?:c7_|\S*_w7_\d+_)(\d{7}) ', line)
        if m: N.add('c7_' + ''.join(map(str, canon(map(int, m.group(1))))))
for line in open(os.path.join(DIS, 'studio17', 'wheels17_verdicts.txt')):
    if line.strip() and not line.startswith('#'): N.add(line.split()[0])
open(OUT, 'w').write(''.join(n + '\n' for n in sorted(N)))
print(len(N), 'names')
