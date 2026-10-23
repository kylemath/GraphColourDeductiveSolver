import json, sys, math, collections
W3 = complex(-0.5, math.sqrt(3)/2)
cz = lambda p: p[0] + p[1]*W3
RS = ['0', '1', '2', '4', '8', '16', 'all']
def run(files, filt=lambda s: True):
    acc = collections.defaultdict(lambda: [0.0, 0.0, 0.0, 0, 0.0])   # sum dot, sum |D|^2, sum |f|^2, count, sum cos
    nst = 0
    for f in files:
        for l in open(f):
            r = json.loads(l)
            if 'flog' not in r or not filt(r['spec']): continue
            ev = [x for x in r['flog'] if x['eps'] == 1]
            for x, y in zip(ev, ev[1:]):
                D = cz(y['a']) - cz(x['a'])
                if abs(D) < 1e-9: continue
                nst += 1
                vecs = {'-t': -cz(x['a'])}
                for k in RS:
                    e, v = x['fr'][k]
                    if e == 1:
                        vecs['f_' + k] = cz(v); vecs['-(t+f)_' + k] = -(cz(x['a']) + cz(v))
                for k, F in vecs.items():
                    a = acc[k]; a[0] += (D * F.conjugate()).real; a[1] += abs(D)**2; a[2] += abs(F)**2; a[3] += 1
                    if abs(F) > 1e-9: a[4] += (D * F.conjugate()).real / abs(D) / abs(F)
    print('increments', nst)
    for k in ['-t'] + ['f_' + k for k in RS] + ['-(t+f)_' + k for k in RS]:
        if k not in acc: continue
        a = acc[k]; c = a[0] / math.sqrt(a[1] * a[2]) if a[2] > 0 else float('nan')
        print('%-12s n=%4d  vector-corr %+.3f  mean-cos %+.3f' % (k, a[3], c, a[4] / a[3]))
if __name__ == '__main__':
    import re
    pat = sys.argv[1]; run(sys.argv[2:], lambda s: re.search(pat, s) is not None)
