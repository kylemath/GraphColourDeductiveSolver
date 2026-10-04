import sys,json,runpy,itertools,collections,argparse,tempfile
from pathlib import Path
sys.dont_write_bytecode=True
parser=argparse.ArgumentParser(description='Independent exterior-root replay and two-swap formula test on graph36/root8.')
parser.add_argument('--input-dir',type=Path,default=Path(__file__).resolve().parent)
parser.add_argument('--output',type=Path,default=Path(__file__).with_name('afternoon-checks.json'))
args=parser.parse_args();folder=args.input_dir
with tempfile.TemporaryDirectory(prefix='afternoon-component-') as temporary:
    sys.argv=['component-mass.py','--output',str(Path(temporary)/'component.json')]
    d=runpy.run_path(str(folder/'component-mass.py'))
canon=d['canon'];colors=d['colors'];pairs=list(itertools.combinations(range(4),2))
def check_root(rot,r):
    V=[v for v in range(len(rot)) if v!=r];H={v:set(rot[v])-{r} for v in V}
    B=rot[r];B=B[B.index(min(B)):]+B[:B.index(min(B))]
    C=colors(H,V);idx={c:i for i,c in enumerate(C)};keys=[];actions=[]
    for c in C:
        cd=dict(zip(V,c));mp={};cc={v:mp.setdefault(cd[v],len(mp)) for v in B+[v for v in V if v not in B]}
        parts=[];acts={};bit=False
        assert all(cc[v]!=cc[w] for v in V for w in H[v])
        for a,b in pairs:
            pending={v for v in V if cc[v] in (a,b)};part=[]
            while pending:
                seed=min(pending);K={seed};queue=[seed];pending.remove(seed)
                for v in queue:
                    ns=H[v]&pending;pending-=ns;K|=ns;queue.extend(ns)
                bi=tuple(i for i,v in enumerate(B) if v in K)
                if (a,b)==(1,3) and min(V) in K and bi:bit=True
                if bi:
                    part.append(bi)
                    t=canon([b if cc[v]==a and v in K else a if cc[v]==b and v in K else cc[v] for v in V])
                    acts[(a,b,bi)]=idx[t]
            parts.append(tuple(sorted(part)))
        keys.append(((tuple(cc[v] for v in B),tuple(parts)),bit));actions.append(acts)
    groups=collections.defaultdict(list)
    for i,k in enumerate(keys):groups[k].append(i)
    winning={k for k in groups if len(set(k[0][0]))<=3};rounds=0
    while True:
        new=set()
        for k,ids in groups.items():
            if k in winning:continue
            common=set(actions[ids[0]])
            for i in ids[1:]:common&=actions[i].keys()
            if any(all(keys[actions[i][a]] in winning for i in ids) for a in common):new.add(k)
        if not new:break
        winning|=new;rounds+=1
    return dict(root=r,boundary=B,vertex_order=V,coloring_orbits=len(C),groups=len(groups),losing_groups=len(groups)-len(winning),winning_rounds=rounds)
board=json.loads((folder/'bit-search-results.json').read_text())
record=next(g for o in board['orders'] if o['order']==20 for g in o['graphs_checked'] if g['graph_index']==36)
assert record['ascii']==(folder/'triangulations-min5-20.txt').read_text().splitlines()[36]
rot=[[ord(c)-97 for c in row] for row in record['ascii'].split(' ',1)[1].split(',')]
assert len(rot)==20 and all(len(set(ns))==len(ns) and v not in ns and len(ns)>=5 and all(v in rot[w] for w in ns) for v,ns in enumerate(rot))
eligible=[r for r in range(20) if len(rot[r])==5 and r!=0 and r not in rot[0]]
rows=[]
for r in eligible:
    result=check_root(rot,r)
    assert result==next(row for row in record['roots'] if row['root']==r)
    rows.append(result)
D=d['D']; minrows=[]
for c,(score,moves) in D.items():
    if not score[0] or any(D[t][0]<score for _,t in moves):continue
    witness=None
    for a,t in moves:
        for b,u in D[t][1]:
            if D[u][0]<score:
                witness={'start':c,'rank':score,'first_move':a,'intermediate':t,'intermediate_rank':D[t][0],'second_move':b,'end':u,'end_rank':D[u][0]};break
        if witness:break
    minrows.append({'start':c,'two_swap_decrease':witness})
out={'scope':'Finite replays of existing root observations and a bounded two-swap experiment for the specific component-mass formula; no uniform coverage theorem.','order':20,'graph_index_zero_based':36,'ascii':record['ascii'],'anchor':0,'eligible_roots':eligible,'root_replays':rows,'component_mass_two_swap_checks':minrows,'all_non_targets_have_decrease_within_two_swaps':all(row['two_swap_decrease'] for row in minrows)}
args.output.write_text(json.dumps(out,indent=2)+'\n')
print([(row['root'],row['losing_groups'],row['winning_rounds']) for row in rows])
print('all non-targets decrease within two swaps:',out['all_non_targets_have_decrease_within_two_swaps'])
