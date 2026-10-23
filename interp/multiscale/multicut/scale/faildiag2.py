# Re-run a spec up to its failing step, then probe the live state: (a) cuts anywhere -> #cuts, distance of each cut
# to the nearest held position and to v; (b) least slide d of held positions (count budget unchanged) that saves it;
# (c) one extra NEW cut allowed within distance d of v (non-vortex creation) -> least d.
import sys, copy, json
sys.path.insert(0, '/mnt/project-files/multiscale/multicut/scale/')
import vrs, vr, mc
from vrs import *
def rerun(spec):
    parts = spec.split(':'); name, oseed, pol, var = parts[:4]; oseed = int(oseed)
    opts = dict(kv.split('=') for kv in parts[4].split(',')) if len(parts) > 4 and parts[4] else {}
    adj = mkmap(name); rot, emb = rotation(adj); rng = random.Random(oseed); n = len(adj)
    f = pick_face(adj, rot, emb, rng, opts.get('face', 'rand'))
    if pol in ('prioA', 'prioB'):
        Aset = set(json.load(open(L18))['A']) if name == 'L18' else set()
        prio = [(1 if (x not in Aset) == (pol == 'prioB') else 0) for x in range(n)]
        order, paths = canon2(adj, rot, f, 'prio', rng, prio)
    else: order, paths = canon2(adj, rot, f, pol, rng)
    I = VRInductor(adj, order, paths, Rmax=4, policy='keep', seed=oseed); I.variant = var; I.slide = 0; I.init_vr()
    for k in range(3, n):
        if I.step(k) is None: return I, k
    return I, None
def probe(spec):
    I, k = rerun(spec)
    if k is None: print(spec, 'no failure'); return
    fl = I.fail; B2 = fl['B']; L = len(B2); pos = {b: i for i, b in enumerate(B2)}; v = fl['v']; pv = pos[v]
    held = [pos[a] for (a, b) in I.posn if a in pos and b in pos and pos[b] == (pos[a]+1) % L]
    def cd(i, S): return min([min((i-j) % L, (j-i) % L) for j in S], default=None)
    J = copy.deepcopy(I); J.Rmax = 4
    # anywhere, non-dry on a copy: get the cut positions
    orig = J.build_allowed
    J.build_allowed = lambda *a, **kw: ([1]*L, 0, BIG, [])
    J.step(k, dry=False) if False else None
    r = I.step(k, dry=True, anywhere=True)
    res = dict(spec=spec, n=k+1, L=L, nodd=I.nodd, dn=I.dn, held=len(held), anywhere=r)
    # anywhere colouring & cuts: replicate step with al = all-1, NB big
    J2 = copy.deepcopy(I); J2.present = list(I.present); 
    J2.build_allowed = lambda B2_, pos_, P_, v_, dn_, extra=0, window_any=False: ([1]*len(B2_), 0, BIG, [])
    try:
        rec = J2.step(k, dry=False)
        if rec:
            H = J2.H_of(J2.B, signs(J2.B, J2.degp)[0], J2.col); cuts = mc.cut_positions(H, J2.nodd % 2 == 1, BIG, I.variant, 1.0, None)
            res['anyw_cuts'] = len(cuts); res['dist_held'] = sorted(cd(i, held) for i in cuts); res['dist_v'] = sorted(cd(i, [pv]) for i in cuts); res['anyw_R'] = rec['R']
    except Exception as e: res['anyw_err'] = repr(e)
    # slides
    for d in range(1, 9):
        J3 = copy.deepcopy(I)
        def ba(B2_, pos_, P_, v_, dn_, extra=0, window_any=False, d=d, J3=J3):
            al, dep, NB, surv = VRInductor.build_allowed(J3, B2_, pos_, P_, v_, dn_)
            Lb = len(B2_)
            for (a, b) in surv:
                for e in range(-d, d+1):
                    j = (pos_[a]+e) % Lb
                    if al[j] == 0: al[j] = 1
            return al, dep, NB, surv
        J3.build_allowed = ba
        if J3.step(k, dry=True) is not None: res['slide_d'] = d; break
    # one extra new cut within distance d of v
    for d in range(1, 40):
        J4 = copy.deepcopy(I)
        def ba(B2_, pos_, P_, v_, dn_, extra=0, window_any=False, d=d, J4=J4):
            al, dep, NB, surv = VRInductor.build_allowed(J4, B2_, pos_, P_, v_, dn_)
            Lb = len(B2_); p = pos_[v_]
            for e in range(-d, d+1):
                j = (p+e) % Lb
                if al[j] == 0: al[j] = 2
            return al, dep, NB + 1, surv
        J4.build_allowed = ba
        if J4.step(k, dry=True) is not None: res['extra1_within_d_of_v'] = d; break
    print(json.dumps(res), flush=True)
if __name__ == '__main__':
    for sp in sys.argv[1:]: probe(sp)
