#!/usr/bin/env python3
"""Track H: pull the smallest violator-free cycle-class graphs from TrackF/out/lpc2/s_*.jsonl.
Writes testbeds.txt in the 'name n rot;rot;...' format used by TrackF/src/lpc_detail.read, plus testbeds.jsonl metadata."""
import json, glob, os
SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'TrackF', 'out', 'lpc2')
want = {(72, 28): 2, (320, 120): 2, (188, 72): 1, (144, 56): 1, (464, 176): 1}
got = {}; meta = []
for p in sorted(glob.glob(os.path.join(SRC, 's_*.jsonl'))):
    for l in open(p):
        try: d = json.loads(l)
        except Exception: continue
        if d.get('ev') != 'cyc': continue
        for c in d['cyc']:
            for cl in c['cyccls']:
                k = (cl[0], cl[1])
                if cl[6] == 0 and k in want and got.get(k, 0) < want[k]:
                    got[k] = got.get(k, 0) + 1
                    name = d['graph'].split()[0]
                    meta.append(dict(key=list(k), surface=d['surface'], name=name, hole=c['hole'], word=c['word'], cls=cl, allDLcyc=c['allDLcyc'], states=c['states'], src=os.path.basename(p), graph=d['graph']))
with open('testbeds.txt', 'w') as f:
    seen = set()
    for m in meta:
        if m['name'] in seen: continue
        seen.add(m['name']); f.write(m['graph'] + '\n')
with open('testbeds.jsonl', 'w') as f:
    for m in meta: f.write(json.dumps({k: v for k, v in m.items() if k != 'graph'}) + '\n')
for m in meta: print(m['key'], m['surface'], m['name'], m['hole'], m['word'], m['cls'], m['allDLcyc'], m['states'], m['src'])
