# Key test: bicolour's L=13, k0=2 collar failure a=3210312031201, b=3023102301201 (w=1 fails, no bicoloured triple).
# Same height data = same seam rows (s_A, s_B).  Do the traces of (a, s_A) / (s_B, b) separate failing from passing (a', b')?
import sys, json, itertools, time
sys.path.insert(0, '/mnt/project-files/multiscale/kempe_trace'); sys.path.insert(0, '/mnt/project-files/multiscale/opus_attack/bandfill')
from kt import *; from t2_tubes import annulus
from tube import level_any, maxrun, stack, PERMS
L = 13; a = tuple(map(int, '3210312031201')); b = tuple(map(int, '3023102301201'))
def succ(r):   # all proper rows r' above r: r'(i) not in {r(i), r(i+1)}, cyclic proper
    out = []
    def rec(p):
        if len(p) == L:
            if p[-1] != p[0]: out.append(tuple(p))
            return
        i = len(p)
        for c in range(4):
            if c in (r[i], r[(i+1) % L]) or (p and c == p[-1]): continue
            rec(p+[c])
    rec([]); return out
def pred(r):   # rows r' below r: r(i) not in {r'(i), r'(i+1)}
    out = []
    def rec(p):
        if len(p) == L:
            if p[-1] != p[0] and all(r[i] not in (p[i], p[(i+1) % L]) for i in range(L)): out.append(tuple(p))
            return
        i = len(p)
        for c in range(4):
            if p and c == p[-1]: continue
            if c == r[i]: continue
            if i >= 1 and r[i-1] == c: continue
            rec(p+[c])
    rec([]); return out
cap = lambda r: maxrun(r) <= 2
SA = [s for s in succ(a) if cap(s) and level_any(s)]; SB = [s for s in pred(b) if cap(s) and level_any(s)]
print('capped level seam rows above a:', len(SA), ' below b:', len(SB))
sA, sB = SA[0], SB[0]
def sig(rows, seam_row):
    adj, col = annulus([''.join(map(str, r)) for r in rows]); n = len(col); bd = [seam_row*L + i for i in range(L)]
    tr = traces(adj, range(n), col, bd)
    return tuple((p, tuple((blk, len(blk) % 2) for blk in tr[p])) for p in PAIRS)
def fillable(a_, b_):
    return any(stack(a_, tuple(p[c] for c in b_), 2) for p in PERMS)
assert not fillable(a, b), 'the bicolour pair should fail at w=1'
Acand = [x for x in pred(sA) if cap(x)]; Bcand = [x for x in succ(sB) if cap(x)]
print('capped a\' with a\'->sA:', len(Acand), ' capped b\' with sB->b\':', len(Bcand))
t0 = time.time(); res = {}
sigA = {x: sig([x, sA], 1) for x in Acand}; sigB = {y: sig([sB, y], 0) for y in Bcand}
print('distinct trace signatures among a\':', len(set(sigA.values())), 'of', len(Acand), '; among b\':', len(set(sigB.values())), 'of', len(Bcand))
pairs = [(x, y) for x in Acand for y in Bcand]
import random; random.Random(1).shuffle(pairs); pairs = pairs[:4000]
fill = {pr: fillable(*pr) for pr in pairs}
print('pairs tested', len(pairs), 'failing', sum(1 for v in fill.values() if not v), f'({time.time()-t0:.0f}s)')
# does the pair of signatures determine fillability?
bysig = {}
for (x, y), f in fill.items(): bysig.setdefault((sigA[x], sigB[y]), set()).add(f)
mixed = sum(1 for v in bysig.values() if len(v) == 2)
print('signature pairs:', len(bysig), ' mixed (both pass and fail):', mixed)
# same-signature neighbours of the failing pair
same_a = [x for x in Acand if sigA[x] == sigA[a]]; same_b = [y for y in Bcand if sigB[y] == sigB[b]]
print('a\' with the same signature as a:', len(same_a), '-> rows', [''.join(map(str, x)) for x in same_a][:6])
print('b\' with the same signature as b:', len(same_b))
ff = [fillable(x, y) for x in same_a for y in same_b]
print('pairs with both signatures equal to the failing pair: ', len(ff), ' fillable:', sum(ff))
# weaker height-only grouping: how many (a',b') with these seam rows fail at all
print('failing fraction overall:', round(sum(1 for v in fill.values() if not v)/len(fill), 3))
print('signature of a on seam sA:'); [print('  ', p, bl) for p, bl in sigA[a]]
json.dump(dict(sA=''.join(map(str, sA)), sB=''.join(map(str, sB)), nA=len(Acand), nB=len(Bcand), distinctA=len(set(sigA.values())), distinctB=len(set(sigB.values())),
               pairs=len(pairs), failing=sum(1 for v in fill.values() if not v), sigpairs=len(bysig), mixed=mixed, same_a=len(same_a), same_b=len(same_b), same_sig_fillable=sum(ff), same_sig_total=len(ff)),
          open('t5_l13.json', 'w'), indent=1)
