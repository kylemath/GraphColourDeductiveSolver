#!/usr/bin/env python3
"""Track F section 9: aggregate out/lpc2/s_*.jsonl (lpc2_search logs) into tables, and pick items to verify.
Dedup: a cycle-class instance is (graph isomorphism class by WL hash, hole word, cls2 tuple); graphs by WL hash.
Writes out/lpc2/report.txt, out/lpc2/verify_items.jsonl.
usage: lpc2_report.py [MAXVERIFY_DIRTY=60]"""
import os, sys, json, glob, collections, random
import networkx as nx
D = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(D, '..', 'out', 'lpc2')
maxdirty = int(sys.argv[1]) if len(sys.argv) > 1 else 60

def wl(line):
    rot = line.split()[2].split(';'); G = nx.Graph()
    for v, r in enumerate(rot):
        for w in r.split(','): G.add_edge(v, int(w))
    return nx.weisfeiler_lehman_graph_hash(G, iterations=4)

prog = [json.loads(open(p).read()) for p in sorted(glob.glob(os.path.join(OUT, 's_*.progress')))]
ev = collections.Counter(); cyc_inst = {}; low_inst = {}; cex = []; graphs = collections.defaultdict(set)
wlc = {}
def origin(p):
    b = os.path.basename(p)
    return 'glue' if b.startswith('s_glue') else 'prevseed' if b.startswith('s_prevseed') else 'focus' if b.startswith('s_focus') else 'random'
for p in sorted(glob.glob(os.path.join(OUT, 's_*.jsonl'))):
    org = origin(p)
    for l in open(p):
        try: d = json.loads(l)
        except Exception: continue
        ev[d['ev']] += 1; g = d['graph']
        if g not in wlc: wlc[g] = wl(g)
        hsh = wlc[g]; key0 = (org, d['surface'], d['n'])
        if d['ev'] == 'cyc':
            graphs[key0].add(hsh)
            for c in d['cyc']:
                for cl in c['cyccls']:
                    k = (hsh, c['word'], tuple(cl))
                    if k not in cyc_inst: cyc_inst[k] = dict(origin=org, surface=d['surface'], n=d['n'], word=c['word'], cls=cl, hole=c['hole'], graph=g, allDLcyc=c['allDLcyc'], states=c['states'])
        elif d['ev'] == 'low':
            for c in d['low']:
                for cl in c['cls']:
                    k = (hsh, c['word'], tuple(cl))
                    if k not in low_inst: low_inst[k] = dict(origin=org, surface=d['surface'], n=d['n'], word=c['word'], cls=cl, hole=c['hole'], graph=g)
        elif d['ev'] == 'cex':
            cex.append(d)

R = []
def P(*a): R.append(' '.join(str(x) for x in a))
P('# lpc2 report'); P('events', dict(ev))
tw = collections.Counter(); te = collections.Counter(); tt = collections.Counter(); tel = collections.Counter()
for pr in prog:
    for s, b in pr['by_surface'].items(): tw[s] += b['walks']; te[s] += b['evals']
    tt['timeouts'] += pr.get('timeouts', 0); tel[pr['seed']] = pr.get('elapsed', 0)
P('walks', dict(tw)); P('evals', dict(te), 'total', sum(te.values())); P('kclass4 timeouts', tt['timeouts'], 'elapsed per worker (s)', dict(tel))
P(); P('## cycle classes at frame-like holes, by surface and n (distinct = (WL graph hash, hole word, class tuple))')
P('origin surface n | graphs | cycle-class instances | violator-free | min viol | min F/N (violator-free cyc) | min filled/onCycles (viol-free) | words')
tab = collections.defaultdict(list)
for k, v in cyc_inst.items(): tab[(v['origin'], v['surface'], v['n'])].append(v)
bys = collections.defaultdict(lambda: collections.Counter())
for key in sorted(tab):
    L = tab[key]; vf = [v for v in L if v['cls'][6] == 0]
    mfn = min((v['cls'][1] / v['cls'][0] for v in vf), default=None); mfc = min((v['cls'][1] / v['cls'][7] for v in vf), default=None)
    P(key[0], key[1], key[2], '|', len(graphs[key]), '|', len(L), '|', len(vf), '|', min(v['cls'][6] for v in L), '|',
      None if mfn is None else round(mfn, 4), '|', None if mfc is None else round(mfc, 3), '|', dict(collections.Counter(v['word'] for v in L)))
    b = bys[(key[0], key[1])]; b['graphs'] += len(graphs[key]); b['inst'] += len(L); b['vf'] += len(vf)
