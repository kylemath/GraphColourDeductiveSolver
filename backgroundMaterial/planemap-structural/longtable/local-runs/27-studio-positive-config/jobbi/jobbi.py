#!/usr/bin/env python3
"""Job BI [exploratory]: full sigma / sigma' accounting for every Gamma-cycle Z in the hole's Kempe classes (all states; lib26.Eng via jobaq.load; both orientations).
Per Z: Lambda(Z) = 5w = L. For every state x of Z (all are DD endpoints): sigma(x) and every sigma' image (link-free swap from x whose result is not DL and lies on another cycle).
Image kind (fixed / lockless / Lock1-only / Lock2-only / DL / filled), target cycle T (w, L, Lambda), the excursion e of T containing the image (u = unfilled run length, f = filled
states after it, mass = u - 3f; lockless images have u = 1 and credit 3f - 1 = -mass).
rem(T) = Lambda(T) + sum of lockless credits landing on T (sigma exits of positive cycles, as Job AQ). Tests per Z:
 (a) Lemma S, sigma only (Job AQ C_neg) and sigma u sigma' (distinct lockless images on nonpositive T) : credit >= Lambda(Z)
 (b) P1^str: some sigma-neighbour T (nonpositive) with -rem(T) >= Lambda(Z); also with sigma u sigma' neighbours
 (c) some sigma-image (any kind, non-fixed) lands on T with Lambda(T) <= -Lambda(Z); also via sigma'
 (d) excursion credit: sum over DISTINCT target excursions (sigma images, nonpositive T) of max(0, -mass) >= Lambda(Z); the same with sigma u sigma'
 (e) charge-back P1 (Job AQ) for the class, and the T that pays Z (cap, def')."""
