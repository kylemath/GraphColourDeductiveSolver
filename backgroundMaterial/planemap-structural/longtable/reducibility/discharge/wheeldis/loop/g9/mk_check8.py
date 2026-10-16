"""G9 (exploratory): writes loop/g9/defect_check2_8.py = WD/defect_check2.py with (1) HERE pinned to WD, (2) verdict files
also read from loop/g9 (g9_*.out dfast, g9_*.cfast), (3) receivers u of degree 7 AND 8 (receiver-centred configurations
at an 8 use the same e8_ keys / g / b hashes), (4) 8-wheel status from c8_ lines (D kills, untested -> open 'untested8',
listed in NEWCFG.w8 as dfast input), (5) a per-candidate list of every wheel with a letter 8 (or centre 8) whose
reducibility was never tested (counted NOT reducible by the search)."""
import os
WD = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
s = open(os.path.join(WD, 'defect_check2.py')).read()
def rep(a, b, cnt=1):
    global s
    assert s.count(a) == cnt, (a, s.count(a)); s = s.replace(a, b)
rep('"""Graph-based receiver-centred check', '"""[G9 copy, see loop/g9/mk_check8.py: receivers of degree 7 and 8, 8-wheels, loop/g9 verdicts]\nGraph-based receiver-centred check')
rep("HERE = os.path.dirname(os.path.abspath(__file__)); DIS = os.path.dirname(HERE)",
    "HERE = %r; DIS = os.path.dirname(HERE); G9 = os.path.join(HERE, 'loop', 'g9')" % WD)
rep("for fn in glob.glob(os.path.join(HERE, 'out', 'def_*.out')):\n",
    "for fn in glob.glob(os.path.join(HERE, 'out', 'def_*.out')) + glob.glob(os.path.join(G9, 'g9_*.dfast.out')):\n")
rep("for fn in glob.glob(os.path.join(HERE, 'job27', '*.cfast')) + glob.glob(os.path.join(HERE, 'out', 'def_*.cfast')):",
    "for fn in glob.glob(os.path.join(HERE, 'job27', '*.cfast')) + glob.glob(os.path.join(HERE, 'out', 'def_*.cfast')) + glob.glob(os.path.join(G9, 'g9_*.cfast')):")
# TESTED (gen.py registry) only reads out/*.out: add loop/g9 dfast outputs for e/p names
rep("_bw = open(os.path.join(HERE, 'bigwheels.py')).read()",
    """for fn in glob.glob(os.path.join(G9, 'g9_*.dfast.out')):
    for line in open(fn):
        f = line.split()
        if f and re.match(r'^[ep]\\d+_', f[0]) and ('D=true' in line or 'D=false' in line):
            TESTED[key_of_name(f[0])] = 'D' if 'D=true' in line else 'notD'
T8 = {}
for fn in ['bigwheels_dfast.out', 'bigwheels1516_dfast_partial.out']:
    for line in open(os.path.join(HERE, 'out', fn)):
        f = line.split()
        if f and f[0].startswith('c8_') and ('D=true' in line or 'D=false' in line): T8[tuple(map(int, f[0][3:]))] = 'D' if 'D=true' in line else 'notD'
for fn in glob.glob(os.path.join(G9, 'g9_*.dfast.out')):
    for line in open(fn):
        f = line.split()
        if f and f[0][:3] in ('c7_', 'c8_') and ('D=true' in line or 'D=false' in line):
            (T7 if f[0][:3] == 'c7_' else T8)[tuple(map(int, f[0][3:]))] = 'D' if 'D=true' in line else 'notD'
# wheels with a letter 8 that the search counted not reducible: tested sets
R5W = {}; 
for line in open(os.path.join(DIS, 'studio17', 'wheels17_verdicts.txt')):
    if line.startswith('#'): continue
    f = line.split(); R5W[tuple(map(int, f[0].split('_')[1]))] = f[2]
_bw = open(os.path.join(HERE, 'bigwheels.py')).read()""")
# T7 also from loop/g9 handled above (must come after T7 defined: T7 is defined before _bw) -- check order
rep("        if u in outer or deg.get(u) != 7: continue\n        lk = rotf(nxt, u); d = len(lk)\n        cw = canon([deg[x] for x in lk]); w7 = T7.get(cw)\n        if w7 == 'D': st['D'] += 1\n        elif w7 is None: st['untested7'] += 1; need.append(('w7', cw))\n",
    "        if u in outer: continue\n"
    "        lkw_ = [deg.get(x) for x in rotf(nxt, u)]\n"
    "        if deg.get(u) in (5, 6) and None not in lkw_ and 8 in lkw_:\n"
    "            cw = canon(lkw_)\n"
    "            if deg[u] == 6 or cw not in R5W: st['unt8_%d_%s' % (deg[u], ''.join(map(str, cw)))] += 1\n"
    "        if deg.get(u) not in (7, 8): continue\n        lk = rotf(nxt, u); d = len(lk)\n        cw = canon([deg[x] for x in lk]); w7 = (T7 if d == 7 else T8).get(cw)\n"
    "        if d == 8 or 8 in cw:\n"
    "            if w7 is None: st['unt8_%d_%s' % (d, ''.join(map(str, cw)))] += 1\n"
    "        if w7 == 'D': st['D'] += 1\n        elif w7 is None and d == 8: st['untested8'] += 1; need.append(('w8', cw))\n        elif w7 is None: st['untested7'] += 1; need.append(('w7', cw))\n        elif d == 8: pass\n")
