"""Dependency of a solved bound on the 10 job27 C entries the ring-merge sweep holds (Long Table 20 Oct 20:55Z).
Runs Studio's st21_check.py set-up (spec rows, loader, l3q, rpatN; read-only) up to the lower check for one solve, then:
 (a) for each held entry H: every receiver arrangement H matches in its own frame (d = 7, link/s letters 5..9, B = 7..9)
     that is admissible under all OTHER patterns (spec admissible() with H's patterns removed); count those matched by H and
     by no other pattern ("sole"), and for each sole arrangement compute its exact receiverR2 load under the solution;
     a load > d - 6 + t means the upper bound depends on H (kill line);
 (b) lower: a cert row depends on H only if it is a receiverR2 row made admissible by removing H, which cannot happen (removing
     patterns only adds admissible rows; every cert row is already admissible), checked directly;
 (c) section 14' kill tables and l3q masks: their forbidden set is RSST + k3x only (no cpat file), so they cannot change.
Usage: (env as the solve's st21_check run) python3 out/job30/ringmerge_cpat_dep.py SOL CERT ARGS"""
import os, sys, itertools, collections
HERE = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
HELD = ['e7_B55B565_.56B6BB_1111111', 'e7_B55B565_.56BBB5_1111111', 'e7_B55B565_B5.66BB_1111111', 'e7_B56B565_55.5BBB_1111111',
        'e7_B56B565_55.B6BB_1111111', 'e7_B56B565_55.BB6B_1111111', 'e7_B55B565_.565BBB_1111111', 'e7_B55B565_.56BB6B_1111111',
        'e7_B55B565_B5.BB66_1111111', 'e7_B56B565_55.BBB5_1111111']
src = open(os.path.join(HERE, 'out', 'job31', 'st21_check.py')).read()
cut = src.index('# ================= 12.8: exact lower check')
G = {'__name__': 'st21_dep', '__file__': os.path.join(HERE, 'out', 'job31', 'st21_check.py')}
exec(src[:cut], G)
parse_name, PAT, admissible, spec_val, recv_spec, T, CERT = (G[k] for k in ('parse_name', 'PAT', 'admissible', 'spec_val', 'recv_spec', 'T', 'CERT'))
LET = (5, 6, 7, 8, 9)
def pm(d, P, w, s):
    for r in range(d):
        for refl in (False, True):
            ok = True
            for kd, i, S in P:
                x_ = (w[(r - i) % d] if refl else w[(i + r) % d]) if kd == 'w' else (s[(r - i - 1) % d] if refl else s[(i + r) % d])
                if x_ not in S: ok = False; break
            if ok: return True
    return False
heldP = {}
for h in HELD:
    d, P = parse_name(h); heldP[h] = (d, P)
D = 7; allP = set(PAT[D]); hp = {heldP[h][1] for h in HELD}
G['PATL'][D] = [tuple(P) for P in allP - hp]          # patterns WITHOUT the 10 (admissible() reads PATL)
print('patterns at d=7: %d, of which held %d (distinct)' % (len(allP), len(hp & allP)), flush=True)
tot = collections.Counter(); worst = -1e9
for h in HELD:
    d, P = heldP[h]; sl = {}
    for kd, i, S in P: sl[(kd, i)] = sorted(S)
    choices = [sl.get(('w', i), LET) for i in range(d)] + [sl.get(('s', i), LET) for i in range(d)]
    nmatch = nsole = nviol = 0; hw = -1e9
    for a in itertools.product(*choices):
        w, s = list(a[:d]), list(a[d:]); nmatch += 1
        if not admissible(d, w, s): continue        # killed by another pattern or an R5/R6/RBIG rule: H is not needed
        nsole += 1
        v = spec_val(d, ''.join(map(str, w)), ''.join(map(str, s))); hw = max(hw, v)
        if v > d - 6 + T + 1e-9: nviol += 1
    worst = max(worst, hw); tot['sole'] += nsole; tot['viol'] += nviol
    print('%s: %d arrangements matched in its frame; sole (admissible without the 10) %d; max load among sole %.6f vs %.6f; above threshold %d' % (
        h, nmatch, nsole, hw if nsole else float('nan'), d - 6 + T, nviol), flush=True)
crow = [e for e in CERT if e['row'][0] == 'receiverR2']
G['PATL'][D] = [tuple(P) for P in allP]
bad = [e['row'] for e in crow if not admissible(e['row'][1], [int(c) for c in e['row'][2]], [int(c) for c in e['row'][3]])]
print('lower cert: %d receiverR2 rows, all admissible WITH the 10 (so none exists only because of them): %s' % (len(crow), not bad))
print('kill tables / l3q masks: forbidden set is RSST + k3x (no cpat file): 0 killed bits change')
print('RESULT: sole arrangements %d, above the upper threshold %d -> %s' % (tot['sole'], tot['viol'], 'UPPER DEPENDS ON THE 10 (kill line)' if tot['viol'] else 'no dependency'))
