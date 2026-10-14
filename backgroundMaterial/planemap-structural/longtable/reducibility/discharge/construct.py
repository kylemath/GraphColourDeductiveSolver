"""B8 (exploratory): deliberate constructions of H-failing graphs.
Start from fullerene duals (degrees 5/6; every hole is 66666 with a flat second ring, so H0 holds there) and apply
edge flips that create 5-7 dislocation pairs (flip of an edge uv between two degree-6 vertices: u, v -> 5, the two
apexes -> +1).  Greedy-random search: while some hole is reducible (in the chosen family), flip an edge within
distance 2 of such a hole.  A graph in which no hole is reducible is class-checked (min degree 5, no separating
3-, 4-, nontrivial 5-cycle) and, if in the class, written as a witness.
Usage: construct.py FAMILIES GRAPHFILE OUT.txt [--trials T] [--steps S] [--seed X] [--maxn N]"""
import sys, os, random, argparse
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import ball, h0


def insert_between(L, p, q, x):
    n = len(L)
    for i in range(n):
        if {L[i], L[(i + 1) % n]} == {p, q}:
            L.insert(i + 1, x); return True
    return False


def flip(rot, u, v):
    """flip edge uv; returns new rot or None"""
    R = rot[u]; i = R.index(v); a, b = R[(i + 1) % len(R)], R[(i - 1) % len(R)]
    if a in rot[b] or len(rot[u]) <= 5 or len(rot[v]) <= 5: return None
    new = [list(r) for r in rot]
    new[u].remove(v); new[v].remove(u)
    if not insert_between(new[a], u, v, b) or not insert_between(new[b], u, v, a): return None
    return new


def holes(rot, red):
    out = []
    for v in range(len(rot)):
        if len(rot[v]) != 5: continue
        w, key, st = ball.ball_at(rot, v)
        out.append((v, red(''.join(map(str, ball.wheel_canon(w))), ball.key_str(key) if key else None)))
    return out


def has_diamond_or_2122(rot):
    """RSST 0.7322 (Birkhoff diamond) or 2.122 present: edge ab whose two face-apexes c, d have degree 5 and are
    non-adjacent, with deg a = deg b = 5 (diamond) or {deg a, deg b} = {5, 6} (2.122)."""
    deg = [len(r) for r in rot]
    for a in range(len(rot)):
        R = rot[a]
        for i, b in enumerate(R):
            if b < a: continue
            c, d = R[(i + 1) % len(R)], R[(i - 1) % len(R)]
            if deg[c] == 5 and deg[d] == 5 and d not in rot[c]:
                if (deg[a], deg[b]) == (5, 5) or {deg[a], deg[b]} == {5, 6}: return True
    return False


def near(rot, v, dmax):
    d = {v: 0}; fr = [v]
    for k in range(dmax):
        nf = []
        for x in fr:
            for y in rot[x]:
                if y not in d: d[y] = k + 1; nf.append(y)
        fr = nf
    return d


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('fams'); ap.add_argument('gfile'); ap.add_argument('out')
    ap.add_argument('--trials', type=int, default=20); ap.add_argument('--steps', type=int, default=60)
    ap.add_argument('--seed', type=int, default=1); ap.add_argument('--maxn', type=int, default=80)
    ap.add_argument('--minn', type=int, default=20)
    a = ap.parse_args()
    red = h0.make_pred(set(a.fams.split(',')))
    rng = random.Random(a.seed)
    G = []
    for line in open(a.gfile):
        if not line.strip(): continue
        name, rot = ball.parse_line(line)
        if a.minn <= len(rot) <= a.maxn: G.append((name, rot))
    out = open(a.out, 'a'); found = 0; tried = 0
    for t in range(a.trials):
        name, rot = rng.choice(G); hist = []
        for s in range(a.steps):
            H = holes(rot, red)
            bad = [v for v, r in H if r]
            if not bad and has_diamond_or_2122(rot): bad = [v for v, r in H]   # keep flipping
            if not bad:
                cc = ball.class_check(rot); tried += 1
                if cc['in_class']:
                    found += 1
                    words = sorted(set(ball.key_str(ball.ball_at(rot, v)[1]) for v, _ in H))
                    out.write('%s+%s %d %s #class=%s holes=%d\n' % (name, '.'.join(hist), len(rot),
                              ';'.join(','.join(map(str, r)) for r in rot), cc, len(H)))
                    out.flush()
                    print('WITNESS', name, len(rot), 'flips', len(hist), 'holes', len(H), flush=True)
                break
            v = rng.choice(bad); D = near(rot, v, 2)
            cand = [(x, y) for x in D for y in rot[x] if x < y and y in D and len(rot[x]) == 6 and len(rot[y]) == 6]
            rng.shuffle(cand); done = False
            for x, y in cand:
                nr = flip(rot, x, y)
                if nr is None: continue
                if min(len(r) for r in nr) < 5 or max(len(r) for r in nr) > 9: continue
                rot = nr; hist.append('%d-%d' % (x, y)); done = True; break
            if not done: break
    print('trials', a.trials, 'class-checked', tried, 'witnesses', found)
