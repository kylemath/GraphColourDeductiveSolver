"""Trace explore's s52r1 / s52r2 f-names (0c2d546e) to Studio's own Job 52 row 1 / row 2 two-engine kill windows (e2cb4e69).
A name traces when f-name == Studio kill a-name with the u marker dropped, and for C when explore's kc X and cfast X both
equal the X in Studio's kills line (same frame, same vertex numbering). Everything else is written to untraced.txt
(with its kc line) for a Studio re-run on both engines.
Usage: python3 out/job30/s52r12/trace.py"""
import os, re, collections
HERE = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
K47 = os.path.join(HERE, 'loop', 'k47'); J52 = os.path.join(HERE, 'out', 'job52'); OUT = os.path.dirname(os.path.abspath(__file__))
mine = {}
for rd in ('row_8_86555665_56586665', 'row_8_86555665_56576665'):
    for l in open(os.path.join(J52, rd, 'kills.txt')):
        f = l.split(); a = f[0]; fn = 'f' + a[1:].replace('_u', '_', 1)
        x = re.search(r'X=\{([^}]*)\}', l)
        mine.setdefault(fn, set()).add(('D', None) if f[1] == 'D' else ('C', frozenset(e.strip() for e in x.group(1).split(','))))
def xs(s): return frozenset(e.strip() for e in s.split(','))
names = {}; verd = {}
for r in ('1', '2'):
    for l in open(os.path.join(K47, 's52r%s_kills.txt' % r)):
        if l.strip(): names.setdefault(l.split()[0], l.rstrip('\n'))
    cur = None
    for l in open(os.path.join(K47, 's52r%s_kills_kc.out' % r)):
        m = re.match(r'^([epf]\d+_\S+) r=\d+ ', l)
        if m: cur = m.group(1); verd.setdefault(cur, {'kD': False, 'kX': set(), 'dD': False, 'cX': set()}); verd[cur]['kD'] |= 'D=true' in l; continue
        mx = re.search(r'C-REDUCIBLE X=\{([^}]*)\}', l) or re.match(r'^\s+X=\{([^}]*)\} adm=yes leftover 0\b', l)
        if cur and mx: verd[cur]['kX'].add(xs(mx.group(1)))
    for l in open(os.path.join(K47, 's52r%s_kills_df.out' % r)):
        m = re.match(r'^([epf]\d+_\S+) r=\d+ ', l)
        if m and 'D=true' in l: verd.setdefault(m.group(1), {'kD': False, 'kX': set(), 'dD': False, 'cX': set()})['dD'] = True
    cur = None
    for l in open(os.path.join(K47, 's52r%s_kills_cf.cfast' % r)):
        m = re.match(r'^([epf]\d+_\S+) r=\d+ ', l)
        if m: cur = m.group(1); continue
        mf = re.search(r'fixed X=\{([^}]*)\} .*C-REDUCIBLE, leftover bad classes extending after contraction = 0$', l)
        if cur and mf: verd.setdefault(cur, {'kD': False, 'kX': set(), 'dD': False, 'cX': set()})['cX'].add(xs(mf.group(1)))
cnt = collections.Counter(); unt = []
for n in sorted(names):
    v = verd.get(n, {'kD': False, 'kX': set(), 'dD': False, 'cX': set()}); m = mine.get(n, set())
    eD = v['kD'] and v['dD']; eC = v['kX'] & v['cX']
    if eD and ('D', None) in m: cnt['D traced'] += 1
    elif not eD and eC and any(k == 'C' and x in eC for k, x in m): cnt['C traced (same X)'] += 1
    else: cnt['untraced ' + ('D' if eD else 'C' if eC else 'one-engine')] += 1; unt.append(names[n])
open(os.path.join(OUT, 'untraced.txt'), 'w').write(''.join(l + '\n' for l in unt))
print('distinct f-names %d (row 1 + row 2 deduped); %s' % (len(names), dict(cnt)))
# second pass: D names traced up to rotation / reflection (the dihedral images used by out/job30/matchtest.py) to a
# Studio D kill window; untraced2.txt = what still needs a Studio re-run
def images(fn):
    f = fn.split('_'); d = int(f[0][1:]); w, s = f[1], f[2]; out = set()
    for refl in (0, 1):
        for r in range(d):
            W = ['.'] * d; S_ = ['.'] * d
            for i in range(d):
                jw = (d - i) % d if refl else i; js = (2 * d - i - 1) % d if refl else i
                W[(jw + r) % d] = w[i]; S_[(js + r) % d] = s[i]
            out.add('%s_%s_%s' % (f[0], ''.join(W), ''.join(S_)))
    return out
myD = {n for n, m in mine.items() if ('D', None) in m}; myDimg = {x for n in myD for x in images(n)}
unt2 = []; c2 = collections.Counter()
for l in unt:
    n = l.split()[0]; v = verd.get(n, {'kD': False, 'kX': set(), 'dD': False, 'cX': set()})
    if v['kD'] and v['dD'] and n in myDimg: c2['D traced up to symmetry'] += 1
    else: c2['still untraced'] += 1; unt2.append(l)
open(os.path.join(OUT, 'untraced2.txt'), 'w').write(''.join(l + '\n' for l in unt2))
print('second pass: %s' % dict(c2))
