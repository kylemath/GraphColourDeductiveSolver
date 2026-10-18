"""EXPLORE round 35: kc-C validation set from cfast outputs (verdicts and X only; no cfast source read).
Reads the three pre-registered cfast files, finds each configuration's input line in the wheeldis *.txt files,
writes valc.txt (config lines), valc_x.txt (name X for cfast's working/best X) and valc_ref.txt (cfast's verdicts)."""
import os, glob, re
W = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FILES = ['job27/k2a.cfast', 'out/job28/r_12.cfast', 'out/def_r1.cfast']
ref = {}; order = []
for fn in FILES:
    cur = None
    for line in open(os.path.join(W, fn)):
        if ' r=' in line and not line.startswith(' '):
            cur = line.split()[0]
            if cur not in ref: order.append(cur); ref[cur] = {'src': fn, 'C': None, 'X': None, 'left': None, 'D': 'D=true' in line}
        elif cur and 'C-REDUCIBLE' in line:
            ref[cur]['C'] = True; ref[cur]['X'] = re.search(r'X=(\{[^}]*\})', line).group(1)
        elif cur and 'search |X|' in line:
            m = re.search(r'best X=(\{[^}]*\}) leftover (\d+)', line)
            if ref[cur]['C'] is None: ref[cur]['C'] = False
            if m: ref[cur]['bestX'] = m.group(1); ref[cur]['left'] = int(m.group(2))
cfg = {}
for fn in glob.glob(os.path.join(W, '**', '*.txt'), recursive=True):
    try:
        for line in open(fn):
            f = line.split()
            if len(f) == 5 and f[0] in ref and f[0] not in cfg and f[1].isdigit(): cfg[f[0]] = line.strip()
    except UnicodeDecodeError: pass
keep = [nm for nm in order if nm in cfg and not ref[nm]['D'] and ref[nm]['C'] is not None]
with open('valc.txt', 'w') as f:
    for nm in keep: f.write(cfg[nm] + '\n')
with open('valc_x.txt', 'w') as f:
    for nm in keep:
        if ref[nm]['X']: f.write('%s %s\n' % (nm, ref[nm]['X']))
        if ref[nm].get('bestX'): f.write('%s %s\n' % (nm, ref[nm]['bestX']))
with open('valc_ref.txt', 'w') as f:
    for nm in keep:
        r = ref[nm]; f.write('%s %s C=%s X=%s best=%s leftover=%s\n' % (nm, r['src'], r['C'], r['X'], r.get('bestX'), r['left']))
print('cfast entries', len(ref), 'not D with verdict', sum(1 for nm in order if not ref[nm]['D'] and ref[nm]['C'] is not None),
      'with input line', len(keep), 'C', sum(1 for nm in keep if ref[nm]['C']))
