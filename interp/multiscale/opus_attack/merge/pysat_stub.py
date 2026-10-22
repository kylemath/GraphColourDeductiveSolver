# Makes the authors' modules (lev.py, wk.py) importable and runnable here: python-sat is not installed in this
# container, so pysat.solvers.* are replaced by a thin wrapper around msat (msat.c).  Only used for cross-checks.
import sys, types
sys.dont_write_bytecode = True
sys.path.insert(0, '/mnt/project-files/multiscale/opus_attack/merge')
import lat

class _S:
    def __init__(self, bootstrap_with=None, **kw):
        self.cls = [list(c) for c in (bootstrap_with or [])]; self.budget = None; self.model = None
    def add_clause(self, c): self.cls.append(list(c))
    def conf_budget(self, b): self.budget = b
    def set_phases(self, *a, **k): pass
    def _run(self, budget):
        nv = max([abs(l) for c in self.cls for l in c] + [1])
        r = lat.solve(nv, self.cls, budget)
        if r == 'UNK': return None
        if r is None: self.model = None; return False
        self.model = [v if v in r else -v for v in range(1, nv+1)]; return True
    def solve(self): return self._run(None)
    def solve_limited(self): return self._run(self.budget)
    def get_model(self): return self.model
    def delete(self): pass

m = types.ModuleType('pysat'); ms = types.ModuleType('pysat.solvers')
ms.Cadical153 = ms.Glucose4 = ms.Minisat22 = _S
m.solvers = ms
sys.modules['pysat'] = m; sys.modules['pysat.solvers'] = ms
sys.path.insert(0, '/mnt/project-files/multiscale/hierarchy/weak'); sys.path.insert(0, '/mnt/project-files/multiscale/hierarchy')
sys.path.insert(0, '/mnt/project-files/multiscale/levelling'); sys.path.insert(0, '/mnt/project-files/multiscale')
