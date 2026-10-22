from lat import PERMS
P=list(PERMS)
pairs=[(P[2*i],P[2*i+1]) for i in range(12)]   # consecutive PERMS share the T class
pocket={}
for n,pr in zip(range(2,13), pairs[:11]): pocket[n]=pr
last=pairs[11]
runs=[('L',n) for n in range(13)]+[('R',n) for n in range(12,1,-1)]
sel=[]
for side,n in runs:
    if n in pocket: sel.append(pocket[n][0] if side=='L' else pocket[n][1])
    else: sel.append(last[0] if n==0 else last[1])
assert sorted(sel)==sorted(P)
SEL=sel
