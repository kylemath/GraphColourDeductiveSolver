"""s60_f2b: Studio-format l3q tables  ->  Opus DICT format (the format pcheck.py's l3qtab= / l3qtab8= read).
Studio file: JSON list of rows [c, ap, w2, w3, w4, o, mask]  (c = neighbour w_{i+sg}, ap = the apex of the 7 next to the private (a in the Opus key),
  w2..w4 = w_{i+2sg..i+4sg}, o = the other apex), 2 x 2 x 5^4 = 2500 rows per side, mask 5 bits over letters 5..9 (bit set = allowed).
Opus file: {"<sg> <c><w2><w3><w4> <ap><o>": [mask, {}]} with sg written %+d ("+1"/"-1"); pcheck reads only v[0].
usage: conv_tables.py to_opus STUDIO.json SG OUT.json | conv_tables.py to_studio OPUS.json OUT.json | conv_tables.py check OPUS_A.json OPUS_B.json"""
import sys, json
def to_opus(src, sg, out):
    S = json.load(open(src)); O = {}
    for c, ap, w2, w3, w4, o, m in S:
        k = '%+d %d%d%d%d %d%d' % (sg, c, w2, w3, w4, ap, o); assert k not in O; O[k] = [m, {}]
    assert len(O) == 2500, len(O); json.dump(O, open(out, 'w'))
def to_studio(src, out):
    O = json.load(open(src)); S = []
    for k, v in O.items():
        sg, wd, ao = k.split(); S.append([int(wd[0]), int(ao[0]), int(wd[1]), int(wd[2]), int(wd[3]), int(ao[1]), v[0]])
    json.dump(sorted(S), open(out, 'w'))
if __name__ == '__main__':
    c = sys.argv[1]
    if c == 'to_opus': to_opus(sys.argv[2], int(sys.argv[3]), sys.argv[4])
    elif c == 'to_studio': to_studio(sys.argv[2], sys.argv[3])
    elif c == 'check':
        A = json.load(open(sys.argv[2])); B = json.load(open(sys.argv[3])); print('keys equal', set(A) == set(B), 'mask differences', sum(1 for k in A if A[k][0] != B[k][0]), 'bits only in A', sum(1 for k in A if A[k][0] & ~B[k][0]), 'bits only in B', sum(1 for k in A if B[k][0] & ~A[k][0]))
