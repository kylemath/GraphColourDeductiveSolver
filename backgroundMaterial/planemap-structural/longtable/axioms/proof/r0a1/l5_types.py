"""L = 5 type/level reading of non-planar R0 solutions: per cubic vertex word (M0..M4) in letters e (M0 H-edge),
o (M1 H-edge), c (chord); level ivb=0, ii=1, i=2, iii=3, iva=4; chords with their levels; odd cycles of the
chord crossing graph (why the solution is non-planar).  usage: l5_types.py n [nsol]"""
import sys
import networkx as nx
from pysat.solvers import Glucose4
from r0sat import R0Enc
LEV = {'eocoс': 0}
LEV = {'eococ': 0, 'eoeoc': 1, 'eoeco': 2, 'eoceo': 3, 'eocec': 4}
n = int(sys.argv[1]); nsol = int(sys.argv[2]) if len(sys.argv) > 2 else 3
enc = R0Enc(n, 5, 'r0', False, True)
s = Glucose4(bootstrap_with=enc.clauses())
for k in range(nsol):
    if not s.solve(): print('no more'); break
    edges, N = enc.decode(s.get_model())
    chords = [e for e in edges if e[0] == 'c' or e[0].startswith('v')]
    lev = {}
    for x in range(1, n):
        w = ''
        for t in range(5):
            e = next(e for e in N[t] if x in (e[1], e[2]))
            if e[0] == 'c' or e[0].startswith('v'): w += 'c'
            else:
                a = min(e[1], e[2]) if e[0] == 'h' else (0 if e[0] == 'f2' else n - 1)
                w += 'e' if a % 2 == 0 else 'o'
        lev[x] = LEV.get(w, w)
    seq = [lev[x] for x in range(1, n)]
    ch = [((e[1], e[2]) if e[0] == 'c' else (e[0], e[2])) for e in chords]
    chl = [(c, (lev[c[0]], lev[c[1]]) if c[0] != c[0] or isinstance(c[0], int) else ('v', lev[c[1]])) for c in ch]
    print(f'sol {k}: levels along H (vertex 1..{n-1}):', seq)
    print('   chords (level pairs):', chl)
    s.add_clause([-enc.pres[e] for e in chords if enc.pres[e] is not None])
