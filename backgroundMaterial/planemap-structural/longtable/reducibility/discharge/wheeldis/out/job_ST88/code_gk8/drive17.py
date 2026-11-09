# W15: replay one dumped receiver query (st21_w15.py SEPQDUMP=QDIR) through the C++ separator.
# usage: python3 drive17.py QDIR d OUT [part=k/n] [neck=0|1] [bugfix=0|1] [thrshift=x] [cap=N] [timeout=s] [sepbin=path]
# claim=1 (default): the job first creates OUT.claim and is skipped if it exists (so two job lists can run from both ends).
# OUT gets one line per reported arrangement "d link s w" (w = the separator's exact leaf value); prints one summary line.
import sys, json, subprocess, os, time
QDIR, d, OUT = sys.argv[1], int(sys.argv[2]), sys.argv[3]
opt = dict(a.split('=', 1) for a in sys.argv[4:])
E = json.load(open(os.path.join(QDIR, 'env.json')))
env = dict(os.environ); env.update({k: v for k, v in E.items() if k.startswith('SEP_')})
env['SEP_BUGFIX'] = opt.get('bugfix', '1'); env['SEP_NECK'] = opt.get('neck', '0')
if 'part' in opt: env['SEP_PART'] = opt['part']
else: env.pop('SEP_PART', None)
q = open(os.path.join(QDIR, 'q_d%d.txt' % d)).read().split('\n', 1)
f = q[0].split(); assert f[0] == 'q' and int(f[1]) == d
thr = float(f[2]) + float(opt.get('thrshift', '0')); f[2] = '%.12f' % thr
if 'cap' in opt: f[3] = opt['cap']
cap = int(f[3]); qt = ' '.join(f) + '\n' + q[1]
binp = opt.get('sepbin', E['SEPBIN']); t0 = time.time()
if opt.get('claim', '1') == '1':   # a second worker may take jobs from the other end of the list: one claim file per output
    try: os.close(os.open(OUT + '.claim', os.O_CREAT | os.O_EXCL | os.O_WRONLY))
    except FileExistsError:
        print('skip17 d=%d part=%s: %s already claimed by another worker' % (d, opt.get('part', '0/1'), OUT), flush=True); sys.exit(0)
import shutil   # round 6 (macpack): macOS has no GNU 'timeout'; then the separator runs without it (W17_NOTIMEOUT=1 forces that path)
_to = [] if (os.environ.get('W17_NOTIMEOUT') == '1' or not shutil.which('timeout')) else ['timeout', opt.get('timeout', '86400')]
p = subprocess.run(_to + ['nice', '-n', os.environ.get('W17NICE', '15'), binp, os.path.join(QDIR, 'sf.in')], input=qt, capture_output=True, text=True, env=env)
n = 0; end = None
with open(OUT, 'w') as g:
    for l in p.stdout.split('\n'):
        if l.startswith('A '):
            a = l.split(); g.write('%d %s %s %s\n' % (d, a[2], a[3], a[1])); n += 1
        elif l.startswith('END'): end = l
print('drive17 d=%d part=%s neck=%s bugfix=%s thr=%.12f reported %d end=[%s] rc=%d %.0fs%s%s' % (d, opt.get('part', '0/1'), env['SEP_NECK'], env['SEP_BUGFIX'], thr, n, end, p.returncode,
      time.time() - t0, ' CAPHIT' if n >= cap else '', '' if end else ' NO-END (died or timed out)'), flush=True)
if end is None: print(p.stderr[-2000:])
