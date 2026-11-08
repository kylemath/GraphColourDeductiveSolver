"""hshim.py -- a pure numpy / scipy stand-in for the part of the highspy API that the s86 engine uses.

Used only when `import highspy` fails (or HSHIM_FORCE=1): every engine `import highspy` is
    try: <HSHIM_FORCE check>; import highspy
    except ImportError: import hshim as highspy

What it does.  Highs() stores the model (column bounds and costs, sparse rows lo <= a.x <= hi) and run() solves it FROM
SCRATCH with scipy.optimize.linprog(method='highs-ipm' or 'highs-ds').  linprog has no ranged rows, so every row is
passed as one or two one-sided rows:
    hi finite, lo = -inf  ->  a.x <= hi            (A_ub)
    lo finite, hi = +inf  ->  -a.x <= -lo          (A_ub)
    lo == hi              ->  a.x == lo            (A_eq)
    both finite, lo < hi  ->  both of the first two
    both infinite         ->  dropped (dual 0)
The row duals come back in HiGHS's convention for a minimisation (the derivative of the optimum with respect to the
row's active bound): row_dual <= 0 when the upper side binds, >= 0 when the lower side binds, either sign for an
equality.  scipy's ineqlin/eqlin marginals are HiGHS's own row duals of the rows passed, so the upper part keeps its
sign and the negated lower part flips it.  col_dual is the reduced cost (lower + upper bound marginals; 0 for a basic
column), as HiGHS reports it.

Options read: solver ('ipm' -> highs-ipm, 'simplex' -> highs-ds, 'choose' / unset -> $HSHIM_SOLVER, default ipm),
primal_feasibility_tolerance, dual_feasibility_tolerance, output_flag.  time_limit is stored and ignored: run() always
solves to the end, so a finished solve reports Optimal, never kTimeLimit (the engine's lpmax fallback is then never
taken).  threads is stored and ignored (HiGHS's IPM + crossover runs essentially on one core).  If highs-ipm ends in a
non-optimal status the shim retries once with highs-ds (and vice versa) before reporting the status.

Environment: HSHIM_SOLVER=ipm|simplex|highs (default for 'choose'), HSHIM_QUIET=1 (no per-run line on stderr),
HSHIM_TMAX_IPM=<s> (v2b: cap a first-try highs-ipm at <s> s, then highs-ds uncapped), HSHIM_DISP=1 (v2b: HiGHS log on stdout),
HSHIM_DUMP=<dir> (np.savez of every model passed to linprog, for debugging), HSHIM_PRESOLVE=0 (presolve off).

clearSolver() (v2 add-on) forgets the solution and status and keeps the model (every run() is from scratch anyway).
getLp() (v2 add-on) returns the model as highspy's HighsLp does: col_cost_, col_lower_, col_upper_, row_lower_, row_upper_,
num_col_, num_row_ and a_matrix_ column-wise (format_ 1, start_ / index_ / value_ of the CSC matrix), as highspy returns it
for a model built with addVar / addRow.

getBasis() is a reconstruction from the solution (strictly-between-bounds columns and inactive rows are basic;
columns / rows with a nonzero dual are nonbasic; ties are filled to reach num_row basics when possible).  It is used
only by lowerR2 exactbasis, which checks the count and returns None when it does not match.
Written for Python >= 3.9, numpy >= 1.20, scipy >= 1.9 (tested here against highspy 1.15.1 with scipy 1.18; the Mac
has scipy 1.13.1, whose linprog / _highs_wrapper code paths used here were read from the v1.13.1 sources).
"""
import os, sys, time, array, warnings
from enum import IntEnum
import numpy as np
import scipy.sparse as sp
from scipy.optimize import linprog

kHighsInf = float('inf')
__version__ = 'hshim-1.1'   # 1.1 (v2 add-on): clearSolver, getLp


class HighsStatus(IntEnum):
    kError = -1
    kOk = 0
    kWarning = 1


