# ST fam-u check (Studio): W17's own st21_w17 head (code_gk7, up to admissible()) on the t and the u args; diff the pattern sets PAT[d]
# and test patmatch / admissible on the two P20 rows and nearby rows. usage: python3 pat_diff.py POINT ARGS_T ARGS_U EXP_T EXP_U
import sys, os
pt, at, au, et, eu = sys.argv[1:6]
src = open('/tmp/swarm-W17/code_gk7/st21_w17.py').read(); cut = src.index('\n', src.index('    return not patmatch(d, w, s)')) + 1
def load(args, exp):
    os.environ['EXPECT_PAT'] = exp; sys.argv = ['st21_w17.py', pt, pt, args]
    g = {'__name__': 'member', '__file__': '/tmp/swarm-W17/code_gk7/st21_w17.py'}; exec(compile(src[:cut], 'st21_w17_head', 'exec'), g); return g
T = load(at, et); U = load(au, eu)
print('KIND t', dict(T['KIND']), 'u', dict(U['KIND']))
for d in sorted(set(T['PAT']) | set(U['PAT'])):
    a, b = T['PAT'].get(d, set()), U['PAT'].get(d, set())
    if a != b: print('d=%d: u-t %d patterns, t-u %d' % (d, len(b - a), len(a - b)))
    for P in sorted(b - a, key=str): print('   new', sorted((k, i, tuple(sorted(S))) for k, i, S in P), 'slots', len(P), 'exact', all(len(S) == 1 for _, _, S in P))
rows = [(7, '8565766', '5557656'), (7, '8565766', '5557657'), (7, '8565766', '5557655'), (7, '8565766', '5557658'), (7, '8565766', '5557666'), (7, '6585676', '5655575')]
for d, L, S in rows:
    w = tuple(map(int, L)); s = tuple(map(int, S))
    print('row %d/%s/%s: t patmatch %s adm %s | u patmatch %s adm %s' % (d, L, S, T['patmatch'](d, w, s), T['admissible'](d, w, s), U['patmatch'](d, w, s), U['admissible'](d, w, s)))
