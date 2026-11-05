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
    for k, v in Sj.get('ks', []): Dd[('ks', str(k))] = float(v)   # s78 K*
    return Dd
def inout_feas(fn): return load_feas_cols(fn, skip=('rr', 'z', 'zr', 'q'))
def inout_blend(xr, xf, lam): return xr if lam >= 1.0 else lam * xr + (1.0 - lam) * xf
INOUT = tuple(float(a) for a in OPT['inout'].split(',')) if 'inout' in OPT else None
INOUTK = int(OPT.get('inoutk', '4')); INOUTMIN = int(OPT.get('inoutmin', '30')); LAM = [INOUT[0] if INOUT else 1.0]
FEAS = None
# s75 (Team A): moving in-point + probe + q7 penalty.
#   inoutmove            a blended round (tail included) that finds no violated row makes the blend the new in-point (FEAS); it is written to
#                        eng/sol_<tag>_in.json (and sol_<tag>_inNN.json) -- a CANDIDATE upper bound, to be checked by upperR2.  At most inoutmaxmove (3) moves per iteration.
#   inoutprobe=f         after a blended round at lam that found rows, also separate at lam*f (rows found there are violated at x_LP as well, so they are valid
#                        LP cuts); if the probe finds none (and inoutmove), the probe point becomes the in-point.
#   feasall              load feas= with every family (rr/z/zr/q kept): use it to resume from a moved in-point sol_<tag>_in.json.
#   q7pen=c              objective cost c on every q column (like xpen on z/zr/rr); removes the free degenerate q mass on the t = 0 face.
#   every iteration the LP point is written to eng/sol_<tag>_lp.json (atomic); inoutctl=lam ... ctlwrite=<json> writes the blended vector (line search -> upperR2).
INOUTMOVE = 'inoutmove' in FLAGS; INOUTPROBE = float(OPT.get('inoutprobe', '0')); INOUTMAXMOVE = int(OPT.get('inoutmaxmove', '3')); INMOVES = []
Q7PEN = [float(OPT.get('q7pen', '0'))]
NVIOL = [0]   # s75: violated rows seen by the last sepround (new or not)
#   feascols             create every in-point column at the start (s70 silently dropped in-point values whose column did not exist yet).
INOUTNPROBE = int(OPT.get('inoutnprobe', '1'))   # s75: number of geometric probes (lam*f^k, k = 1..n), stop at the first feasible one
