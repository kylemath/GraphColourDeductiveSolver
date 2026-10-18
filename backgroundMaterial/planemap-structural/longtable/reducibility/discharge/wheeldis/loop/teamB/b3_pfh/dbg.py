import sys
sys.argv=['pfh.py','dex=8']
exec(open('pfh.py').read().split("if __name__ == '__main__':")[0])
rows=[]
for w, terms in S5: rows.append(([(-1, i) for i in terms], -1, -1))
seen=set()
for it in range(4):
    x,t,res=solve(rows)
    best=(-9,None,None)
    for v in V6:
        vv,tm=six_row(v,x)
        if tm is not None and vv>best[0]: best=(vv,tm,v)
    vv,tm,v=best
    key=('6',tuple(sorted(tm)))
    print(it,'t',t,'worst6',vv,v,'seen',key in seen)
    if key in seen:
        # evaluate the stored row at x
        tot=sum(sg*val(x,k) for sg,k in tm); print('row eval',tot, tm)
    for v in V6:
        vv,tm=six_row(v,x)
        if tm is not None and vv>t+1e-9:
            k2=('6',tuple(sorted(tm)))
            if k2 not in seen: seen.add(k2); rows.append(([(sg,var(k)) for sg,k in tm],-1,0))
