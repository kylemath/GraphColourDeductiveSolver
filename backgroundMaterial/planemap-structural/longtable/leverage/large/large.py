#!/usr/bin/env python3
"""Distant leverage on large-diameter sphere maps [exploratory].

Follow-up to ../README.md. Two modes per hole:
  exact  : S <= --maxS, the HoleGame engine via leverage.LevGame/analyse (exact dF; same output as ../leverage.py)
  sample : uniform sample of the hole's Kempe class (Metropolis-corrected random Kempe walk from a backtracking
           colouring of T - v), single-step quantities only (unlock DL -> not DL, lock changes, fill, pi-orbit jump);
           no dF. Same histogram keys, so the analysis can mix the two (keys that need dF are absent).

Graph sources (--kind):
  rot    : lines 'name n r0;r1;...' (TrackF graphs); holes = degree-5 vertices
  sw     : as rot, but every graph is first given one Stone-Wales flip (dual: flip an edge between two degree-6
           vertices whose apices have degree 5) that makes two pentagons adjacent -> a non-IPR fullerene dual
  glued  : ../../gluing/*.jsonl records with 'rot'; holes = the evaluated holes of the record
  pad    : lines 'name n rot' or --json maps; the farthest face (a,b,c) from the hole gets k = 0..K outer bands
           (new A,B,C with AB,BC,CA,Aa,Ab,Bb,Bc,Cc,Ca), each band then becomes the next outer face
"""
import sys, os, json, random, collections, argparse, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from leverage import LevGame, analyse, bfs, parse_line


# ------------------------------------------------------------------------------------------------ graph sources
def sw_flip(rot, rng):
    """one Stone-Wales flip making two degree-5 vertices adjacent; returns new rot or None"""
    n = len(rot); cand = []
    for u in range(n):
        if len(rot[u]) != 6: continue
        for i, v in enumerate(rot[u]):
            if v < u or len(rot[v]) != 6: continue
            p, q = rot[u][i - 1], rot[u][(i + 1) % 6]
            if len(rot[p]) == 5 and len(rot[q]) == 5 and q not in rot[p]: cand.append((u, v, p, q))
    if not cand: return None
    u, v, p, q = rng.choice(cand)
    R = [list(r) for r in rot]
    R[u].remove(v); R[v].remove(u)
    for x, y in ((p, q), (q, p)):          # insert y between u and v in the rotation of x
        r = R[x]; iu, iv = r.index(u), r.index(v)
        if (iu + 1) % len(r) == iv: r.insert(iu + 1, y)
        else: r.insert(iv + 1, y)
    return R


def pad(rot, hole, k):
    """add k outer bands around the face farthest from the hole (adjacency only; the hole's link order is kept)"""
    adj = [list(r) for r in rot]
    dist = bfs([sorted(set(a)) for a in adj], hole)
    best = None
    for v in range(len(rot)):
        r = rot[v]
        for i in range(len(r)):
            f = (v, r[i], r[(i + 1) % len(r)])
            key = (min(dist[x] for x in f), sum(dist[x] for x in f))
            if best is None or key > best[0]: best = (key, f)
    a, b, c = best[1]
    for _ in range(k):
        A, B, C = len(adj), len(adj) + 1, len(adj) + 2
        adj += [[B, C, a, b], [A, C, b, c], [A, B, c, a]]
        adj[a] += [A, C]; adj[b] += [A, B]; adj[c] += [B, C]
        a, b, c = A, B, C
    return adj


