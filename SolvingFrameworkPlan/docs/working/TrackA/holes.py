#!/usr/bin/env python3
"""Track A hole evaluators [exploratory].
Engine 1: picyc --full (C++, bin/picyc built from 27-studio-positive-config/picyc.cpp): per degree-5 hole the Kempe classes
          of T - v (states = proper 4-colourings up to renaming; moves = whole-component Kempe swaps), clsig = [size, F, ...].
Engine 2: kempe_py.Space (independent stdlib Python, local-runs/common/kempe_py.py): build_graph + classes + filled.
PureClean(v) <=> every class has F > 0.  minfrac(v) = min over classes of F/size."""
import os, sys, json, subprocess, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
PICYC = os.path.join(HERE, 'bin/picyc')
sys.path.insert(0, '/Users/kylemathewson/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/local-runs/common')
from tracka_lib import rot_line

def picyc_holes(rot, name='g', holes=None, timeout=None):
    """{hole: [(size, F), ...]} for every degree-5 hole (engine 1)."""
    with tempfile.NamedTemporaryFile('w', suffix='.txt', delete=False, dir=os.environ.get('TMPDIR')) as fh:
        fh.write(rot_line(name, rot) + '\n'); fn = fh.name
    try:
        cmd = [PICYC, fn, '--full'] + (['--holes', ','.join(map(str, holes))] if holes else [])
        o = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout).stdout
    finally: os.unlink(fn)
    out = {}
    for l in o.splitlines():
        r = json.loads(l)
        if r.get('kind') == 'hole':
            assert not r.get('cls_bad') and r.get('states', 0) > 0, r.get('hole')
            out[r['hole']] = [(c[0], c[1]) for c in r['clsig']]
            assert sum(c[0] for c in out[r['hole']]) == r['states']
    return out

def py_holes(rot, holes=None):
    """engine 2 (independent)."""
    from kempe_py import Space
    adj = {v: set(r) for v, r in enumerate(rot)}; out = {}
    for h in (holes if holes is not None else [v for v in range(len(rot)) if len(rot[v]) == 5]):
        sp = Space(adj, h, link=rot[h]); sp.build_graph(); cl, n = sp.classes()
        size = [0] * n; F = [0] * n
        for k in range(len(sp.states)):
            size[cl[k]] += 1; F[cl[k]] += sp.filled(k)
        out[h] = sorted(zip(size, F))
    return out

def score(H):
    """H = {hole: classes}. Returns dict: deg5, npc (# PureClean deg-5 vertices), per-hole minfrac, margin = max_v minfrac, worst = min_v minfrac."""
    mf = {h: min(F / s for s, F in c) for h, c in H.items()}
    pc = [h for h, c in H.items() if all(F > 0 for s, F in c)]
    return dict(deg5=len(H), npc=len(pc), nonpc=sorted(set(H) - set(pc)), minfrac=mf,
                margin=max(mf.values()) if mf else None, worst=min(mf.values()) if mf else None,
                ncls={h: len(c) for h, c in H.items()})
