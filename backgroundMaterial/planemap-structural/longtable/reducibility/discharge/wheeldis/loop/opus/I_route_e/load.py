"""I_route_e: load the 7/27 y (out/wlp3_j28_13.txt) and sep3's c-check, as k36/w2load.py, with sep3's input file
written to this folder's bin/.  import: from load import yv, ix, root, roots, check, isR5, isR6"""
import sys, os, re
I = os.path.dirname(os.path.abspath(__file__)); WD = os.path.normpath(os.path.join(I, '..', '..', '..'))
cwd = os.getcwd(); os.chdir(WD)
YF = os.path.join(WD, 'out', 'wlp3_j28_13.txt')
hdr = open(YF).readline().split()
args = [a for a in hdr[2:] if a == 'w7plus' or (a.startswith(('pat=', 'cpat=')) and os.path.exists(a.split('=', 1)[1]))]
args += ['pat=loop/n9/win%s.out' % x for x in ('9', '25', '25b', '27', '29', '31')] + ['tag=i_route_e']
src = open(os.path.join(WD, 'wlp3.py')).read()
src = src.replace("os.path.join(HERE, 'bin'", "os.path.join(%r" % os.path.join(I, 'bin'))
G = {'__file__': os.path.join(WD, 'wlp3.py'), '__name__': 'wlp3x'}
sv_ = sys.argv; sys.argv = ['wlp3'] + args
exec(src[:src.index('A_ub, b_ub = [], []')], G); sys.argv = sv_
roots, ix, root, isR5, isR6, SEP = G['roots'], G['ix'], G['root'], G['isR5'], G['isR6'], G['SEP']
def check(d, lk, sv):
    SEP.stdin.write('c %d %s %s\n' % (d, lk, sv)); SEP.stdin.flush(); return SEP.stdout.readline().strip() == '1'
yv = [0.0] * len(roots); ny = 0
for line in open(YF):
    m = re.match(r'^\s+(\d)\|(\d{4})\s+([\d.]+)\s*$', line)
    if m:
        r = (int(m.group(1)),) + tuple(int(c) for c in m.group(2)); yv[ix[r]] = float(m.group(3)); ny += 1
os.chdir(cwd)
def Y(w): return yv[ix[root(list(w), 0)]]
