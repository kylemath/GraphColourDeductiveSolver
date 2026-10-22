# per-instance analysis: SDP (low-rank, exact-feasibility penalty) on seam bands, twist profile vs SAT repair vs offset
import os; os.environ['OPENBLAS_NUM_THREADS'] = '1'
from tw import *
import json
from scipy.stats import spearmanr
def auc(score, lab):
    s = np.array(score); l = np.array(lab, bool)
    if l.all() or (~l).all(): return None
    from scipy.stats import rankdata
    r = rankdata(s); n1 = l.sum(); n0 = (~l).sum()
    return float((r[l].sum() - n1*(n1+1)/2)/(n1*n0))
def circ_smooth(a, w=7):
    k = np.ones(w)/w; m = len(a); ext = np.concatenate([a[-w:], a, a[:w]])
    return np.convolve(ext, k, 'same')[w:w+m]
def four_col_nbr(T, col, free):
    fs = set(free); return sum(1 for v in fs if len(set(col[w] for w in T.adj[v] if w not in fs)) == 4)

def analyse(fn, D=12, ks=(0,1,2,3)):
    T, A, B, a, b, R0 = load(fn); n = len(T.adj); allv = set(range(n))
    c = close(T, A, B, a, b); col, new, K = c['col'], c['new'], c['K']
    ch = set(v for v in new if new[v] != col[v])
    sv = set(x for u in A for w in T.adj[u] if w not in A for x in (u, w)); dS = multi_bfs(T.adj, list(sv), allv)
    cA, cB, lab = seam_geometry(T, A, B, a, c['p'])
    colBp = {v: c['p'][b[v]] for v in B}
    off = offset_profile(T, cA, cB, a, colBp)
    out = dict(file=os.path.basename(fn), R=c['R'], L=len(seam_edges(T, A)), nconf=len(K), nchanged=len(ch),
               tA=cA.tau(a), tB=cB.tau(colBp), off_radius=round(off['radius'], 2), sigma=off['sigma'])
    # feasibility scans
    feas = {}
    for k in ks:
        free = [v for v in range(n) if dS[v] <= k]
        pen = min(bm(T, col, free, d=D, seed=s)[0] for s in range(2))
        feas['band%d' % k] = (len(free), float('%.2e' % pen), four_col_nbr(T, col, free))
    dK = multi_bfs(T.adj, list(K), allv)
    for r in range(0, c['R']+1):
        free = [v for v in range(n) if dK.get(v, 99) <= r]
        pen = min(bm(T, col, free, d=D, seed=s)[0] for s in range(2))
        feas['conf%d' % r] = (len(free), float('%.2e' % pen), four_col_nbr(T, col, free))
    out['feas'] = feas
    # twist profiles on band k=1 (4 rows) and k=2 (6 rows)
    mA = cA.m; dev = np.array([off['dev'].get(i, np.nan) for i in range(mA)])
    dev = np.where(np.isnan(dev), np.nanmean(dev), dev)
    chg_i = np.zeros(mA); conf_i = np.zeros(mA)
    for v in ch: chg_i[lab[v]] += 1
    for v in K: conf_i[lab[v]] += 1
    prof = {}
    for k in (1, 2):
        free = [v for v in range(n) if dS[v] <= k]
        for init in ('rand', 'old'):
            pen, Y, C = bm(T, col, free, d=D, init=init, seed=1)
            Xv = bm_X(Y, C); vm = vec_metrics(free, Xv)
            dist = np.array([vm[v]['dist'] for v in free]); proj = np.array([vm[v]['proj'] for v in free])
            snapped = float(np.mean(dist < 0.1)); far = float(np.mean(dist > 0.5))
            near_old = float(np.mean([vm[v]['near'] == col[v] for v in free])); near_new = float(np.mean([vm[v]['near'] == new[v] for v in free]))
            # triangle frame angles (projected vectors; pinned = corners)
            pv = {v: vm[v]['p'] for v in free}
            ang_i = [[] for _ in range(mA)]; angs = []
            for f in T.faces:
                if not any(x in pv for x in f): continue
                P = np.array([pv[x] if x in pv else TT[col[x]] for x in f])
                g = frame_angle(P); angs.append(g); ang_i[lab[f[0]]].append(g)
            ang_p = np.array([max(x) if x else 0 for x in ang_i])
            del_i = np.zeros(mA); cnt = np.zeros(mA)
            for v in free: del_i[lab[v]] += vm[v]['dist']; cnt[lab[v]] += 1
            del_i = del_i/np.maximum(cnt, 1)
            S = lambda x: circ_smooth(x)
            rho = lambda x, y: round(float(spearmanr(S(x), S(y))[0]), 2)
            # per-vertex AUCs: does SDP distance flag SAT-changed vertices? baseline: closeness to a conflict
            lv = [v in ch for v in free]
            # lag-1 autocorrelation of per-position angle (smoothness of twist along the seam)
            ac = float(np.corrcoef(ang_p, np.roll(ang_p, 1))[0, 1])
            prof['k%d_%s' % (k, init)] = dict(pen=float('%.1e' % pen), n=len(free), dist_med=round(float(np.median(dist)), 3),
                dist_max=round(float(dist.max()), 3), proj_med=round(float(np.median(proj)), 3), snapped=round(snapped, 3), far=round(far, 3),
                near_old=round(near_old, 3), near_new=round(near_new, 3), ang_med=round(float(np.median(angs)), 1), ang_max=round(float(max(angs)), 1),
                ang_ac1=round(ac, 2),
                rho_dist_chg=rho(del_i, chg_i), rho_dist_dev=rho(del_i, dev), rho_ang_chg=rho(ang_p, chg_i), rho_ang_dev=rho(ang_p, dev),
                rho_conf_chg=rho(conf_i, chg_i), rho_dev_chg=rho(dev, chg_i),
                auc_dist=auc([vm[v]['dist'] for v in free], lv), auc_conf=auc([-dK.get(v, 99) for v in free], lv),
                auc_conf_given_far=auc([-dK.get(v, 99) for v in free if dK.get(v, 99) >= 1], [v in ch for v in free if dK.get(v, 99) >= 1]),
                auc_dist_given_far=auc([vm[v]['dist'] for v in free if dK.get(v, 99) >= 1], [v in ch for v in free if dK.get(v, 99) >= 1]))
            if k == 2 and init == 'rand':
                np.savez(fn.replace('.pkl', '').replace('/inst/', '/prof/') + '.npz', ang=ang_p, dist=del_i, chg=chg_i, conf=conf_i, dev=dev)
    out['prof'] = prof
    return out
if __name__ == '__main__':
    os.makedirs('/mnt/project-files/multiscale/sphere/twist/prof', exist_ok=True)
    o = open(sys.argv[1], 'a')
    for fn in sys.argv[2:]:
        t0 = time.time()
        try: r = analyse(fn)
        except Exception as e: r = dict(file=fn, err=repr(e))
        r['sec'] = round(time.time()-t0); o.write(json.dumps(r)+'\n'); o.flush(); print(json.dumps(r), flush=True)
