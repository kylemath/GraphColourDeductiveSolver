# Stage 22 probe (design-only, no LP solve). Run inside the pcheck namespace with the stage-20 flags.
# Part 1: exact column sums of cert_st20xL (as lowerR2 computes them) and the reverse-column screen for the
#         co-facial edge directions a face-charge re-basing with free face->corner rules would add.
# Part 2: arithmetic on the s19e/family.json face family under the re-based charges of RELAY_SPEC 18.
import json, collections
from fractions import Fraction
OUT = open('probe22.log', 'w')
def P(*a):
    s = ' '.join(str(x) for x in a); print(s); OUT.write(s + '\n'); OUT.flush()
load_patterns()
xon = 'xon' in FLAGS
C = json.load(open(OPT['cert']))
SR = {(wd, tuple(map(str, b))): cf for wd, cf, b in R2_sender_rows()}
tot = collections.defaultdict(Fraction); tco = Fraction(0); D = Fraction(0)
touch = collections.defaultdict(set)   # column -> labels of cert rows it appears in
for c in C:
    w = Fraction(c['w']).limit_denominator(10 ** 7); row = c['row']; lab = json.dumps(row)
    if row[0] == 'senderR2':
        cf = SR[(row[1], tuple(map(str, row[2])))]
        for k, v in cf.items(): tot[k] += w * v; touch[k].add(lab)
        tco += w; D += w
    elif row[0] == 'cons2':
        for k, v in cons2_coef(tuple(row[1]), tuple(row[2])).items(): tot[k] += w * v; touch[k].add(lab)
    elif row[0] == 'mrowR2':
        sg = tuple(row[1]); k = tuple(row[2]); tot[('h', k)] += w; tot[('M', sg)] -= w
        touch[('h', k)].add(lab); touch[('M', sg)].add(lab)
    elif row[0] == 'receiverR2':
        d, lk, sv = int(row[1]), row[2], row[3]
        for k, v in recv_coef_R2(d, lk, sv, xon).items(): tot[k] += w * v; touch[k].add(lab)
        tco -= w; D += w * (d - 6)
    else: raise SystemExit('unknown row ' + row[0])
P('cert', OPT['cert'], 'rows', len(C), ' t-coefficient', tco, ' objective', D / tco, '=', float(D / tco))
rc = {k: -v / tco for k, v in tot.items()}
fam = collections.defaultdict(lambda: [0, 0, 0, Fraction(0)])
for k, r in rc.items():
    f = fam[k[0]]
    if r > 0: f[0] += 1; f[3] = max(f[3], r)
    elif r == 0: f[1] += 1
    else: f[2] += 1
P('\nreduced costs over the columns the cert touches (rc = -(sum w*coef)/tco; dual feasibility needs rc >= 0, x priced at cap):')
P('  family  rc>0  rc=0  rc<0  max rc')
for k in sorted(fam): P('  %-6s %5d %5d %5d  %s' % (k, fam[k][0], fam[k][1], fam[k][2], fam[k][3]))
# Reverse-direction screen. A co-facial transfer b->a in the opposite direction of an existing edge column
# (big->five against y, 6->five against g, big->6 against h), with the same key, has every coefficient negated,
# so its reduced cost is -rc. It is profitable against this cert iff rc(forward) > 0 strictly.
P('\nreverse-direction columns (same key, opposite direction): profitable iff forward rc > 0')
face_lab = set()
for c in C:
    row = c['row']
    if row[0] == 'receiverR2':
        lk, sv = row[2], row[3]; d = len(lk)
        if any(lk[i] == '5' and lk[(i + 1) % d] == '5' and sv[i] == '5' for i in range(d)): face_lab.add(json.dumps(row))
    if row[0] == 'senderR2' and row[1][:2] == '55': face_lab.add(json.dumps(row))
