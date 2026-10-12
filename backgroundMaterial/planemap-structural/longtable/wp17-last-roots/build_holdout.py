"""Build caches for plantri -m5 orders 21, 22 (holdout corpus generated here)."""
import pickle, sys
from multiprocessing import Pool
from engine import *

def job(args):
    order, gi, line = args
    fn = CACHE / f"{order}-{gi}.pkl"
    if fn.exists(): return
    rot = parse_ascii(line)
    roots = {r: build_root(rot, r) for r in degree_five(rot)}
    fn.write_bytes(pickle.dumps({"rot": rot, "ascii": line.strip(), "roots": roots}))

if __name__ == "__main__":
    CACHE.mkdir(exist_ok=True)
    jobs = []
    for n in map(int, sys.argv[1:]):
        for gi, line in enumerate(open(HERE / f"triangulations-min5-{n}.txt")):
            jobs.append((n, gi, line))
    with Pool(12) as p:
        for k, _ in enumerate(p.imap_unordered(job, jobs)):
            if k % 50 == 0: print(k, flush=True)
