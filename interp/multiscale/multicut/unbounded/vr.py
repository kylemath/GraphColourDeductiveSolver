# Vortex-restricted, uncapped cut induction (follow-up to ../RESULTS.md).
# Invariant (per step): the lifted boundary walk has circumradius <= 1 after cuts with jumps in 2*Lambda (|s| = 2; a cut
# position carrying s = 0 is dormant), variant 'nc' (no opposite pair) or 'any'; |t| free (even: sum of jumps = t);
# odd: one reflection cut among the cuts.  NO cap on the number of cuts.  Cut POSITIONS are persistent objects:
#   * a position keeps its boundary edge (a, b) while (a, b) is a boundary edge;
#   * an edge that leaves the boundary (it lies on the attachment path P) is reassigned to the two new edges at v
#     (P[0]-v, v-P[-1]); more than two departing positions merge (their jumps are re-optimised, so the merge condition
#     |sum| <= 2 is automatically met by the new single jump on the surviving edge);
#   * new positions are created ONLY at vortex steps (the step encloses dn > 0 new odd vertices), at most dn of them,
#     on the edges at offset -1/0/+1 of v (P[0]-v, v-P[-1], P[-1]-next);
#   * jumps on positions are re-chosen at every step (the 'att' convention of mcstep.py).
# Implementation: mc.Frontier is replaced by FrontierVR, whose state also counts cuts placed on non-carried edges
# (budget NB = #departed + dn); edge allow codes 0 = no cut, 1 = carried position, 2 = new / reassigned edge.
import sys, os, json, time, random, pickle, collections
sys.path.insert(0, '/mnt/project-files/multiscale/multicut/'); sys.path.insert(0, '/mnt/project-files/multiscale/localdetrend/'); sys.path.insert(0, '/mnt/project-files/multiscale/canonical/')
import mc
from mcstep import MCInductor
from pi import make, rotation, canonical, check_proper, signs, ball
from pi_step import maxrun
BIG = 10**6
_OrigFrontier = mc.Frontier

class FrontierVR(_OrigFrontier):
    NB = BIG
    def start(self):
        return {(k, 0, 0, 0, 0, 0): 0 for k in range(len(self.A))}
    def adv(self, F, p, allow=True):
        A = self.A; G = {}; NB = FrontierVR.NB
        allow = 1 if allow is True else (0 if allow is False or allow is None else allow)
        def put(k, v):
            if G.get(k, BIG) > v: G[k] = v
        for (a, ph, x, y, m, cn), c in F.items():
            S = A[a]
            q = (p[0]-x, p[1]-y) if ph == 0 else (x-p[0], y-p[1])
            if q in S: put((a, ph, x, y, m, cn), c)
            if not allow or c >= self.J: continue
            cn2 = cn + (1 if allow == 2 else 0)
            if cn2 > NB: continue
            for d, u in enumerate(mc.U):
                if not self._jump_ok(m, d): continue
                q2 = (q[0]-u[0], q[1]-u[1])
                if q2 in S:
                    m2 = m | (1 << d) if self.nc else 0
                    if ph == 0: put((a, 0, x+u[0], y+u[1], m2, cn2), c+1)
                    else: put((a, 1, x-u[0], y-u[1], m2, cn2), c+1)
            if self.odd and ph == 0:
                for r in S: put((a, 1, r[0]+p[0], r[1]+p[1], m, cn2), c+1)
        return G
    def close(self, F, HL, allow=True):
        best = None; NB = FrontierVR.NB
        allow = 1 if allow is True else (0 if allow is False or allow is None else allow)
        for (a, ph, x, y, m, cn), c in F.items():
            cn2 = cn + (1 if allow == 2 else 0); ok2 = allow and cn2 <= NB
            if not self.odd:
                if ph != 0: continue
                dx, dy = x - HL[0], y - HL[1]
                if (dx, dy) == (0, 0): cc = c
                elif ok2 and (-dx, -dy) in mc.UI and self._jump_ok(m, mc.UI[(-dx, -dy)]): cc = c + 1
                else: continue
            else:
                if ph == 0:
                    if not ok2: continue
                    cc = c + 1
                else:
                    dx, dy = x - HL[0], y - HL[1]
                    if (dx, dy) == (0, 0): cc = c
                    elif ok2 and (dx, dy) in mc.UI and self._jump_ok(m, mc.UI[(dx, dy)]): cc = c + 1
                    else: continue
            if cc <= self.J and (best is None or cc < best): best = cc
        return best
mc.Frontier = FrontierVR      # used by mc.ncuts / mc.cut_positions / MCInductor.solve_step through the module global

