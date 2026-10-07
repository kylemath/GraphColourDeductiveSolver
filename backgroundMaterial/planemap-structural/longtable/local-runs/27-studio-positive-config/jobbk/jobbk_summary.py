#!/usr/bin/env python3
"""Job BK summary from out/bk{25,26,27}{,m}.jsonl (picyc.bk --jobbk). pos rows: [w, L, gamma, (c) over all unfilled states, (c) over DD endpoints, #distinct cycles hit,
giant hit, class]; class rows: [class, #cycles, |class|, F, w(giant), L(giant), F on giant, sum Lambda of positive cycles hitting the giant, rem(giant)]."""
import json
from collections import Counter, defaultdict
P = Counter(); fails = []; frac = []; small_ok = Counter(); nhit = Counter(); hall = Counter(); gfr = []; halls = []
for o in (25, 26, 27):
    for suf in ('', 'm'):
        for l in open('../out/bk%d%s.jsonl' % (o, suf)):
            if '"jobbk"' not in l: continue
            r = json.loads(l); b = r['jobbk']; pat = r['pattern']; C = {c[0]: c for c in b['classes']}
            for w, L, gam, okA, okD, nh, hg, ci, *_ in b["pos"]:
                c = C[ci]; P[(pat, 'positive cycles')] += 1; P[(pat, '(c) all states fails')] += 1 - okA; P[(pat, '(c) DD endpoints fails')] += 1 - okD
                if not okA or not okD: fails.append((r['name'], r['hole'], suf or 'plantri', pat, w, L, gam, okA, okD, nh, hg))
                gshare = c[5] / c[2]; P[(pat, 'giant hit by sigma-images')] += hg
                big = gshare > 1 - 1 / L; small_ok[('giant share > 1 - 1/L(Z)' if big else 'giant share <= 1 - 1/L(Z)', '(c) holds' if okA else '(c) fails', 'giant hit' if hg else 'giant not hit')] += 1
                nhit[min(nh, 10)] += 1
            for c in b['classes']:
                gfr.append((c[5] / c[2], c[6] / max(1, c[3]), c[1]))
                hall['classes'] += 1; hall['need <= -rem(giant)'] += c[7] <= -c[8]; hall['need <= -Lambda(giant)'] += c[7] <= -5 * c[4]
                if c[7] > -c[8]: halls.append((r['name'], r['hole'], suf or 'plantri', pat, c))
print('(1) statement (c) by pattern (positive cycles / failures over all unfilled states / failures over DD endpoints / giant hit):')
pats = sorted({k[0] for k in P})
for p in pats: print('    %-12s %6d %5d %5d %6d' % (p, P[(p, 'positive cycles')], P[(p, '(c) all states fails')], P[(p, '(c) DD endpoints fails')], P[(p, 'giant hit by sigma-images')]))
print('    totals:', sum(P[(p, 'positive cycles')] for p in pats), 'cycles; fail(all)', sum(P[(p, '(c) all states fails')] for p in pats), 'fail(DD)', sum(P[(p, '(c) DD endpoints fails')] for p in pats))
print('    failures (first 30):'); [print('     ', f) for f in fails[:30]]
import statistics
print('(2) giant cycle: share of class states min/median/max %.3f / %.3f / %.3f; share of filled states min/median/max %.3f / %.3f / %.3f; #cycles per class median %d max %d' % (
    min(g[0] for g in gfr), statistics.median(g[0] for g in gfr), max(g[0] for g in gfr), min(g[1] for g in gfr), statistics.median(g[1] for g in gfr), max(g[1] for g in gfr),
    statistics.median(g[2] for g in gfr), max(g[2] for g in gfr)))
print('    share-of-class histogram:', dict(Counter(round(g[0], 1) for g in gfr)))
print('(3) #distinct cycles hit by a positive cycle\'s sigma-images:', dict(sorted(nhit.items())))
print('    giant share vs (c) vs giant hit:'); [print('     ', v, k) for k, v in sorted(small_ok.items())]
print('(4) Hall on the giant (sum Lambda(Z) of positive Z whose images hit it, vs its -rem):', dict(hall)); [print('     ', h) for h in halls[:10]]
# statement (c) ratio baseline: best sigma-target ratio -Lambda(T)/Lambda(Z) = bestneg / w (row field 8)
rat = []
for o in (25, 26, 27):
    for suf in ('', 'm'):
        for l in open('../out/bk%d%s.jsonl' % (o, suf)):
            if '"jobbk"' not in l: continue
            r = json.loads(l)
            for row in r['jobbk']['pos']:
                if len(row) > 8: rat.append((row[8] / row[0], r['pattern'], row[2], r['name'], r['hole'], suf or 'plantri', row[0], row[1]))
rat.sort()
print('(c) ratio baseline: min over all positive cycles of best -Lambda(T)/Lambda(Z):', rat[:5])
g6 = [x for x in rat if x[1] == '5,5,5,5,6' and x[2]]
print('    over (5,5,5,5,6) Gamma-cycles:', g6[:5])
print('    by pattern (min ratio):', {p: min(x[0] for x in rat if x[1] == p) for p in sorted({x[1] for x in rat})})
