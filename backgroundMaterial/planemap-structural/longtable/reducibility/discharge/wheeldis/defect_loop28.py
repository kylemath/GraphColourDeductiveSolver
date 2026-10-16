"""Job 28 task 3 (exploratory): process the K = 4 defect candidates as the searches write them.
Every POLL seconds, each candidate file's new complete lines form a batch.  Per batch:
  defect_check2.py BATCH WORK bf  (R_opt+)  ->  dfast18 on the needed configurations with ring <= 16
  (out/def_loop_j28_<tag>_<n>.out), cfast --search --limit 1 on the needed C tests (out/def_loop_j28_<tag>_<n>.cfast),
  and repeat until nothing is left to test.  The verdict files are named def_*, so defect_check2.py reads them back.
Survivors (status SURVIVES) and still-open candidates are appended to out/job28/defect_survivors.txt / defect_open.txt.
One line per batch in out/job28/defect.log.  Usage: python3 defect_loop28.py DFAST CFAST FILE [FILE ...] [poll=600]"""
import sys, os, subprocess, time, collections
HERE = os.path.dirname(os.path.abspath(__file__)); J = os.path.join(HERE, 'out', 'job28')
DFAST, CFAST = sys.argv[1], sys.argv[2]
FILES = [a for a in sys.argv[3:] if '=' not in a]
POLL = int(next((a[5:] for a in sys.argv[3:] if a.startswith('poll=')), '600'))
OFF = os.path.join(J, 'defect_offsets.txt')
off = collections.defaultdict(int)
if os.path.exists(OFF):
    for l in open(OFF): k, v = l.split(); off[k] = int(v)
def log(s): open(os.path.join(J, 'defect.log'), 'a').write(time.strftime('%m-%d %H:%M ') + s + '\n')
def run(binary, args, inp, out):
    with open(out, 'w') as o: subprocess.run(['nice', '-n', '18', binary, inp] + args, stdout=o, stderr=subprocess.STDOUT)
nb = sum(1 for _ in open(os.path.join(J, 'defect.log'))) if os.path.exists(os.path.join(J, 'defect.log')) else 0
while True:
    did = False
    for fn in FILES:
        tag = os.path.basename(fn).replace('.txt', '')
        if not os.path.exists(fn): continue
        lines = open(fn).read().split('\n')[:-1]          # complete lines only
        new = lines[off[fn]:]
        if not new: continue
        did = True; nb += 1; b = '%s_b%d' % (tag, nb)
        bf = os.path.join(J, 'batch_%s.txt' % b); open(bf, 'w').write('\n'.join(new) + '\n')
        W = os.path.join(J, 'work_%s' % b); ntest = collections.Counter()
        for n in range(1, 13):
            out = subprocess.run([sys.executable, os.path.join(HERE, 'defect_check2.py'), bf, W, 'bf'], capture_output=True, text=True, cwd=HERE).stdout
            dl = [l for l in open(W + '.d') if l.strip() and int(l.split()[1]) <= 16]
            cl = [l for l in open(W + '.c') if l.strip() and int(l.split()[1]) <= 16]
            if not dl and not cl: break
            if dl:
                open(W + '.d%d.in' % n, 'w').write(''.join(dl)); ntest['dfast'] += len(dl)
                run(DFAST, [], W + '.d%d.in' % n, os.path.join(HERE, 'out', 'def_loop_j28_%s_%d.out' % (b, n)))
            else:
                open(W + '.c%d.in' % n, 'w').write(''.join(cl)); ntest['cfast'] += len(cl)
                run(CFAST, ['--search', '--limit', '1'], W + '.c%d.in' % n, os.path.join(HERE, 'out', 'def_loop_j28_%s_%d.cfast' % (b, n)))
        st = collections.Counter(l.split()[0] for l in open(W + '.status') if l.strip())
        for l in open(W + '.status'):
            if l.startswith('SURVIVES'): open(os.path.join(J, 'defect_survivors.txt'), 'a').write(l)
            elif l.startswith('open'): open(os.path.join(J, 'defect_open.txt'), 'a').write(l)
        log('%s: %d candidates (%s .. ) %s; tested %s' % (b, len(new), new[0].split()[1][:24], dict(st), dict(ntest)))
        off[fn] = len(lines)
        open(OFF, 'w').write(''.join('%s %d\n' % kv for kv in off.items()))
    done = all(os.path.exists(os.path.join(J, x)) for x in ('defK4_c56.DONE', 'defK4_c7.DONE'))
    if done and not did: break
    time.sleep(POLL if not did else 5)
