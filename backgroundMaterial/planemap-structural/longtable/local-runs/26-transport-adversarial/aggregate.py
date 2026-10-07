import json, glob
def load(fs): return [json.loads(l) for f in fs for l in open(f)]
small = load(sorted(glob.glob('small-*.jsonl'))); big = load(['big.jsonl'])
def line(r):
    t = r['transport']; a, b = t['a_DL_allpairs'], t['b_DL_otherpair']
    return dict(supply=r['supply'], capA=a['capreach'], capB=b['capreach'], okA=a['ok'], okB=b['ok'], hallA=a['hall_ratio'], hallB=b['hall_ratio'],
                relay=r['zero_relay_needed'], okD=t['d_DL_lockbreaking']['ok'], okE=t['e_DL_otherpair_lockbreaking']['ok'],
                lbany=r['every_pos_has_lb_exit_to_neg'], lball=r['all_neg_exits_lockbreaking'])
print('== item 1+2: C6 adversarial classes (13) ==')
for r in big:
    t = r['tag']; print(t['graph'], 'h%d' % t['hole'], 'states', r['states'], 'posW', r['posW'], 'sumW', r['sumw'], 'minW', r['minw'], line(r))
print('\n== item 1 detail: A7 h22 21078 ==')
r = [x for x in big if x['states'] == 21078 and x['tag']['hole'] == 22][0]
print('cycles', r['ncyc'], 'zero', r['nzero'], 'neg', r['nneg']); print('hist (w,L,count):', r['hist'])
for k, v in r['transport'].items(): print(k, v)
for x in r['lockbreak']: print(x)
print('\n== items 3: all %d small classes ==' % len(small))
bad = [r for r in small if not r['transport']['a_DL_allpairs']['ok']]; badb = [r for r in small if not r['transport']['b_DL_otherpair']['ok']]
print('(a) fails', len(bad), '(b) fails', len(badb), 'relay needed', sum(r['zero_relay_needed'] for r in small),
      '(d) lockbreaking-only fails', sum(not r['transport']['d_DL_lockbreaking']['ok'] for r in small),
      '(e) otherpair-lockbreaking-only fails', sum(not r['transport']['e_DL_otherpair_lockbreaking']['ok'] for r in small),
      'every positive has a lb exit to neg: fails', sum(not r['every_pos_has_lb_exit_to_neg'] for r in small),
      'all neg exits lb: holds', sum(r['all_neg_exits_lockbreaking'] for r in small))
print('min Hall ratio (a)', min(r['transport']['a_DL_allpairs']['hall_ratio'] for r in small), '(b)', min(r['transport']['b_DL_otherpair']['hall_ratio'] for r in small))
print('min cap/supply (a)', min(r['transport']['a_DL_allpairs']['capreach'] / r['supply'] for r in small))
print('\n w>=+8 classes (orders<=24):')
for r in sorted(small, key=lambda r: -r['posW'][0]):
    if r['posW'][0] >= 8: print(r['tag'], r['posW'], line(r))
print('\n 5 tightest by Hall ratio (b):')
for r in sorted(small, key=lambda r: r['transport']['b_DL_otherpair']['hall_ratio'])[:6]: print(r['tag'], r['posW'], line(r))
print('\n multi-positive small classes:')
for r in small:
    if r['npos'] > 1: print(r['tag'], r['posW'], line(r))
# lock-breaking totals over all
allr = small + big; tot = sum(x['exits_to_neg'] for r in allr for x in r['lockbreak']); lb = sum(x['exits_to_neg_lockbreaking'] for r in allr for x in r['lockbreak'])
print('\nDL exits to negative cycles from positive cycles, all 136 classes: %d, lock-breaking %d (%.1f%%)' % (tot, lb, 100 * lb / tot))
