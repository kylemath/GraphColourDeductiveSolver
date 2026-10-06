"""nprove_verify23.py: independent verification of Case I x Case I on the order-23 discs of res_23.txt.
Order 23 is outside the order <= 17 brief; used only on the 14 given lines (a few ms each, 1 process)."""
import sys
from nprove_lib import *
fn = sys.argv[1]
for i, line in enumerate(l for l in open(fn) if 'DISC' in l):
    col, E = parse(line); x, adj = build(col, E)
    cert = certify(adj)
    c1p, c2p, K2, K0 = neighbours_cprime(adj, x, col + [0])
    a, d1 = case_cprime(adj, x, c1p); b, d2 = mirror_case(adj, x, c2p)
    print(i + 1, "sizes", tuple(col.count(k) for k in range(4)), "tri/min deg/sep3:", cert['links'], cert['euler'], cert['mindeg'], cert['sep_triangles'], "| c'", a, " c''", b, "| |K2|,|K0|", len(K2), len(K0))
