# Aggregate per-merge logs: python summarize.py
import json, glob, collections
def H(xs): return dict(sorted(collections.Counter(xs).items(), key=lambda t: (t[0] is None, t[0] or 0)))
for grp, pat in (('topdown6', 'logs/[!v]*_L??.jsonl'), ('topdown24', 'logs/*_p24.jsonl'), ('voronoi', 'logs/vor_*.jsonl')):
    rs = []
    for f in sorted(glob.glob(pat)): rs += [json.loads(l) for l in open(f)]
    if not rs: continue
    ch = [r for r in rs if r['chords']]; cl = [r for r in rs if not r['chords']]
    kc = [r for r in cl if r.get('kid_chords')]
    print('==', grp, 'merges', len(rs), 'chorded', len(ch), 'chordless-with-chorded-kids', len(kc))
    for nm, S in (('chorded', ch), ('chordless', cl), ('chordless,kids chorded', kc)):
        if not S: continue
        print(' ', nm, 'R', H(r['R'] for r in S), 'w', H(r['w'] for r in S), 'fallback', H(r['fallback'] for r in S))
        print('    chords max', max(r['chords'] for r in S), 'pockets max', max(r['pockets'] for r in S), 'nU max', max(r['nU'] for r in S),
              'ptau_before max', max(r['ptau_before'] for r in S), 'strict_tau_after max', max(r['strict_tau_after'] for r in S))
    sa = [(r.get('sA'), r.get('sB')) for r in rs if r.get('sA') is not None]
    if sa:
        print('  seam pockets sA+sB', H(a+b for a, b in sa))
        for k in sorted(set(a+b for a, b in sa)):
            S = [r for r in rs if r.get('sA') is not None and r['sA']+r['sB'] == k]
            print('    s=%d R %s' % (k, H(r['R'] for r in S)))
    big = sorted(ch, key=lambda r: -r['chords'])[:5]
    for r in big: print('   top chorded:', {k: r.get(k) for k in ('nU', 'chords', 'pockets', 'maxpocket', 'R', 'w', 'ptau_before', 'strict_tau_after', 'sA', 'sB')})
