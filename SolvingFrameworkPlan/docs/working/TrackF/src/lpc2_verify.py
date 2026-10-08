#!/usr/bin/env python3
"""Track F section 9: verify (graph, hole) items with three engines.
  kclass3 (kclass_pi.cpp, unchanged engine of section 8): class list cls[7], allDLcyc, cycClasses[onCycles,pathEnds,filled]
  kclass4 (kclass_pi2.cpp): cls2[9] (cls + onCycles + piPathEnds)
  lpc_detail.analyse (pure Python, no shared code): cls, cls2, allDLcyc, cycClasses[onCycles,filled]
  kclass_py.py (pure Python, enumerates all colourings, no normal form trick): class-size histogram (only if states <= PYMAX)
Checks: kclass3 cls == Python cls; kclass4 cls2 == Python cls2; kclass4 cls2[:7] == kclass3 cls; allDLcyc equal in all three;
kclass3 cycClasses == kclass4 cycle classes [onCycles, pathEnds, filled]; kclass_py size histogram == class sizes.
input: ITEMS.jsonl lines {"graph": "<name n rot>", "hole": h, ...}; output: one JSON line per item with ok flags + the cls2 list.
usage: lpc2_verify.py ITEMS.jsonl OUT.jsonl [PYMAX=300000] [KCPYMAX=60000]"""
import sys, os, json, subprocess, tempfile
from collections import Counter
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, D)
import lpc_detail
K = 'cls[size,filled,DL,unfilledNonDL,minKdeg,maxKdeg,lockParityViolations]'
K2 = 'cls2[size,filled,DL,unfilledNonDL,minKdeg,maxKdeg,lockParityViolations,onCycles,piPathEnds]'
CC = 'cycClasses[onCycles,pathEnds,filled]'

def kc(binary, line, h):
    with tempfile.NamedTemporaryFile('w', suffix='.txt', delete=False) as f: f.write(line + '\n'); p = f.name
    out = subprocess.run([os.path.join(D, binary), p, f'{h},'], capture_output=True, text=True).stdout; os.unlink(p)
    return json.loads(out.strip().splitlines()[0])

def verify(line, h, pymax, kcpymax):
    name = line.split()[0]; rot = [list(map(int, r.split(','))) for r in line.split()[2].split(';')]
    a = kc('kclass3', line, h); b = kc('kclass4', line, h)
    r = dict(graph=name, hole=h, states=a['states'], allDLcyc=a['allDLcyc'], cls2=sorted(b[K2]))
    ok = dict(k3_k4=sorted(a[K]) == sorted(c[:7] for c in b[K2]) and a['allDLcyc'] == b['allDLcyc'] and
              sorted(a[CC]) == sorted([c[7], c[8], c[1]] for c in b[K2] if c[7]),
              pid=a['pid_bad'] == [0, 0, 0])
    if a['states'] <= pymax:
        res, _ = lpc_detail.analyse(rot, h, False)
        ok['py_cls'] = res['cls'] == sorted(a[K]); ok['py_cls2'] = res['cls2'] == sorted(b[K2])
        ok['py_cyc'] = res['allDLcyc'] == sorted(a['allDLcyc']); ok['py_pid'] = res['pid_bad'] == [0, 0, 0]
    if a['states'] <= kcpymax:
        with tempfile.NamedTemporaryFile('w', suffix='.txt', delete=False) as f: f.write(line + '\n'); p = f.name
        o = subprocess.run([sys.executable, os.path.join(D, 'kclass_py.py'), p, name, str(h)], capture_output=True, text=True).stdout; os.unlink(p)
        hist = o.split('size histogram')[1].strip()
        ok['kclass_py_hist'] = hist == str(sorted(Counter(c[0] for c in a[K]).items()))
    r['ok'] = ok; r['all_ok'] = all(ok.values()); return r

if __name__ == '__main__':
    pymax = int(sys.argv[3]) if len(sys.argv) > 3 else 300000; kcpymax = int(sys.argv[4]) if len(sys.argv) > 4 else 60000
    done = set()
    if os.path.exists(sys.argv[2]):
        for l in open(sys.argv[2]): d = json.loads(l); done.add((d['graph'], d['hole']))
    out = open(sys.argv[2], 'a')
    for l in open(sys.argv[1]):
        it = json.loads(l); key = (it['graph'].split()[0], it['hole'])
        if key in done: continue
        done.add(key); r = verify(it['graph'], it['hole'], pymax, kcpymax)
        for k in it:
            if k not in ('graph', 'hole') and k not in r: r[k] = it[k]
        out.write(json.dumps(r) + '\n'); out.flush(); print(r['graph'], r['hole'], r['states'], r['ok'], flush=True)
