"""independent spot-check of witness lines: full fd = the completion; config must embed via grow.embeddings."""
import sys, random, pickle, collections
sys.argv = sys.argv[:1] + ['/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/ex55', 'x', 'y', 'z']
exec(open('sdrop.py').read().rsplit("if __name__ == '__main__':", 1)[0])
C = {c[0]: c for c in registry()}
L = [l for l in open('sdrop_witness.txt') if not l.startswith('#')]
random.seed(1); pick = [l for l in L if l.split()[0] in ('55667', '55758')][:40] + random.sample(L, 300)
bad = 0
for l in pick:
    ctx, nm, comp, img = [x.strip() for x in l.split('|')[0:1] + l.split('|')[2:5]] if False else (None, None, None, None)
    parts = [x.strip() for x in l.split(' | ')]
    wd = parts[0].split()[0]; nm = parts[1]; comp = dict(kv.split('=') for kv in parts[2].split())
    LK = [int(c) for c in wd]; P, pa, pf = build5(LK)
    fd = {('v',): 5}
    for i in range(5): fd[('w', i)] = LK[i] if LK[i] <= 8 else NEVER
    nmap = {''.join(map(str, x)): x for x in P}
    for x in P:
        if x[0] == 'p' and LK[x[1]] >= 9: fd[x] = NEVER
    for k, v in comp.items(): fd[nmap[k]] = int(v)
    assert all(x in fd for x in P)
    if not grow.embeddings(C[nm], P, pa, pf, fd): bad += 1; print('FAIL', l.strip()[:150])
print('witness spot-check: %d lines, %d fail' % (len(pick), bad))
