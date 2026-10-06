#!/usr/bin/env python3
"""Regenerate certificates for finished seeds with best_len >= MIN (same seeds, same code path; the original certificates stored rot by reference
and were corrupted by later moves -- bug fixed in searcher.cert(); RNG consumption unchanged). Writes runs/band_X/recert_seed_N.json. [computed, exploratory]"""
import json, os, sys, glob
import searcher as S
MIN = int(sys.argv[1]) if len(sys.argv) > 1 else 4
n = bad = 0
for f in sorted(glob.glob(os.path.join(S.HERE, 'runs', 'band_*', 'seed_*.json'))):
    r = json.load(open(f))
    if r['status'] != 'done' or r['best_len'] < MIN: continue
    o = f.replace('seed_', 'recert_seed_')
    if os.path.exists(o): continue
    new = S.run_seed(r['band'], r['seed'], r['steps'])
    same = (new['best_len'], new['best_tiebreak'], new['eval_hist']) == (r['best_len'], r['best_tiebreak'], r['eval_hist'])
    new['reproduces_original'] = same
    S.atomic_write(o, new); n += 1; bad += (not same)
print('regenerated', n, 'not reproducing:', bad)
