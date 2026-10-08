#!/usr/bin/env python3
"""Census29 [exploratory]: evaluate one file of frame-class graphs (frame.c output lines "name n r0;r1;... flags").

Per graph:
  engine 1  bin/picyc --full (copy of TrackA/bin/picyc.cpp): Kempe classes of T - v at every degree-5 v, clsig [size, F, ...]
            -> PureClean count, per-hole min class F/size (quarter floor), class multiset.
  lock parity  bin/f66_w1 --lockparity (TrackF/src/f66.cpp, W=1): every unfilled state at every degree-5 hole,
            lp = [#checked, #Lock2 mismatches, #Lock1 mismatches, #K_alpha,mu even]; also nUnf (must equal picyc U) and allDL.
  sample (deterministic 10%: md5(name) % 10 == 0, or --all):
     engine 2  kempe_py.Space (TrackA/holes.py py_holes): class multisets must equal engine 1;
     lock parity engine 2: independent Python re-check of Theorem LP on every unfilled state of kempe_py's state list;
     filter engine 2: TrackA/tracka_lib.G(rot).summary()['frame'] must be True.
usage: eval_shard.py IN.txt OUT.jsonl [--all]"""
import sys, os, json, hashlib, subprocess, tempfile, itertools
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE); WK = os.path.dirname(ROOT)
sys.path.insert(0, os.path.join(WK, 'TrackA'))
sys.path.insert(0, '/Users/kylemathewson/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/local-runs/common')

def canon(w):
    return min(tuple(s[i:] + s[:i]) for s in (w, w[::-1]) for i in range(len(s)))

def wfmt(w):
    return ''.join(str(d) if d < 8 else '8+' for d in w)

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0: raise RuntimeError('%s failed: %s' % (cmd, r.stderr[-2000:]))
    return [json.loads(l) for l in r.stdout.splitlines() if l.strip()]

def py_lockparity(rot, h):
    """engine-2 lock parity at hole h: returns (#unfilled, #bad) over kempe_py's states (colourings of T-h up to renaming)."""
    from kempe_py import Space
    adj = {v: set(r) for v, r in enumerate(rot)}
    sp = Space(adj, h, link=rot[h]); L = sp.linki
    odd = 0
    for v in range(len(rot)):
        if v != h and len(rot[v]) % 2: odd |= 1 << sp.idx[v]
    nU = bad = 0
    for s in sp.states:
        lc = [s[i] for i in L]
        if len(set(lc)) < 4: continue
        nU += 1
        j = [t for t in range(5) if lc[t] == lc[(t + 2) % 5]]; assert len(j) == 1; j = j[0]
        x = lambda t: L[(j + t) % 5]
        al, mu, A, B = lc[j], lc[(j + 1) % 5], lc[(j + 3) % 5], lc[(j + 4) % 5]
        cm = sp.cmasks(s)
        l1 = sp.flood(1 << x(1), cm[mu] | cm[A]) >> x(3) & 1
        l2 = sp.flood(1 << x(1), cm[mu] | cm[B]) >> x(4) & 1
        par = lambda p, q: bin(sp.flood(1 << x(2), cm[p] | cm[q]) & odd).count('1') & 1
        if par(al, A) != l2 or par(al, B) != l1 or par(al, mu) != 1: bad += 1
    return nU, bad

def main():
    inp, outp = sys.argv[1], sys.argv[2]; ALL = '--all' in sys.argv
    lines = [l.split() for l in open(inp) if l.strip()]
    if not lines: open(outp, 'w').close(); return
    with tempfile.NamedTemporaryFile('w', suffix='.in', delete=False, dir=os.environ.get('TMPDIR')) as fh:
        for p in lines: fh.write(' '.join(p[:3]) + '\n')
        fn = fh.name
    try:
        P = run([os.path.join(ROOT, 'bin/picyc'), fn, '--full'])
        Fq = run([os.path.join(ROOT, 'bin/f66_w1'), fn, '--lockparity'])
    finally: os.unlink(fn)
    ph = {}; fh_ = {}
    for r in P:
        if r['kind'] == 'hole': ph[(r['name'], r['hole'])] = r
    for r in Fq:
        if r['kind'] == 'hole': fh_[(r['graph'], r['hole'])] = r
    with open(outp, 'w') as out:
        for p in lines:
            name, n = p[0], int(p[1]); rot = [list(map(int, x.split(','))) for x in p[2].split(';')]
            deg = [len(r) for r in rot]; holes = [v for v in range(n) if deg[v] == 5]
            rec = dict(name=name, n=n, deg5=len(holes), flags=' '.join(p[3:]), maxdeg=max(deg))
            cls = {}; minfrac = {}; words = {}; lp = [0, 0, 0, 0]; errs = []; allDL = 0
            for h in holes:
                a = ph.get((name, h)); b = fh_.get((name, h))
                if a is None or b is None: errs.append('missing hole %d' % h); continue
                if a.get('cls_bad') or a.get('f5_bad') or a.get('cyc_split'): errs.append('picyc flags hole %d' % h)
                c = sorted((x[0], x[1]) for x in a['clsig'])
                if sum(x[0] for x in c) != a['states'] or sum(x[1] for x in c) != a['F']: errs.append('clsig sum hole %d' % h)
                if a['U'] != b['nUnf']: errs.append('U mismatch hole %d: picyc %d f66 %d' % (h, a['U'], b['nUnf']))
                if b['cap']: errs.append('f66 cap hole %d' % h)
                if b['lp'][0] != b['nUnf']: errs.append('lp count hole %d' % h)
                for k in range(4): lp[k] += b['lp'][k]
                allDL += b['allDL']
                cls[h] = c; minfrac[h] = min(F / s for s, F in c)
                words[h] = wfmt(canon([min(deg[u], 8) for u in rot[h]]))
            pc = [h for h in cls if all(F > 0 for s, F in cls[h])]
            rec.update(npc=len(pc), nonpc=sorted(set(cls) - set(pc)), worst=min(minfrac.values()), margin=max(minfrac.values()),
                       quarter_break=[h for h in cls if any(4 * F < s for s, F in cls[h])],
                       quarter_eq=[h for h in cls if any(4 * F == s for s, F in cls[h])],
                       minfrac={str(h): round(v, 6) for h, v in minfrac.items()}, classes={str(h): v for h, v in cls.items()},
                       words={str(h): w for h, w in words.items()}, wordset=sorted(set(words.values())),
                       lp=lp, allDL=allDL, errs=errs)
            if ALL or int(hashlib.md5(name.encode()).hexdigest(), 16) % 10 == 0:
                from holes import py_holes
                from tracka_lib import G
                Hp = py_holes(rot)
                v2 = dict(classes_ok=set(Hp) == set(cls) and all(sorted(cls[h]) == Hp[h] for h in cls))
                nU = bad = 0; U1 = sum(ph[(name, h)]['U'] for h in holes)
                for h in holes:
                    a_, b_ = py_lockparity(rot, h); nU += a_; bad += b_
                v2.update(lp_unf=nU, lp_bad=bad, lp_unf_ok=nU == U1, frame=bool(G(rot).summary()['frame']))
                rec['engine2'] = v2
            out.write(json.dumps(rec, separators=(',', ':')) + '\n')

if __name__ == '__main__':
    main()
