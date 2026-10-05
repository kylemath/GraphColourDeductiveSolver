"""Long Table replay of the audit's 21-vertex correction (5 October): two Kempe swaps, one
slide, fill. Uses wp18/wp18_check's graph checks only; colours are kept raw (no renaming)."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent / "wp18"))
from wp18_check import HOLE, check_graph, parse, proper  # noqa: E402

A = 'bcdef,aflghijkc,abkmd,acmnoe,adopqf,aeqlb,blrsh,bgsoi,bhotj,bituk,bjumc,bfqrg,ckund,dmuto,dntihspe,eosrq,eprlf,glqps,grpoh,ionuj,jtnmk'
rot = parse('21 ' + A)
check_graph(rot)
c = [0, HOLE, 1, 2, 1, 2, 0, 1, 2, 0, 3, 3, 0, 1, 0, 2, 0, 1, 3, 3, 2]
assert proper(rot, c)


def swap(c, s, a, b):
    comp, todo = {s}, [s]
    while todo:
        x = todo.pop()
        for y in rot[x]:
            if y not in comp and c[y] in (a, b):
                comp.add(y)
                todo.append(y)
    return [(b if c[x] == a else a) if x in comp else c[x] for x in range(len(c))], sorted(comp)


link = lambda c, h: [c[w] for w in rot[h]]  # noqa: E731
print("edges", sum(map(len, rot)) // 2, "faces", 2 - len(rot) + sum(map(len, rot)) // 2)
print("start link at 1", link(c, 1))
c1, k1 = swap(c, 0, 0, 3)
c2, k2 = swap(c1, 2, 0, 1)
print("swap (0,3) on", k1, "; swap (0,1) on", k2, "; link at 1", link(c2, 1))
assert len(set(link(c2, 1))) == 4 and link(c2, 1).count(c2[6]) == 1
c3 = list(c2); c3[1], c3[6] = c2[6], HOLE
assert proper(rot, c3)
free = sorted(set(range(4)) - set(link(c3, 6)))
print("slide 1 -> 6; link at 6", link(c3, 6), "; free colours", free)
c4 = list(c3); c4[6] = free[0]
assert proper(rot, c4) and HOLE not in c4
print("filled: proper 4-colouring of all 21 vertices after 2 swaps + 1 slide")
