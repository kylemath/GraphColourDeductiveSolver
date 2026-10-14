"""Aggregate kclass4 output at good holes (T non-4-colourable, T - h 4-colourable): per class [size, filled, DL,
unfilledNonDL, minK, maxK, viol, onCycles, piPathEnds].  A parity-clean class (viol = 0) with filled = 0 is an LPC
counterexample.  usage: analyse.py KCLASS.jsonl HOLES.jsonl"""
import sys, json, collections
holes = {}
for l in open(sys.argv[2]):
    r = json.loads(l); holes[r['name']] = (set(r['good']), r)
K = 'cls2[size,filled,DL,unfilledNonDL,minKdeg,maxKdeg,lockParityViolations,onCycles,piPathEnds]'
surf = lambda r: next(s for s in ('rp2x3', 'genus2', 'klein', 'rp2', 'torus') if s in r['orig'] or s in r.get('surface', ''))
T = collections.defaultdict(collections.Counter); cex = []; sizes = collections.Counter(); fr = collections.defaultdict(list)
for l in open(sys.argv[1]):
    r = json.loads(l)
    good, meta = holes[r['graph']]
    if r['hole'] not in good: continue
    s = surf(meta); t = T[s]
    t['holes'] += 1; t['states'] += r['states']; t['pid_bad'] += sum(r['pid_bad'])
    for c in r[K]:
        size, filled, DL, nonDL, minK, maxK, viol, onc, pe = c
        t['classes'] += 1; sizes[size] += 1
        if filled: t['FILLED?!'] += 1
        if viol == 0: t['parity_clean'] += 1; cex.append((r['graph'], r['hole'], c))
        if size == 1: t['singletons'] += 1
        if onc: t['classes_with_cycle_states'] += 1
        fr[s].append(viol / size)
    t['allDLcyc'] += len(r['allDLcyc'])
for s in sorted(T):
    v = sorted(fr[s]); print(s, dict(T[s]), 'violator fraction min %.3f median %.3f' % (v[0], v[len(v) // 2]))
print('class sizes', sorted(sizes.items())[:20], 'max', max(sizes))
print('PARITY-CLEAN (LPC counterexamples):', len(cex)); [print(x) for x in cex[:20]]
