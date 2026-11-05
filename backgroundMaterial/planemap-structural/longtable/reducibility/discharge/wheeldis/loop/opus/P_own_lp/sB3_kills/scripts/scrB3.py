# B3 first-hit screener (after B1 screen2.py): families screened ring by ring (round robin), a family stops at its first
# two-engine D (kcc + dfast + dfast18) or confirmed C (kcc -C then cfast --fixed X). Skips every code with a verdict in
# b1res/res_*.tsv, results/res_*.tsv, W13 results (if present), and ring-14 codes of B1's famK2 window list (W13's territory).
# usage: python3 scrB3.py OUT.tsv RMAX FAMFILE FAMLIST   (FAMLIST: file with one family tag per line, in priority order)
import sys, os, re, glob, subprocess, time, collections, gzip
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from score import score
O = '/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus'
KC = O + '/K_frame_kill/kcc'; DF1 = O + '/C_kc_ring17/dfast'; DF2 = O + '/K_frame_kill/dfast18'; CF = O + '/A_rsst_defects/bin/cfast'
WD = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
out, rmax, famf, flist = sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4]
TO = int(os.environ.get('TO', '1800'))
MINSC = {int(a): int(b) for a, b in (x.split(':') for x in os.environ.get('MINSC', '').split(',') if x)}   # ring:minscore
res = {}
def loadres(fn):
    op = gzip.open if fn.endswith('.gz') else open
    try:
        for l in op(fn, 'rt'):
            g = l.rstrip('\n').split('\t')
            if len(g) > 4: res[g[0]] = g[4] + ('?' if g[4] == 'D' and len(g) > 10 and 'noD' in g[10] else '')
    except (OSError, EOFError): pass
for fn in glob.glob(WD + '/b1res/res_*.tsv') + glob.glob(WD + '/results/res_*.tsv'): loadres(fn)
for fn in glob.glob('/mnt/project-files/swarm/round6/W13-open-row-kills/results/*.tsv*'): loadres(fn)
w13 = set()
try:
    for l in gzip.open('/mnt/project-files/swarm/round6/B1-dual-kills/windows/famK2_R14.tsv.gz', 'rt'):
        g = l.split('\t')
        if g[1] == '14': w13.add(g[0])
except OSError: pass
for fn in glob.glob('/mnt/project-files/swarm/round6/W13-open-row-kills/windows/*.tsv*'):
    op = gzip.open if fn.endswith('.gz') else open
    try:
        for l in op(fn, 'rt'): w13.add(l.split('\t')[0])
    except (OSError, EOFError): pass
order = [l.strip() for l in open(flist) if l.strip() and not l.startswith('#')]
want = set(order)
fam = collections.defaultdict(list)
for l in open(famf):
    f = l.rstrip('\n').split('\t'); r = int(f[1])
    if r > rmax or f[4] not in want: continue
    if r in MINSC and score(f[6]) < MINSC[r]: continue
    fam[f[4]].append((r, -score(f[6]), -int(f[2]), f[0], f))
for k in fam: fam[k].sort()
def run(cmd, inp=None):
    try: return subprocess.run(['nice', '-n', '15'] + cmd, input=inp, capture_output=True, text=True, timeout=TO).stdout
    except subprocess.TimeoutExpired: return 'TIMEOUT'
state = {k: None for k in fam}
for k, L in fam.items():
    for r, _, _, c, f in L:
        if res.get(c) in ('D', 'C'): state[k] = ('hit-prior', f[5]); break
print('families', len(fam), 'already hit', sum(1 for v in state.values() if v), 'skip-W13 codes', len(w13), flush=True)
tmp = out + '.one'; nrun = 0
for ring in range(4, rmax + 1):
    for k in order:
        if k not in fam or state[k]: continue
        for r, _, _, c, f in fam[k]:
            if r != ring or c in res: continue
            if r == 14 and c in w13: continue
            line = f[6]; t0 = time.time(); o = run([KC, '-C'], line + '\n')
            isD = 'D=true' in o; isC = ('C-REDUCIBLE' in o) or ('C=true' in o)   # kcc prints C-REDUCIBLE (W13: B1's 'C=true' test never fires)
            m = re.search(r'leftover (\d+)', o); lo = m.group(1) if m else ''
            mx = re.search(r'X=\{([^}]*)\}', o); X = mx.group(1) if mx else ''
            mr = re.search(r'classes=(\d+) ext=\d+ reached=(\d+)', o); rr = '%s/%s' % (mr.group(2), mr.group(1)) if mr else ''
            conf = ''
            if 'TIMEOUT' in o: v = 'TIMEOUT'
            elif isD:
                a = run([DF1, '/dev/stdin'], line + '\n'); b = run([DF2, '/dev/stdin'], line + '\n')
                conf = 'dfast:%s dfast18:%s' % ('D' if 'D=true' in a else 'noD', 'D' if 'D=true' in b else 'noD'); v = 'D'
            elif isC:
                open(tmp, 'w').write(line + '\n'); cf = run([CF, tmp, '--fixed', X]); conf = 'cfast:' + re.sub(r'\s+', ' ', cf.strip())[:200]; v = 'C'
            else: v = 'N'
            res[c] = v; nrun += 1
            with open(out, 'a') as g:
                g.write('\t'.join([c, f[1], f[2], f[5], v, lo, X, rr, '%.0f' % (time.time() - t0), f[4], conf, line]) + '\n')
            if (v == 'D' and 'noD' not in conf) or (v == 'C' and 'C-REDUCIBLE' in conf.upper()):
                state[k] = ('hit', f[5]); print('HIT', k, v, f[5], conf[:80], flush=True); break
            elif v == 'D': print('kcc-D only', k, f[5], conf, flush=True)
            elif v == 'C': print('kc-C only (check cfast)', k, f[5], conf[:120], flush=True)
    print('ring', ring, 'done; run so far', nrun, '; open families:', sum(1 for k in fam if not state[k]), time.strftime('%H:%M:%S'), flush=True)
print('FINAL', {k: s for k, s in state.items() if s}, flush=True)