P('  face-family cert rows (5-5-5 face at a receiver, or sender with w0 = w1 = 5):', len(face_lab))
for fk, name in (('y', 'big->five (reverse y)'), ('g', '6->five (reverse g)'), ('h', 'big->6 (reverse h)')):
    pos = sorted(((r, k) for k, r in rc.items() if k[0] == fk and r > 0), key=lambda z: -z[0])
    onface = [(r, k) for r, k in pos if touch[k] & face_lab]
    P('  %s: %d profitable keys, %d of them in a face-family row; top: %s' % (name, len(pos), len(onface), [(str(k[1]), str(r)) for r, k in pos[:6]]))
    for r, k in onface[:12]:
        P('     face key', k, 'rc', r, '=', float(r), 'rows:', sorted(touch[k] & face_lab)[:3])
# Part 2: family.json arithmetic
F = json.load(open('../s19e/family.json'))
P('\nfamily.json:', F['registry'])
def k555(word):   # number of 5-5-5 faces at a sender five v: consecutive link fives w_k = w_{k+1} = 5 (cyclic)
    return sum(1 for i in range(len(word)) if word[i] == '5' and word[(i + 1) % len(word)] == '5')
P('\n(i) e-family re-basing (vertex 6-(1+e/3)d, face e; e/3 back to each corner): every row changes by')
P('    vertex: -(e/3)d + (e/3)d = 0 ; so every receiver cap and every sender RHS is unchanged:')
e = Fraction(3)
for R in F['receivers']:
    d = R['d']; old = 6 - d; new = 6 - (1 + e / 3) * d + d * (e / 3)
    assert new == old
for S in F['senders']:
    assert 6 - (1 + e / 3) * 5 + 5 * (e / 3) == 1
P('    checked for all %d receivers and %d sender contexts (e = 3 shown; identity in e)' % (len(F['receivers']), len(F['senders'])))
P('\n(ii) 5-5-5 shared charge: each 5-5-5 face takes sigma from each corner.')
P('    (a) face transit (must end at 0) under current shapes: only disposal is sigma back to each corner -> delta 0.')
P('    (b) face kept as a holder (ends <= t): sigma <= t/3, sender RHS 1 - k*sigma, k = #5-5-5 faces at v.')
srows = [c for c in C if c['row'][0] == 'senderR2']
kap = 1 + sum(Fraction(c['w']).limit_denominator(10 ** 7) * k555(c['row'][1]) for c in srows) / 3 / tco
P('        cert_st20xL sender rows with k >= 1:', sum(1 for c in srows if k555(c['row'][1])), 'of', len(srows),
  '; dual weight on them', float(sum(c['w'] for c in srows if k555(c['row'][1]))))
P('        old cert stays dual-feasible; t-column becomes kappa =', kap, '=', float(kap))
P('        so t*(b) >= (16/101)/kappa =', D / tco / kap, '=', float(D / tco / kap), '(a normalisation, see RELAY_SPEC 18.4)')
P('\n(iii) face rows of the family at sol_st20xL (kill_st20x.log): load r 0.02339 + y 0.71423 + y 0.42079 = 1 + t.')
P('     Under (i) and (ii)(a) the receiver row of the face 7 is the same row: the 7 ends at charge t* = 16/101 > 0')
P('     (balanced/negative convention: at -16/101), i.e. it still goes negative and still binds at 16/101.')
for R in F['receivers']:
    P('     receiver d=%d %s/%s faces_at_i=%s duals(10/63 certs)=%s' % (R['d'], R['link'], R['apex'], R['faces_at_i'], {a: round(b, 4) for a, b in R['dual'].items()}))
adm = [S for S in F['senders'] if any(x['admissible'] for x in S['expansion'])]
P('     sender contexts surviving exact admissibility: %d of %d; k555 per word: %s' % (len(adm), len(F['senders']),
  dict(collections.Counter((S['word'], k555(S['word'])) for S in adm))))
OUT.close()
OUT = open('probe22.log', 'a')
P('\ncolumns with rc > 0 in the non-face-local families (reverse would be a distance-2 or bound column, not a face rule):')
for k, r in sorted(rc.items(), key=lambda z: -z[1]):
    if r > 0: P('  ', k, 'rc', r, '; in face-family rows:', len(touch[k] & face_lab), '; rows:', sorted(touch[k])[:2])
OUT.close()
