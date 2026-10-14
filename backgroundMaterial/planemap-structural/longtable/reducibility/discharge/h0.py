"""B8 (exploratory): test unavoidability of a reducible family R on scanned census graphs.
Families:
  W12  = the 12 D-reducible wheels (Studio Job 8)
  S66  = 66666 2-balls with every second-ring degree <= 6 (Job 9, 78/78 D-reducible)
  J9   = every D-reducible 66666 2-ball of Job 9 (ring <= 15)
  EXT  = extra D-reducible 2-ball keys from this folder (out/dres-*.txt, name = 'k' + keystr)
Usage: h0.py FAMILIES(comma) scan.jsonl.gz...   e.g. h0.py W12,S66 out/scan-*.jsonl.gz"""
import sys, gzip, json, glob, collections, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ball

W12 = {'55555', '55556', '55557', '55566', '55567', '55656', '55657', '56566', '56567', '55666', '56657', '56666'}


def load_j9():
    D = {}
    for line in gzip.open(os.path.join(HERE, '../wheels/studio/run9_results.txt.gz'), 'rt'):
        f = line.split()
        if len(f) > 6 and f[6].startswith('D='): D[f[0]] = f[6] == 'D=true'
    return D


def load_ext():
    D = {}
    for fn in glob.glob(os.path.join(HERE, 'out/dres-*.txt')):
        for line in open(fn):
            f = line.split()
            if len(f) > 6 and f[6].startswith('D='): D[f[0][1:]] = f[6] == 'D=true'
    return D


def make_pred(fams):
    j9 = load_j9() if 'J9' in fams else {}
    ext = load_ext() if 'EXT' in fams else {}
    def red(word, ks):
        if 'W12' in fams and word in W12: return 'W12'
        if ks is None: return None
        key = ball.key_from_str(ks)
        if word == '66666':
            if 'S66' in fams and all(d <= 6 for b in key for d in b[1] + (b[2],)): return 'S66'
            if 'J9' in fams and j9.get(ball.key_to_66666_name(key)): return 'J9'
        if 'EXT' in fams and ext.get(ks): return 'EXT'
        return None
    return red


if __name__ == '__main__':
    fams = set(sys.argv[1].split(','))
    red = make_pred(fams)
    per_n = collections.defaultdict(lambda: [0, 0]); smallest = None; status = collections.Counter()
    failing = []; via = collections.Counter()
    for fn in sys.argv[2:]:
        for line in gzip.open(fn, 'rt'):
            g = json.loads(line); hit = None
            for v, w, ks, st in g['h']:
                status[st] += 1
                r = red(w, ks)
                if r: via[r] += 1; hit = hit or r
            per_n[g['n']][0] += 1
            if not hit:
                per_n[g['n']][1] += 1; failing.append(g['g'])
                if smallest is None: smallest = g['g']
    print('families', sorted(fams))
    print('hole status', dict(status))
    print('reducible holes by family', dict(via))
    print('order  graphs  H-fails  frac')
    T = [0, 0]
    for n in sorted(per_n):
        a, b = per_n[n]; T[0] += a; T[1] += b
        print('%5d %7d %7d  %.4f' % (n, a, b, b / a))
    print('total %7d %7d  %.4f' % (T[0], T[1], T[1] / T[0]))
    print('first failing graph:', smallest)
    if len(sys.argv) and os.environ.get('FAILOUT'):
        open(os.environ['FAILOUT'], 'w').write('\n'.join(failing) + '\n')
