#!/usr/bin/env python3
"""[Track B] Hitting-set / adversary loop (single process).
Round k: S_k = exact minimum hitting set of the word sets of all known frame-class graphs (census + IPR + bigsample +
witnesses found so far). Then avoid.search looks for a frame-class triangulation with no degree-5 word in S_k; every
witness is re-verified by ./frame (Lean Occ matcher, NoSep, min degree) before it is added. Stops when a round finds no
witness within its budget, or after --rounds rounds.  Log: out/iterate-cap<CAP>.log, witnesses: out/witness-cap<CAP>.txt
Usage: python3 iterate.py --cap 8 --rounds 40 --steps 20000 --tries 12"""
import argparse, random, subprocess, sys, time
from words import load, graph_words, hitting, fmt
import avoid

ap = argparse.ArgumentParser()
ap.add_argument('--cap', type=int, default=8); ap.add_argument('--rounds', type=int, default=40)
ap.add_argument('--steps', type=int, default=20000); ap.add_argument('--tries', type=int, default=12)
ap.add_argument('--rng', type=int, default=7); ap.add_argument('--base', nargs='+',
    default=['out/census-frame-22-28.txt', 'out/frame-ext-ipr.txt', 'out/frame-ext-bigsample.txt'])
a = ap.parse_args(); cap = a.cap; rng = random.Random(a.rng)
wfile = 'out/witness-cap%d.txt' % cap; log = open('out/iterate-cap%d.log' % cap, 'a')
def P(*x):
    s = ' '.join(map(str, x)); print(s); log.write(s + '\n'); log.flush()
G = load(a.base)
try: G += load([wfile])
except FileNotFoundError: pass
seeds = [(nm, rot) for nm, n, rot in G]
P('start', time.ctime(), 'graphs', len(G))
for rd in range(a.rounds):
    sets = [frozenset(graph_words(rot, cap)) for _, _, rot in G]
    U = set().union(*sets)
    _, S = hitting(sets, U)
    P('round', rd, '|S| =', len(S), 'S =', ','.join(fmt(w, cap) for w in sorted(S)), '| universe seen', len(U))
    found = None
    for t in range(a.tries):
        nm, rot = rng.choice(seeds)
        T = avoid.search(rot, set(S), cap, a.steps, rng)
        if T is None: continue
        line = avoid.dump(T, 'w-cap%d-r%d-t%d' % (cap, rd, t))
        out = subprocess.run(['./frame'], input=line + '\n', capture_output=True, text=True).stdout
        if not out.strip(): P('  witness rejected by frame.c (not frame class)'); continue
        ws = graph_words(T.rot, cap)
        assert not (set(ws) & set(S))
        found = line; break
    if not found:
        P('round', rd, 'no witness in', a.tries, 'tries x', a.steps, 'steps'); break
    open(wfile, 'a').write(found + '\n')
    nm, n, rot = load_line = (found.split()[0], int(found.split()[1]), [list(map(int, r.split(','))) for r in found.split()[2].split(';')])
    G.append((nm, n, rot)); seeds.append((nm, rot))
    P('  witness n=%d words=%s' % (n, ','.join(sorted(fmt(w, cap) for w in set(graph_words(rot, cap))))))
P('end', time.ctime())
