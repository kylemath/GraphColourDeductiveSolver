"""Independent constructive replay on the already studied G5, G8 and G11.

No shortest-path search, producer imports, new order or new census. Every move
is checked on the full graph. Symmetries relabel vertices and colours only.
"""
import hashlib
import json
from collections import Counter
from pathlib import Path
from wp18_independent import deletion_starts, parse_graph, state_ok, target


def graph(n):
    u=lambda i: 2+i%n
    v=lambda i: 2+n+i%n
    faces=[]
    for i in range(n):
        faces.extend([(0,u(i),u(i+1)),(1,v(i+1),v(i)),
                      (u(i),v(i-1),v(i)),(u(i),v(i),u(i+1))])
    succ=[{} for _ in range(2+2*n)]
    for x,y,z in faces:
        for a,b,c in ((x,y,z),(y,z,x),(z,x,y)):
            assert a not in succ[b] or succ[b][a]==c
            succ[b][a]=c
    rot=[]
    for row in succ:
        start=min(row); ns=[start]; nxt=row[start]
        while nxt!=start:
            ns.append(nxt); nxt=row[nxt]
        assert len(ns)==len(row)
        rot.append(ns)
    ascii_=str(len(rot))+' '+','.join(''.join(chr(97+w) for w in row) for row in rot)
    assert parse_graph(ascii_)==rot
    return rot,ascii_


class Strategy:
    def __init__(self,n,rot,start):
        self.n=n; self.rot=rot; self.s=list(start)
        self.vertex_map=list(range(len(start)))
        self.path=[]; self.phases=[]
        self.poles=tuple(start[:2])

    def u(self,i): return 2+i%self.n
    def v(self,i): return 2+self.n+i%self.n
    def done(self): return target(self.rot,self.s)

    def slide(self,w):
        h=self.s.index(4)
        assert w in self.rot[h]
        assert sum(self.s[x]==self.s[w] for x in self.rot[h])==1
        self.s[h],self.s[w]=self.s[w],4
        self.path.append(self.vertex_map[w])
        state_ok(self.rot,self.s,w)
        assert tuple(self.s[:2])==self.poles

    def reindex(self,shift=0,reflect=False):
        # New u_i=old u_(shift +/- i), new v_i=old v_(shift+i)
        # in the forward case, old v_(shift-i-1) under reflection.
        perm=[0,1]
        perm += [self.u(shift-i if reflect else shift+i) for i in range(self.n)]
        perm += [self.v(shift-i-1 if reflect else shift+i) for i in range(self.n)]
        assert all({perm[w] for w in self.rot[x]}==set(self.rot[perm[x]])
                   for x in range(len(perm)))
        self.s=[self.s[w] for w in perm]
        self.vertex_map=[self.vertex_map[w] for w in perm]

    def link(self):
        assert self.s[self.u(0)]==4
        return [self.s[x] for x in (0,self.u(1),self.v(0),self.v(-1),self.u(-1))]

    def run(self):
        if self.done(): return 'already'
        assert self.s[:2]==[0,1] and self.s[self.u(0)]==4
        doubled=next(c for c,k in Counter(self.link()).items() if k==2)
        if doubled==0:
            if self.s[self.v(0)]==0: self.reindex(reflect=True)
            assert self.s[self.v(-1)]==0
            if self.s[self.u(1)]==1:
                self.phases.append('D0-I')
                if self.s[self.v(1)]==0:
                    self.slide(self.v(0)); assert self.done(); return 'D0-I'
                self.slide(self.u(1))
                if self.done(): return 'D0-I'
                self.reindex(shift=1)
                self.tight()
                return 'D0-I'
            self.phases.append('D0-II')
            assert self.s[self.u(-1)]==1
            i=0
            while not self.done():
                assert i<self.n-1, 'D0-II reached cap without filling'
                self.slide(self.u(i+1))
                if self.done(): break
                self.slide(self.u(i+2)); i+=2
            return 'D0-II'
        if doubled==1:
            self.phases.append('D1')
            i=0
            while not self.done():
                assert i<self.n-1, 'D1 reached cap without filling'
                self.slide(self.v(i))
                if self.done(): break
                self.slide(self.v(i+1))
                if self.done(): break
                self.slide(self.u(i+2)); i+=2
            return 'D1'
        self.tight()
        return 'tight'

    def tight(self):
        if self.s[self.u(1)]!=1: self.reindex(reflect=True)
        p=self.link(); rho=p[2]; tau=p[3]
        assert p==[0,1,rho,tau,rho] and {rho,tau}=={2,3}
        self.phases.append('prepared')
        self.slide(self.v(-1))
        if self.done(): return
        self.slide(self.v(-2))
        i=self.n-2
        last=i
        # Consume the next local gap. The final cap uses the same displayed
        # singleton moves; stop immediately at the first three-colour link.
        while not self.done():
            assert 0<i<=last, 'prepared walk crossed its cap'
            last=i
            if self.s[self.v(i-1)]==tau:
                self.slide(self.v(i-1))
                if self.done(): break
                self.slide(self.v(i-2)); i-=2
            else:
                assert self.s[self.v(i-1)]==rho
                self.slide(self.u(i))
                if self.done(): break
                self.slide(self.u(i-1))
                if self.done(): break
                # A_rho has the previous lower vertex zero. Otherwise B_tau
                # has the previous lower vertex tau and the far vertex zero.
                if self.s[self.v(i-2)]==0:
                    self.slide(self.v(i-1))
                    if self.done(): break
                    self.slide(self.v(i-2)); i-=2
                else:
                    assert self.s[self.v(i-2)]==tau
                    self.slide(self.v(i-2))
                    if self.done(): break
                    self.slide(self.v(i-3)); i-=3
        assert self.done()


def verify(n):
    rot,ascii_=graph(n)
    starts=deletion_starts(rot,2)
    counts=Counter(); lengths=Counter(); certificates=[]
    for start in starts:
        if start[0]==start[1]: continue
        runner=Strategy(n,rot,start)
        case=runner.run()
        assert len(runner.path)<=2*n, 'joined proof slide bound exceeded'
        # Replay the returned vertex certificate directly on the original,
        # untransformed state. This checks all reindexing and orientation use.
        s=list(start)
        for w in runner.path:
            h=s.index(4)
            assert w in rot[h] and sum(s[x]==s[w] for x in rot[h])==1
            s[h],s[w]=s[w],4
            state_ok(rot,s,w)
            assert s[:2]==[0,1]
        assert target(rot,s)
        missing=min(set(range(4))-{s[w] for w in rot[s.index(4)]})
        h=s.index(4); s[h]=missing
        assert all(s[x]!=s[y] for x,row in enumerate(rot) for y in row)
        counts[case]+=1; lengths[str(len(runner.path))]+=1
        certificates.append({'start':list(start),'case':case,'slides':runner.path,
                             'fill_vertex':h,'fill_colour':missing})
    return {'n':n,'scope':'replay on an already studied named belt',
            'rotation':ascii_,'all_deletion_orbits':len(starts),
            'unequal_starts':sum(counts.values()),'opening_counts':dict(counts),
            'strategy_length_histogram':dict(lengths),'certificates':certificates}


if __name__=='__main__':
    rows=[]
    for n in (5,8,11):
        row=verify(n); rows.append(row)
        print('PASS',n,row['unequal_starts'],row['opening_counts'],row['strategy_length_histogram'])
    out={'scope':'independent constructive strategy replay on G5/G8/G11 only',
         'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
         'graphs':rows}
    Path(__file__).with_name('belt-strategy-replay-results.json').write_text(json.dumps(out,indent=2)+'\n')
