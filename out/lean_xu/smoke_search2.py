import glob, re, subprocess, itertools, sys
W='backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/'; T='/private/tmp/claude-501/-Users-kylemathewson-GraphColourDeductiveSolver--claude-worktrees-inspiring-lamport-831744/0e83ace3-9fad-4ff7-8f00-938be72dceb2/scratchpad/xu_smoke/'
ents=[l.split() for l in open('out/lean_cxint/95ba762d/entries.txt') if l.strip()]
names={e[2]:int(e[1]) for e in ents}
lines={}
for fn in glob.glob(W+'loop/k*/*.txt'):
    for l in open(fn,errors='ignore'):
        f=l.split()
        if len(f)==5 and f[0] in names and f[0] not in lines and f[1].isdigit(): lines[f[0]]=l.strip()
CF=W+'../studio15/cfast'; out=open(T+'found2.txt','a'); tested=0; nf=0
for nm,l in sorted(lines.items(), key=lambda x:(int(x[1].split()[1]), x[0])):
    _,r,m,ra,ia=l.split(); m=int(m)
    adj=[set() if g=='-' else {int(x) for x in g.split(',')} for g in ia.split(';')]
    tris=[(a,b,c) for a in range(m) for b in adj[a] for c in adj[a]&adj[b] if a<b<c]
    open(T+'cfg2.txt','w').write(l+'\n'); hit=False
    for (a,b,c) in tris:
        tri={(a,b),(a,c),(b,c)}
        ext=sorted({tuple(sorted((x,y))) for x in (a,b,c) for y in adj[x] if y not in (a,b,c)} | {tuple(sorted((x,y))) for x in range(m) for y in adj[x] if x<y and not ({x,y}&{a,b,c})})
        for e1,e2 in itertools.combinations(ext,2):
            X=sorted(tri|{e1,e2}); xs=','.join('I%d-I%d'%(p,q) for p,q in X)
            o=subprocess.run([CF,T+'cfg2.txt','--nogonthier','--fixed',xs],capture_output=True,text=True,timeout=600).stdout; tested+=1
            m2=re.search(r'fixed X=\{[^}]*\} \((\d+) edges\): (\S+), leftover bad classes extending after contraction = (-?\d+)',o)
            if m2 and m2.group(1)=='5' and m2.group(2)=='C-REDUCIBLE,':
                out.write('%s r=%s X=%s\n'%(nm,r,xs)); out.flush(); nf+=1; hit=True; break
        if hit: break
    print(nm, r, 'tested so far', tested, 'found', nf, flush=True)
    if nf>=3: break
