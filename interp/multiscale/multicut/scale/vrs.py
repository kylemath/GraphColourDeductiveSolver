# Scale / adversarial driver for the vortex-restricted uncapped-cut induction.  Reuses ../unbounded/vr.py unchanged
# (VRInductor, FrontierVR patched into mc) and adds: extra maps (L18 = Opus bandfill sphere), outer-face choice,
# priority orderings (peel one side first -> prefix boundary = the seam), seeding A with the adversarial colA,
# larger R on the final steps, and t-tracking after the last odd vertex is enclosed.  Output only in scale/.
# spec: map:oseed:pol:var[:k=v,k=v...]   pol in left|right|rand|prioA|prioB ; opts: face=rand|odd|seam, Rlast=<R>,
#       lastk=<steps>, seedA=1, Rmax=<R>
import sys, os, json, time, random, pickle, collections
sys.path.insert(0, '/mnt/project-files/multiscale/multicut/unbounded/')
import vr, mc
from vr import VRInductor, FrontierVR, BIG
from pi import make, rotation, check_proper, signs, ball
OUT = '/mnt/project-files/multiscale/multicut/scale/fails/'
L18 = '/mnt/project-files/multiscale/opus_attack/bandfill/sphere_L18_w4.json'
_L18 = None
def mkmap(name):
    global _L18
    if name == 'L18':
        if _L18 is None: _L18 = json.load(open(L18))
        return [set(a) for a in _L18['adj']]
    return make(name)

def canon2(adj, rot, outer, policy, rng, prio=None):
    """pi.canonical with an extra policy 'prio': among valid candidates peel one of maximum prio (random ties)."""
    v1, v2, vn = outer; n = len(adj)
    present = [True]*n; C = [v1, vn, v2]; onC = {v1, vn, v2}
    def cnb(x):
        i = C.index(x); a = C[i-1] if i > 0 else v2; b = C[i+1] if i+1 < len(C) else v1
        return a, b
    chord = collections.Counter()
    def recompute(x):
        a, b = cnb(x); chord[x] = sum(1 for y in adj[x] if present[y] and y in onC and y != a and y != b)
    for x in C: recompute(x)
    peeled = []; paths = {}; direction = None
    while sum(present) > 3:
        cs = [x for x in C[1:-1] if chord[x] == 0]
        if policy == 'left': v = cs[0]
        elif policy == 'right': v = cs[-1]
        elif policy == 'prio':
            m = max(prio[x] for x in cs); v = rng.choice([x for x in cs if prio[x] == m])
        else: v = rng.choice(cs)
        j = C.index(v); pred, succ = C[j-1], C[j+1]; r = rot[v]; d = len(r)
        def arc(dr):
            i = r.index(pred); out = [pred]
            while out[-1] != succ: i = (i+dr) % d; out.append(r[i])
            return out
        if direction is None:
            a1, a2 = arc(1), arc(-1); direction = 1 if len(a1) > len(a2) else -1
        P = arc(direction)
        assert set(y for y in adj[v] if present[y]) == set(P)
        present[v] = False; onC.discard(v); new = P[1:-1]
        C[j:j+1] = new; onC.update(new)
        aff = set(new) | {pred, succ}
        for u in new: aff |= set(y for y in adj[u] if present[y] and y in onC)
        for x in aff: recompute(x)
        chord.pop(v, None); peeled.append(v); paths[v] = P
    rest = [x for x in range(n) if present[x]]; v3 = next(x for x in rest if x not in (v1, v2))
    return [v1, v2, v3] + peeled[::-1], [None, None, None] + [paths[v] for v in peeled[::-1]]

