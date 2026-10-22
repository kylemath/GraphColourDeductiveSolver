# python run_mc.py out.jsonl name:oseed:order:J:variant:k0:cutmode ...   (policy keep-by-fewest-cuts, Rmax 4)
import sys, json, time, collections, random, pickle
sys.path.insert(0, '/mnt/project-files/multiscale/multicut/'); sys.path.insert(0, '/mnt/project-files/multiscale/canonical/')
from multiprocessing import Pool
from pi import make, rotation, canonical, check_proper
from mcstep import MCInductor, RepairInductor
TLIM = int(__import__('os').environ.get('TLIM', '1500'))
def job(spec):
    parts = spec.split(':'); name, oseed, pol, J, var, k0, cm = parts[:7]; rep = parts[7:]; oseed = int(oseed); J = int(J); k0 = None if k0 == 'none' else int(k0)
    t0 = time.time(); adj = make(name); rot, emb = rotation(adj); rng = random.Random(oseed)
    u = rng.randrange(len(adj)); w = rot[u][rng.randrange(len(rot[u]))]; f = tuple(emb.traverse_face(u, w))
    order, paths = canonical(adj, rot, f, pol, rng=rng)
    I = (RepairInductor if rep else MCInductor)(adj, order, paths, Rmax=4, policy='keep', seed=oseed); I.node_cap = 400000
    if rep: I.rep_d = int(rep[0]); I.rep_r = int(rep[1])
    I.J = J; I.tfree = var.endswith('T'); I.variant = var.rstrip('T'); I.k0 = k0; I.cutmode = cm
    status = 'ok'; err = None
    try:
        for k in range(3, len(order)):
            if I.step(k) is None: status = 'FAIL'; break
            if time.time() - t0 > TLIM: status = 'timeout'; break
    except RuntimeError as e: status = 'UNK'; err = str(e)
    rs = I.recs; Rh = collections.Counter(r['R'] for r in rs); Ch = collections.Counter(r['ncuts'] for r in rs)
    out = dict(spec=spec, name=name, n=len(adj), status=status, err=err, steps=len(rs), Rhist=dict(sorted(Rh.items())), cuthist=dict(sorted(Ch.items())),
               maxR=max([r['R'] for r in rs], default=0), maxcuts=max([r['ncuts'] for r in rs], default=0), maxnodd=I.nodd, ncapfail=len(I.capfails or []),
               maxL=max([r['L'] for r in rs], default=0), nrep=getattr(I, 'nrep', None), nrep_try=getattr(I, 'nrep_try', None), maxcuts_after=max([r.get('ncuts_after', r['ncuts']) for r in rs], default=0), sec=round(time.time()-t0))
    # cuts-over-time: (n, nodd, ncuts) at every change of ncuts or nodd
    tr = []; last = None
    for r in rs:
        key = (r['nodd'], r['ncuts'], r.get('ncuts_after'))
        if key != last: tr.append((r['n'], r['nodd'], r['ncuts'], r.get('ncuts_after'), r['R'])); last = key
    out['trace'] = tr[:400]; out['Rtrace'] = [(r['n'], r['R'], r['nodd'], r['ncuts']) for r in rs if r['R'] > 0][:300]
    if status == 'ok': out['proper'] = check_proper(adj, I.col)
    else:
        k = len(rs) + 3; out['fail_step'] = dict(n=k+1, nodd=I.nodd, L=len(I.B) + 1, odd=I.nodd % 2 == 1)
        fn = '/mnt/project-files/multiscale/multicut/fail_%s.pkl' % spec.replace(':', '_')
        pickle.dump(dict(spec=spec, fail=I.fail, k=k, recs=rs[-60:]), open(fn, 'wb'))
    return out
if __name__ == '__main__':
    with Pool(int(__import__('os').environ.get('NP', '4'))) as P, open(sys.argv[1], 'a') as fo:
        for r in P.imap_unordered(job, sys.argv[2:]):
            fo.write(json.dumps(r) + '\n'); fo.flush()
            print({k: r[k] for k in ('spec', 'status', 'err', 'steps', 'Rhist', 'cuthist', 'maxnodd', 'ncapfail', 'nrep', 'maxcuts_after', 'sec')}, r.get('fail_step'), flush=True)
