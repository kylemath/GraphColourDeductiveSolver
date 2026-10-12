#!/usr/bin/env python3
"""Track H (library part of th_rigidscan.py): how often are unfilled states 'rigid' on closed triangulated surfaces?
Rigid = pair-graph component counts (am, AB, aA, mB, aB, mA) = (1, 1, 2, 1, 2, 1) (the minimum for a DL state obeying D;
both general-graph LPC counterexamples consist only of rigid states).  On the sphere (Euler identity) rigid <=> all six
pair graphs are forests <=> every bicoloured cycle of the dual Tait colouring passes through the hole.
Also counts 'near-rigid' states (sum of counts = 9, one above the minimum 8) and states of Kempe degree <= 2.
usage: th_rigidscan.py GRAPHFILE MAXGRAPHS STRIDE OUT.jsonl   (every degree-5 vertex of every STRIDE-th graph)"""
import sys, json
from th_engine import Hole

def counts(H, col, roles):
    al, mu, A, B = roles; cs = []
    for pr in [(al, mu), (A, B), (al, A), (mu, B), (al, B), (mu, A)]:
        left = {v for v in H.V if col[v] in pr}; k = 0
        while left:
            s = next(iter(left)); left -= H.comp(col, s, pr); k += 1
        cs.append(k)
    return cs

