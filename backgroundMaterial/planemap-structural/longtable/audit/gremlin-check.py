"""Independent bounded replay of explicit gremlin witnesses; no census runs.

Uses only the Python standard library, and does not import the team's move code.
Reads existing outputs and writes its own results beside this file.
"""
import hashlib
import itertools
import json
from collections import Counter, deque
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
OUT = Path(__file__).resolve().parent

def proper(adj, c):
    return all(c[v] is None or c[w] is None or c[v] != c[w]
               for v in adj for w in adj[v])

def link(adj, c, h):
    return Counter(c[w] for w in adj[h])

def swaps(adj, c, h):
    for a, b in itertools.combinations(range(4), 2):
        todo = {v for v in adj if v != h and c[v] in (a, b)}
        comps = []
        while todo:
            v = min(todo); todo.remove(v)
            comp = {v}; stack = [v]
            while stack:
                for w in adj[stack.pop()]:
                    if w in todo:
                        todo.remove(w); comp.add(w); stack.append(w)
            comps.append(comp)
        for comp in comps:
            cc = list(c)
            for v in comp:
                cc[v] = b if c[v] == a else a
            assert proper(adj, cc)
            yield (a, b), comp, tuple(cc), len(comps) == 1

def slide(adj, c, h, w):
    assert w in adj[h] and link(adj, c, h)[c[w]] == 1
    cc = list(c); cc[h], cc[w] = cc[w], None
    assert proper(adj, cc)
    return tuple(cc), w

def frozen(adj, c, h):
    counts = link(adj, c, h)
    return len(counts) == 4 and min(counts.values()) >= 2

def sphere(rot):
    n = len(rot); edges = sum(map(len, rot)) // 2
    assert all(len(set(ns)) == len(ns) and v not in ns and
               all(v in rot[w] for w in ns) for v, ns in enumerate(rot))
    seen = set(); faces = []
    for v, ns in enumerate(rot):
        for w in ns:
            if (v, w) in seen: continue
            start = dart = (v, w); face = []
            while dart not in seen:
                seen.add(dart); face.append(dart[0])
                a, b = dart
                dart = (b, rot[b][(rot[b].index(a) + 1) % len(rot[b])])
            assert dart == start and len(face) == 3
            faces.append(face)
    assert edges == 3*n-6 and n-edges+len(faces) == 2
    reached={0}; stack=[0]
    while stack:
        for w in rot[stack.pop()]:
            if w not in reached: reached.add(w); stack.append(w)
    assert len(reached)==n
    return {'vertices': n, 'edges': edges, 'faces': len(faces),
            'minimum_degree': min(map(len, rot))}

ascii21 = 'bcdef,aflghijkc,abkmd,acmnoe,adopqf,aeqlb,blrsh,bgsoi,bhotj,bituk,bjumc,bfqrg,ckund,dmuto,dntihspe,eosrq,eprlf,glqps,grpoh,ionuj,jtnmk'
rot21 = [[ord(x)-97 for x in ns] for ns in ascii21.split(',')]
adj21 = dict(enumerate(rot21))
c21 = (0,None,1,2,1,2,0,1,2,0,3,3,0,1,0,2,0,1,3,3,2)
assert proper(adj21,c21) and frozen(adj21,c21,1)
moves21 = list(swaps(adj21,c21,1))
assert len(moves21) == 16 and all(frozen(adj21,m[2],1) for m in moves21)
pairs = [(m1,m2) for m1 in moves21 for m2 in swaps(adj21,m1[2],1) if not m2[3]]
assert len(pairs) == 224
assert sum(frozen(adj21,m2[2],1) for _,m2 in pairs) == 172
def named(c, pair, comp):
    return next(m[2] for m in swaps(adj21,c,1) if m[0] == pair and m[1] == comp)
c1 = named(c21,(0,3),{0})
c2 = named(c1,(0,1),{2,4,6,7,12,13,14,16,17})
c3,h3 = slide(adj21,c2,1,6)
assert len(link(adj21,c3,h3)) == 3 and 2 not in link(adj21,c3,h3)
cfull = list(c3); cfull[h3] = 2
assert proper(adj21,cfull)
results = {'witness21': {**sphere(rot21), 'single_swaps':16,
    'all_single_swaps_frozen':True, 'ordered_pairs':224,'frozen_pairs':172,
    'verified_fill':'swap (0,3) on {0}; swap (0,1) on {2,4,6,7,12,13,14,16,17}; slide 1->6; fill 6 with 2',
    'minimum_kempe_swaps_with_slides':2}}
