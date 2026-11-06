#!/usr/bin/env python3
# W13b round-5 Mac screener (K-2). Same logic and the same 12-column output as W13's screenallF.py (round 4), but
# self-contained (python3 standard library only) and with the engine paths taken from the environment.
#   per window, in file order:  kc -C  (D closure; if not D, search X with |X| <= 4)
#     kc says D            -> dfast18 on the same line (and dfast too when DF is set and ring <= 16)  => verdict D
#     kc says C-REDUCIBLE  -> cfast FILE --fixed X with kc's X                                      => verdict C
#     otherwise            -> verdict N
#   A hit counts only when its confirmation agrees: D needs "dfast18:D", C needs "cfast:C-REDUCIBLE".
# Resumable: windows whose code (column 1) is already in OUT are skipped (except ERROR lines), so a stopped batch restarts where it left off.
# usage:  KC=/path/kc DF18=/path/dfast18 CF=/path/cfast [DF=/path/dfast] [TO=1500] python3 mscreen.py BATCH.tsv OUT.tsv [MAXSEC]
# BATCH lines (famR4 format): code ring m n5 family name kcline      (tab separated; kcline = "name r m ringadj intadj")
# OUT lines (W13 res format): code ring m name verdict leftover X reached secs family confirm kcline
import os, re, sys, time, subprocess
if len(sys.argv) < 3: sys.exit(__doc__ or 'usage: python3 mscreen.py BATCH.tsv OUT.tsv [MAXSEC]')
batch, out = sys.argv[1], sys.argv[2]; maxsec = float(sys.argv[3]) if len(sys.argv) > 3 else 1e18
KC = os.environ.get('KC', 'kc'); DF18 = os.environ.get('DF18', 'dfast18'); CF = os.environ.get('CF', 'cfast'); DF = os.environ.get('DF', '')
TO = int(os.environ.get('TO', '1500')); T0 = time.time()
done = set()
if os.path.exists(out):
    for l in open(out):
        g = l.split('\t')
        if l.strip() and len(g) > 4 and g[4] != 'ERROR': done.add(g[0])     # ERROR lines (engine gave no output) are retried
todo = []
for l in open(batch):
    if not l.strip() or l.startswith('#'): continue
    f = l.rstrip('\n').split('\t')
    if f[0] in done: continue
    done.add(f[0]); todo.append(f)
print('todo', len(todo), 'batch', os.path.basename(batch), 'engines', KC, DF18, CF, DF or '(no dfast)', flush=True)
tmp = out + '.one'
def run(cmd):
    try: return subprocess.run(cmd, capture_output=True, text=True, timeout=TO).stdout
    except subprocess.TimeoutExpired: return 'TIMEOUT'
n = 0
for f in todo:
    if time.time() - T0 > maxsec: print('STOPPED left', len(todo) - n, flush=True); sys.exit(0)
    c, r, line = f[0], int(f[1]), f[6]
    with open(tmp, 'w') as g: g.write(line + '\n')
    t0 = time.time(); o = run([KC, '-C', tmp])
    isD = 'D=true' in o; isC = 'C-REDUCIBLE' in o
    m = re.search(r'leftover (\d+)', o); lo = m.group(1) if m else ''
    mx = re.search(r'X=\{([^}]*)\}', o); X = mx.group(1) if mx else ''
    mr = re.search(r'classes=(\d+) ext=\d+ reached=(\d+)', o); rr = '%s/%s' % (mr.group(2), mr.group(1)) if mr else ''
    conf = ''
    if 'TIMEOUT' in o: v = 'TIMEOUT'
    elif isD:
        a = (run([DF, tmp]) if r <= 16 else 'skip') if DF else 'na'; b = run([DF18, tmp])
        conf = 'dfast:%s dfast18:%s' % ('na' if a == 'na' else ('D' if 'D=true' in a else 'noD'), 'D' if 'D=true' in b else 'noD'); v = 'D'
    elif isC:
        cf = run([CF, tmp, '--fixed', X])
        conf = 'cfast:' + ('C-REDUCIBLE' if 'C-REDUCIBLE' in cf else 'noC'); v = 'C'
    elif not o.strip(): v = 'ERROR'
    else: v = 'N'
    n += 1
    with open(out, 'a') as g:
        g.write('\t'.join([c, f[1], f[2], f[5], v, lo, X, rr, '%.0f' % (time.time() - t0), f[4], conf, line]) + '\n')
    if v != 'N': print('HIT' if v in ('D', 'C') else 'WARN', v, f[1], f[5], f[4], X, conf, flush=True)
print('COMPLETE', n, flush=True)
