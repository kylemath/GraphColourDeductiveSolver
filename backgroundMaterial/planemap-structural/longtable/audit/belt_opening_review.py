"""Bounded audit of missing opening coverage; no large belt enumeration.

Symbolically enumerates only five link positions and replays the existing G5
regression graph to show that omitted classes have proper global extensions.
"""
import itertools
import json
from collections import Counter
from pathlib import Path
from wp18_independent import deletion_starts, parse_graph, state_ok

patterns=[]
for u1,v0,vm,um in itertools.product((1,2,3),(0,2,3),(0,2,3),(1,2,3)):
    p=(0,u1,v0,vm,um)
    if len(set(p))==4 and u1!=v0 and v0!=vm and vm!=um:
        patterns.append({'link':list(p),'doubled':next(c for c,n in Counter(p).items() if n==2)})
assert len(patterns)==14
assert Counter(p['doubled'] for p in patterns)=={0:8,1:2,2:2,3:2}

n=5; faces=[]
for i in range(n):
    u=2+i; un=2+(i+1)%n; v=2+n+i; vn=2+n+(i+1)%n; vp=2+n+(i-1)%n
    faces += [(0,u,un),(1,vn,v),(u,vp,v),(u,v,un)]
succ=[{} for _ in range(12)]
for x,y,z in faces:
    for pred,mid,nxt in ((x,y,z),(y,z,x),(z,x,y)):
        assert pred not in succ[mid] or succ[mid][pred]==nxt
        succ[mid][pred]=nxt
rot=[]
for mapping in succ:
    start=min(mapping); current=start; ns=[]
    while True:
        ns.append(current); current=mapping[current]
        if current==start: break
    assert len(ns)==len(mapping); rot.append(ns)
ascii_='12 '+','.join(''.join(chr(97+w) for w in ns) for ns in rot)
assert parse_graph(ascii_)==rot
found={}; starts=deletion_starts(rot,2)
for state in starts:
    if state[0]==state[1]: continue
    p=[state[v] for v in (0,3,7,11,6)]
    if len(set(p))!=4: continue
    doubled=next(c for c,k in Counter(p).items() if k==2)
    if doubled in (0,1) and doubled not in found:
        state_ok(rot,state,2)
        found[doubled]={'vertex_order':['a','b']+[f'u{i}' for i in range(n)]+[f'v{i}' for i in range(n)],
            'hole':'u0','state':list(state),'link':p}
assert set(found)=={0,1}
result={'scope':'five-position local truth table plus existing named G5 regression',
    'local_non_target_patterns':patterns,'counts_by_doubled_colour':dict(Counter(p['doubled'] for p in patterns)),
    'G5_rotation':ascii_,'G5_deletion_orbits':len(starts),'proper_omitted_opening_examples':found}
(Path(__file__).parent/'belt-opening-review-results.json').write_text(json.dumps(result,indent=2)+'\n')
print('PASS: eight doubled-0 and two doubled-1 local patterns are outside the cap opening assumption; G5 examples proper')
