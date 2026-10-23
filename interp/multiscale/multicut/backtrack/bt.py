# Bounded backtracking ("turning back") for the vortex-restricted uncapped-cut induction.
# Model unchanged: ../unbounded/vr.py (VRInductor, FrontierVR) via ../scale/vrs.py (maps, orderings, faces).
# New: a step returns ALL admissible colourings (up to caps) instead of the first; the induction keeps a history of the
# last d steps (exact undo) and, on
#   (F) failure  : no admissible colouring at R <= 4 at step k, or
#   (G) guard    : a vortex step whose chosen colouring would raise |t| or the active-cut count above the running peak,
# undoes delta = 1..d steps (iterative deepening => the minimal depth is found), re-chooses at step k-delta among its
# admissible alternatives (R in [Rmin, Rmin+1], distinct (t, cut set) signatures, ordered to turn the walk back:
# smallest |t| first, then fewest cuts) and replays k-delta+1..k with the primary rule.  (F) succeeds when step k is
# coloured; (G) when no replayed step exceeds the old peaks.  Unresolved (G) => the original path is restored and the
# increase accepted; unresolved (F) => FAIL.  Depth 0 for (G) = another alternative at step k itself.
# Variant ord=dip: at every vortex step the primary choice prefers a t-increment opposite to the most recent
# uncancelled one (stack of increments; an exactly cancelling increment pops it).
# spec: map:oseed:pol:var[:k=v,...]  opts: d=<depth>, guard=0|1, ord=keep|dip, face=..., fb=<budget F>, gb=<budget G>
import sys, os, json, time, random, collections, inspect, textwrap, math
sys.path.insert(0, '/mnt/project-files/multiscale/multicut/scale/')
import vrs
from vrs import canon2, pick_face, VRInductor, FrontierVR, BIG, mc
import mcstep
RIG = '/mnt/project-files/multiscale/opus_attack/control/rigid/'
def mkmap(name):
    if name.endswith('.json'): return [set(a) for a in json.load(open(name if name.startswith('/') else RIG + name))['adj']]
    return vrs.mkmap(name)
from pi import rotation, check_proper, signs, ball

_src = inspect.getsource(mcstep.MCInductor.solve_step).replace('def solve_step(', 'def solve_all(')
for a, b in [("        if not FI:\n            a, nc, _ = ev[0]; return a, nc, len(ev), 0\n",
              "        if not FI:\n            return [(a, nc) for a, nc, _ in ev[:self.KOUT]]\n"),
             ("        S = Cadical153(bootstrap_with=cls); nsat = 0\n", "        S = Cadical153(bootstrap_with=cls); nsat = 0; outs = []\n"),
             ("                nsat += 1\n", "                nsat += 1\n                if nsat > self.KSAT: break\n"),
             ("                    return out, nc, len(ev), nsat\n",
              "                    outs.append((out, nc))\n                    if len(outs) >= self.KOUT: return outs\n"),
             ("            if len(cands) >= ccap: raise", "            if outs: return outs\n            if len(cands) >= ccap: raise")]:
    assert a in _src, a; _src = _src.replace(a, b, 1)
_src = textwrap.dedent(_src)
_ns = dict(vars(mcstep)); exec(_src, _ns)

class Ov:
    def __init__(s, base, top): s.b = base; s.t = top
    def __getitem__(s, x): return s.t[x] if x in s.t else s.b[x]

