# Round 3: the grammar's EDGE and HAT paths with extra context positions that read the payer's second ring.
# EDGE (u -> v): the 14 positions of grammar.EPOS, plus the payer's further apexes S.A+2, S.A+3, S.A-2, S.A-3 and the payee's
#   further apexes R.A+2, R.A-2 (with u's link SL rooted at v: S.A+k = apex of SL[k], SL[k+1] away from u; S.A-k = apex of
#   SL[-k-1], SL[-k]; for a d = 7 payer, S.L+-1..3 and S.A+-1..3 are its whole link and its whole second ring).
# HAT (u -> b across the edge x y): the 8 positions of grammar.HPOS, plus the payer's further link U+2, U+3, U-2, U-3 and its
#   further apexes UA+2, UA+3, UA-2, UA-3 (u's link rooted x, y, U+1, U+2, ...; UA+k = apex of its k-th and (k+1)-th link
#   vertices away from u; for a d = 7 payer, X Y U+-1..3 and XA YA UA+-2..3 are its whole link and second ring).
# Same conservative semantics as grammar.py (payer: context surely matches; payee: possibly).  A position the picture cannot see
# is the wildcard.
import grammar as G
EPOS = G.EPOS + ['S.A+2', 'S.A+3', 'S.A-2', 'S.A-3', 'R.A+2', 'R.A-2']
EMIRROR = G.EMIRROR + [16, 17, 14, 15, 19, 18]
HPOS = G.HPOS + ['U+2', 'U+3', 'U-2', 'U-3', 'UA+2', 'UA+3', 'UA-2', 'UA-3']
HMIRROR = G.HMIRROR + [10, 11, 8, 9, 14, 15, 12, 13]
def edge_vec(P, u, v, sg):
    base = G.edge_vec(P, u, v, sg)
    if base is None: return None
    SL, SA = G.frame(P, u, v, sg)
    for sv in (1, -1):
        RL, RA = G.frame(P, v, u, sv)
        if RL[1] == SL[1]: break
    du, dv = len(SA), len(RA)
    ext = [SA[2 % du], SA[3 % du], SA[-3 % du], SA[-4 % du], RA[2 % dv], RA[-3 % dv]]
    return base + [G.lt(P, z) for z in ext]
def hat_vec(P, u, x, y, b):
    base = G.hat_vec(P, u, x, y, b)
    if u not in P.rot: return base + [G.ALL] * 8
    for sg in (1, -1):
        L, A = G.frame(P, u, x, sg)
        if L[1] == y: break
    else: return base + [G.ALL] * 8
    d = len(L)
    ext = [L[3 % d], L[4 % d], L[-2 % d], L[-3 % d], A[2 % d], A[3 % d], A[-2 % d], A[-3 % d]]
    return base + [G.lt(P, z) for z in ext]
def slots(P):
    """grammar.slots with the extended vectors"""
    out = []; c = 0
    so = 1 if P.kind == 'S' else -1; si = -so
    for v in P.rot[c]:
        for sg in (1, -1):
            out.append(('EDGE', 'out', P.let[c], P.let[v], edge_vec(P, c, v, sg), so))
            out.append(('EDGE', 'in', P.let[v], P.let[c], edge_vec(P, v, c, sg), si))
    L = P.rot[c]; d = len(L)
    for k in range(d):
        x, y = L[k], L[(k + 1) % d]; b = G.apex_of(P, x, y, c)
        if b is None: continue
        for (xx, yy) in ((x, y), (y, x)):
            out.append(('HAT', 'out', P.let[c], P.let[b], hat_vec(P, c, xx, yy, b), so))
            out.append(('HAT', 'in', P.let[b], P.let[c], hat_vec(P, b, xx, yy, c), si))
    return out
def rule_str(path, um, vm, ctx):
    names = EPOS if path == 'EDGE' else HPOS
    s = '%s(%s->%s)' % (path, G.msym(um), G.msym(vm))
    if ctx: s += '[' + ' '.join('%s=%s' % (names[p], G.msym(m)) for p, m in sorted(ctx.items())) + ']'
    return s
def canon(path, um, vm, ctx):
    mir = EMIRROR if path == 'EDGE' else HMIRROR
    a = tuple(sorted(ctx.items())); b = tuple(sorted((mir[p], m) for p, m in ctx.items()))
    return (path, um, vm, min(a, b))
HDESC = {'X': 'x', 'Y': 'y', 'U-1': "the payer's link vertex beyond x", 'U+1': "the payer's link vertex beyond y",
         'XA': "the payer's apex beyond x", 'YA': "the payer's apex beyond y", 'V-1': "the payee's neighbour beyond x",
         'V+1': "the payee's neighbour beyond y", 'U+2': "the payer's 2nd link vertex beyond y", 'U+3': "the payer's 3rd link vertex beyond y",
         'U-2': "the payer's 2nd link vertex beyond x", 'U-3': "the payer's 3rd link vertex beyond x",
         'UA+2': "the payer's 2nd apex beyond y", 'UA+3': "the payer's 3rd apex beyond y", 'UA-2': "the payer's 2nd apex beyond x",
         'UA-3': "the payer's 3rd apex beyond x"}
