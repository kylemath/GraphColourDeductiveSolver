"""Ring-merge sweep step 2 (Long Table 20 Oct 20:49Z): each held entry -> kc -C -s 60 -t 600; guard (union-find) on kc's X;
cfast --fixed kc's X. CONFIRMED = kc C with a guarded (no ring merge) X and cfast leftover 0. KILL LINE = no such X.
Usage: python3 run2.py inputs.tsv NW"""
import os, sys, re, subprocess, threading, collections, tempfile
H = os.path.dirname(os.path.abspath(__file__)); WD = os.path.abspath(os.path.join(H, '..', '..', '..'))
KC = os.path.join(WD, 'loop', 'kc', 'kc'); CF = os.path.join(WD, '..', 'studio15', 'cfast')
rows = [l.rstrip('\n').split('\t') for l in open(sys.argv[1]) if l.strip()]; NW = int(sys.argv[2])
lock = threading.Lock(); sem = threading.Semaphore(NW)
def ringmerge(x):
    par = {}
    def fd(a):
        while par.setdefault(a, a) != a: a = par[a]
        return a
    for e in x:
        a, b = e.strip().split('-'); par[fd(a)] = fd(b)
    return max(collections.Counter(fd(v) for v in par if v.startswith('R')).values(), default=0) >= 2
def run(cmd): return subprocess.run(['nice', '-n', '15'] + cmd, capture_output=True, text=True).stdout.rstrip('\n')
def work(fn, line):
    with sem:
        nm = line.split()[0]
        with tempfile.NamedTemporaryFile('w', suffix='.in', dir=H, delete=False) as t: t.write(line + '\n'); tf = t.name
        o = run([KC, '-C', '-s', '60', '-t', '600', tf])
        with lock: open(os.path.join(H, 'A_kcc.out'), 'a').write(o + '\n')
        m = re.search(r'C-REDUCIBLE X=\{([^}]*)\}', o); kD = 'D=true' in o.split('\n')[0]
        if kD: st = 'kc-D (not C; D on kc)'
        elif not m: st = 'NO-C on kc'
        else:
            x = m.group(1); rm = ringmerge(x.split(','))
            o3 = run([CF, tf, '--fixed', x])
            with lock: open(os.path.join(H, 'A_cf.out'), 'a').write(o3 + '\n')
            ok = 'C-REDUCIBLE, leftover bad classes extending after contraction = 0' in o3
            st = ('CONFIRMED X={%s}' % x) if ok and not rm else ('KCX-MERGES X={%s} cfast %s' % (x, 'ok' if ok else 'rejects') if rm else 'CFAST-REJECTS X={%s}' % x)
        os.unlink(tf)
        with lock: open(os.path.join(H, 'results.txt'), 'a').write('%s %s %s\n' % (nm, fn, st))
ts = [threading.Thread(target=work, args=r) for r in rows]
for t in ts: t.start()
for t in ts: t.join()
open(os.path.join(H, 'A.DONE'), 'w').write('complete\n')
