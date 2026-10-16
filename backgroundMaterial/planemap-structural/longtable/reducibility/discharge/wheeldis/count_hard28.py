"""Job 28: classify the receiver rows of an LP (allrows file) at degree D by what their B-fixed sender sets need:
killed (some S D/C), open (an untested S at ring <= 16), HARD16 (every ring <= 16 S tested neither, and some S at ring >= 17
untested), DEAD (no S at ring <= 16 at all; only ring >= 17).  Usage: python3 count_hard28.py ALLROWS D"""
import sys, os, re, collections
HERE = os.path.dirname(os.path.abspath(__file__))
ROWS, DD = sys.argv[1], int(sys.argv[2])
src = open(os.path.join(HERE, 'gen28.py')).read()
sys.argv = ['gen28.py', '/dev/null', '99', '/dev/null', 'all']
exec(src[:src.index('\narrs = []')])
st = collections.Counter(); ex = {}
for line in open(ROWS):
    m = re.search(r'receiver d=(\d+) link (\d+) s (\d+)', line)
    if not m or int(m.group(1)) != DD: continue
    d, lk, sv = int(m.group(1)), m.group(2), m.group(3)
    vs = variants(d, lk, sv)
    if any(DV.get(x[5]) == 'D' or CV.get(x[5]) == 'C' for x in vs): k = 'killed'
    elif any(x[0] <= 16 and (x[5] not in DV or (DV[x[5]] == 'notD' and x[5] not in CV)) for x in vs): k = 'open'
    elif any(x[0] <= 16 for x in vs): k = 'HARD16 (all ring<=16 S tested neither; ring>=17 left)'
    else: k = 'DEAD16 (no S at ring<=16)'
    st[k] += 1; ex.setdefault(k, (lk, sv, min(x[0] for x in vs) if vs else None))
print('d=%d rows' % DD, sum(st.values()), dict(st))
for k, v in ex.items(): print('  e.g.', k, 'link', v[0], 's', v[1], 'min ring', v[2])
