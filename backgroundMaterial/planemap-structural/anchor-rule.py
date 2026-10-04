"""Inspect a concrete exterior-anchor selection rule against recorded experiments."""
import argparse,importlib.util,json
from pathlib import Path
import networkx as nx
from search import parse

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--bit-results',type=Path,default=Path(__file__).with_name('bit-search-results.json'));ap.add_argument('--census-results',type=Path,default=Path(__file__).with_name('search-results.json'));ap.add_argument('--kittell-input',type=Path,default=Path(__file__).parent.parent/'agent1720/groups/K6_kittell.json');ap.add_argument('--escape-results',type=Path,default=Path(__file__).with_name('results.json'));ap.add_argument('--output',type=Path,default=Path(__file__).with_name('anchor-rule-results.json'));args=ap.parse_args();bits=json.loads(args.bit_results.read_text());census=json.loads(args.census_results.read_text());selected=[];failedroots=[];failures=[]
 spec=importlib.util.spec_from_file_location('bit_search',Path(__file__).with_name('bit-search.py'));bs=importlib.util.module_from_spec(spec);spec.loader.exec_module(bs)
 for o in bits['orders']:
  for g in o['graphs_checked']:
   G,rot=parse(g['ascii']);a=min(G);eligible=sorted(rr['root'] for rr in g['roots'] if rr['root']!=a and not G.has_edge(a,rr['root']));assert len(eligible)>=6;by={r['root']:r for r in g['roots']};r=eligible[0];selected.append({'order':o['order'],'graph_index':g['graph_index'],'anchor':a,'eligible':eligible,'selected_root':r,'selected_losing_groups':by[r]['losing_groups']})
   for rr in g['roots']:
    if rr['losing_groups']:failedroots.append({'order':o['order'],'graph_index':g['graph_index'],'root':rr['root'],'outside_anchor_closed_neighborhood':rr['root']!=a and not G.has_edge(a,rr['root']),'losing_groups':rr['losing_groups']})
   if by[r]['losing_groups']:
    co=next(p for p in census['orders'] if p['order']==o['order']);cg=next(p for p in co['graphs_checked'] if p['graph_index']==g['graph_index']);assert cg['ascii']==g['ascii'];cr=next(p for p in cg['roots'] if p['root']==r);failures.append({'order':o['order'],'graph_index':g['graph_index'],'ascii':g['ascii'],'anchor':a,'eligible':eligible,'selected_root':r,'robust_game_certificate':bs.check_root(G,rot,r,True),'full_kempe_result':cr})
 kd=json.loads(args.kittell_input.read_text());G=nx.Graph(kd['edges']);a=min(G);eligible=sorted(v for v in G if G.degree(v)==5 and v!=a and not G.has_edge(a,v));r=eligible[0];er=json.loads(args.escape_results.read_text());rr=next(p for p in er['kittell']['roots'] if p['root']==r);k={'anchor':a,'eligible':eligible,'selected_root':r,'losing_groups':rr['named_min_vertex_13_bit']['certificate']['losing_groups']}
 out={'scope':'Finite test of a labelled exterior-root rule in the robust observation game, not a Kempe-class counterexample.','rule':'anchor=minvertex; root=min degree-five vertex outside closed neighborhood of anchor','checked_graphs':len(selected),'failed_root_instances':len(failedroots),'failed_roots_outside_anchor_closed_neighborhood':sum(r['outside_anchor_closed_neighborhood'] for r in failedroots),'selected_failures':failures,'per_graph_selection':selected,'failed_roots':failedroots,'kittell':k};args.output.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ('selected_failures','per_graph_selection','failed_roots')},indent=2))
if __name__=='__main__':main()
