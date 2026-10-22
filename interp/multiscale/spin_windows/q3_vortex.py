"""Q3: vortex content of windows and where their spin goes.
Per window: forced vortices (odd-degree interior vertices). Per sampled ring class: extension (SAT), boundary
charge Psi (ring word only) and flux |delta|_1; for extending classes, the interior per-colour spin vector S."""
import sys, csv, random, collections, json
import numpy as np
sys.path.insert(0, '/mnt/project-files/multiscale/spin_windows')
from spinlib import *
from q2_budget import Window, random_ring, all_rings
rows = list(csv.DictReader(open('/mnt/project-files/explore/dataset/windows_judged.tsv'), delimiter='\t'))
# dataset-level vortex counts
cnt = collections.defaultdict(collections.Counter)
for x in rows:
    d = [int(t) for t in x['int_degrees'].split(',')]; odd = sum(t % 2 for t in d)
    lab = 'D' if x['two_engine'] == 'D' else ('C' if x['two_engine'] == 'C' else ('notD' if x['kc_D'] == 'false' else 'other'))
    cnt[(x['name'].split('_')[0], lab)][odd] += 1
dl = {}
for k in sorted(cnt):
    c = cnt[k]; tot = sum(c.values()); mean = sum(a * b for a, b in c.items()) / tot; oddfrac = sum(b for a, b in c.items() if a % 2) / tot
    dl['%s_%s' % k] = dict(n=tot, mean_vortices=round(mean, 2), frac_odd_count=round(oddfrac, 3))
    print(k, 'n=%d mean#vortices=%.2f frac(odd #vortices)=%.3f' % (tot, mean, oddfrac))
rng = random.Random(7); res = {}
NW = int(sys.argv[1]) if len(sys.argv) > 1 else 20; NS = int(sys.argv[2]) if len(sys.argv) > 2 else 150
for g, pool in {'a7_D': [x for x in rows if x['name'].startswith('a7_') and x['two_engine'] == 'D'],
                'a7_notD': [x for x in rows if x['name'].startswith('a7_') and x['kc_D'] == 'false' and 11 <= int(x['ring']) <= 15]}.items():
    rng.shuffle(pool); agg = collections.Counter(); spreadh = collections.Counter(); Sabs = collections.Counter()
    for row in pool[:NW]:
        W = Window(row); r, m = W.r, W.m; nodd = sum(W.deg[v] % 2 for v in range(r, r + m))
        for ring in {random_ring(r, rng) for _ in range(NS)}:
            P = Psi12([ring[v] for v in W.word]); neutral = all(p == 0 for p in P)
            D = flux([ring[v] for v in W.word]); fl = sum(abs(D[c][d]) for c in range(4) for d in range(c + 1, 4))
            col = W.extend(ring); good = col is not None
            agg['cls'] += 1; agg['good'] += good; agg['neutral'] += neutral; agg['neutral_good'] += neutral and good
            agg['flux_good'] += fl * good; agg['flux_bad'] += fl * (not good)
            if good:
                exts = [col] + sat_colourings(W.adj, fixed={v: ring[v] for v in range(r)}, k=2, seed=agg['cls'])
                for c in exts:
                    S = [0] * 4
                    for v in range(r, r + m): S[c[v]] += spin(c, W.rot, v)
                    spreadh[max(S) - min(S)] += 1; Sabs[sum(abs(s) for s in S)] += 1
                    agg['ext_samples'] += 1; agg['balanced'] += (max(S) == min(S))
                    agg['nodd_x_samples'] += nodd
        agg['windows'] += 1; agg['vortices'] += nodd; agg['odd_count_windows'] += nodd % 2
    out = dict(agg); out['spread_hist'] = dict(sorted(spreadh.items())); out['sum_abs_S_hist'] = dict(sorted(Sabs.items()))
    out['ext_rate'] = agg['good'] / agg['cls']; out['ext_rate_neutral'] = agg['neutral_good'] / max(1, agg['neutral'])
    out['ext_rate_nonneutral'] = (agg['good'] - agg['neutral_good']) / max(1, agg['cls'] - agg['neutral'])
    out['mean_flux_good'] = agg['flux_good'] / max(1, agg['good']); out['mean_flux_bad'] = agg['flux_bad'] / max(1, agg['cls'] - agg['good'])
    out['frac_balanced_extensions'] = agg['balanced'] / max(1, agg['ext_samples'])
    res[g] = out; print(g, json.dumps(out), flush=True)
json.dump(dict(dataset=dl, sampled=res), open('/mnt/project-files/multiscale/spin_windows/q3_summary.json', 'w'), indent=1)
