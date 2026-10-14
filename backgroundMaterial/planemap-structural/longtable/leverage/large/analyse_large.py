#!/usr/bin/env python3
"""Aggregate out/*.jsonl from large.py -> TABLES.md (stdout) and plots/*.png.

Source DL (doubly locked states). From a DL state 'unlock' (DL -> not DL) is the single-step quantity available in both
modes; on the sphere non-DL => dF = 1, so from a dF = 2 state unlock <=> dF-reducing (../README.md, fact 2).
Exact mode also gives source D2 (dF = 2) with dF-1."""
import json, glob, os, collections, math, gzip
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def load(f):
    out = []
    for l in (gzip.open(f, 'rt') if f.endswith('.gz') else open(f)):
        try: r = json.loads(l)
        except ValueError: continue
        if 'skip' in r or 'H' not in r: continue
        out.append(r)
    return out

R = {os.path.basename(f).split('.')[0]: load(f) for f in sorted(glob.glob('out/*.jsonl') + glob.glob('out/*.jsonl.gz'))}

def fam(rows, **kw):
    return [r for r in rows if all(r.get(k) == v for k, v in kw.items())]

SETS = collections.OrderedDict()
SETS['IPR C60-C82 exact'] = R.get('a_ipr_exact', [])
SETS['non-IPR (SW) C60-C82 exact'] = R.get('a_sw_exact', [])
SETS['IPR C92-C120 sample'] = R.get('a_ipr_sample', [])
SETS['non-IPR (SW) C92-C120 sample'] = R.get('a_sw_sample', [])
SETS['tubes+Goldberg n<=44 exact'] = R.get('a_tubes_exact', [])
tub = R.get('a_tubes_sample', [])
SETS['tubes n<=92 sample'] = [r for r in tub if not r['name'].startswith('GC') and r['n'] <= 92]
SETS['tubes n>92 sample'] = [r for r in tub if not r['name'].startswith('GC') and r['n'] > 92]
SETS['Goldberg C80-C540 sample'] = [r for r in tub if r['name'].startswith('GC')] + R.get('a_goldberg2_sample', [])
SETS['glued n=42-43 exact'] = R.get('b_glued_exact', []) + R.get('b_glued_exact2', [])
SETS['glued n=42-57 sample'] = R.get('b_glued_sample', [])
for k in range(5):
    SETS['pad k=%d exact' % k] = [r for r in R.get('c_pad_exact', []) if r.get('k') == k and r['mode'] == 'exact']
for k in range(5):
    SETS['pad k=%d sample' % k] = [r for r in R.get('c_pad_sample', []) if r.get('k') == k]
# exact sets keep only exact rows (holes above maxS fell back to sampling); fallbacks join the glued sample set
fb = [r for k, v in SETS.items() if 'exact' in k for r in v if r['mode'] != 'exact']
for k in list(SETS):
    if 'exact' in k: SETS[k] = [r for r in SETS[k] if r['mode'] == 'exact']
if 'glued n=42-57 sample' in SETS: SETS['glued n=42-57 sample'] += [r for r in fb if r.get('family') == 'glued']
SETS = collections.OrderedDict((k, v) for k, v in SETS.items() if v)

SMALL = {  # ../TABLES.md, D2 dF-1 per swap (= unlock), d = 1..4
    'small: frame 30-33 (D2)': [0.711, 0.489, 0.338, 0.240],
    'small: frame 22-28 (D2)': [0.741, 0.494, 0.365, 0.275],
    'small: plantri24 (D2)': [0.743, 0.563, 0.320, 0.145]}

HW = False   # True: every hole weighs the same (counts divided by the hole's source-state count)

def agg(rows, src):
    H = collections.defaultdict(collections.Counter); st = collections.Counter(); sh = collections.Counter()
    for r in rows:
        w = 1.0
        if HW:
            if not r['states'].get(src): continue
            w = 1.0 / r['states'][src]
        for k, v in r['H'].items():
            s, d = k.split('|')
            if s == src: H[int(d)].update({kk: vv * w for kk, vv in v.items()})
        if HW: st.update({src: 1})
        else: st.update(r['states'])
        for d, c in r['shell'].items(): sh[int(d)] += c
    return H, st, sh

