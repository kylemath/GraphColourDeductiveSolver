# s44: diagnose a lowerR2 run: every negative reduced cost (family, size), via the engine's own cmd_lowerR2.
#   python3 lowchk44.py REG CERT [extra engine args...]
import sys, re, collections
REG, CERT = sys.argv[1], sys.argv[2]; EXTRA = sys.argv[3:]
B = '/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp'
E = B + '/s44/eng'; Q = B + '/s33z/reg_' + REG; H = B + '/s39o'
M = '/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/P/m/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis'
ARGS = ['xon', 'apexcls', 'filt16', 'killtab=' + Q + '/f/kill/kill6', 'hat5', 'consall', 'l3q', 'l3qtab=' + Q + '/tab_1.json,' + Q + '/tab_-1.json',
        'lqcap=3', 'rpatN=' + H + '/rpatN3.txt', 'cert=' + CERT, 'xcap=3', 'root=' + M, 'args=' + Q + '/args_%s.txt' % REG, 'rpat=' + B + '/rpatD.txt',
        'exname=' + B + '/s40f/exname_rm128.txt', 'work=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/P/wr44_low'] + EXTRA
sys.argv = [E + '/pcheck.py', 'none'] + ARGS
src = open(E + '/pcheck.py').read(); last = src.rstrip().rsplit('\n', 1)
G = {'__file__': E + '/pcheck.py', '__name__': 'pcheck_exec'}; exec(compile(last[0], E + '/pcheck.py', 'exec'), G)
p2 = open(E + '/prelay2.py').read()
f = re.search(r'\ndef cmd_lowerR2\(\):\n(.*?)\n(?=\S)', p2, re.S).group(0)
OLD = "    if neg: log('  negative reduced costs:', len(neg), neg[:5]); ok = False"
f = f.replace(OLD, "    NEG[:] = sorted(neg, key=lambda kv: kv[1]); TOT.update(tot); TCO[0] = tco; DD_[0] = D\n" + OLD)
G['NEG'] = []; G['TOT'] = {}; G['TCO'] = [None]; G['DD_'] = [None]
exec(f, G); G['cmd_lowerR2']()
NEG = G['NEG']
fam = collections.defaultdict(list)
for k, rc in NEG: fam[k[0]].append(float(rc))
print('negative columns by family:', {k: (len(v), min(v), max(v)) for k, v in fam.items()})
print('sum of |rc| over negatives: %.3e; worst %.3e' % (sum(-float(r) for _, r in NEG), min([float(r) for _, r in NEG] or [0])))
print('D (lower bound before the negative columns) = %.12f' % float(G['DD_'][0]))
