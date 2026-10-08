#!/usr/bin/env python3
"""TrackO: aggregate to_eng JSON lines.
usage: to_summary.py LABEL=glob[,glob] [LABEL=...]  > summary.txt
Per label and order n: holes, skipped, R histogram (per hole; 'cyc' = interior pi-cycle), max R, NR max,
interior states by N, long-run (L>=4) near-rigid share, and the holes attaining the label's max R.
"""
import sys, json, glob
from collections import Counter, defaultdict


def load(globs):
    for g in globs.split(','):
        for f in sorted(glob.glob(g)):
            for l in open(f):
                if l.startswith('{'):
                    yield json.loads(l)


def main():
    for arg in sys.argv[1:]:
        lab, gl = arg.split('=', 1)
        byn = defaultdict(lambda: dict(holes=0, skip=0, R=Counter(), NR=Counter(), intN=Counter(), runs=Counter(), runsNR=Counter(), longAll=0, longNR=0, graphs=set(), states=0))
        runs_long = Counter(); runs_long_nr = Counter(); best = []
        maxNlong = Counter(); joint = Counter()
        for r in load(gl):
            if r.get('run'):
                L = r['L']; runs_long[L] += 1
                if max(r['N']) <= 9: runs_long_nr[L] += 1
                maxNlong[(L, min(r['N']))] += 1
                continue
            d = byn[r['n']]; d['graphs'].add(r['g'])
            if 'skip' in r: d['skip'] += 1; continue
            d['holes'] += 1; d['states'] += r['S']
            R = r['R'] if r['R'] >= 0 else 'cyc'; d['R'][R] += 1
            NR = r['NR'] if r['NR'] >= 0 else 'cyc'; d['NR'][NR] += 1
            for i, c in enumerate(r['intN']): d['intN'][8 + i] += c
            for i, c in enumerate(r['runs']): d['runs'][i + 1] += c
            for i, c in enumerate(r.get('runsNR', [])): d['runsNR'][i + 1] += c
            if r['R'] >= 4 or r['R'] < 0: joint[(r['R'], r['NR'])] += 1
            d['longAll'] += r['longAll']; d['longNR'] += r['longNR']
            best.append((r['R'] if r['R'] >= 0 else 999, r['g'], r['h'], r['NR'], r['RmaxN']))
        print(f"=== {lab} ===")
        tot = dict(holes=0, skip=0, R=Counter(), NR=Counter(), intN=Counter(), runs=Counter(), runsNR=Counter(), longAll=0, longNR=0, graphs=0, states=0)
        for n in sorted(byn):
            d = byn[n]
            Rh = ' '.join(f"{k}:{v}" for k, v in sorted(d['R'].items(), key=lambda x: (isinstance(x[0], str), x[0])))
            NRmax = max((k for k in d['NR'] if k != 'cyc'), default=0)
            Rmax = 'cyc' if 'cyc' in d['R'] else max(d['R'], default=0)
            print(f"n={n:3d} graphs={len(d['graphs']):6d} holes={d['holes']:7d} skip={d['skip']:4d} states={d['states']:11d} maxR={Rmax} maxNR={NRmax}{' NRcyc' if 'cyc' in d['NR'] else ''}  R-hist {Rh}")
            for k in ('holes', 'skip', 'longAll', 'longNR', 'states'): tot[k] += d[k]
            tot['graphs'] += len(d['graphs'])
            for k in ('R', 'NR', 'intN', 'runs', 'runsNR'): tot[k].update(d[k])
        print(f"TOTAL graphs={tot['graphs']} holes={tot['holes']} skipped={tot['skip']} states={tot['states']}")
        print("  R-hist (holes):", ' '.join(f"{k}:{v}" for k, v in sorted(tot['R'].items(), key=lambda x: (isinstance(x[0], str), x[0]))))
        print("  NR-hist (holes):", ' '.join(f"{k}:{v}" for k, v in sorted(tot['NR'].items(), key=lambda x: (isinstance(x[0], str), x[0]))))
        print("  maximal interior runs by length:", ' '.join(f"{k}:{v}" for k, v in sorted(tot['runs'].items()) if v))
        if tot['runsNR']:
            print("  of which entirely near-rigid (all N<=9):", ' '.join(f"{k}:{tot['runsNR'][k]}" for k, v in sorted(tot['runs'].items()) if v))
        print("  holes with R>=4: (R, NR) ->", dict(sorted(joint.items())))
        print("  interior states by N:", ' '.join(f"{k}:{v}" for k, v in sorted(tot['intN'].items()) if v))
        ni = sum(tot['intN'].values()); nnr = sum(v for k, v in tot['intN'].items() if k <= 9)
        print(f"  interior states with N<=9: {nnr}/{ni}")
        print("  runs L>=4 (dumped, <=20 per hole): by L", dict(sorted(runs_long.items())), " all-N<=9:", dict(sorted(runs_long_nr.items())))
        print("  runs L>=4 by (L, min N along run):", dict(sorted(maxNlong.items())))
        best.sort(reverse=True)
        print("  top holes (R, graph, h, NR, maxN on a longest run):", best[:8])
        print()


if __name__ == '__main__':
    main()
