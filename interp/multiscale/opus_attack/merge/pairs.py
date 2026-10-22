# which pairs of renamings can be twisted simultaneously on ONE chordless level A against ONE level B?
import sys, itertools, json; sys.dont_write_bytecode=True
import exp2 as E, twist
from lat import PERMS
from mergecheck import pockets
from heights import ball_pts
g, A, B, U = E.rect(44,4,6,6)
PA=pockets(g,A); PB=pockets(g,B)
consA={x:set(ball_pts((0,0),1.0)) for W in PA for x in W['walk']}
consB={x:set(ball_pts((0,0),1.0)) for W in PB for x in W['walk']}
out=open(sys.argv[1],'w')
for p,q in itertools.combinations(PERMS,2):
    d,seq=E.design(g,A,B,U,4,1,[p,q],3)
    h,Ts=twist.build(g,A,B,consA,consB,d[0],cap=3)
    out.write(json.dumps(dict(p=p,q=q,ok=isinstance(h,dict)))+'\n'); out.flush()
