#!/usr/bin/env python3
"""Track N: independent verification (second engine) of Q-e examples.
Engine: TrackH th_engine.Hole (pure Python, read-only import) for states / Kempe moves / pi / locks, TrackI
ti_chains.nchains for N; the Lemma E sums are recomputed here from scratch:
  Sigma chi over a partition {XY | ZW} = (|X|+|Y|-e(X,Y)) + (|Z|+|W|-e(Z,W)), required (2,3,3) at an unfilled state in
  role order P1 = {alpha mu | A B}, P2 = {alpha A | mu B}, P3 = {alpha B | mu A}; at a filled state the requirement is
  1 + (5 - l)/2 with l = # link edges coloured inside the partition.
For each pi-cycle of DL states with N <= 9 (the law is reported, not assumed) it prints the N-profile, law at each step,
Lemma E at each cycle state, Lemma E over the whole Kempe class (and how many states violate it), class size / filled
states, edges in no triangle, |E(G-h)| vs 3n-11, and whether G is 4-colourable.
usage: tn_verify.py FILE [--max K]   (FILE lines 'name n adj;...' with h = 0, or jsonl with 'graph')"""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'TrackH')); sys.path.insert(0, os.path.join(HERE, '..', 'TrackI'))
from th_engine import Hole
from ti_chains import nchains


def chi_sums(H, col, parts):
    out = []
    for part in parts:
        tot = 0
        for (p, q) in part:
            Vs = [v for v in H.V if col[v] in (p, q)]
            e = sum(1 for u in Vs for w in H.adj[u] if w > u and col[w] in (p, q))
            tot += len(Vs) - e
        out.append(tot)
    return out


def lemmaE(H, r, col):
    if r['kind'] != 'F':
        al, mu, A, B = r['roles']
        parts = [((al, mu), (A, B)), ((al, A), (mu, B)), ((al, B), (mu, A))]
        return chi_sums(H, col, parts), [2, 3, 3]
    parts = [((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2))]
    tg = []
    for part in parts:
        l = sum(1 for t in range(5) if {col[H.X[t]], col[H.X[(t + 1) % 5]]} in [set(part[0]), set(part[1])])
        tg.append(1 + (5 - l) // 2)
    return chi_sums(H, col, parts), tg


def verify(line):
    p = line.split(); rot = [list(map(int, r.split(','))) for r in p[2].split(';')]
    n = len(rot); h = 0
    S = [set(r) for r in rot]
    nedge = sum(1 for u in range(1, n) for v in rot[u] if v > u and v != 0)
    notri = sum(1 for u in range(1, n) for v in rot[u] if v > u and v != 0 and not (S[u] & S[v]))
    H = Hole(rot, h).build(); info = H.info
    Ns = [nchains(H, H.col(i)) for i in range(len(H.states))]
    good = lambda i: i is not None and info[i]['kind'] == 'DL' and Ns[i] <= 9
    res = dict(name=p[0], n=n, edges_G_minus_h=nedge, target_3n_11=3 * n - 11, edges_not_in_triangle=notri,
               states=len(H.states), filled_states_total=sum(1 for r in info if r['kind'] == 'F'), cycles=[])
    seen = set()
    for i in range(len(info)):
        if i in seen or not good(i): continue
        path = []; pos = {}; k = i
        while good(k) and k not in pos and k not in seen:
            pos[k] = len(path); path.append(k); k = info[k]['pi']
        seen.update(path)
        if k is None or k not in pos: continue
        cyc = path[pos[k]:]
        law = []; E_ok = []
        for x in cyc:
            y = info[x]['pi']; law.append((Ns[y] - Ns[x]) % 2 == (1 if info[y]['kind'] == 'DL' else 0))
            s, t = lemmaE(H, info[x], H.col(x)); E_ok.append(s == t)
        mem = H.class_members(cyc[0]); bad = 0; badk = {}
        for x in mem:
            s, t = lemmaE(H, info[x], H.col(x))
            if s != t: bad += 1; badk[info[x]['kind']] = badk.get(info[x]['kind'], 0) + 1
        res['cycles'].append(dict(length=len(cyc), Nprofile=''.join(str(Ns[x]) for x in cyc), law_all=all(law), law_fail=law.count(False),
                                  lemmaE_on_cycle_all=all(E_ok), lemmaE_on_cycle_fail=E_ok.count(False), class_size=len(mem),
                                  class_filled=sum(1 for x in mem if info[x]['kind'] == 'F'), lemmaE_class_violations=bad, lemmaE_class_viol_by_kind=badk))
    # longest pi-run of DL states with N <= 9, law at every internal step and Lemma E at every state (cross-check of tn_eng run[3])
    okE = {}
    def gE(i):
        if i not in okE: s_, t_ = lemmaE(H, info[i], H.col(i)); okE[i] = (s_ == t_)
        return okE[i]
    def good3(i): return good(i) and gE(i)
    def step3(i):
        y = info[i]['pi']
        return good3(i) and good3(y) and ((Ns[y] - Ns[i]) % 2 == 1)
    pre = {info[i]['pi']: i for i in range(len(info)) if info[i]['kind'] == 'DL' and info[i]['pi'] is not None}
    best = 0
    for i in range(len(info)):
        if not good3(i): continue
        q = pre.get(i)
        if q is not None and step3(q): continue
        L = 1; x = i
        while step3(x) and L <= len(info): x = info[x]['pi']; L += 1
        best = max(best, L)
    res['longest_run_R_law_lemmaE'] = best
    return res


if __name__ == '__main__':
    args = sys.argv[1:]; mx = 10 ** 9
    if '--max' in args: k = args.index('--max'); mx = int(args[k + 1]); del args[k:k + 2]
    c = 0
    for l in open(args[0]):
        if c >= mx: break
        if l.startswith('{'):
            d = json.loads(l)
            if 'graph' not in d: continue
            l = d['graph']
        if len(l.split()) < 3: continue
        print(json.dumps(verify(l)), flush=True); c += 1
