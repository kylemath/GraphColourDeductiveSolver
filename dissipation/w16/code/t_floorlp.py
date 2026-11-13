import sys, json; sys.path.insert(0, '/tmp/swarm-W16/code')
import w16lib as W
ns = W.init()
C = json.load(open('/mnt/project-files/swarm/round6/W12-studio-K/from_opus/cert_floor_t0.json'))
labs = []
for e in C:
    r = e['row']
    if r[0] == 'senderR2':
        w = tuple(int(c) for c in r[1]); bits = r[2]; cut = bits.index('|'); six = [k for k in range(5) if w[k] == 6]
        F = [-1] * 5
        for k, b in zip(six, bits[cut + 1:]): F[k] = b
        labs.append(('S', w, tuple(bits[:cut]), tuple(F)))
    elif r[0] == 'receiverR2': labs.append(('R', r[1], tuple(int(c) for c in r[2]), tuple(int(c) for c in r[3])))
    elif r[0] == 'cons2': labs.append(('C', tuple(r[1]), tuple(r[2])))
print(labs)
for fam in ('base', 'rrz', 'all'):
    rows = W.build_lp(labs, fam); res, keys, rmap = W.solve_lp(rows)
    print(fam, 'rows', len(rows), 'vars', len(keys), 'status', res.status, 't', res.fun)
