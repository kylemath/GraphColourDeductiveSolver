"""EXPLORE round 9 (exploratory): H-R1 oracle for a 5 -> 6 -> big rule.  Reads the certificate receivers (positive dual)
of wlp3 outputs and classifies each arrangement:
  lone five w_i: w_i = 5, w_i-1, w_i+1, s_i-1, s_i in {5, 6} (u is its only big neighbour);
  second-ring route: a 6-neighbour of w_i has a neighbour at distance <= 2 from u, not adjacent to w_i, that is big or
  left open by the letters.  A link 6 always has one (its p slot); an s_i = 6 between two fives reaches s_i+1 (big?).
  'routed': at least one lone five, and every lone five has a route.  'unrouted': some lone five has none.
  'plain': no lone five.
With out=FILE, writes every routed certificate arrangement as a full f<d>_ pattern line (D=true, oracle only: these are
NOT reducible configurations) so wlp3s can be rerun as if the rule relieved them completely (optimistic for H-R1).
Usage: python3 hr1_oracle.py WLP3_OUT... [out=FILE]"""
import sys, re
OUT = next((a[4:] for a in sys.argv[1:] if a.startswith('out=')), None)
files = [a for a in sys.argv[1:] if not a.startswith('out=')]
big = lambda c: c in '789'

def classify(d, lk, sv):
    lone, unrouted = [], []
    for i in range(d):
        if lk[i] != '5': continue
        nb = (lk[(i - 1) % d], lk[(i + 1) % d], sv[(i - 1) % d], sv[i])
        if not all(c in '56' for c in nb): continue
        lone.append(i)
        r = lk[(i - 1) % d] == '6' or lk[(i + 1) % d] == '6'
        r = r or (sv[i] == '6' and lk[(i + 1) % d] == '5' and big(sv[(i + 1) % d]))
        r = r or (sv[(i - 1) % d] == '6' and lk[(i - 1) % d] == '5' and big(sv[(i - 2) % d]))
        if not r: unrouted.append(i)
    kind = 'plain' if not lone else ('unrouted' if unrouted else 'routed')
    return kind, lone, unrouted

def fname(d, lk, sv):
    m = {'9': 'B'}
    return 'f%d_%s_%s' % (d, ''.join(m.get(c, c) for c in lk), ''.join(m.get(c, c) for c in sv))

routed = []
for fn in files:
    t = None
    for line in open(fn):
        if line.startswith('t*') or line.startswith('t ='): t = line.strip()
        m = re.match(r'\s+([\d.]+)\s+receiver d=(\d+) link (\S+) s (\S+),', line)
        if not m: continue
        dv, d, lk, sv = float(m.group(1)), int(m.group(2)), m.group(3), m.group(4)
        kind, lone, un = classify(d, lk, sv)
        print('%s  %.4f d=%d link %s s %s  %s lone=%s unrouted=%s' % (fn.split('/')[-1], dv, d, lk, sv, kind, lone, un))
        if kind == 'routed': routed.append(fname(d, lk, sv))
if OUT:
    open(OUT, 'a').write(''.join('%s D=true oracle-H-R1\n' % n for n in sorted(set(routed))))
    print('appended', len(set(routed)), 'routed arrangements to', OUT)
