"""Twin-hole maps: glue a map to its mirror copy along one face triangle, both holes kept.

    python3 tools/twin_map.py BASE [--face far|near|x,y,z] [--key KEY] [--write]

BASE is a key in maps/ (e.g. trap17). The copy's regions get new numbers n, n+1, ... in order (the three glued
regions keep theirs). The result is a triangulation with a separating triangle and two holes, written as
maps/<KEY>.json with "holes": [h, h'] and "twin": {base, face, copy}. Without --write it only checks and prints.

Why a triangle: by the projection lemma (GraphColour longtable/twinhole/README.md) each move of the twin is at most
one move on each side, so the game can get exact distances from the base map's own census table plus a short search
(core.js), and the sequential and simultaneous win rules have the same depth on every start tested.
"""
import os, sys, json, collections, argparse

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)
from mapio import load_map, check_rot  # noqa: E402


def faces(rot):
    pos = [{w: k for k, w in enumerate(r)} for r in rot]
    seen, out = set(), []
    for u in range(len(rot)):
        for v in rot[u]:
            if (u, v) in seen: continue
            f, a, b = [], u, v
            while (a, b) not in seen:
                seen.add((a, b)); f.append(a)
                r = rot[b]; a, b = b, r[(pos[b][a] - 1) % len(r)]
            out.append(tuple(f))
    return out


def pick_face(rot, hole, how):
    n = len(rot); hd = [-1] * n; hd[hole] = 0; q = collections.deque([hole])
    while q:
        u = q.popleft()
        for w in rot[u]:
            if hd[w] < 0: hd[w] = hd[u] + 1; q.append(w)
    fs = [f for f in faces(rot) if len(f) == 3 and hole not in f]
    if how == 'far': return max(fs, key=lambda f: (min(hd[u] for u in f), sum(hd[u] for u in f)))
    if how == 'near': return min(fs, key=lambda f: (sum(hd[u] for u in f), f))
    want = set(int(x) for x in how.split(','))
    f = [f for f in fs if set(f) == want]
    if not f: raise SystemExit('face %s is not a face avoiding the hole' % how)
    return f[0]


def twin(rot, hole, D):
    n = len(rot); Dset = set(D)
    cp = {}; k = n
    for u in range(n):
        if u in Dset: cp[u] = u
        else: cp[u] = k; k += 1
    N = k; R = [None] * N
    for u in range(n):
        if u not in Dset:
            R[u] = list(rot[u])
            R[cp[u]] = [cp[w] for w in reversed(rot[u])]          # the mirror image
    for x in D:
        r = list(rot[x]); y, z = [w for w in D if w != x]
        i = r.index(y)
        if r[(i + 1) % len(r)] != z: y, z = z, y; i = r.index(y)
        r = r[i:] + r[:i]                                      # r = [y, z, a1, ..., ak]; the face x,y,z sits between y and z
        assert r[1] == z
        a = r[2:]
        R[x] = [y] + [cp[w] for w in reversed(a)] + [z] + a  # the copy's side goes into that gap
    return R, cp


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('base'); ap.add_argument('--face', default='far'); ap.add_argument('--key'); ap.add_argument('--write', action='store_true')
    a = ap.parse_args()
    spec = json.load(open(os.path.join(HERE, 'maps', a.base + '.json')))
    rot, tri = load_map(spec); hole = spec['hole']
    assert tri, 'the base map must be a triangulation'
    D = pick_face(rot, hole, a.face)
    R, cp = twin(rot, hole, D)
    ok = check_rot(R) and all(len(f) == 3 for f in faces(R))
    n2 = len(R); E = sum(len(r) for r in R) // 2
    print('%s: n=%d -> twin n=%d, E=%d, faces=%d, glued face %s, holes %d and %d, sphere+triangles: %s'
          % (a.base, len(rot), n2, E, len(faces(R)), list(D), hole, cp[hole], ok))
    if not ok: raise SystemExit('gluing failed')
    key = a.key or a.base + '-tw'
    out = {'name': '%s twin' % spec.get('name', a.base),
           'source': 'tools/twin_map.py %s --face %s: %s glued to its mirror copy along face %s; both holes kept. %s'
                     % (a.base, a.face, a.base, list(D), spec.get('source', '')),
           'holes': [hole, cp[hole]], 'hole': hole, 'world': False,
           'twin': {'base': a.base, 'face': list(D), 'copy': [cp[u] for u in range(len(rot))]},
           'rot': R}
    if a.write:
        path = os.path.join(HERE, 'maps', key + '.json')
        with open(path, 'w') as f:
            f.write('{\n' + ',\n'.join('  %s: %s' % (json.dumps(k), json.dumps(v)) for k, v in out.items()) + '\n}\n')
        print('wrote', path)


if __name__ == '__main__':
    main()
