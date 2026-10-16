"""summarise bf3_misses_3.txt: shapes of the k = 3 misses; write the configs still needing dfast (ring <= 15)."""
import collections, sys
cur=None; recs=[]
for l in open('bf3_misses_3.txt'):
    if l.startswith('MISS'):
        f=l.split(); cur=[f[1],f[2],[]]; recs.append(cur)
    else:
        f=l.split(); cur[2].append((int(f[0][2:]), int(f[1][4:]), f[2][2:], f[3], f[4], ' '.join(f[5:])))
def shape(L):
    F=[i for i in range(7) if L[i]=='5']
    return tuple(sorted([(F[(i+1)%3]-F[i])%7 for i in range(3)]))
st=collections.Counter(); need={}
for L,s,cs in recs:
    unt = any(v=='?' and r<=15 for r,k,S,v,ck,cb in cs)
    st[(shape(L), 'untested' if unt else 'noD')]+=1
    for r,k,S,v,ck,cb in cs:
        if v=='?' and r<=15: need[ck]=(r,cb)
for k,v in sorted(st.items()): print(k,v)
print('distinct untested configs ring<=15:', len(need), collections.Counter(r for r,cb in need.values()))
with open('k3_need.txt','w') as f:
    for ck,(r,cb) in sorted(need.items(), key=lambda x:x[1][0]): f.write('%s %s\n'%(ck,cb))
