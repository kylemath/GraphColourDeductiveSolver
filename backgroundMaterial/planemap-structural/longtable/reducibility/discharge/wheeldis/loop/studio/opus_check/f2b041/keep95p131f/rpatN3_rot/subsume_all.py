"""ST-10 fix: an rpatN3 pattern P is rotation-justified when SOME rotation-preserving pool pattern Q (nl51 rebuild, non-RSST keep pool,
RSST) MATCHES P (witness14.justifies: Q's fixed positions satisfied by P under a rotation / reflection). Replaces the equality test."""
import sys, collections
R = 'loop/studio/opus_check/f2b041/keep95p131f/rpatN3_rot/'
def load(fn):
    out = {}
    for l in open(fn):
        if not l.strip() or l.startswith('#'): continue
        a, ann = (l.split('#', 1) + [''])[:2]; t = a.split(); out[(int(t[0]), t[1], t[2])] = ann.strip()
    return out
src = open(R + 'witness14.py').read(); ns = {}
exec(src.split('def sat(q, p):')[1].join(['def sat(q, p):', '']) if False else 'def sat(q, p):' + src.split('def sat(q, p):')[1].split('rows = [')[0], ns)
J = ns['justifies']
A = load(R + 'rpatN3_flagoff.txt'); Q = {}
for fn in ('rpatN3_rot.txt', 'rpat_keeppool_rot.txt', 'rpat_rsst_rot.txt'): Q.update(load(R + fn))
byd = collections.defaultdict(list)
for q, ann in Q.items(): byd[q[0]].append((q, ann))
U = {(int(l.split()[0]), l.split()[1], l.split()[2]) for l in open(R + 'in/rpatN3_unjustified46.txt') if l.strip() and not l.startswith('#')}
kept = {}; drop = []
for P in A:
    w = next((ann + ' [' + ' '.join(map(str, q)) + ']' for q, ann in byd[P[0]] if J(q, P)), None)
    if w: kept[P] = w
    else: drop.append(P)
with open(R + 'rpatN3_dropped_rot.txt', 'w') as f:
    f.write('# rpatN3 patterns with no rotation-preserving matching witness in the keep95p131f pool (Studio ST-10, RPATN_ROT=1, matching test)\n')
    for P in sorted(drop): f.write('%d %s %s # %s | %s\n' % (P + (A[P], 'W18:yes' if P in U else 'W18:no')))
with open(R + 'rpatN3_rotation_justified_studio.txt', 'w') as f:
    f.write('# rpatN3 patterns with a rotation-preserving matching witness: pattern # witness [witness pattern]\n')
    for P in sorted(kept): f.write('%d %s %s # %s\n' % (P + (kept[P],)))
print('patterns %d; justified %d; dropped %d; dropped & W18-46 %d; only us %d; only W18 %d' % (len(A), len(kept), len(drop), len(set(drop) & U), len(set(drop) - U), len(U - set(drop))))
