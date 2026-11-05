# Team C analysis helper: exec the s75 engine with the given flags, load sol=, expose row loads by family and sender slacks.
# usage (module): import via exec of this file after setting sys.argv = [ana.py, flags...]; or run: python3 ana.py <flags> sol=FILE mode=senders|rows rows=FILE out=FILE
import sys, os, json, collections, itertools
ENG = '/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s75_teamA/eng/pcheck.py'
_argv = sys.argv[1:]
sys.argv = [ENG, 'help'] + _argv
ns = {'__file__': ENG, '__name__': 'pcheck_sC'}
import io, contextlib
with contextlib.redirect_stdout(io.StringIO()): exec(compile(open(ENG).read(), ENG, 'exec'), ns)
OPT, FLAGS = ns['OPT'], ns['FLAGS']
GRP = {'y': 'y', 'x': 'x', 'M': 'M', 'r': 'r', 'rr': 'rr', 'z': 'z', 'zr': 'zr', 'lq': 'l3q', 'lQ': 'l3q', 'Q': 'q7', 'q': 'q7', 'g': 'g'}
class Sol:
    def __init__(s, fn):
        S = json.load(open(fn)); s.t = S['t']; s.S = S
        s.Y = {}
        for k, v in S['y'].items():
            u, rest = k.split('|'); r_ = ns['root'](list((int(u),) + tuple(int(c) for c in rest)), 0); s.Y[r_] = v
        s.F = {}
        for fam in ('g', 'h', 'z', 'zr', 'r', 'rr', 'lq', 'lQ', 'q'):
            s.F[fam] = {tuple(k): v for k, v in S.get(fam, [])}
        s.X = {int(k): v for k, v in S.get('x', {}).items()}
        # engine globals the coefficient code reads (LQV/LQQ for Qeff)
        ns['LQV'].clear(); ns['LQV'].update(s.F['lq']); ns['LQQ'].clear(); ns['LQQ'].update(s.F['lQ'])
        ns['QV'].clear(); ns['QV'].update(s.F['q'])
        s.mc = {}
    def val(s, k):
        f, key = k
        if f == 'y': return s.Y.get(key, 0.0)
        if f == 'x': return s.X.get(key, 0.0)
        if f == 'M':
            if key not in s.mc:
                ks = ns['sig2_keys'](key); s.mc[key] = max([s.F['h'].get(tuple(kk), 0.0) for kk in ks] or [0.0])
            return s.mc[key]
        if f == 'lQ':
            return ns['l3q_QeffV'](key[0], *key[1:]) if len(key) == 4 else ns['l3q_Qeff'](*key)
        if f == 'Q': return max([s.F['q'].get(tuple(kk), 0.0) for kk in ns['q7keys'](key)] or [0.0])
        if f in s.F: return s.F[f].get(key, 0.0)
        raise KeyError(k)
    def row(s, d, lk, sv):
        cf = ns['recv_coef_R2'](d, lk, sv, 'xon' in FLAGS)
        g = collections.defaultdict(float); fams = collections.Counter(); tot = 0.0
        for k, c in cf.items():
            if not c: continue
            v = s.val(k); tot += c * v; g[GRP.get(k[0], k[0])] += c * v; fams[GRP.get(k[0], k[0])] += 1
        return tot, d - 6 + s.t - tot, dict(g), dict(fams), cf
    def senders(s):
        out = []
        for wd, cf, bits in ns['R2_sender_rows']():
            v = 0.0; g = collections.defaultdict(float)
            for k, c in cf.items():
                x = s.Y.get(k[1], 0.0) if k[0] == 'y' else s.F[k[0]].get(k[1], 0.0); v += c * x; g[GRP.get(k[0], k[0])] += c * x
            out.append((v - (1 - s.t), wd, ''.join(map(str, bits)), dict(g), cf))
        return out
if __name__ == '__main__' or True:
    pass