class BT(VRInductor):
    KOUT = 1; KSAT = BIG
    solve_all = _ns['solve_all']
    def setup(self, d, guard, ordr, fb, gb):
        self.init_vr(); self.d = d; self.guard = guard; self.ordr = ordr; self.fb = fb; self.gb = gb
        self.tstack = []; self.pk_c = 0; self.pk_t = 0.0; self.tprev = 0j
        self.hist = collections.deque(); self.events = []; self.nsolve = 0; self.insearch = False; self.ncapalt = 0
    # ---- one step, split into enter / candidates / commit / undo ----
    def enter(self, k):
        v = self.order[k]; P = self.paths[k]; B = self.B
        ip = B.index(P[0]); iq = B.index(P[-1]); assert iq == ip + len(P) - 1
        B2 = B[:ip+1] + [v] + B[iq:]
        self.present[v] = True; self.degp[v] = len(P)
        for w in P: self.degp[w] += 1
        dn = sum(1 for w in P[1:-1] if len(self.adj[w]) % 2); self.nodd += dn; self.dn = dn
        s, odd = signs(B2, self.degp); assert odd == (self.nodd % 2 == 1)
        pos = {b: i for i, b in enumerate(B2)}
        al, dep, NB, surv = self.build_allowed(B2, pos, P, v, dn)
        return dict(k=k, v=v, P=P, B2=B2, s=s, odd=odd, pos=pos, al=al, dep=dep, NB=NB, surv=surv, dn=dn)
    def leave(self, c):
        v = c['v']; self.present[v] = False; self.degp[v] = 0
        for w in c['P']: self.degp[w] -= 1
        self.nodd -= c['dn']
    def cands(self, c, extra=0, kout=1, ksat=BIG):
        self.al = c['al']; FrontierVR.NB = c['NB']; self.J = BIG; self.cap_on = None; self.capfails = []
        self.KOUT = kout; self.KSAT = ksat; res = []; Rtop = self.Rmax
        for R in range(0, self.Rmax + 1):
            if R > Rtop: break
            self.nsolve += 1
            try: out = self.solve_all(c['v'], c['B2'], c['pos'], c['s'], c['odd'], ball(self.nb, c['v'], R), R)
            except RuntimeError:
                if res or self.insearch: self.ncapalt += 1; break     # cap while enumerating alternatives: stop, not UNK
                raise
            if out:
                if not res: Rtop = min(self.Rmax, R + extra)
                res += [self.evalc(c, R, o, nc) for o, nc in out]
        return res
    def evalc(self, c, R, newcol, nc):
        FrontierVR.NB = c['NB']
        H = self.H_of(c['B2'], c['s'], Ov(self.col, newcol)); t = mc.cz(H[-1])
        cuts = mc.cut_positions(H, c['odd'], BIG, self.variant, 1.0, c['al'])
        return dict(R=R, col=newcol, t=t, cuts=cuts, nc=len(cuts), sig=(round(t.real, 3), round(t.imag, 3), tuple(cuts)))
    def alts(self, c):
        A = self.cands(c, extra=1, kout=24, ksat=60); seen = set(); out = []
        for a in A:
            if a['sig'] in seen: continue
            seen.add(a['sig']); out.append(a)
        return out[:8]
    def order_primary(self, c, A):
        if self.ordr == 'dip' and c['dn'] > 0 and self.tstack:
            top = self.tstack[-1]
            def key(a):
                dt = a['t'] - self.tprev; dot = (dt * top.conjugate()).real
                return (0 if dot < -1e-6 else (1 if abs(dt) < 1e-6 else 2), a['R'], abs(a['t']), a['nc'])
            return sorted(A, key=key)
        return A
    def commit(self, c, a):
        newcol = a['col']; B2 = c['B2']; pos = c['pos']; al = c['al']; dep = c['dep']; NB = c['NB']; dn = c['dn']; L = len(B2)
        snap = dict(old={x: self.col.get(x) for x in newcol}, B=self.B, posn=self.posn, nrecs=len(self.recs), ncre=len(self.created),
                    tstack=list(self.tstack), pk=(self.pk_c, self.pk_t), tprev=self.tprev)
        self.col.update(newcol); self.B = B2; cuts = a['cuts']; t = a['t']
        used_new = [j for j in cuts if al[j] == 2]
        newpos = list(c['surv']) + [(B2[j], B2[(j+1) % L]) for j in used_new]
        slots = NB - len(used_new); cand = [pos[c['v']], (pos[c['v']]-1) % L, (pos[c['v']]+1) % L]; have = set(newpos)
        for j in cand:
            if slots <= 0: break
            e = (B2[j], B2[(j+1) % L])
            if al[j] == 2 and e not in have: newpos.append(e); have.add(e); slots -= 1
        self.created.append(len(used_new) - min(len(used_new), dep) if dn > 0 else 0)
        assert dn > 0 or len(used_new) <= dep
        self.posn = newpos
        rec = dict(n=c['k']+1, L=L, R=a['R'], odd=c['odd'], t=round(abs(t), 3), ncuts=len(cuts), npos=len(newpos), nodd=self.nodd,
                   dn=dn, dep=dep, newcuts=len(used_new))
        self.recs.append(rec)
        dt = t - self.tprev
        if abs(dt) > 1e-6:
            if self.tstack and abs(self.tstack[-1] + dt) < 1e-6: self.tstack.pop()
            else: self.tstack.append(dt)
        self.tprev = t; self.pk_c = max(self.pk_c, len(cuts)); self.pk_t = max(self.pk_t, abs(t))
        return snap
    def undo(self, c, snap, lv=True):
        for x, o in snap['old'].items():
            if o is None: del self.col[x]
            else: self.col[x] = o
        self.B = snap['B']; self.posn = snap['posn']; del self.recs[snap['nrecs']:]; del self.created[snap['ncre']:]
        self.tstack = snap['tstack']; self.pk_c, self.pk_t = snap['pk']; self.tprev = snap['tprev']
        if lv: self.leave(c)
    def push(self, c, a, snap):
        self.hist.append((c, a, snap))
        while len(self.hist) > max(self.d, 1): self.hist.popleft()
    def exceeds(self, a, pk):
        return a['nc'] > pk[0] or abs(a['t']) > pk[1] + 1e-6
    # ---- primary choice at an entered step (no backtracking) ----
    def isdead(self, a):
        # [P] all odd vertices enclosed and t != 0: the uncoloured remainder is flat, so the run cannot finish unless a
        # later ball reaches an enclosed odd vertex; with dead=1 such a state is treated as a failure at once.
        return self.deadon and self.nodd == self.oddtot and abs(a['t']) > 1e-6
    def choose(self, c, pk, soft):
        """returns (choice or None, kind of trouble or None, list of hard-admissible options)."""
        if c['dn'] > 0 and (self.guard or self.ordr == 'dip'): A = self.order_primary(c, self.alts(c))
        else: A = self.cands(c)
        hard = [a for a in A if not self.isdead(a)]
        if A and not hard: A = self.order_primary(c, self.alts(c)); hard = [a for a in A if not self.isdead(a)]
        if not A: return None, 'F', hard
        if not hard: return None, 'D', hard
        if soft and c['dn'] > 0:
            s = [a for a in hard if not self.exceeds(a, pk)]
            if not s: return hard[0], 'G', hard
            return s[0], None, hard
        return hard[0], None, hard
    # ---- backtracking search ----
    def search(self, k, kind, pk):
        """state: step k not entered.  Returns ((delta, j, used), used) on success (history updated), (None, used) otherwise."""
        self.insearch = True
        try: return self._search(k, kind, pk)
        finally: self.insearch = False
    def _search(self, k, kind, pk):
        budget = self.fb if kind != 'G' else self.gb; used = [0]; undone = []
        maxd = min(self.d, len(self.hist)); res = None; soft = kind == 'G'
        for delta in range(1, maxd + 1):
            cj, aj, sj = self.hist.pop(); self.undo(cj, sj); undone.append((cj, aj))
            j = k - delta; assert cj['k'] == j
            if self.vonly and cj['dn'] == 0 and abs(aj['t'] - sj['tprev']) < 1e-6: continue
            c = self.enter(j); used[0] += 1
            A = [a for a in self.alts(c) if a['sig'] != aj['sig'] and not self.isdead(a)]
            A.sort(key=lambda a: (round(abs(a['t']), 3), a['nc'], a['R']))
            for a in A:
                if used[0] >= budget: break
                if soft and c['dn'] > 0 and self.exceeds(a, pk): continue
                sn = self.commit(c, a); new = [(c, a, sn)]; ok = True
                for i in range(j + 1, k + 1):
                    ci = self.enter(i); used[0] += 1
                    ai, tr, _ = self.choose(ci, pk, soft)
                    if ai is None or tr is not None: self.leave(ci); ok = False; break
                    new.append((ci, ai, self.commit(ci, ai)))
                if ok:
                    for e in new: self.push(*e)
                    res = (delta, j, used[0]); break
                for (ci, ai, si) in reversed(new[1:]): self.undo(ci, si)
                self.undo(c, sn, lv=False)
            if res: break
            self.leave(c)
            if used[0] >= budget: break
        if res is None:      # restore the original path exactly (stored choices, no re-solving)
            for (cj, aj) in reversed(undone):
                c = self.enter(cj['k']); self.push(c, aj, self.commit(c, aj))
            return None, used[0]
        return res, used[0]
    def run(self, n, t0, tlim):
        k = 3
        while k < n:
            c = self.enter(k); pk = (self.pk_c, self.pk_t)
            a, kind, hard = self.choose(c, pk, self.guard)
            if kind == 'G' and self.d == 0: kind = None          # accept
            if kind is None and a is not None and c['dn'] > 0 and self.guard and hard and a is not hard[0]:
                self.events.append(dict(k=k, kind='G', depth=0, ok=True, used=0, dn=c['dn']))
            if kind:
                nodd0 = self.nodd; self.leave(c)
                res, used = (None, 0) if self.d == 0 else self.search(k, kind, pk)
                ev = dict(k=k, n=k+1, kind=kind, ok=res is not None, used=used, dn=c['dn'], last=(k == n-1), nodd=nodd0, full=(nodd0 == self.oddtot))
                if res is not None:
                    delta, j, _ = res; ev.update(depth=delta, j=j, jvortex=self.recs[-(delta+1)]['dn'] > 0,
                                                 gdist=self.gdist(self.order[k], self.order[j]))
                    self.events.append(ev); k += 1
                    if time.time() - t0 > tlim: return 'timeout'
                    continue
                self.events.append(ev)
                if kind != 'G':
                    self.fail = dict(k=k, kind=kind); return 'FAIL'
                c = self.enter(k); a, _, _ = self.choose(c, pk, False)     # accept the increase
            self.push(c, a, self.commit(c, a)); k += 1
            if time.time() - t0 > tlim: return 'timeout'
        return 'ok'
    def gdist(self, a, b):
        seen = {a: 0}; fr = [a]
        while fr:
            nx = []
            for x in fr:
                for y in self.adj[x]:
                    if y not in seen:
                        seen[y] = seen[x] + 1
                        if y == b: return seen[y]
                        nx.append(y)
            fr = nx
        return seen.get(b)

