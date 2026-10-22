import json, sys, numpy as np, collections
rows = [json.loads(l) for f in sys.argv[1:] for l in open(f) if l.strip()]
rows = [r for r in rows if 'err' not in r]
print('n', len(rows))
for r in sorted(rows, key=lambda r: -r['R']):
    f = r['feas']; minband = next((k for k in range(4) if f['band%d' % k][1] < 1e-6), None)
    minconf = next((k for k in range(r['R']+1) if f.get('conf%d' % k, (0, 9))[1] < 1e-6), None)
    p = r['prof']; o = p['k2_old']; q = p['k2_rand']
    print('%-28s R%d L%3d conf%3d chg%3d offR %.2f | band pen %s minband %s minconf %s | rand: dist_med %.2f proj %.2f snap %.2f | old: dist_med %.2f far %.2f ang med/max %.1f/%.1f ac %.2f rho(d,chg) %.2f rho(conf,chg) %.2f rho(d,dev) %.2f rho(dev,chg) %.2f AUCd %.2f AUCc %.2f | far-only AUCd %.2f AUCc %s' % (
        r['file'][:28], r['R'], r['L'], r['nconf'], r['nchanged'], r['off_radius'], [f['band%d' % k][1] for k in range(4)], minband, minconf,
        q['dist_med'], q['proj_med'], q['snapped'], o['dist_med'], o['far'], o['ang_med'], o['ang_max'], o['ang_ac1'], o['rho_dist_chg'], o['rho_conf_chg'],
        o['rho_dist_dev'], o['rho_dev_chg'], o['auc_dist'], o['auc_conf'], o['auc_dist_given_far'] or 0, o.get('auc_conf_given_far')))
