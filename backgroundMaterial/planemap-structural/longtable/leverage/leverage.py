#!/usr/bin/env python3
"""Distant-leverage measurement [exploratory].

For each degree-5 hole v of a triangulation T (sphere or other surface), enumerate all 4-colourings of T - v up to
renaming (via ~/4square/kempe_engine.HoleGame: exact moves, dF, locks, pi). For every unfilled state s and every Kempe
move (chain K, non-web) s -> t record d(K) = min BFS distance in T from v to K (rim = 1), dmax, |K|, and effects:
lock count before/after (F = filled), dF change, and for DL -> DL whether the pi-orbit (cycle or the exit it flows to)
is the same. Output: one JSON line per hole with histograms keyed by source class and d.

usage: leverage.py GRAPHFILE OUT.jsonl [--sample K --seed S] [--maxstates M] [--surface NAME]
graph lines: 'name n r0;r1;...' (rotation systems), or --json map files from ~/4square/maps.
"""
import sys, os, json, random, collections, argparse, time
sys.path.insert(0, os.path.expanduser('~/4square'))
from kempe_engine import HoleGame

def bfs(adj, s):
    d = [-1] * len(adj); d[s] = 0; q = collections.deque([s])
    while q:
        u = q.popleft()
        for w in adj[u]:
            if d[w] < 0: d[w] = d[u] + 1; q.append(w)
    return d

class LevGame(HoleGame):
    def __init__(self, n, adj, hole, link, **kw):
        self.dist = bfs([sorted(set(a)) for a in adj], hole)
        super().__init__(n, adj, hole, link, **kw)
    def _moves(self):
        self.moves, self.N, self.mx = [], [], []
        self.filled = [self.rimcount(c) <= self.goal for c in self.states]
        dist = self.dist
        for c in self.states:
            ch = self.chains(c); self.N.append(len(ch)); mv = []; mx = []
            for K in ch:
                if K['web']: continue
                ds = [dist[u] for u in K['set']]
                mv.append((self.index[self.canon(self.flip(c, K))], len(K['set']), len(K['rim']), K['pair']))
                mx.append((min(ds), max(ds)))
            self.moves.append(mv); self.mx.append(mx)

def orbits(g):
    """pi-orbit id of every DL state: ('c', cycle-min) if it reaches a closed all-DL cycle, else ('x', exit state)"""
    orb = {}
    for s in range(g.S):
        if not g.dl[s] or s in orb: continue
        path, pos, k = [], {}, s
        while k is not None and g.dl[k] and k not in pos and k not in orb:
            pos[k] = len(path); path.append(k); k = g.pi[k]
        if k in orb: o = orb[k]
        elif k is not None and k in pos: o = ('c', min(path[pos[k]:]))
        else: o = ('x', k)
        for p in path: orb[p] = o
    return orb

def lk(g, k):
    return 'F' if g.filled[k] else str(g.locks(k))

