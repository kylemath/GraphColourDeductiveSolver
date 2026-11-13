# which pure-world rows are excused only by the tierA k3x_C_A111 C patterns (non-Lean); add them back and re-solve
import sys, os, pickle, json, itertools, collections, re
sys.path.insert(0, '/tmp/swarm-W16/code')
import numpy as np
import w16lib as W, world as WD, torus as TT
ARGV = list(sys.argv); W.init(); ns = W.NS
fn = '/tmp/swarm-W10/pat/loop__studio__opus_check__f2b041__tierA__k3x_C_A111.cfast'
lines = open(fn).read().splitlines(); names = []
for k, l in enumerate(lines):
    if ' r=' in l and not l.startswith(' '):
        for l2 in lines[k + 1:]:
            if ' r=' in l2 and not l2.startswith(' '): break
            if 'C-REDUCIBLE' in l2: names.append(l.split()[0]); break
A111 = collections.defaultdict(set)
for nm in names:
    if re.match(r'^[epf]\d+_', nm): d, P = ns['parse_name'](nm); A111[d].add((nm, P))
print('A111 C patterns:', {d: len(v) for d, v in A111.items()})
world = tuple(int(c) for c in ARGV[1]); degs = [int(x) for x in ARGV[2].split(',')]
# rebuild PATA without A111 (keep a copy)
full = {d: list(v) for d, v in ns['PATL'].items()}
extra = []
for d in degs:
    _drop = {Q for _, Q in A111[d]}; keepP = [P for P in ns["PATL"][d] if frozenset(P) not in _drop]
    A = np.full((len(keepP), 2 * d), 31, dtype=np.uint8)
    for k, P in enumerate(keepP):
        for kd, i, S in P:
            A[k, i if kd == 'w' else d + i] &= sum(1 << (x - 5) for x in S)
    REQ = np.zeros((len(keepP), 2, len(W.CLASSES)), dtype=np.int16)
    for ci, cm in enumerate(W.CLASSES):
        inside = (A & ~np.uint8(cm)) == 0; REQ[:, 0, ci] = inside[:, :d].sum(1); REQ[:, 1, ci] = inside[:, d:].sum(1)
    old = W.PATA[d]; W.PATA[d] = (A, REQ)
    r_wo, st = WD.receivers(set(world), d)
    W.PATA[d] = old
    r_w, st2 = WD.receivers(set(world), d)
    sw = set(r_w); add = [r for r in r_wo if r not in sw]
    for r in add:
        who = [nm for nm, P in A111[d] if ns['_pm1'](d, r[2], r[3], P)]
        print('excused only by A111: %s  by %s' % (W.lab_str(r) if hasattr(W, 'lab_str') else r, who))
    extra += add
labs = pickle.load(open(ARGV[3], 'rb'))
pickle.dump(labs + extra, open(ARGV[4], 'wb')); print('saved', len(labs) + len(extra))
