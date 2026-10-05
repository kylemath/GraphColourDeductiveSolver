"""Exercise full-replay rejection of false positive claims on fixed old fixtures.

The producer imports here generate test inputs only; the actual replay imports
no producer code. No new phase or graph order is run.
"""
import copy
import json
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'wp19'))
import wp19_core
from wp18_independent import ROOT, parse_graph
from wp19_math_replay import replay_graph


def main():
    results=[]
    for phase,n,idx in [('P1',12,0),('P1',14,0),('P1',17,1),('P4',22,93)]:
        g=next(g for g in json.loads((ROOT/'wp18'/('wp18-'+phase+'.json')).read_text())['graphs']
               if (g['order'],g['graph_index'])==(n,idx))
        report=wp19_core.graph_report(parse_graph(g['ascii']),order=n,graph_index=idx,ascii_=g['ascii'])
        r=replay_graph(report);rejections=[]
        for what in ('histogram','starts','positive_U','classes','coverage'):
            bad=copy.deepcopy(report)
            if what=='histogram':bad['pairs'][0]['hist_l']['0']+=1
            if what=='starts':bad['pairs'][0]['starts']+=1
            if what=='positive_U':bad['pairs'][0]['U']=not bad['pairs'][0]['U']
            if what=='classes':bad['pairs'][0]['tstar_classes']+=1
            if what=='coverage':bad['pairs'].pop()
            try:replay_graph(bad)
            except ValueError:rejections.append(what)
            else:raise AssertionError('corruption accepted: '+what)
        results.append({'order':n,'index':idx,'m':r['m'],'U_exists':r['U_exists'],'rejected':rejections})
        print('PASS',n,idx,'valid report plus',len(rejections),'corruptions',flush=True)
    Path(__file__).with_name('wp19-math-replay-regression-results.json').write_text(json.dumps(results,indent=2)+'\n')


if __name__=='__main__':main()
