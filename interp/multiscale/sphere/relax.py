import numpy as np, collections, sys
sys.path.insert(0,'/tmp/claude-0/ms'); exec(open('/tmp/claude-0/ms/vortex_spin.py').read().split('def colour')[0])
T=np.array([[1,1,1],[1,-1,-1],[-1,1,-1],[-1,-1,1]])/np.sqrt(3)
def relax(adj,seed,steps=3000,lr=0.05):
    rng=np.random.default_rng(seed); n=len(adj); U=rng.normal(size=(n,3)); U/=np.linalg.norm(U,axis=1)[:,None]
    E=np.array([(a,b) for a in range(n) for b in adj[a] if a<b])
    for t in range(steps):
        d=(U[E[:,0]]*U[E[:,1]]).sum(1)+1/3
        g=np.zeros_like(U); np.add.at(g,E[:,0],2*d[:,None]*U[E[:,1]]); np.add.at(g,E[:,1],2*d[:,None]*U[E[:,0]])
        g-= (g*U).sum(1)[:,None]*U
        U-=lr*g; U/=np.linalg.norm(U,axis=1)[:,None]
    d=(U[E[:,0]]*U[E[:,1]]).sum(1)+1/3
    # best global rotation to tetra: round by nearest corner after aligning with a random rotation search
    best=None
    for k in range(200):
        Q,_=np.linalg.qr(rng.normal(size=(3,3))); C=np.argmax(U@Q@T.T,axis=1)
        bad=int((C[E[:,0]]==C[E[:,1]]).sum())
        if best is None or bad<best[0]: best=(bad,C)
    return U,E,d,best
for name,(p,adj) in [('sphere2000',sphere(2000,0)),('sphere2000b',sphere(2000,1))]:
    deg=np.array([len(a) for a in adj])
    for seed in range(2):
        U,E,d,(bad,C)=relax(adj,seed)
        ve=np.zeros(len(adj)); np.add.at(ve,E[:,0],d**2); np.add.at(ve,E[:,1],d**2)
        bydeg={k:round(float(ve[deg==k].mean()),4) for k in sorted(set(deg)) if (deg==k).sum()>10}
        conf_v=collections.Counter(deg[v] for e in E[C[E[:,0]]==C[E[:,1]]] for v in e)
        print(name,seed,'energy %.3f'%float((d**2).sum()),'rounded conflicts',bad,'of',len(E),'| mean local strain by degree',bydeg,'| conflict endpoints by degree',dict(sorted(conf_v.items())),flush=True)