class VRInductor(MCInductor):
    J = BIG; tfree = True; cutmode = 'vr'; dormant = True; slide = 0; nmatchfail = 0
    def init_vr(self):
        self.posn = []                     # persistent positions: list of directed boundary edges (a, b)
        self.created = []; self.nonvortex_need = []
    def build_allowed(self, B2, pos, P, v, dn, extra=0, window_any=False):
        L = len(B2); al = [0]*L; surv = []; dep = 0
        for (a, b) in self.posn:
            if a in pos and b in pos and pos[b] == (pos[a] + 1) % L:
                for e in range(-self.slide, self.slide + 1): al[(pos[a] + e) % L] = 1
                surv.append((a, b))
            else: dep += 1
        pv = pos[v]; newe = []
        if dep > 0: newe += [(pv - 1) % L, pv]
        if dn > 0 or window_any: newe += [(pv - 1) % L, pv, (pv + 1) % L]
        for e in set(newe):
            if al[e] == 0: al[e] = 2
        return al, dep, dep + dn + extra, surv
    def step(self, k, extra=0, window_any=False, anywhere=False, dry=False):
        v = self.order[k]; P = self.paths[k]; B = self.B
        ip = B.index(P[0]); iq = B.index(P[-1]); assert iq == ip + len(P) - 1
        B2 = B[:ip+1] + [v] + B[iq:]
        if not dry:
            self.present[v] = True; self.degp[v] = len(P)
            for w in P: self.degp[w] += 1
            dn = 0
            for w in P[1:-1]:
                if len(self.adj[w]) % 2: self.nodd += 1; dn += 1
            self.dn = dn
        dn = self.dn
        s, odd = signs(B2, self.degp); assert odd == (self.nodd % 2 == 1)
        pos = {b: i for i, b in enumerate(B2)}
        al, dep, NB, surv = self.build_allowed(B2, pos, P, v, dn, extra, window_any)
        self.J = BIG if self.slide == 0 else len(surv) + NB
        if anywhere: al = [1]*len(B2); NB = BIG; self.J = BIG
        self.al = al; FrontierVR.NB = NB; self.cap_on = None; self.capfails = []
        for R in range(0, self.Rmax + 1):
            F = ball(self.nb, v, R)
            res = self.solve_step(v, B2, pos, s, odd, F, R)
            if res is not None:
                if dry: return dict(R=R, nc=res[1])
                newcol, nc, ncand, nsat = res
                self.col.update(newcol); self.B = B2
                H = self.H_of(B2, s, self.col); t = mc.cz(H[-1])
                cuts = mc.cut_positions(H, odd, self.J, self.variant, 1.0, al)
                L = len(B2); used_new = [j for j in cuts if al[j] == 2]
                if self.slide:
                    # match cuts on carried-window edges to surviving positions within the slide distance (Kuhn)
                    cw = [j for j in cuts if al[j] == 1]; sp = [pos[a] for (a, b) in surv]; mt = {}
                    def dist(i, j): return min((i - j) % L, (j - i) % L)
                    def aug(ci, seen):
                        for pi_ in range(len(sp)):
                            if pi_ in seen or dist(cw[ci], sp[pi_]) > self.slide: continue
                            seen.add(pi_)
                            if pi_ not in mt or aug(mt[pi_], seen): mt[pi_] = ci; return True
                        return False
                    unm = [ci for ci in range(len(cw)) if not aug(ci, set())]
                    self.nmatchfail += len(unm)
                    moved = [surv[pi_] if pi_ not in mt else (B2[cw[mt[pi_]]], B2[(cw[mt[pi_]]+1) % L]) for pi_ in range(len(sp))]
                    newpos = list(dict.fromkeys(moved)) + [(B2[j], B2[(j+1) % L]) for j in used_new]
                    newpos = list(dict.fromkeys(newpos))
                else:
                    newpos = list(surv) + [(B2[j], B2[(j+1) % L]) for j in used_new]
                if self.dormant:
                    # unused reassignment / creation slots stay as dormant positions on the window edges
                    slots = NB - len(used_new); cand = [pos[v], (pos[v]-1) % L, (pos[v]+1) % L]
                    have = set(newpos)
                    for j in cand:
                        if slots <= 0: break
                        e = (B2[j], B2[(j+1) % L])
                        if al[j] == 2 and e not in have: newpos.append(e); have.add(e); slots -= 1
                self.created.append(len(used_new) - min(len(used_new), dep) if dn > 0 else 0)
                assert dn > 0 or len(used_new) <= dep
                self.posn = newpos
                rec = dict(n=k+1, L=L, R=R, odd=odd, t=round(abs(t), 3), ncuts=len(cuts), npos=len(newpos), nodd=self.nodd,
                           dn=dn, dep=dep, newcuts=len(used_new))
                self.recs.append(rec); return rec
        if dry: return None
        self.fail = dict(k=k, v=v, P=P, B=B2, s=s.tolist(), odd=odd, col=dict(self.col), nodd=self.nodd, al=al, NB=NB, dn=dn, dep=dep,
                         posn=list(self.posn))
        return None