rep("    elif st['untestedD'] or st['untestedC'] or st['untested7'] or",
    "    elif st['untestedD'] or st['untestedC'] or st['untested7'] or st['untested8'] or")
rep("    summ = collections.Counter(); needD = {}; needC = {}; need7 = set(); out = []",
    "    summ = collections.Counter(); needD = {}; needC = {}; need7 = set(); need8 = set(); out = []")
rep("                else: need7.add(x[1])", "                elif x[0] == 'w8': need8.add(x[1])\n                else: need7.add(x[1])")
rep("    print('to test (from candidates not yet killed): dfast %d, cfast %d, 7-wheels %d' % (len(needD), len(needC), len(need7)))",
    """    fmt_ = lambda L: ';'.join(','.join(map(str, v)) if v else '-' for v in L)
    with open(NEWF + '.w78', 'w') as fo:
        for nm_, ws in (('c7_', need7), ('c8_', need8)):
            for w_ in sorted(ws):
                r_, m_, ra_, ia_ = wheel(list(w_)); fo.write('%s%s %d %d %s %s\\n' % (nm_, ''.join(map(str, w_)), r_, m_, fmt_(ra_), fmt_(ia_)))
    print('to test (from candidates not yet killed): dfast %d, cfast %d, 7-wheels %d, 8-wheels %d' % (len(needD), len(needC), len(need7), len(need8)))""")
rep("C7 = set(); NC7 = set()\nfor fn in glob.glob(os.path.join(HERE, 'out', 'def_*.cfast')):",
    "C7 = set(); NC7 = set()\nfor fn in glob.glob(os.path.join(HERE, 'out', 'def_*.cfast')) + glob.glob(os.path.join(G9, 'g9_*.cfast')):")
rep("        if w7 == 'D': st['D'] += 1\n        elif w7 is None and d == 8:", "        if w7 == 'D': st['D'] += 1; st['W%dD' % d] += 1\n        elif w7 is None and d == 8:")
rep("        elif STRICT7 and cw in C7: st['C7'] += 1", "        elif STRICT7 and cw in C7: st['C7'] += 1; st['W7C'] += 1")
rep("                        if db == 'D': st['bfD'] += 1", "                        if db == 'D': st['bfD'] += 1; st['bfD@%d' % d] += 1")
rep("                        elif cbv == 'C': st['bfC'] += 1", "                        elif cbv == 'C': st['bfC'] += 1; st['bfC@%d' % d] += 1")
rep("                if dv == 'D': st['D'] += 1", "                if dv == 'D': st['D'] += 1; st['rcD@%d' % d] += 1")
rep("                elif cv == 'C': st['C'] += 1", "                elif cv == 'C': st['C'] += 1; st['rcC@%d' % d] += 1")
rep("                    if cfg is None: st['nosimple'] += 1; continue", "                    if cfg is None: st['nosimple'] += 1; st['nosimple@%d' % d] += 1; continue")
rep("                    if cb is None: st['bf_nosimple'] += 1", "                    if cb is None: st['bf_nosimple'] += 1; st['bf_nosimple@%d' % d] += 1")
open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'defect_check2_8.py'), 'w').write(s)
print('ok')
