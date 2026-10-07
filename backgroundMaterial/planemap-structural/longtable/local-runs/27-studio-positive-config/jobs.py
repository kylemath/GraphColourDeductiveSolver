#!/usr/bin/env python3
"""jobs.py LABEL=FILE ...: Job S (NightF6Flow §1). Per hole: rem(T) for every nonpositive target hit by an exit (exits = R3 DD-endpoint states of positive cycles with a
lockless sigma-image on another cycle), double hits (#exits vs #distinct excursions), and Lemma P1: assign each def(Z) > 0 to ONE nonpositive sigma-neighbour T with
the assigned total at T <= -rem(T) (exact backtracking); also the splittable form (max-flow) and the group-free class check sum def + sum rem."""
import sys, json
from collections import Counter
def assign_single(Z, cap):
    order = sorted(Z, key=lambda z: (-z[1], len(z[2])))
    used = Counter()
    def bt(i):
        if i == len(order): return True
        zid, d, nb = order[i]
        for t in sorted(nb, key=lambda t: -(cap[t] - used[t])):
            if cap[t] - used[t] >= d:
                used[t] += d
                if bt(i + 1): return True
                used[t] -= d
        return False
    return bt(0)
def maxflow_ok(Z, cap):
    # simple augmenting paths on bipartite graph with integer capacities
    from collections import defaultdict, deque
    g = defaultdict(lambda: defaultdict(int))
    for zid, d, nb in Z:
        g['S'][('z', zid)] += d
        for t in nb: g[('z', zid)][('t', t)] += 10 ** 9
    for t, c in cap.items(): g[('t', t)]['T'] += max(c, 0)
    need = sum(d for _, d, _ in Z); flow = 0
    while True:
        par = {'S': None}; q = deque(['S'])
        while q:
            u = q.popleft()
            for v, c in g[u].items():
                if c > 0 and v not in par: par[v] = u; q.append(v)
        if 'T' not in par: break
        b = 10 ** 18; v = 'T'
        while par[v] is not None: b = min(b, g[par[v]][v]); v = par[v]
        v = 'T'
        while par[v] is not None: g[par[v]][v] -= b; g[v][par[v]] += b; v = par[v]
        flow += b
    return flow >= need
for a in sys.argv[1:]:
    lab, f = a.split('='); T = Counter(); remviol = []; dbl = []; p1fail = []; p1split_fail = []; worst = None
    for l in open(f):
        if '"jobs": {"pos": [{' not in l: continue
        r = json.loads(l); js = r['jobs']; T['holes'] += 1
        tg = {t[0]: dict(Lam=t[1], L=t[2], hit=t[3], nh=t[4], nd=t[5], rem=t[6]) for t in js['targets']}
        for tid, t in tg.items():
            if t['nh'] > 0:
                T['hit_targets'] += 1
                if t['rem'] > 0: remviol.append((r['name'], r['hole'], tid, t))
                if worst is None or t['rem'] > worst[0]: worst = (t['rem'], r['name'], r['hole'], tid, t)
            if t['nh'] != t['nd']: dbl.append((r['name'], r['hole'], tid, t))
        T['pos'] += len(js['pos']); deficits = [(z['id'], z['def'], z['nbrN']) for z in js['pos'] if z['def'] > 0]
        T['def_pos'] += len(deficits); T['def_pos_gamma'] += sum(1 for z in js['pos'] if z['def'] > 0 and z['gamma'])
        if deficits:
            cap = {t: -tg[t]['rem'] for t in tg}
            if not assign_single(deficits, cap): p1fail.append((r['name'], r['hole'], deficits, {t: cap[t] for z in deficits for t in z[2]}))
            if not maxflow_ok(deficits, cap): p1split_fail.append((r['name'], r['hole']))
    print('== %s: holes with a positive cycle %d, positive cycles %d (def > 0: %d, of which Gamma %d); hit nonpositive targets %d'
          % (lab, T['holes'], T['pos'], T['def_pos'], T['def_pos_gamma'], T['hit_targets']))
    print('   Lemma R: targets with rem > 0: %d %s; max rem %s' % (len(remviol), remviol[:3], worst[:4] if worst else None))
    print('   double hits (#exits != #distinct excursions): %d %s' % (len(dbl), dbl[:3]))
    print('   Lemma P1 single-target assignment fails at %d holes %s; splittable form fails at %d' % (len(p1fail), p1fail[:3], len(p1split_fail)))