results['witness21']['two_swap_direct_fills']=sum(len(link(adj21,m2[2],1))<=3 for _,m2 in pairs)
results['witness21']['three_swap_direct_fill_exists']=any(
    len(link(adj21,m3[2],1))<=3 for _,m2 in pairs
    for m3 in swaps(adj21,m2[2],1))
assert results['witness21']['two_swap_direct_fills']==0
assert results['witness21']['three_swap_direct_fill_exists']

# Explicit order-14 witness, using the graph construction in fan-link.md.
N,S=12,13
adj14={v:set() for v in range(14)}
def edge(v,w): adj14[v].add(w); adj14[w].add(v)
for i in range(6):
    edge(N,i); edge(S,6+i); edge(i,(i+1)%6); edge(6+i,6+(i+1)%6)
    edge(i,6+i); edge(i,6+(i+1)%6)
c14=(None,0,3,0,2,0,2,3,1,2,3,1,1,0)
assert proper(adj14,c14)
assert c14[N]!=c14[6] and c14[N]!=c14[7]
m14=list(swaps(adj14,c14,0))
assert all(len(link(adj14,m[2],0))==4 for m in m14)
slides14=[]
for w in adj14[0]:
    if link(adj14,c14,0)[c14[w]]==1:
        cc,hh=slide(adj14,c14,0,w)
        assert len(link(adj14,cc,hh))==4
        slides14.append(w)
assert set(slides14)=={N,6,7}
# Find a concrete two-move fill, checking only this explicit start.
success=[]
first=[('swap '+str((p,sorted(k))),cc,0) for p,k,cc,_ in m14]
first += [('slide 0->'+str(w),*slide(adj14,c14,0,w)) for w in slides14]
for label,cc,h in first:
    for p,k,dd,_ in swaps(adj14,cc,h):
        if len(link(adj14,dd,h))<=3:
            success.append([label,'swap '+str((p,sorted(k))),h])
    for w in adj14[h]:
        if link(adj14,cc,h)[cc[w]]==1:
            dd,j=slide(adj14,cc,h,w)
            if len(link(adj14,dd,j))<=3:
                success.append([label,'slide '+str(h)+'->'+str(w),j])
assert success
assert len(success)==36
results['witness14']={'edges':sum(map(len,adj14.values()))//2,
    'minimum_degree':min(map(len,adj14.values())), 'single_kempe_components':len(m14),
    'single_move_fills':0,'legal_first_slides':slides14,'minimum_mixed_moves':2,
    'two_move_fill_example':success[0],'two_move_sequences_that_fill':len(success),
    'scope':'one explicit fan-proper start, not the best vertex/fan statistic'}

# Missing A_rho tile: symbolic neighbourhood replay for both rho/tau choices
# and every possible outer boundary colour. No belt-colouring enumeration.
tile=[]
for rho,tau in [(2,3),(3,2)]:
    for x in (rho,tau):  # u_{i-2}, adjacent to a=0 and u_{i-1}=1
        for d in (rho,tau):  # v_{i-3}, adjacent to b=1 and v_{i-2}=0
            if x==d: continue  # the edge u_{i-2} v_{i-3}
            col={'a':0,'b':1,'v0':None,'v-1':rho,'v-2':0,'v1':0,
                 'u0':tau,'u-1':1,'u1':rho,'u-2':x,'v-3':d}
            links={'v0':['b','v-1','u0','u1','v1'],
                   'u0':['a','u1','v0','v-1','u-1'],
                   'u-1':['a','u0','v-1','v-2','u-2'],
                   'v-1':['b','v-2','u-1','u0','v0'],
                   'v-2':['b','v-3','u-2','u-1','v-1']}
            h='v0'; path=['u0','u-1']
            if x==tau: path+=['v-1','v-2']
            frames=[]
            for w in path:
                counts=Counter(col[v] for v in links[h])
                assert w in links[h] and counts[col[w]]==1
                frames.append([h,[col[v] for v in links[h]],w])
                col[h],col[w]=col[w],None; h=w
            final=[col[v] for v in links[h]]
            if x==rho: assert len(set(final))==3
            else: assert final==[1,d,tau,rho,0]
            tile.append({'rho':rho,'tau':tau,'u_i_minus_2':x,
                'v_i_minus_3':d,'steps':frames,'final_hole':h,'final_link':final})
