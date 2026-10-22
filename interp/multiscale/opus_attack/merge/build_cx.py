# Driver: python3 build_cx.py "__import__('order').SEL" k h M ms mb ell avoid out.pkl   (gap=1, one stretch pair per blob side, B pockets free)
import sys, pickle; sys.path.insert(0,'/mnt/project-files/multiscale/opus_attack/merge'); sys.dont_write_bytecode=True
import exp5
from lat import PERMS
P=list(PERMS)
sel = eval(sys.argv[1]); k,h,M,ms,mb,ell,avoid=[int(x) for x in sys.argv[2:9]]; out=sys.argv[9]
r=exp5.make(k,h,M,ms,mb,ell,1,avoid,sel,perrun=1,bfree=True)
print(sys.argv[1:], r.get('err') or (isinstance(r['h'],dict), r['centres']), round(r.get('sec',0)), flush=True)
if isinstance(r.get('h'),dict):
    pickle.dump(dict(pts=r['g'].pts, A=sorted(r['A']), B=sorted(r['B']), h=r['h'], Ts=r['Ts'], centres=r['centres'],
                     meta=r['meta'], params=r['params']), open(out, 'wb'))
