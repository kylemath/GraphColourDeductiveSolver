#!/usr/bin/env python3
"""path3-local/summarize.py -- aggregate kc_search_local logs: per run the seed score, best score, lowest large-class filled fraction
(and where), evaluations, accepted/improving moves by type, Intern C signature totals, stuck stops. Usage: summarize.py RUNDIR [RUNDIR...]"""
import sys, os, json, glob, gzip
rows = []
for d in sys.argv[1:]:
    for p in sorted(glob.glob(os.path.join(d, 'log-*.jsonl*'))):
        seed = best = end = None; low = None; n_eval = 0; one = viol = 0; stop = None; frac_hist = {}
        for L in (gzip.open(p, 'rt') if p.endswith('.gz') else open(p)):
            r = json.loads(L)
            if 'END' in r: end = r; continue
            if 'STOP' in r: stop = r; continue
            if r.get('score') is None: continue
            n_eval += 1; one += r['sig']['onefill']; viol += r['sig']['viol']
            if r['move'] == 'seed': seed = r
            if r['large10']:
                fr, size, filled, dl, h = r['large10'][0]
                k = round(fr, 4); frac_hist[k] = frac_hist.get(k, 0) + 1
                if low is None or (fr, -size) < (low[0], -low[1]): low = (fr, size, filled, dl, h, r['sha'], r['step'], r['move'])
        rows.append({'run': os.path.basename(p)[4:].split('.jsonl')[0], 'dir': d, 'n': seed['n'] if seed else None,
                     'seed_low': seed['large10'][0][:4] if seed and seed['large10'] else None,
                     'seed_kappa_max': max(seed['kappa'].values()) if seed else None,
                     'lowest': {'frac': round(low[0], 4), 'size': low[1], 'filled': low[2], 'DL': low[3], 'hole': low[4], 'sha16': low[5],
                                'step': low[6], 'move': low[7]} if low else None,
                     'evals': n_eval, 'onefill_classes_seen': one, 'intern_C_violations': viol, 'stuck_stop': stop is not None,
                     'end_stats': end['stats'] if end else None, 'best_score': end['best_score'] if end else None,
                     'lowest5_fraction_counts': sorted(frac_hist.items())[:5]})
for r in rows: print(json.dumps(r))
