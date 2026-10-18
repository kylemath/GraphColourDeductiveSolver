"""Job 30 F: independent check of the deleted sender rows. For each deleted row, random full fillings of every second-
ring and private slot (5..9): each must contain a K on lettered vertices by networkx (tkill.embeds_nx), unless the
filling cannot occur (an R5 link 5-wheel or an R6 6-wheel). Usage: python3 checkdel.py KCFILE DELROWS [n=300]"""
import sys, os, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import tkill as TK
HERE = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
src = open(os.path.join(HERE, 'wlp.py')).read().replace('__file__', repr(os.path.join(HERE, 'wlp.py')))
sys.argv, ARGV = ['wlp'], sys.argv[1:]; exec(src[:src.index('# ---- option bigw')])
KS, _ = TK.load(ARGV[0]); N = int(next((a[2:] for a in ARGV if a.startswith('n=')), '300')); random.seed(9)
bad = ok = imp = 0
for line in open(ARGV[1]):
    f = line.split()
    if not f: continue
    w = tuple(int(c) for c in f[0]); fixed = {('t', int(x[1])): int(x.split('=')[1]) for x in f[1:]}
    nodes = TK.MODEL.setdefault(w, TK.model(w))[0]
    for _ in range(N):
        let = dict(fixed)
        for x in nodes:
            if x != 'v' and x[0] != 'a' and x not in let: let[x] = random.choice(TK.LET)
        fl = tuple(let.items())
        if TK.impossible(w, fl, isR5, isR6): imp += 1; continue
        if any(TK.embeds_nx(K, w, fl) for K in KS): ok += 1
        else: bad += 1; print('NOT KILLED', line.strip(), sorted(let.items(), key=str)); break
print('deleted rows checked: fillings %d contain a K (networkx), %d cannot occur, %d escape' % (ok, imp, bad))
