"""Job 52 (Long Table 19 Oct 12:45Z): ring <= 18 reducibility of one surviving face-receiver row from explore's round-52
window file (out/job52/win52_<d>_<link>_<s>_todo.txt, from bcb72b47; one row's win45 windows in ring order).
Per window, in file order (ring order):
  1. kc -C -s 60 -t 600 (loop/kc/kc).
  2. kc D=true  -> dfast18 (wheels/studio/dfast18.cpp; ring <= 19) must also give D=true      => two-engine D.
     kc C-REDUCIBLE X -> cfast --fixed X (studio15/cfast) must give C-REDUCIBLE, leftover 0    => two-engine C.
  3. The first two-engine kill decides the row; afterwards only windows of ring <= 16 are run (they yield more f-names),
     and no ring 17-18 time is spent on the row.
Row cap: 6 h wall clock (every engine call gets the remaining time as an alarm). Ring 17-18 dfast18 / cfast calls take
one of 4 global memory slots (mkdir locks in out/job52/.heavy). Nothing is admitted to any registry.
Output: out/job52/row_<d>_<link>_<s>/results.txt (one line per window), kills.txt, STATUS (final: KILLED / SURVIVES /
CAPPED with the counts), and the raw engine outputs.
Usage: python3 out/job52/job52.py out/job52/win52_..._todo.txt"""
import os, sys, re, time, subprocess, glob
HERE = os.path.dirname(os.path.abspath(__file__)); WD = os.path.abspath(os.path.join(HERE, '..', '..'))
KC = os.path.join(WD, 'loop', 'kc', 'kc'); CF = os.path.join(WD, '..', 'studio15', 'cfast')
DF = os.environ.get('DFAST18', os.path.join(WD, '..', '..', 'wheels', 'studio', 'dfast18'))
CAP = float(os.environ.get('ROWCAP', str(6 * 3600))); NHEAVY = int(os.environ.get('NHEAVY', '4'))
src = sys.argv[1]; tag = os.path.basename(src).replace('win52_', '').replace('_todo.txt', '')
RD = os.path.join(HERE, 'row_' + tag); os.makedirs(RD, exist_ok=True)
T0 = time.time()
def left(): return CAP - (time.time() - T0)
def run(cmd, infile, outfile, heavy):
    """run one engine on one window file with the remaining row time as an alarm; returns (output text, seconds) or None."""
    lock = None
    if heavy:
        os.makedirs(os.path.join(HERE, '.heavy'), exist_ok=True)
        while lock is None:
            for k in range(NHEAVY):
                p = os.path.join(HERE, '.heavy', 'slot%d' % k)
                try: os.mkdir(p); lock = p; break
                except FileExistsError: pass
            if lock is None:
                if left() <= 0: return None
                time.sleep(30)
    try:
        if left() <= 0: return None
        t = time.time()
        with open(outfile, 'w') as fo:
            argv = [infile if a == '{in}' else a for a in cmd] if '{in}' in cmd else cmd + [infile]   # cfast wants FILE first
            subprocess.run(['nice', '-n', '10', 'perl', '-e', 'alarm shift; exec @ARGV', str(int(max(1, left())))] + argv,
                           stdout=fo, stderr=subprocess.STDOUT)
        return open(outfile).read(), time.time() - t
    finally:
        if lock: os.rmdir(lock)
wins = [l.rstrip('\n') for l in open(src) if l.strip()]
res = open(os.path.join(RD, 'results.txt'), 'a'); kills = open(os.path.join(RD, 'kills.txt'), 'a')
done = {l.split()[0] for l in open(os.path.join(RD, 'results.txt'))} if os.path.getsize(os.path.join(RD, 'results.txt')) else set()
killed = any(True for _ in open(os.path.join(RD, 'kills.txt'))) if os.path.getsize(os.path.join(RD, 'kills.txt')) else False
nrun = nskip = 0; best = None; capped = False
for w in wins:
    nm, ring = w.split()[0], int(w.split()[1])
    if nm in done: continue
    if killed and ring >= 17: nskip += 1; continue
    if left() <= 0: capped = True; break
    safe = re.sub(r'[^A-Za-z0-9_.-]', '_', nm)
    wf = os.path.join(RD, 'w_%s.in' % safe); open(wf, 'w').write(w + '\n')
    r = run([KC, '-C', '-s', '60', '-t', '600'], wf, os.path.join(RD, 'w_%s.kc' % safe), False)
    if r is None: capped = True; break
    kout, kt = r; kD = 'D=true' in kout; mx = re.search(r'C-REDUCIBLE X=\{([^}]*)\}', kout)
    line = '%s ring=%d kc=%s(%.0fs)' % (nm, ring, 'D' if kD else ('C:{%s}' % mx.group(1) if mx else ('timeout' if 'D=' not in kout else 'neither')), kt)
    if kD:
        r2 = run([DF], wf, os.path.join(RD, 'w_%s.df' % safe), ring >= 17)
        if r2 is None: capped = True; res.write(line + ' dfast18=capped\n'); res.flush(); break
        dD = 'D=true' in r2[0]; line += ' dfast18=%s(%.0fs)' % ('D' if dD else ('notD' if 'D=false' in r2[0] else 'none'), r2[1])
        if dD: killed = True; kills.write('%s D kc+dfast18 ring=%d\n' % (nm, ring)); kills.flush()
    elif mx:
        r3 = run([CF, '{in}', '--fixed', mx.group(1)], wf, os.path.join(RD, 'w_%s.cf' % safe), ring >= 17)
        if r3 is None: capped = True; res.write(line + ' cfast=capped\n'); res.flush(); break
        cC = re.search(r'C-REDUCIBLE, leftover bad classes extending after contraction = 0', r3[0]) is not None
        lo = re.search(r'leftover[^=]*= (\d+)', r3[0]); line += ' cfast_fixed=%s(%.0fs)' % ('C' if cC else ('leftover %s' % lo.group(1) if lo else 'none'), r3[1])
        if cC: killed = True; kills.write('%s C kc+cfast X={%s} ring=%d\n' % (nm, mx.group(1), ring)); kills.flush()
    res.write(line + '\n'); res.flush(); nrun += 1
    os.remove(wf)
nk = sum(1 for _ in open(os.path.join(RD, 'kills.txt')))
left_w = sum(1 for w in wins if w.split()[0] not in {l.split()[0] for l in open(os.path.join(RD, 'results.txt'))} and not (nk and int(w.split()[1]) >= 17))
st = 'KILLED (%d two-engine kills)' % nk if nk else ('CAPPED (%d windows left)' % left_w if capped else 'SURVIVES')
open(os.path.join(RD, 'STATUS'), 'w').write('%s; windows run %d this pass, ring 17-18 skipped after kill %d; wall %.0fs\n' % (st, nrun, nskip, time.time() - T0))
print(tag, st)
