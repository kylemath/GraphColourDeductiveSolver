"""s80 Team E: compare two rowdump outputs (A.jsonl B.jsonl) row by row: identical coefficient lists?  With f2bx dumps also
summarise cf vs cf0 (rows changed by the extra rules) and the value drop val0 - val.
usage: python3 rowcmp.py A.jsonl [B.jsonl]"""
import sys, json, collections
A = [json.loads(l) for l in open(sys.argv[1])]
if len(sys.argv) > 2:
    Bx = [json.loads(l) for l in open(sys.argv[2])]; assert len(A) == len(Bx)
    nd = 0; nv = 0; mv = 0.0; byd = collections.Counter()
    for a, b in zip(A, Bx):
        assert a['row'] == b['row']; byd[a['row'][0]] += 1
        if a['cf'] != b['cf']:
            nd += 1
            if nd <= 5: print('DIFF', a['row'])
        if 'val' in a and 'val' in b: mv = max(mv, abs(a['val'] - b['val']))
    print('rows %d (by d %s): coefficient lists differ on %d; max |value diff| %.3g' % (len(A), dict(sorted(byd.items())), nd, mv))
else:
    ch = [a for a in A if 'cf0' in a and a['cf'] != a['cf0']]
    print('rows %d: %d change with the extra rules' % (len(A), len(ch)))
    ch.sort(key=lambda a: -(a.get('val0', 0) - a.get('val', 0)))
    for a in ch[:40]:
        c0 = dict((k, v) for k, v in a['cf0']); c1 = dict((k, v) for k, v in a['cf'])
        dk = sorted((k, c1.get(k, 0) - c0.get(k, 0)) for k in set(c0) | set(c1) if c1.get(k, 0) != c0.get(k, 0))
        print('  %s/%s d=%d  value %.6f -> %.6f (drop %.6f)  %s' % (a['row'][1], a['row'][2], a['row'][0], a.get('val0', float('nan')), a.get('val', float('nan')), a.get('val0', 0) - a.get('val', 0), dk))
