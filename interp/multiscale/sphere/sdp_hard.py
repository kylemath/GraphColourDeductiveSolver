import sys; exec(open('/tmp/claude-0/sph/sdp_ext.py').read().split("rows=[x for x")[0])
import csv,random
def propagate_ok(r,m,adj,rc):
    dom=[set(range(4))-{rc[u] for u in adj[r+j] if u<r} for j in range(m)]
    ch=True
    while ch:
        ch=False
        for j in range(m):
            if not dom[j]: return False
            if len(dom[j])==1:
                c=next(iter(dom[j]))
                for u in adj[r+j]:
                    if u>=r and c in dom[u-r]: dom[u-r].discard(c); ch=True
    return all(dom)
rows=[x for x in csv.DictReader(open('/mnt/project-files/explore/dataset/windows_judged.tsv'),delimiter='\t') if 9<=int(x['ring'])<=12 and int(x['m'])>=5]
random.Random(int(sys.argv[2])).shuffle(rows)
T2=[0,0,0,0]
for x in rows[:int(sys.argv[1])]:
    w=dict(r=int(x['ring']),m=int(x['m']),ra=x['ring_adj'],ia=x['int_adj']); r,m,adj=parse(w)
    hard=caught=fa=ext_tested=0
    for rc in ring_cols(r):
        if not propagate_ok(r,m,adj,rc): continue
        e=extends(r,m,adj,rc)
        if e:
            if ext_tested<20:
                ext_tested+=1; fa+= sdp_ok(r,m,adj,rc) is False
            continue
        hard+=1; caught+= sdp_ok(r,m,adj,rc) is False
    T2[0]+=hard;T2[1]+=caught;T2[2]+=fa;T2[3]+=ext_tested
    print(x['name'],'r',r,'m',m,'hard non-extending',hard,'SDP caught',caught,'| false alarms',fa,'of',ext_tested,'extending sampled',flush=True)
print('TOTAL hard %d caught %d false-alarm %d/%d'%tuple(T2))
