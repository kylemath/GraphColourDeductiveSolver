import pickle, json, numpy as np, net as NT, hashlib
from fractions import Fraction as Fr
B = pickle.load(open('cache_B.pkl', 'rb')); H = pickle.load(open('hard_s0_300.pkl', 'rb'))
P, th, W, m = H['P'], int(H['theta']), H['W'], int(H['margin'])
E = NT.exact(B, P, th, W, m); live = ~B['excused']
f7 = np.where(live, E['f7'], -10**12); mx = max(f7.max(), E['f5'].max(), E['f6'].max())
out = dict(max_final=str(Fr(int(mx), NT.SCALE)), max_final_t_units=str(Fr(int(mx), NT.SCALE * 60)), theta=th, margin=m,
           nonzero_push=int((P != 0).sum()), nonzero_attention=int((W != 0).sum()),
           binding_7=[[''.join(map(str, B['R7'][i][0])), ''.join(map(str, B['R7'][i][1])), int(E['c1'][i])] for i in np.flatnonzero(f7 == mx)],
           binding_5=[''.join(map(str, B['W5'][i])) for i in np.flatnonzero(E['f5'] == mx)],
           binding_6=[''.join(map(str, B['W6'][i])) for i in np.flatnonzero(E['f6'] == mx)],
           rows=dict(live7=int(live.sum()), excused7=int((~live).sum()), r5=len(B['W5']), r6=len(B['W6'])),
           push={'%d->%d {%d,%d} n5=%d' % (du, dv, x, y, n5): int(P[NT.pidx(du, dv, x, y, n5)]) for du in (5, 6) for dv in (6, 7)
                 for (x, y) in sorted({tuple(sorted(k)) for k in NT.PAIR}) for n5 in range(7) if P[NT.pidx(du, dv, x, y, n5)]})
json.dump(out, open('result_stage1.json', 'w'), indent=1)
print(json.dumps({k: v for k, v in out.items() if k != 'push'}, indent=1)); print(len(out['push']), 'push entries')