class HighsModelStatus(IntEnum):
    kNotset = 0
    kLoadError = 1
    kModelError = 2
    kPresolveError = 3
    kSolveError = 4
    kPostsolveError = 5
    kModelEmpty = 6
    kOptimal = 7
    kInfeasible = 8
    kUnboundedOrInfeasible = 9
    kUnbounded = 10
    kObjectiveBound = 11
    kObjectiveTarget = 12
    kTimeLimit = 13
    kIterationLimit = 14
    kUnknown = 15
    kSolutionLimit = 16
    kInterrupt = 17
    kMemoryLimit = 18
    kHighsInterrupt = 19


_STATUS_STR = {0: 'Not Set', 1: 'Load error', 2: 'Model error', 3: 'Presolve error', 4: 'Solve error', 5: 'Postsolve error',
               6: 'Empty', 7: 'Optimal', 8: 'Infeasible', 9: 'Primal infeasible or unbounded', 10: 'Unbounded',
               11: 'Bound on objective reached', 12: 'Target for objective reached', 13: 'Time limit reached',
               14: 'Iteration limit reached', 15: 'Unknown', 16: 'Solution limit reached', 17: 'Interrupted by user',
               18: 'Memory limit reached', 19: 'Interrupted by HiGHS'}


class HighsBasisStatus(IntEnum):
    kLower = 0
    kBasic = 1
    kUpper = 2
    kZero = 3
    kNonbasic = 4


class HighsSolution(object):
    def __init__(self):
        self.col_value = []; self.col_dual = []; self.row_value = []; self.row_dual = []
        self.value_valid = False; self.dual_valid = False


class HighsBasis(object):
    def __init__(self):
        self.col_status = []; self.row_status = []; self.valid = False


class HighsInfo(object):
    def __init__(self):
        self.objective_function_value = 0.0; self.valid = False
        self.simplex_iteration_count = 0; self.ipm_iteration_count = 0; self.crossover_iteration_count = 0
        self.primal_solution_status = 0; self.dual_solution_status = 0
        self.max_primal_infeasibility = 0.0; self.max_dual_infeasibility = 0.0


def _f(x):
    x = float(x)
    if x >= 1e30: return kHighsInf
    if x <= -1e30: return -kHighsInf
    return x


class HighsSparseMatrix(object):
    def __init__(self):
        self.format_ = 1; self.num_col_ = 0; self.num_row_ = 0; self.start_ = []; self.p_end_ = []; self.index_ = []; self.value_ = []


class HighsLp(object):
    def __init__(self):
        self.num_col_ = 0; self.num_row_ = 0; self.col_cost_ = []; self.col_lower_ = []; self.col_upper_ = []
        self.row_lower_ = []; self.row_upper_ = []; self.a_matrix_ = HighsSparseMatrix(); self.offset_ = 0.0; self.model_name_ = ''


