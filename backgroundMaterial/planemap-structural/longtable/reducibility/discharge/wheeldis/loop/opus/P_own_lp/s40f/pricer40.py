# s40f fy pricer (Opus). Prices the fy columns z[fykey] (s25c fy, RELAY_SPEC_s20 level 1; port s35f/fyq/port_fy.py)
# against the l3q + rpatN3 A74 cert s39o/run_n3_A74/cert_q39n3A74L.json, using the s40f engine with fy ON.
# Runs the engine's own cmd_lowerR2 (rows re-derived from labels) with the neg[:5] print widened to the full sorted list,
# then reports, for every negative column, its coefficient in each cert receiverR2 row (the 4 A74 face binders flagged).
import os, sys, json, re
from fractions import Fraction
B = '/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp'
E = B + '/s40f/eng'; Q = B + '/s33z/reg_A74'; H = B + '/s39o'
M = '/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/P/m/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis'
CERT = H + '/run_n3_A74/cert_q39n3A74L.json'
ARGS = ['xon', 'apexcls', 'filt16', 'killtab=' + Q + '/f/kill/kill6', 'hat5', 'consall', 'l3q',
        'l3qtab=' + Q + '/tab_1.json,' + Q + '/tab_-1.json', 'lqcap=3', 'rpatN=' + H + '/rpatN3.txt', 'fy',
        'cert=' + CERT, 'xcap=3', 'root=' + M, 'args=' + Q + '/args_A74.txt', 'rpat=' + B + '/rpatD.txt',
        'work=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/P/wr40_ctlfy']
sys.argv = [E + '/pcheck.py', 'none'] + ARGS
src = open(E + '/pcheck.py').read(); last = src.rstrip().rsplit('\n', 1); assert "'lowerR2': cmd_lowerR2" in last[1]
G = {'__file__': E + '/pcheck.py', '__name__': 'pcheck_exec'}; exec(compile(last[0], E + '/pcheck.py', 'exec'), G)
assert G['FY'] and G['ZH'] and not G['ZR']
p2 = open(E + '/prelay2.py').read()
f = re.search(r'\ndef cmd_lowerR2\(\):\n(.*?)\n(?=\S)', p2, re.S).group(0)
OLD = "    if neg: log('  negative reduced costs:', len(neg), neg[:5]); ok = False"
assert f.count(OLD) == 1
f = f.replace(OLD, "    NEG[:] = sorted(neg, key=lambda kv: kv[1]); TOT.update(tot); TCO[0] = tco\n" + OLD)
G['NEG'] = []; G['TOT'] = {}; G['TCO'] = [None]
exec(f, G); G['cmd_lowerR2']()
NEG = G['NEG']; C = json.load(open(CERT))
FACE = {('7766556', '6567566'), ('7766556', '6566576'), ('7766556', '6576576'), ('7665566', '6675676')}
recv = []
for c in C:
    r = c['row']
    if r[0] == 'receiverR2':
        cf = G['recv_coef_R2'](int(r[1]), r[2], r[3], True)
        recv.append((Fraction(c['w']).limit_denominator(10 ** 7), r[1:], cf, (r[2], r[3]) in FACE))
print('\nfy pricing against %s: %d negative columns (all kinds); by kind %s' % (os.path.basename(CERT), len(NEG),
      dict(__import__('collections').Counter(k[0] for k, _ in NEG))))
print('rank  rc  (exact)  key  | cert receiverR2 rows with nonzero coef (w, d link sword, coef) [FACE = one of the 4 A74 face binders]')
touch = 0
for i, (k, rc) in enumerate(NEG):
    hits = [(float(w), ' '.join(map(str, rr)), cf[k], fc) for w, rr, cf, fc in recv if cf.get(k)]
    tf = any(h[3] for h in hits); touch += tf
    print('%3d  %+.6f  %s  %s %s %s | %s' % (i + 1, float(rc), rc, k[0], str(k[1]), 'TOUCHES-FACE' if tf else '-',
          '; '.join('%.6f %s x%d%s' % (h[0], h[1], h[2], ' FACE' if h[3] else '') for h in hits) or 'no receiver row'))
print('negative columns touching a face binder: %d of %d' % (touch, len(NEG)))
for w, rr, cf, fc in recv:
    if fc: print('FACE row %s w=%.6f fy keys: %s' % (' '.join(map(str, rr)), float(w), sorted((k[1], v) for k, v in cf.items() if k[0] == 'z')))
