"""Answer Long Table using frozen outputs and targeted independent replay only."""
import hashlib,json,time
from collections import Counter
from multiprocessing import Pool
from pathlib import Path
from wp18_independent import ROOT,deletion_starts,fans,parse_graph,target,require
from wp19_math_replay import flood


def weighted(hist):return sum(int(k)*v for k,v in hist.items() if k.isdigit())

def joint(g):
    rot=parse_graph(g['ascii']);allstarts={h:deletion_starts(rot,h) for h in range(len(rot))}
    U=set().union(*allstarts.values());ld=flood(rot,[s for s in U if target(rot,s)],6,universe=U)
    legal=fans(rot);roots={v for v,i in legal}
    kd={v:flood(rot,[s for s in allstarts[v] if target(rot,s)],kempe=True,universe=set(allstarts[v])) for v in roots}
    memberships=Counter();distinct={};hl=Counter();hk=Counter()
    for (v,i),chords in legal.items():
        for s in allstarts[v]:
            if not all(s[a]!=s[b] for a,b in chords):continue
            ell=ld[s];kap=kd[v][s];require(kap>=ell,'Kempe/mixed inclusion');delta=kap-ell
            memberships[delta]+=1;distinct[s]=delta;hl[str(ell)]+=1;hk[str(kap)]+=1
    require(dict(hl)=={k:v for k,v in g['hist_l'].items() if v},'targeted mixed histogram')
    require(dict(hk)=={k:v for k,v in g['hist_k'].items() if v},'targeted Kempe histogram')
    return {'order':g['order'],'graph_index':g['graph_index'],'membership_gaps':dict(memberships),
            'distinct_start_gaps':dict(Counter(distinct.values()))}


def main():
    t0=time.monotonic();phases={};tasks=[];manifest=json.loads((ROOT/'wp19/WP19-verified-output-manifest.json').read_text())
    for phase in ('P1','P2','P3'):
        raw=ROOT/'wp19'/f'wp19-{phase}.json';require(hashlib.sha256(raw.read_bytes()).hexdigest()==manifest[phase]['raw_sha256'],'raw binding')
        d=json.loads(raw.read_text());a=json.loads((ROOT/'audit'/f'wp19-{phase}-math-replay.json').read_text());ar={(g['order'],g['graph_index']):g for g in a['graphs']}
        summary={'m_hist':d['summary']['m_hist'],'max_ell':d['summary']['max_L_at_least'],
                 'U_failing_pairs':sum(p['U'] is False for g in d['graphs'] for p in g['pairs']),
                 'm3_graphs':[[g['order'],g['graph_index']] for g in d['graphs'] if g['m']==3],
                 'membership_gaps':Counter(),'distinct_start_gaps':Counter(),'near_misses':[],
                 'raw_sha256':manifest[phase]['raw_sha256'],'archive_sha256':manifest[phase]['archive_sha256'],
                 'positive_gap_graphs':0}
        for g in d['graphs']:
            r=ar[g['order'],g['graph_index']];delta=weighted(r['hist_k'])-weighted(r['hist_l']);require(delta>=0,'nonnegative gap sum')
            if delta:
                tasks.append((phase,r,g));summary['positive_gap_graphs']+=1
            else:
                summary['membership_gaps'][0]+=sum(r['hist_l'].values());summary['distinct_start_gaps'][0]+=r['distinct_admitted_starts']
            rot=parse_graph(g['ascii']);degree5=[v for v,ns in enumerate(rot) if len(ns)==5];byroot={v:[] for v in degree5}
            for p in g['pairs']:byroot[p['v']].append(p)
            require(all(byroot.values()),'degree5 root without legal nonempty fan needs separate handling')
            good=[v for v,ps in byroot.items() if min(p['L'] for p in ps)<=2]
            if len(good) in (1,2):
                summary['near_misses'].append({'order':g['order'],'graph_index':g['graph_index'],'degree5_vertices':len(degree5),
                                              'good_vertices':good,'bad_vertices':[v for v in degree5 if v not in good],
                                              'm':g['m'],'vertex_min_L':{str(v):min(p['L'] for p in ps) for v,ps in byroot.items()}})
        phases[phase]=summary
    print('Targeted existing-output replay graphs',len(tasks),flush=True)
    with Pool(10,maxtasksperchild=1) as pool:
        for index,(res,(phase,r,g)) in enumerate(zip(pool.imap(joint,[x[1] | {'ascii':x[2]['ascii']} for x in tasks]),tasks),1):
            require(sum(res['distinct_start_gaps'].values())==r['distinct_admitted_starts'],'distinct-start coverage')
            require(sum(int(k)*v for k,v in res['membership_gaps'].items())==weighted(r['hist_k'])-weighted(r['hist_l']),'gap total binding')
            phases[phase]['membership_gaps'].update(res['membership_gaps']);phases[phase]['distinct_start_gaps'].update(res['distinct_start_gaps'])
            if index%50==0:print('Verified',index,'/',len(tasks),round(time.monotonic()-t0,1),'seconds',flush=True)
    for s in phases.values():
        s['membership_gaps']=dict(sorted(s['membership_gaps'].items()));s['distinct_start_gaps']=dict(sorted(s['distinct_start_gaps'].items()))
    out={'scope':'saved WP19 outputs only; no new graph/search phase','binding_manifest':'wp19/WP19-verified-output-manifest.json',
         'gap_conventions':'membership counts one start per admitted fan; distinct counts each canonical (hole,colouring) once per graph',
         'near_miss_definition':'exactly one or two degree5 vertices have some legal fan with L<=2; all others have every legal fan L>=3',
         'method':'Zero weighted gap implies every gap is zero by kappa>=ell. Positive-gap graphs are independently replayed to obtain joint/deduplicated counts.',
         'seconds':round(time.monotonic()-t0,2),'phases':phases}
    (ROOT/'audit/wp19-followup-results.json').write_text(json.dumps(out,indent=2)+'\n')
    print('PASS',json.dumps({p:{k:v for k,v in s.items() if k!='near_misses'} | {'near_miss_graphs':len(s['near_misses'])} for p,s in phases.items()}),flush=True)

if __name__=='__main__':main()
