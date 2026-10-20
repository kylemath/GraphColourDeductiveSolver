"""EXPLORE round 54c: our two engines on the 2026-set configurations the census needs (cen54 XOUT file).  Each kc
line goes through cen54.Engines (cen53's verdict rule: kc -C -s 60 -t TSEC; a kc D re-run on dfast, ring <= 16, or
dfast18; a kc C on cfast --fixed with kc's X), cache and outputs N54_kcc.out, _df.out, _cf.out, N54_res.txt.  Prints
one line per configuration and a tally; a configuration counts only with verdict D or C{X}.
usage: python3 nl54e.py KCFILE TSEC   (NW workers, default 3)"""
import sys, os, collections
from concurrent.futures import ThreadPoolExecutor
KC, TSEC = sys.argv[1], int(sys.argv[2])
sys.argv = ['cen54.py', '7', '8666655', '5677657']       # cen54 builds its frame at import; any row will do
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, H)
import cen54
eng = cen54.Engines(TSEC, 'N54')
L = [l.rstrip('\n') for l in open(KC) if l.strip()]
L.sort(key=lambda l: (int(l.split()[1]), l.split()[0]))   # smaller rings first
tally = collections.Counter()
with ThreadPoolExecutor(int(os.environ.get('NW', '3'))) as ex:
    for l, v in zip(L, ex.map(eng.verdict, L)):
        tally[v.split('{')[0]] += 1; print('%s ring %s %s' % (l.split()[0], l.split()[1], v), flush=True)
print('# %d configurations: %s' % (len(L), dict(tally)), flush=True)
