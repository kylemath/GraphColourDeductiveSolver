#!/usr/bin/env python3
"""Census34 summary: usage summarise34.py out/eval-34.jsonl [out/frame-34.txt] -> stdout"""
import sys, json, collections
recs = [json.loads(l) for l in open(sys.argv[1])]
ng = len(recs); nh = sum(len(r['holes']) for r in recs); deg5 = sum(r['deg5'] for r in recs)
errs = [(r['name'], r['errs']) for r in recs if r['errs']]
print(f"graphs {ng}  degree-5 holes evaluated {nh} / {deg5}  graphs with errors {len(errs)}")
for e in errs[:20]: print('  ERR', e)
H = [(r['name'], int(h), e) for r in recs for h, e in r['holes'].items()]
npc = sum(e['pc'] for _, _, e in H); print(f"PureClean {npc} / {nh}; non-PureClean: {[(g, h) for g, h, e in H if not e['pc']][:20]}")
mf = min(e['mf'] for _, _, e in H); print(f"min class F/N {mf}; holes at 1/4: {sum(1 for _, _, e in H if e['q'] == 0)} in {len({g for g, _, e in H if e['q'] == 0})} graphs; below 1/4: {[(g, h) for g, h, e in H if e['q'] < 0]}")
marg = max(min(e['mf'] for e in r['holes'].values()) for r in recs if r['holes'])
gm = {r['name']: max(e['mf'] for e in r['holes'].values()) for r in recs if r['holes']}
low = sorted(gm.items(), key=lambda x: x[1])[:5]; print(f"lowest graph margins (max over v of min class F/N): {low}")
smp = [r for r in recs if r['sample']]; lp = [sum(r['lp'][k] for r in smp) for k in range(4)]
print(f"lock parity sample: {len(smp)} graphs ({100*len(smp)/ng:.1f}%), {sum(len(r['holes']) for r in smp)} holes, {lp[0]} unfilled states, failures L2 {lp[1]} L1 {lp[2]} Kam-even {lp[3]}")
print(f"f66 allDL vs c33 all-DL cycle count on sample holes: mismatches {sum(1 for r in smp for e in r['holes'].values() if e.get('f66allDL') != e['ndlc'])}")
C = [(g, h, c) for g, h, e in H for c in e['dlc']]
print(f"all-DL pi-cycles: {len(C)} at {sum(1 for _, _, e in H if e['ndlc'])} holes; with filled-free class: {[x for x in C if x[2][4] == 0]}")
for g, h, c in C: print(f"   {g} h{h} L={c[0]} N={c[1]}..{c[2]} class size {c[3]} filled {c[4]}")
key = lambda v: 999 if v < 0 else v
Rh = collections.Counter(key(e['R']) for _, _, e in H); NRh = collections.Counter(key(e['NR']) for _, _, e in H)
print('R histogram', sorted(Rh.items())); print('NR histogram', sorted(NRh.items()))
print(f"Rcyc holes {sum(1 for _, _, e in H if e['Rcyc'])}  NRcyc holes (NRC violations) {sum(1 for _, _, e in H if e['NRcyc'])}")
mR = max(Rh); mNR = max(NRh)
print(f"max R {mR} at {[(g, h, e['NR'], e['w']) for g, h, e in H if key(e['R']) == mR]}")
print(f"max NR {mNR} at {[(g, h, e['R'], e['w']) for g, h, e in H if key(e['NR']) == mNR]}")
pairs = collections.Counter((key(e['R']), key(e['NR'])) for _, _, e in H if key(e['R']) >= 4)
print('(R,NR) pairs with R>=4', sorted(pairs.items()))
runs = collections.Counter(); runsNR = collections.Counter()
for _, _, e in H:
    for L, c in enumerate(e['runs'], 1): runs[L] += c
    for L, c in enumerate(e['runsNR'], 1): runsNR[L] += c
print('maximal interior runs by length L (all / entirely N<=9):', [(L, runs[L], runsNR[L]) for L in sorted(runs) if L >= 3])
print('max degree', collections.Counter(r['maxdeg'] for r in recs))
