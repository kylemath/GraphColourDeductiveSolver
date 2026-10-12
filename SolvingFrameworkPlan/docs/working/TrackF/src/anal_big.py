#!/usr/bin/env python3
"""Track F: summaries of sampled runs (Goldberg, long tubes, IPR C108-C120 samples)."""
import sys, json, collections, re
def load(f): return [json.loads(l) for l in open(f) if l.strip()]
mode, f = sys.argv[1], sys.argv[2]
R = load(f)
if mode == 'gold':
    G = collections.defaultdict(list)
    for d in R: G[d['graph']].append(d)
    for g, L in G.items():
        print(f"{g}: hole {L[0]['hole']} flat radius {L[0]['dpent']-1}; samples {sum(d['samples'] for d in L)}; distinct runs {sum(d['runs'] for d in L)}; maxrun {max(d['maxrun'] for d in L)}; all-DL {sum(d['allDL'] for d in L)}; pocket/pi/Jordan failures {sum(d['parfail1']+d['parfail2']+d['piFail']+d['jordanfail'] for d in L)}")
elif mode == 'tubes':
    G = collections.defaultdict(list)
    for d in R: G[d['graph']].append(d)
    for g, L in sorted(G.items(), key=lambda x: (x[0].split('_')[0], x[1][0]['n'])):
        m66 = [d['maxrun'] for d in L if d['pattern'] == '66666']; mo = [d['maxrun'] for d in L if d['pattern'] != '66666']
        print(f"{g}: n {L[0]['n']} holes {len(L)} maxrun66666 {max(m66) if m66 else '-'} maxrun-other {max(mo) if mo else '-'} allDL {sum(d['allDL'] for d in L)} bad {sum(d['parfail1']+d['parfail2']+d['piFail']+d['jordanfail'] for d in L)}")
elif mode == 'big':
    by = collections.defaultdict(list)
    for d in R: by[d['n']].append(d)
    for n in sorted(by):
        L = by[n]; flat = [d for d in L if d['dpent'] >= 3]
        print(f"n={n} C{2*n-4}: graphs {len({d['graph'] for d in L})} holes {len(L)} (flat {len(flat)}) samples/hole {L[0]['samples']} maxrun {max(d['maxrun'] for d in L)} allDL {sum(d['allDL'] for d in L)} bad {sum(d['parfail1']+d['parfail2']+d['piFail']+d['jordanfail'] for d in L)}")
    top = sorted(R, key=lambda d: -d['maxrun'])[:5]; print('top:', [(d['graph'], d['hole'], d['maxrun']) for d in top])