def analyse(g, word):
    orb = orbits(g)
    H = collections.defaultdict(lambda: collections.Counter())   # key 'src|d' -> counter
    st = collections.Counter()
    # nb1[k]: number of dF-reducing swaps at k whose chain touches the rim (d = 1): the 'paths near the hole'
    nb1 = [sum(1 for (t, *_), (dm, _) in zip(g.moves[k], g.mx[k]) if dm == 1 and g.dF[k] > 0 and g.dF[t] == g.dF[k] - 1)
           for k in range(g.S)]
    shell = collections.Counter(d for u, d in enumerate(g.dist) if u != g.hole)
    for s in range(g.S):
        if g.filled[s]: continue
        srcs = ['U', 'L%d' % g.locks(s)]
        if g.dl[s]: srcs.append('DL')
        if g.dF[s] >= 3: srcs.append('deep')
        if g.dF[s] in (1, 2): srcs.append('D%d' % g.dF[s])
        if g.dF[s] < 0: srcs.append('targetless')
        for src in srcs: st[src] += 1; st[src + '_moves'] += len(g.moves[s])
        best_d = []
        for (t, size, nrim, pair), (dmin, dmax) in zip(g.moves[s], g.mx[s]):
            ev = collections.Counter()
            ev['n'] = 1; ev['size'] = size; ev['dmax'] = dmax; ev['rim'] = int(nrim > 0)
            ev['lk_' + lk(g, s) + lk(g, t)] = 1
            if g.dl[s] and not g.dl[t]: ev['unlockDL'] = 1
            if not g.filled[t] and (g.L1[s], g.L2[s]) != (g.L1[t], g.L2[t]): ev['lockbits'] = 1
            if g.locks(s) > 0 and not g.filled[t] and g.locks(t) < g.locks(s): ev['lockdown'] = 1
            if g.locks(s) < 2 and not g.filled[t] and g.locks(t) > g.locks(s): ev['lockup'] = 1
            if g.filled[t]: ev['fill'] = 1
            if g.dF[s] >= 0 and g.dF[t] >= 0:
                dd = g.dF[t] - g.dF[s]; ev['dF%+d' % dd] = 1
                if dd < 0: best_d.append(dmin)
            if g.dl[s] and g.dl[t]:
                ev['pi_same' if orb[s] == orb[t] else 'pi_jump'] = 1
                if t == g.pi[s]: ev['is_pi'] = 1
                if orb[t][0] == 'c': ev['to_cycle'] = 1
            if g.dF[t] == g.dF[s] and g.dF[s] > 0:     # a sideways swap: does it open / close paths near the hole?
                ev['side'] = 1; ev['side_gain'] = nb1[t] - nb1[s]
                if nb1[t] > nb1[s]: ev['side_open'] = 1
                if nb1[t] < nb1[s]: ev['side_close'] = 1
                if nb1[s] == 0 and nb1[t] > 0: ev['side_open_from0'] = 1
            if g.cls[t] != g.cls[s]: ev['BUG_cls'] = 1
            for src in srcs: H['%s|%d' % (src, dmin)].update(ev)
        if best_d:
            for src in srcs:
                st[src + '_bestnear%d' % min(best_d)] += 1   # nearest dF-reducing move
                st[src + '_bestfar%d' % max(best_d)] += 1
                st[src + '_allbestfar'] += int(min(best_d) >= 2)
    ncyc = len(set(o for o in orb.values() if o[0] == 'c'))
    return {'S': g.S, 'unfilled': sum(1 for x in g.filled if not x), 'maxdF': max(g.dF, default=-1), 'ncls': len(g.classes),
            'npicyc': ncyc, 'word': word, 'shell': dict(shell), 'states': dict(st),
            'H': {k: dict(v) for k, v in H.items()}}

def parse_line(line):
    p = line.split()
    name, n = p[0], int(p[1])
    rot = [[int(x) for x in r.split(',')] for r in p[2].split(';')]
    return name, n, rot

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('graphs'); ap.add_argument('out')
    ap.add_argument('--sample', type=int, default=0); ap.add_argument('--seed', type=int, default=1)
    ap.add_argument('--maxstates', type=int, default=400000)
    ap.add_argument('--surface', default='sphere'); ap.add_argument('--json', action='store_true')
    ap.add_argument('--holes', default='')    # for --json: override hole list
    ap.add_argument('--tlimit', type=float, default=840)
    a = ap.parse_args()
    t0 = time.time()
    items = []
    if a.json:
        for f in a.graphs.split(','):
            d = json.load(open(f)); rot = d['rot']
            items.append((os.path.basename(f)[:-5], len(rot), rot, [d['hole']]))
    else:
        for line in open(a.graphs):
            if not line.strip() or line.startswith('#'): continue
            name, n, rot = parse_line(line)
            items.append((name, n, rot, [v for v in range(n) if len(rot[v]) == 5]))
    holes = [(nm, n, rot, h) for nm, n, rot, hs in items for h in hs]
    if a.sample and a.sample < len(holes):
        random.Random(a.seed).shuffle(holes); holes = holes[:a.sample]
    done = set()
    if os.path.exists(a.out):
        for l in open(a.out): r = json.loads(l); done.add((r['name'], r['hole']))
    with open(a.out, 'a') as fo:
        for nm, n, rot, h in holes:
            if (nm, h) in done: continue
            if time.time() - t0 > a.tlimit: print('time limit', file=sys.stderr); break
            word = ''.join(sorted(str(min(len(rot[x]), 9)) for x in rot[h]))
            try:
                g = LevGame(n, rot, h, rot[h], limit=a.maxstates)
            except RuntimeError as e:
                fo.write(json.dumps({'name': nm, 'hole': h, 'n': n, 'surface': a.surface, 'skip': str(e)}) + '\n'); continue
            r = analyse(g, word); r.update(name=nm, hole=h, n=n, surface=a.surface)
            fo.write(json.dumps(r) + '\n'); fo.flush()
    print('done %.1fs' % (time.time() - t0), file=sys.stderr)

if __name__ == '__main__':
    main()
