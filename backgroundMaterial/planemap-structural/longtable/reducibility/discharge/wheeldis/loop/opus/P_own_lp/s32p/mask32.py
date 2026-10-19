"""Stage 32 LG payee mask (Opus s32p), generalising s28q/mask28.py to any big link vertex u = w_j (letter 7 or 8) of a
payee row v (centre, degree D). For side sg: a = s_j (sg=+1) / s_{j-1} (sg=-1); the free slot a2 = u's private adjacent
to a. Strict 14': every vertex not known has degree 99 and an embedding touching it is no match; letter 9 is never exact.
Variants: full = v, whole link, all apexes known; win = v, u, w_{j+sg..j+4sg}, s_{j-1}, s_j known (the RELAY_SPEC_s21 window).
Registry 7360eb92 = ex60 + s29/k3x_{D,C}_7360eb92 (3,424 configurations), containment = k42 grow.embeddings.
usage: python3 mask32.py OUT.json D/LK/SV [D/LK/SV ...]"""
import sys, os, json, time
B = '/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/'
EX = '/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/ex60'
OUTF, ROWS = sys.argv[1], sys.argv[2:]
sys.argv = [sys.argv[0], EX, B + 's29/k3x_D_7360eb92.out', B + 's29/k3x_C_7360eb92.cfast', 'unused']
exec(open(B + 's29/f/s16_filter.py').read().replace("if __name__ == '__main__':", "if False:"))
SUSPECT = 'f7_..56757_...5...'
def masks(C, D, LK, SV, variant):
    P, pa, pf = build(D, LK); res = {}
    for j in range(D):
        if LK[j] < 7 or LK[j] > 8: continue
        for sg in (1, -1):
            a = ('s', j) if sg == 1 else ('s', (j - 1) % D)
            priv = [x for x in P if x[0] == 'p' and x[1] == j]
            slot = [x for x in priv if a in pa[x]]; assert len(slot) == 1, (j, sg, priv); slot = slot[0]
            known = {('u',), ('w', j)}
            if variant == 'full': known |= {('w', i) for i in range(D)} | {('s', i) for i in range(D)}
            else: known |= {('w', (j + k * sg) % D) for k in range(1, 5)} | {('s', j), ('s', (j - 1) % D)}
            deg = {('u',): D if D < 9 else NEVER}
            for i in range(D): deg[('w', i)] = LK[i] if LK[i] < 9 else NEVER; deg[('s', i)] = SV[i] if SV[i] < 9 else NEVER
            fd = {}; UNKV = set()
            for x in P:
                if x == slot: continue
                if x in known: fd[x] = deg[x]
                else: fd[x] = NEVER; UNKV.add(x)
            kill = {}
            for c in C:
                for e_ in grow.embeddings(c, P, pa, pf, fd):
                    if any(v in UNKV for u, v in e_): continue
                    req = dict((v, c[3][u]) for u, v in e_ if v not in fd)
                    if slot in req: kill.setdefault(req[slot], set()).add(c[0])
            m = 31; m_nos = 31
            for val, names in kill.items():
                m &= ~(1 << LET.index(val))
                if names - {SUSPECT}: m_nos &= ~(1 << LET.index(val))
            res['%d %+d' % (j, sg)] = {'mask': m, 'mask_without_suspect': m_nos, 'kills': {str(k): sorted(v)[:6] for k, v in sorted(kill.items())}}
    return res
C = registry(); print('forbidden', len(C), 'suspect present', any(c[0] == SUSPECT for c in C), flush=True); out = {}
for r in ROWS:
    d, lk, sv = r.split('/'); D = int(d); LK = [int(c) for c in lk]; SV = [int(c) for c in sv]
    for variant in ('win', 'full'):
        t0 = time.time(); R = masks(C, D, LK, SV, variant)
        for k, v in R.items():
            j, sg = k.split()
            out['%s %d %s %s %s %s' % (variant, D, lk, sv, j, int(sg))] = v
            print(variant, D, lk, sv, 'u=w_%s' % k, 'mask', [l for i, l in enumerate(LET) if v['mask'] >> i & 1],
                  'w/o suspect', [l for i, l in enumerate(LET) if v['mask_without_suspect'] >> i & 1], 'kills', v['kills'], '%.0fs' % (time.time() - t0), flush=True)
json.dump(out, open(OUTF, 'w'), indent=1)
