#!/usr/bin/env python3
"""[exploratory] NightImagesBoundary: where the sigma-images of Gamma-cycles land, by lock kind (Lemma P position) and by
the target cycle's excursion structure. Engine lib26.Eng via jobaq.load (as Job BI / NightStatementC cls.py).
Per class with a Gamma-cycle: every pi-cycle's (L, Lambda, F, #N0, #L1, #L2, #DL, #exc, max u, max f); the full sigma kind
matrix on the class's unfilled states; every Gamma-cycle's images (target cycle, target kind, fixed?)."""
import sys, os, json, glob
from collections import Counter
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__)); P27 = os.path.join(HERE, '../27-studio-positive-config'); C36 = os.path.join(HERE, '../36-nightstatementc')
for d in ('jobaq', '../26-transport-adversarial', '../25-transport', '../common', '../22-winding-escape'): sys.path.insert(0, os.path.join(P27, d))
import jobaq
def account(args):
    tag, path, mirror = args
    src = json.load(open(path)); hole = src['hole']
    jobaq.GDIR = os.path.join(HERE, 'gl') + '/'; os.makedirs(jobaq.GDIR, exist_ok=True); gname = os.path.basename(path)[:-5]
    lk = jobaq.GDIR + 'best-%s.json' % gname
    if not os.path.lexists(lk):
        try: os.symlink(os.path.abspath(path), lk)
        except FileExistsError: pass
    E, adj, link, w = jobaq.load(gname, hole, mirror)
    li = E.li; lc = lambda s: [s[i] for i in li]; done = set(); out = []
    def jj(c):
        cnt = Counter(c); return next(j for j in range(5) if c[j] == c[(j + 2) % 5] and cnt[c[j]] == 2)
    def lockinfo(s):
        if E.is_filled(s): return 'F'
        c = lc(s); j = jj(c); mu, A, B = c[(j + 1) % 5], c[(j + 3) % 5], c[(j + 4) % 5]
        l1 = E.comp(s, li[(j + 1) % 5], mu, A) >> li[(j + 3) % 5] & 1; l2 = E.comp(s, li[(j + 1) % 5], mu, B) >> li[(j + 4) % 5] & 1
        return {(0, 0): 'N0', (1, 0): 'L1', (0, 1): 'L2', (1, 1): 'DL'}[(l1, l2)]
    def sigma(s):
        c = lc(s); j = jj(c); al, mu = c[j], c[(j + 1) % 5]
        return E.swap(s, E.comp(s, li[(j + 1) % 5], al, mu), al, mu)
    from kempe_py import Space
    sp = Space({v: set(a) for v, a in adj.items()}, hole, link=link)
    for s0 in sp.states:
        if s0 in done: continue
        mem = E.bfs(s0); done |= set(mem)
        pi = {}; lam = {}
        for x in mem: pi[x], lam[x] = E.pi_of(x)
        kind = {x: lockinfo(x) for x in mem}
        cyc = {}; cycles = []
        for x in mem:
            if x in cyc: continue
            z = []; y = x
            while y not in cyc: cyc[y] = len(cycles); z.append(y); y = pi[y]
            cycles.append(z)
        G = [c for c, z in enumerate(cycles) if all(kind[x] == 'DL' for x in z)]
        if not G: continue
        part = {}
        for x in mem:
            if kind[x] != 'F': part[x] = sigma(x)
        cy = []
        for z in cycles:
            k = Counter(kind[x] for x in z); umax = fmax = 0; run = 0; frun = 0
            # runs along the cycle (start at a filled->unfilled boundary if any)
            n = len(z); st = next((i for i in range(n) if kind[z[i - 1]] == 'F' and kind[z[i]] != 'F'), 0)
            for t in range(n):
                x = z[(st + t) % n]
                if kind[x] == 'F': frun += 1; fmax = max(fmax, frun); run = 0
                else: run += 1; umax = max(umax, run); frun = 0
            pdl = sum(1 for x in z if x in part and part[x] != x and kind[part[x]] == 'DL')
            cy.append([n, sum(lam[x] for x in z), k['F'], k['N0'], k['L1'], k['L2'], k['DL'], k['N0'] + k['L2'], umax, fmax, pdl])
        sm = Counter(); imgs = {}
        for x in mem:
            if kind[x] == 'F': continue
            s = part[x]; assert s in cyc
            sm[(kind[x], 'fixed' if s == x else kind[s])] += 1
        for g in G:
            L = []
            for x in cycles[g]:
                s = sigma(x); L.append([cyc[s], 'fixed' if s == x else kind[s], int(cyc[s] in G)])
            imgs[g] = L
        out.append(dict(tag=tag, orientation='mirror' if mirror else 'plantri', N=len(mem), cycles=cy, gamma=G,
                        smat={'%s>%s' % k: v for k, v in sm.items()}, imgs={str(k): v for k, v in imgs.items()}))
    return out
if __name__ == '__main__':
    which = sys.argv[1]
    if which == 'census':
        jobs = [('census:' + os.path.basename(p)[:-5], p, m) for p in sorted(glob.glob(os.path.join(C36, 'census/*.json'))) for m in (False, True)]
    else:
        V = json.load(open(os.path.join(P27, 'jobaw/jobaw-verified.json'))); jobs = []; seen = set()
        for v in V:
            p = os.path.join(P27, 'jobaw', v['file'])
            if p in seen: continue
            seen.add(p); jobs += [(v['file'], p, m) for m in (False, True)]
    with Pool(2) as P: res = [x for xs in P.imap_unordered(account, jobs) for x in xs]
    json.dump(res, open(os.path.join(HERE, 'ib-%s.json' % which), 'w'))
    print('class records', len(res))
