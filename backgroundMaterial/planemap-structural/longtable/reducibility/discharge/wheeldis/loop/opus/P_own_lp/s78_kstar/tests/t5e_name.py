# s78 test 5 (generic EDGE): every violated row of the planted run (vfile: d load excess link apexes), its A1 coefficient from the engine,
# the payers (link 7s at j, orientation e, whose window bound credits the row), and the row value with A1 = 0 (rows are linear in A1),
# which must be <= d - 6 + t: A1 alone causes each violation.   usage: python3 t5e_name.py vfile amount t stack
import sys, os, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from loadeng import load
VF, AM, T0, ST = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), sys.argv[4]
ns = load(ST, 'full', ['edgekeys=' + os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'eng', 'edgekeys_r4.txt')]); ns['l3q_load'](); ns['kt_load']()
key = [k for k in ns['EGKEYS'] if k['name'] == 'A1'][0]
C = collections.Counter(); ex = {}
for l in open(VF):
    if not l.strip(): continue
    d, val, exc, lk, sv = l.split(); d = int(d); w = [int(c) for c in lk]; s = [int(c) for c in sv]
    cf = ns['eg_terms'](d, w, s).get(('ks', 'A1'), 0); U = min(d, 9); Tb = ns['eg_tables'](key, U)
    pay = [(j, e) for j in range(d) if w[j] == 7 for ei, e in ((0, 1), (1, -1)) if Tb[ei][ns['eg_widx'](w, s, j)]]
    v0 = float(val) - AM * cf
    C[d, 'rows'] += 1; C[d, 'pos'] += cf > 0; C[d, 'v0ok'] += v0 <= d - 6 + T0 + 1e-9
    if d not in ex: ex[d] = 'R %d %s %s: value %.9f (excess %s), A1 coefficient %+d, credited by the payers (link index j, orientation e) %s, value at A1 = 0: %.9f (<= %.9f)' % (d, lk, sv, float(val), exc, cf, pay, v0, d - 6 + T0)
for d in sorted({k[0] for k in C}):
    print('d=%d: %d violated rows named; A1 coefficient > 0 on %d; value at A1 = 0 <= d-6+t on %d' % (d, C[d, 'rows'], C[d, 'pos'], C[d, 'v0ok']))
    print('   e.g. ' + ex[d])
