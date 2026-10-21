#!/usr/bin/env python3
"""Run a prebuilt kc/kcf binary over window lines. No compiler, no GNU xargs/timeout needed (works on macOS).
usage: KT=600 python3 run_bin.py BINARY WINDOWS.txt OUTDIR WORKERS [kc|kcf]
  kc  : BINARY -C -s 60 -t $KT          (one NAME.txt per window in OUTDIR; INCOMPLETE/timeout windows get NAME.timeout, not NAME.txt)
  kcf : BINARY -C -F 8                  (kcf pass; add NICE=10 to lower priority)
Resumable: finished windows (NAME.txt) are skipped. Prints a summary with KILL_D / KILL_C / FZERO lines at the end."""
import sys, os, subprocess, glob
from concurrent.futures import ThreadPoolExecutor
exe, win, out, nw = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4])
mode = sys.argv[5] if len(sys.argv) > 5 else 'kc'
kt = os.environ.get('KT', '600'); nice = int(os.environ.get('NICE', '0'))
os.makedirs(out, exist_ok=True)
lines = [l.strip() for l in open(win) if l.strip()]
cmd = [exe, '-C', '-s', '60', '-t', kt] if mode == 'kc' else [exe, '-C', '-F', '8']
wd = int(kt) + 300 if mode == 'kc' else 7200
def run(l):
    n = l.split()[0]; f = os.path.join(out, n + '.txt')
    if os.path.exists(f): return
    try:
        o = subprocess.run(cmd, input=l + '\n', capture_output=True, text=True, timeout=wd, preexec_fn=(lambda: os.nice(nice)) if nice else None).stdout
    except subprocess.TimeoutExpired: open(f + '.timeout', 'w').write(l + '\n'); return
    if mode == 'kc' and 'INCOMPLETE' in o: open(f + '.timeout', 'w').write(o); return
    if o.strip(): open(f + '.tmp', 'w').write(o); os.replace(f + '.tmp', f)
with ThreadPoolExecutor(nw) as ex: list(ex.map(run, lines))
done = glob.glob(os.path.join(out, '*.txt')); print('done', len(done), 'of', len(lines), 'timeouts', len(glob.glob(os.path.join(out, '*.timeout'))))
for f in done:
    for x in open(f).read().splitlines():
        if 'D=true' in x: print('KILL_D', x[:220])
        if 'C-REDUCIBLE' in x: print('KILL_C', x[:220])
        if 'FZERO' in x: print('FZERO', x[:300])
