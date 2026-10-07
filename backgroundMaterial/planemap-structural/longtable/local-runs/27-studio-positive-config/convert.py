#!/usr/bin/env python3
"""[exploratory] convert graph lists to picyc input lines: "name n r0;r1;...", r_v = comma-separated 0-based neighbours in rotation
order as given by the source (planar code / plantri orientation). Modes:
  gentri FILE          studiointel/gentri/triN.txt (names triN#index, 1-based index as in runs 22-26)
  plantri FILE         plantri -a ascii output (names pN#index, 1-based, file order)
  pc FILE              planar_code binary (names FILE#index, 0-based, file order, as ipr_run.py)
  faces FILE.json ...  {'faces': [[a,b,c],...]} (oriented faces); the rotation is derived from the faces and REVERSED, so that a file
                       produced by ipr_run.read_pc (which reverses planar code) gets back the planar-code orientation."""
import sys, json, os
def emit(name, rot): print('%s %d %s' % (name, len(rot), ';'.join(','.join(map(str, r)) for r in rot)))
mode = sys.argv[1]
if mode == 'gentri':
    for f in sys.argv[2:]:
        base = os.path.basename(f).replace('.txt', '')
        for gi, line in enumerate((l for l in open(f) if l.startswith('G')), 1):
            parts = line.split(); n = int(parts[1]); h = parts[2]; bs = [int(h[i:i + 2], 16) for i in range(0, len(h), 2)]
            rot, cur = [], []
            for b in bs:
                if b == 0: rot.append(cur); cur = []
                else: cur.append(b - 1)
            assert len(rot) == n; emit('%s#%d' % (base, gi), rot)
elif mode == 'plantri':
    for f in sys.argv[2:]:
        base = os.path.basename(f).replace('.txt', '')
        for gi, line in enumerate((l for l in open(f) if l.strip()), 1):
            n, lists = line.split(); rot = [[ord(ch) - 97 for ch in w] for w in lists.split(',')]
            assert len(rot) == int(n); emit('%s#%d' % (base, gi), rot)
elif mode == 'pc':
    for f in sys.argv[2:]:
        base = os.path.basename(f); data = open(f, 'rb').read(); assert data[:15] == b'>>planar_code<<'; i = 15; gi = 0
        while i < len(data):
            n = data[i]; i += 1; rot = []
            for v in range(n):
                nb = []
                while data[i] != 0: nb.append(data[i] - 1); i += 1
                i += 1; rot.append(nb)
            emit('%s#%d' % (base, gi), rot); gi += 1
elif mode == 'faces':
    for f in sys.argv[2:]:
        F = json.load(open(f))['faces']; labels = sorted({x for t in F for x in t}); m = {u: i for i, u in enumerate(labels)}
        nxt = {}
        for t in F:
            for i in range(3): nxt.setdefault(m[t[i]], {})[m[t[(i + 1) % 3]]] = m[t[(i + 2) % 3]]
        rot = []
        for v in range(len(labels)):
            s = min(nxt[v]); r = [s]
            while nxt[v][r[-1]] != s: r.append(nxt[v][r[-1]])
            assert len(r) == len(nxt[v]); rot.append(r[::-1])
        emit(os.path.basename(f).replace('.json', ''), rot)
