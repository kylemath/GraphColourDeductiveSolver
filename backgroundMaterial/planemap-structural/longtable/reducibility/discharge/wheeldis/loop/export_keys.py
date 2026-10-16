"""EXPLORE round 4: export the receiver-centred (B free) keys at d = 7 that count as reducible in R_opt (dfast D, or a
cfast C-candidate), as 'lk sv' lines for bin/defectr2's in-DFS pruning.  Usage: python3 loop/export_keys.py OUT"""
import sys, os
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KEYS_OUT = sys.argv[1]
sys.argv = ['defect_check2.py', '/dev/null', '/dev/null']; __file__ = os.path.join(HERE, 'defect_check2.py')
src = open(__file__).read(); exec(src[:src.index("if __name__ == '__main__':")])
keys = set()
for k, v in TESTED.items():
    if isinstance(k, tuple) and k[0] == 7 and v == 'D': keys.add(k)
for k, v in CRES.items():
    if isinstance(k, tuple) and k[0] == 7 and v == 'C': keys.add(k)
with open(KEYS_OUT, "w") as f:
    for k in sorted(keys): f.write('%s %s\n' % (k[1], k[2]))
print(len(keys), 'keys;', sum(1 for k, v in TESTED.items() if isinstance(k, tuple) and k[0] == 7), 'd=7 keys tested')
