"""Constructive candidate proof controller; existing named G5/G8/G11 checks only."""
import json
from collections import Counter
from pathlib import Path
from wp18_independent import deletion_starts

def graph(n):
    a,b=0,1; u=lambda i:2+i%n; v=lambda i:2+n+i%n
    adj=[set() for _ in range(2*n+2)]
    for i in range(n):
        for x,y in ((a,u(i)),(b,v(i)),(u(i),u(i+1)),(v(i),v(i+1)),(u(i),v(i)),(u(i),v(i-1))):
            adj[x].add(y);adj[y].add(x)
    return [sorted(x) for x in adj]

def solve(n,initial):
    adj=graph(n);s=list(initial);h=s.index(4);path=[]
    u=lambda i:2+i%n; v=lambda i:2+n+i%n
    def proper():
        assert s.count(4)==1
        assert s[0]==0 and s[1]==1
        assert all(s[x]==4 or s[y]==4 or s[x]!=s[y] for x in range(len(s)) for y in adj[x])
    def done():return len({s[x] for x in adj[h]})<=3
    def slide(w):
        nonlocal h
        assert w in adj[h] and sum(s[x]==s[w] for x in adj[h])==1,(n,h,w,s)
        s[h],s[w]=s[w],4;h=w;path.append(w);proper()
    proper()
    if done():return path
    # This named regression is at u0. Reorient reflection when needed, recording
    # the original-coordinate permutation so the emitted path remains replayable.
    perm=list(range(len(s)))
    def reflect():
        nonlocal s,h,perm
        p=[0,1]+[u(-i) for i in range(n)]+[v(-i-1) for i in range(n)]
        s=[s[p[j]] for j in range(len(s))];perm=[perm[p[j]] for j in range(len(s))]
        h=s.index(4)
    def move(w):
        slide(w);path[-1]=perm[w]
    def tight():
        nonlocal h
        i=h-2
        if s[u(i+1)]!=1: reflect();i=h-2
        rho=s[v(i)];tau=s[v(i-1)]
        assert [s[x] for x in (0,u(i+1),v(i),v(i-1),u(i-1))]==[0,1,rho,tau,rho]
        move(v(i-1));
        if done():return
        move(v(i-2))
        for _ in range(n):
            if done():return
            j=h-(2+n)
            assert s[u(j+1)]==rho and s[v(j+1)]==0
            x=s[v(j-1)]; y=s[u(j)]
            if x==tau:
                assert y==1
                move(v(j-1))
                if done():return
                move(v(j-2))
            else:
                assert x==rho and y==tau
                kind='A' if s[v(j-2)]==0 else 'B'
                move(u(j))
                if done():return
                move(u(j-1))
                if done():return
                if kind=='A':
                    move(v(j-1))
                    if done():return
                    move(v(j-2))
                else:
                    move(v(j-2))
                    if done():return
                    move(v(j-3))
        raise AssertionError('tight traversal failed termination')
    word=[s[x] for x in (0,u(1),v(0),v(-1),u(-1))]
    repeated=next(c for c,k in Counter(word).items() if k==2)
    case=f'doubled-{repeated}'
    if repeated==0:
        if s[v(0)]==0:reflect()
        rho=s[v(0)];tau=5-rho
        if s[u(1)]==1:
            if s[v(1)]==0:move(v(0))
            else:move(u(1));tight()
        else:
            assert s[u(1)]==tau and s[u(-1)]==1
            for _ in range(n):
                i=h-2;move(u(i+1))
                if done():break
                move(u(i+2))
                if done():break
            else:raise AssertionError('II failed termination')
    elif repeated==1:
        for _ in range(n):
            i=h-2;move(v(i))
            if done():break
            move(v(i+1))
            if done():break
            move(u(i+2))
            if done():break
        else:raise AssertionError('D1 failed termination')
    else:tight()
    assert done(),(case,n,s)
    # Independent original-coordinate path replay, with full-neighbour singleton checks.
    original=list(initial);oldhole=original.index(4)
    for w in path:
        assert w in adj[oldhole] and sum(original[x]==original[w] for x in adj[oldhole])==1
        original[oldhole],original[w]=original[w],4;oldhole=w
    assert len({original[x] for x in adj[oldhole]})<=3
    return path

def main():
    out={'scope':'existing named G5/G8/G11 unequal-pole upper-hole starts; no new belt orders','graphs':[]}
    for n in (5,8,11):
        adj=graph(n);hist=Counter();cases=Counter();certs=[]
        for start in deletion_starts(adj,2):
            if start[0]==start[1]:continue
            # Restricted-growth enumeration has a=0,b=1 on every unequal start.
            assert start[0]==0 and start[1]==1
            p=[start[x] for x in (0,3,2+n,2+n+n-1,2+n-1)]
            case='target' if len(set(p))<=3 else f'doubled-{next(c for c,k in Counter(p).items() if k==2)}'
            path=solve(n,start);hist[len(path)]+=1;cases[case]+=1
            certs.append({'start':list(start),'path':path})
        out['graphs'].append({'n':n,'starts':sum(hist.values()),'length_histogram':dict(sorted(hist.items())),'cases':dict(cases),'certificates':certs})
        print(n,sum(hist.values()),dict(sorted(hist.items())))
    (Path(__file__).parent/'team-b-belt-controller-results.json').write_text(json.dumps(out,indent=2)+'\n')
if __name__=='__main__':main()
