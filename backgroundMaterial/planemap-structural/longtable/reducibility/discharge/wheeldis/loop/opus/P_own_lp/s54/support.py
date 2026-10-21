# s54 support.py SOL OUT [tol=1e-7]: the nonzero features (|theta| > tol) of a lasso-path sol, per family, as a sup: model file
import sys, json, collections
S = json.load(open(sys.argv[1])); tol = float(sys.argv[3]) if len(sys.argv) > 3 else 1e-7
sup = collections.defaultdict(list); cnt = collections.Counter()
for fam, f, v in S['theta']:
    if abs(v) > tol: sup[fam].append(f); cnt[(fam, eval(f)[0])] += 1
for fam in S['pm']: sup.setdefault(fam, [])
json.dump(dict(sup), open(sys.argv[2], 'w'), indent=0)
print('support', sum(len(v) for v in sup.values()), dict(sorted(cnt.items())))
