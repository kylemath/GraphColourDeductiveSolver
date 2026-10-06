#!/usr/bin/env python3
"""path3-local/lib.py -- [exploratory] Local intel (MacBook stand-in for Studio intel), 6 Oct 2026.
Shared helpers: load seed graphs (several JSON formats), run the engine kempe_classes3 (compiled here from ../fast/kempe_classes3.cpp),
convert faces to the rotation-system JSON that Math's independent checker (path3_kclasses.py) reads."""
import os, sys, json, subprocess, tempfile, hashlib
from collections import defaultdict
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
sys.path.insert(0, os.path.join(HERE, '..'))
import graphs  # noqa: E402  (studiointel/graphs.py: adjacency, flip, degrees, n_separating_triangles, check_triangulation)
BIN = os.path.join(HERE, 'kempe_classes3')
MATH = os.path.join(REPO, 'SolvingFrameworkPlan', 'docs', 'working', 'MathPath3-scripts')


def load_faces(path):
    """faces (ccw, every directed edge once) from: {'faces'}, builder .tri, HoG/heawood JSON, builder NAME.json ('faces_oriented')."""
    if path.endswith('.tri'):
        L = open(path).read().split('\n')
        n, F = map(int, L[0].split())
        return [tuple(map(int, L[1 + i].split())) for i in range(F)]
    d = json.load(open(path))
    F = d.get('faces_oriented') or d['faces']
    return [tuple(f) for f in F]


def ghash(F):
    return hashlib.sha256(json.dumps(sorted(map(list, F))).encode()).hexdigest()


def kclasses(F, h, cap=300000000, lmin=40):
    labels = sorted({x for f in F for x in f}); m = {u: i for i, u in enumerate(labels)}
    with tempfile.NamedTemporaryFile('w', suffix='.txt', delete=False) as fh:
        fh.write('%d %d\n' % (len(labels), len(F)))
        for f in F: fh.write('%d %d %d\n' % tuple(m[x] for x in f))
    out = subprocess.run([BIN, fh.name, str(m[h]), str(cap), str(lmin)], capture_output=True, text=True).stdout
    os.unlink(fh.name)
    r = json.loads(out)
    if 'min_class' in r:  # translate the BFS order back to original labels
        r['min_class']['order'] = [labels[i] for i in r['min_class']['order']]
    return r


def rotation(F):
    """ccw rotation at each vertex (labels must be 0..n-1) from oriented faces."""
    n = 1 + max(x for f in F for x in f)
    nxt = defaultdict(dict)
    for (a, b, c) in F:
        nxt[a][b] = c; nxt[b][c] = a; nxt[c][a] = b
    rot = []
    for x in range(n):
        s = min(nxt[x]); r = [s]
        while nxt[x][r[-1]] != s: r.append(nxt[x][r[-1]])
        assert len(r) == len(nxt[x]), 'link of %d not a cycle' % x
        rot.append(r)
    return rot


def checker_json(F, name):
    """minimal NAME.json accepted by path3_kclasses.py (it reads 'name', 'n', 'rotation', 'deg5_orbit_reps')."""
    rot = rotation(F)
    return {'name': name, 'n': len(rot), 'rotation': rot, 'faces_oriented': [list(f) for f in F],
            'deg5_orbit_reps': [{'v': x} for x in range(len(rot)) if len(rot[x]) == 5]}


def core_ok(F, maxdeg=99):
    ok, msg = graphs.check_triangulation(F)
    if not ok: return False, msg
    dg = graphs.degrees(F)
    if min(dg.values()) < 5: return False, 'min degree %d' % min(dg.values())
    if max(dg.values()) > maxdeg: return False, 'max degree %d' % max(dg.values())
    s = graphs.n_separating_triangles(F)
    if s: return False, '%d separating triangles' % s
    return True, 'ok'
