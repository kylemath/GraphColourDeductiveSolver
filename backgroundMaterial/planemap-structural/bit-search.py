"""Stress the fixed one-bit robust quotient game on a finite Plantri census."""
import argparse,collections,hashlib,json,time
from pathlib import Path
from escape import colors,canon,P,attractor
from search import parse

def check_root(G,rot,r,details=False):
 H=G.copy();H.remove_node(r);V=sorted(H);B=list(rot[r]);B=B[B.index(min(B)):]+B[:B.index(min(B))];C=colors(H,V);idx={c:i for i,c in enumerate(C)};vadj={v:set(H[v]) for v in V};S=[];A=[];bits=[]
 for c in C:
  cd=dict(zip(V,c));mp={};cc={v:mp.setdefault(cd[v],len(mp)) for v in B+[v for v in V if v not in B]};parts=[];actions={};bit=False
  assert all(cd[u]!=cd[v] for u,v in H.edges)
  for a,b in P:
   pending={v for v in V if cc[v] in (a,b)};p=[]
   while pending:
    seed=min(pending);K={seed};q=[seed];pending.remove(seed)
    for v in q:
     ns=vadj[v]&pending;pending-=ns;K|=ns;q.extend(ns)
    bi=tuple(j for j,v in enumerate(B) if v in K)
    if (a,b)==(1,3) and min(V) in K and bi:bit=True
    if bi:
     p.append(bi);actions[(a,b,bi)]=idx[canon([b if cc[v]==a and v in K else a if cc[v]==b and v in K else cc[v] for v in V])]
   parts.append(tuple(sorted(p)))
  S.append((tuple(cc[v] for v in B),tuple(parts)));A.append(actions);bits.append(bit)
 keys=[(S[i],bits[i]) for i in range(len(S))];good={i for i,s in enumerate(S) if len(set(s[0]))<=3};win,gr,rounds=attractor(S,A,good,lambda i:keys[i]);losing=set(gr)-win
 result={'root':r,'boundary':B,'vertex_order':V,'coloring_orbits':len(C),'groups':len(gr),'losing_groups':len(losing),'winning_rounds':rounds}
 if details:
  cert=[]
  for k in sorted(losing,key=repr):
   ids=gr[k];assert not any(i in good for i in ids);common=set(A[ids[0]])
   for i in ids[1:]:common.intersection_update(A[i])
   blockers=[]
   for a in sorted(common,key=repr):
    witnesses=[i for i in ids if keys[A[i][a]] in losing];assert witnesses
    i=witnesses[0];blockers.append({'action':a,'source_coloring':C[i],'successor_coloring':C[A[i][a]],'successor_observation':repr(keys[A[i][a]])})
   cert.append({'observation':repr(k),'states':len(ids),'representative_coloring':C[ids[0]],'common_action_blockers':blockers})
  result['robust_losing_certificate']=cert
 return result

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--input-dir',type=Path,default=Path(__file__).parent);ap.add_argument('--max-order',type=int,default=20);ap.add_argument('--output',type=Path,default=Path(__file__).with_name('bit-search-results.json'));args=ap.parse_args();start=time.time()
 out={'scope':'Finite robust quotient-game stress test, not a universal theorem or Kempe-class kill witness.','observation_bit':'minimum remaining labelled vertex belongs to canonical {1,3} component meeting boundary','orders':[],'all_roots_robust_game_failure':None}
 for n in range(12,args.max_order+1):
  path=args.input_dir/f'triangulations-min5-{n}.txt';lines=path.read_text().splitlines();order={'order':n,'input_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'graphs_available':len(lines),'graphs_checked':[]};out['orders'].append(order)
  for gi,line in enumerate(lines):
   G,rot=parse(line);rs=[check_root(G,rot,r) for r in G if G.degree(r)==5];bad=all(r['losing_groups']>0 for r in rs);order['graphs_checked'].append({'graph_index':gi,'ascii':line,'roots':rs,'good_roots':sum(r['losing_groups']==0 for r in rs)});print(n,gi+1,'/',len(lines),'goodroots',sum(r['losing_groups']==0 for r in rs),flush=True)
   if 'first_failing_root_fixture' not in out and any(r['losing_groups'] for r in rs):
    failing=next(r for r in rs if r['losing_groups']);out['first_failing_root_fixture']={'order':n,'graph_index':gi,'ascii':line,'root':check_root(G,rot,failing['root'],True)}
   if bad:
    out['all_roots_robust_game_failure']={'order':n,'graph_index':gi,'ascii':line,'roots':[check_root(G,rot,r,True) for r in G if G.degree(r)==5]};break
  out['elapsed_seconds']=time.time()-start;args.output.write_text(json.dumps(out,indent=2)+'\n')
  if out['all_roots_robust_game_failure']:break
 if not out['all_roots_robust_game_failure']:out['completed_through_order']=args.max_order
 out['elapsed_seconds']=time.time()-start;args.output.write_text(json.dumps(out,indent=2)+'\n')
if __name__=='__main__':main()
