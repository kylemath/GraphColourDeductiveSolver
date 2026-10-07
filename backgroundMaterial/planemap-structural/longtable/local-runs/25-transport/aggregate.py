import json, glob
from collections import Counter
R = [json.loads(l) for f in sorted(glob.glob('out-*.jsonl')) for l in open(f)]
print('classes with positive cycle:', len(R), ' positive cycles:', sum(r['npos'] for r in R), ' classes npos>1:', sum(r['npos'] > 1 for r in R))
print('nzero>0 classes:', sum(r['nzero'] > 0 for r in R))
for k in R[0]['v']:
    vs = [(r, r['v'][k]) for r in R]
    ok = sum(v['ok'] for _, v in vs)
    sl = min(vs, key=lambda x: x[1]['slack']); hs = min(vs, key=lambda x: x[1]['hall_ratio'])
    fails = [(r['n'], r['gentri'], r['hole'], r['posW']) for r, v in vs if not v['ok']]
    print(f'{k:20s} holds {ok}/{len(R)}  min slack {sl[1]["slack"]} (n{sl[0]["n"]} g{sl[0]["gentri"]} h{sl[0]["hole"]} posW{sl[0]["posW"]}, cap {sl[1]["capreach"]})  min Hall ratio cap/supply {hs[1]["hall_ratio"]} bad cut {hs[1]["bad_cut"]}')
    if fails: print('   first failures:', fails[:3], 'count', len(fails))
print('\nbad cuts under T2_any, 8 tightest by Hall ratio:')
for r in sorted(R, key=lambda r: r['v']['T2_any']['hall_ratio'])[:8]:
    v = r['v']['T2_any']; print(r['n'], r['gentri'], r['hole'], 'posW', r['posW'], 'ncyc', r['ncyc'], 'ratio', v['hall_ratio'], 'bad cut', v['bad_cut'], 'slack', v['slack'])
print('\nbad cuts under T1_DL, 8 tightest:')
for r in sorted(R, key=lambda r: r['v']['T1_DL']['hall_ratio'])[:8]:
    v = r['v']['T1_DL']; print(r['n'], r['gentri'], r['hole'], 'posW', r['posW'], 'ratio', v['hall_ratio'], 'bad cut', v['bad_cut'], 'slack', v['slack'])
print('\nT1 vs T2 differences:', sum(r['v']['T1_DL']['capreach'] != r['v']['T2_any']['capreach'] for r in R), 'classes with different reachable capacity')
print('zero relay changes reach (T2 vs T4 any_zero):', sum(r['v']['T2_any']['capreach'] != r['v']['T4_d2_any_zero']['capreach'] for r in R))
print('T1 not ok but relay-zero ok:', sum((not r['v']['T1_DL']['ok']) and r['v']['T4_d2_DL_zero']['ok'] for r in R))
print('multi-positive classes worst:', [(r['n'], r['gentri'], r['hole'], r['posW'], r['v']['T1_DL']['hall_ratio']) for r in R if r['npos'] > 1])
print('max slack-ratio hist (capreach/supply, T2) min:', min(r['v']['T2_any']['capreach'] / r['v']['T2_any']['supply'] for r in R))
