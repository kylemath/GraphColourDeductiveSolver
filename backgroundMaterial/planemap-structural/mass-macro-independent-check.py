"""Independent standard-library verification of saved failure witnesses; no census rerun."""
import argparse, json, hashlib, itertools
from pathlib import Path
SCRIPT_DIR=Path(__file__).resolve().parent
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--input-dir',type=Path,default=SCRIPT_DIR)
parser.add_argument('--results',type=Path,default=SCRIPT_DIR/'mass-macro-results.json')
parser.add_argument('--output',type=Path,default=SCRIPT_DIR/'mass-macro-independent-check.json')
args=parser.parse_args()
BASE=args.input_dir
SOURCE=args.results
data=json.loads(SOURCE.read_text())
def canonical(c):
    labels=sorted(set(c),key=lambda k:c.index(k))
    return tuple(labels.index(k) for k in c)
def components(c,adj,pair):
    unseen=[v for v in range(len(c)) if c[v] in pair]; ans=[]
    while unseen:
        todo=[unseen.pop(0)]; seen=set(todo)
        while todo:
            v=todo.pop()
            for w in adj[v]:
                if w in unseen:
                    unseen.remove(w); seen.add(w); todo.append(w)
        ans.append(seen)
    return ans
def rank(c,adj,B,n):
    p=max(0,len(set(c[v] for v in B))-3)
    q=sum(len(K-B)**2 for pair in itertools.combinations(range(4),2)
          for K in components(c,adj,pair) if K&B)
    return (p,q),(6*n*n+1)*p+q
def moves(c,adj,B,n,labels):
    out=[]
    for pair in itertools.combinations(range(4),2):
        for K in components(c,adj,pair):
            t=list(c)
            for v in K: t[v]=pair[1] if c[v]==pair[0] else pair[0]
            t=canonical(t)
            assert all(t[v]!=t[w] for v in range(len(t)) for w in adj[v])
            lex,R=rank(t,adj,B,n)
            out.append((tuple(pair),tuple(sorted(labels[v] for v in K)),t,lex,R))
    return out
def recorded(ms):
    return sorted((tuple(m['pair']),tuple(m['component']),tuple(m['successor_coloring']),tuple(m['successor_lex_rank']),m['successor_rank']) for m in ms)
checks=[]
for name,expected in data['input_hashes'].items():
    assert hashlib.sha256((BASE/name).read_bytes()).hexdigest()==expected
for order in data['orders']:
    n=order['order']; lines=(BASE/f'triangulations-min5-{n}.txt').read_text().splitlines()
    for g in order['graphs_checked']:
        line=lines[g['graph_index']]
        assert line==g['ascii'] and hashlib.sha256(line.encode()).hexdigest()==g['ascii_sha256']
        rotation=[[ord(x)-97 for x in row] for row in line.split(' ',1)[1].split(',')]
        assert len(rotation)==n
        assert sum(map(len,rotation))==6*n-12
        assert all(len(set(ns))==len(ns) and v not in ns and all(v in rotation[z] for z in ns) for v,ns in enumerate(rotation))
        darts={(v,z) for v,ns in enumerate(rotation) for z in ns}; unseen=set(darts); face_count=0
        while unseen:
            d=next(iter(unseen)); start=d; walk=[]
            while d not in walk:
                assert d in unseen; unseen.remove(d); walk.append(d)
                v,z=d; incoming=rotation[z].index(v)
                d=(z,rotation[z][(incoming+1)%len(rotation[z])])
            assert d==start and len(walk)==3
            face_count+=1
        assert face_count==2*n-4
        reached={0}; todo=[0]
        while todo:
            v=todo.pop()
            for z in rotation[v]:
                if z not in reached: reached.add(z); todo.append(z)
        assert len(reached)==n
        for rr in g['roots']:
            if rr['outcome']!='fails': continue
            root=rr['root']; labels=[v for v in range(n) if v!=root]
            assert labels==rr['vertex_order']
            adj=[{labels.index(w) for w in rotation[v] if w!=root} for v in labels]
            B={labels.index(v) for v in rotation[root]}
            w=rr['failure_witness']; c=tuple(w['coloring'])
            assert all(c[v]!=c[z] for v in range(n-1) for z in adj[v])
            lex,R=rank(c,adj,B,n)
            assert lex==tuple(w['lex_rank']) and R==w['rank'] and lex[0]==1
            first=moves(c,adj,B,n,labels)
            assert sorted(first)==recorded(w['one_step_moves'])
            successors={m[2] for m in first}
            assert successors=={tuple(layer['intermediate_coloring']) for layer in w['two_step_layers']}
            secondcount=0
            for layer in w['two_step_layers']:
                t=tuple(layer['intermediate_coloring']); second=moves(t,adj,B,n,labels)
                assert rank(t,adj,B,n)[1]==layer['rank']
                assert sorted(second)==recorded(layer['moves'])
                assert all(m[-1]>=R and m[-2]>=lex for m in second)
                secondcount+=len(second)
            assert all(m[-1]>=R and m[-2]>=lex for m in first)
            for permutation in itertools.permutations(range(4)):
                pc=tuple(permutation[a] for a in c)
                assert rank(pc,adj,B,n)==(lex,R)
                assert {m[2] for m in moves(pc,adj,B,n,labels)}==successors
            perm=list(reversed(range(n-1)))
            pc=tuple(c[perm[i]] for i in range(n-1))
            pa=[{perm.index(z) for z in adj[perm[i]]} for i in range(n-1)]
            pb={perm.index(z) for z in B}
            assert rank(pc,pa,pb,n)==(lex,R)
            checks.append(dict(order=n,graph_index=g['graph_index'],root=root,coloring=c,lex_rank=lex,rank=R,first_moves=len(first),distinct_first_successors=len(successors),second_moves=secondcount,minimum_successor_rank=min([m[-1] for m in first]+[m['successor_rank'] for l in w['two_step_layers'] for m in l['moves']])))
report=dict(status='passed',scope='All saved failing-root first witnesses only; no rerun of corpus colouring enumeration',source_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),checker_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),checks=checks,failed_root_witnesses=len(checks),first_failure=checks[0] if checks else None,color_permutations_per_witness=24,vertex_invariance_check='reverse deletion-vertex order',enumeration_review='DSATUR chooses next vertex using colour-equality patterns and degrees, hence ordering is unchanged by colour permutation. Assigning existing names or exactly one fresh name preserves one representative of every proper-colouring orbit. Canonicalization by original vertex order merges any duplicate representatives. Closure under all six-pair component swaps is explicitly checked against enumerated states.')
args.output.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
