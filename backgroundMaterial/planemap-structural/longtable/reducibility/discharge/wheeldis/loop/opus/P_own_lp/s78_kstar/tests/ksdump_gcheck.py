# s78: cross-check a ksdump TSV against W6's grammar.py on W6's own picture (as test_edge.py): per row and family, F_pay_n == grammar SURE
# payer count and F_rec_x == grammar POSSIBLE payee count (F_rec_n >= it).  usage: python3 ksdump_gcheck.py <tsv> <stack> [args file]
import sys, os, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'w6'))
import numpy as np
TSV, ST = sys.argv[1], sys.argv[2]
import loadeng
from loadeng import load
import grammar as G, gext as X
HERE = os.path.dirname(os.path.abspath(__file__))
ns = load(ST, 'full', ['kstar', 'edgekeys=' + os.path.join(os.path.dirname(HERE), 'eng', 'edgekeys_r4.txt')]); ns['l3q_load'](); ns['kt_load']()
src = open(os.path.join(HERE, 'test_edge.py')).read()
exec(src[src.index('def pic('):src.index('rng = random.Random')])                                              # pic, ctx_of, gcols
KEYS = {k['name']: k for k in ns['EGKEYS']}; KEYS['K1'] = ns['eg_parse']('K1x EDGE(7->7)[S.L+1=B S.L-1=S S.L-2=5 S.L-3=5 S.A-1=B]'); KEYS['K1']['name'] = 'K1'
L = [l.rstrip('\n').split('\t') for l in open(TSV) if not l.startswith('#')]; H = L[0]; R = L[1:]
C = collections.Counter()
for d in sorted({int(r[0]) for r in R}):
    rows = [r for r in R if int(r[0]) == d]; n = len(rows)
    arrs = [([int(c) for c in r[1]], [int(c) for c in r[2]]) for r in rows]
    items = [(rid, sl) for rid, (w, s) in enumerate(arrs) for sl in X.slots(pic(d, w, s)) if sl[0] == 'EDGE']
    T = G.SlotTable(items).G['EDGE']
    for f_, key in KEYS.items():
        gp, gr = gcols(T, key, ctx_of(key), n)
        pn = np.array([int(r[H.index(f_ + '_pay_n')]) for r in rows]); rx = np.array([int(r[H.index(f_ + '_rec_x')]) for r in rows]); rn = np.array([int(r[H.index(f_ + '_rec_n')]) for r in rows])
        C[f_, 'rows'] += n; C[f_, 'pay_eq'] += int((pn == gp).sum()); C[f_, 'recx_eq'] += int((rx == gr).sum()); C[f_, 'rec_ge'] += int((rn >= gr).sum())
ok = all(C[f_, 'pay_eq'] == C[f_, 'rows'] and C[f_, 'recx_eq'] == C[f_, 'rows'] and C[f_, 'rec_ge'] == C[f_, 'rows'] for f_ in KEYS)
for f_ in KEYS: print('%s: %d rows; pay_n == grammar SURE on %d; rec_x == grammar POSSIBLE on %d; rec_n >= grammar on %d' % (f_, C[f_, 'rows'], C[f_, 'pay_eq'], C[f_, 'recx_eq'], C[f_, 'rec_ge']))
print('KSDUMP-GRAMMAR-CHECK: %s' % ('PASS' if ok else 'FAIL'))
