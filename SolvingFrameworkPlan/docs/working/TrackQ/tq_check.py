#!/usr/bin/env python3
"""Track Q: build G' from a solver edge set K (+ hole 0 joined to link 1..5) and check it with engine 1 (tn_eng: law
R-cycle present, cyc[f]) ; write the graph line.  Engine 2 = tn_verify.py on the written file (run separately).
usage: tq_check.py DATA.json SOLVERLOG OUT.txt NAME"""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from tn_lib import Engine, adjof, to_line
from tn_forest import parse_dump, cycles_in_R_law
d = json.load(open(sys.argv[1])); K = None
for l in open(sys.argv[2]):
    if l.startswith('K '): K = [tuple(e) for e in json.loads(l[2:])]
n = d['n']; adj = adjof({frozenset(e) for e in K}, n); line = to_line(sys.argv[4], adj)
ed = Engine(dump=True, maxstates=400000); js, tn, dump = ed.run(line); S = parse_dump(dump); cyc = cycles_in_R_law(S)
cols0 = [''.join('-' if c < 0 else str(c) for c in col) for col in d['cols']]
same = [sorted(cols0) == sorted(S[x]['col'] for x in C) for C in cyc]
print(json.dumps(dict(name=sys.argv[4], n=n, nedge=len(K), e=len(K) - (3 * (n - 1) - 8), cyc=tn['cyc'], run=tn['run'], nlawcycles=len(cyc),
                      Nprofs=[''.join(str(S[x]['N']) for x in C) for C in cyc], same_colourings_as_source=same, states=js.get('states'), filled=js.get('filled'))))
open(sys.argv[3], 'a').write(line + '\n')
