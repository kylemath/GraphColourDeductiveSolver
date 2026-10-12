#!/usr/bin/env python3
"""Job BS: the 153 flat holes (link and second ring all degree 6) of the IPR-dual samples n = 56, 58, 60, 62 (C108-C120, buckygen part 0/400): picyc.bo --jobbo --nocls
(classes: studiointel flat_kclass found kappa = 1 at all 153, so class F/N = hole F/N), both orientations, 4 processes."""
import json, os, subprocess, tempfile
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__)); BIN = os.path.join(HERE, '../picyc.bo')
def job(a):
    N, line, hs, mir = a
    with tempfile.NamedTemporaryFile('w', suffix='.txt', delete=False) as fh: fh.write(line + '\n'); fn = fh.name
    try:
        o = subprocess.run(['nice', '-n', '10', BIN, fn, '--jobbo', '--nocls', '--cap', '200000000', '--holes', ','.join(map(str, hs))] + (['--mirror'] if mir else []), capture_output=True, text=True).stdout
    finally: os.unlink(fn)
    return [l for l in o.splitlines() if '"kind": "hole"' in l]
if __name__ == '__main__':
    L = json.load(open(os.path.join(HERE, 'flat-holes.json'))); jobs = [(N, line, hs, m) for N, line, hs in L for m in (False, True)]
    with Pool(4) as P, open(os.path.join(HERE, 'jobbs-flat.jsonl'), 'w') as f:
        for k, ls in enumerate(P.imap_unordered(job, jobs)):
            for l in ls: f.write(l + '\n')
            f.flush(); print(k + 1, '/', len(jobs), flush=True)