class Highs(object):
    def __init__(self):
        self._opt = {'output_flag': True, 'solver': 'choose', 'time_limit': kHighsInf, 'threads': 0,
                     'primal_feasibility_tolerance': 1e-7, 'dual_feasibility_tolerance': 1e-7, 'presolve': 'choose'}
        self._clb = []; self._cub = []; self._cost = []            # columns
        self._rlo = []; self._rhi = []; self._rlen = []             # rows
        self._ri = array.array('i'); self._rv = array.array('d')   # row entries, row-major
        self._status = HighsModelStatus.kNotset
        self._sol = HighsSolution(); self._info = HighsInfo(); self._basis = None
        self._runtime = 0.0; self._nrun = 0

    # ---------------- options ----------------
    def setOptionValue(self, name, value):
        self._opt[name] = value
        return HighsStatus.kOk

    def getOptionValue(self, name):
        return self._opt.get(name)

    def resetGlobalScheduler(self, blocking=False):
        return None

    # ---------------- model building ----------------
    def _changed(self):
        self._status = HighsModelStatus.kNotset; self._info = HighsInfo(); self._basis = None
        self._sol.value_valid = False; self._sol.dual_valid = False

    def addVar(self, lower, upper):
        self._clb.append(_f(lower)); self._cub.append(_f(upper)); self._cost.append(0.0)
        if self._sol.col_value is not None and len(self._sol.col_value):   # highspy pads an existing solution with 0
            self._sol.col_value.append(0.0); self._sol.col_dual.append(0.0)
        self._changed(); return HighsStatus.kOk

    def addVars(self, num_new_col, lower, upper):
        lower = np.asarray(lower, dtype=float).ravel(); upper = np.asarray(upper, dtype=float).ravel()
        for k in range(int(num_new_col)): self.addVar(lower[k], upper[k])
        return HighsStatus.kOk

    def addRow(self, lower, upper, num_new_nz, indices, values):
        n = int(num_new_nz)
        idx = np.ascontiguousarray(np.asarray(indices)[:n], dtype=np.int32)
        val = np.ascontiguousarray(np.asarray(values, dtype=float)[:n], dtype=np.float64)
        if n and (idx.min() < 0 or idx.max() >= len(self._clb)):
            raise IndexError('hshim.addRow: column index out of range (%d..%d, %d columns)' % (idx.min(), idx.max(), len(self._clb)))
        self._ri.frombytes(idx.tobytes()); self._rv.frombytes(val.tobytes())
        self._rlo.append(_f(lower)); self._rhi.append(_f(upper)); self._rlen.append(n)
        if self._sol.row_value is not None and len(self._sol.row_value):
            self._sol.row_value.append(0.0); self._sol.row_dual.append(0.0)
        self._changed(); return HighsStatus.kOk

    def addRows(self, num_new_row, lower, upper, num_new_nz, starts, indices, values):
        nr = int(num_new_row); nz = int(num_new_nz)
        lower = np.asarray(lower, dtype=float).ravel(); upper = np.asarray(upper, dtype=float).ravel()
        st = list(np.asarray(starts).ravel()[:nr]) + [nz]
        indices = np.asarray(indices).ravel(); values = np.asarray(values, dtype=float).ravel()
        for k in range(nr):
            a, b = int(st[k]), int(st[k + 1])
            self.addRow(lower[k], upper[k], b - a, indices[a:b], values[a:b])
        return HighsStatus.kOk

    def changeColCost(self, col, cost):
        self._cost[int(col)] = float(cost); self._changed(); return HighsStatus.kOk

    def changeColsCost(self, num_set_entries, indices, cost):
        indices = np.asarray(indices).ravel(); cost = np.asarray(cost, dtype=float).ravel()
        for k in range(int(num_set_entries)): self._cost[int(indices[k])] = float(cost[k])
        self._changed(); return HighsStatus.kOk

    def changeColBounds(self, col, lower, upper):
        self._clb[int(col)] = _f(lower); self._cub[int(col)] = _f(upper); self._changed(); return HighsStatus.kOk

    def changeColsBounds(self, num_set_entries, indices, lower, upper):
        indices = np.asarray(indices).ravel(); lower = np.asarray(lower, dtype=float).ravel(); upper = np.asarray(upper, dtype=float).ravel()
        for k in range(int(num_set_entries)): self._clb[int(indices[k])] = _f(lower[k]); self._cub[int(indices[k])] = _f(upper[k])
        self._changed(); return HighsStatus.kOk

    def changeRowBounds(self, row, lower, upper):
        self._rlo[int(row)] = _f(lower); self._rhi[int(row)] = _f(upper); self._changed(); return HighsStatus.kOk

    # ---------------- queries ----------------
    def getNumCol(self): return len(self._clb)
    def getNumRow(self): return len(self._rlo)
    def getNumNz(self): return len(self._ri)
    def getRunTime(self): return self._runtime
    def getModelStatus(self): return self._status
    def modelStatusToString(self, st): return _STATUS_STR.get(int(st), 'Unknown')
    def getSolution(self): return self._sol
    def getInfo(self): return self._info
    def getObjectiveValue(self): return self._info.objective_function_value

    def getCols(self, num_set_entries, indices):
        """(status, num_col, cost, lower, upper, num_nz) for the given columns, as highspy."""
        ix = np.asarray(indices, dtype=np.int64).ravel()[:int(num_set_entries)]
        c = np.asarray(self._cost, dtype=float)[ix]; lo = np.asarray(self._clb, dtype=float)[ix]; hi = np.asarray(self._cub, dtype=float)[ix]
        cnt = np.bincount(np.frombuffer(self._ri, dtype=np.int32), minlength=len(self._clb)) if len(self._ri) else np.zeros(len(self._clb), dtype=np.int64)
        return HighsStatus.kOk, len(ix), c, lo, hi, int(cnt[ix].sum())

    def getLp(self):
        """the model, as highspy's HighsLp (a_matrix_ column-wise)."""
        L = HighsLp(); m, n = len(self._rlo), len(self._clb)
        L.num_col_ = n; L.num_row_ = m
        L.col_cost_ = np.asarray(self._cost, dtype=float); L.col_lower_ = np.asarray(self._clb, dtype=float); L.col_upper_ = np.asarray(self._cub, dtype=float)
        L.row_lower_ = np.asarray(self._rlo, dtype=float); L.row_upper_ = np.asarray(self._rhi, dtype=float)
        A = self._matrix().tocsc(); A.sort_indices()
        M = L.a_matrix_; M.format_ = 1; M.num_col_ = n; M.num_row_ = m
        M.start_ = np.asarray(A.indptr, dtype=np.int64); M.index_ = np.asarray(A.indices, dtype=np.int64); M.value_ = np.asarray(A.data, dtype=float)
        return L

    def clearSolver(self):
        """forget the solution, basis and status; keep the model (run() solves from scratch in any case)."""
        self._status = HighsModelStatus.kNotset; self._info = HighsInfo(); self._basis = None; self._sol = HighsSolution()
        return HighsStatus.kOk

    def getBasis(self):
        if self._basis is None: self._basis = self._make_basis()
        return self._basis

    # ---------------- solve ----------------
    def _matrix(self):
        m, n = len(self._rlo), len(self._clb)
        ind = np.array(np.frombuffer(self._ri, dtype=np.int32)) if len(self._ri) else np.zeros(0, dtype=np.int32)   # copies: a live
        val = np.array(np.frombuffer(self._rv, dtype=np.float64)) if len(self._rv) else np.zeros(0)                # view would block addRow
        ptr = np.zeros(m + 1, dtype=np.int64); np.cumsum(np.asarray(self._rlen, dtype=np.int64), out=ptr[1:])
        return sp.csr_matrix((val, ind, ptr), shape=(m, n))

    def _method(self, solver):
        s = str(solver or 'choose').lower()
        if s in ('choose', ''): s = os.environ.get('HSHIM_SOLVER', 'ipm').lower()
        return {'ipm': 'highs-ipm', 'simplex': 'highs-ds', 'highs': 'highs', 'pdlp': 'highs-ipm'}.get(s, 'highs-ipm')

    def run(self):
        t0 = time.time(); self._nrun += 1
        m, n = len(self._rlo), len(self._clb)
        lo = np.asarray(self._rlo, dtype=float); hi = np.asarray(self._rhi, dtype=float)
        c = np.asarray(self._cost, dtype=float)
        bnd = np.column_stack([np.asarray(self._clb, dtype=float), np.asarray(self._cub, dtype=float)]) if n else np.zeros((0, 2))
        if n == 0:
            self._status = HighsModelStatus.kModelEmpty; self._runtime += time.time() - t0; return HighsStatus.kOk
        A = self._matrix()
        eq = np.isfinite(lo) & np.isfinite(hi) & (lo == hi)
        up = np.isfinite(hi) & ~eq
        dn = np.isfinite(lo) & ~eq
        iu = np.nonzero(up)[0]; idn = np.nonzero(dn)[0]; ie = np.nonzero(eq)[0]
        if len(iu) or len(idn):
            A_ub = sp.vstack([A[iu], -A[idn]], format='csr'); b_ub = np.concatenate([hi[iu], -lo[idn]])
        else:
            A_ub = None; b_ub = None
        if len(ie): A_eq = A[ie]; b_eq = lo[ie]
        else: A_eq = None; b_eq = None
        opts = {}
        for k in ('primal_feasibility_tolerance', 'dual_feasibility_tolerance'):
            if k in self._opt and self._opt[k] is not None: opts[k] = float(self._opt[k])
        if os.environ.get('HSHIM_PRESOLVE', '1') == '0' or self._opt.get('presolve') == 'off': opts['presolve'] = False
        if os.environ.get('HSHIM_DUMP'):
            try:
                os.makedirs(os.environ['HSHIM_DUMP'], exist_ok=True)
                fn = os.path.join(os.environ['HSHIM_DUMP'], 'hshim_%d_%d.npz' % (os.getpid(), self._nrun))
                np.savez(fn, c=c, bnd=bnd, lo=lo, hi=hi, data=A.data, indices=A.indices, indptr=A.indptr, shape=np.array(A.shape))
            except Exception as e:
                sys.stderr.write('hshim: dump failed: %s\n' % e)
        meth = self._method(self._opt.get('solver'))
        tries = [meth] + [{'highs-ipm': 'highs-ds', 'highs-ds': 'highs-ipm', 'highs': 'highs-ipm'}[meth]]
        res = None; used = None; msgs = []
        # v2b: HSHIM_TMAX_IPM=<s> caps a FIRST-try highs-ipm (IPM + crossover) at <s> seconds; on the cap the existing retry runs
        # highs-ds with no cap.  The model is unchanged, so only which solver returns the optimum changes.  HSHIM_DISP=1: HiGHS log to stdout.
        tmax = float(os.environ.get('HSHIM_TMAX_IPM', '0') or 0)
        if os.environ.get('HSHIM_DISP', '0') == '1': opts['disp'] = True
        for i_, mt in enumerate(tries):
            o_ = dict(opts)
            if i_ == 0 and mt == 'highs-ipm' and tmax > 0: o_['time_limit'] = tmax
            with warnings.catch_warnings():
                warnings.simplefilter('ignore')
                res = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=bnd, method=mt, options=o_)
            used = mt; msgs.append('%s: status %d%s' % (mt, res.status, ' (HSHIM_TMAX_IPM %gs cap)' % tmax if ('time_limit' in o_ and res.status != 0) else ''))
            if res.status == 0 and res.x is not None: break
        st = {0: HighsModelStatus.kOptimal, 1: HighsModelStatus.kIterationLimit, 2: HighsModelStatus.kInfeasible,
              3: HighsModelStatus.kUnbounded}.get(int(res.status), HighsModelStatus.kSolveError)
        if int(res.status) == 4 and 'unbounded or infeasible' in str(res.message).lower(): st = HighsModelStatus.kUnboundedOrInfeasible
        if int(res.status) == 1 and 'time limit' in str(res.message).lower(): st = HighsModelStatus.kTimeLimit
        S = HighsSolution(); info = HighsInfo()
        if res.x is not None:
            x = np.asarray(res.x, dtype=float)
            yd = np.zeros(m)
            mi = np.asarray(res.ineqlin.marginals, dtype=float) if A_ub is not None else np.zeros(0)
            if len(iu): yd[iu] += mi[:len(iu)]
            if len(idn): yd[idn] -= mi[len(iu):]
            if len(ie): yd[ie] += np.asarray(res.eqlin.marginals, dtype=float)
            cd = np.asarray(res.lower.marginals, dtype=float) + np.asarray(res.upper.marginals, dtype=float)
            rv = A @ x
            S.col_value = x.tolist(); S.col_dual = cd.tolist(); S.row_value = rv.tolist(); S.row_dual = yd.tolist()
            S.value_valid = True; S.dual_valid = st == HighsModelStatus.kOptimal
            info.objective_function_value = float(c @ x); info.valid = True
            info.primal_solution_status = 2 if st == HighsModelStatus.kOptimal else 0
            info.dual_solution_status = 2 if st == HighsModelStatus.kOptimal else 0
            nit = int(getattr(res, 'nit', 0) or 0)
            if used == 'highs-ipm': info.ipm_iteration_count = nit
            else: info.simplex_iteration_count = nit
            info.crossover_iteration_count = int(getattr(res, 'crossover_nit', 0) or 0)
        self._sol = S; self._info = info; self._status = st; self._basis = None
        dt = time.time() - t0; self._runtime += dt
        if os.environ.get('HSHIM_QUIET', '0') in ('', '0'):
            sys.stderr.write('hshim: run %d: %d x %d (nnz %d; %d <=, %d >=, %d =) %s -> %s, obj %.12g, %.1fs%s\n' % (
                self._nrun, m, n, len(self._ri), len(iu), len(idn), len(ie), used, _STATUS_STR[int(st)],
                info.objective_function_value, dt, '' if len(msgs) == 1 else ' [%s]' % '; '.join(msgs)))
            sys.stderr.flush()
        return HighsStatus.kOk if st == HighsModelStatus.kOptimal else HighsStatus.kWarning

    def _make_basis(self):
        B = HighsBasis(); S = self._sol
        n, m = len(self._clb), len(self._rlo)
        if not S.value_valid or len(S.col_value) != n: return B
        x = np.asarray(S.col_value); cd = np.asarray(S.col_dual); rv = np.asarray(S.row_value); rd = np.asarray(S.row_dual)
        lb = np.asarray(self._clb, dtype=float); ub = np.asarray(self._cub, dtype=float)
        lo = np.asarray(self._rlo, dtype=float); hi = np.asarray(self._rhi, dtype=float)
        tol = 1e-9
        def side(v, l, u, d):
            atl = np.isfinite(l) & (np.abs(v - l) <= tol * (1 + np.abs(l)))
            atu = np.isfinite(u) & (np.abs(v - u) <= tol * (1 + np.abs(u)))
            st = np.full(len(v), int(HighsBasisStatus.kBasic))
            st[atl] = int(HighsBasisStatus.kLower); st[atu & ~atl] = int(HighsBasisStatus.kUpper)
            st[atl & atu & (d < 0)] = int(HighsBasisStatus.kUpper)
            free0 = ~np.isfinite(l) & ~np.isfinite(u) & (np.abs(v) <= tol) & (np.abs(d) > tol)
            st[free0] = int(HighsBasisStatus.kZero)
            return st, (st != int(HighsBasisStatus.kBasic)) & (np.abs(d) <= tol)   # (status, nonbasic-but-could-be-basic)
        cs, camb = side(x, lb, ub, cd); rs, ramb = side(rv, lo, hi, rd)
        need = m - int((cs == int(HighsBasisStatus.kBasic)).sum()) - int((rs == int(HighsBasisStatus.kBasic)).sum())
        for st_, amb in ((rs, ramb), (cs, camb)):   # degenerate vertex: promote zero-dual nonbasics until the count is m
            if need <= 0: break
            ii = np.nonzero(amb)[0][:need]; st_[ii] = int(HighsBasisStatus.kBasic); need -= len(ii)
        B.col_status = [HighsBasisStatus(int(v)) for v in cs]; B.row_status = [HighsBasisStatus(int(v)) for v in rs]
        B.valid = need == 0
        return B
