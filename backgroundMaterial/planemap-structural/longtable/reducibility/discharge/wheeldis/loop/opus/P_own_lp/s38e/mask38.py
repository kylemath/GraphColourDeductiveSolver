"""Stage 38e payee masks (Opus s38e) for the 8 -> 7 second-stage family (Steinberger stage 2: big pays an adjacent 7).
Payee v = centre of a d = 7 receiver row (L, t); payer u = L_j with letter >= 8 (8 exact, 9 = '>= 9', never exact).
Free slots (strict 14': every other private is unknown = degree 99, an embedding touching one is no match; letter 9 is never
an exact degree, so a requirement of 9 never kills):
  E2: e+ = the private of c+ = L_{j+1} adjacent to t_j (none if c+ = 5: then e+ = t_{j+1}, exact)
      e- = the private of c- = L_{j-1} adjacent to t_{j-1} (none if c- = 5: then e- = t_{j-2}, exact)
  E3: E2 + a2+ = u's private adjacent to t_j, a2- = u's private adjacent to t_{j-1}
Known: v (7), the whole link L and all apexes t (variant 'full', valid at the d = 7 jsep5 leaf); variant 'win' knows only
v, u, c+-, L_{j+-2}, t_j, t_{j-1}, t_{j+1}, t_{j-2} (the vertices the payer key itself names) -- a coarser (larger) mask.
Only an embedding that uses at least one free slot kills (RELAY_SPEC_s21 21.4 reading). A kill is a partial assignment
{slot: letter}; a completion is killed if it extends one.
  LG+-: one side's a2 only (per-side l3q-shape column, RELAY_SPEC_s21 with U = 8/9, V = 7, letters 5..9)
Registry 3cfd7f18 = ex62 + s31/k3x_{D,C}_3cfd7f18 (3,989 configurations), containment k42 grow.embeddings.
usage: python3 mask38.py OUT.json D/LK/SV [...]"""
import sys, os, json, time
B = '/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/'
EX = '/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/ex62'
OUTF, ROWS = sys.argv[1], sys.argv[2:]
sys.argv = [sys.argv[0], EX, B + 's31/k3x_D_3cfd7f18.out', B + 's31/k3x_C_3cfd7f18.cfast', 'unused']
exec(open(B + 's29/f/s16_filter.py').read().replace("if __name__ == '__main__':", "if False:"))
def slots(P, pa, D, LK, j):
    """name of each free slot (or None if exact) for e+, e-, a2+, a2-"""
    def priv_adj(k, apex):
        x = [p for p in P if p[0] == 'p' and p[1] == k and apex in pa[p]]; assert len(x) == 1, (k, apex, x); return x[0]
    jp, jm = (j + 1) % D, (j - 1) % D
    ep = None if LK[jp] == 5 else priv_adj(jp, ('s', j))
    em = None if LK[jm] == 5 else priv_adj(jm, ('s', jm))
    return {'e+': ep, 'e-': em, 'a2+': priv_adj(j, ('s', j)), 'a2-': priv_adj(j, ('s', jm))}
def masks(C, D, LK, SV, j, fam, variant):
    P, pa, pf = build(D, LK); sl = slots(P, pa, D, LK, j)
    names = {'E2': ['e+', 'e-'], 'E3': ['e+', 'e-', 'a2+', 'a2-'], 'LG+': ['a2+'], 'LG-': ['a2-']}[fam]
    free = {sl[n]: n for n in names if sl[n] is not None}
    if variant == 'full': known = {('u',)} | {('w', i) for i in range(D)} | {('s', i) for i in range(D)}
    else:
        known = {('u',), ('w', j)} | {('w', (j + k) % D) for k in (1, 2, -1, -2)} | {('s', (j + k) % D) for k in (0, -1, 1, -2)}
    deg = {('u',): D}
    for i in range(D): deg[('w', i)] = LK[i] if LK[i] < 9 else NEVER; deg[('s', i)] = SV[i] if SV[i] < 9 else NEVER
    fd = {}; UNKV = set()
    for x in P:
        if x in free: continue
        if x in known: fd[x] = deg[x]
        else: fd[x] = NEVER; UNKV.add(x)
    kills = set(); nine = 0; base = 0; who = {}
    for c in C:
        for e_ in grow.embeddings(c, P, pa, pf, fd):
            if any(v in UNKV for u, v in e_): continue
            req = dict((free[v], c[3][u]) for u, v in e_ if v in free)
            if not req: base += 1; continue
            if any(val >= 9 for val in req.values()): nine += 1; continue      # >= 9 is never exact: no kill
            k = tuple(sorted(req.items()))
            if k not in kills: kills.add(k); who[str(k)] = c[0]
    return {'free': sorted(free.values()), 'kills': sorted([list(map(list, k)) for k in kills]), 'nine_skipped': nine,
            'no_slot_embeddings': base, 'who': who}
if __name__ == '__main__':
    C = registry(); print('forbidden', len(C), flush=True); out = {}
    for r in ROWS:
        d, lk, sv = r.split('/'); D = int(d); LK = [int(c) for c in lk]; SV = [int(c) for c in sv]
        for j in range(D):
            if LK[j] < 8: continue
            for fam in ('E2', 'E3', 'LG+', 'LG-'):
                for variant in ('full', 'win'):
                    t0 = time.time(); R = masks(C, D, LK, SV, j, fam, variant)
                    out['%s %s %d %s %s %d' % (fam, variant, D, lk, sv, j)] = R
                    print(fam, variant, D, lk, sv, 'u=w_%d' % j, 'free', R['free'], 'kills', R['kills'][:12], 'n', len(R['kills']),
                          'nine', R['nine_skipped'], 'noslot', R['no_slot_embeddings'], '%.1fs' % (time.time() - t0), flush=True)
    json.dump(out, open(OUTF, 'w'), indent=0)
