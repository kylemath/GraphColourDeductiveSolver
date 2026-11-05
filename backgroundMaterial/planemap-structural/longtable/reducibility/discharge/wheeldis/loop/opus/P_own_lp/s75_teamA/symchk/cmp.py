import sys
def canon(w, s):
    d = len(w); P = list(zip(w, s))
    return min(tuple(P[k:] + P[:k]) for k in range(d))
for d in sys.argv[1:]:
    res = {}
    for m in ('sym', 'nosym'):
        try: L = [l.split() for l in open('out%s_%s.txt' % (d, m)) if l.startswith('V ')]
        except FileNotFoundError: continue
        D = {}
        for _, tot, w, s in L: D.setdefault(canon(w, s), set()).add(round(float(tot), 9))
        end = [l for l in open('out%s_%s.txt' % (d, m)) if l.startswith('END')]
        clamp = [l.strip() for l in open('err%s_%s.txt' % (d, m)) if 'clamped' in l]
        res[m] = D; print('d=%s %s: %d rows, %d classes, totals consistent per class: %s, %s, %s' % (d, m, len(L), len(D), all(len(v) == 1 for v in D.values()), end[0].strip() if end else 'NO END', clamp))
    if len(res) == 2:
        a, b = set(res['sym']), set(res['nosym'])
        print('d=%s classes only in sym %d, only in nosym %d, totals equal on common: %s' % (d, len(a - b), len(b - a), all(res['sym'][k] == res['nosym'][k] for k in a & b)))
