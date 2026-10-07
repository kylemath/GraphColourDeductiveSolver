#!/usr/bin/env python3
"""aggregate.py LABEL=FILE [LABEL=FILE ...]: Job A (positive classes vs configurations, base rates), Job A2 (link-degree patterns),
Job B (transport, lock-breaking exits, Hall ratio) and chirality comparison over picyc outputs."""
import sys, json
from collections import Counter, defaultdict
def canon(ld, cap=8):
    d = [min(x, cap) for x in ld]; best = None
    for s in (d, d[::-1]):
        for r in range(5):
            t = tuple(s[r:] + s[:r])
            if best is None or t < best: best = t
    return best
def pat(t): return ','.join(('%d' % x) if x < 8 else '8+' for x in t)
runs = []
for a in sys.argv[1:]:
    lab, f = a.split('='); G = {}; H = []
    for l in open(f):
        r = json.loads(l)
        if r['kind'] == 'graph': G[r['name']] = r
        elif 'states' in r: H.append(r)
    runs.append((lab, G, H))
print('=== inputs'); [print(' ', lab, 'graphs', len(G), 'holes', len(H), 'inconclusive', sum(1 for h in H if 'inconclusive' in h)) for lab, G, H in runs]
# ---------- Job A
print('\n=== Job A: positive pi-cycles versus configurations (per hole; "positive" = the hole has a class with a positive cycle)')
print('%-8s %7s %7s %7s | %-34s | %-34s | %-30s' % ('run', 'holes', 'pos', 'rate%', 'config-free GRAPH holes: pos/holes', 'v in NO configuration: pos/holes', 'dist_config>=2: pos/holes'))
tot = Counter()
for lab, G, H in runs:
    c = Counter()
    for h in H:
        g = G[h['name']]; p = h['npos'] > 0; c['holes'] += 1; c['pos'] += p
        if g['cfree']: c['cf'] += 1; c['cfpos'] += p
        if g['cfree'] and g['adj55'] > 0: c['cfa'] += 1; c['cfapos'] += p
        if h['vrole'] == 0: c['nv'] += 1; c['nvpos'] += p
        if h['dist_config'] < 0 or h['dist_config'] >= 2: c['far'] += 1; c['farpos'] += p
    tot.update(c)
    print('%-8s %7d %7d %7.3f | %5d / %-7d (cfree+adj55 graphs: %3d/%-5d) | %5d / %-7d %-14s | %5d / %-7d' % (lab, c['holes'], c['pos'], 100.0 * c['pos'] / max(1, c['holes']), c['cfpos'], c['cf'], c['cfapos'], c['cfa'], c['nvpos'], c['nv'], '(%.3f%%)' % (100.0 * c['nvpos'] / max(1, c['nv'])), c['farpos'], c['far']))
c = tot; print('%-8s %7d %7d %7.3f | %5d / %-7d (cfree+adj55 graphs: %3d/%-5d) | %5d / %-7d %-14s | %5d / %-7d' % ('ALL', c['holes'], c['pos'], 100.0 * c['pos'] / max(1, c['holes']), c['cfpos'], c['cf'], c['cfapos'], c['cfa'], c['nvpos'], c['nv'], '(%.3f%%)' % (100.0 * c['nvpos'] / max(1, c['nv'])), c['farpos'], c['far']))
print('expected positives among config-free-graph holes at the overall rate: %.2f ; among v-in-no-configuration holes: %.2f' % (c['cf'] * c['pos'] / max(1, c['holes']), c['nv'] * c['pos'] / max(1, c['holes'])))
# distance to configuration
dc = defaultdict(Counter)
for lab, G, H in runs:
    for h in H: dc[h['dist_config']]['holes'] += 1; dc[h['dist_config']]['pos'] += h['npos'] > 0
print('by dist_config (-1 = none in graph):', ' '.join('%d: %d/%d' % (d, dc[d]['pos'], dc[d]['holes']) for d in sorted(dc)))
vr = defaultdict(Counter)
for lab, G, H in runs:
    for h in H: vr[h['vrole']]['holes'] += 1; vr[h['vrole']]['pos'] += h['npos'] > 0
print('by vrole bits (1 diamond centre, 2 diamond tip, 4 2.122 deg-5 centre, 16 2.122 tip):', ' '.join('%d: %d/%d' % (d, vr[d]['pos'], vr[d]['holes']) for d in sorted(vr)))
# graphs
gp = Counter()
for lab, G, H in runs:
    posg = {h['name'] for h in H if h['npos']}
    for name, g in G.items(): gp[('cfree' if g['cfree'] else 'config', 'pos' if name in posg else 'nopos')] += 1
