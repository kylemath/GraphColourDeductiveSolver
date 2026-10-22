# J = 1 agreement with ld.tau_step_le (even, |t|<=2) and odd step; base-point invariance of tau_J for J = 1..4.
import sys, random, numpy as np
sys.path.insert(0, '/mnt/project-files/multiscale/multicut/'); sys.path.insert(0, '/mnt/project-files/multiscale/localdetrend/'); sys.path.insert(0, '/mnt/project-files/multiscale/canonical/')
import mc, ld
rng = random.Random(1); agree = [0, 0]; tot = [0, 0]; bp = 0; bpt = 0
def rot_walk(lab, sg, odd, r):
    L = len(lab); lab2 = lab[r:] + lab[:r]; s2 = sg[r:] + [(-1 if odd else 1)*x for x in sg[:r]]
    return lab2, s2
for trial in range(3000):
    L = rng.randrange(6, 26)
    while True:
        col = [rng.randrange(4) for _ in range(L)]
        if all(col[i] != col[(i+1) % L] for i in range(L)): break
    lab = [col[i] ^ col[(i+1) % L] for i in range(L)]; sg = [rng.choice((1, -1)) for _ in range(L)]
    odd = rng.random() < 0.4
    H = mc.int_walk(lab, sg); Hc = np.array([mc.cz(p) for p in H])
    if not odd and abs(Hc[-1]) > 2 + 1e-9: continue
    ok_ld = ld.tau_step_le(Hc, 1.0, odd)[0]; ok_mc = mc.ncuts(H, odd, 1) is not None
    tot[odd] += 1; agree[odd] += ok_ld == ok_mc
    if trial % 6 == 0:
        for J in (1, 2, 3, 4):
            for var in ('nc', 'any'):
                base = mc.ncuts(H, odd, J, var); r = rng.randrange(1, L)
                l2, s2 = rot_walk(lab, sg, odd, r); H2 = mc.int_walk(l2, s2)
                bpt += 1; bp += (mc.ncuts(H2, odd, J, var) == base)
print('J=1 vs tau_step: even agree %d/%d, odd agree %d/%d' % (agree[0], tot[0], agree[1], tot[1]))
print('base-point shift: ncuts equal %d/%d' % (bp, bpt))
