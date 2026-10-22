# Control map: same constraints as build.py (deg 5..8, no separating triangle, no chordless 4-cycle) but random flips, no binder steering
import sys,random,collections,pickle
sys.path.insert(0,'/mnt/project-files/multiscale/binder_maps')
import build
CAP=int(sys.argv[5]) if len(sys.argv)>5 else 8; f=int(sys.argv[1]); nfl=int(sys.argv[2]); rng=random.Random(int(sys.argv[3])); name=sys.argv[4]
adj=build.icosphere(f); n=len(adj); done=0
while done<nfl:
    a=rng.randrange(n); b=rng.choice(tuple(adj[a])); c,d=adj[a]&adj[b]
    if len(adj[a])<=5 or len(adj[b])<=5 or len(adj[c])>=CAP or len(adj[d])>=CAP or adj[c]&adj[d]!={a,b}: continue
    if any(y in adj[c] and y not in adj[d] and y!=d for x in adj[d] if x not in (a,b) and x not in adj[c] for y in adj[x]): continue
    adj[a].discard(b); adj[b].discard(a); adj[c].add(d); adj[d].add(c); done+=1
deg,full,lo=build.census(adj); print(name,'deg',sorted(deg.items()),'fullmatch',len(full),'linkonly',len(lo),'checks',build.sep_checks(adj))
pickle.dump(adj,open('/mnt/project-files/multiscale/binder_maps/%s.pkl'%name,'wb'))
