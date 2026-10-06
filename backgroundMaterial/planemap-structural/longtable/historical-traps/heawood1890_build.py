import itertools, collections, json
# Edges read by hand from MathWorld's drawing HeawoodOriginalGraph.svg (graph overlaid on Heawood 1890 Fig. 18).
E_ = """G1 B1;G1 Y1;G1 R2;G1 B5;G1 B3;G1 Y6
Y1 B1;Y1 R1;Y1 G3;Y1 B3
B1 R1;B1 G2;B1 R2
R1 G2;R1 Y2;R1 G3
G2 Y2;G2 R2;G2 B2
Y2 G3;Y2 B2;Y2 R3
G3 R3;G3 B3
R2 B2;R2 Y3;R2 B5
B2 R3;B2 Y3
R3 B3;R3 Y3;R3 V
B3 V;B3 R4;B3 Y6
Y3 V;Y3 B5;Y3 G4
V G4;V R4
R4 G4;R4 B4;R4 G5;R4 Y6
G4 B4;G4 R5;G4 Y4;G4 B5
B4 R5;B4 G5;B4 Y5
R5 Y4;R5 G6;R5 Y5
Y4 B5;Y4 G6;Y4 R6
G5 Y5;G5 B6;G5 Y6
B5 R6;B5 Y6
G6 Y5;G6 R6;G6 B6
Y5 B6
R6 B6;R6 Y6
B6 Y6"""
edges=set()
for line in E_.split('\n'):
    for p in line.split(';'):
        a,b=p.split(); edges.add(tuple(sorted((a,b))))
V=sorted({x for e in edges for x in e})
adj={x:set() for x in V}
for a,b in edges: adj[a].add(b); adj[b].add(a)
deg=collections.Counter(len(adj[x]) for x in V)
tri=[t for t in itertools.combinations(V,3) if t[1] in adj[t[0]] and t[2] in adj[t[0]] and t[2] in adj[t[1]]]
ec=collections.Counter(e for t in tri for e in itertools.combinations(t,2))
print('vertices',len(V),'edges',len(edges),'degrees',dict(deg),'3-cycles',len(tri),'edge-in-triangles',collections.Counter(ec[e] for e in edges))
col={x:(x[0].lower() if x!='V' else None) for x in V}
bad=[e for e in edges if col[e[0]] and col[e[0]]==col[e[1]]]
print('colouring proper (V uncoloured):',not bad, bad, 'link of V colours', sorted(col[x] for x in adj['V']))
# faces = triangles if 46 and each edge in 2
assert len(tri)==2*len(V)-4 and all(ec[e]==2 for e in edges)
# rotation from faces: orient consistently
faces=[list(t) for t in tri]
# orient: BFS flipping
oriented={}; f0=faces[0]; oriented[0]=f0
dire={}
def dedges(f): return [(f[i],f[(i+1)%3]) for i in range(3)]
for d in dedges(f0): dire[d]=0
queue=[0]; idx={tuple(sorted(f)):i for i,f in enumerate(faces)}
byedge=collections.defaultdict(list)
for i,f in enumerate(faces):
    for e in itertools.combinations(sorted(f),2): byedge[e].append(i)
while queue:
    i=queue.pop(); f=oriented[i]
    for a,b in dedges(f):
        for j in byedge[tuple(sorted((a,b)))]:
            if j in oriented: continue
            g=faces[j]; c=[x for x in g if x not in (a,b)][0]
            oriented[j]=[b,a,c]
            for d in dedges(oriented[j]):
                assert d not in dire, 'non-orientable?'
                dire[d]=j
            queue.append(j)
F=[oriented[i] for i in range(len(faces))]
# rotation: for each vertex, cycle neighbours via faces (x,a,b) -> a then b
rot={}
for x in V:
    nxt={}
    for f in F:
        if x in f:
            k=f.index(x); nxt[f[(k+1)%3]]=f[(k+2)%3]
    start=next(iter(nxt)); cyc=[start]
    while nxt[cyc[-1]]!=start: cyc.append(nxt[cyc[-1]])
    assert len(cyc)==len(adj[x]); rot[x]=cyc
print('Euler V-E+F =',len(V)-len(edges)+len(F))
json.dump({'vertices':V,'edges':sorted(edges),'faces':F,'rotation':rot,'colouring':col},open('heawood1890_core.json','w'))
