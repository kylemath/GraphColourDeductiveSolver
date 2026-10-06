#!/usr/bin/env python3
"""studiointel fast/fast.py -- wrapper around the C++ engine kempe.cpp with the same output as ../radius.py analyse()
(including 'witness' {'state','order'} in original labels and 'targetless' when a class is unreached)."""
import os, sys, json, subprocess, tempfile
HERE = os.path.dirname(os.path.abspath(__file__)); BIN = os.environ.get('KEMPE_BIN', os.path.join(HERE, 'kempe'))

def analyse(faces, hole, cap=200000000):
    labels = sorted({x for f in faces for x in f}); m = {u: i for i, u in enumerate(labels)}
    with tempfile.TemporaryDirectory() as d:
        g = os.path.join(d, 'g.txt'); tl = os.path.join(d, 'tl.txt')
        with open(g, 'w') as fh:
            fh.write('%d %d\n' % (len(labels), len(faces)))
            for f in faces: fh.write('%d %d %d\n' % tuple(m[x] for x in f))
        out = subprocess.run([BIN, g, str(m[hole]), str(cap), tl], capture_output=True, text=True, check=True).stdout
        r = json.loads(out)
        if 'inconclusive' in r or 'error' in r: return {'hole': hole, 'inconclusive': r.get('inconclusive', r.get('error'))}
        r['hole'] = hole
        if 'witness' in r:
            order = [labels[i] for i in r['witness']['order']]; r['witness']['order'] = order
        if r['unreached_DL'] and os.path.exists(tl):
            r['targetless'] = [[int(ch) for ch in line.strip()] for line in open(tl)]
    return r
