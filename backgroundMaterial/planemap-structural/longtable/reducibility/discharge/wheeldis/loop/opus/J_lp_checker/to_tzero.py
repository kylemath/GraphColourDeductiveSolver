"""Validation helper: turn a y-only solution JSON into rule-T format with T = 0 and Y[r, fa, fe] = y[r] for every flag
(so jcheck's T code path must give exactly the same verdict as the y path).  Usage: python3 to_tzero.py IN OUT"""
import sys, json, itertools
S = json.load(open(sys.argv[1])); yT = {}
for k, v in S['y'].items():
    u, rest = k.split('|'); r = u + rest
    for fa, fe in itertools.product((0, 1), repeat=2):
        if (fa and r[1] != '6') or (fe and r[4] != '6'): continue
        yT['%s|%d%d' % (r, fa, fe)] = v
json.dump({'t': S['t'], 'z9': 0.0, 'x': {}, 'yT': yT, 'tau': {}}, open(sys.argv[2], 'w'))
