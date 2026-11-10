# Is a receiver row killed on a W17 family (patterns D/C/RPAT/RPATN and the R5/R6/RBIG admissibility tables)?
# Runs W17's own st21_w17.py (code_gk7) up to and including admissible(); usage: python3 member.py POINT ARGS d LINK SWORD
import sys, os, time
pt, args, d, L, S = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4], sys.argv[5]
src = open('/tmp/swarm-W17/code_gk7/st21_w17.py').read()
cut = src.index('\n', src.index('    return not patmatch(d, w, s)')) + 1
sys.argv = ['st21_w17.py', pt, pt, args]; t0 = time.time()
g = {'__name__': 'member', '__file__': '/tmp/swarm-W17/code_gk7/st21_w17.py'}; exec(compile(src[:cut], 'st21_w17_head', 'exec'), g)
w = tuple(int(c) for c in L); s = tuple(int(c) for c in S)
print('row %d/%s/%s: patmatch %s, admissible %s (%.0fs)' % (d, L, S, g['patmatch'](d, w, s), g['admissible'](d, w, s), time.time() - t0))