results['A_rho_tile']=tile

# Summaries of existing data, not new searches.
distance=json.loads((BASE/'wp15-kempe-distance/kempe-distance-results.json').read_text())
rows=[r for g in distance for r in g['roots']]
results['existing_kempe_distance']={'graphs':len(distance),'orders':dict(Counter(g['order'] for g in distance)),
    'roots':len(rows),'roots_with_unreachable':sum(bool(r['all']['unreachable']) for r in rows),
    'targetless_classes':sum(r['all']['classes_without_target'] for r in rows),
    'root_max_distance_histogram':dict(Counter(r['all']['ecc'] for r in rows)),
    'best_root_distance_histogram':dict(Counter(min(r['all']['ecc'] for r in g['roots']) for g in distance)),
    'scope':'read existing JSON and inspected producer; not an independent move-graph replay'}

def canonical(c):
    rename={}; out=[]
    for x in c:
        if x is None: out.append(None); continue
        if x not in rename: rename[x]=len(rename)
        out.append(rename[x])
    return tuple(out)

def enumerate_deletion(adj,h):
    vertices=[v for v in sorted(adj) if v!=h]
    c=[None]*len(adj); out=[]
    def walk(i,top):
        if i==len(vertices): out.append(tuple(c)); return
        v=vertices[i]; banned={c[w] for w in adj[v] if c[w] is not None}
        for a in range(min(3,top+1)+1):
            if a not in banned:
                c[v]=a; walk(i+1,max(top,a)); c[v]=None
    walk(0,-1)
    return out

# Independently replay the already reported icosahedron computation.
ico=next(g for g in distance if g['order']==12)
rot12=[[ord(x)-97 for x in ns] for ns in ico['ascii'].split()[1].split(',')]
adj12=dict(enumerate(rot12)); sphere(rot12)
ico_rows=[]
for h in range(12):
    cs=enumerate_deletion(adj12,h)
    assert len(cs)==20
    assert sum(len(link(adj12,c,h))<=3 for c in cs)==10
    assert all(len(link(adj12,c,h))<=3 or
        any(len(link(adj12,m[2],h))<=3 for m in swaps(adj12,c,h)) for c in cs)
    boundary=rot12[h]
    union=set()
    for i in range(5):
        apex=boundary[i]; far=boundary[(i+2)%5]; near=boundary[(i+3)%5]
        assert far not in adj12[apex] and near not in adj12[apex]
        starts=[c for c in cs if c[apex]!=c[far] and c[apex]!=c[near]]
        union.update(starts); assert len(starts)==8
        lengths=[]
        for c in starts:
            if len(link(adj12,c,h))<=3: lengths.append(0); continue
            one=[]
            for w in adj12[h]:
                if link(adj12,c,h)[c[w]]==1:
                    one.append(slide(adj12,c,h,w))
            if any(len(link(adj12,cc,j))<=3 for cc,j in one):
                lengths.append(1); continue
            assert any(len(link(adj12,dd,k))<=3
                for cc,j in one for w in adj12[j]
                if link(adj12,cc,j)[cc[w]]==1
                for dd,k in [slide(adj12,cc,j,w)])
            lengths.append(2)
        assert Counter(lengths)=={0:2,1:3,2:3}
        ico_rows.append({'vertex':h,'fan':i,'slide_distances':dict(Counter(lengths))})
    assert len(union)==20
results['independent_icosahedron_replay']={'vertices':12,'fans':len(ico_rows),
    'deletion_orbits_per_vertex':20,'orbits_per_fan':8,
    'per_fan_slide_distances':{'0':2,'1':3,'2':3},
    'maximum_kempe_distance':1}

