import json,subprocess,sys,os,re,time
B='/tmp/swarm-A3/bin/'
lo,hi,budget,to=int(sys.argv[1]),int(sys.argv[2]),float(sys.argv[3]),int(sys.argv[4])  # queue slice, wall budget s, per-window timeout
q=json.load(open('queue.json'))
done=set()
if os.path.exists('res.jsonl'):
    for l in open('res.jsonl'): done.add(json.loads(l)['nm'])
t0=time.time()
def run(cmd,inp,t):
    return subprocess.run(['nice','-n','10']+cmd,input=inp,capture_output=True,text=True,timeout=t).stdout
R=open('res.jsonl','a')
for nm,line,rs,ring in q[lo:hi]:
    if nm in done: continue
    if time.time()-t0>budget: break
    s=time.time(); rec={'nm':nm,'ring':ring,'row':min(rs),'rows':rs}
    try:
        o=run([B+'kc','-C'],line+'\n',to)
        rec['D']='D=true' in o.split('\n')[0]; rec['C']='C-REDUCIBLE' in o or 'C=true' in o
        m=re.search(r'leftover (\d+)',o); rec['left']=int(m.group(1)) if m else None
        if rec['D']: rec['dfast']=run([B+'dfast','/dev/stdin'],line+'\n',to)[:300]
        if rec['C']:
            mm=re.search(r'X=\{([^}]*)\}',o) or re.search(r'X=(\S+)',o)
            open('one.txt','w').write(line+'\n'); rec['kc']=o[:400]
            rec['cfast']=run([B+'cfast','one.txt','--fixed',mm.group(1)],'',to)[:300]
    except subprocess.TimeoutExpired:
        rec['timeout']=True
    rec['t']=round(time.time()-s,1)
    R.write(json.dumps(rec)+'\n'); R.flush()
