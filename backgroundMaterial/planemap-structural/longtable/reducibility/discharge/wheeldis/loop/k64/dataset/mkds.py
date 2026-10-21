import os, re, glob, sys, collections
K47 = sys.argv[1]; OUT = sys.argv[2]
cfg = {}
for fn in sorted(glob.glob(os.path.join(K47, 'win*_*.txt'))):
    row = os.path.basename(fn)
    for l in open(fn):
        f = l.split()
        if len(f) == 5 and f[0][:1] == 'a' and f[0] not in cfg: cfg[f[0]] = (f[1:], row)
kc = {}; cur = None
for l in open(os.path.join(K47, 'A_kcc.out')):
    if not l.strip(): continue
    if not l.startswith(' '):
        f = l.split(); cur = f[0]
        d = re.search(r'D=(true|false)', l); kc[cur] = {'kcD': d.group(1) if d else '?', 'kcC': '', 'kcX': ''}
    elif cur:
        if 'C-REDUCIBLE' in l:
            kc[cur]['kcC'] = 'true'; x = re.search(r'X=(\{[^}]*\})', l)
            kc[cur]['kcX'] = x.group(1) if x else ''
        elif 'C=false' in l: kc[cur]['kcC'] = 'false_Xle%s' % re.search(r'\|X\|<=(\d+)', l).group(1)
df = {}
for l in open(os.path.join(K47, 'A_df.out')):
    m = re.match(r'^(a\S+) r=\d+ .*D=(true|false)', l)
    if m: df.setdefault(m.group(1), m.group(2))
cf = {}; cur = None
for l in open(os.path.join(K47, 'A_cf.out')):
    m = re.match(r'^(a\S+) r=\d+ ', l)
    if m: cur = m.group(1); continue
    if cur and 'fixed X=' in l: cf[cur] = 'leftover0' if 'leftover bad classes extending after contraction = 0' in l else 'rejected'
kill = {}
for l in open(os.path.join(K47, 'KILL')):
    f = l.split(' ', 1)
    if len(f) == 2 and not f[1].startswith('MISMATCH'): kill.setdefault(f[0], 'D' if f[1].startswith('D') else 'C')
w = open(os.path.join(OUT, 'windows_judged.tsv'), 'w')
w.write('name\tring\tm\tn5\tn6\tn7\tn8\tint_degrees\tring_adj\tint_adj\tkc_D\tkc_C\tkc_X\tdfast_D\tcfast_fixedX\ttwo_engine\tfirst_window_file\n')
miss = 0; cnt = collections.Counter()
for nm in sorted(kc):
    if nm not in cfg: miss += 1; continue
    (r, m, ra, ia), src = cfg[nm]; m = int(m)
    ras = ra.split(';'); ias = ia.split(';')
    deg = [(0 if ras[v] == '-' else len(ras[v].split(','))) + (0 if ias[v] == '-' else len(ias[v].split(','))) for v in range(m)]
    c = collections.Counter(deg); k = kc[nm]; te = kill.get(nm, '-'); cnt[te] += 1
    w.write('\t'.join(map(str, [nm, r, m, c[5], c[6], c[7], c[8], ','.join(map(str, deg)), ra, ia, k['kcD'], k['kcC'] or '-', k['kcX'] or '-',
                                 df.get(nm, '-'), cf.get(nm, '-'), te, src])) + '\n')
w.close()
print('kc verdicts', len(kc), 'with a config line', len(kc) - miss, 'missing', miss, 'two-engine', dict(cnt))
