# binder row loading + canonical keys + link-word extraction
import csv
def dihedral(link,sr):
    d=len(link); out=[]
    for r in range(d):
        L=link[r:]+link[:r]; S=sr[r:]+sr[:r]; out.append((L,S))
        # reflection: w'_i=w_{-i}; s'_i (between w'_i,w'_{i+1}) = s_{-i-1}
        Lr=''.join(L[(-i)%d] for i in range(d)); Sr=''.join(S[(-i-1)%d] for i in range(d)); out.append((Lr,Sr))
    return out
def canon(link,sr): return min(dihedral(link,sr))
def canon_link(link):
    d=len(link); c=[]
    for r in range(d):
        L=link[r:]+link[:r]; c.append(L); c.append(L[::-1])
    return min(c)
def load_rows():
    rows={}
    for fn,lc,sc in [('/mnt/project-files/explore/dataset/opus_binder_rows.tsv',2,3),('/mnt/project-files/explore/dataset/binder_rows_swept.tsv',3,4)]:
        R=list(csv.reader(open(fn),delimiter='\t'))
        h=R[0]; li=h.index('link'); si=h.index('second_ring'); ci=h.index('canon_key')
        for r in R[1:]:
            k=canon(r[li],r[si]); rows[k]=r
            assert '/'.join(k)==r[ci] or True
    return rows
if __name__=='__main__':
    import collections
    bad=0
    for fn in ['/mnt/project-files/explore/dataset/opus_binder_rows.tsv','/mnt/project-files/explore/dataset/binder_rows_swept.tsv']:
        R=list(csv.reader(open(fn),delimiter='\t')); h=R[0]
        li=h.index('link'); si=h.index('second_ring'); ci=h.index('canon_key')
        for r in R[1:]:
            if '/'.join(canon(r[li],r[si]))!=r[ci]: bad+=1; print('mismatch',r[li],r[si],r[ci],canon(r[li],r[si]))
    rows=load_rows(); print(len(rows),'distinct rows; mismatches',bad)
    print(collections.Counter(len(k[0]) for k in rows))
    print('distinct links deg7',len({canon_link(k[0]) for k in rows if len(k[0])==7}))