def curve(rows, src, key):
    """per d: n swaps, rate per swap, swaps/state, succ/state, shell (mean per hole over holes that reach d),
    succ per state per shell vertex"""
    H, st, sh = agg(rows, src); ns = st.get(src, 0)
    reach = collections.Counter(int(d) for r in rows for d in r['shell'])
    out = []
    for d in sorted(H):
        h = H[d]; n = h['n']
        if not n: continue
        # holes that reach shell d: normalise per-state numbers by shell size averaged over the same holes
        shell = sh[d] / max(1, reach[d])
        out.append(dict(d=d, n=n, rate=h.get(key, 0) / n, per_state=n / ns if ns else 0,
                        succ=h.get(key, 0) / ns if ns else 0, shell=shell, meanK=h['size'] / n,
                        pij=h.get('pi_jump', 0) / n, swaps_shell=(n / ns / shell) if ns and shell else 0,
                        succ_shell=(h.get(key, 0) / ns / shell) if ns and shell else 0))
    return out, ns

def eccs(rows):
    c = collections.Counter(r['ecc'] for r in rows)
    return ','.join('%d:%d' % kv for kv in sorted(c.items()))

def table(name, rows, src, key, minn=200):
    c, ns = curve(rows, src, key)
    s = ['', '**%s** — source %s, key %s (%d holes, ecc %s, %d source states, modes %s)' % (
        name, src, key, len(rows), eccs(rows), ns, ','.join(sorted(set(r['mode'] for r in rows)))), '',
         '| d | shell (mean) | swaps/state | swaps/state/shell-vtx | mean K | rate per swap | ratio to d-1 | successes/state | successes/state/shell-vtx | pi-jump rate |',
         '|---|---|---|---|---|---|---|---|---|---|']
    prev = None
    for r in c:
        thin = r['n'] < minn
        ratio = ('%.2f' % (r['rate'] / prev)) if prev and not thin else '-'
        s.append('| %d | %.1f | %.3f | %.4f | %.1f | %s | %s | %.3f | %.4f | %.3f |' % (
            r['d'], r['shell'], r['per_state'], r['swaps_shell'], r['meanK'],
            ('%.3f' % r['rate']) + (' (n=%d)' % r['n'] if thin else ''), ratio, r['succ'], r['succ_shell'], r['pij']))
        prev = r['rate'] if not thin else prev
    return '\n'.join(s)

def onlyfar(rows):
    st = collections.Counter()
    for r in rows: st.update(r['states'])
    out = []
    for src in ('DL', 'D2', 'deep'):
        tot = sum(v for k, v in st.items() if k.startswith(src + '_bestnear'))
        if tot: out.append('%s (exact dF): %d states with a dF-reducing swap, only-far (d>=2) %d = %.4f'
                           % (src, tot, st[src + '_allbestfar'], st[src + '_allbestfar'] / tot))
    if st.get('DL_unl_any') or st.get('DL_unl_none'):
        tot = st['DL_unl_any'] + st['DL_unl_none']
        out.append('DL (sampled, single step): %d DL samples, with an unlocking swap %d, only-far unlocks %d = %.4f '
                   '(of those with one), a far unlock available %.3f, no unlocking swap (dF>=3) %d'
                   % (tot, st['DL_unl_any'], st['DL_unl_onlyfar'], st['DL_unl_onlyfar'] / max(1, st['DL_unl_any']),
                      st['DL_unl_far_avail'] / max(1, st['DL_unl_any']), st['DL_unl_none']))
    return out

