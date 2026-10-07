#!/usr/bin/env python3
"""[Track B] Rigorous lower bound on |S| from data: maximum number of known frame-class graphs whose capped word sets are
pairwise disjoint (any unavoidable S needs one word per such graph). Exact MILP; also lists the monotype words
(words w such that some graph has all degree-5 vertices of word w: then w must be in every unavoidable S).
Usage: python3 packing.py CAP files..."""
import sys, numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from words import load, graph_words, fmt
cap = int(sys.argv[1]); G = load(sys.argv[2:])
sets = {}
for nm, n, rot in G: sets.setdefault(frozenset(graph_words(rot, cap)), nm)
X = list(sets); U = sorted(set().union(*X)); A = np.zeros((len(U), len(X)))
for j, s in enumerate(X):
    for w in s: A[U.index(w), j] = 1
res = milp(c=-np.ones(len(X)), constraints=LinearConstraint(A, -np.inf, 1), integrality=np.ones(len(X)), bounds=Bounds(0, 1))
pick = [X[j] for j in range(len(X)) if res.x[j] > 0.5]
print('distinct word-sets', len(X), '| max disjoint packing =', len(pick))
for s in pick: print('  ', sets[s], sorted(fmt(w, cap) for w in s))
print('monotype words:', sorted({fmt(next(iter(s)), cap) for s in X if len(s) == 1}))
