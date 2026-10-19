"""Stage 28 l3q payee mask (Opus s28q). For a payee row (v = centre, d, link LK, apexes SV) and every link 7 u = w_j,
each side sg in {+1,-1}: the private a2 of u adjacent to a = s_j (sg=+1) or s_{j-1} (sg=-1) is the only free vertex.
Every other private is unknown (degree 99, strict rule: an embedding touching it is no match). Forbidden set = s25/f
registry (RSST 582 + k3x names at 0125c46b). Containment = k42 grow.embeddings, exactly as s16_filter.fullrow.
Variants: full = whole row known; win = only v, u, w_{j+sg..j+4sg}, s_{j-1}, s_j known (the note's window), everything
else unknown/strict.  Letter 9 (= deg >= 9) is never exact.
usage: python3 mask28.py OUT.json LK/SV [LK/SV ...]"""
import sys, os, json, time
F = '/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s25/f/'
EX = '/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/ex59'
OUTF, ROWS = sys.argv[1], sys.argv[2:]
sys.argv = [sys.argv[0], EX, F + '../k3x_D_0125c46b.out', F + '../k3x_C_0125c46b.cfast', 'unused']
exec(open(F + 's16_filter.py').read().replace("if __name__ == '__main__':", "if False:"))
def masks(C, LK, SV, variant):
    D = len(LK); P, pa, pf = build(D, LK); res = {}
    for j in range(D):
        if LK[j] != 7: continue
        for sg in (1, -1):
            a = ('s', j) if sg == 1 else ('s', (j - 1) % D)
            priv = [x for x in P if x[0] == 'p' and x[1] == j]
            slot = [x for x in priv if a in pa[x]]; assert len(slot) == 1, (j, sg, priv)
            slot = slot[0]
            known = {('u',), ('w', j)}
            if variant == 'full':
                known |= {('w', i) for i in range(D)} | {('s', i) for i in range(D)}
            else:
                known |= {('w', (j + k * sg) % D) for k in range(1, 5)} | {('s', j), ('s', (j - 1) % D)}
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
            m = 31
            for val in kill: m &= ~(1 << LET.index(val))
            res['%d %+d' % (j, sg)] = {'slot': list(map(str, slot)), 'a': list(map(str, a)), 'mask': m,
                                       'kills': {str(k): sorted(v)[:6] for k, v in sorted(kill.items())}}
    return res
C = registry(); print('forbidden', len(C), flush=True); out = {}
for r in ROWS:
    lk, sv = r.split('/'); LK = [int(c) for c in lk]; SV = [int(c) for c in sv]
    for variant in ('full', 'win'):
        t0 = time.time(); out['%s/%s %s' % (lk, sv, variant)] = R = masks(C, LK, SV, variant)
        for k, v in R.items(): print(lk, sv, variant, 'u=w_%s' % k, 'slot', v['slot'], 'adj', v['a'], 'mask', bin(v['mask']), 'allowed', [l for i, l in enumerate(LET) if v['mask'] >> i & 1], 'kills', v['kills'], '%.0fs' % (time.time() - t0), flush=True)
json.dump(out, open(OUTF, 'w'), indent=1)
