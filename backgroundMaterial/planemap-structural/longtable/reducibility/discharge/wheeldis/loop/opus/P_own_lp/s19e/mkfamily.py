# exec'd after the s19e engine defs (pcheck namespace): writes family.json (FINDINGS "family.json README")
import json, itertools, collections
from fractions import Fraction as Fr
CERTS = {'st18hL': '../s18d/cert_st18hL.json', 'st19wL': '../s19d/cert_st19wL.json', 'st19fL': 'cert_st19fL.json'}
def canon_arr(lk, sv):
    w = [int(c) for c in lk]; s = [int(c) for c in sv]; d = len(w); best = None
    for k in range(d):
        for refl in (False, True):
            if not refl: w2 = [w[(i + k) % d] for i in range(d)]; s2 = [s[(i + k) % d] for i in range(d)]
            else: w2 = [w[(k - i) % d] for i in range(d)]; s2 = [s[(k - i - 1) % d] for i in range(d)]
            c = (''.join(map(str, w2)), ''.join(map(str, s2)))
            if best is None or c < best: best = c
    return best
def faces(lk, sv):
    w = [int(c) for c in lk]; s = [int(c) for c in sv]; d = len(w)
    return [i for i in range(d) if w[i] == 5 and w[(i + 1) % d] == 5 and s[i] == 5]
rec = {}; snd = {}
for tag, fn in CERTS.items():
    for c in json.load(open(fn)):
        r = c['row']; wt = float(c['w'])
        if r[0] == 'receiverR2':
            d, lk, sv = int(r[1]), r[2], r[3]
            if not faces(lk, sv): continue
            key = (d, lk, sv); e = rec.setdefault(key, {'d': d, 'link': lk, 'apex': sv, 'canonical': list(canon_arr(lk, sv)), 'faces_at_i': faces(lk, sv), 'dual': {}})
            e['dual'][tag] = wt
        elif r[0] == 'senderR2':
            wd = r[1]; w = [int(ch) for ch in wd]
            fpos = [k for k in range(5) if w[k] == 5 and w[(k + 1) % 5] == 5]
            if not fpos: continue
            bits = r[2]; j = bits.index('|'); H = bits[:j]; F = bits[j + 1:]
            key = (wd, tuple(H), tuple(F)); e = snd.setdefault(key, {'word': wd, 'H': H, 'F': F, 'face_pairs': [[k, (k + 1) % 5] for k in fpos], 'dual': {}})
            e['dual'][tag] = wt
# the face rows Long Table named, with their status (in a cert or not)
named = [('7665566', '6675666'), ('7655667', '6756656'), ('7766556', '6567566'), ('7665566', '6765766'), ('7766556', '6576576'), ('7655666', '6756666')]
for lk, sv in named:
    rec.setdefault((7, lk, sv), {'d': 7, 'link': lk, 'apex': sv, 'canonical': list(canon_arr(lk, sv)), 'faces_at_i': faces(lk, sv), 'dual': {}})
for e in rec.values(): e['admissible_argsA54'] = admissible(e['d'], e['link'], e['apex']) is None
# exact expansion of each sender context: small -> {5,6}, big -> {7,8,9 (= >=9)}; admissibility of each small choice
def expand(e):
    w = [int(ch) for ch in e['word']]; sixes = [k for k in range(5) if w[k] == 6]
    Fd = dict(zip(sixes, e['F'])); out = []
    small = [('H%d' % k, k) for k in range(5) if e['H'][k] == 0] + [('F%d' % k, k) for k in sixes if Fd[k] == 0]
    for ch in itertools.product((5, 6), repeat=len(small)):
        let = dict(zip([n for n, _ in small], ch))
        hl = lambda k: [let['H%d' % k]] if e['H'][k] == 0 else list(BIGL)
        fl = lambda k: [let['F%d' % k]] if Fd[k] == 0 else list(BIGL)
        ok = True; why = []
        for k in sixes:   # the 6-spoke's wheel (5, w_{k+1}, H[k], F[k], H[k-1], w_{k-1}) must be non-R6 for some big letters
            if not any(not isR6((5, w[(k + 1) % 5], a, q, b, w[(k - 1) % 5])) for a in hl(k) for q in fl(k) for b in hl((k - 1) % 5)): ok = False; why.append('R6 at w%d' % k)
        for k in range(5):  # a five-spoke's link (5, w_{k-1}, H[k-1], H[k], w_{k+1}) must be non-R5 for some big letters
            if w[k] == 5 and not any(not isR5((5, w[(k - 1) % 5], a, b, w[(k + 1) % 5])) for a in hl((k - 1) % 5) for b in hl(k)): ok = False; why.append('R5 at w%d' % k)
        out.append({'letters': let, 'admissible': ok, 'why_not': why})
    return out
for e in snd.values():
    ex = expand(e); e['n_small'] = len(ex[0]['letters']) if ex else 0
    e['expansion'] = ex; e['n_cases'] = len(ex); e['n_admissible'] = sum(x['admissible'] for x in ex)
# fixed bits per word across all sibling contexts
fixed = {}
for wd in sorted({e['word'] for e in snd.values()}):
    L = [e for e in snd.values() if e['word'] == wd]
    fixed[wd] = {'H': [L[0]['H'][k] if all(x['H'][k] == L[0]['H'][k] for x in L) else None for k in range(5)],
                 'F': [L[0]['F'][k] if all(x['F'][k] == L[0]['F'][k] for x in L) else None for k in range(len(L[0]['F']))], 'n_contexts': len(L)}
fam = {'version': 1, 'registry': 's21/argsA54.txt (880d25c6), kill tables s21/f/kill/kill6, engine s19e (hat5 class)',
       'certs': CERTS,
       'definition': {'face': 'two consecutive link fives w_i, w_{i+1} of the receiver u and their apex s_i = 5 (a 5-5-5 face next to u)',
                      'sender_face': 'a sender five v whose canonical word has w_k = w_{k+1} = 5: (v, w_k, w_{k+1}) is a 5-5-5 face',
                      'hat_convention': 'H[k] = class of the hat between w_k and w_{k+1} of the sender five (0 = small {5,6}, 1 = big >= 7); F[k] = class of the private of the 6-spoke w_k',
                      'w3_condition': 'in the d = 7 face rows u = 7 and the link 6s next to the face; for the 55667 sender (v, w0 = w1 = 5) w2 = w3 = 6, w4 = 7',
                      'fixed_bits_per_word': fixed},
       'receivers': sorted(rec.values(), key=lambda e: (e['d'], e['link'], e['apex'])),
       'senders': sorted(snd.values(), key=lambda e: (e['word'], e['H'], e['F']))}
json.dump(fam, open('family.json', 'w'), indent=1)
log('family.json: %d face receivers, %d face sender contexts; fixed bits %s' % (len(rec), len(snd), json.dumps(fixed)))
for e in fam['senders']: log('  %s H=%s F=%s dual=%s cases %d admissible %d' % (e['word'], e['H'], e['F'], e['dual'], e['n_cases'], e['n_admissible']))
for e in fam['receivers']: log('  R %d %s/%s canon %s dual=%s adm=%s' % (e['d'], e['link'], e['apex'], e['canonical'], e['dual'], e['admissible_argsA54']))
