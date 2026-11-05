# first-hit screener: per family (cell), windows in ring order (score desc inside a ring); a family stops at its first two-engine D/C.
# usage: python3 screen2.py OUT.tsv RMAX FAMFILE [FAMREGEX]
import sys, os, re, json, glob, subprocess, time, collections
from kcanon import code
from score import score
O = '/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus'
KC = O + '/K_frame_kill/kcc'; DF1 = O + '/C_kc_ring17/dfast'; DF2 = O + '/K_frame_kill/dfast18'; CF = O + '/A_rsst_defects/bin/cfast'
out, rmax, famf = sys.argv[1], int(sys.argv[2]), sys.argv[3]; rx = re.compile(sys.argv[4]) if len(sys.argv) > 4 else None
TO = int(os.environ.get('TO', '900'))
res = {}
for fn in glob.glob('res_*.tsv'):
    for l in open(fn):
        g = l.rstrip('\n').split('\t'); res[g[0]] = g[4] + ('' if g[4] != 'D' else ('' if 'noD' not in g[10] else '?'))
for fn in glob.glob('prior_*.json'):
    for c in json.load(open(fn)): res.setdefault(c, 'N')
fam = collections.defaultdict(list)
for l in open(famf):
    f = l.rstrip('\n').split('\t'); r = int(f[1])
    if r > rmax or (rx and not rx.search(f[4])): continue
    fam[f[4]].append((r, -score(f[6]), -int(f[2]), code(f[6]), f))
def run(cmd, inp=None):
    try: return subprocess.run(['nice', '-n', '15'] + cmd, input=inp, capture_output=True, text=True, timeout=TO).stdout
    except subprocess.TimeoutExpired: return 'TIMEOUT'
for k in fam: fam[k].sort()
state = {k: None for k in fam}
for k, L in fam.items():
    for r, _, _, c, f in L:
        if res.get(c) in ('D', 'C'): state[k] = ('hit', f[5]); break
print('families', len(fam), 'already hit', sum(1 for v in state.values() if v), flush=True)
tmp = out + '.one'
# round robin by ring so cheap rings of every family go first
for ring in range(4, rmax + 1):
    for k, L in sorted(fam.items()):
        if state[k]: continue
        for r, _, _, c, f in L:
            if r != ring or c in res: continue
            line = f[6]; t0 = time.time(); o = run([KC, '-C'], line + '\n')
            isD = 'D=true' in o; isC = 'C=true' in o
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
            res[c] = v
            with open(out, 'a') as g:
                g.write('\t'.join([c, f[1], f[2], f[5], v, lo, X, rr, '%.0f' % (time.time() - t0), f[4], conf, line]) + '\n')
            if (v == 'D' and 'noD' not in conf) or (v == 'C' and 'C-REDUCIBLE' in conf.upper()):
                state[k] = ('hit', f[5]); print('HIT', k, v, f[5], conf[:80], flush=True); break
            elif v == 'C': print('kc-C only (check cfast)', k, f[5], conf[:120], flush=True)
    print('ring', ring, 'done; open families:', sorted(k for k, s in state.items() if not s), flush=True)
print('FINAL', json.dumps({k: s for k, s in state.items()}), flush=True)
