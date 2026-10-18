"""EXPLORE round 46 part A: windows (ring <= 14, from win45.py) of the cert_s7 receivers that contain a sender wheel of
55677 or 56687 (the five w_i plus u, w_i-1, w_i+1, s_i-1, s_i).  Writes ctx46_A.txt (window lines, ring order) and
ctx46_A.map (window -> contexts).  usage: python3 ctx46.py"""
import os, json, collections
H = os.path.dirname(os.path.abspath(__file__))
CTX = [  # (d, link, s, sender position, sender word, weight /47) from cert_s7.json (Opus fa4705f2, studio/opus_check)
    (8, '75657565', '55655565', 3, '56687', 1), (8, '75657565', '55655565', 7, '56687', 1),
    (7, '7565765', '6855555', 3, '55677', 4), (7, '7565765', '6855555', 6, '55677', 4),
    (7, '8558655', '6665666', 1, '56687', 2), (7, '8558655', '6665666', 2, '56687', 2), (7, '8558655', '6665666', 6, '56687', 2),
    (7, '7557565', '6566666', 1, '55677', 2), (7, '7557565', '6566666', 2, '55677', 2),
    (7, '7557656', '6565665', 1, '55677', 2), (7, '7557656', '6565665', 2, '55677', 2),
    (8, '76565565', '57765865', 7, '56687', 2),
    (8, '75657565', '66656665', 3, '56687', 1), (8, '75657565', '66656665', 7, '56687', 1)]
def verts(nm):
    _, l, s = nm.split('_')
    return ({('u',)} if l[0] == 'u' else set()) | {('w', j) for j, c in enumerate(l[1:]) if c in '5678'} | {('s', j) for j, c in enumerate(s) if c != '.'}
out = {}; mp = collections.defaultdict(list)
for d, lk, sv, i, wd, wt in CTX:
    fn = os.path.join(H, 'win45_%d_%s_%s_A14.txt' % (d, lk, sv)) if os.path.exists(os.path.join(H, 'win45_%d_%s_%s_A14.txt' % (d, lk, sv))) \
        else os.path.join(H, '..', 'k45', 'win45_%d_%s_%s_A14.txt' % (d, lk, sv))
    wheel = {('u',), ('w', (i - 1) % d), ('w', i), ('w', (i + 1) % d), ('s', (i - 1) % d), ('s', i)}
    for l in open(fn):
        nm = l.split()[0]
        if wheel <= verts(nm):
            key = '%s@%s' % (nm, sv)          # window names repeat across rows with the same link; tag with the s word
            out[key] = l.replace(nm + ' ', key.replace('@', '_r') + ' ', 1); mp[key].append('%d %s/%s w%d %s %d/47' % (d, lk, sv, i, wd, wt))
L = sorted(out.items(), key=lambda kv: (int(kv[1].split()[1]), kv[0]))
open(os.path.join(H, 'ctx46_A.txt'), 'w').write(''.join(v for k, v in L))
open(os.path.join(H, 'ctx46_A.map'), 'w').write(''.join('%s | %s\n' % (k.replace('@', '_r'), '; '.join(mp[k])) for k, v in L))
print('windows', len(L), collections.Counter(int(v.split()[1]) for k, v in L))
for d, lk, sv, i, wd, wt in CTX:
    print(d, lk, sv, 'w%d' % i, wd, sum(1 for k in mp if any(x.startswith('%d %s/%s w%d ' % (d, lk, sv, i)) for x in mp[k])))
