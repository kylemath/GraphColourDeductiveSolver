import pickle, numpy as np, json, itertools, re, sys, collections
P = pickle.load(open('prov.pkl','rb')); cls = P['cls']
B='/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s60_f2b/'
keepC = {l.split()[0] for l in open('/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/keep95/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/studio/opus_check/f2b041/keep95p131/keep95p131_C.txt') if not l.startswith('#')}
def is_keep(n):
    c = cls[n]
    if c.endswith('D') or c == 'nl51': return True
    if c == 'rsstC': return n.split('_')[0].replace('rsst','rss') in {k.split('_')[0] for k in keepC} or n.split('_')[0] in {k.split('_')[0] for k in keepC}
    return n in keepC
print('keep size', sum(is_keep(n) for n in cls), 'of', len(cls), collections.Counter(cls[n] for n in cls if is_keep(n)))
def build(U, keepf):
    K = np.zeros((5,)*9, bool)
    for mk, ws in P['KTREC'][U]:
        if keepf and not any(keepf(n) for n in ws): continue
        K[np.ix_(*[[i for i in range(5) if (m>>i)&1] for m in mk])] = True
    return K
def pack(K):
    A = np.zeros((5,)*8, np.uint8)
    for b in range(5): A |= K[...,b].astype(np.uint8) << b
    return A
for U in (7,9):
    full = np.load(B+'tab/kill/kill6_U%d.npy'%U); kp = np.load(B+'tab_keep95p131/kill/kill6_U%d.npy'%U)
    Kf = pack(build(U, None)); Kk = pack(build(U, is_keep))
    print('U%d scratch-TierA vs outside tables: scratch-not-theirs %d theirs-not-scratch %d (theirs=base|TierA)'%(U,int(((Kf&~full)!=0).sum()), int(((full&~Kf)!=0).sum())))
    print('U%d keep rebuild vs tab_keep95p131: eq %s  rebuild-not-file %d file-not-rebuild %d'%(U,bool((Kk==kp).all()),int(((Kk&~kp)!=0).sum()),int(((kp&~Kk)!=0).sum())))
