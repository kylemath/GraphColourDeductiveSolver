# driver: for each config (mode, K0, collar, L) find w* = least w in 1..6 with C(w)=TRUE using bfr.
import subprocess, sys, json, time, re
from concurrent.futures import ThreadPoolExecutor
BIN = sys.argv[1]; OUT = sys.argv[2]; NW = int(sys.argv[3])
jobs = []
for L in range(5, 16):
    for K0 in (2, 3, 4):
        jobs.append((1, K0, 0, L))
    jobs.append((3, 2, 0, L))
for L in range(5, 16):
    for K0 in (2, 3, 4, 5):
        jobs.append((1, K0, 1, L))
    jobs.append((3, 2, 1, L)); jobs.append((3, 3, 1, L))
import os
done = set()
if os.path.exists(OUT):
    for l in open(OUT): r = json.loads(l); done.add((r['mode'], r['K0'], r['collar'], r['L']))
# seam-only K0>=3 in mode 1 equals the unfiltered problem when every level row already has maxrun<=K0
# (histograms: L%3 in {0,1} -> maxrun<=3); those are not rerun (= Opus table).
jobs = [j for j in jobs if j not in done and not (j[0] == 1 and j[2] == 0 and j[1] >= 3 and j[3] % 3 != 2)]
pri = lambda j: (j[3] >= 14, 0 if (j[2] == 0 and j[1] == 2) else (1 if j[2] == 1 else 2), j[3])
jobs.sort(key=pri)
def run(j):
    m, K0, col, L = j; rec = dict(mode=m, K0=K0, collar=col, L=L, w={}); t0 = time.time()
    for w in range(1, 7):
        p = subprocess.run([BIN, str(L), str(w), str(m), '1', '1', str(K0), str(col)], capture_output=True, text=True)
        o = p.stdout; nl = int(re.search(r'nlevel=(\d+)', o).group(1)); rec['nlevel'] = nl
        rec['hist'] = o.splitlines()[0]
        if nl == 0: rec['wstar'] = 'vacuous'; break
        res = re.search(r'canonical_a=(\d+) bad_a=(\d+) bad_pairs=(\d+)  C\(w\)=(\w+)', o)
        if not res: rec['w'][w] = 'ERR'; break
        rec['w'][w] = [int(res.group(1)), int(res.group(2)), int(res.group(3))]
        bad = re.search(r'BAD w=\d+ a=(\d+) b=(\d+)', o)
        if bad: rec.setdefault('ex', {})[w] = [bad.group(1), bad.group(2)]
        if res.group(4) == 'TRUE': rec['wstar'] = w; break
    rec['sec'] = round(time.time() - t0, 1)
    with open(OUT, 'a') as f: f.write(json.dumps(rec) + '\n')
    print(rec['mode'], rec['K0'], rec['collar'], rec['L'], rec.get('wstar'), rec['sec'], flush=True)
with ThreadPoolExecutor(NW) as ex: list(ex.map(run, jobs))
