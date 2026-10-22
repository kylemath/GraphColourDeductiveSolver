import json,collections,glob,os,sys
for f in sorted(glob.glob('/mnt/project-files/multiscale/binder_maps/runms_*.json')):
    st=json.load(open(f)); name=os.path.basename(f)[6:-5]
    tot=collections.Counter(); nb=collections.Counter(); far=collections.Counter(); byL=collections.defaultdict(collections.Counter); merges=0
    for s in st:
        for L,sz,nc,R,nf,b in s:
            merges+=1
            if nc==0: continue
            tot[R]+=1; (nb if b else far)[R]+=1; byL[L][R]+=1
    print('%-20s seeds %d merges %d conflicted %d R %s | nearBinder %s | other %s | maxR %d'%(name,len(st),merges,sum(tot.values()),dict(sorted(tot.items())),dict(sorted(nb.items())),dict(sorted(far.items())),max(tot)))
    print('    per level:',' '.join('L%d:%s'%(L,dict(sorted(c.items()))) for L,c in sorted(byL.items())))
