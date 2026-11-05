"""s77: drop the wrong-sign float duals of an L cert (senderR2 w<0, receiverR2/mrow* w>0; HiGHS IPM+simplex noise, |w| <= 1e-7) so that lowerR2's
exact repair (cons2 / negative mrow weights pinned exactly) can run.  The kept weights are unchanged; lowerR2 then decides VALID/INVALID exactly.
usage: certclean.py IN.json OUT.json [maxdrop=1e-6]"""
import json, sys, collections
C = json.load(open(sys.argv[1])); mx = float(sys.argv[3]) if len(sys.argv) > 3 else 1e-6
out = []; drop = collections.Counter(); big = 0.0
for c in C:
    w = float(c['w']); k = c['row'][0]
    bad = (k == 'senderR2' and w < 0) or ((k == 'receiverR2' or k.startswith('mrow')) and w > 0)
    if bad:
        drop[k] += 1; big = max(big, abs(w))
        if abs(w) > mx: sys.exit('wrong-sign weight %g beyond maxdrop %g: %s' % (w, mx, c['row']))
        continue
    out.append(c)
json.dump(out, open(sys.argv[2], 'w'), indent=0)
print('kept %d of %d rows; dropped wrong-sign %s (largest |w| %.3g)' % (len(out), len(C), dict(drop), big))