def pick_face(adj, rot, emb, rng, face):
    n = len(adj)
    if face == 'seam':        # L18: v1, v2 consecutive in tube row 16 (A's seam row), vn in row 17 (B)
        i = rng.randrange(18); a, b, c = 16*18+i, 16*18+(i+1) % 18, 17*18+i
        assert b in adj[a] and c in adj[a] and c in adj[b]
        f = tuple(emb.traverse_face(a, b)) if c in emb.traverse_face(a, b) else tuple(emb.traverse_face(b, a))
        f = list(f)
    elif face == 'odd':       # outer face incident to an odd-degree vertex, which becomes vn (the LAST vertex)
        u = rng.choice([x for x in range(n) if len(adj[x]) % 2]); w = rot[u][rng.randrange(len(rot[u]))]
        f = list(emb.traverse_face(u, w)); c = u
    else:
        u = rng.randrange(n); w = rot[u][rng.randrange(len(rot[u]))]; f = list(emb.traverse_face(u, w)); c = f[2]
    k = f.index(c); f = f[k+1:] + f[:k+1]   # rotate so that c is last (keeps orientation)
    return tuple(f)

class VRW(VRInductor):
    # opt win=W: departed positions and new (vortex) positions may land on any edge within offset -W..+W of v
    # (vr.py: departed -> offsets -1, 0; created -> -1, 0, +1).  Count budget NB = #departed + dn unchanged.
    win = 1
    def build_allowed(self, B2, pos, P, v, dn, extra=0, window_any=False):
        al, dep, NB, surv = VRInductor.build_allowed(self, B2, pos, P, v, dn, extra, window_any)
        if dep > 0 or dn > 0 or window_any:
            L = len(B2); pv = pos[v]
            for e in range(-self.win, self.win + 1):
                j = (pv + e) % L
                if al[j] == 0: al[j] = 2
        return al, dep, NB, surv
# ---- greedy policy + Lyapunov hook (coordinator request, section 'walk') ----
import inspect, textwrap, mcstep
_src = textwrap.dedent(inspect.getsource(mcstep.MCInductor.solve_step))
_src = _src.replace("    if not FI:\n", "    ev = self._lyap_hook(ev, B2, s, odd, FBs)\n    if not FI:\n", 1)
assert '_lyap_hook' in _src
_ns = dict(vars(mcstep)); exec(_src, _ns); solve_step_hooked = _ns['solve_step']
def _lyap_hook(self, ev, B2, s, odd, FBs):
    prev = self.recs[-1] if self.recs else dict(ncuts=0, t=0.0)
    ts = []
    for a, nc, mr in ev:
        if odd: ts.append(0.0); continue
        c2 = dict(self.col); c2.update(a); H = self.H_of(B2, s, c2); ts.append(round(abs(mc.cz(H[-1])), 3))
    noninc = [i for i, e in enumerate(ev) if e[1] <= prev['ncuts'] and (odd or ts[i] <= prev['t'] + 1e-9)]
    self._ly = dict(nev=len(ev), minnc=min(e[1] for e in ev), mint=min(ts), noninc=len(noninc), prevc=prev['ncuts'], prevt=prev['t'])
    if getattr(self, 'greedy', False):
        col = self.col; v = self.order[len(self.recs) + 3]
        idx = sorted(range(len(ev)), key=lambda i: (ev[i][1], ts[i], sum(1 for x in FBs if x != v and ev[i][0][x] != col[x])))
        ev = [ev[i] for i in idx]
    return ev
VRInductor.solve_step = solve_step_hooked
VRInductor._lyap_hook = _lyap_hook
TZ = [False]
U6 = list(mc.U)
_close0 = FrontierVR.close
def _close_tz(self, F, HL, allow=True):
    # two-sided rule (opt tz=1): once the uncoloured remainder holds no odd vertex, an even walk must close (t = 0)
    if TZ[0] and not self.odd and tuple(HL) != (0, 0): return None
    return _close0(self, F, HL, allow)
