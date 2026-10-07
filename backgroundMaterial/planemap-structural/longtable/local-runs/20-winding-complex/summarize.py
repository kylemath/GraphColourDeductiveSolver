import json, glob, collections
tot = collections.defaultdict(collections.Counter)
det = collections.Counter(); posC=[]
for fn in sorted(glob.glob('out-*.jsonl')):
    for l in open(fn):
        r = json.loads(l); o = r['tag']['order']; T = tot[o]
        T['classes'] += 1; T['states'] += r['d_A']['states']
        T['piperm_ok'] += r['pi_is_perm']; T['lam_table_ok'] += r['lambda_table_mismatch'] == 0; T['thmW_ok'] += r['thmW_ok']
        T['asymA_fail'] += r['asym_fail_A']; T['asymC_fail'] += r['asym_fail_C']
        T['squares'] += r['squares']; T['sqfailA'] += r['square_fail_A']; T['sqfailC'] += r['square_fail_C']
        T['tri'] += r['tri'][0]; T['triA'] += r['tri'][1]; T['triC'] += r['tri'][2]
        T['c4'] += r['c4'][0]; T['c4A'] += r['c4'][1]; T['c4C'] += r['c4'][2]
        T['cls_inconsA'] += r['d_A']['inconsistent'] > 0; T['cls_inconsC'] += r['d_C']['inconsistent'] > 0
        T['cyc_inconsA'] += r['d_A']['inconsistent']; T['cyc_inconsC'] += r['d_C']['inconsistent']; T['cycrank'] += r['d_A']['cycle_rank']
        T['cls_pos'] += r['hasPos']; T['cls_pos_and_inconsC'] += r['hasPos'] and r['d_C']['inconsistent'] > 0
        T['cls_inconsC_nopos'] += (not r['hasPos']) and r['d_C']['inconsistent'] > 0
        T['cls_pos_exactC'] += r['hasPos'] and r['d_C']['inconsistent'] == 0
        T['pi_cycles'] += len(r['pi_cycles']); T['pi_pos'] += sum(c['w5'] > 0 for c in r['pi_cycles']); T['pi_neg'] += sum(c['w5'] < 0 for c in r['pi_cycles'])
        T['floor_classes'] += all(c['w5'] == 0 for c in r['pi_cycles'])
        T['sumw_pos'] += sum(c['w5'] for c in r['pi_cycles']) > 0
        for k, v in r['square_fail_detail'].items(): det[(o, k)] += v
for o, T in sorted(tot.items()): print(o, dict(T))
