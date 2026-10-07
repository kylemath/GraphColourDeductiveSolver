#!/usr/bin/env python3
"""[exploratory] NightBudget summary of nightbudget-records.jsonl."""
import json, os, sys
from collections import Counter, defaultdict
HERE = os.path.dirname(os.path.abspath(__file__))
R = [json.loads(l) for l in open(os.path.join(HERE, 'nightbudget-records.jsonl'))]
bad = [r for r in R if 'groups' not in r]
print('records', len(R), 'without groups (skipped/error)', len(bad), Counter(('skipped' if 'skipped' in r else r.get('error', '?')[:60]) for r in bad))
R = [r for r in R if 'groups' in r]
def fam(r):
    return r['src'] if r['src'] != 'census' else 'census'
for scope in ('(5,5,5,5,6)', '(5,5,5,5,5)', 'other (witness holes)'):
    if scope == '(5,5,5,5,6)': RR = [r for r in R if tuple(r['pattern']) == (5, 5, 5, 5, 6)]
    elif scope == '(5,5,5,5,5)': RR = [r for r in R if tuple(r['pattern']) == (5, 5, 5, 5, 5)]
    else: RR = [r for r in R if tuple(r['pattern']) not in ((5, 5, 5, 5, 6), (5, 5, 5, 5, 5))]
    print('\n######## pattern', scope, ': hole-orientations', len(RR), 'by source', dict(Counter(fam(r) for r in RR)))
    for gk in ('sigma', 'union'):
        for src in sorted({fam(r) for r in RR}) + ['ALL']:
            S = [r for r in RR if src == 'ALL' or fam(r) == src]
            G = [(r, g) for r in S for g in r['groups'][gk]]
            nontriv = [(r, g) for r, g in G if g['lit']['R'] > 0 or g['DD'] > 0]
            c = Counter()
            for r, g in G:
                c['groups'] += 1
                c['lam>0 (floor fails on group)'] += g['lam'] > 0
                c["B'lit fails"] += g['lit']['slack'] < 0
                c["B'rho fails"] += g['rho']['slack'] < 0
                c['|DD|>2|R| (lit)'] += g['lit']['ddloss'] > 0
                c["B'lit holds & |DD|>2|R| & lam>0"] += g['lit']['slack'] >= 0 and g['lit']['ddloss'] > 0 and g['lam'] > 0
                c['R- nonempty'] += g['lit']['Rm'] > 0
            ms = min((g['lit']['slack'] for r, g in nontriv), default=None)
            mr = min((g['rho']['slack'] for r, g in nontriv), default=None)
            ml = max((g['lam'] for r, g in G), default=None)
            print('  [%s-groups | %s] %s | min slack lit %s, rho %s (groups with R or DD: %d); max group lam %s' % (gk, src, dict(c), ms, mr, len(nontriv), ml))
    # tightest groups (union) with R- nonempty
    for gk in ('sigma', 'union'):
        T = sorted([(g['lit']['slack'], r['src'], r['name'], r['hole'], r['mirror'], g) for r in RR for g in r['groups'][gk] if g['lit']['Rm'] > 0], key=lambda t: t[0])[:8]
        print('  tightest %s-groups with R- nonempty:' % gk)
        for s, src, nm, h, m, g in T:
            print('    slack %d  %s %s h%d %s | size %d cyc %d (pos %d) lam %d DD %d N0 %d E2 %d tau %d | R %d R- %d %s N0f %d ddloss %d | rho: R %d R- %d slack %d' % (
                s, src, nm, h, 'mirror' if m else 'plantri', g['size'], g['ncyc'], g['ncyc_pos'], g['lam'], g['DD'], g['N0'], g['E2'], g['tau'],
                g['lit']['R'], g['lit']['Rm'], g['lit']['Rm_kinds'], g['lit']['N0f'], g['lit']['ddloss'], g['rho']['R'], g['rho']['Rm'], g['rho']['slack']))
    for gk in ('sigma', 'union'):
        F = [(r, g) for r in RR for g in r['groups'][gk] if g['lit']['slack'] < 0 or g['rho']['slack'] < 0]
        if F:
            print('  %s-groups failing lit or rho (%d), first 12:' % (gk, len(F)))
            for r, g in sorted(F, key=lambda t: min(t[1]['lit']['slack'], t[1]['rho']['slack']))[:12]:
                print('    %s %s n%s h%d %s linkdeg %s | size %d cyc %d (pos %d, maxw %d) lam %d DD %d N0 %d E2 %d tau %d | lit R %d R- %d %s N0f %d slack %d ddloss %d | rho R %d R- %d slack %d ddloss %d' % (
                    r['src'], r['name'], r.get('n'), r['hole'], 'mirror' if r['mirror'] else 'plantri', r['linkdeg'], g['size'], g['ncyc'], g['ncyc_pos'], g['maxw'], g['lam'], g['DD'], g['N0'], g['E2'], g['tau'],
                    g['lit']['R'], g['lit']['Rm'], g['lit']['Rm_kinds'], g['lit']['N0f'], g['lit']['slack'], g['lit']['ddloss'], g['rho']['R'], g['rho']['Rm'], g['rho']['slack'], g['rho']['ddloss']))
    U = Counter(); UR = Counter()
    for r in RR:
        for k, v in r['u34'].items(): U[(fam(r) if fam(r) in ('census',) else 'constr/AW/wp13/witness', k)] += v
        for k, v in r['u34rhs'].items(): UR[(fam(r) if fam(r) in ('census',) else 'constr/AW/wp13/witness', k)] += v
    print('  R- images (k = deg-6 position rel. j, kind, back-position in run / u / f):')
    for k, v in sorted(U.items(), key=lambda t: (t[0][0], str(t[0][1]))): print('    %6d %s' % (v, k))
    print("  R- images: right side of B' put by the image's own excursion (rhs = 2[u=1] + [u=2] + 3(f-1)), its DD steps and R states:")
    for k, v in sorted(UR.items(), key=lambda t: (t[0][0], str(t[0][1]))): print('    %6d %s' % (v, k))
