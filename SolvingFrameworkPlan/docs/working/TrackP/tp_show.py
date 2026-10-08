#!/usr/bin/env python3
"""Track P: summarise tn_forest output lines (stdin or files)."""
import sys, json
for f in sys.argv[1:]:
    for l in open(f):
        d = json.loads(l)
        print(d['src'], 'n', d['n'], 'E', d['nedge'], 'tgt', d['target'], 'L', d['cyclen'], d['Nprof'], 'lawf', d['lawfails'], d['status'], 'mindev', d['mindev'],
              'K', d.get('kedges'), 'exc', (d.get('kedges') or 0) - d['target'], 'chk', d.get('check_cyc'), d.get('excess_P1P2P3'))
