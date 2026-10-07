#!/usr/bin/env python3
"""run.py INPUT OUTPREFIX WORKERS SHARDLINES [picyc options...]: shard INPUT into chunks of SHARDLINES lines, run ./picyc on each under
nice 10 with WORKERS processes, write OUTPREFIX.jsonl (concatenation, shard order) and OUTPREFIX.log. Resumable: finished shards are kept."""
import sys, os, subprocess, time
from multiprocessing.pool import ThreadPool
inp, pref, W, SL = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]); opts = sys.argv[5:]
lines = [l for l in open(inp) if l.strip()]; d = pref + '.shards'; os.makedirs(d, exist_ok=True)
shards = [(i, lines[i:i + SL]) for i in range(0, len(lines), SL)]
def job(a):
    i, ls = a; fn = '%s/s%07d' % (d, i)
    if os.path.exists(fn + '.done'): return i, 0.0
    open(fn + '.in', 'w').write(''.join(ls)); t = time.time()
    with open(fn + '.out', 'w') as fo, open(fn + '.err', 'w') as fe:
        r = subprocess.run(['nice', '-n', '10', os.path.abspath(os.environ.get('PICYC', './picyc')), fn + '.in'] + opts, stdout=fo, stderr=fe)
    if r.returncode == 0: open(fn + '.done', 'w').write('%.1f\n' % (time.time() - t))
    return i, time.time() - t
t0 = time.time(); log = open(pref + '.log', 'a'); log.write('%s start %s shards %d opts %s\n' % (time.strftime('%F %T'), inp, len(shards), opts)); log.flush()
with ThreadPool(W) as p:
    for k, (i, dt) in enumerate(p.imap_unordered(job, shards)):
        if k % 20 == 0 or dt > 60: log.write('%s shard %d done in %.0fs (%d/%d)\n' % (time.strftime('%F %T'), i, dt, k + 1, len(shards))); log.flush()
with open(pref + '.jsonl', 'w') as fo:
    for i, _ in shards: fo.write(open('%s/s%07d.out' % (d, i)).read())
errs = sum(1 for i, _ in shards if not os.path.exists('%s/s%07d.done' % (d, i)))
log.write('%s DONE %s wall %.0fs shards failed %d\n' % (time.strftime('%F %T'), pref, time.time() - t0, errs)); log.close()
print('DONE', pref, 'failed shards', errs)
