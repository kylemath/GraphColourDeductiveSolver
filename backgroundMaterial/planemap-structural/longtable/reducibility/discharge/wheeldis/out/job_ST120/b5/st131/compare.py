#!/usr/bin/env python3
"""ST-131: compare the Studio rotation-aware failure census (st131/census<d>.tsv: link, ub, DFS path code=class) with
W6r's mirror_only_states.tsv (d, link, apexes, privates 3/site, hi, lo, plain killer, mirror-only configs, recheck).
Our state -> W6r leaf format: apex s_j = its letter if its class is a singleton exact letter, else 9; private
p_i.(k+1) likewise (9 when absent, non-host or in a 9-class); W6r privates: 3 per site, first npriv(L) entries real.
States are compared up to the dihedral group of the window (rotations; reflection j -> -j with s_j -> s_{-j-1} and the
privates of a site reversed). For each state: mirror-only configs = configs with a rotation-blind embedding but no
rotation-respecting one (rotcheck), computed on the filled 2-ball. One-side states are re-checked on rotcheck + rcore
(hi from the ledger). usage: python3 -I compare.py D [D ...]"""
import os, sys, collections
H = os.path.dirname(os.path.abspath(__file__)); B5 = os.path.normpath(os.path.join(H, '..'))
sys.path.insert(0, os.path.join(B5, 'py'))
import export_cert as E, rotcheck as RC
R = E.R; R.U_HOST_ALWAYS = True
KC = [l for l in open(os.path.join(B5, 'st127', 'k767_kc.txt')) if l.strip()]
NAMES = [l.split()[0] for l in KC]
PREP = [E.prep_kc(l) for l in KC]
R.PARTS[:] = E.load_parts_file(os.path.join(B5, 'cert', 'parts79.txt'))

def canon(link, apex, priv):
    d = len(link); best = None
    for refl in (False, True):
        for r in range(d):
            if not refl:
                L = tuple(link[(j + r) % d] for j in range(d)); A = tuple(apex[(j + r) % d] for j in range(d))
                P = tuple(priv[(j + r) % d] for j in range(d))
            else:
                L = tuple(link[(-j + r) % d] for j in range(d)); A = tuple(apex[(-j - 1 + r) % d] for j in range(d))
                P = tuple(tuple(reversed(priv[(-j + r) % d])) for j in range(d))
            k = (L, A, P)
            if best is None or k < best: best = k
    return best

def ours(d):
    out = []
    for l in open(os.path.join(H, 'census%d.tsv' % d)):
        w, ub, path = l.rstrip('\n').split('\t')
        link = [int(c) for c in w]; st = {}
        for t in path.split():
            c, S = t.split('='); st[int(c)] = [int(x) for x in S]
        lt = lambda c: st[c][0] if c in st and len(st[c]) == 1 and st[c][0] <= 8 else 9
        apex = [lt(100 + j) for j in range(d)]
        priv = [tuple(9 if (link[i] >= 9 and k == 1) else lt(200 + 3 * i + k) for k in range(R.npriv(link[i]))) for i in range(d)]
        out.append((link, apex, priv, int(ub)))
    return out

def theirs(d):
    out = []
    for l in open(os.path.join(H, 'w6r', 'mirror_only_states.tsv')):
        f = l.rstrip('\n').split('\t')
        if f[0] != str(d): continue
        link = [int(c) for c in f[1]]; apex = [int(c) for c in f[2]]; pv = [int(c) for c in f[3]]
        priv = [tuple(pv[3 * i + k] for k in range(R.npriv(link[i]))) for i in range(d)]
        out.append((link, apex, priv, int(f[4]), f[7].split(',')))
    return out

