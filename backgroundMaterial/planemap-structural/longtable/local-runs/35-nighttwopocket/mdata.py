#!/usr/bin/env python3
"""[exploratory] NightTwoPocket data: the m-neighbourhood automaton on Job AV's 256 L = 20 degree-6 Gamma-cycles (both runs of each cycle).
Every colouring is put in the table frame of NightA34 §1.1 position by position (the colour map is read off the 11 hole vertices).
Run r in {0, 1}: from position 9 + 10r through ten steps to position 19 + 10r (mod 20); the start is c_9 (r = 0) or c_19 (r = 1), the end is
the other one: in the pulled-back frame start = u_9, end = G u_9. Records per run: deg(m); m's far neighbours with their table-frame colours at every
position; which step components contain them; break flags at start and end; pocket (component of m in G_{0,2} - h - p - x+) and its path to w+."""
import json, sys, os
from collections import Counter, deque
AV = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../27-studio-positive-config/jobav/jobav-cycles.jsonl')
TAB = {  # pos: x0..x4, w0..w4, m
    0: ([3, 0, 1, 0, 2], [2, 3, 2, 3, 1], 0), 1: ([3, 0, 1, 2, 0], [2, 3, 0, 3, 1], 0), 2: ([3, 1, 0, 2, 0], [2, 3, 1, 3, 1], 0),
    3: ([0, 1, 0, 2, 3], [2, 3, 1, 0, 1], 3), 4: ([0, 1, 2, 0, 3], [2, 3, 1, 2, 1], 3), 5: ([1, 0, 2, 0, 3], [2, 3, 1, 2, 0], 3),
    6: ([1, 0, 2, 3, 0], [2, 3, 1, 2, 3], 0), 7: ([1, 2, 0, 3, 0], [0, 3, 1, 2, 3], 2), 8: ([0, 2, 0, 3, 1], [1, 3, 1, 2, 3], 2),
    9: ([0, 2, 3, 0, 1], [1, 0, 1, 2, 3], 2)}
HN = ['p', 'xp', 'x2', 'x3', 'xm', 'z', 'wp', 'w2', 'w3', 'y', 'm']
def tabcol(pos):
    x, w, m = TAB[pos]; return dict(zip(HN, x + w + [m]))
def comp(adj, col, s, pair, avoid=()):
    if col[s] not in pair or s in avoid: return set()
    S = {s}; st = [s]
    while st:
        u = st.pop()
        for t in adj[u]:
            if t not in S and t not in avoid and col[t] in pair: S.add(t); st.append(t)
    return S
def load():
    for l in open(AV):
        r = json.loads(l)
        if r.get('L') == 20 and r.get('source') == 'census': yield r
def frame(r):
    """returns adj (T - h), names, list of 20 table-frame colourings, steps (pos, K)"""
    N = r['names']; V = r['vertices']; hole = [v for v in range(len(r['rotation'])) if v not in V]
    adj = {v: set() for v in V}
    for a, b in r['edges']:
        if a in adj and b in adj: adj[a].add(b); adj[b].add(a)
    cols = []
    for t, cl in enumerate(r['colourings']):
        col = dict(zip(V, cl)); T = tabcol(t % 10); phi = {}
        for k in HN:
            a = col[N[k]]
            if phi.get(a, T[k]) != T[k]: raise ValueError('frame')
            phi[a] = T[k]
        cols.append({v: phi[c] for v, c in col.items()})
    return adj, N, cols
def pocket(adj, N, col):
    pm = (col[N['p']], col[N['m']]); P = comp(adj, col, N['m'], pm, avoid=(N['p'], N['xp'])); return P, N['wp'] in P
def run(adj, N, cols, start):
    """ten steps from position-9 state cols[start]; returns per-step membership of m's far nbrs (by colour change in table frame is not enough:
    the frame changes at the rho step, so membership is computed from the actual step component)"""
    m, z, y, p = N['m'], N['z'], N['y'], N['p']
    far = sorted(adj[m] - {p, y, z})
    traj = []
    for i in range(11):
        c = cols[(start + i) % 20]; traj.append([c[u] for u in far])
    return far, traj
def main():
    out = []; C = Counter()
    for r in load():
        adj, N, cols = frame(r)
        m, z, y, p = N['m'], N['z'], N['y'], N['p']
        far = sorted(adj[m] - {p, y, z})
        if len(far) == 2:
            u1 = next(u for u in far if z in adj[u]); u2 = next(u for u in far if y in adj[u]); far = [u1, u2]
            assert u1 != u2 and u2 in adj[u1]
        steps = r['steps']
        for start in (9, 19):
            other = (start + 10) % 20
            c9, d9 = cols[start], cols[other]
            assert all(c9[N[k]] == d9[N[k]] for k in HN)
            Pc, bc = pocket(adj, N, c9); Pd, bd = pocket(adj, N, d9)
            mem = []
            for i in range(10):
                st = steps[(start + i) % 20]; K = set(st['K'])
                mem.append([u in K for u in far])
            traj = [[cols[(start + i) % 20][u] for u in far] for i in range(11)]
            X9 = {v for v in c9 if c9[v] != d9[v]}
            rec = dict(name=r['name'], hole=r['hole'], ori=r['orientation'], start=start, degm=len(adj[m]), far=far,
                       s9=[c9[u] for u in far], e9=[d9[u] for u in far], brk_start=bc, brk_end=bd, traj=traj, mem=mem,
                       Pc=sorted(Pc), Pd=sorted(Pd), X9=sorted(X9), names=N)
            out.append(rec)
    json.dump(out, open('mdata.json', 'w'))
    return out
if __name__ == '__main__':
    out = main(); C = Counter()
    for x in out:
        if x['degm'] != 5: C[('degm', x['degm'], 'brk start/end', x['brk_start'], x['brk_end'])] += 1; continue
        key = ('deg5', 'brk start' if x['brk_start'] else 'no brk start', 'brk end' if x['brk_end'] else 'no brk end',
               '%s->%s' % (tuple(x['s9']), tuple(x['e9'])))
        C[key] += 1
        mm = ''.join(('1' if a else '.') + ('1' if b else '.') + ' ' for a, b in x['mem'])
        C[('deg5', 'brk start' if x['brk_start'] else ('brk end' if x['brk_end'] else 'none'), 'membership u1u2 per step 9,0..8: ' + mm)] += 1
    for k, v in sorted(C.items(), key=str): print(v, k)