TLIM = int(os.environ.get('TLIM', '1500'))
def job(spec):
    parts = spec.split(':'); name, oseed, pol, var = parts[:4]; oseed = int(oseed)
    opts = dict(kv.split('=') for kv in parts[4].split(',')) if len(parts) > 4 and parts[4] else {}
    d = int(opts.get('d', '0')); guard = opts.get('guard', '1') == '1'; ordr = opts.get('ord', 'keep')
    vrs.TZ[0] = False; mc.U[:] = vrs.U6; mc.UI.clear(); mc.UI.update({u: i for i, u in enumerate(mc.U)})
    t0 = time.time(); adj = mkmap(name); rot, emb = rotation(adj); rng = random.Random(oseed); n = len(adj)
    f = pick_face(adj, rot, emb, rng, opts.get('face', 'rand'))
    if pol in ('prioA', 'prioB'):
        Aset = set(json.load(open(vrs.L18))['A']) if name == 'L18' else set()
        prio = [(1 if (x not in Aset) == (pol == 'prioB') else 0) for x in range(n)]
        order, paths = canon2(adj, rot, f, 'prio', rng, prio)
    else: order, paths = canon2(adj, rot, f, pol, rng)
    oddtot = sum(1 for x in range(n) if len(adj[x]) % 2)
    I = BT(adj, order, paths, Rmax=int(opts.get('Rmax', '4')), policy='keep', seed=oseed); I.node_cap = int(os.environ.get('NCAP', '400000'))
    I.cand_cap = int(os.environ.get('CCAP', '20000')); I.variant = var; I.slide = 0
    I.setup(d, guard, ordr, int(opts.get('fb', '6000')), int(opts.get('gb', '300')))
    I.oddtot = oddtot; I.deadon = opts.get('dead', '0') == '1'; I.vonly = opts.get('vonly', '0') == '1'
    err = None
    try: status = I.run(n, t0, TLIM)
    except RuntimeError as e: status = 'UNK'; err = str(e)
    rs = I.recs; full = [r for r in rs if r['nodd'] == oddtot]
    W = [(r['n'], r['nodd'], r['ncuts'], r['t'], r['R']) for r in rs]
    # running peaks sampled at n checkpoints (for growth fits)
    out = dict(spec=spec, name=name, n=n, d=d, guard=guard, ordr=ordr, oddtot=oddtot, status=status, err=err, steps=len(rs),
               failn=I.fail['k'] + 1 if I.fail else None, failkind=I.fail['kind'] if I.fail else None, faillast=bool(I.fail) and I.fail['k'] == n-1,
               maxR=max([r['R'] for r in rs], default=0), peakcuts=max([r['ncuts'] for r in rs], default=0),
               peakt=max([r['t'] for r in rs], default=0), full_n=full[0]['n'] if full else None, t_at_full=full[0]['t'] if full else None,
               events=I.events, nsolve=I.nsolve, ncapalt=I.ncapalt, sec=round(time.time() - t0), cuts_le_nodd=all(r['ncuts'] <= r['nodd'] for r in rs),
               newcut_nonvortex=sum(1 for r in rs if r['dn'] == 0 and r['newcuts'] > r['dep']))
    if opts.get('walk') == '1': out['walk'] = W[::5]
    if status == 'ok': out['proper'] = check_proper(adj, I.col)
    return out

if __name__ == '__main__':
    from multiprocessing import Pool
    specs = sys.argv[2:]
    if len(specs) == 1 and os.path.exists(specs[0]): specs = open(specs[0]).read().split()
    with Pool(int(os.environ.get('NP', '4')), maxtasksperchild=1) as Pp, open(sys.argv[1], 'a') as fo:
        for r in Pp.imap_unordered(job, specs):
            fo.write(json.dumps(r) + '\n'); fo.flush()
            ev = r['events']; nb = [e for e in ev if e.get('depth')]
            print(r['spec'], r['status'], r['steps'], 'failn', r['failn'], 'last', r['faillast'], 'pc', r['peakcuts'], 'pt', r['peakt'],
                  'ev', len(ev), 'F', sum(1 for e in ev if e['kind'] == 'F'), 'Fok', sum(1 for e in ev if e['kind'] == 'F' and e['ok']),
                  'depths', [e['depth'] for e in nb][:20], r['sec'], 's', flush=True)
