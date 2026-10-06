from chain import *
D_='/Users/fulkanjou/GraphColour/SolvingFrameworkPlan/docs/working/MathNDiscSearch/'
files=[('res2_24_p0.txt',9,1),('res2_24_p1.txt',3,1),('res2_24_p3.txt',4,0),('res2_24_p3.txt',5,0)]
for fn,k,mir in files:
    li=0
    for line in open(D_+fn):
        if 'DISC' not in line: continue
        li+=1
        if li!=k: continue
        l=line[line.index('DISC'):].strip()
        r=analyse(l,mir); seen=r['seen']; adj=r['adj'];x=r['x'];V=r['V'];Dp=r['Dp'];apex=r['apex']
        # walk from c0 via c1 (swap of the [alpha,gamma'] comp), print path with degree, good, pairinfo
        print(fn,k,mir,'class',r['size'])
        prev=None; cur=r['c0']; 
        for step in range(8):
            inf=r['info'][cur]
            nbs=neighbours(adj,x,seen[cur],Dp)
            print(' step',step,'dist',inf[2],'pairs(comps,cyc)',inf[0],'deg',inf[1],'good',inf[3],'ring',''.join(N[seen[cur][q]] for q in range(5)))
            nxt=[k2 for k2 in nbs if k2!=prev]
            if inf[1]!=2 or inf[3]: break
            if step==0:
                # choose A direction: swap of [alpha,gamma'] comp
                pass
            prev,cur=cur,nxt[0] if step>0 else nxt[0]
