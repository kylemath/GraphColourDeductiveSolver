"""Shared helpers for the fable experiments. Run from a folder holding
synth_rules_588.txt, real58.npz, real911.npz and the families code (parts.py, mir.py, behav.py)."""
import sys, os, random, collections as C
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE)); sys.path.insert(0, os.getcwd())
from parts import parse
import behav
FULL = (5, 9)
RULES = os.environ.get('RULES', 'synth_rules_588.txt')

def load():
    sc, P = parse(RULES)
    return P

def norm_slot(s):
    """(sp, hat, fans) with fans always explicit when the spoke is exact 6..8, else ()."""
    sp, hat, fans = (s[0], s[1]), (s[2], s[3]), tuple(s[4])
    if sp[0] == sp[1] and 6 <= sp[0] <= 8:
        k = sp[0] - 5
        if len(fans) == 0: fans = (FULL,) * k
        assert len(fans) == k, s
    else:
        assert all(f == FULL for f in fans), s
        fans = ()
    return (sp, hat, fans)

def norm(p):
    return (p['hub'], tuple(norm_slot(s) for s in p['slots']))

def nulls(P, seeds=(1, 2, 3)):
    return [behav.null_parts(P, s) for s in seeds]
