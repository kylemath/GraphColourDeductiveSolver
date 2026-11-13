# final exact evaluation of the best (c) run: rational amounts on a 1/U grid, binding rows, parameter counts.
import pickle, sys, json, numpy as np, net2 as N2
from fractions import Fraction as Fr
B = pickle.load(open('cache_B2.pkl', 'rb')); R = pickle.load(open(sys.argv[1], 'rb')); s = R['sol']; U = int(sys.argv[2]); A7, A6 = B['A7'], B['A6']
P = np.maximum(np.round(s['P'] * U), 0).astype(np.int64); a = int(round(s['th7'] * U)); b = int(round(s['th6'] * U))
E = N2.exact(B, P, a, b, R['W2'], R['m2'], R['W3'], R['m3'], U=U); sc = U * N2.SCALE; mx = N2.maxfinal(B, E)
st = lambda w: ''.join(map(str, w))
b7 = np.flatnonzero(~A7['excused'] & (E['f7'] == mx)); b6 = np.flatnonzero(~A6['excused'] & (E['f6'] == mx)); b5 = np.flatnonzero(E['f5'] == mx)
out = dict(run=sys.argv[1], lp_t_float=s['t'], U=U, max_final=str(Fr(int(mx), sc)), max_final_float=mx / sc, max_final_t_units=mx / sc / 60,
           th7=str(Fr(a, U)), th6=str(Fr(b, U)), m2=int(R['m2']), m3=int(R['m3']),
           nonzero_push=int((P > 0).sum()), nonzero_W2=int((R['W2'] != 0).sum()), nonzero_W3=int((R['W3'] != 0).sum()),
           n_binding=dict(r7=len(b7), r6=len(b6), r5=len(b5)),
           binding_7=[[st(B['R7'][i][0]), st(B['R7'][i][1])] for i in b7[:40]], binding_6=[[st(B['R6'][i][0]), st(B['R6'][i][1])] for i in b6[:40]],
           binding_5=[st(B['W5'][i]) for i in b5],
           rows=dict(r7=A7['n'], r7_excused=int(A7['excused'].sum()), r6=A6['n'], r6_excused=int(A6['excused'].sum()), r5=len(B['W5'])),
           push={N2.pname(i): str(Fr(int(P[i]), U)) for i in np.flatnonzero(P)})
json.dump(out, open('result_stage1c.json', 'w'), indent=1)
print(json.dumps({k: v for k, v in out.items() if k not in ('push', 'binding_7', 'binding_6')}, indent=1))
