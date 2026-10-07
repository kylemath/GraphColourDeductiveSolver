#!/usr/bin/env python3
"""Track A step 1 [exploratory]: frame-class filter over the plantri -m5 -c4 census (orders 12-27, in-plantri-*.txt).
Per graph: quick_frame (min deg 5, NoSep, Occ of the 4 Lean configurations; Occ only searched when an Appears exists).
Writes out/frame-<tag>.txt (picyc lines of frame-class graphs) and out/filter-<tag>.json (counts by order and reason).
usage: census_filter.py TAG FILE [FILE ...]   (4 workers, nice 10)"""
import sys, os, json
from multiprocessing import Pool
from collections import Counter, defaultdict
from tracka_lib import parse_line, quick_frame, G
def work(line):
    name, rot = parse_line(line)
    ok, g, why = quick_frame(rot)
    extra = None
    if why == 'appear_noocc':  # TipsClean caveat: appearances but no Occ -> record details
        extra = {k: [(list(i), t) for i, t in g.appears(k)] for k in ('Diamond', 'C2122')}
    return name, len(rot), ok, why, (line.strip() if ok else None), extra
if __name__ == '__main__':
    tag = sys.argv[1]; os.makedirs('out', exist_ok=True)
    cnt = defaultdict(Counter); frames = []; caveat = []
    def lines():
        for fn in sys.argv[2:]:
            for l in open(fn):
                if l.strip(): yield l
    with Pool(4) as P:
        for name, n, ok, why, line, extra in P.imap(work, lines(), chunksize=200):
            cnt[n][why] += 1; cnt[n]['total'] += 1
            if ok: cnt[n]['frame'] += 1; frames.append(line)
            if extra: caveat.append(dict(name=name, frame=ok, appears=extra))
    open('out/frame-%s.txt' % tag, 'w').write(''.join(l + '\n' for l in frames))
    json.dump(dict(counts={n: dict(c) for n, c in sorted(cnt.items())}, tipsclean_caveat=caveat), open('out/filter-%s.json' % tag, 'w'), indent=1)
    for n, c in sorted(cnt.items()): print(n, dict(c), flush=True)
