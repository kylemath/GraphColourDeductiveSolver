"""Build the run data set + per-state feature table (INVARIANTS-1).
Usage: build_data.py out_prefix  (reads data/win_*.jsonl, data/planar_*.jsonl, TrackU t1_n22_walk.txt)
Writes <out_prefix>_runs.json.gz (graph line, matchings, frames, run meta) and <out_prefix>_feat.jsonl.gz."""
import sys, os, glob, json, gzip
from feat import *

pref = sys.argv[1]
maxt1 = int(sys.argv[2]) if len(sys.argv) > 2 else 10 ** 9
runs = []
for p in sorted(glob.glob('data/win_*_axv1.jsonl')): runs += load_windows(p, True)
for p in sorted(glob.glob('data/win_*_axv0.jsonl')) + sorted(glob.glob('data/win_*_axv2.jsonl')): runs += load_windows(p, False)
# windows found by the free/anti search are also re-read as A5v runs? no: keep them as 'free' maximal runs.
for p in ['data/planar_p33_r147.jsonl', 'data/planar_p34_r178.jsonl', 'data/planar_nr6_runs.jsonl']:
    if os.path.exists(p): runs += load_planar(p)
runs += load_t1(os.path.expanduser('~/GraphColour/SolvingFrameworkPlan/docs/working/TrackU/out/t1_n22_walk.txt'), maxt1)
# dedup across files (same key)
seen = set(); R2 = []
for r in runs:
    if r['kind'] in ('a5', 'free'):
        key = (r['kind'],) + normal_key(r['g'], r['Ms']) if not r['closed'] else None
        if key is not None and key in seen: continue
        seen.add(key)
    R2.append(r)
runs = R2
print('runs', len(runs), {k: sum(1 for r in runs if r['kind'] == k) for k in ('a5', 'free', 'planar', 't1')}, flush=True)

def line_of(g):
    toks = [g.n, g.m]
    for a, b in g.E: toks += [a, b]
    return ' '.join(map(str, toks + list(g.fv)))

fo = gzip.open(pref + '_feat.jsonl.gz', 'wt'); ro = []
for ri, r in enumerate(runs):
    g = r['g']; Ms = r['Ms']; R = len(Ms)
    a5 = [a5bit(g, M) for M in Ms]
    words = [g.ncomp(Ms[t - 1] | Ms[t]) if (t > 0 or r['closed']) else None for t in range(R)]
    ro.append(dict(id=ri, src=r['src'], kind=r['kind'], n=r['n'], line=line_of(g), M=[sorted(M) for M in Ms],
                   k=[g.kidx(M) for M in Ms], a5=a5, word=words, start=r['start'], end=r['end'], closed=r['closed'],
                   **({'hole': r['hole'], 'Nch': r['Nch']} if r['kind'] == 'planar' else {})))
    for t in range(R):
        F = state_features(g, Ms, t, r['closed'])
        if r['kind'] == 'planar':
            P = planar_features(r, t); side = P.pop('_side', None); F.update(P)
            if side is not None:
                F['_sideA'] = sorted(e for e, s in side.items() if s == 'A')
        F.update(run=ri, kind=r['kind'], n=r['n'], R=R, closed=r['closed'])
        fo.write(json.dumps(F) + '\n')
fo.close()
with gzip.open(pref + '_runs.json.gz', 'wt') as f: json.dump(ro, f)
print('done', flush=True)
