"""ST-10 diagnosis: for each pattern dropped only by Studio, find the face-set embeddings of its nl51 source that produce it and
report which rotcheck condition fails (nodeg / shift / ring) per orientation sign."""
import os, sys, collections
os.environ['RPATN_ROT'] = '1'
sys.argv = ['rpatN_studio.py']; M = {'__name__': 'rp', '__file__': os.path.abspath('out/job31/rpatN_studio.py')}
exec(open('out/job31/rpatN_studio.py').read().split("if __name__ == '__main__':")[0], M)
RC = M['RC']; GG = M['GG']
R = 'loop/studio/opus_check/f2b041/keep95p131f/rpatN3_rot/'
pat = lambda fn: {' '.join(l.split('#')[0].split()): l.split('#')[1].strip() for l in open(fn) if l.strip() and not l.startswith('#')}
A = pat(R + 'rpatN3_flagoff.txt'); B = pat(R + 'rpatN3_rot.txt'); U = pat(R + 'in/rpatN3_unjustified46.txt')
only = {p: A[p] for p in A if p not in B and p not in U and p != '7 .556.65 .56..65'}
src = {l.split()[0]: l for l in open(R + 'only_us_src.txt')}
def why(phi, rotK, frm):
    rotF = frm[3]; res = {}
    for sg in (1, -1):
        ring = {}; st = 'pass'
        for u in sorted(phi, key=lambda u: -sum(x[0] == 'I' for x in rotK[u])):
            rc = rotK[u]; v = phi[u]
            if v not in rotF or len(rotF[v]) != len(rc): st = 'nodeg(%s)' % (u,); break
            rf = rotF[v]; g = len(rc); intr = [(i, x[1]) for i, x in enumerate(rc) if x[0] == 'I']
            sh = [(rf.index(phi[intr[0][1]]) - sg * intr[0][0]) % g] if intr and phi[intr[0][1]] in rf else ([] if intr else range(g))
            ok = [t for t in sh if not any(rf[(t + sg * i) % g] != phi[w] for i, w in intr)]
            if not ok: st = 'shift(at %s)' % u; break
            good = None
            for t in ok:
                cand = {x[1]: rf[(t + sg * i) % g] for i, x in enumerate(rc) if x[0] == 'R'}
                if all(ring.get(j, fv) == fv for j, fv in cand.items()): good = cand; break
            if good is None: st = 'ring(at %s)' % u; break
            ring.update(good)
        res[sg] = st
    return res
for p, ann in sorted(only.items()):
    nm = ann.split()[0]; line = src[nm]; rk = RC.kc_rotation(line); _, m, g, E, tri = M['parse'](line)
    out = collections.Counter()
    # re-enumerate face-set embeddings (ROT off inside) and keep those giving pattern p
    M['ROT'] = False
    cap = {}
    orig = M['embeddings']
    for c in [c for c in range(m) if 7 <= g[c] <= 17]:
        # capture pos by instrumenting: rebuild via the recursion with ROT temporarily on but rot_pass replaced
        def rp(c_, d, L, S, pos, c=c):
            k = (d, M['canon'](d, L, S)); cap.setdefault(k, []).append((c_, d, list(L), list(S), dict(pos))); return True
        M['ROT'] = True; M['rot_pass'] = rp
        for _ in orig(m, g, E, tri, c): pass
    d0 = int(p.split()[0]); key = (d0, ' '.join(p.split()[1:]))
    for c_, d, L, S, pos in cap.get(key, []):
        lk = [int(L[i]) if L[i] in '5678' else 6 for i in range(d)]; r2 = {('s', i): int(S[i]) for i in range(d) if S[i] in '5678'}
        frm = RC.frame_rotation(GG, d, lk, {}, r2); inv = frm[2]; phi = {c_: inv[('u',)]}
        for v, sl in pos.items(): phi[v] = inv[sl]
        r = why(phi, rk, frm); out['%s / %s' % (r[1], r[-1])] += 1
    print('%s\t%s\t%d face-set embeddings\t%s' % (p, nm, sum(out.values()), dict(out)))
