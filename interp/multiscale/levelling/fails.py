# analyse clusters U on which re-levelling to tau<=1 failed in E4 (skipped merges): chords, depth, exact min tau
import pickle, glob, json, math
from lev import *
from e1_survey import graph
from e2_strips import ascend
out = open('fails.jsonl', 'w')
for f in sorted(glob.glob('fail_*.pkl')):
    d = pickle.load(open(f, 'rb')); T = graph(d['name']); U = disc_or_none(T, d['A'] | d['B'])
    K, unk = ascend(U); info = U.info()
    # does the cluster become levelable if we cut it at its chords?  -> min tau of each chordless piece is reported elsewhere
    rec = dict(file=f, n=info['n'], m=info['m'], nodd=info['nodd'], depth=info['maxdepth'], chords=len(chords(U)), min_tau=K, unk=unk)
    out.write(json.dumps(rec)+'\n'); out.flush(); print(rec, flush=True)