# ------------------------------------------------------------------------------------------------ sampler
class Sampler:
    def __init__(self, adj, hole, link):
        self.n = len(adj); self.hole = hole; self.link = list(link); self.rimset = set(link)
        self.adj = [sorted(set(a)) for a in adj]
        self.V = [u for u in range(self.n) if u != hole]
        self.nb = [[w for w in self.adj[u] if w != hole] for u in range(self.n)]
        self.dist = bfs(self.adj, hole)
        # odd-degree vertices of T other than the hole and the rim (the 'charges' of the lock-parity reading)
        self.odd = {u for u in self.V if len(self.adj[u]) % 2 == 1 and u not in self.rimset}

    def colour(self, rng):
        """a proper 4-colouring of T - v by randomised backtracking in BFS order"""
        s0 = rng.choice(self.V); order = [s0]; seen = {s0}; i = 0
        while i < len(order):
            for w in self.nb[order[i]]:
                if w not in seen: seen.add(w); order.append(w)
            i += 1
        pos = {u: j for j, u in enumerate(order)}
        back = [[w for w in self.nb[u] if pos[w] < pos[u]] for u in order]
        c = [-1] * self.n; budget = [200000]
        sys.setrecursionlimit(max(2000, 6 * self.n))

        def rec(j):
            if j == len(order): return True
            budget[0] -= 1
            if budget[0] < 0: return False
            bad = {c[w] for w in back[j]}; cols = [0, 1, 2, 3]; rng.shuffle(cols)
            for x in cols:
                if x in bad: continue
                c[order[j]] = x
                if rec(j + 1): return True
            c[order[j]] = -1
            return False
        if not rec(0): return None
        return c

    def moves(self, c):
        """non-web chains: list of (a, b, frozenset)"""
        out = []
        for a in range(4):
            for b in range(a + 1, 4):
                seen = set(); comps = []
                for s in self.V:
                    if s in seen or (c[s] != a and c[s] != b): continue
                    comp = [s]; seen.add(s); st = [s]
                    while st:
                        u = st.pop()
                        for w in self.nb[u]:
                            if w not in seen and (c[w] == a or c[w] == b): seen.add(w); comp.append(w); st.append(w)
                    comps.append(comp)
                if len(comps) > 1: out.extend((a, b, comp) for comp in comps)
        return out

    @staticmethod
    def flip(c, a, b, comp):
        d = list(c)
        for u in comp: d[u] = b if c[u] == a else a
        return d

    def canon(self, c):
        mp = {}
        return ''.join(str(mp.setdefault(c[u], len(mp))) for u in self.V)

    def filled(self, c):
        return len({c[x] for x in self.link}) <= 3

    def chain_at(self, c, u, b):
        a = c[u]; comp = {u}; st = [u]
        while st:
            v = st.pop()
            for w in self.nb[v]:
                if w not in comp and (c[w] == a or c[w] == b): comp.add(w); st.append(w)
        return comp

    def status(self, c):
        """(filled, L1, L2, pi-target or None)"""
        if self.filled(c): return True, False, False, None
        L = self.link; col = [c[x] for x in L]
        for t in range(5):
            if col[t] == col[(t + 2) % 5]:
                x = [L[(t + i) % 5] for i in range(5)]; al, ga, de = col[t], col[(t + 3) % 5], col[(t + 4) % 5]
                break
        l1 = x[3] in self.chain_at(c, x[1], ga)
        l2 = x[4] in self.chain_at(c, x[1], de)
        pit = None
        if l1 and l2:
            K = self.chain_at(c, x[2], ga); pit = self.flip(c, al, ga, K)
        return False, l1, l2, pit

    def orbit(self, c, cap=600):
        """pi-orbit id as in leverage.orbits: ('c', min key of the all-DL cycle) or ('x', key of the exit state)"""
        pos = {}; path = []; k = c
        while True:
            f, l1, l2, pit = self.status(k)
            key = self.canon(k)
            if not (l1 and l2): return ('x', key)
            if key in pos: return ('c', min(path[pos[key]:]))
            pos[key] = len(path); path.append(key)
            if len(path) > cap: return ('?', key)
            k = pit

    def measure(self, c, H, st, mv):
        f, l1, l2, pit = self.status(c)
        if f: st['filled'] += 1; return
        dl = l1 and l2; nl = int(l1) + int(l2)
        srcs = ['U', 'L%d' % nl] + (['DL'] if dl else [])
        for s in srcs: st[s] += 1; st[s + '_moves'] += len(mv)
        if dl:
            o_s = self.orbit(c); pikey = self.canon(pit)
        unl = []
        for a, b, comp in mv:
            ds = [self.dist[u] for u in comp]; dmin = min(ds)
            t = self.flip(c, a, b, comp)
            ft, t1, t2, _ = self.status(t)
            ev = collections.Counter(n=1, size=len(comp), dmax=max(ds), rim=int(dmin == 1))
            if any(u in self.odd for u in comp): ev['odd'] = 1
            ltn = 'F' if ft else str(int(t1) + int(t2))
            ev['lk_%d%s' % (nl, ltn)] = 1
            if ft: ev['fill'] = 1
            else:
                if (l1, l2) != (t1, t2): ev['lockbits'] = 1
                if nl > 0 and int(t1) + int(t2) < nl: ev['lockdown'] = 1
                if nl < 2 and int(t1) + int(t2) > nl: ev['lockup'] = 1
            if dl:
                if not (t1 and t2):
                    ev['unlockDL'] = 1; unl.append(dmin)
                    if ev['odd']: ev['unlock_odd'] = 1
                else:
                    ev['pi_same' if self.orbit(t) == o_s else 'pi_jump'] = 1
                    if self.canon(t) == pikey: ev['is_pi'] = 1
            for s in srcs: H['%s|%d' % (s, dmin)].update(ev)
        if dl:
            if unl:
                st['DL_unl_nearest%d' % min(unl)] += 1; st['DL_unl_any'] += 1
                st['DL_unl_onlyfar'] += int(min(unl) >= 2)
                st['DL_unl_far_avail'] += int(max(unl) >= 2)
            else: st['DL_unl_none'] += 1

    def run(self, rng, nsamp, burn, thin, tmax):
        t0 = time.time()
        H = collections.defaultdict(collections.Counter); st = collections.Counter()
        c = None
        for _ in range(5):
            c = self.colour(rng)
            if c is not None: break
        if c is None: return None
        mv = self.moves(c); taken = 0; acc = 0; steps = 0
        while taken < nsamp and time.time() - t0 < tmax:
            if not mv: break
            a, b, comp = rng.choice(mv)
            t = self.flip(c, a, b, comp); mt = self.moves(t)
            if mt and rng.random() < len(mv) / len(mt): c, mv = t, mt; acc += 1
            steps += 1
            if steps > burn and (steps - burn) % thin == 0:
                self.measure(c, H, st, mv); taken += 1
        return {'H': {k: dict(v) for k, v in H.items()}, 'states': dict(st), 'samples': taken, 'steps': steps,
                'acc': acc / max(1, steps), 'secs': round(time.time() - t0, 1)}


