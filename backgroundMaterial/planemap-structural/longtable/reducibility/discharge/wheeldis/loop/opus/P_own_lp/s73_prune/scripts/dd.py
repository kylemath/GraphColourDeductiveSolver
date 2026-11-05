# chunked ddmin (monotone feasibility): python3 dd.py START.json OUT.json  ; levels 32,8,2,1 ; state in OUT, log run/dd.log
import sys, json, random, time
from client import *
start, outp = sys.argv[1:3]; cur = sorted(json.load(open(start))); rnd = random.Random(7)
LOG = open(S73 + 'run/dd.log', 'a')
def log(m): LOG.write('%s %s\n' % (time.strftime('%H:%M:%S'), m)); LOG.flush()
log('start %d' % len(cur)); tests = 0
for c in (2, 1):
    order = cur[:]; rnd.shuffle(order); chunks = [order[i:i + c] for i in range(0, len(order), c)]
    acc = 0; tried = 0; q = list(chunks); curset = set(cur)
    while q:
        batch = [q.pop(0)]
        if q: batch.append(q.pop(0))
        sets = [curset - set(b) for b in batch]
        res = check_many(sets); tests += len(batch); tried += len(batch)
        done = False
        for b, (ok, m) in zip(batch, res):
            if ok and not done:
                curset -= set(b); acc += 1; done = True   # accept the first passing chunk only (the other is retested against the new set)
            elif ok: q.insert(0, b)
        cur = sorted(curset); json.dump(cur, open(outp, 'w'))
        if tried % 10 < 2 or True: log('c=%d tried %d accepted %d size %d tests %d queue %d' % (c, tried, acc, len(cur), tests, len(q)))
    log('LEVEL c=%d done: size %d accepted %d tests %d' % (c, len(cur), acc, tests))
log('FINAL %d' % len(cur))
