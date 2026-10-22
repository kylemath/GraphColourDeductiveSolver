# batch: python run_step.py out.jsonl name:oseed:order:k0 ...  (k0 = none | 3 | 4)   (policy keep, Rmax 4, 25 min cap per job)
import sys, json, time, collections, random, pickle
sys.path.insert(0, '/mnt/project-files/multiscale/localdetrend/'); sys.path.insert(0, '/mnt/project-files/multiscale/canonical/')
from multiprocessing import Pool
from pi import *
from pi_step import StepInductor
def job(a):
    name, oseed, pol, ipol, Rmax, k0, cm = a; t0 = time.time()
    adj = make(name); rot, emb = rotation(adj); rng = random.Random(oseed)
    u = rng.randrange(len(adj)); w = rot[u][rng.randrange(len(rot[u]))]; f = tuple(emb.traverse_face(u, w))
    order, paths = canonical(adj, rot, f, pol, rng=rng)
    I = StepInductor(adj, order, paths, Rmax=Rmax, policy=ipol, seed=oseed); I.node_cap = 300000; I.k0 = k0; I.cutmode = cm
    status = 'ok'; err = None
    try:
        for k in range(3, len(order)):
            if I.step(k) is None: status = 'FAIL'; break
            if time.time() - t0 > 1500: status = 'timeout'; break
    except RuntimeError as e: status = 'UNK'; err = str(e)
    Rh = collections.Counter(r['R'] for r in I.recs)
    out = dict(name=name, n=len(adj), oseed=oseed, order=pol, policy=ipol, Rmax=Rmax, status=status, err=err,
               steps=len(I.recs), Rhist=dict(sorted(Rh.items())), maxL=max([r['L'] for r in I.recs], default=0),
               t2frac=round(sum(1 for r in I.recs if r['t'] and r['t'] > 1) / max(1, len(I.recs)), 3),
               maxtau_even=max([r['tau'] for r in I.recs if not r['odd']], default=0),
               maxnodd=I.nodd, k0=k0, cutmode=cm, att_ne_min=[(r['n'], r['Rmin'], r['Ratt'], r['tau_min'], r['tau_att']) for r in I.recs if r.get('Rmin') != r.get('Ratt') or abs((r.get('tau_min') or 0) - (r.get('tau_att') or 0)) > 1e-6][:40], capfails=I.capfails, ncapfail=len(I.capfails or []), maxrun=max([r.get('run', 0) for r in I.recs], default=0), sec=round(time.time()-t0))
    if status == 'ok': out['proper'] = check_proper(adj, I.col)
    if status in ('FAIL', 'UNK', 'timeout'):
        k = len(I.recs) + 3; v = order[k]; P = paths[k]
        out['fail_step'] = dict(k=k, n=k+1, L=len(I.B)+2-len(P), plen=len(P), degv=len(adj[v]), nodd=I.nodd)
        fn = '/mnt/project-files/multiscale/localdetrend/fail_%s_%d_%s_%s.pkl' % (name, oseed, pol, ipol)
        pickle.dump(dict(job=a, fail=I.fail, order=order, paths=paths, k=k, col=I.col, B=I.B, recs=I.recs[-50:]), open(fn, 'wb')); out['pkl'] = fn
    out['Rtrace'] = [(r['n'], r['L'], r['R'], r['odd'], r['t'], r['tau_min'], r['tau_att']) for r in I.recs if r['R'] > 0][:300]
    out['nodd_trace'] = [(r['n'], r['t']) for r in I.recs if not r['odd'] and r['t'] and r['t'] > 1][:50]
    return out
if __name__ == '__main__':
    jobs = []
    for spec in sys.argv[2:]:
        name, oseed, pol, k0, cm = spec.split(':'); jobs.append((name, int(oseed), pol, 'keep', 4, None if k0 == 'none' else int(k0), cm))
    with Pool(4) as P, open(sys.argv[1], 'a') as fo:
        for r in P.imap_unordered(job, jobs):
            fo.write(json.dumps(r) + '\n'); fo.flush()
            print({k: r[k] for k in ('name', 'order', 'oseed', 'k0', 'cutmode', 'status', 'err', 'steps', 'Rhist', 'maxL', 'maxtau_even', 'maxnodd', 'ncapfail', 'maxrun', 'sec')}, r.get('fail_step'), flush=True)
