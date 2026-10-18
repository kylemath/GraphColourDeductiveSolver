"""For Studio's Job 30 (requests 09:16-09:17Z): every D/C receiver window in the registry that wlp3's five-slot
pattern encoding cannot carry exactly.  wlp3.parse keeps, per link five i, the code (w_{i+1}, s_i, s_{i-1}, w_{i-1})
only when all four are specified; every other fixed letter is lost.  A window is listed when some fixed letter is in
no kept code ('lossy': the old encoding drops the window, or would widen it if loaded) or no code is kept at all
('empty': parse asserts).  Verdicts: D from dfast / dfast18 / kc lines (D=true), C from cfast or kc-C C-REDUCIBLE.
usage: python3 dropped.py > dropped.txt"""
import os, re, glob, collections
W = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
NAME = re.compile(r'^([epf])(\d+)_([^_\s]+)_([^_\s]+)')
def lossy(nm):
    m = NAME.match(nm)
    if not m: return None
    kind, d, lk, sv = m.group(1), int(m.group(2)), m.group(3), m.group(4)
    if len(lk) != d or len(sv) != d: return None
    def spec(ch, k):
        if ch == '.': return False
        if kind == 'p' and ((k == 'w' and ch == '9') or (k == 's' and ch == '0')): return False
        return True
    ws = [spec(c, 'w') for c in lk]; ss = [spec(c, 's') for c in sv]
    cov_w, cov_s, codes = set(), set(), 0
    for i in range(d):
        if lk[i] != '5' or not ws[i]: continue
        if ws[(i + 1) % d] and ss[i] and ss[(i - 1) % d] and ws[(i - 1) % d]:
            codes += 1; cov_w |= {i, (i + 1) % d, (i - 1) % d}; cov_s |= {i, (i - 1) % d}
    lost_w = [i for i in range(d) if ws[i] and i not in cov_w]; lost_s = [i for i in range(d) if ss[i] and i not in cov_s]
    if codes == 0: return 'empty', lost_w, lost_s
    if lost_w or lost_s: return 'lossy', lost_w, lost_s
    return None
ver = collections.defaultdict(lambda: {'ring': None, 'eng': set(), 'v': set()})
def scan_out(fn):
    cur = None
    for line in open(fn, errors='replace'):
        f = line.split()
        if not f: continue
        if not line.startswith(' ') and ' r=' in line:
            cur = f[0]; m = re.search(r' r=(\d+)', line); ring = int(m.group(1)) if m else None
            if 'D=true' in line and NAME.match(cur):
                eng = 'kc' if 'mode=' in line else ('dfast18' if 'dfast18' in fn or '18' in os.path.basename(fn) else 'dfast')
                ver[cur]['ring'] = ring; ver[cur]['eng'].add(eng); ver[cur]['v'].add('D')
            elif NAME.match(cur): ver[cur]['ring'] = ver[cur]['ring'] or ring
        elif 'C-REDUCIBLE' in line and cur and NAME.match(cur):
            eng = 'kc-C' if '(kc-C' in line else 'cfast'
            ver[cur]['eng'].add(eng); ver[cur]['v'].add('C')
files = glob.glob(os.path.join(W, 'out', '**', '*.out'), recursive=True) + glob.glob(os.path.join(W, 'out', '**', '*.cfast'), recursive=True) \
      + glob.glob(os.path.join(W, 'loop', '**', '*.out'), recursive=True) + glob.glob(os.path.join(W, 'loop', '**', '*.cfast'), recursive=True) \
      + glob.glob(os.path.join(W, 'job27', '*.cfast'))
for fn in sorted(set(files)): scan_out(fn)
rows = []
for nm, v in ver.items():
    if not v['v']: continue
    L = lossy(nm)
    if L: rows.append((v['ring'] or 0, nm, '/'.join(sorted(v['v'])), ','.join(sorted(v['eng'])), L))
rows.sort()
print('# Job 30 input: D/C receiver windows whose fixed letters the five-slot encoding (wlp3.parse) loses.')
print('# columns: name ring verdict engines kind lost-link-positions lost-s-positions  (positions in the name\'s own frame)')
print('# kind: empty = no five has all four code slots fixed (parse asserts); lossy = some fixed letter is in no code')
print('# engines: dfast, dfast18, kc (D); cfast, kc-C (C, engine level; kc-C uses conservative admissibility)')
for r, nm, v, e, (k, lw, ls) in rows:
    print('%s %d %s %s %s w%s s%s' % (nm, r, v, e, k, ''.join(map(str, lw)) or '-', ''.join(map(str, ls)) or '-'))
c = collections.Counter((x[2], x[4][0], '+' in x[3] or ',' in x[3]) for x in rows)
print('# totals:', len(rows), dict(c))
