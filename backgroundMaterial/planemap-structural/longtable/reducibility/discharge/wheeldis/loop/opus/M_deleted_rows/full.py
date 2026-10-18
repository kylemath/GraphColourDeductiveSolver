import sys; sys.argv=['mcheck']; exec(open('mcheck.py').read().split("if __name__ == '__main__':")[0])
R = rows(); D=set()
for l in open('deleted_rows.txt'):
    f=l.split(); D.add((tuple(map(int,f[0])), tuple(sorted(((('t',int(t[1])),int(t[3:])) for t in f[1:]),key=str))))
mine=set(); outright=0; fills=0
for r in R:
    nF,eK,e2,ex,us=check(r[0],dict(r[1]))
    if e2==0:
        mine.add(r); 
        if nF==1: outright+=1
        else: fills+=1
print('rows',len(R),'my deletions',len(mine),'outright',outright,'via fillings',fills)
print('mine-studio',[fmt(*x) for x in mine-D][:10],len(mine-D),' studio-mine',len(D-mine))
