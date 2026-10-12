#!/usr/bin/env python3
"""TrackO task 2: adversarial flip search on triangulated spheres, objective = max interior pi-run R over all holes.

usage: to_search.py OUT_PREFIX --seeds FILE[:name1,name2] [--mindeg 5|3] [--nmax 60] [--minutes 60] [--batch 12]
                    [--cap 400000] [--seed 1]
Moves: edge flips keeping the graph simple and min degree >= mindeg; with --mindeg 3 also insertion of a degree-3 vertex
into a face (n <= nmax) and deletion of a degree-3 vertex (n >= 20).  Each round proposes --batch candidates (1-2 moves
each) from the current graph, scores them with to_eng -q (states per hole capped at --cap; holes over the cap are
ignored), moves to the best candidate if its score (maxR, W) is >= the current one, otherwise with probability --pdown;
returns to the seed's best graph every --revert stale rounds and switches seed after --restart stale rounds.
Score W = sum over maximal interior runs of 4^L.  With --frame every candidate must pass Census29/bin/frame (frame class).
Every graph reaching a new best maxR, and every graph with maxR >= 6,
is appended to OUT_PREFIX.hits.txt (rotation line) with its score in OUT_PREFIX.log.
"""
import sys, os, random, subprocess, time, argparse

HERE = os.path.dirname(os.path.abspath(__file__))
ENG = os.path.join(HERE, 'to_eng2')


class Tri:
    def __init__(self, rot):
        # build oriented faces from rotations (rotation order = cyclic link order)
        faces = set()
        for v, r in enumerate(rot):
            k = len(r)
            for i in range(k):
                a, b = r[i], r[(i + 1) % k]
                f = (v, a, b)
                m = min(range(3), key=lambda t: f[t])
                faces.add(f[m:] + f[:m])
        # consistent orientation check: each directed edge once
        nxt = {}
        for (a, b, c) in faces:
            for (x, y, z) in ((a, b, c), (b, c, a), (c, a, b)):
                nxt[(x, y)] = z
        self.nxt = nxt
        self.n = len(rot)
        self.adj = [set(r) for r in rot]
        assert len(nxt) == sum(len(r) for r in rot), 'orientation inconsistent'

    def copy(self):
        t = Tri.__new__(Tri); t.nxt = dict(self.nxt); t.n = self.n; t.adj = [set(a) for a in self.adj]; return t

    def deg(self, v): return len(self.adj[v])

    def flip(self, a, b, mindeg):
        if (a, b) not in self.nxt: return False
        c = self.nxt[(a, b)]; d = self.nxt[(b, a)]
        if c == d or d in self.adj[c]: return False
        if self.deg(a) - 1 < mindeg or self.deg(b) - 1 < mindeg: return False
        N = self.nxt
        for e in ((a, b), (b, c), (c, a), (b, a), (a, d), (d, b)): del N[e]
        N[(c, a)] = d; N[(a, d)] = c; N[(d, c)] = a
        N[(d, b)] = c; N[(b, c)] = d; N[(c, d)] = b
        self.adj[a].discard(b); self.adj[b].discard(a); self.adj[c].add(d); self.adj[d].add(c)
        return True

    def insert(self, a, b):
        """insert a new vertex into face (a, b, nxt[(a,b)])"""
        c = self.nxt[(a, b)]; v = self.n; N = self.nxt
        for e in ((a, b), (b, c), (c, a)): del N[e]
        for (x, y) in ((a, b), (b, c), (c, a)):
            N[(x, y)] = v; N[(y, v)] = x; N[(v, x)] = y
        self.adj.append({a, b, c}); self.adj[a].add(v); self.adj[b].add(v); self.adj[c].add(v); self.n += 1

    def delete3(self, v):
        """delete a degree-3 vertex (relabel the last vertex to v)"""
        if self.deg(v) != 3: return False
        a = next(iter(self.adj[v])); b = self.nxt[(v, a)]; c = self.nxt[(v, b)]
        if min(self.deg(a), self.deg(b), self.deg(c)) - 1 < 3: return False
        N = self.nxt
        for k in [k for k in N if v in k]: del N[k]
        N[(a, b)] = c; N[(b, c)] = a; N[(c, a)] = b
        for x in (a, b, c): self.adj[x].discard(v)
        self.adj[v] = set()
        last = self.n - 1
        if last != v:
            # relabel last -> v
            newN = {}
            for (x, y), z in N.items():
                f = lambda u: v if u == last else u
                newN[(f(x), f(y))] = f(z)
            self.nxt = newN
            self.adj[v] = {x for x in self.adj[last]}
            for x in self.adj[last]: self.adj[x].discard(last); self.adj[x].add(v)
        self.adj.pop(); self.n -= 1
        return True

    def rot(self):
        out = []
        for v in range(self.n):
            s = min(self.adj[v]); r = [s]
            while True:
                y = self.nxt[(v, r[-1])]
                if y == s: break
                r.append(y)
            out.append(r)
        return out

    def line(self, name):
        return f"{name} {self.n} " + ";".join(",".join(map(str, r)) for r in self.rot())


def read_lines(spec):
    path, _, names = spec.partition(':')
    names = set(names.split(',')) if names else None
    out = []
    for l in open(path):
        p = l.split()
        if len(p) >= 3 and (names is None or p[0] in names):
            out.append((p[0], [list(map(int, r.split(','))) for r in p[2].split(';')]))
    return out


