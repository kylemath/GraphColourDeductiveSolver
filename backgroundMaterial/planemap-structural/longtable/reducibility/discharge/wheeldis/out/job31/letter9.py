"""Letter-9 reading for f-names (rule: loop/studio/opus_check/letter9_rule.md; Long Table 19 Oct 09:00Z).
A '9' in the link or s word of an e/f-name is an interior vertex of exact degree 9 (explore's cutter builds every
lettered window vertex at its exact degree; kc, dfast and cfast reduce that exact configuration).
- parse9(name): the name's frame, {('w', j) / ('s', j): letter} with 9 = exactly 9 (plus ('u',): d when the link starts
  with the u marker of an a-name).
- lp_reading(name): what the LP registry may do with it. The LP alphabet's letter 9 means degree >= 9, so an exact-9
  slot matches no LP letter. 'unmatchable' means the pattern can never forbid an LP arrangement: sound but useless,
  and it is excluded from the k3x registry with a log line. 'lp' means no link/s 9 (a 9 only at the centre, d = 9,
  is exact for a d = 9 receiver), so the LP parser reads it as before.
p-names keep their own convention: '9' in a p-link and '0' in a p-s word mean free."""
def parse9(name):
    f = name.split('_'); k0 = f[0][0]; d = int(f[0][1:]); lk, sv = f[1], f[2]; out = {}
    if k0 == 'a':
        if lk[0] == 'u': out[('u',)] = d
        lk = lk[1:]
    for kind, word in (('w', lk), ('s', sv)):
        for j, ch in enumerate(word):
            if k0 == 'p' and ((kind == 'w' and ch == '9') or (kind == 's' and ch == '0')): continue
            if ch in '56789': out[(kind, j)] = int(ch)
    return out
def lp_reading(name):
    if name[0] == 'p': return 'lp'
    fr = parse9(name)
    return 'unmatchable' if any(v == 9 for k, v in fr.items() if k[0] in ('w', 's')) else 'lp'
