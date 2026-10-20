# s44 fb pricer (RELAY_SPEC_s44 44.6): fb adds columns only, so the engine's own lowerR2 (flag fb, fbdir=ARG) prices them
# exactly against cert_q39n3A74L.  Prints every negative column and the cert rows (receiverR2 / cons2) it touches.
#   python3 pricer44.py 6|7|67
import os, sys, json, re, collections
from fractions import Fraction
DIR = sys.argv[1]
B = '/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp'
E = B + '/s44/eng'; Q = B + '/s33z/reg_A74'; H = B + '/s39o'
M = '/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/P/m/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis'
CERT = H + '/run_n3_A74/cert_q39n3A74L.json'
ARGS = ['xon', 'apexcls', 'filt16', 'killtab=' + Q + '/f/kill/kill6', 'hat5', 'consall', 'l3q',
        'l3qtab=' + Q + '/tab_1.json,' + Q + '/tab_-1.json', 'lqcap=3', 'rpatN=' + H + '/rpatN3.txt', 'fb', 'fbdir=' + DIR,
        'cert=' + CERT, 'xcap=3', 'root=' + M, 'args=' + Q + '/args_A74.txt', 'rpat=' + B + '/rpatD.txt',
        'work=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/P/wr44_price' + DIR]
sys.argv = [E + '/pcheck.py', 'none'] + ARGS
src = open(E + '/pcheck.py').read(); last = src.rstrip().rsplit('\n', 1)
G = {'__file__': E + '/pcheck.py', '__name__': 'pcheck_exec'}; exec(compile(last[0], E + '/pcheck.py', 'exec'), G)
assert G['FB'] and G['FBDIR'] == DIR
p2 = open(E + '/prelay2.py').read()
f = re.search(r'\ndef cmd_lowerR2\(\):\n(.*?)\n(?=\S)', p2, re.S).group(0)
OLD = "    if neg: log('  negative reduced costs:', len(neg), neg[:5]); ok = False"
assert f.count(OLD) == 1
f = f.replace(OLD, "    NEG[:] = sorted(neg, key=lambda kv: kv[1]); TOT.update(tot); TCO[0] = tco\n" + OLD)
G['NEG'] = []; G['TOT'] = {}; G['TCO'] = [None]
exec(f, G); G['cmd_lowerR2']()
NEG = [(k, rc) for k, rc in G['NEG'] if k[0] == 'fb']; other = [(k, rc) for k, rc in G['NEG'] if k[0] != 'fb']
C = json.load(open(CERT)); tco = G['TCO'][0]
FACE = {('7766556', '6567566'), ('7766556', '6566576'), ('7766556', '6576576'), ('7665566', '6675676'), ('7665566', '6775676')}
rows = []
for c in C:
    r = c['row']; w = Fraction(c['w']).limit_denominator(10 ** 7)
    if r[0] == 'receiverR2': rows.append((w, 'R %s %s %s' % tuple(r[1:4]), G['recv_coef_R2'](int(r[1]), r[2], r[3], True), (r[2], r[3]) in FACE))
    elif r[0] == 'cons2': rows.append((w, 'C %s %s' % (''.join(map(str, r[1])), ''.join(map(str, r[2]))), G['cons2_coef'](tuple(r[1]), tuple(r[2])), False))
fbk = sorted({k for _, _, cf, _ in rows for k in cf if k[0] == 'fb' and cf[k]}, key=str)
print('\nfb (fbdir=%s) against %s: fb keys in cert rows %d; negative fb columns %d; other negative columns %d %s' % (DIR, os.path.basename(CERT), len(fbk), len(NEG), len(other), other[:3]))
def rc(k): return -G['TOT'].get(k, 0) / tco
face_neg = 0; sneg = Fraction(0); sface = Fraction(0)
for k, r_ in NEG:
    hits = [(w, lab, cf[k], fc) for w, lab, cf, fc in rows if cf.get(k)]
    tf = any(h[3] for h in hits); face_neg += tf; sneg += -r_; sface += -r_ if tf else 0
    print('  rc %s = %+.6f (%+.2f/183)  fb%s %s %s | %s' % (r_, float(r_), float(r_) * 183, '6' if k[1][1] == 6 else '7', k[1], 'TOUCHES-FACE' if tf else '-',
          '; '.join('%s w=%s x%+d%s' % (lab, w, v, ' FACE' if fc else '') for w, lab, v, fc in hits)))
print('every fb key in a cert row, with rc and rows:')
for k in fbk:
    hits = [(w, lab, cf[k], fc) for w, lab, cf, fc in rows if cf.get(k)]
    print('  %s rc %s | %s' % (k[1], rc(k), '; '.join('%s w=%s x%+d%s' % (lab, w, v, ' FACE' if fc else '') for w, lab, v, fc in hits)))
for w, lab, cf, fc in rows:
    if fc: print('FACE row %s: fb keys %s' % (lab, [(k[1], v, str(rc(k))) for k, v in cf.items() if k[0] == 'fb' and v]))
print('KILL LINE (fbdir=%s): %s; negative fb columns touching a face row: %d of %d' % (DIR, 'PASSED' if face_neg else 'NOT passed', face_neg, len(NEG)))
for cap in ('0.05', '0.1'):
    print('first-order gain at cap %s: all fb %.6f, face-touching fb %.6f' % (cap, float(sneg * Fraction(cap)), float(sface * Fraction(cap))))
