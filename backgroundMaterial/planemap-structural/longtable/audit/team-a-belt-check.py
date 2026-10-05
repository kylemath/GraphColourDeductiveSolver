"""Independent constructive strategy regression, existing named belts only."""
import json
from collections import Counter
from pathlib import Path
from wp18_independent import deletion_starts

H=4
stats=Counter()

def adjacency(n):
    u=lambda i:2+i%n
    v=lambda i:2+n+i%n
    adj=[set() for _ in range(2+2*n)]
    def edge(x,y):adj[x].add(y);adj[y].add(x)
    for i in range(n):
        for x,y in [(0,u(i)),(1,v(i)),(u(i),u(i+1)),(v(i),v(i+1)),(u(i),v(i)),(u(i),v(i-1))]:edge(x,y)
    return [sorted(x) for x in adj]

class State:
    def __init__(self,n,s):
        self.n=n;self.c=list(s);self.adj=adjacency(n);self.names=list(range(len(s)));self.path=[]
    def u(self,i):return 2+i%self.n
    def v(self,i):return 2+self.n+i%self.n
    def hole(self):return self.c.index(H)
    def ok(self):
        assert self.c.count(H)==1
        assert all(self.c[x]!=self.c[y] for x,ne in enumerate(self.adj) for y in ne if self.c[x]!=H and self.c[y]!=H)
    def target(self):return len({self.c[x] for x in self.adj[self.hole()]})<=3
    def slide(self,d):
        h=self.hole();assert d in self.adj[h]
        assert sum(self.c[x]==self.c[d] for x in self.adj[h])==1
        self.path.append((self.names[h],self.names[d]))
        self.c[h],self.c[d]=self.c[d],H;self.ok()
    def permute(self,perm,colors=None):
        assert sorted(perm)==list(range(len(self.c)))
        assert all({perm[y] for y in self.adj[x]}==set(self.adj[perm[x]]) for x in range(len(perm)))
        self.c=[self.c[x] for x in perm];self.names=[self.names[x] for x in perm]
        if colors:self.c=[colors[x] if x!=H else H for x in self.c]
        self.ok()
    def reflect(self):
        self.permute([0,1]+[self.u(-i) for i in range(self.n)]+[self.v(-i-1) for i in range(self.n)])
    def normalize_hole(self):
        h=self.hole()
        if h>=2+self.n:
            k=h-2-self.n
            self.permute([1,0]+[self.v(k-i) for i in range(self.n)]+[self.u(k-i) for i in range(self.n)])
        else:
            k=h-2
            self.permute([0,1]+[self.u(k+i) for i in range(self.n)]+[self.v(k+i) for i in range(self.n)])
        a,b=self.c[:2];assert a!=b
        remain=sorted(set(range(4))-{a,b})
        self.permute(list(range(len(self.c))),{a:0,b:1,remain[0]:2,remain[1]:3})
        assert self.hole()==self.u(0)

def one(s):
    stats['D1']+=1
    i=0
    while not s.target():
        assert i<s.n-1
        assert s.hole()==s.u(i)
        assert s.c[s.u(i-1)]==s.c[s.u(i+1)]==1
        assert {s.c[s.v(i-1)],s.c[s.v(i)]}=={2,3}
        s.slide(s.v(i))
        if s.target():return
        assert i+2<s.n-1 # untouched fixed u_(n-1)=1 excludes last return
        assert s.c[s.v(i+1)]==0
        s.slide(s.v(i+1));s.slide(s.u(i+2));i+=2
        stats['D1_returns']+=1

def prepared(s,i,r):
    t=5-r
    old_i=i
    while not s.target():
        assert s.hole()==s.v(i)
        assert s.c[s.u(i+1)]==r and s.c[s.v(i+1)]==0
        assert i>=3 # P1 target; P2 improper in longcap
        if s.c[s.v(i-2)]==0:
            if s.c[s.v(i-1)]==t:
                assert s.c[s.u(i)]==1
                s.slide(s.v(i-1));s.slide(s.v(i-2));i-=2
                stats['A_tau_returns']+=1
            else:
                assert s.c[s.v(i-1)]==r and s.c[s.u(i)]==t
                s.slide(s.u(i));s.slide(s.u(i-1))
                if s.target():return
                s.slide(s.v(i-1));s.slide(s.v(i-2));i-=2
                stats['A_rho_returns']+=1
        else:
            assert s.c[s.v(i-3)]==0
            assert s.c[s.v(i-2)]==t and s.c[s.v(i-1)]==r
            s.slide(s.u(i));s.slide(s.u(i-1));s.slide(s.v(i-2));s.slide(s.v(i-3));i-=3
            stats['B_tau_returns']+=1
        assert i<old_i;old_i=i

def solve(s):
    if s.target():stats['initial_target']+=1;return
    s.normalize_hole()
    word=lambda:[s.c[x] for x in [0,s.u(1),s.v(0),s.v(-1),s.u(-1)]]
    w=word();double=next(x for x,num in Counter(w).items() if num==2)
    if double==1:return one(s)
    if s.c[s.u(1)]!=1:s.reflect()
    w=word();assert w[1]==1
    if double==0:
        if w[2]==0:
            stats['D0_A']+=1
            s.slide(s.v(-1));s.normalize_hole();return one(s)
        stats['D0_B']+=1
        assert w[3]==0
        r=w[2]
        s.slide(s.u(-1));s.slide(s.v(-2))
        if s.target():return
        assert s.c[s.v(-3)]==5-r
        s.slide(s.v(-3));s.slide(s.v(-4))
        return prepared(s,s.n-4,r)
    stats['tight_double']+=1
    r=w[2];assert w==[0,1,r,5-r,r]
    s.slide(s.v(-1));s.slide(s.v(-2));return prepared(s,s.n-2,r)

def main():
    results=[]
    for n in (5,8,11):
        adj=adjacency(n);total=unequal=0;maxlen=0;hist=Counter();witnesses=[]
        for start in deletion_starts(adj,2):
            total+=1
            if start[0]==start[1]:continue
            unequal+=1;s=State(n,start);s.ok();solve(s);assert s.target()
            # Replay the actual original labelled path independently.
            replay=list(start);initial_poles=replay[:2]
            for h,d in s.path:
                assert replay[h]==H and d in adj[h]
                assert sum(replay[x]==replay[d] for x in adj[h])==1
                replay[h],replay[d]=replay[d],H
                assert replay[:2]==initial_poles
                assert all(replay[x]!=replay[y] for x,ne in enumerate(adj) for y in ne if replay[x]!=H and replay[y]!=H)
            h=replay.index(H);missing=set(range(4))-{replay[x] for x in adj[h]};assert missing
            maxlen=max(maxlen,len(s.path));hist[len(s.path)]+=1
            witnesses.append({'start':list(start),'slides':s.path,'fill_vertex':h,'fill_colour':min(missing)})
        results.append({'ring_n':n,'deletion_orbits':total,'unequal_starts':unequal,'max_strategy_slides':maxlen,'strategy_slide_histogram':dict(sorted(hist.items())),'witnesses':witnesses})
        print({k:v for k,v in results[-1].items() if k!='witnesses'},flush=True)
    out={'scope':'Deterministic proof strategy regression only on previously named G5/G8/G11; no BFS or new graphs','results':results,'branch_counts':dict(stats)}
    Path(__file__).with_name('team-a-belt-check-results.json').write_text(json.dumps(out,indent=2)+'\n')
    print('ALL PASS',dict(stats))
if __name__=='__main__':main()
