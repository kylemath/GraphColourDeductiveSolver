import json,sys
from collections import Counter
R=[json.loads(l) for f in sys.argv[1:] for l in open(f)]
# absolute alpha-graph trajectories in the window 4..8: a2=(f4,h5,g6,f7,h8), a3=(h4,g5,f6,h7,g8), a4=(g4,f5,h6,g7,f8)
T=Counter()
for r in R:
    s=r['seq']; L=len(s); cyc=r['kind']=='gamma'
    rng=range(L) if cyc else range(1,L-1)
    for i in rng:
        if s[i]['pos']!=4 or not s[i]['fix']: continue
        if not cyc and i+4>=L-1: continue
        w=[s[(i+t)%L] for t in range(5)]
        if not all(d['DL'] for d in w): continue
        F=lambda t:w[t]['c'][0]; G=lambda t:w[t]['c'][1]; H=lambda t:w[t]['c'][2]
        a2=(F(0),H(1),F(3),H(4)); a3=(H(0),F(2),H(3)); a4=(G(0),F(1),H(2),F(4))
        T[(r['kind'], 'F8' if w[4]['fix'] else '--', 'F6' if w[2]['fix'] else '--', a2,a3,a4)]+=1
for k,v in sorted(T.items()): print(v,k)
