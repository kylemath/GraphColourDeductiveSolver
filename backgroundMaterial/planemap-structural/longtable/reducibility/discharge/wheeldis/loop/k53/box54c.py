"""EXPLORE round 54c: does anything reach 8666655/5677657's all->= 7 box one step wider?  Frame: cen54's slots with
the ring-3 neighbours of every s (J3S=0..6: 20 slots, 32 parts); the part with p11, p21, p31, p41 and the apex all
6-9.  Containment only (registry, then the 2026 set, round 54c's XREG file), no engine windows.  Counts the box
fillings: the 14 slots of round 54b at 7..9, the 6 new slots (next to s0, s1, s2) at 5..9; by registry alone and with
the 2026 set, and lists every minimal requirement that touches the box.
usage: python3 box54c.py TWOENG XREG"""
import sys, os, collections
TW, XREG = sys.argv[1], sys.argv[2]
sys.argv = ['cen54.py', '7', '8666655', '5677657']
os.environ.update({'J3S': '0,1,2,3,4,5,6', 'FOCUS': '3,6'})
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, H)
import cen54 as C, grow
from cen54 import F
OLD = {'p01', 'p02', 'p03', 'p11', 'p21', 'p31', 'p41', 'ts4/s5/s6', 'ts6', 'tp01/s6', 'tp31/s3', 'ts3', 'tp41/s3', 'tp41/s4'}
lab, EXp, SLp, LETp = [p for p in C.parts() if 'p11=5' not in p[0] and 'p21=5' not in p[0] and 'p31=5' not in p[0]
                       and 'p41=5' not in p[0] and 'ts4/s5/s6=5' not in p[0]][0]
NEW = [x for x in SLp if C.sname(x) not in OLD]
assert len(SLp) == 20 and len(NEW) == 6, (len(SLp), [C.sname(x) for x in NEW])
BOX = {x: ((5, 6, 7, 8, 9) if x in NEW else (7, 8, 9)) for x in SLp}
P, pa, pf = C.structure(EXp, SLp, LETp)
REG, miss = F.registry(os.path.join(TW, 'k3x_D.out'), os.path.join(TW, 'k3x_C.cfast'))
NL = [grow.kcline(l, 'xreg') for l in open(XREG) if l.strip()]
print('part %s: %d slots (new %s); box %d fillings; registry %d, 2026 set %d' % (lab, len(SLp), ' '.join(C.sname(x) for x in NEW),
      C.prod(len(BOX[x]) for x in SLp), len(REG), len(NL)), flush=True)
def reqs(confs):
    cyl = []; src = collections.defaultdict(set)
    for c in confs:
        for e in grow.embeddings(c, P, pa, pf, EXp):
            req = {v: c[3][u] for u, v in e if v not in EXp}
            if all(l in LETp[x] and l != 9 for x, l in req.items()):
                cyl.append(req); src[tuple(sorted(req.items(), key=repr))].add(c[0])
    return C.minimal(cyl), src
cr, sr = reqs(REG); cn, sn = reqs(NL); ca = C.minimal(cr + cn)
TOT = C.prod(len(BOX[x]) for x in SLp)
for nm, cy in (('registry', cr), ('2026 set', cn), ('both', ca)):
    n = C.count(cy, SLp, BOX)
    print('%s: %d minimal requirements; box covered %d of %d (%.4f%%)' % (nm, len(cy), n, TOT, 100.0 * n / TOT), flush=True)
for nm, cy, sr_ in (('registry', cr, sr), ('2026 set', cn, sn)):
    for c in cy:
        if all(v in BOX[x] for x, v in c.items()):
            print('  %s box hit: %s | %s' % (nm, ' '.join('%s=%d' % (C.sname(k), v) for k, v in sorted(c.items(), key=repr)),
                  ' '.join(sorted(sr_[tuple(sorted(c.items(), key=repr))])[:4])))
