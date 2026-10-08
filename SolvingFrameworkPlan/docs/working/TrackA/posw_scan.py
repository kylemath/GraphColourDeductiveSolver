#!/usr/bin/env python3
"""Track A task 3 [exploratory]: positive pi-cycles (w > 0) at degree-5 holes of frame-class graphs.
Engine: bin/picyc --full (plantri orientation as given, and --mirror). Per hole: hist [w, L, count] of pi-cycles, clsig [N, F, sum w];
per class slack = -sum w / N. Positive cycles per CLASS are not in picyc output; holes with npos > 0 are re-done in Python (uv_lib.Hole) for the class split.
usage: posw_scan.py OUT.jsonl LIST.txt... [--faces JSON...]   (Pool(4))"""
import sys, os, json, subprocess, tempfile
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from tracka_lib import parse_line, rot_from_faces, rot_line, G
from holes import PICYC
def picyc_raw(rot, name='g', mirror=False, holes=None):
    with tempfile.NamedTemporaryFile('w', suffix='.txt', delete=False) as fh: fh.write(rot_line(name, rot) + '\n'); fn = fh.name
    try:
        cmd = [PICYC, fn, '--full'] + (['--mirror'] if mirror else []) + (['--holes', ','.join(map(str, holes))] if holes else [])
        o = subprocess.run(cmd, capture_output=True, text=True).stdout
    finally: os.unlink(fn)
    return [json.loads(l) for l in o.splitlines() if '"kind": "hole"' in l]
def hole_summary(r):
    pos = [(w, L, c) for w, L, c in r['hist'] if w > 0]
    return dict(hole=r['hole'], linkdeg=r['linkdeg'], states=r['states'], npos=sum(c for *_, c in pos), posw=sum(w * c for w, L, c in pos),
                maxw=r['maxw'], pos=pos, cls=[(c[0], c[1], c[2]) for c in r['clsig']],
                max_cls_sumw=max(c[2] for c in r['clsig']), min_slack=min(-c[2] / c[0] for c in r['clsig']))
def work(item):
    name, rot = item; out = dict(name=name, n=len(rot), frame=G(rot).summary()['frame'], orient={})
    for mir in (False, True):
        out['orient']['m' if mir else 'p'] = [hole_summary(r) for r in picyc_raw(rot, name, mir)]
    return out
if __name__ == '__main__':
    out = sys.argv[1]; args = sys.argv[2:]; items = []
    lists, faces = (args[:args.index('--faces')], args[args.index('--faces') + 1:]) if '--faces' in args else (args, [])
    for fn in lists:
        for l in open(fn):
            if l.strip(): items.append(parse_line(l))
    for fn in faces:
        d = json.load(open(fn))
        for r in (d if isinstance(d, list) else [d]): items.append((r['name'], rot_from_faces([tuple(t) for t in r['faces']])))
    with Pool(4) as P, open(out, 'w') as f:
        for r in P.imap_unordered(work, items): f.write(json.dumps(r) + '\n'); f.flush()