def by_ecc(name, rows, src, key):
    out = []
    for e in sorted(set(r['ecc'] for r in rows)):
        rs = [r for r in rows if r['ecc'] == e]
        c, ns = curve(rs, src, key)
        if ns < 100: continue
        r1 = next((r['rate'] for r in c if r['d'] == 1), None)
        if not r1: continue
        cells = ' '.join('%d:%.3f(%.2f)' % (r['d'], r['rate'], r['rate'] / r1) for r in c if r['n'] >= 200)
        out.append('| %s | %d | %d | %d | %s |' % (name, e, len(rs), ns, cells))
    return out

if __name__ == '__main__':
    os.makedirs('plots', exist_ok=True)
    print('# Large-diameter leverage tables (generated by analyse_large.py)\n')
    print('| set | holes | modes | n range | hole ecc | samples or S | unfilled | DL | D2 (exact) | deep (exact) |')
    print('|---|---|---|---|---|---|---|---|---|---|')
    for nm, rows in SETS.items():
        st = collections.Counter()
        for r in rows: st.update(r['states'])
        print('| %s | %d | %s | %d-%d | %s | %d | %d | %d | %d | %d |' % (
            nm, len(rows), ','.join(sorted(set(r['mode'] for r in rows))), min(r['n'] for r in rows), max(r['n'] for r in rows),
            eccs(rows), sum(r.get('samples', r.get('S', 0)) for r in rows), st['U'], st['DL'], st['D2'], st['deep']))
    print('\n## Summary: DL unlock rate per swap by d, every hole weighted equally (bins with >= 200 swaps), per-hop factor fitted on d >= 2\n')
    print('| set | holes | ' + ' | '.join('d=%d' % d for d in range(1, 13)) + ' | factor/hop (d>=2) | xi = -1/ln f |')
    print('|---|---|' + '---|' * 12 + '---|---|')
    for nm, rows in SETS.items():
        c0, _ = curve(rows, 'DL', 'unlockDL'); ok = {r['d'] for r in c0 if r['n'] >= 200}
        HW = True; c, ns = curve(rows, 'DL', 'unlockDL'); HW = False
        cd = {r['d']: r for r in c if r['d'] in ok}
        pts = [(d, math.log(cd[d]['rate'])) for d in cd if d >= 2 and cd[d]['rate'] > 0]
        f = xi = '-'
        if len(pts) >= 2:
            mx = sum(p[0] for p in pts) / len(pts); my = sum(p[1] for p in pts) / len(pts)
            sl = sum((p[0] - mx) * (p[1] - my) for p in pts) / sum((p[0] - mx) ** 2 for p in pts)
            f = '%.2f' % math.exp(sl); xi = '%.2f' % (-1 / sl) if sl < 0 else 'inf'
        print('| %s | %d | ' % (nm, len(rows)) + ' | '.join(('%.3f' % cd[d]['rate']) if d in cd else '' for d in range(1, 13)) + ' | %s | %s |' % (f, xi))
    print('\n(small maps, ../TABLES.md, D2 = DL one unlock away): ' + '; '.join('%s %s' % (k, v) for k, v in SMALL.items()))
    print('\n## Odd-degree split: unlock rate per swap for far chains (d >= 2) that do / do not contain an odd-degree vertex (rim excluded)\n')
    print('| set | d | swaps with odd vtx | unlock rate | swaps all-even | unlock rate |'); print('|---|---|---|---|---|---|')
    for nm, rows in SETS.items():
        rows = [r for r in rows if any('odd' in v for v in r['H'].values())]   # rows run with the flag
        if not rows: continue
        H, st, sh = agg(rows, 'DL')
        for d in sorted(H):
            h = H[d]
            if d < 2 or d > 8 or nm.startswith('pad') or 'odd' not in h and not any('unlock_odd' in r['H'].get('DL|%d' % d, {}) for r in rows): continue
            no, ne = h.get('odd', 0), h['n'] - h.get('odd', 0); uo = h.get('unlock_odd', 0); ue = h.get('unlockDL', 0) - uo
            if no + ne < 200: continue
            print('| %s | %d | %d | %s | %d | %s |' % (nm, d, no, '%.3f' % (uo / no) if no else '-', ne, '%.3f' % (ue / ne) if ne else '-'))
    for nm, rows in SETS.items():
        print('\n## %s' % nm)
        print(table(nm, rows, 'DL', 'unlockDL'))
        if any(r['mode'] == 'exact' for r in rows):
            print(table(nm, rows, 'D2', 'dF-1'))
        print()
        for l in onlyfar(rows): print('- ' + l)
    print('\n## By hole eccentricity: DL unlock rate per swap at d (ratio to d=1), bins with >= 200 swaps\n')
    print('| set | ecc | holes | DL states | d:rate(ratio) |'); print('|---|---|---|---|---|')
    for nm, rows in SETS.items():
        for l in by_ecc(nm, rows, 'DL', 'unlockDL'): print(l)
    # pad: per base hole, rate at d for each k (pooled over bases)
    print('\n## Padding: DL unlock rate per swap at d, by number of bands k (pooled over base holes)\n')
    for mode in ('exact', 'sample'):
        rows = [r for r in R.get('c_pad_' + mode, []) if r['mode'] == mode]
        if not rows: continue
        print('\n%s mode\n' % mode)
        print('| k | holes | ecc | ' + ' | '.join('d=%d' % d for d in range(1, 11)) + ' |')
        print('|---|---|---|' + '---|' * 10)
        for k in range(5):
            rs = [r for r in rows if r.get('k') == k]
            if not rs: continue
            c, ns = curve(rs, 'DL', 'unlockDL'); cd = {r['d']: r for r in c}
            print('| %d | %d | %s | ' % (k, len(rs), eccs(rs)) + ' | '.join(
                ('%.3f' % cd[d]['rate'] + ('*' if cd[d]['n'] < 200 else '')) if d in cd else '' for d in range(1, 11)) + ' |')
        print('\n(swaps per DL state at d)\n')
        print('| k | ' + ' | '.join('d=%d' % d for d in range(1, 11)) + ' |'); print('|---|' + '---|' * 10)
        for k in range(5):
            rs = [r for r in rows if r.get('k') == k]
            if not rs: continue
            c, ns = curve(rs, 'DL', 'unlockDL'); cd = {r['d']: r for r in c}
            print('| %d | ' % k + ' | '.join('%.3f' % cd[d]['per_state'] if d in cd else '' for d in range(1, 11)) + ' |')
    # plots
    fig, ax = plt.subplots(1, 3, figsize=(16, 4.6))
    cols = plt.cm.tab20.colors
    for i, (nm, rows) in enumerate(SETS.items()):
        if nm.startswith('pad') and 'k=0' not in nm and 'k=4' not in nm: continue
        c0, _ = curve(rows, 'DL', 'unlockDL'); ok = {r['d'] for r in c0 if r['n'] >= 200}
        HW = True; c, ns = curve(rows, 'DL', 'unlockDL'); HW = False
        c = [r for r in c if r['d'] in ok and r['rate'] > 0]
        if not c: continue
        ls = '-' if 'exact' in nm else '--'
        ax[0].semilogy([r['d'] for r in c], [r['rate'] for r in c], ls, marker='o', color=cols[i % 20], label=nm)
        ax[1].semilogy([r['d'] for r in c], [r['per_state'] for r in c], ls, marker='o', color=cols[i % 20])
        ax[2].semilogy([r['d'] for r in c], [r['succ_shell'] for r in c], ls, marker='o', color=cols[i % 20])
    for nm, v in SMALL.items():
        ax[0].semilogy(range(1, 5), v, ':', color='k', marker='x', label=nm)
    ax[0].set_title('P(swap at d unlocks a DL state), holes weighted equally'); ax[1].set_title('swaps available per DL state')
    ax[2].set_title('unlocking swaps per DL state per shell vertex')
    for x in ax: x.set_xlabel('d(K)'); x.grid(alpha=.3, which='both')
    ax[0].legend(fontsize=6); fig.tight_layout(); fig.savefig('plots/DL_unlock_large.png', dpi=90); plt.close(fig)
