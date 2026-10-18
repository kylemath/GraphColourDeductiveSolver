import collections, os, sys
H=os.path.dirname(os.path.abspath(__file__))
new=collections.defaultdict(set)
for l in open(os.path.join(H,'pert_nosym.out')):
    f=l.split()
    if f[0]=='V':
        k=''.join(str(int(x)-5) for x in (f[2][0],f[3][0],f[2][1],f[3][1])); new[k].add((f[2],f[3]))
done=set(); bad=[]; nv=0
for l in open(os.path.join(H,'pref','summary.txt')):
    f=l.split()
    if f[1]!='rc=0' or f[0] in done: continue
    done.add(f[0]); old=set()
    for m in open(os.path.join(H,'pref',f[0]+'.out')):
        g=m.split()
        if g and g[0]=='V': old.add((g[2],g[3]))
    nv+=len(old)
    if old!=new[f[0]]: bad.append((f[0],len(old),len(new[f[0]])))
tot=sum(len(v) for v in new.values())
print('prefixes compared %d/625, violations matched %d (new total %d), mismatches %s'%(len(done),nv,tot,bad))
