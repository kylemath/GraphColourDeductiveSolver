# usage: addforbid.py OLD CERT NEW ROUNDLABEL : NEW = OLD + every receiver row with nonzero dual in CERT
import json, sys
old, cert, new, lab = sys.argv[1:5]
txt = open(old).read(); have = set()
for line in txt.splitlines():
    f = line.split('#')[0].split()
    if f: have.add(tuple(f[:3]))
out = [txt.rstrip('\n')]; n = 0
for c in sorted(json.load(open(cert)), key=lambda c: c['w']):
    r = c['row']
    if r[0] == 'receiverR2' and abs(c['w']) > 1e-11 and (str(r[1]), r[2], r[3]) not in have:
        out.append('%d %s %s # w=%.6f %s' % (r[1], r[2], r[3], c['w'], lab)); have.add((str(r[1]), r[2], r[3])); n += 1
open(new, 'w').write('\n'.join(out) + '\n'); print('added', n, 'total', len(have))
