#!/usr/bin/env python3
"""Track N helpers: drive tn_eng (TrackJ engine + Track N additions) through a persistent pipe.

Per hole the engine prints a Track N line (first), then the TrackJ JSON line. Track N line: {"tn":1, ...}:
  nedge          |E(G - h)|
  run[f], cyc[f] longest pi-run / longest pi-cycle inside the set S_f, f = bits (law, E):
                   f=0: R = {DL, N <= 9}; f=1: R + chain-parity law at every step; f=2: R + Lemma E constants (2,3,3)
                   at every state; f=3: R + law + (2,3,3)
  clsF           [root, class size, class-wide sum of dev, # class states with dev > 0] for the best cycle/run of S_f
  win[f], winL[f] best window of 10 consecutive DL states on a pi-path/cycle: penalty (3 per missing state) and length
  ref            colourings (char per vertex, h='-') of the best window's states for f = reff
  bc[f]          best all-DL pi-cycle by P = sum max(0,N-9) + sum dev + #law failures (with its N profile and class dev)
dev(state) = sum_m |E_m - (nv - 1 - (5 - l_m)/2)| over the 3 perfect matchings m of K4 (general Lemma E form; at an
unfilled state this is |E1-(n-3)| + |E2-(n-4)| + |E3-(n-4)|, n = |V(G)|, i.e. Sigma chi = 2,3,3 iff dev = 0).
Graph lines: 'name n adj0;adj1;...' with h = 0 and adj[0] = link in cyclic order.
"""
import subprocess, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
ENG = os.path.join(HERE, 'tn_eng')


class Engine:
    def __init__(self, hole=0, maxstates=60000, dump=False, reff=3):
        args = [ENG, '--maxstates', str(maxstates), '--hole', str(hole), '--reff', str(reff)] + (['--dump'] if dump else [])
        self.dump = dump
        self.p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True, bufsize=1)

    def run(self, line):
        self.p.stdin.write(line.strip() + '\n'); self.p.stdin.flush()
        tn = json.loads(self.p.stdout.readline())
        if 'err' in tn: return tn, None, None
        js = json.loads(self.p.stdout.readline())
        sts = None
        if self.dump:
            sts = []
            while True:
                l = self.p.stdout.readline()
                if l.startswith('END'): break
                sts.append(l)
        return js, tn, sts

    def close(self):
        self.p.stdin.close(); self.p.wait()


def relabel(rot, h):
    """Return edge set (frozensets) and n with h -> 0 and link (rot[h] order) -> 1..5."""
    n = len(rot); lab = {h: 0}
    for t, x in enumerate(rot[h]): lab[x] = 1 + t
    for v in range(n):
        if v not in lab: lab[v] = len(lab)
    E = set(frozenset((lab[u], lab[v])) for u in range(n) for v in rot[u] if u != h and v != h)
    return n, E


def adjof(E, n):
    adj = [[] for _ in range(n)]; adj[0] = [1, 2, 3, 4, 5]
    for t in range(1, 6): adj[t].append(0)
    for e in sorted(tuple(sorted(e)) for e in E):
        u, v = e; adj[u].append(v); adj[v].append(u)
    return adj


def to_line(name, adj):
    return f"{name} {len(adj)} " + ';'.join(','.join(map(str, a)) for a in adj)


def notri(adj):
    S = [set(a) for a in adj]
    return sum(1 for u in range(1, len(adj)) for v in adj[u] if v > u and not (S[u] & S[v]))


def load_seeds(path):
    out = []
    for l in open(path):
        p = l.split()
        if len(p) < 3: continue
        rot = [list(map(int, r.split(','))) for r in p[2].split(';')]
        h = int(p[3]) if len(p) >= 4 and p[3].isdigit() else (0 if len(rot[0]) == 5 else next((v for v in range(len(rot)) if len(rot[v]) == 5), -1))
        if h < 0: continue
        n, E = relabel(rot, h)
        out.append((p[0] + ('' if h == 0 and len(p) < 4 else f':h{h}'), n, E))
    return out
