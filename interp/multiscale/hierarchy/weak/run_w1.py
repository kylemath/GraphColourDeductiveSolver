# Driver: python run_w1.py name seed  -> logs/name_seed.jsonl (per-merge) and summary.jsonl
import sys, json, time, collections, random, os
sys.path.insert(0, '/mnt/project-files/multiscale/hierarchy/weak'); sys.path.insert(0, '/mnt/project-files/multiscale/hierarchy')
import wk
from wk import run
if os.environ.get('NPERM'): wk.NPERM = int(os.environ['NPERM'])
from e1_hier import make
name, seed = sys.argv[1], int(sys.argv[2]); L = int(sys.argv[3]) if len(sys.argv) > 3 else 40
os.makedirs('logs', exist_ok=True)
log = open('logs/%s_s%d_L%d%s.jsonl' % (name, seed, L, '_p24' if wk.NPERM > 6 else ''), 'w')
res = run(name, make(name), seed=seed, L=L, log=log)
recs = res.pop('recs'); leaves = res.pop('leaves')
ch = [r for r in recs if r['chords']]; cl = [r for r in recs if not r['chords']]; kc = [r for r in recs if not r['chords'] and r['kid_chords']]
H = lambda rs, k: dict(sorted(collections.Counter(r[k] for r in rs).items(), key=lambda t: (t[0] is None, t[0] if t[0] is not None else 0)))
summ = dict(nperm=wk.NPERM, name=name, seed=seed, L=L, **res, merges=len(recs), chorded_merges=len(ch), bad_split_merges=sum(r['bad_split'] for r in recs),
            R_chordless=H(cl, 'R'), R_chorded=H(ch, 'R'), R_chordless_kids_chorded=H(kc, 'R'), w_chordless_kids_chorded=H(kc, 'w'), w_chordless=H(cl, 'w'), w_chorded=H(ch, 'w'),
            max_chords=max([r['chords'] for r in recs], default=0), max_pockets=max([r['pockets'] for r in recs], default=0),
            fallbacks=collections.Counter(r['fallback'] for r in recs if r['fallback']),
            max_ptau_before=max([r['ptau_before'] for r in recs], default=0), max_strict_tau=max([r['strict_tau_after'] for r in recs], default=0),
            leaves_n=len(leaves), leaves_chorded=sum(1 for l in leaves if l['chords']), leaves_not_weak=sum(1 for l in leaves if not l['weak_level']),
            maxleaf=max(l['n'] for l in leaves))
print(json.dumps(summ), flush=True)
open('summary.jsonl', 'a').write(json.dumps(summ)+'\n')
