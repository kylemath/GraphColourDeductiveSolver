#!/usr/bin/env python3
"""TrackO: convert face-list JSON graphs (jobbv/*.json, {"faces": [...]}) into rotation lines 'name n adj0;adj1;...'.
usage: to_conv.py FILE.json [FILE.json ...] > out.txt
"""
import sys, json, os


def rot_from_faces(F):
    nxt = {}
    for f in F:
        for i in range(3):
            nxt[(f[i], f[(i + 1) % 3])] = f[(i + 2) % 3]
    n = 1 + max(max(f) for f in F)
    rot = []
    for v in range(n):
        start = min(b for (a, b) in nxt if a == v)
        r = [start]
        while True:
            y = nxt[(v, r[-1])]
            if y == start:
                break
            r.append(y)
        rot.append(r)
    return rot


def line(name, rot):
    return f"{name} {len(rot)} " + ";".join(",".join(map(str, r)) for r in rot)


if __name__ == '__main__':
    for p in sys.argv[1:]:
        d = json.load(open(p))
        F = d['faces'] if isinstance(d['faces'], list) else json.loads(d['faces'])
        print(line(os.path.basename(p).replace('.json', ''), rot_from_faces(F)))
