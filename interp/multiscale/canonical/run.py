# batch pair induction: python run.py out.jsonl  (jobs inline)
import sys, json, time, collections, random, pickle
sys.path.insert(0, '/mnt/project-files/multiscale/canonical/')
from multiprocessing import Pool
from pi import *
def job(a):
    name, oseed, pol, ipol, Rmax = a; t0 = time.time()
    adj = make(name); rot, emb = rotation(adj); rng = random.Random(oseed)
    faces = []
    u = rng.randrange(len(adj)); w = rot[u][rng.randrange(len(rot[u]))]; f = tuple(emb.traverse_face(u, w))
    order, paths = canonical(adj, rot, f, pol, rng=rng)
    I = Inductor(adj, order, paths, Rmax=Rmax, policy=ipol, seed=oseed); I.node_cap = 150000
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
               maxtau_even=max([r['tau'] for r in I.recs if not r['odd']], default=0), sec=round(time.time()-t0))
    if status == 'ok': out['proper'] = check_proper(adj, I.col)
    if status in ('FAIL', 'UNK'):
        k = len(I.recs) + 3; v = order[k]; P = paths[k]
        out['fail_step'] = dict(k=k, n=k+1, L=len(I.B)+2-len(P), plen=len(P), degv=len(adj[v]), nodd=I.nodd)
        fn = '/mnt/project-files/multiscale/canonical/fail_%s_%d_%s_%s.pkl' % (name, oseed, pol, ipol)
        pickle.dump(dict(job=a, fail=I.fail, order=order, paths=paths, k=k, col=I.col, B=I.B, recs=I.recs[-50:]), open(fn, 'wb')); out['pkl'] = fn
    out['Rtrace'] = [(r['n'], r['L'], r['R']) for r in I.recs if r['R'] > 0][:200]
    return out
if __name__ == '__main__':
    jobs = []
    for name in ['ico4', 'ico10', 'flip7_1', 'flip10_1', 'flip17_1', 'defect10_1', 'hub7_1_14', 'hub10_2_18']:
        for oseed, pol in [(0, 'left'), (0, 'right'), (1, 'rand'), (2, 'rand')]:
            jobs.append((name, oseed, pol, 'keep', 3))
    for name in ['ico4', 'flip7_1']:
        for pol in ['advtau', 'advt', 'rand']: jobs.append((name, 3, 'rand', pol, 3))
    with Pool(3) as P, open(sys.argv[1], 'a') as fo:
        for r in P.imap_unordered(job, jobs):
            fo.write(json.dumps(r) + '\n'); fo.flush()
            print({k: r[k] for k in ('name', 'order', 'policy', 'status', 'steps', 'Rhist', 'maxL', 'sec')}, r.get('fail_step'), flush=True)
