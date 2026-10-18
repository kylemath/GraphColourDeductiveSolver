"""EXPLORE round 40 (Long Table's request, 10:12Z): validation set for kc -C2 restricted to cfast X's that put two ring
vertices in one X-component.  Every cfast output in the registry (out/, job27/, loop/, except round 37/38's own kill
files k37/cwin.cfast and k38/kills.cfast), configurations not D, whose working X (C) or best X (not C) has such a
component, with an input line found in the wheeldis *.txt files and ring <= RMAX.  Writes val2.txt, val2_x.txt,
val2_ref.txt.  usage: python3 mkval2.py RMAX"""
import os, glob, re, sys, collections
W = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RMAX = int(sys.argv[1])
def tworing(x):
    par = {}
    def f(a):
        par.setdefault(a, a)
        while par[a] != a: par[a] = par[par[a]]; a = par[a]
        return a
    for e in x.strip('{}').split(','):
        a, b = e.split('-'); par[f(a)] = f(b)
    C = collections.Counter(f(v) for v in list(par) if v.startswith('R'))
    return any(c >= 2 for c in C.values())
skip = {os.path.join(W, 'loop', 'k37', 'cwin.cfast'), os.path.join(W, 'loop', 'k38', 'kills.cfast')}
files = sorted(set(glob.glob(os.path.join(W, 'out', '**', '*.cfast'), recursive=True) + glob.glob(os.path.join(W, 'job27', '*.cfast'))
                   + glob.glob(os.path.join(W, 'loop', '**', '*.cfast'), recursive=True)) - skip)
ref = {}
for fn in files:
    cur = None
    for line in open(fn, errors='replace'):
        if ' r=' in line and not line.startswith(' '):
            cur = line.split()[0]; m = re.search(r' r=(\d+)', line)
            if cur not in ref: ref[cur] = {'src': os.path.relpath(fn, W), 'C': None, 'X': None, 'best': None, 'left': None, 'D': 'D=true' in line, 'r': int(m.group(1))}
            else: cur = None          # first occurrence only
        elif cur and 'C-REDUCIBLE' in line and ref[cur]['X'] is None:
            ref[cur]['C'] = True; ref[cur]['X'] = re.search(r'X=(\{[^}]*\})', line).group(1)
        elif cur and 'search |X|' in line:
            m = re.search(r'best X=(\{[^}]*\}) leftover (\d+)', line)
            if ref[cur]['C'] is None: ref[cur]['C'] = False
            if m: ref[cur]['best'] = m.group(1); ref[cur]['left'] = int(m.group(2))
want = {nm for nm, r in ref.items() if not r['D'] and r['C'] is not None and r['r'] <= RMAX and
        ((r['C'] and tworing(r['X'])) or (not r['C'] and r['best'] and tworing(r['best'])))}
cfg = {}
for fn in glob.glob(os.path.join(W, '**', '*.txt'), recursive=True):
    try:
        for line in open(fn):
            f = line.split()
            if len(f) == 5 and f[0] in want and f[0] not in cfg and f[1].isdigit(): cfg[f[0]] = line.strip()
    except (UnicodeDecodeError, IsADirectoryError): pass
keep = sorted((nm for nm in want if nm in cfg), key=lambda n: (ref[n]['r'], n))
with open('val2.txt', 'w') as f:
    for nm in keep: f.write(cfg[nm] + '\n')
with open('val2_x.txt', 'w') as f:
    for nm in keep: f.write('%s %s\n' % (nm, ref[nm]['X'] if ref[nm]['C'] else ref[nm]['best']))
with open('val2_ref.txt', 'w') as f:
    for nm in keep:
        r = ref[nm]; f.write('%s %s r=%d C=%s X=%s leftover=%s\n' % (nm, r['src'], r['r'], r['C'], r['X'] if r['C'] else r['best'], 0 if r['C'] else r['left']))
print('cfast files', len(files), 'entries', len(ref), 'two-ring X at ring <= %d' % RMAX, len(want), 'with input line', len(keep),
      'C', sum(1 for n in keep if ref[n]['C']), 'not C', sum(1 for n in keep if not ref[n]['C']),
      'rings', sorted(collections.Counter(ref[n]['r'] for n in keep).items()))
