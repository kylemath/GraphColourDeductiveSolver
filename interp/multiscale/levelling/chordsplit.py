# For clusters with chords that failed re-levelling: cut along every chord into chordless pieces and test each piece.
import pickle, glob, json
from lev import *
from e1_survey import graph
def pieces(T, S):
    cl = disc_or_none(T, S)
    if cl is None: return [('nodisc', S)]
    ch = chords(cl)
    if not ch: return [cl]
    x, y = ch[0]; pos = {v: i for i, v in enumerate(cl.walk)}
    i, j = sorted((pos[x], pos[y])); arc = set(cl.walk[i+1:j])
    rest = S - {x, y}
    comps = []; seen = set()
    for v in rest:
        if v in seen: continue
        c = bfs_set(T.adj, v, rest); seen |= c; comps.append(c)
    s1 = set().union(*[c for c in comps if c & arc]) | {x, y}
    s2 = (S - s1) | {x, y}
    return pieces(T, s1) + pieces(T, s2)
out = open('chordsplit.jsonl', 'w')
for f in sorted(glob.glob('fail_*.pkl')):
    d = pickle.load(open(f, 'rb')); T = graph(d['name']); S = d['A'] | d['B']
    P = pieces(T, S); res = []
    for cl in P:
        if isinstance(cl, tuple): res.append(('nodisc', len(cl[1]))); continue
        if len(cl.tris) < 1: continue
        ok = sat_level(cl, 1.0, budget=3*10**6)
        res.append((len(cl.S), cl.m, ok not in (None, 'UNK') if ok != 'UNK' else 'UNK'))
    rec = dict(file=f, pieces=len(P), all_level=all(r[2] is True for r in res if r[0] != 'nodisc'), res=res[:40])
    out.write(json.dumps(rec)+'\n'); out.flush(); print(f, len(P), rec['all_level'], flush=True)
