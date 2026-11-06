# s84: sign guard the audit found unchecked: q / q7 amounts must be >= 0 (a negative one would make a bonus negative,
# and prelay2.write_bonus drops v <= 0, so the leaf would under-count). Prints min over every numeric leaf of keys q, q7.
import json, sys
def leaves(x):
    if isinstance(x, dict):
        for v in x.values(): yield from leaves(v)
    elif isinstance(x, (list, tuple)):
        for v in x: yield from leaves(v)
    elif isinstance(x, (int, float)) and not isinstance(x, bool): yield x
for fn in sys.argv[1:]:
    d = json.load(open(fn)); out = []
    for k in ('q', 'q7', 'q7m'):
        vals = list(leaves(d.get(k, {})))
        out.append('%s n=%d min=%s' % (k, len(vals), ('%.3g' % min(vals)) if vals else '-'))
    bad = any(v < 0 for k in ('q', 'q7') for v in leaves(d.get(k, {})))
    print('%-60s t=%.9f %s %s' % (fn.split('/')[-1], d.get('t', float('nan')), ' '.join(out), 'NEGATIVE' if bad else 'ok'))