# ------------------------------------------------------------------------------------------------ driver
def items_from(a, rng):
    """yield (name, adj/rot, hole-list, extra-dict)"""
    if a.kind in ('rot', 'sw'):
        for f in a.src.split(','):
            for line in open(f):
                if not line.strip() or line.startswith('#'): continue
                nm, n, rot = parse_line(line)
                if a.minn and n < a.minn or a.maxn and n > a.maxn: continue
                ex = {}
                if a.kind == 'sw':
                    rot = sw_flip(rot, rng)
                    if rot is None: continue
                    nm += '/sw'; ex['ipr'] = False
                yield nm, rot, [v for v in range(n) if len(rot[v]) == 5], ex
    elif a.kind == 'glued':
        for f in a.src.split(','):
            for line in open(f):
                r = json.loads(line)
                if 'rot' not in r: continue
                rot = [[int(x) for x in s.split(',')] for s in r['rot'].split(';')]
                yield r['name'], rot, [h['h'] for h in r['holes']], {'Sknown': {h['h']: h['S'] for h in r['holes']}}
    elif a.kind == 'pad':
        base = []
        for f in a.src.split(','):
            if f.endswith('.json'):
                d = json.load(open(f)); base.append((os.path.basename(f)[:-5], d['rot'], [d['hole']]))
            else:
                for line in open(f):
                    if line.strip() and not line.startswith('#'):
                        nm, n, rot = parse_line(line); base.append((nm, rot, [v for v in range(n) if len(rot[v]) == 5]))
        for nm, rot, hs in base:
            hs = list(hs)
            if a.holes and len(hs) > a.holes: rng.shuffle(hs); hs = hs[:a.holes]
            for h in hs:
                for k in range(a.kmax + 1):
                    adj = pad(rot, h, k)
                    yield '%s+pad%d' % (nm, k), adj, [h], {'k': k, 'base': nm, 'link': rot[h]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('kind'); ap.add_argument('src'); ap.add_argument('out')
    ap.add_argument('--family', default='')
    ap.add_argument('--holes', type=int, default=0, help='max holes per graph (random)')
    ap.add_argument('--graphs', type=int, default=0, help='max graphs (random sample)')
    ap.add_argument('--minn', type=int, default=0); ap.add_argument('--maxn', type=int, default=0)
    ap.add_argument('--kmax', type=int, default=4)
    ap.add_argument('--mode', default='auto'); ap.add_argument('--maxS', type=int, default=200000)
    ap.add_argument('--exactn', type=int, default=44, help='auto: try exact only when n <= this')
    ap.add_argument('--nsamp', type=int, default=3000); ap.add_argument('--burn', type=int, default=400)
    ap.add_argument('--thin', type=int, default=3); ap.add_argument('--htime', type=float, default=60)
    ap.add_argument('--tlimit', type=float, default=840); ap.add_argument('--seed', type=int, default=1)
    a = ap.parse_args()
    rng = random.Random(a.seed); t0 = time.time()
    items = list(items_from(a, rng))
    if a.graphs and a.graphs < len(items) and a.kind != 'pad':
        rng.shuffle(items); items = items[:a.graphs]
    jobs = []
    for nm, rot, hs, ex in items:
        hs = list(hs)
        if a.holes and len(hs) > a.holes: rng.shuffle(hs); hs = hs[:a.holes]
        jobs += [(nm, rot, h, ex) for h in hs]
    done = set()
    if os.path.exists(a.out):
        for l in open(a.out):
            try: r = json.loads(l); done.add((r['name'], r['hole'], r.get('mode')))
            except ValueError: pass
    with open(a.out, 'a') as fo:
        for nm, rot, h, ex in jobs:
            if time.time() - t0 > a.tlimit: print('time limit', file=sys.stderr); break
            n = len(rot); link = ex.get('link', rot[h])
            mode = a.mode
            if mode == 'auto':
                Sk = ex.get('Sknown', {}).get(h)
                mode = 'exact' if (n <= a.exactn and (Sk is None or Sk <= a.maxS)) else 'sample'
            if (nm, h, mode) in done: continue
            dist = bfs([sorted(set(x)) for x in rot], h)
            rec = {'name': nm, 'hole': h, 'n': n, 'family': a.family, 'ecc': max(dist),
                   'shell': dict(collections.Counter(d for u, d in enumerate(dist) if u != h))}
            rec.update({k: v for k, v in ex.items() if k in ('k', 'base', 'ipr')})
            rec['word'] = ''.join(sorted(str(min(len(set(rot[x])), 9)) for x in link))
            th = time.time()
            if mode == 'exact':
                try:
                    g = LevGame(n, rot, h, link, limit=a.maxS)
                    r = analyse(g, rec['word']); r.pop('shell', None); rec.update(r); rec['mode'] = 'exact'
                except RuntimeError:
                    mode = 'sample'
            if mode == 'sample':
                r = Sampler(rot, h, link).run(random.Random(rng.random()), a.nsamp, a.burn, a.thin, a.htime)
                if r is None: rec['skip'] = 'no colouring'
                else: rec.update(r)
                rec['mode'] = 'sample'
            rec['secs'] = round(time.time() - th, 1)
            fo.write(json.dumps(rec) + '\n'); fo.flush()
            print(nm, h, rec['mode'], rec.get('S', rec.get('samples')), rec['secs'], file=sys.stderr)
    print('done %.1fs' % (time.time() - t0), file=sys.stderr)


if __name__ == '__main__':
    main()
