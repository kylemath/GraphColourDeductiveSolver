#!/usr/bin/env python3
"""Track R: greedy joint anchored-rule test (tr_rule.py R partA): add cycles one by one to the reference set, keep a
cycle if the shared rule still certifies every cycle in the set (min excess bound > 0).  Anchors: try all type-aligned
anchors of the new cycle.  usage: tr_greedy.py R REF.json@a CAND.json ..."""
import sys, subprocess, re, json
HERE = sys.path[0]
r = sys.argv[1]; S = [sys.argv[2]]
def val(files):
    o = subprocess.run(['nice', '-n', '10', sys.executable, HERE + '/tr_rule.py', r, 'partA'] + files, capture_output=True, text=True).stdout
    m = re.search(r'min excess bound (\S+)', o); return float(m.group(1)) if m else None
for c in sys.argv[3:]:
    dd = json.load(open(c)); L = len(dd['cols']); best = None
    r0 = json.load(open(S[0].split('@')[0]))['Nprof'][int(S[0].split('@')[1])]
    for b in range(L):
        if dd['Nprof'][b] != r0: continue   # type-aligned anchors only (misaligned anchors share no keys)
        v = val(S + ['%s@%d' % (c, b)])
        if v is not None and (best is None or v > best[1]): best = (b, v)
        if v is not None and v > 0.99: break
    ok = best[1] > 0.01
    print('+ %s best anchor %d -> %.4f %s' % (c, best[0], best[1], 'KEEP' if ok else 'drop'), flush=True)
    if ok: S.append('%s@%d' % (c, best[0]))
print('final set', S)