print('graphs (per run, summed):', dict(gp))
# positive holes in configuration-free graphs: list
print('positive holes in configuration-free graphs:')
for lab, G, H in runs:
    for h in H:
        if h['npos'] and G[h['name']]['cfree']: print('  ', lab, h['name'], 'hole', h['hole'], 'n', h['n'], 'linkdeg', h['linkdeg'], 'adj55', G[h['name']]['adj55'], 'posW', [p['w'] for p in h['pos']], 'L', [p['L'] for p in h['pos']], 'states', h['states'])
# ---------- Job A2
print('\n=== Job A2: link-degree patterns (cyclic, up to reflection, degrees >= 8 capped), positives / holes, all runs summed')
pc = defaultdict(Counter)
for lab, G, H in runs:
    for h in H: k = canon(h['linkdeg']); pc[k]['holes'] += 1; pc[k]['pos'] += h['npos'] > 0; pc[k]['posclasses'] += h['npos']
rate = c['pos'] / max(1, c['holes'])
rows = sorted(pc.items(), key=lambda kv: -kv[1]['holes'])
print('%-14s %8s %5s %8s %9s' % ('pattern', 'holes', 'pos', 'rate%', 'expected'))
for k, v in rows: print('%-14s %8d %5d %8.3f %9.2f %s' % (pat(k), v['holes'], v['pos'], 100.0 * v['pos'] / v['holes'], v['holes'] * rate, '  <-- ZERO' if v['pos'] == 0 and v['holes'] * rate >= 3 else ''))
for key in [(5, 5, 5, 5, 6), (5, 5, 5, 6, 6), (5, 6, 6, 6, 6)]:
    v = pc.get(key, Counter()); print('target pattern %s: %d positives in %d holes (expected %.1f)' % (pat(key), v['pos'], v['holes'], v['holes'] * rate))
# ---------- Job B
print('\n=== Job B: transport on every positive hole (sharp form d = lock-breaking exits from DL states only)')
V = ['a_DL_allpairs', 'b_DL_otherpair', 'c_anystate', 'd_DL_lockbreaking', 'e_DL_otherpair_lockbreaking']
for lab, G, H in runs:
    st = Counter(); hall = {v: [] for v in V}; fails = {v: [] for v in V}; nolb = []; thmw_bad = 0; maxw = 0; wset = Counter(); Lmax = 0
    for h in H:
        if not h['npos']: continue
        st['posholes'] += 1; st['poscycles'] += h['npos']
        for p in h['pos']:
            wset[p['w']] += 1; maxw = max(maxw, p['w']); Lmax = max(Lmax, p['L'])
            if p['exits_to_neg_lockbreaking'] == 0: nolb.append((h['name'], h['hole'], p['w'], p['L']))
            if 'class' in p and not p['class']['thmW']: thmw_bad += 1
        for t in h['transport']:
            st['components'] += 1
            for v in V:
                r = t[v]
                if not r['ok']: fails[v].append((h['name'], h['hole'], t['posW'], r['flow'], r['supply']))
                if r['hall_ratio'] is not None: hall[v].append((r['hall_ratio'], h['name'], h['hole'], t['posW'], r['hall_set']))
                else: st['hall_none_' + v] += 1
    print('-- %s: positive holes %d, positive cycles %d, transport components %d, Theorem W failures %d, max w %d, max L %d, windings %s' % (lab, st['posholes'], st['poscycles'], st['components'], thmw_bad, maxw, Lmax, sorted(wset.items())))
    print('   positive cycles with NO lock-breaking exit to a negative cycle: %d %s' % (len(nolb), nolb[:5]))
    for v in V:
        hs = sorted(hall[v])
        print('   %-28s fails %3d; min Hall ratio %s; tightest: %s' % (v, len(fails[v]), ('%.3f' % hs[0][0]) if hs else 'n/a', [(round(x[0], 3), x[1], x[2], x[3]) for x in hs[:3]]))
        if fails[v]: print('      failures:', fails[v][:5])
# ---------- chirality
print('\n=== chirality: positive holes under the two orientations of the same graph list')
byname = {lab: {(h['name'], h['hole']) for h in H if h['npos']} for lab, G, H in runs}
labs = [lab for lab, _, _ in runs]
for i in range(len(labs)):
    for j in range(i + 1, len(labs)):
        a, b = labs[i], labs[j]
        if {x[0] for x in byname[a]} and a.rstrip('m') == b.rstrip('m') and a != b:
            A, B = byname[a], byname[b]; ga = {x[0] for x in A}; gb = {x[0] for x in B}
            print('  %s vs %s: positive holes %d vs %d, common holes %d; graphs with a positive hole: %d vs %d, both %d, only %s %d, only %s %d' % (a, b, len(A), len(B), len(A & B), len(ga), len(gb), len(ga & gb), a, len(ga - gb), b, len(gb - ga)))
