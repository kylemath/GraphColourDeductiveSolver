"""Planar features (coordinator request): (a) H_t side sizes, (b) figure-eight region areas and the
local side data at v, (c) chord side swaps between consecutive Hamiltonian states.  planar_stats.py prefix"""
import sys, json, gzip
from collections import defaultdict, Counter
pref = sys.argv[1]
runs = defaultdict(list)
for l in gzip.open(pref + '_feat.jsonl.gz', 'rt'):
    r = json.loads(l)
    if r['kind'] == 'planar': runs[r['run']].append(r)
meta = {r['id']: r for r in json.load(gzip.open(pref + '_runs.json.gz', 'rt'))}
C = Counter(); dA = Counter(); d2 = Counter(); aOc = Counter(); f8 = Counter(); sw = Counter(); swr = []
mono_aX = Counter()
for rid, s in runs.items():
    s.sort(key=lambda r: r['t']); m = meta[rid]; n = m['n']; tot = (n + 6) // 2
    for r in s:
        f8[(r['f8_regions'], r['f8_ok'])] += 1
        aOc[r['aO'] - (tot - 1) // 2] += 1
        if 'hA' in r:
            dA[r['hA'] - r['hB']] += 1
            C['hamstates'] += 1; C['hA_link_ok'] += r['hA_link_ok']
    hs = [r for r in s if 'hA' in r]
    for a, b in zip(hs, hs[1:]):
        if b['t'] - a['t'] != 2: continue
        d2[b['hA'] - a['hA']] += 1
        # chord side swaps: chords of H_t (with side) vs chords of H_{t+2}
        A0 = set(a['_sideA']); A1 = set(b['_sideA'])
        Ms = [set(M) for M in m['M']]
        H0 = Ms[a['t'] - 1] | Ms[a['t']]; H1 = Ms[b['t'] - 1] | Ms[b['t']]
        E = set(range(len(m['line'].split()) // 2))  # rough upper bound, not used
        C0 = None
        # all dual edges: chords = complement of H
        m_edges = int(m['line'].split()[1]); allE = set(range(m_edges))
        C0 = allE - H0; C1 = allE - H1
        B0 = C0 - A0; B1 = C1 - A1
        pers = C0 & C1
        key = dict(persA_A=len(pers & A0 & A1), persB_B=len(pers & B0 & B1), persA_B=len(pers & A0 & B1),
                   persB_A=len(pers & B0 & A1), outA=len((C0 - C1) & A0), outB=len((C0 - C1) & B0),
                   inA=len((C1 - C0) & A1), inB=len((C1 - C0) & B1), nchords=len(C0))
        swr.append(key)
        sw['side_flips'] += key['persA_B'] + key['persB_A']; sw['steps'] += 1
    # aX monotone along the run?
    xs = [r['aX'] for r in s]
    mono_aX['up' if all(b >= a for a, b in zip(xs, xs[1:])) else 'down' if all(b <= a for a, b in zip(xs, xs[1:])) else 'no'] += 1
print('planar runs', len(runs), 'states', sum(len(s) for s in runs.values()))
print('(b) figure-eight regions (count, frame-consistent):', dict(f8))
print('(b) aO - (faces-1)//2 :', dict(sorted(aOc.items())))
print('(a) Hamiltonian states', C['hamstates'], 'side A holds x_{k+1},x_{k+2} and not x_{k+3}:', C['hA_link_ok'])
print('(a) hA - hB at Hamiltonian states:', dict(sorted(dA.items())))
print('(a) hA(t+2) - hA(t):', dict(sorted(d2.items())))
print('(c) H_t -> H_{t+2} steps', sw['steps'], 'persistent chords changing side:', sw['side_flips'])
agg = Counter()
for k in swr:
    for a, b in k.items(): agg[a] += b
print('(c) totals over steps:', dict(agg))
print('(c) per-step (outA,outB,inA,inB) distribution:', Counter((k['outA'], k['outB'], k['inA'], k['inB']) for k in swr).most_common(12))
print('aX monotone along run:', dict(mono_aX))
