# W16: which link classes of the 5/6/7 world carry the t > 0 obstruction? On the row-generation active set (a subset of the world,
# so every positive value here is a valid lower bound for the world minus the dropped rows), drop all receivers of one canonical
# link class at a time, then cumulatively in order of effect.  usage: python3 -I drop_links.py ROWS.pkl CERT_SUMMARY.json OUT.json [NTOP]
import sys, os, pickle, json, collections, time
sys.path.insert(0, '/tmp/swarm-W16/code')
import w16lib as W
T0 = time.time()
def log(*a): print(*a, '[%.0fs]' % (time.time() - T0), flush=True)
if __name__ == '__main__':
    ARGV = list(sys.argv); W.init()
    rows = pickle.load(open(ARGV[1], 'rb'))['rows']; S = json.load(open(ARGV[2])); out = ARGV[3]; ntop = int(ARGV[4]) if len(ARGV) > 4 else 12
    L = collections.Counter()
    for v, k in S['support']:
        if k.startswith('R'): L[k.split()[1].split('/')[0]] += v
    top = [l for l, _ in L.most_common(ntop)]
    def lp(drop):
        sub = [r for r in rows if not (r[2] == 'le' and ''.join(map(str, r[0][2])) in drop)]
        res, keys, rmap = W.solve_lp(sub); return float(res.fun) if res.status == 0 else None, sum(1 for r in rows if r[2] == 'le') - sum(1 for r in sub if r[2] == 'le')
    t0, _ = lp(set()); log('baseline t = %.12f' % t0); R = dict(baseline=t0, single={}, cumulative=[])
    for l in top:
        t, n = lp({l}); R['single'][l] = (t, n, round(L[l], 6)); log('drop %s (%d rows, cert weight %.4f): t = %.12f' % (l, n, L[l], t))
    order = sorted(top, key=lambda l: R['single'][l][0]); drop = set()
    for l in order:
        drop.add(l); t, n = lp(drop); R['cumulative'].append((sorted(drop), t, n)); log('cumulative drop %s (%d rows): t = %.12f' % (sorted(drop), n, t))
        json.dump(R, open(out, 'w'), indent=1)
        if t is not None and t <= 1e-9: break
    json.dump(R, open(out, 'w'), indent=1)
