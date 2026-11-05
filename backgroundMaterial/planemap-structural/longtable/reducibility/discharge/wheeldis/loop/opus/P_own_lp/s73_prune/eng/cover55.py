def cmd_cover55():
    """s66: for each arrangement 'd LINK SWORD ...' in arr=FILE list every loaded pattern (all dihedral placements) matching it; out=FILE tsv"""
    load_patterns()
    out = open(OPT['out'], 'w')
    for line in open(OPT['arr']):
        f = line.split()
        if not f or f[0].startswith('#'): continue
        d, lk, sv = int(f[0]), f[1], f[2]
        w = [int(c) for c in lk]; s = [int(c) for c in sv]
        hits = {}
        for P in PATS[d]:
            ok = False
            for r in range(d):
                for refl in (False, True):
                    good = True
                    for (typ, i), S in P:
                        if not refl: j = (i + r) % d
                        else: j = (r - i) % d if typ == 'w' else (r - i - 1) % d
                        v = w[j] if typ == 'w' else s[j]
                        if v not in S: good = False; break
                    if good: ok = True; break
                if ok: break
            if ok: hits[P] = NAMEALL.get((d, P), [('?', '?')])
        names = sorted(set('%s|%s' % (nm, src.split('/')[-1]) if src not in ('D', 'C', 'RPAT', 'RPATN') else '%s|%s' % (nm, src) for L in hits.values() for nm, src in L))
        out.write('%d\t%s\t%s\t%s\n' % (d, lk, sv, ';'.join(names)))
    out.close()
