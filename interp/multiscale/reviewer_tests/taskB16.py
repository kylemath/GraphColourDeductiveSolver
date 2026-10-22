# Task B at large L (old measure only): exact BFS from a SAMPLE of sources a (lower bound on k*), targets = all level rows.
import sys, random, json, subprocess, collections, time
sys.path.insert(0, '/mnt/project-files/multiscale/reviewer_tests'); sys.path.insert(0, '/mnt/project-files/multiscale/bandfill')
from lev import gen_level
from taskB import BFS
L = int(sys.argv[1]); ns = int(sys.argv[2]); t0 = time.time()
lev = gen_level(L); rng = random.Random(0)
# sources: rows with the most 'gap-4 / hidden run' structure first (max cyclic run of equal edge labels), then random
def maxrun(r):
    lab = [r[i] ^ r[(i+1) % L] for i in range(L)]; best = 0
    for s in range(L):
        c = 1
        while c < L and lab[(s+c) % L] == lab[s]: c += 1
        best = max(best, c)
    return best
byrun = collections.defaultdict(list)
for r in lev: byrun[maxrun(r)].append(r)
src = []
for k in sorted(byrun, reverse=True): src += rng.sample(byrun[k], min(len(byrun[k]), max(1, ns//len(byrun))))
src = src[:ns]
print(json.dumps(dict(L=L, nlevel=len(lev), runs={k: len(v) for k, v in byrun.items()}, nsrc=len(src), prep=round(time.time()-t0))), flush=True)
inp = f"{L} 12 {len(src)} {len(lev)}\n" + "\n".join("".join(map(str, r)) for r in src) + "\n" + "\n".join("".join(map(str, r)) for r in lev) + "\n"
p = subprocess.Popen([BFS], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True); p.stdin.write(inp); p.stdin.close()
for a, line in zip(src, p.stdout):
    line = line.strip(); h = collections.Counter(line)
    print(json.dumps(dict(L=L, a=''.join(map(str, a)), run=maxrun(a), hist={str(ord(c)-49) if c != 'x' else 'inf': v for c, v in sorted(h.items())},
                          kmax=max(ord(c)-49 for c in line if c != 'x'), sec=round(time.time()-t0))), flush=True)