TLIM = int(os.environ.get('TLIM', '2400'))
def job(spec):
    parts = spec.split(':'); name, oseed, pol, var = parts[:4]; oseed = int(oseed); slide = int(parts[4]) if len(parts) > 4 else 0
    t0 = time.time(); adj = make(name); rot, emb = rotation(adj); rng = random.Random(oseed)
    u = rng.randrange(len(adj)); w = rot[u][rng.randrange(len(rot[u]))]; f = tuple(emb.traverse_face(u, w))
    order, paths = canonical(adj, rot, f, pol, rng=rng)
    I = VRInductor(adj, order, paths, Rmax=4, policy='keep', seed=oseed); I.node_cap = int(os.environ.get('NCAP', '400000')); I.cand_cap = int(os.environ.get('CCAP', '20000')); I.variant = var; I.slide = slide; I.init_vr()
    status = 'ok'; err = None; diag = None
    try:
        for k in range(3, len(order)):
            if I.step(k) is None: status = 'FAIL'; break
            if time.time() - t0 > TLIM: status = 'timeout'; break
    except RuntimeError as e: status = 'UNK'; err = str(e)
    rs = I.recs
    if status == 'FAIL':
        k = len(rs) + 3; diag = dict(n=k+1, nodd=I.nodd, dn=I.dn, vortex=I.dn > 0, dep=I.fail['dep'], NB=I.fail['NB'], npos=len(I.posn))
        # what would have saved the step (R <= 4): one extra new cut in the window / cuts anywhere, unbounded
        for key, kw in (('extra1_window', dict(extra=1, window_any=True)), ('extra2_window', dict(extra=2, window_any=True)),
                        ('anywhere', dict(anywhere=True))):
            try: r = I.step(k, dry=True, **kw)
            except RuntimeError as e: r = 'UNK ' + str(e)
            diag[key] = r
        pickle.dump(dict(spec=spec, fail=I.fail, k=k, recs=rs[-60:], diag=diag), open('/mnt/project-files/multiscale/multicut/unbounded/fail_%s.pkl' % spec.replace(':', '_'), 'wb'))
    Rh = collections.Counter(r['R'] for r in rs)
    # max simultaneous active cuts and positions vs enclosed odd vertices
    ratio = max([r['ncuts'] / max(1, r['nodd']) for r in rs], default=0)
    out = dict(spec=spec, n=len(adj), status=status, err=err, steps=len(rs), maxR=max([r['R'] for r in rs], default=0), Rhist=dict(sorted(Rh.items())),
               maxcuts=max([r['ncuts'] for r in rs], default=0), maxpos=max([r['npos'] for r in rs], default=0), maxnodd=I.nodd,
               cuts_minus_nodd=max([r['ncuts'] - r['nodd'] for r in rs], default=0), pos_minus_nodd=max([r['npos'] - r['nodd'] for r in rs], default=0),
               maxratio=round(ratio, 3), created=sum(I.created), nvortex=sum(1 for r in rs if r['dn'] > 0),
               newcut_nonvortex=sum(1 for r in rs if r['dn'] == 0 and r['newcuts'] > r['dep']), diag=diag, nmatchfail=I.nmatchfail, sec=round(time.time()-t0))
    tr = []; last = None
    for r in rs:
        key = (r['nodd'], r['ncuts'], r['npos'])
        if key != last: tr.append((r['n'], r['nodd'], r['ncuts'], r['npos'], r['R'])); last = key
    out['trace'] = tr[:600]
    if status == 'ok': out['proper'] = check_proper(adj, I.col)
    return out

if __name__ == '__main__':
    from multiprocessing import Pool
    with Pool(int(os.environ.get('NP', '4'))) as Pp, open(sys.argv[1], 'a') as fo:
        for r in Pp.imap_unordered(job, sys.argv[2:]):
            fo.write(json.dumps(r) + '\n'); fo.flush()
            print({k: r[k] for k in ('spec', 'status', 'err', 'steps', 'maxR', 'maxcuts', 'maxpos', 'maxnodd', 'cuts_minus_nodd', 'created', 'newcut_nonvortex', 'diag', 'sec')}, flush=True)
