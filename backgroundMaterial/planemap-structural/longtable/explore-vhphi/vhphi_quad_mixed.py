"""EXPLORATORY. Mixed quad game (Kempe with adversary + singleton slides to holes off phi)
on one recorded member. Usage: python3 vhphi_quad_mixed.py SEED_JSON INDEX_OF_FAIL"""
import json, sys, time
from collections import deque
import vhphi_explore as E
import vhphi_quad_explore as Q

def slides(adj_rot, st, phi):
    h = st.index(E.HOLE)
    cols = [st[w] for w in adj_rot[h]]
    for u in adj_rot[h]:
        if u in phi: continue
        if cols.count(st[u]) == 1:
            nxt = list(st); nxt[h] = st[u]; nxt[u] = E.HOLE
            yield E.canon(nxt)

def kempe_out(adj, st, phi):
    h = st.index(E.HOLE)
    # components in G - h: hole has colour HOLE so it is never included
    return list(Q.outcomes(adj, st, phi))

def solve(r, budget=3_000_000):
    n = r['n']; faces = {tuple(f) for f in r['faces']}
    adjT = E.adjacency(faces, n); rot = E.rotation(faces, n)
    s, t = r['deleted']; phi = set(r['phi'])
    adj = [set(a) for a in adjT]; adj[s].discard(t); adj[t].discard(s)
    rotG = [[w for w in rot[v] if w in adj[v]] for v in range(n)]  # cyclic order minus deleted
    report = {}
    for v in r['deg5_off']:
        fans = Q.legal_fans_adj(rot, v, adj)
        starts = list(dict.fromkeys(E.canon(x) for x in E.deletion_states([sorted(a) for a in adj], v)))
        # closure
        succ = {}; q = deque(starts); seen = set(starts)
        while q and len(seen) < budget:
            x = q.popleft()
            moves = kempe_out(adj, x, phi) + [[y] for y in slides(rotG, x, phi)]
            succ[x] = moves
            for res in moves:
                for y in res:
                    if y not in seen: seen.add(y); q.append(y)
        if q:
            report[v] = 'inconclusive (budget)'; continue
        def filled(x):
            h = x.index(E.HOLE); return len({x[w] for w in adj[h]}) <= 3
        win = {x for x in seen if filled(x)}
        changed = True
        while changed:
            changed = False
            for x in seen:
                if x in win: continue
                for res in succ[x]:
                    if all(y in win for y in res):
                        win.add(x); changed = True; break
        res = []
        for i, (p, qq), (a, b) in fans:
            sts = [x for x in starts if x[p] != x[qq] and x[a] != x[b]]
            res.append((i, sum(x in win for x in sts), len(sts)))
        report[v] = {'states': len(seen), 'fans': res}
        print(v, report[v], flush=True)
    return report

if __name__ == '__main__':
    data = json.load(open(sys.argv[1]))
    fails = [r for r in data if r['verdict'] != 'pass']
    r = fails[int(sys.argv[2])]
    print('member', r['n'], r['phi'], r['deleted'])
    t = time.time(); rep = solve(r); print('time', round(time.time()-t))
    json.dump({'member': r, 'report': {str(k): v for k, v in rep.items()}}, open(sys.argv[1].replace('.json', f'-mixed{sys.argv[2]}.json'), 'w'))
