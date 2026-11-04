# dump recv_coef_R2 / sender-row coefficients for cert rows + random arrangements; run with and without q7.  usage: python3 dumprows.py OUT.json <engine args>
import sys, os, json, random
ENG = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'eng', 'pcheck.py')
out = sys.argv[1]; sys.argv = [ENG, 'help'] + sys.argv[2:]
ns = {'__file__': ENG, '__name__': 'pcheck_s62d'}; exec(compile(open(ENG).read(), ENG, 'exec'), ns); ns['l3q_load']()
C = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'certs', 'certP2full_rat.json')))
res = {}
def dump(cf): return {repr(k): v for k, v in cf.items() if v}
for i, c in enumerate(C):
    r = c['row']
    if r[0] == 'receiverR2': res['cert%d' % i] = dump(ns['recv_coef_R2'](int(r[1]), r[2], r[3], True, None))
rnd = random.Random(5); n = 0
while n < 4000:
    d = rnd.choice((7, 7, 8, 9)); lk = ''.join(rnd.choice('56789') for _ in range(d)); sv = ''.join(rnd.choice('56789') for _ in range(d))
    try: cf = ns['recv_coef_R2'](d, lk, sv, True, None)
    except Exception as e: continue
    res['r%d_%s_%s' % (n, lk, sv)] = dump(cf); n += 1
res['sender'] = [[wd, dump(cf)] for wd, cf, b in ns['R2_sender_rows']()]
json.dump(res, open(out, 'w')); print('dumped', len(res))
