# W16: small label set = dual-support S/R rows of given families (from a world_lp json, top <= 40 covers support n <= 40)
#      + all senders + all cons2 of the world + extra pickles; for fast exact certificates.  usage: python3 -I support_pkl.py WORLD.pkl LP.json FAMS OUT.pkl [EXTRA.pkl ...]
import sys, pickle, json, collections
sys.path.insert(0, '/tmp/swarm-W16/code')
from lp_patterns import lab_str
labs = pickle.load(open(sys.argv[1], 'rb')); lp = json.load(open(sys.argv[2])); fams = sys.argv[3].split(','); out = sys.argv[4]
want = set()
for f in fams:
    d = lp[f].get('dual')
    if not d: continue
    assert d['n'] <= len(d['top']), (f, d['n'])
    want |= {k for _, k in d['top']}
keep = []; seen = set(); hit = set()
for l in labs:
    if l[0] in ('S', 'C') or (l[0] == 'R' and lab_str(l) in want):
        if l[0] == 'R': hit.add(lab_str(l))
        keep.append(l)
for e in sys.argv[5:]:
    for l in pickle.load(open(e, 'rb')):
        if l not in keep: keep.append(l)
miss = {k for k in want if k.startswith('R') and k not in hit}
print('support_pkl: wanted R %d, found %d, missing %s; total labels %d %s' % (len({k for k in want if k.startswith('R')}), len(hit), sorted(miss), len(keep), dict(collections.Counter(l[0] for l in keep))))
pickle.dump(keep, open(out, 'wb'))
