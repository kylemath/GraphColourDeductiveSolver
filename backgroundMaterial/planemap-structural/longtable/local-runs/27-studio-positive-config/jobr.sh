#!/bin/bash
# Job R: order-27 versions of the Job I/K/L/M/N/O/P/Q summaries, from out/r27.jsonl and out/r27m.jsonl, in jobr27/
cd "$(dirname "$0")"; mkdir -p jobr27; D=$(pwd)
python3 - <<'PY'
import json
def ex(key, fields, fn, filt=None, runmap=None):
    with open('jobr27/' + fn, 'w') as o:
        for lab, f in (('27', 'out/r27.jsonl'), ('27m', 'out/r27m.jsonl')):
            for l in open(f):
                if '"%s": ' % key not in l: continue
                r = json.loads(l)
                if key not in r or not r[key] or (filt and not filt(r)): continue
                o.write(json.dumps(dict(run=runmap + lab, **{k: r[k] for k in fields})) + '\n')
ex('jobg', ('name', 'hole', 'linkdeg', 'pattern', 'states', 'npos', 'jobg'), 'jobi-cycles.jsonl', runmap='i')
ex('jobk_pos', ('name', 'hole', 'linkdeg', 'pattern', 'states', 'npos', 'jobk_pos', 'lemmaR', 'lemmaR_bad'), 'jobk-records.jsonl', runmap='k')
ex('jobm', ('name', 'hole', 'linkdeg', 'pattern', 'jobm'), 'jobm-gamma-sequences.jsonl', runmap='m')
ex('jobn', ('name', 'hole', 'linkdeg', 'pattern', 'jobn'), 'jobn-visits.jsonl', runmap='n')
ex('jobo', ('name', 'hole', 'linkdeg', 'pattern', 'jobo'), 'jobo-steps.jsonl', filt=lambda r: r['jobo']['cycles'], runmap='o')
ex('jobp', ('name', 'hole', 'linkdeg', 'pattern', 'jobp'), 'jobp-steps.jsonl', filt=lambda r: r['jobp']['cycles'], runmap='pp')
ex('jobq', ('name', 'hole', 'linkdeg', 'pattern', 'jobq'), 'jobq-steps.jsonl', filt=lambda r: r['pattern'] == '5,5,5,5,6', runmap='q')
PY
cd jobr27
for s in jobl jobm jobn jobo jobp jobq; do echo "##### $s"; python3 $D/$s.py; done > jobr27-summary.txt 2>&1
python3 - <<'PY' >> jobr27-summary.txt
import json
from collections import Counter
# A34': at each of k = 3, 4, at most L/20 failing R3 visits per Gamma-cycle; Lemma R from jobk records
bad = []; n = 0
for l in open('jobn-visits.jsonl'):
    r = json.loads(l)
    for cyc in r['jobn']:
        n += 1; L = 5 * len(cyc)   # visits at k=3,4 are L/10 each -> 2L/10 rows
        for k in (3, 4):
            nf = sum(1 for x in cyc if x[1] == k and not x[2])
            if nf > L / 20: bad.append((r['run'], r['name'], r['hole'], 'k', k, 'fails', nf, 'L', L))
print("##### A34' (<= L/20 failing visits at each of k=3,4): cycles %d, violations %d %s" % (n, len(bad), bad[:3]))
rb = []; tg = 0
for l in open('jobk-records.jsonl'):
    r = json.loads(l)
    for w, L, nh, hs, rem in r['lemmaR']:
        tg += 1
        if w <= 0 and rem > 0: rb.append((r['run'], r['name'], r['hole'], w, L, nh, rem))
print('##### Lemma R on nonpositive targets (Job K form): targets %d, violations %d %s' % (tg, len(rb), rb[:3]))
PY
echo JOBR SUMMARY DONE