FrontierVR.close = _close_tz
TLIM = int(os.environ.get('TLIM', '3000'))
def job(spec):
    parts = spec.split(':'); name, oseed, pol, var = parts[:4]; oseed = int(oseed)
    opts = dict(kv.split('=') for kv in parts[4].split(',')) if len(parts) > 4 and parts[4] else {}
    face = opts.get('face', 'rand'); Rlast = int(opts.get('Rlast', '-1')); lastk = int(opts.get('lastk', '1'))
    Rmax = int(opts.get('Rmax', '4')); seedA = opts.get('seedA', '0') == '1'
    TZ[0] = False                                  # per-job reset (the flag is a module global in a pool worker)
    mc.U[:] = U6; mc.UI.clear(); mc.UI.update({u: d for d, u in enumerate(mc.U)})
    if opts.get('U12') == '1':   # also allow jumps of norm 2*sqrt(3) (2*(e_i - e_j)); only meaningful for variant 'any'
        assert var == 'any'
        mc.U[:] = [(2, 0), (0, 2), (-2, -2), (-2, 0), (0, -2), (2, 2)] + [(2, -2), (4, 2), (2, 4), (-2, 2), (-4, -2), (-2, -4)]
        mc.UI.clear(); mc.UI.update({u: d for d, u in enumerate(mc.U)})
    t0 = time.time(); adj = mkmap(name); rot, emb = rotation(adj); rng = random.Random(oseed); n = len(adj)
    f = pick_face(adj, rot, emb, rng, face)
    prio = None
    if pol in ('prioA', 'prioB'):
        Aset = set(json.load(open(L18))['A']) if name == 'L18' else set()
        # prioB: peel B first => A is inserted first (prefix = A, boundary = A's seam row); prioA: the reverse
        prio = [(1 if (x not in Aset) == (pol == 'prioB') else 0) for x in range(n)]
        order, paths = canon2(adj, rot, f, 'prio', rng, prio)
    else:
        order, paths = canon2(adj, rot, f, pol, rng)
    oddtot = sum(1 for x in range(n) if len(adj[x]) % 2)
    I = (VRW if 'win' in opts else VRInductor)(adj, order, paths, Rmax=Rmax, policy='keep', seed=oseed)
    if 'win' in opts: I.win = int(opts['win'])
    I.greedy = opts.get('greedy') == '1'; walk = []
    I.node_cap = int(os.environ.get('NCAP', '400000')); I.cand_cap = int(os.environ.get('CCAP', '20000')); I.variant = var; I.slide = 0; I.init_vr()
    status = 'ok'; err = None; diag = None; seedinfo = None; seamk = None; Ahit = None
    if name == 'L18':
        Aset = set(json.load(open(L18))['A']); seam = set(range(16*18, 17*18)); seamB = set(range(17*18, 18*18))
    try:
        for k in range(3, n):
            if k >= n - lastk and Rlast >= 0: I.Rmax = Rlast
            if opts.get('tz') == '1':
                nxt = I.nodd + sum(1 for w in paths[k][1:-1] if len(adj[w]) % 2)
                TZ[0] = (nxt == oddtot)
            I._ly = None
            if I.step(k) is None: status = 'FAIL'; break
            r_ = I.recs[-1]; ly = I._ly or {}
            walk.append([r_['n'], r_['nodd'], r_['ncuts'], r_['t'], r_['R'], r_['L'], ly.get('noninc'), ly.get('minnc'), ly.get('mint'), ly.get('prevc'), ly.get('prevt')])
            if name == 'L18':
                Bset = set(I.B); pref = set(order[:k+1])
                if pref == Aset or pref == set(range(n)) - Aset:
                    Ahit = dict(k=k, n=k+1, L=len(I.B), seamrowA_on_bd=len(Bset & seam), seamrowB_on_bd=len(Bset & seamB), R=I.recs[-1]['R'], t=I.recs[-1]['t'], ncuts=I.recs[-1]['ncuts'], npos=I.recs[-1]['npos'])
                    if seedA and pref == Aset:
                        D = json.load(open(L18)); cA = {int(a): b for a, b in D['colA'].items()}
                        H = I.H_of(I.B, signs(I.B, I.degp)[0], {**I.col, **cA})
                        cp = mc.cut_positions(H, I.nodd % 2 == 1, BIG, var, 1.0, [0]*len(I.B)) if H is not None else None
                        seedinfo = dict(n=k+1, proper=check_proper([adj[x] & Aset for x in range(n)], {x: cA[x] for x in Aset}) if False else None,
                                        t=abs(mc.cz(H[-1])) if H else None, accepted_no_cuts=cp is not None)
                        if cp is not None:
                            I.col.update(cA); I.posn = []
                        else: status = 'seed_rejected'; break
            if time.time() - t0 > TLIM: status = 'timeout'; break
    except RuntimeError as e: status = 'UNK'; err = str(e)
    rs = I.recs
    if status == 'FAIL':
        k = len(rs) + 3; fl = I.fail
        diag = dict(n=k+1, last=(k == n-1), nodd=I.nodd, dn=I.dn, vortex=I.dn > 0, dep=fl['dep'], NB=fl['NB'], npos=len(I.posn), L=len(fl['B']))
        for key, kw in (('extra1_window', dict(extra=1, window_any=True)), ('anywhere', dict(anywhere=True))):
            try: r = I.step(k, dry=True, **kw)
            except RuntimeError as e: r = 'UNK ' + str(e)
            diag[key] = r
        pickle.dump(dict(spec=spec, fail=fl, k=k, recs=rs[-80:], diag=diag, order=order), open(OUT + 'fail_%s.pkl' % spec.replace(':', '_').replace(',', '_').replace('=', ''), 'wb'))
    Rh = collections.Counter(r['R'] for r in rs)
    # t once every odd vertex is enclosed (the uncoloured remainder is then flat)
    full = [r for r in rs if r['nodd'] == oddtot]
    out = dict(spec=spec, n=n, oddtot=oddtot, status=status, err=err, steps=len(rs), maxR=max([r['R'] for r in rs], default=0), Rhist=dict(sorted(Rh.items())),
               maxcuts=max([r['ncuts'] for r in rs], default=0), maxpos=max([r['npos'] for r in rs], default=0), maxnodd=I.nodd,
               maxratio=round(max([r['ncuts'] / max(1, r['nodd']) for r in rs], default=0), 3),
               cuts_le_nodd=all(r['ncuts'] <= r['nodd'] for r in rs), pos_le_nodd=all(r['npos'] <= max(r['nodd'], 0) + 0 for r in rs),
               newcut_nonvortex=sum(1 for r in rs if r['dn'] == 0 and r['newcuts'] > r['dep']),
               full_n=full[0]['n'] if full else None, t_at_full=full[0]['t'] if full else None, tmax_after_full=max([r['t'] for r in full], default=None),
               Rmax_last5=max([r['R'] for r in rs[-5:]], default=None), diag=diag, Ahit=Ahit, seedinfo=seedinfo, sec=round(time.time()-t0))
    # cuts vs nodd profile: max ncuts per nodd bucket
    prof = collections.defaultdict(int)
    for r in rs: prof[r['nodd']] = max(prof[r['nodd']], r['ncuts'])
    out['prof'] = sorted(prof.items())
    if opts.get('walk') == '1': out['walk'] = walk
    if status == 'ok': out['proper'] = check_proper(adj, I.col)
    return out

if __name__ == '__main__':
    from multiprocessing import Pool
    with Pool(int(os.environ.get('NP', '4'))) as Pp, open(sys.argv[1], 'a') as fo:
        for r in Pp.imap_unordered(job, sys.argv[2:]):
            fo.write(json.dumps(r) + '\n'); fo.flush()
            print({k: r[k] for k in ('spec', 'n', 'status', 'steps', 'maxR', 'maxcuts', 'maxpos', 'maxnodd', 'newcut_nonvortex', 'full_n', 't_at_full', 'diag', 'Ahit', 'seedinfo', 'sec')}, flush=True)
