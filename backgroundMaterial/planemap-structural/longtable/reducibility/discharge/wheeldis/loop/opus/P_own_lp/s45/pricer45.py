# s45 l3qV pricer (RELAY_SPEC_s45 45.6): the V = 8 / 9 columns add columns only, so the engine's own lowerR2 (l3qV=7,8,9,
# V-tables restricted to the cert's payee keys, flag l3qpartial) prices them exactly against cert_q42aA78L.  Prints every new
# column with nonzero rc, the cert rows it touches, the bundle rc (lq + the lQ of every cert mask containing a2) and the
# first-order gains at caps 0.05 / 0.1.   python3 pricer45.py [CERT]
import os, sys, json, re, collections, itertools
from fractions import Fraction
B = '/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp'
E = B + '/s45/eng'; Q = B + '/s33z/reg_A78'; H = B + '/s39o'; T = B + '/s45/tabV'
M = '/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/P/m/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis'
CERT = sys.argv[1] if len(sys.argv) > 1 else B + '/s42a/run_A78/cert_q42aA78L.json'
ARGS = ['xon', 'apexcls', 'filt16', 'killtab=' + Q + '/f/kill/kill6', 'hat5', 'consall', 'l3q',
        'l3qtab=' + Q + '/tab_1.json,' + Q + '/tab_-1.json', 'lqcap=3', 'rpatN=' + H + '/rpatN3.txt',
        'l3qV=7,8,9', 'l3qtab8=%s/tabV8cert_1.json,%s/tabV8cert_-1.json' % (T, T), 'l3qtab9=%s/tabV9cert_1.json,%s/tabV9cert_-1.json' % (T, T), 'l3qpartial',
        'cert=' + CERT, 'xcap=3', 'root=' + M, 'args=' + Q + '/args_A78.txt', 'exname=' + B + '/s40f/exname_rm128.txt', 'rpat=' + B + '/rpatD.txt',
        'work=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/P/wr45_price']
sys.argv = [E + '/pcheck.py', 'none'] + ARGS
src = open(E + '/pcheck.py').read(); last = src.rstrip().rsplit('\n', 1)
G = {'__file__': E + '/pcheck.py', '__name__': 'pcheck_exec'}; exec(compile(last[0], E + '/pcheck.py', 'exec'), G)
assert G['LQVX'] == (8, 9)
p2 = open(E + '/prelay2.py').read()
f = re.search(r'\ndef cmd_lowerR2\(\):\n(.*?)\n(?=\S)', p2, re.S).group(0)
OLD = "    if neg: log('  negative reduced costs:', len(neg), neg[:5]); ok = False"
assert f.count(OLD) == 1
f = f.replace(OLD, "    NEG[:] = sorted(neg, key=lambda kv: kv[1]); TOT.update(tot); TCO[0] = tco\n" + OLD)
G['NEG'] = []; G['TOT'] = {}; G['TCO'] = [None]
exec(f, G); G['cmd_lowerR2']()
tco = G['TCO'][0]; TOT = G['TOT']
def rc(k): return -TOT.get(k, Fraction(0)) / tco
def new(k): return k[0] in ('lq', 'lQ') and len(k[1]) == 4
C = json.load(open(CERT))
R58 = {('8665556', '7675865'): 'r58c', ('8665566', '6765765'): 'r58g', ('7766556', '6567568'): 'r58b'}
rows = []
for c in C:
    r = c['row']; w = Fraction(c['w']).limit_denominator(10 ** 7)
    if r[0] == 'receiverR2':
        cf = G['recv_coef_R2'](int(r[1]), r[2], r[3], True)
        rows.append((w, 'R %s %s/%s%s' % (r[1], r[2], r[3], ' (' + R58[(r[2], r[3])] + ')' if (r[2], r[3]) in R58 else ''), cf))
    elif r[0] == 'cons2':
        cf = G['cons2_coef'](tuple(r[1]), tuple(r[2])); assert not any(new(k) for k in cf)
other_neg = [(k, v) for k, v in G['NEG'] if not new(k)]
print('\nl3qV=7,8,9 against %s (tco %s): other negative uncapped columns %d %s' % (os.path.basename(CERT), tco, len(other_neg), other_neg[:3]))
newk = sorted({k for _, _, cf in rows for k in cf if new(k) and cf[k]}, key=str)
lqall = [('lq', (V, c, a, a2)) for V in (8, 9) for c, a in itertools.product((5, 6), repeat=2) for a2 in (5, 6, 7, 8, 9)]
print('new columns in the family: lq %d (V = 8, 9); new keys with a coefficient in a cert row: %d' % (len(lqall), len(newk)))
lQin = [k for k in newk if k[0] == 'lQ']
def bundle(k):
    V, c, a, a2 = k[1]
    hit = [q for q in lQin if q[1][:3] == (V, c, a) and a2 in G['l3q_mask_letters'](q[1][3])]
    return rc(k) + sum(rc(q) for q in hit), hit
print('every new key in a cert row:')
for k in newk:
    hits = [(w, lab, cf[k]) for w, lab, cf in rows if cf.get(k)]
    extra = ''
    if k[0] == 'lq':
        b, hq = bundle(k); extra = ' | bundle rc %s (%+.6f) with %s' % (b, float(b), [q[1] for q in hq])
    print('  %s %s rc %s (%+.6f)%s\n      rows: %s' % (k[0], k[1], rc(k), float(rc(k)), extra, '; '.join('%s w=%s x%+d' % (lab, w, v) for w, lab, v in hits)))
negs = [k for k in lqall if rc(k) < 0]
print('NEGATIVE new lq columns: %d of %d' % (len(negs), len(lqall)))
print('NEGATIVE new lQ columns: %d (lQ rc < 0 would make the extended cert invalid outright)' % sum(1 for k in lQin if rc(k) < 0))
for cap in ('0.05', '0.1'):
    raw = sum(-rc(k) for k in negs) * Fraction(cap); bun = sum(max(Fraction(0), -bundle(k)[0]) for k in negs) * Fraction(cap)
    r58 = sum(-rc(k) for k in negs if any(cf.get(k) and '(r58' in lab for _, lab, cf in rows)) * Fraction(cap)
    r58b = sum(max(Fraction(0), -bundle(k)[0]) for k in negs if any(cf.get(k) and '(r58' in lab for _, lab, cf in rows)) * Fraction(cap)
    print('first-order gain at cap %s: raw all %.6f (r58-touching %.6f); bundle all %.6f (r58-touching %.6f)' % (cap, float(raw), float(r58), float(bun), float(r58b)))
for w, lab, cf in rows:
    if '(r58' in lab: print('r58 row %s w=%s: new keys %s' % (lab, w, [(k[1], v, str(rc(k))) for k, v in cf.items() if new(k) and v]))
