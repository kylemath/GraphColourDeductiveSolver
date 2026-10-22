import json,sys
print('| map | mode | variant | merges | R hist | max R | final R (sizes) | w hist | max tau before relevel | relevel skips (chords) | proper |')
print('|---|---|---|---|---|---|---|---|---|---|---|')
for l in open('e4_summary.jsonl'):
    r=json.loads(l); fl=r['relevel_fails']
    v=r['variant']+('+chordless' if r.get('chordless') else '')
    hw=r['hist_w'] if r['variant'].startswith('level') else '-'
    print('| %s s%d | %s | %s | %s | %s | %s | %s %s | %s | %s | %d %s | %s |'%(r['name'],r['seed'],r['mode'],v,r['merges'],r['hist_R'],r['maxR'],r['R_final'],r['final_sizes'],hw,r['max_tau_before'],len(fl),[f['chords'] for f in fl][:6],r['proper'] if not r['err'] else r['err']))