def score_lines(lines, cap):
    r = subprocess.run(['nice', '-n', '10', ENG, '-q', '-M', str(cap)], input='\n'.join(lines) + '\n', capture_output=True, text=True)
    res = {}
    for l in r.stdout.split('\n'):
        p = l.split()
        if len(p) == 7: res[p[0]] = (int(p[1]), float(p[6]), int(p[2]), int(p[3]), int(p[4]), int(p[5]))
    return res


FRAME = os.path.abspath(os.path.join(HERE, '../../Census29/bin/frame'))


def frame_filter(cands):
    """keep candidates in the frame class (Census29/bin/frame = TrackB frame.c: min degree 5, no separating triangle,
    occ/app-free); input as planar_code"""
    if not cands: return cands
    buf = bytearray(b'>>planar_code<<')
    for nm, t in cands:
        rot = t.rot(); buf.append(len(rot))
        for r in rot: buf += bytes([x + 1 for x in r] + [0])
    r = subprocess.run([FRAME, 'f'], input=bytes(buf), capture_output=True)
    keep = set()
    for l in r.stdout.decode().split('\n'):
        if l.startswith('f#'): keep.add(int(l.split()[0][2:]) - 1)
    return [c for i, c in enumerate(cands) if i in keep]


def mutate(t, rng, mindeg, nmax):
    t = t.copy(); k = rng.choice((1, 1, 2))
    done = 0; tries = 0
    while done < k and tries < 200:
        tries += 1
        u = rng.random()
        if mindeg <= 3 and u < 0.08 and t.n < nmax:
            a, b = rng.choice(list(t.nxt.keys())); t.insert(a, b); done += 1
        elif mindeg <= 3 and u < 0.14 and t.n > 20:
            d3 = [v for v in range(t.n) if t.deg(v) == 3]
            if d3 and t.delete3(rng.choice(d3)): done += 1
        else:
            a, b = rng.choice(list(t.nxt.keys()))
            if t.flip(a, b, mindeg): done += 1
    if not any(t.deg(v) == 5 for v in range(t.n)): return None
    return t


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('out'); ap.add_argument('--seeds', required=True, action='append')
    ap.add_argument('--mindeg', type=int, default=5); ap.add_argument('--nmax', type=int, default=60)
    ap.add_argument('--minutes', type=float, default=60); ap.add_argument('--batch', type=int, default=12)
    ap.add_argument('--cap', type=int, default=400000); ap.add_argument('--seed', type=int, default=1)
    ap.add_argument('--restart', type=int, default=150, help='rounds without improvement before switching seed')
    ap.add_argument('--pdown', type=float, default=0.03, help='probability of accepting a worse best candidate')
    ap.add_argument('--frame', action='store_true', help='restrict candidates to the frame class (Census29/bin/frame)')
    ap.add_argument('--revert', type=int, default=30, help='return to the local best every this many stale rounds')
    a = ap.parse_args()
    rng = random.Random(a.seed)
    seeds = []
    for s in a.seeds: seeds += read_lines(s)
    logf = open(a.out + '.log', 'a'); hitf = open(a.out + '.hits.txt', 'a')
    t_end = time.time() + 60 * a.minutes
    gbest = (-1, 0); rounds = 0; si = 0; best_logged = {}
    while time.time() < t_end:
        name0, rot0 = seeds[si % len(seeds)]; si += 1
        cur = Tri(rot0)
        sc = score_lines([cur.line('cur')], a.cap).get('cur')
        if sc is None: continue
        cur_s = sc[:2]; best_local = cur_s; best_local_t = cur; stale = 0
        print(f"seed {name0} n={cur.n} score={sc}", file=logf, flush=True)
        while time.time() < t_end and stale < a.restart:
            rounds += 1
            cands = []
            for i in range(a.batch):
                t = mutate(cur, rng, a.mindeg, a.nmax)
                if t is not None: cands.append((f"c{i}", t))
            if a.frame: cands = frame_filter(cands)
            res = score_lines([t.line(nm) for nm, t in cands], a.cap)
            scored = sorted(((res[nm][:2], rng.random(), nm, t) for nm, t in cands if nm in res), reverse=True)
            if not scored: stale += 1; continue
            s_best, _, nm, t = scored[0]
            full = res[nm]
            if s_best >= cur_s or rng.random() < a.pdown:
                cur, cur_s = t, s_best
            if s_best > best_local: best_local = s_best; best_local_t = t; stale = 0
            else:
                stale += 1
                if stale % a.revert == 0: cur, cur_s = best_local_t, best_local   # back to the local best
            if s_best[0] > gbest[0] or (s_best[0] >= 6 and s_best > best_logged.get(name0, (0, 0))):
                best_logged[name0] = s_best
                tag = f"{os.path.basename(a.out)}_r{rounds}_R{s_best[0]}"
                hitf.write(t.line(tag) + '\n'); hitf.flush()
                print(f"HIT round={rounds} seed={name0} n={t.n} R={s_best[0]} W={s_best[1]:.0f} full={full} tag={tag}", file=logf, flush=True)
            if s_best > gbest: gbest = s_best
            if rounds % 25 == 0:
                print(f"round={rounds} seed={name0} n={cur.n} cur={cur_s} local={best_local} global={gbest}", file=logf, flush=True)
    print(f"END rounds={rounds} global={gbest}", file=logf, flush=True)


if __name__ == '__main__':
    main()