import sys, os, json, itertools
from fractions import Fraction
from collections import Counter, defaultdict
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__))
for d in ('../jobaq', '../../26-transport-adversarial', '../../25-transport', '../../common', '../../22-winding-escape'): sys.path.insert(0, os.path.join(HERE, d))
import jobaq
from kempe_py import Space
def account(args):
    tag, gdir, gname, hole, mirror = args
    jobaq.GDIR = gdir
    E, adj, link, w = jobaq.load(gname, hole, mirror)
    deg = [len(adj[x]) for x in link]
    if sorted(deg) not in ([5, 5, 5, 5, 6], [5, 5, 5, 5, 7]): return []
    sp = Space({v: set(a) for v, a in adj.items()}, hole, link=link); assert sp.order == E.order
    li = E.li; lc = lambda s: [s[i] for i in li]; done = set(); out = []
    def lockinfo(s):
        if E.is_filled(s): return 'filled'
        c = lc(s); cnt = Counter(c); j = next(j for j in range(5) if c[j] == c[(j + 2) % 5] and cnt[c[j]] == 2); mu, A, B = c[(j + 1) % 5], c[(j + 3) % 5], c[(j + 4) % 5]
        l1 = E.comp(s, li[(j + 1) % 5], mu, A) >> li[(j + 3) % 5] & 1; l2 = E.comp(s, li[(j + 1) % 5], mu, B) >> li[(j + 4) % 5] & 1
        return {(0, 0): 'lockless', (1, 0): 'Lock1-only', (0, 1): 'Lock2-only', (1, 1): 'DL'}[(l1, l2)]
    def sigma(s):
        c = lc(s); cnt = Counter(c); j = next(j for j in range(5) if c[j] == c[(j + 2) % 5] and cnt[c[j]] == 2); al, mu = c[j], c[(j + 1) % 5]
        return E.swap(s, E.comp(s, li[(j + 1) % 5], al, mu), al, mu)
    for s0 in sp.states:
        if s0 in done: continue
        mem = E.bfs(s0); done |= set(mem)
        pi = {}; lam = {}
        for x in mem: pi[x], lam[x] = E.pi_of(x)
        cyc = {}; cycles = []
        for x in mem:
            if x in cyc: continue
            z = []; y = x
            while y not in cyc: cyc[y] = len(cycles); z.append(y); y = pi[y]
            cycles.append(z)
        W = [sum(lam[y] for y in z) // 5 for z in cycles]; Lam = [5 * x for x in W]
        kind = {x: lockinfo(x) for x in mem}
        G = [c for c, z in enumerate(cycles) if all(kind[x] == 'DL' for x in z)]
        if not G: continue
        pos = {}
        for c, z in enumerate(cycles):
            for i, x in enumerate(z): pos[x] = i
        exc_cache = {}
        def excursion(s):
            c = cyc[s]; z = cycles[c]; L = len(z)
            if kind[s] == 'filled': return None
            i = pos[s]; a = i
            while kind[z[(a - 1) % L]] != 'filled' and (i - a) < L: a -= 1
            if i - a >= L: return dict(cycle=c, start=0, u=L, f=0, mass=L)   # all-unfilled cycle
            u = 0; t = a
            while kind[z[t % L]] != 'filled': u += 1; t += 1
            f = 0
            while kind[z[t % L]] == 'filled': f += 1; t += 1
            return dict(cycle=c, start=a % L, u=u, f=f, mass=u - 3 * f)
        def fafter(s):
            y = pi[s]; f = 0
            while kind[y] == 'filled': f += 1; y = pi[y]
            return f
        pinv = {pi[x]: x for x in mem}; isDD = lambda x: kind[x] == 'DL' and (kind[pi[x]] == 'DL' or kind[pinv[x]] == 'DL')
        # class-wide sigma exits (Job AQ convention) for rem and charge-back
        sig = defaultdict(set); sigp = defaultdict(set); exits = {}; pexits = {}
        for x in mem:
            if not isDD(x): continue
            s = sigma(x); a, b = cyc[x], cyc[s]
            if a != b:
                sig[a].add(b); sig[b].add(a)
                if W[a] > 0 and kind[s] == 'lockless': exits.setdefault(s, (a, 3 * fafter(s) - 1))
            for t, p, q, K in E.moves(x):
                if t == x or K & E.linkmask or kind[t] == 'DL' or cyc[t] == a: continue
                sigp[a].add(cyc[t]); sigp[cyc[t]].add(a)
                if W[a] > 0 and kind[t] == 'lockless': pexits.setdefault(t, (a, 3 * fafter(t) - 1))
        src = defaultdict(lambda: defaultdict(int)); crN = defaultdict(int)
        for s, (a, cr) in exits.items():
            if W[cyc[s]] <= 0: src[cyc[s]][a] += cr; crN[a] += cr
        rem = {t: Lam[t] + sum(src[t].values()) for t in range(len(cycles)) if W[t] <= 0}
        charge = defaultdict(Fraction)
        for t, r in rem.items():
            if r > 0 and src[t]:
                tot = sum(src[t].values())
                for a, cr in src[t].items(): charge[a] += Fraction(r * cr, tot)
        cap = {t: Fraction(-r) for t, r in rem.items() if r < 0}
        defs = sorted([(z, Lam[z] - crN[z] + charge[z], [t for t in sig[z] if t in cap]) for z in range(len(cycles)) if W[z] > 0 and Lam[z] - crN[z] + charge[z] > 0], key=lambda d: -d[1])
        used = defaultdict(Fraction); assign = {}
        def bt(i):
            if i == len(defs): return True
            z, d, nb = defs[i]
            for t in sorted(nb, key=lambda t: -(cap[t] - used[t])):
                if cap[t] - used[t] >= d:
                    used[t] += d; assign[z] = t
                    if bt(i + 1): return True
                    used[t] -= d; assign.pop(z, None)
            return False
        p1 = bt(0)
        for gc in G:
            z = cycles[gc]; LZ = Lam[gc]; imgs = []
            for x in z:
                s = sigma(x); e = excursion(s) if s != x else None
                imgs.append(dict(via='sigma', kind='fixed' if s == x else kind[s], same=cyc[s] == gc, T=cyc[s], Tw=W[cyc[s]], TL=len(cycles[cyc[s]]), exc=e,
                                 credit=(3 * fafter(s) - 1) if s != x and kind[s] == 'lockless' else 0))
                for t, p, q, K in E.moves(x):
                    if t == x or K & E.linkmask or kind[t] == 'DL' or cyc[t] == gc: continue
                    imgs.append(dict(via='sigmap', kind=kind[t], same=False, T=cyc[t], Tw=W[cyc[t]], TL=len(cycles[cyc[t]]), exc=excursion(t), credit=(3 * fafter(t) - 1) if kind[t] == 'lockless' else 0, state=hash(t)))
            S_sig = [i for i in imgs if i['via'] == 'sigma' and i['kind'] != 'fixed' and not i['same']]
            crA = sum(i['credit'] for i in S_sig if i['Tw'] <= 0)
            seenL = {}
            for i in imgs:
                if i['kind'] == 'lockless' and i['Tw'] <= 0 and not i['same']: seenL[(i['T'], i['exc']['start'])] = i['credit']
            crB = sum(seenL.values())
            nbS = {i['T'] for i in S_sig if i['Tw'] <= 0}; nbSP = nbS | {i['T'] for i in imgs if i['via'] == 'sigmap' and i['Tw'] <= 0}
            ex1 = {(i['T'], i['exc']['start']): -i['exc']['mass'] for i in S_sig if i['Tw'] <= 0 and i['exc']}
            ex2 = dict(ex1); ex2.update({(i['T'], i['exc']['start']): -i['exc']['mass'] for i in imgs if i['via'] == 'sigmap' and i['Tw'] <= 0 and i['exc']})
            rec = dict(tag=tag, graph=gname, hole=hole, orientation='mirror' if mirror else 'plantri', linkdeg=sorted(deg), class_states=len(mem), class_sumw=sum(W), L=len(z), Lambda=LZ,
                       a_sigma=crA >= LZ, crA=crA, a_sigma_sigmap=crB >= LZ, crB=crB,
                       b_P1str_sigma=any(-rem[t] >= LZ for t in nbS if t in rem), b_P1str_sigma_sigmap=any(-rem[t] >= LZ for t in nbSP if t in rem),
                       best_rem_sigma=max([-rem[t] for t in nbS if t in rem] + [None], key=lambda v: -10**9 if v is None else v),
                       c_sigma=any(Lam[i['T']] <= -LZ for i in S_sig), c_sigma_sigmap=any(Lam[i['T']] <= -LZ for i in imgs if not i['same'] and i['kind'] != 'fixed'),
                       d_exc_sigma=sum(max(0, v) for v in ex1.values()) >= LZ, exc_sigma=sum(max(0, v) for v in ex1.values()),
                       d_exc_sigma_sigmap=sum(max(0, v) for v in ex2.values()) >= LZ, exc_sigma_sigmap=sum(max(0, v) for v in ex2.values()),
                       P1_class=p1, def_prime=str(Lam[gc] - crN[gc] + charge[gc]), paid_by=(assign.get(gc), str(cap.get(assign.get(gc))) if assign.get(gc) is not None else None,
                                                                                         Lam[assign[gc]] if gc in assign else None, len(cycles[assign[gc]]) if gc in assign else None),
                       sigma_images=[dict(k=i['kind'], T=(i['Tw'], i['TL']), exc=(i['exc']['u'], i['exc']['f'], i['exc']['mass']) if i['exc'] else None, cr=i['credit']) for i in S_sig],
                       sigma_kinds=dict(Counter(i['kind'] for i in imgs if i['via'] == 'sigma')), sigmap_count=sum(1 for i in imgs if i['via'] == 'sigmap'),
                       sigmap_lockless_credit=sum(i['credit'] for i in imgs if i['via'] == 'sigmap' and i['Tw'] <= 0))
            out.append(rec)
    return out
if __name__ == '__main__':
    jobs = []
    V = json.load(open(os.path.join(HERE, '../jobaw/jobaw-verified.json')))
    hd = os.path.join(HERE, 'hitgraphs/'); os.makedirs(hd, exist_ok=True)
    for i, v in enumerate(V):
        g = 'hit%02d' % i
        src = json.load(open(os.path.join(HERE, '../jobaw/', v['file']))) if v.get('file') else None
        if src is None:
            # re-find the faces from the walks file
            for l in open(os.path.join(HERE, '../jobaw/jobaw-walks.jsonl')):
                r = json.loads(l)
                for h in r['hits']:
                    if r['seed'] == v['seed'] and r['objective'] == v['objective'] and r['walk'] == v['walk'] and h['it'] == v['it']: src = dict(faces=h['faces'], hole=r['hole'])
        json.dump(src, open(hd + 'best-%s.json' % g, 'w'))
        for m in (False, True): jobs.append(('hit:%s/%s/w%d/it%d' % (v['seed'], v['objective'], v['walk'], v['it']), hd, g, src['hole'], m))
    if len(sys.argv) > 1 and sys.argv[1] == 'census':
        sys.path.insert(0, os.path.join(HERE, '../jobuv')); sys.path.insert(0, os.path.join(HERE, '../jobaw'))
        from jobag import canon
        from uv_lib import load
        from jobaw import faces_of_rot
        cd = os.path.join(HERE, 'censusgraphs/'); os.makedirs(cd, exist_ok=True); seen = set()
        for lab in ['z25', 'z26', 'z27']:
            for l in open(os.path.join(HERE, '../out/%s.jsonl' % lab)):
                if '"jobs": {"pos": [{' not in l: continue
                r = json.loads(l)
                if canon(r['linkdeg']) == (5, 5, 5, 5, 6) and any(z['gamma'] for z in r['jobs']['pos']) and (r['name'], r['hole']) not in seen:
                    seen.add((r['name'], r['hole'])); g = r['name'].replace('#', '_')
                    if not os.path.exists(cd + 'best-%s.json' % g): json.dump(dict(faces=faces_of_rot(load(r['name'], False))), open(cd + 'best-%s.json' % g, 'w'))
                    for m in (False, True): jobs.append(('census:' + r['name'], cd, g, r['hole'], m))
    with Pool(12) as P: res = [x for xs in P.imap_unordered(account, jobs) for x in xs]
    fn = 'jobbi-cycles%s.json' % ('-census' if len(sys.argv) > 1 else '')
    json.dump(res, open(os.path.join(HERE, fn), 'w'))
    print('Gamma-cycle records', len(res))
