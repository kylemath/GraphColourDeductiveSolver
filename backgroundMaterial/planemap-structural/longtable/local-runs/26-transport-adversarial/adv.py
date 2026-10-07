#!/usr/bin/env python3
"""adv.py JSON HOLE SEED TRIALS [out.jsonl]: large adversarial graph (C6 face-list json); classes from random colourings (like run-22 sweeps)."""
import sys, json, itertools, random, time
from lib26 import *
P, H, seed, T = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
out = open(sys.argv[5], 'a') if len(sys.argv) > 5 else sys.stdout
faces = json.load(open(P))['faces']; adj = {}
for t in faces:
    for a, b in itertools.combinations(t, 2): adj.setdefault(a, set()).add(b); adj.setdefault(b, set()).add(a)
nxt = {}
for t in faces:
    if H in t:
        i = t.index(H); nxt[t[(i + 1) % 3]] = t[(i + 2) % 3]
start = min(nxt); link = [start]
while nxt[link[-1]] != start: link.append(nxt[link[-1]])
assert len(link) == 5
E = Eng(adj, H, link); rng = random.Random(seed); done = set(); t0 = time.time()
name = P.split('/')[-1].replace('.json', '')
for trial in range(T):
    s = E.randcol(rng)
    if s in done: continue
    mem = E.bfs(s); done |= set(mem)
    r = analyse_class(E, mem, dict(graph=name, hole=H, seed=seed))
    if r:
        r['sec'] = round(time.time() - t0); out.write(json.dumps(r) + '\n'); out.flush()