P(); P('## totals by surface');
for s, b in sorted(bys.items()):
    L = [v for v in cyc_inst.values() if (v['origin'], v['surface']) == s]; vf = [v for v in L if v['cls'][6] == 0]
    P(s, dict(b), 'min filled/onCycles (viol-free)', min((round(v['cls'][1] / v['cls'][7], 3) for v in vf), default=None), 'minviol', min(v['cls'][6] for v in L), 'violator-free min F/N', min((round(v['cls'][1] / v['cls'][0], 4) for v in vf), default=None),
      'cycle lengths', dict(collections.Counter(x for v in L for x in v['allDLcyc'])))
P(); P('## violator-free cycle classes (signature [size,filled,DL,single,minK,maxK,viol,onCycles,pathEnds] -> count)')
P(dict(collections.Counter((v['origin'], v['surface'], v['word'], tuple(v['cls'])) for v in cyc_inst.values() if v['cls'][6] == 0).most_common()))
P(); P('## the 15 lowest-F/N violator-free cycle classes')
for v in sorted([v for v in cyc_inst.values() if v['cls'][6] == 0], key=lambda v: v['cls'][1] / v['cls'][0])[:15]: P(v['origin'], v['surface'], v['n'], v['word'], v['cls'], round(v['cls'][1] / v['cls'][0], 4), v['graph'].split()[0], 'h', v['hole'])
P(); P('## violators in cycle classes: histogram of viol'); P(dict(sorted(collections.Counter(v['cls'][6] for v in cyc_inst.values()).items())))
P(); P('## violator-free classes with F/N <= 1/4 at frame-like holes (any class, from "low" events), by (surface, size, filled)')
P(dict(collections.Counter((v['surface'], v['cls'][0], v['cls'][1]) for v in low_inst.values()).most_common()))
P('below 1/4:', [v for v in low_inst.values() if 4 * v['cls'][1] < v['cls'][0]])
P(); P('## counterexample events (LPC: viol=0, filled=0; LPC-1/4: viol=0, F/N<1/4):', len(cex))
for d in cex[:20]: P(json.dumps(dict(graph=d['graph'].split()[0], cex=d['cex'])))
open(os.path.join(OUT, 'report.txt'), 'w').write('\n'.join(R) + '\n'); print('\n'.join(R))

# verification items: all violator-free cycle classes (one per (WL, hole word, class)), a sample of dirty ones, all cex,
# the non-trivial (size >= 8) low classes (cap 40)
rng = random.Random(9); items = []
vf = [v for v in cyc_inst.values() if v['cls'][6] == 0]; dirty = [v for v in cyc_inst.values() if v['cls'][6] > 0]
dirty.sort(key=lambda v: (v['cls'][6], v['cls'][1] / v['cls'][0])); pick = dirty[:maxdirty // 2] + rng.sample(dirty[maxdirty // 2:], min(maxdirty // 2, max(0, len(dirty) - maxdirty // 2)))
bysig = collections.defaultdict(list)
for v in sorted(vf, key=lambda v: (v['cls'][1] / v['cls'][0], v['states'])): bysig[(v['surface'], v['word'], tuple(v['cls']))].append(v)
for sig, L in sorted(bysig.items(), key=lambda kv: kv[0][2][1] / kv[0][2][0]):   # up to 3 instances per class signature, lowest F/N first
    for v in L[:3]: items.append(dict(kind='cyc_violator_free', nsig=len(L), **v))
for v in pick: items.append(dict(kind='cyc_dirty', **v))
nt = sorted([v for v in low_inst.values() if v['cls'][0] >= 8], key=lambda v: -v['cls'][0])[:40]
for v in nt: items.append(dict(kind='low', **v))
for d in cex:
    for c in d['cex']: items.append(dict(kind='cex', surface=d['surface'], n=d['n'], word=c['word'], cls=c['cls'], hole=c['hole'], graph=d['graph']))
with open(os.path.join(OUT, 'verify_items.jsonl'), 'w') as f:
    for it in items: f.write(json.dumps(it) + '\n')
print('verify items', collections.Counter(it['kind'] for it in items))
