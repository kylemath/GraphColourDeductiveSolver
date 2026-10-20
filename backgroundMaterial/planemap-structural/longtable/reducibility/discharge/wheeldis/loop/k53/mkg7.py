"""Twoeng-ready files for the round-53 held g7 kills (Long Table 01:44Z): kc lines from held53, engine blocks copied from
k53's G_kcc.out / G_df.out / G_cf.out (one block per name required), as minkill47 writes them.
usage: python3 -I mkg7.py K53DIR OUTDIR PREFIX"""
import sys, os
K, O, P = sys.argv[1:4]; os.makedirs(O, exist_ok=True)
held = [l.rstrip('\n') for l in open(os.path.join(K, 'held53_7_7665566_6765766.txt')) if l.strip() and not l.startswith('#')]
kills = {l.split()[0]: (l.split(' | ')[0], l.split(' | ')[2]) for l in held}
def blocks(f):
    out, cur = {}, None
    for l in open(os.path.join(K, f)):
        if l.strip() and not l.startswith(' ') and not l.startswith('#'):
            cur = l.split()[0]
            if cur in kills: out.setdefault(cur, []).append([])
        if cur in kills and not l.startswith('#'): out[cur][-1].append(l)
    return out
kb, db, cb = blocks('G_kcc.out'), blocks('G_df.out'), blocks('G_cf.out')
with open(os.path.join(O, P + '_kills.txt'), 'w') as a, open(os.path.join(O, P + '_kills_kc.out'), 'w') as b, \
     open(os.path.join(O, P + '_kills_cf.cfast'), 'w') as c, open(os.path.join(O, P + '_kills_df.out'), 'w') as d:
    for nm, (line, v) in sorted(kills.items(), key=lambda t: (int(t[1][0].split()[1]), t[0])):
        r, m = line.split()[1:3]
        for B in (kb, db if v.startswith('D') else cb):
            bl = [x for x in B.get(nm, []) if x[0].split()[1:3] == ['r=' + r, 'm=' + m]]
            assert len(bl) >= 1 and all(x == bl[0] for x in bl), (nm, len(bl))
        a.write(line + '\n'); b.write(''.join(kb[nm][0]))
        (d if v.startswith('D') else c).write(''.join((db if v.startswith('D') else cb)[nm][0]))
        print(nm, r, m, v.strip())
