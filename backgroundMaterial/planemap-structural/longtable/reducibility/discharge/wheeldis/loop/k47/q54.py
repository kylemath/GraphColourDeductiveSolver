"""Round 54 queue (Long Table 21:53Z: the binders of Opus's l3q solve 11f050ea).  q52r16.sh plus stop14 in one driver:
per row, win45 windows (ring 16 and 18), drive45 at ring <= 16 (STOP=0, NW 3, CAP s), stopped as soon as every ring <=
RSTOP window is done and the row has a two-engine kill (or, after that, at its first kill); then minkill47; a row with
no kill gets its ring <= 18 windows not yet run written to win52_<row>_todo.txt for Studio.
usage: python3 q54.py ROWS RSTOP CAP   (ROWS: lines 'D LK SV PREFIX ...'; '#' starts a comment) -> R54_<P>.DONE per row"""
import sys, os, time, subprocess
H = os.path.dirname(os.path.abspath(__file__)); os.chdir(H)
ROWS, RSTOP, CAP = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
now = lambda: time.strftime('%H:%MZ', time.gmtime())
def done_names():
    return {l.split()[0] for l in open('A_kcc.out') if l.strip() and not l.startswith(' ')}
def kills(W):
    if not os.path.exists('KILL'): return []
    return [l.split()[0] for l in open('KILL') if l.split() and l.split()[0] in W and not l.split()[1].startswith('MISMATCH')]
def kill_tree(pid):
    ps = subprocess.run(['ps', '-eo', 'pid,ppid'], capture_output=True, text=True).stdout.split('\n')[1:]
    kids = {}
    for a in ps:
        if a.split(): kids.setdefault(int(a.split()[1]), []).append(int(a.split()[0]))
    todo, allp = [pid], []
    while todo:
        p = todo.pop(); allp.append(p); todo += kids.get(p, [])
    for p in allp:
        try: os.kill(p, 15)
        except ProcessLookupError: pass
    return allp
for line in open(ROWS):
    f = line.split('#')[0].split()
    if len(f) < 4: continue
    D, LK, SV, P = f[:4]
    if os.path.exists('R54_%s.DONE' % P): continue
    W16, W18 = ('win45_%s_%s_%s_A%d.txt' % (D, LK, SV, R) for R in (16, 18))
    for R, w in ((16, W16), (18, W18)):
        if not os.path.exists(w): subprocess.run(['python3', 'win45.py', str(R), D, LK, SV], stdout=subprocess.DEVNULL, check=True)
    W = {l.split()[0]: int(l.split()[1]) for l in open(W16) if l.strip()}
    low = {n for n, r in W.items() if r <= RSTOP}
    print(now(), 'row', P, D, LK, SV, '-', len(W), 'windows at ring <= 16,', len(low), 'at ring <=', RSTOP, flush=True)
    with open('drive54_%s_16.log' % P, 'w') as lg:
        pr = subprocess.Popen(['timeout', str(CAP), 'python3', 'drive45.py', W16, '600'], stdout=lg, stderr=subprocess.STDOUT,
                              env=dict(os.environ, STOP='0', NW='3'))
    lowdone = False
    while pr.poll() is None:
        time.sleep(30)
        if not lowdone and low <= done_names():
            lowdone = True; print(now(), 'ring <=', RSTOP, 'done;', len(kills(W)), 'kills', flush=True)
        if lowdone and kills(W):
            print(now(), 'stopped drive', kill_tree(pr.pid), flush=True); pr.wait(); break
    subprocess.run(['python3', 'minkill47.py', W16, LK, P])
    if not (os.path.exists(P + '_kills.txt') and os.path.getsize(P + '_kills.txt') > 0):
        dn = done_names()
        out = [l for l in open(W18) if l.strip() and l.split()[0] not in dn]
        fn = 'win52_%s_%s_%s_todo.txt' % (D, LK, SV)
        open(fn, 'w').write(''.join(out)); print(now(), len(out), 'windows left ->', fn, flush=True)
    print(now(), 'row', P, 'closed', flush=True); open('R54_%s.DONE' % P, 'w').close()
