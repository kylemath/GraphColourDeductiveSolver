#!/usr/bin/env python3
"""Track Q: exact min excess (CP-SAT, compact arborescence model of tq_arb.py) for every law R-cycle of every graph
in the input files, with partitions fixed (= min over ALL graphs carrying that cycle's colouring data + partitions).
Deduplicates by the cycle's colouring data.  usage: tq_batch.py OUT.jsonl SHARD NSHARDS TLIM FILE [FILE ...]"""
import sys, os, json, hashlib, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from tn_lib import Engine
from tn_forest import parse_dump, cycles_in_R_law
from tq_exact import build
from tq_mcf import solve_mcf
import math
LPONLY = os.environ.get('TQ_LPONLY') == '1'
done = set()
for fn in os.listdir(os.path.join(HERE, 'out')):
    if fn.startswith('batch_') and fn.endswith('.jsonl'):
        for x in open(os.path.join(HERE, 'out', fn)): done.add(json.loads(x)['src'])
out = open(sys.argv[1], 'a'); shard, nsh, tlim = int(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4])
ed = Engine(dump=True, maxstates=200000); seen = set(); k = -1
for f in sys.argv[5:]:
    for l in open(f):
        if l.startswith('{'):
            d = json.loads(l)
            if d.get('ev', 'example') != 'example' or 'graph' not in d: continue
            l = d['graph']
        p = l.split()
        if len(p) < 3: continue
        k += 1
        if k % nsh != shard or p[0] in done: continue
        rot = [list(map(int, r.split(','))) for r in p[2].split(';')]
        n = len(rot); E = {frozenset((u, v)) for u in range(1, n) for v in rot[u] if v != 0}
        js, tn, dump = ed.run(l)
        if tn is None: continue
        S = parse_dump(dump)
        for ci, C in enumerate(cycles_in_R_law(S)):
            cols = [[-1 if ch == '-' else int(ch) for ch in S[x]['col']] for x in C]
            U, parts, forced = build(n, E, cols)
            # canonical key: sorted multiset of (partition structure) -- use colourings up to rotation of the cycle
            key = hashlib.md5(json.dumps(sorted(sorted(map(sorted, [P for t, a, b, P in parts if t == s])) for s in range(len(cols)))).encode()).hexdigest()
            if key in seen: continue
            seen.add(key)
            base = 3 * (n - 1) - 8
            dd = dict(n=n, cols=cols, forced=forced)
            rl = solve_mcf(dd, U, parts, None, tlim, True)
            rec = dict(src=p[0], file=os.path.basename(f), cyc=ci, n=n, nedge=len(E), e_in=len(E) - base, L=len(C), Nprof=''.join(str(S[x]['N']) for x in C),
                       U=len(U), lp_e=round(rl['e'], 6) if 'e' in rl else None, lp_secs=rl['secs'])
            if LPONLY and 'e' in rl and rl['e'] > 1e-6:
                rec.update(status='lp_only', e_lb=math.ceil(rl['e'] - 1e-6))
            elif 'e' in rl and math.ceil(rl['e'] - 1e-6) < len(E) - base:
                r = solve_mcf(dd, U, parts, None, tlim, False)
                rec.update(status=r['status'], gap=r['gap'], e=r.get('e'), secs=r['secs'])
                if r.get('e') is not None and r['e'] <= 0: rec['K'] = r['K']
            else:
                rec.update(status=0, e=len(E) - base, note='LP bound = input excess')
            out.write(json.dumps(rec) + '\n'); out.flush()
