# Check one published colouring (fan-link.md): gyroelongated hexagonal dipyramid, hole U0.
import itertools
V=['N','S']+[f'U{i}' for i in range(6)]+[f'L{i}' for i in range(6)]
E=set()
def e(a,b): E.add(frozenset((a,b)))
for i in range(6):
    j=(i+1)%6
    e('N',f'U{i}'); e('S',f'L{i}'); e(f'U{i}',f'U{j}'); e(f'L{i}',f'L{j}')
    e(f'U{i}',f'L{i}'); e(f'U{i}',f'L{j}')
adj={v:{w for x in E if v in x for w in x if w!=v} for v in V}
assert len(E)==36 and all(len(adj[v])>=5 for v in V)
c={'N':1,'S':0,'U1':0,'U2':3,'U3':0,'U4':2,'U5':0,'L0':2,'L1':3,'L2':1,'L3':2,'L4':3,'L5':1}
def proper(c): return all(c[a]!=c[b] for a,b in map(tuple,E) if a in c and b in c)
assert proper(c)
hole='U0'
def linkcols(c,h): return {c[w] for w in adj[h]}
def swaps(c,h):
    out=[]
    for a,b in itertools.combinations(range(4),2):
        seen=set()
        for s in c:
            if c[s] in (a,b) and s not in seen:
                comp={s};st=[s]
                while st:
                    x=st.pop()
                    for y in adj[x]:
                        if y in c and c[y] in (a,b) and y not in comp: comp.add(y);st.append(y)
                seen|=comp
                d=dict(c)
                for x in comp: d[x]=b if c[x]==a else a
                out.append(d)
    return out
def slides(c,h):
    out=[]
    for u in adj[h]:
        if sum(c[w]==c[u] for w in adj[h])==1:
            d=dict(c); d[h]=c[u]; del d[u]; out.append((d,u))
    return out
print('link colours at U0:', [c[w] for w in ['U1','N','U5','L0','L1']])
print('fills at once:', len(linkcols(c,hole))<=3)
sw=[d for d in swaps(c,hole) if len(linkcols(d,hole))<=3]
print('single Kempe swaps that fill:', len(sw), 'of', len(swaps(c,hole)))
for d,u in slides(c,hole):
    assert proper(d)
    print('slide to',u,'link colours',sorted(linkcols(d,u)),'fills:',len(linkcols(d,u))<=3)
# two mixed moves
two=0
for d,h in [(x,hole) for x in swaps(c,hole)]+slides(c,hole):
    for d2,h2 in [(x,h) for x in swaps(d,h)]+slides(d,h):
        if len(linkcols(d2,h2))<=3: two+=1
print('two-move sequences that fill:', two)
