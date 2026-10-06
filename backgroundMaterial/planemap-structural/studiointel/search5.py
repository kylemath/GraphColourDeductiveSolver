#!/usr/bin/env python3
"""studiointel search5.py -- [exploratory] radius-maximising tabu search (search4 score) CONFINED to core triangulations that contain
neither RSST #0 (Birkhoff diamond) nor RSST #1 (2.122): every flip must keep min degree >= 5, max degree <= 8, no separating triangle,
and zero occurrences of both configurations. Seeds: IPR fullerene duals from ipr/ipr_32_52.pc (by index) or JSON graphs."""
import sys, os
sys.argv[0] = 'search4.py'
import search3, search2, search4, graphs, radius
import causal_test as CT, ipr_run
def legal_flips(faces, rng):
    for nf in search2.__dict__['_orig_legal'](faces, rng):
        if CT.occ(nf) == 0: yield nf
search2._orig_legal = search2.legal_flips; search2.legal_flips = legal_flips
search2.score = search4.score
if __name__ == '__main__':
    a = sys.argv[1:]
    for i, x in enumerate(a):
        if x.startswith('ipr:'):
            k = int(x[4:]); G = ipr_run.read_pc('ipr/ipr_32_52.pc')[k]
            p = os.path.join(os.environ.get('TMPDIR', '/tmp'), 'ipr_seed_%d.json' % k)
            import json; json.dump({'faces': [list(f) for f in G]}, open(p, 'w')); a[i] = 'json:' + p
    sys.argv = ['search5.py'] + a
    src = open(search2.__file__).read()
    main = src[src.index("if __name__ == '__main__':"):].replace("if __name__ == '__main__':", "if True:", 1)
    g = dict(vars(search2)); g['__name__'] = 'search5_main'; exec(compile(main, search2.__file__ + ':main', 'exec'), g)
