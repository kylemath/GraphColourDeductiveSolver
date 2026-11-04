# s70: in-out (stabilised) separation for the K loop (cmd_solveR2).  Flags/options:
#   inout=lam0,lam1,step   separate at x_sep = lam*x_LP + (1-lam)*x_feas (columns keyed as in the LP; t blends too).  lam starts at lam0,
#                          is raised by step (cap lam1) whenever a blended round finds nothing or fewer than inoutmin cuts, and a
#                          raw (lam = 1) separation is done when the blended round at lam1 finds nothing.
#   inoutk=k               every k-th iteration: separate at the raw LP point (its cuts are added as well); convergence (the old
#                          keeppen stop) is declared only when a raw-point separation finds nothing.   default 4
#   inoutmin=n             a blended round with fewer than n new rows also raises lam.   default 30
#   feas=<sol json>        the feasible point (rr / z / zr / q columns are set to 0 on loading).
#   control (no LP, no warm rows needed): inoutctl=lam [rawsol=<sol json>]  dry run: counts violated rows at lam*raw + (1-lam)*feas.
# Soundness: only valid rows are ever added to the LP (the separator returns rows of the relay system), the blend only chooses WHERE
# to look; a row violated at the blend is violated by at least as much at x_LP (x_feas satisfies every valid row).
def load_feas_cols(fn, skip=()):
    Sj = json.load(open(fn)); Dd = {('t',): float(Sj['t'])}
    for k, v in Sj.get('y', {}).items():
        u, rest = k.split('|'); r_ = root(list((int(u),) + tuple(int(c) for c in rest)), 0); Dd[('y', ROOTS[RIX[r_]])] = float(v)
    for fam in ('g', 'h', 'z', 'zr', 'rr', 'r', 'q', 'v', 'f', 'fb', 'lq', 'lQ', 'z6', 'Z6'):
        if fam in skip: continue
        for kk, v in Sj.get(fam, []): Dd[(fam, tuple(kk))] = float(v)
    for k, v in Sj.get('x', {}).items(): Dd[('x', int(k))] = float(v)
    for k, v in Sj.get('xo', {}).items(): Dd[('xo', int(k))] = float(v)
    for k, v in Sj.get('D', []): Dd[('D', eval(k))] = float(v)
    return Dd
def inout_feas(fn): return load_feas_cols(fn, skip=('rr', 'z', 'zr', 'q'))
def inout_blend(xr, xf, lam): return xr if lam >= 1.0 else lam * xr + (1.0 - lam) * xf
INOUT = tuple(float(a) for a in OPT['inout'].split(',')) if 'inout' in OPT else None
INOUTK = int(OPT.get('inoutk', '4')); INOUTMIN = int(OPT.get('inoutmin', '30')); LAM = [INOUT[0] if INOUT else 1.0]
FEAS = None