# One existing graph with best fixed-root distance four: independent replay.
g17=next(g for g in distance if g['order']==17 and g['graph_index']==1)
rot17=[[ord(x)-97 for x in ns] for ns in g17['ascii'].split()[1].split(',')]
adj17=dict(enumerate(rot17)); sphere(rot17); replay=[]
for h in range(17):
    if len(rot17[h])!=5: continue
    cs=enumerate_deletion(adj17,h); ids={c:i for i,c in enumerate(cs)}
    neighbours=[]
    for c in cs:
        neighbours.append({ids[canonical(m[2])] for m in swaps(adj17,c,h)})
    assert all(i in neighbours[j] for i,ns in enumerate(neighbours) for j in ns)
    dist={i:0 for i,c in enumerate(cs) if len(link(adj17,c,h))<=3}
    q=deque(dist)
    while q:
        i=q.popleft()
        for j in neighbours[i]:
            if j not in dist: dist[j]=dist[i]+1; q.append(j)
    assert len(dist)==len(cs)
    ecc=max(dist.values())
    saved=next(r for r in g17['roots'] if r['root']==h)
    assert saved['states']==len(cs) and saved['all']['ecc']==ecc
    replay.append({'root':h,'states':len(cs),'maximum_swaps':ecc})
assert min(r['maximum_swaps'] for r in replay)==4
results['independent_order17_graph1_replay']={'roots':replay,'best_root_worst_swaps':4,
    'scope':'fixed hole; arbitrary deletion starts; no slide or selected-fan restriction'}

# Check existing generated graphs, without trusting the generator's validator.
generated=json.loads((BASE/'wp13-generator/corpus.json').read_text())
gen_fail=[]
for g in generated['graphs']:
    try:
        shape=sphere(g['rotation'])
        assert shape['vertices']==g['order'] and shape['minimum_degree']>=5
        assert {str(k):v for k,v in Counter(map(len,g['rotation'])).items()}==g['degree_counts']
        assert [i for i,ns in enumerate(g['rotation']) if len(ns)==5]==g['degree_five_roots']
    except AssertionError: gen_fail.append(g['id'])
assert not gen_fail
results['independent_generated_graph_validation']={'graphs_checked':len(generated['graphs']),
    'failures':gen_fail,'scope':'simplicity, connectivity, spherical triangular rotation, degree metadata; non-isomorphism not rechecked'}

results['existing_scale_sweeps']=[]
for order in range(20,27):
    d=json.loads((BASE/f'wp12-scale/sweep-{order}-all.json').read_text())
    results['existing_scale_sweeps'].append({'order':order,'graphs':d['graphs_checked'],
        'roots':d['roots_checked'],'existential_survivors':len(d['validation_existential_survivors_still_existentially_good']),
        'q_bad_roots':d['per_weight'][0]['bad_roots'],
        'q_graphs_without_good_root':len(d['per_weight'][0]['graphs_with_no_good_root']),
        'lin_bad_roots':d['per_weight'][1]['bad_roots'],
        'lin_graphs_without_good_root':len(d['per_weight'][1]['graphs_with_no_good_root']),
        'scope':'existing producer output only; no independent sweep replay'})
for rel in ['wp14-theory/check_lock.json','wp14-theory/rank_probe.json',
            'wp14-theory/hard_census.json','wp17-last-roots/checks3.json']:
    data=json.loads((BASE/rel).read_text())
    results[rel]={k:v for k,v in data.items() if isinstance(v,(int,float,str,bool)) or k=='stats'}
hold=json.loads((BASE/'wp17-last-roots/holdout_eval.json').read_text())
results['existing_holdout']={}
for lo,hi in [(12,18),(19,20),(21,21),(22,22)]:
    sub=[r for r in hold if lo<=r[0]<=hi]
    results['existing_holdout'][f'{lo}-{hi}']={'roots':len(sub),'graphs':len({(r[0],r[1]) for r in sub}),
        'max_distance_histogram':dict(Counter(r[3] for r in sub)),
        'bad_roots_by_rank':dict(Counter(name for r in sub for name in r[4]))}
# Verify the entire saved WP11 manifest without running its experiment.
manifest=BASE/'wp11-validation/SHA256SUMS'; failures=[]; checked=0
for row in manifest.read_text().splitlines():
    digest,rel=row.split(None,1); p=manifest.parent/rel.strip()
    if hashlib.sha256(p.read_bytes()).hexdigest()!=digest: failures.append(rel)
    checked+=1
results['WP11_manifest']={'files_checked':checked,'mismatches':failures}
assert not failures
(OUT/'gremlin-check-results.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
