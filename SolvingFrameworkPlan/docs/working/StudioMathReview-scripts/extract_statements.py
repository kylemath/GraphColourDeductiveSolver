import re, sys, os
P = sys.argv[1]; mods = sys.argv[2].split(',')
GEN = {'DiamondCert', 'Conf2122Cert', 'DiamondMCert', 'DiamondPCert', 'C2122MCert', 'C2122PCert'}
OCC = {'DiamondMOcc', 'DiamondPOcc', 'C2122MOcc', 'C2122POcc'}
for m in mods:
    s = open(os.path.join(P, m + '.lean')).read()
    ns = re.findall(r'^namespace (\S+)', s, re.M)
    print(f'\n### `{m}`\n')
    if m in GEN:
        names = re.findall(r'^theorem (\S+)', s, re.M)
        print(f'Generated certificate: {len(names)} theorems, all closed by `decide` or by the ring-reduction library; exported: `colorable`.\n')
        keep = {'colorable'}
    elif m in OCC:
        keep = {'configOcc', 'colorable_of_occ'}
    else:
        keep = None
    out = []
    for mt in re.finditer(r'^(?:(?:private|protected|noncomputable) )*(theorem|lemma|def|structure|abbrev) (\S+)(.*?)(?=:=|\bwhere\b)', s, re.M | re.S):
        kind, name, body = mt.groups()
        if keep is not None and name not in keep and not (m in OCC and name == 'Occ'):
            continue
        if kind in ('def', 'structure', 'abbrev'):
            full = s[mt.start():].split('\n\n')[0]
            full = re.sub(r'^/--.*?-/\s*', '', full, flags=re.S)
            if len(full) > 1500: full = full[:1500] + ' …'
            out.append(f'- **{kind}**\n\n```lean\n{full}\n```')
        else:
            txt = ' '.join((name + body).split())
            out.append(f'- **{kind}** `{txt}`')
    print('\n'.join(out))
