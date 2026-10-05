"""Stream independent per-graph verification while a released phase produces.

Uses the frozen Math replay implementation. After production finishes, binds
every verified record to the final phase, source files, raw input and summary.
It never feeds a result back to the producer or changes the declared tests.
"""
import argparse
import hashlib
import json
import time
from collections import Counter
from multiprocessing import Pool
from pathlib import Path
from wp18_independent import ROOT, require
from wp19_math_replay import replay_graph


def digest_record(g):
    return hashlib.sha256(json.dumps(g,sort_keys=True,separators=(',',':')).encode()).hexdigest()


def work(g):
    return digest_record(g),replay_graph(g)


def incoming(phase,number):
    temp=ROOT/'wp19'/f'.wp19-{phase}.graphs.tmp'
    final=ROOT/'wp19'/f'wp19-{phase}.json'
    while not temp.exists():
        if final.exists():
            yield from json.loads(final.read_text())['graphs'];return
        time.sleep(1)
    # An open descriptor survives unlinking after the producer finalises.
    with temp.open() as f:
        buffer='';decoder=json.JSONDecoder();count=0
        while count<number:
            buffer=buffer.lstrip(', \t\r\n')
            if buffer:
                try:g,end=decoder.raw_decode(buffer)
                except json.JSONDecodeError:pass
                else:
                    buffer=buffer[end:];count+=1;yield g;continue
            new=f.read(1<<20)
            if new:buffer+=new;continue
            if final.exists():
                raise ValueError('final phase appeared before complete expected streamed records')
            time.sleep(1)


def main():
    ap=argparse.ArgumentParser();ap.add_argument('phase',choices=['P1','P2','P3'])
    ap.add_argument('--graphs',type=int,required=True);ap.add_argument('--procs',type=int,default=12)
    a=ap.parse_args();t0=time.monotonic();rows=[];hashes=[]
    sources=[Path(__file__),Path(__file__).with_name('wp19_math_replay.py'),
             Path(__file__).with_name('wp18_independent.py')]
    source_hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}
    with Pool(a.procs,maxtasksperchild=1) as pool:
        for h,r in pool.imap(work,incoming(a.phase,a.graphs)):
            hashes.append(h);rows.append(r)
            if len(rows)%200==0:
                print(a.phase,'stream verified',len(rows),'/',a.graphs,
                      round(time.monotonic()-t0,1),'seconds',flush=True)
    path=ROOT/'wp19'/f'wp19-{a.phase}.json'
    while not path.exists():time.sleep(1)
    data=json.loads(path.read_text());require(len(rows)==len(data['graphs'])==a.graphs,'complete count')
    require(hashes==[digest_record(g) for g in data['graphs']],'stream/final graph binding')
    require(data['phase']==a.phase and data['caps']=={'mixed':6,'kempe':7},'phase/caps')
    require(hashlib.sha256((ROOT/data['declaration']).read_bytes()).hexdigest()==data['declaration_sha256'],'declaration binding')
    for f,h in data['source_sha256'].items():require(hashlib.sha256((ROOT/f).read_bytes()).hexdigest()==h,'producer source binding')
    require(source_hashes=={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},'audit source changed during replay')
    expected_order=23 if a.phase=='P1' else 24
    require(a.phase!='P2','stream driver raw-input binding supports single-order phases only')
    require(all(g['order']==expected_order and g['graph_index']==i for i,g in enumerate(data['graphs'])),'ordered graph coverage')
    raw=''.join(g['ascii']+'\n' for g in data['graphs']).encode()
    require(hashlib.sha256(raw).hexdigest()==data['input_sha256'],'complete raw input binding')
    hl=Counter();hk=Counter();mh=Counter();uh=Counter();kills=Counter()
    for r in rows:
        hl.update(r['hist_l']);hk.update(r['hist_k']);kills.update(r['kills'])
        mh[str(r['m']) if r['m'] is not None else '>='+str(r['m_at_least'])]+=1
        uh[str(r['U_exists']).lower()]+=1
    summary=data['summary']
    require(dict(mh)==summary['m_hist'],'phase minima')
    require(dict(hl)==summary['hist_l'] and dict(hk)==summary['hist_k'],'complete phase histograms')
    require(all(uh.get(k,0)==v for k,v in summary['U_exists'].items()),'phase U counts')
    for stmt,s in summary['statements'].items():require(kills.get(stmt,0)==s['killed_count'],'phase kills')
    out={'scope':'complete independent WP19 replay, streamed concurrently with producer',
         'phase':a.phase,'complete':True,'phase_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
         'source_sha256':source_hashes,'seconds':round(time.monotonic()-t0,2),'graphs':rows,
         'summary':{'graphs':len(rows),'m_hist':dict(mh),'U_exists':dict(uh),
                    'kills':dict(kills),'hist_l':dict(hl),'hist_k':dict(hk)}}
    Path(__file__).with_name(f'wp19-{a.phase}-math-replay.json').write_text(json.dumps(out,indent=2)+'\n')
    print('PASS',a.phase,json.dumps(out['summary']),flush=True)


if __name__=='__main__':main()