def check_state(link, apex, priv):
    """hi (ledger) and, per config, rot-respecting / blind embeddings on the filled 2-ball."""
    d = len(link); W = R.Window(d, link, apex)
    f = {}
    for i in range(d):
        for k, x in enumerate(priv[i]): f['p%d.%d' % (i, k + 1)] = x
    lo, hi, _ = R.ledger(d, R.instances(W), f)
    host, adj, var = R.window_hostgraph(W)
    # fix the private letters: drop privates whose letter is not exact / not the needed one
    rot, blind = set(), set()
    for ci, p in enumerate(PREP):
        deg, Ek, order = p['deg'], p['E'], p['order']; m = len(order)
        if m > len(host): continue
        phi = {}; used = set(); found = [False, False]
        def letter(h):
            if h in var:
                nm = var[h]
                if nm[0] == 'p': return f[nm] if f[nm] <= 8 else None
                return None
            return next(iter(host[h]))
        def rec(k):
            if found[0]: return
            if k == m:
                found[1] = True
                letters = {h: (W.link[h[1]] if h[0] == 'w' else d if h == 'u' else deg[x]) for x, h in phi.items()}
                if RC.chirality(W, dict(phi), p['cyc'], letters)[0]: found[0] = True
                return
            x = order[k]; nb = [y for y in order[:k] if y in Ek[x]]
            for t in (adj[phi[nb[0]]] if nb else host.keys()):
                if t in used or letter(t) != deg[x]: continue
                if any((y in Ek[x]) != (phi[y] in adj[t]) for y in order[:k]): continue
                phi[x] = t; used.add(t); rec(k + 1); del phi[x]; used.discard(t)
        rec(0)
        if found[0]: rot.add(NAMES[ci])
        elif found[1]: blind.add(NAMES[ci])
    return hi, rot, blind

def main():
    rep = []
    for d in map(int, sys.argv[1:]):
        O = ours(d); T = theirs(d)
        co = collections.defaultdict(list); ct = collections.defaultdict(list)
        for s in O: co[canon(s[0], s[1], s[2])].append(s)
        for s in T: ct[canon(s[0], s[1], s[2])].append(s)
        wo = set(k[0] for k in co); wt = set(k[0] for k in ct)
        rep.append('d%d: ours %d leaves / %d distinct states / %d dihedral link words; W6r %d leaves / %d states / %d link words'
                   % (d, len(O), len(co), len(wo), len(T), len(ct), len(wt)))
        both = set(co) & set(ct); onlyo = set(co) - set(ct); onlyt = set(ct) - set(co)
        rep.append('  states in both %d, only ours %d, only W6r %d; link words both %d, only ours %d, only W6r %d'
                   % (len(both), len(onlyo), len(onlyt), len(wo & wt), len(wo - wt), len(wt - wo)))
        # mirror-only configs per side (W6r column for theirs; computed for ours)
        cfo = collections.Counter(); cft = collections.Counter()
        for s in T:
            for n in s[4]: cft[n] += 1
        bad = []
        for k in co:
            hi, rot, blind = check_state(list(k[0]), list(k[1]), [list(x) for x in k[2]])
            for n in blind: cfo[n] += 1
            if rot or hi <= 0: bad.append((k, hi, sorted(rot)))
        rep.append('  our states re-checked on the filled 2-ball: %d with hi <= 0 or a rotation-respecting kill %s'
                   % (len(bad), bad[:3]))
        rep.append('  mirror-only configs ours (states): %s' % dict(cfo.most_common()))
        rep.append('  mirror-only configs W6r (leaves): %s' % dict(cft.most_common()))
        rep.append('  only ours: %s; only W6r: %s' % (sorted(set(cfo) - set(cft)), sorted(set(cft) - set(cfo))))
        for k in sorted(onlyt)[:12]:
            hi, rot, blind = check_state(list(k[0]), list(k[1]), [list(x) for x in k[2]])
            rep.append('  W6r-only state %s/%s/%s: hi %d, rotation-respecting kills %s, mirror-only %s'
                       % (''.join(map(str, k[0])), ''.join(map(str, k[1])), '.'.join(''.join(map(str, x)) for x in k[2]), hi, sorted(rot), sorted(blind)))
        for k in sorted(onlyo)[:12]:
            hi, rot, blind = check_state(list(k[0]), list(k[1]), [list(x) for x in k[2]])
            rep.append('  ours-only state %s/%s/%s: hi %d, rotation-respecting kills %s, mirror-only %s'
                       % (''.join(map(str, k[0])), ''.join(map(str, k[1])), '.'.join(''.join(map(str, x)) for x in k[2]), hi, sorted(rot), sorted(blind)))
        print('\n'.join(rep[-8:]), flush=True)
    open(os.path.join(H, 'compare_%s.txt' % '_'.join(sys.argv[1:])), 'w').write('\n'.join(rep) + '\n')

if __name__ == '__main__':
    main()
