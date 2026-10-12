#!/usr/bin/env python3
"""[Track B] Adversarial search: find frame-class triangulations in which NO degree-5 vertex has a word in a given set S.
State: a triangulation (rotation system), fixed order n. Moves: edge flips.
Hard constraints after every move: min degree >= 5, NoSep (no separating triangle).
Soft (penalised): number of clean-tip appearances of the diamond / 2.122 (on NoSep triangulations this is equivalent to
Occ in either orientation: Lean appearFree_of_free + Occ => clean appearance; and frame.c re-checks with the Lean Occ
schedule), plus the number of degree-5 vertices whose capped word lies in S.
Every reported witness is re-verified by ./frame (Lean Occ matcher) before use.
Usage: python3 avoid.py --seed-file F --cap 8 --S "55666,..." --steps N --rng K --out FILE"""
import sys, random, argparse, math
from words import canon, fmt

class Tri:
    def __init__(self, rot):
        self.rot = [list(r) for r in rot]; self.n = len(rot)
        self.nb = [set(r) for r in rot]
    def deg(self, v): return len(self.rot[v])
    def nxt(self, x, y): r = self.rot[x]; return r[(r.index(y) + 1) % len(r)]
    def prv(self, x, y): r = self.rot[x]; return r[(r.index(y) - 1) % len(r)]
    def can_flip(self, a, b):
        c, d = self.nxt(a, b), self.prv(a, b)
        if c == d or d in self.nb[c]: return None
        if self.deg(a) <= 5 or self.deg(b) <= 5: return None
        # new edge cd: separating triangle iff c,d have a common neighbour other than a,b
        if (self.nb[c] & self.nb[d]) - {a, b}: return None
        return c, d
    def flip(self, a, b, c, d):
        self.rot[a].remove(b); self.rot[b].remove(a); self.nb[a].discard(b); self.nb[b].discard(a)
        for (x, y, z, w) in ((c, a, b, d), (d, a, b, c)):
            r = self.rot[x]; i, j = r.index(y), r.index(z)
            if (i + 1) % len(r) == j: r.insert(j if j > 0 else len(r), w)
            else: r.insert(i if i > 0 else len(r), w)  # j+1 == i
            self.nb[x].add(w)
    def bad_appear(self, near=None):
        """number of clean-tip appearances (diamond ![5,5,5,5], 2.122 ![6,5,5,5]) with int0 in `near`"""
        cnt = 0; V = range(self.n) if near is None else near
        for c0 in V:
            if self.deg(c0) not in (5, 6): continue
            for c2 in self.rot[c0]:
                if self.deg(c2) != 5: continue
                cm = [t for t in self.rot[c0] if t != c2 and t in self.nb[c2] and self.deg(t) == 5]
                for t1 in cm:
                    for t3 in cm:
                        if t1 == t3 or t3 in self.nb[t1]: continue
                        if not ((self.nb[t1] & self.nb[t3]) - {c0, c2}): cnt += 1
        return cnt
    def word(self, v, cap): return canon([min(self.deg(u), cap) for u in self.rot[v]])

def score(T, S, cap, W):
    bad = sum(1 for v in range(T.n) if T.deg(v) == 5 and T.word(v, cap) in S)
    return W * T.bad_appear() + bad, bad

def search(rot, S, cap, steps, rng, W=3, temp0=1.5):
    T = Tri(rot); cur, _ = score(T, S, cap, W); best = cur
    for it in range(steps):
        temp = temp0 * (1 - it / steps) + 0.05
        a = rng.randrange(T.n); b = rng.choice(T.rot[a])
        cd = T.can_flip(a, b)
        if not cd: continue
        c, d = cd; T.flip(a, b, c, d)
        new, bad = score(T, S, cap, W)
        if new <= cur or rng.random() < math.exp((cur - new) / temp):
            cur = new
            if cur == 0: return T
        else:
            T.flip(c, d, *reversed_flip(T, c, d, a, b))
    return None

def reversed_flip(T, c, d, a, b):
    # undo: flipping edge cd gives back ab; need (a, b) in the orientation expected by flip(c, d, x, y)
    x, y = T.nxt(c, d), T.prv(c, d)
    return x, y

def load_line(line):
    p = line.split(); return p[0], [list(map(int, r.split(','))) for r in p[2].split(';')]

def dump(T, name):
    return '%s %d %s' % (name, T.n, ';'.join(','.join(map(str, r)) for r in T.rot))

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--seed-file'); ap.add_argument('--cap', type=int, default=8); ap.add_argument('--S')
    ap.add_argument('--steps', type=int, default=20000); ap.add_argument('--rng', type=int, default=1)
    ap.add_argument('--tries', type=int, default=5); ap.add_argument('--out')
    a = ap.parse_args(); rng = random.Random(a.rng)
    def parse_word(s):
        out = []; i = 0
        while i < len(s):
            if s[i:i + 2] == str(a.cap) + '+' or (i + 1 < len(s) and s[i + 1] == '+'): out.append(a.cap); i += 2
            else: out.append(int(s[i])); i += 1
        return canon(out)
    S = {parse_word(w) for w in a.S.split(',') if w}
    seeds = [load_line(l) for l in open(a.seed_file) if l.strip()]
    found = 0
    with open(a.out, 'a') as fo:
        for t in range(a.tries):
            name, rot = rng.choice(seeds)
            T = search(rot, S, a.cap, a.steps, rng)
            if T is not None:
                found += 1; fo.write(dump(T, 'avoid-r%d-t%d-from-%s' % (a.rng, t, name)) + '\n'); fo.flush()
    print('found', found, 'of', a.tries)
