#!/usr/bin/env python3
"""Track F: aggregate f66 hole records (IPR C60-C100) + cross-check against Studio Job BO (picyc.bo --jobbo) where available.
usage: anal_ipr.py HOLES.jsonl... > summary"""
import sys, json, glob, collections, os
recs = []
for f in sys.argv[1:]:
    for l in open(f):
        d = json.loads(l)
        if d.get('kind') == 'hole': recs.append(d)
by_n = collections.defaultdict(list)
for d in recs: by_n[d['n']].append(d)
print('order(dual) C_N graphs holes  maxrun  allDL piFail parfail1 parfail2 jordanfail  mod4-violations  run-length histogram (summed)')
tot = collections.Counter()
for n in sorted(by_n):
    R = by_n[n]; g = len({d['graph'] for d in R}); hist = collections.Counter()
    for d in R: hist.update({int(k): v for k, v in d['runlen'].items()})
    m4bad = sum(v for d in R for k, v in d['mod4'].items() if not (k == 'p1 curv+E mod4=1' or k == 'p2 curv+E mod4=0'))
    row = dict(maxrun=max(d['maxrun'] for d in R), allDL=sum(d['allDL'] for d in R), piFail=sum(d['piFail'] for d in R), pf1=sum(d['parfail1'] for d in R),
               pf2=sum(d['parfail2'] for d in R), jf=sum(d['jordanfail'] for d in R))
    for k, v in row.items(): tot[k] += v if k != 'maxrun' else 0
    tot['holes'] += len(R); tot['graphs'] += g; tot['m4bad'] += m4bad; tot['nDL'] += sum(d['nDL'] for d in R)
    print(f"{n:5d} C{2*n-4:<4d} {g:5d} {len(R):6d} {row['maxrun']:6d} {row['allDL']:6d} {row['piFail']:6d} {row['pf1']:8d} {row['pf2']:8d} {row['jf']:8d} {m4bad:8d}   {dict(sorted(hist.items()))}")
print('TOTAL', dict(tot))
# per-hole maxrun distribution and the per-graph min/max over its 12 holes (multi-hole view)
print('\nper-graph: min over holes of maxrun (best hole) / max over holes, by order')
G = collections.defaultdict(list)
for d in recs: G[(d['n'], d['graph'])].append(d)
for n in sorted(by_n):
    mins = collections.Counter(); maxs = collections.Counter()
    for (nn, g), R in G.items():
        if nn != n: continue
        mins[min(d['maxrun'] for d in R)] += 1; maxs[max(d['maxrun'] for d in R)] += 1
    print(f"  n={n} C{2*n-4}: best-hole maxrun {dict(sorted(mins.items()))} | worst-hole maxrun {dict(sorted(maxs.items()))}")
# cross-check vs Job BO
bo = {}
for f in glob.glob(os.path.join(os.path.dirname(__file__), '../../../../../backgroundMaterial/planemap-structural/longtable/local-runs/27-studio-positive-config/out/boipr.shards/*.out')):
    for l in open(f):
        try: d = json.loads(l)
        except Exception: continue
        if d.get('kind') == 'hole' and 'jobbo' in d: bo[(d['name'], d['hole'])] = d
match = mism = 0; ex = []; nofill = 0; ncls = collections.Counter()
for d in recs:
    k = (d['graph'], d['hole'])
    if k not in bo: continue
    b = bo[k]['jobbo']; nofill += b['classes_without_filled']; ncls[b['classes']] += 1
    same = (b['maxrun'] == d['maxrun'] and {int(a): v for a, v in b['runlen'].items()} == {int(a): v for a, v in d['runlen'].items()} and len(b['all_DL_cycles']) == d['allDL'] and bo[k]['nDL'] == d['nDL'])
    if same: match += 1
    else:
        mism += 1
        if len(ex) < 5: ex.append((k, b['maxrun'], d['maxrun'], bo[k]['nDL'], d['nDL']))
print(f"\ncross-check vs Studio Job BO (picyc.bo --jobbo, same holes, same link orientation): {match} holes identical (nDL, run-length histogram, #all-DL cycles), {mism} differ {ex}")
print(f"  Job BO Kempe classes per hole on these holes: {dict(ncls)}; classes without a filled state: {nofill}")
