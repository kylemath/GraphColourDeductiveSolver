import json, sys, collections, statistics as st
fn = sys.argv[1] if len(sys.argv) > 1 else '/mnt/project-files/multiscale/multicut/multifront/main.jsonl'
R = [json.loads(l) for l in open(fn)]
def fam(spec):
    p = spec.split(':'); mp = p[0]
    return mp, int(p[1]), p[3] if len(p) > 3 else ''
G = collections.defaultdict(list)
for r in R: G[fam(r['spec'])].append(r)
print('map m opts | runs ok(strict) ok(with waits) FAIL/STUCK/UNK | maxR | mind/diam | precontact peak cuts,|t| per front | global peak cuts,|t| | merges | ren')
for key in sorted(G, key=lambda k: (k[2], k[0], k[1])):
    rs = G[key]; ok = [r for r in rs if r['status'] == 'ok']; strict = [r for r in ok if r['nskip'] == 0]
    bad = collections.Counter(r['status'] for r in rs if r['status'] != 'ok')
    pc = []; pt = []; gc = []; gt = []; nm = []; nren = []
    for r in rs:
        recs = r['recs']; first = next((i for i, x in enumerate(recs) if x[3] == 'merge'), len(recs))
        pre = recs[:first]
        pc.append(max([max([w[1] for w in x[6]], default=0) for x in pre], default=0))
        pt.append(max([max([w[2] for w in x[6]], default=0) for x in pre], default=0))
        gc.append(max([max([w[1] for w in x[6]], default=0) for x in recs], default=0))
        gt.append(max([max([w[2] for w in x[6]], default=0) for x in recs], default=0))
        nm.append(sum(1 for x in recs if x[3] == 'merge')); nren.append(sum(1 for x in recs if x[12]))
    print(f"{key[0]:>16} {key[1]:>2} {key[2]:<11}| {len(rs):>2} {len(strict):>2} {len(ok):>2} {dict(bad)} | {max(r['maxR'] for r in rs)} | "
          f"{min((r['mind'] or 0) for r in rs)}/{rs[0]['diam']} | {st.mean(pc):.1f},{st.mean(pt):.1f} | {st.mean(gc):.1f},{st.mean(gt):.1f} (max {max(gc)},{max(gt):.1f}) | {st.mean(nm):.1f} | {sum(nren)}")
# ---- collision analysis ----
print('\n== events (all runs of each opts group): R histograms ==')
for opts in sorted(set(k[2] for k in G)):
    rr = [r for k, v in G.items() if k[2] == opts for r in v]
    for mfam in ('ico', 'L18', 'dense', 'rigid'):
        sel = [r for r in rr if (mfam == 'ico' and r['spec'].startswith('ico')) or (mfam == 'L18' and r['spec'].startswith('L18')) or
               (mfam == 'dense' and (r['spec'].startswith('defect') or r['spec'].startswith('flip'))) or (mfam == 'rigid' and r['spec'].startswith('rigid'))]
        sel = [r for r in sel if r['m'] > 1]
        if not sel: continue
        H = collections.defaultdict(collections.Counter)
        holes = []; skipcls = collections.Counter(); zip_after = collections.Counter()
        for r in sel:
            recs = r['recs']
            for i, x in enumerate(recs):
                k, tag, Rr, ev, nt, comps, W, dn, npos, nodd, hole, split, ren, ov = x
                if ev == 'merge': H['first contact (merge)'][Rr] += 1
                elif ev == 'close':
                    H['hole close, %s' % ('>=3 tags (V-vertex)' if hole and hole['tags'] >= 3 else '<=2 tags')][Rr] += 1
                    if hole: holes.append((hole['tags'], hole['t'], hole['L'], Rr, hole['odd']))
                elif ev == 'split': H['split (annulus/hole created), ntags=%s' % min(nt, 3)][Rr] += 1
                elif nt >= 3: H['junction step (>=3 tags, V-vertex)'][Rr] += 1
                elif nt == 2: H['seam step (2 tags, V-edge)'][Rr] += 1
                else: H['interior growth (1 tag)'][Rr] += 1
            for f in r['fails']:
                cl = max(f['ntags'], default=0); skipcls[('V-vertex' if cl >= 3 else 'V-edge' if cl == 2 else 'cell-interior')] += 1
        print(f'-- {opts} {mfam} ({len(sel)} runs, m>1)')
        for kk in sorted(H):
            c = H[kk]; tot = sum(c.values()); print(f'   {kk:<45} n={tot:>6}  R: {dict(sorted(c.items()))}  frac R>0 {1 - c[0]/tot:.3f}')
        print('   blocked turns (front waited) by candidate type:', dict(skipcls))
        if holes:
            v3 = [h for h in holes if h[0] >= 3]; v2 = [h for h in holes if h[0] < 3]
            for nm_, hs in (('V-vertex holes', v3), ('other holes', v2)):
                if not hs: continue
                tc = collections.Counter(h[1] for h in hs); print(f'   {nm_}: {len(hs)}; |t| of the hole walk just before closing: {dict(sorted(tc.items()))}; R at close: {dict(collections.Counter(h[3] for h in hs))}')
# ---- splits (holes created), final failures ----
print('\n== holes created by splits (smaller side), main opts, m>1 vs m=1 ==')
for opts in sorted(set(k[2] for k in G)):
    for mm in ('m=1', 'm>1'):
        hs = []
        for k_, v in G.items():
            if k_[2] != opts: continue
            for r in v:
                if (r['m'] == 1) != (mm == 'm=1'): continue
                for x in r['recs']:
                    if x[3] == 'split' and x[11]:
                        W = x[6]; sp = x[11]; i = min(range(len(sp)), key=lambda j: sp[j][0])
                        hs.append((sp[i][0], sp[i][1], W[i][2], W[i][1], x[4]))
        if not hs: continue
        big = [h for h in hs if h[0] >= 3]
        print(f'  {opts} {mm}: {len(hs)} holes, size dist {dict(collections.Counter(min(h[0], 20) for h in hs))}; holes with 0 odd inside and |t|>0: {sum(1 for h in hs if h[1] == 0 and h[2] > 0)}; |t| at creation {dict(collections.Counter(h[2] for h in hs))}')
print('\n== failing runs: where ==')
for r in R:
    if r['status'] == 'ok': continue
    f = r['fails'][-1] if r['fails'] else {}
    last = r['recs'][-1] if r['recs'] else None
    print(f"  {r['spec']:<28} {r['status']:<7} colored {r['colored']}/{r['n']} nodd {f.get('nodd')} cand ntags {f.get('ntags')} kinds {[c[1] for c in f.get('cands', [])]} lastW {last[6] if last else None} err {r.get('err')}")
