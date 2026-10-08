#!/usr/bin/env python3
"""Census33 [exploratory]: evaluate one chunk of frame-class graphs (frame.c lines "name n r0;r1;... flags").
Per graph, every degree-5 hole:
  engine 1  bin/picyc --full (Census29 copy of TrackA picyc.cpp): Kempe classes (clsig) -> PureClean, min class F/N.
  TrackO    bin/c33_eng (TrackO to_eng.c + all-DL pi-cycle analysis): R, NR, NRcyc, Rcyc, run histograms,
            all-DL pi-cycles [L, Nmin, Nmax, class size, class #filled]; long-run dumps (L>=4) go to OUT.runs.
  sample    (md5(name) % 10 == 0): bin/f66_w1 --lockparity: every unfilled state; nUnf must equal picyc U; allDL count
            must equal c33_eng's number of all-DL pi-cycles.
usage: eval33.py IN.txt OUT.jsonl"""
import sys, os, json, hashlib, subprocess, tempfile
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def run(cmd, inp=None):
    r = subprocess.run(cmd, capture_output=True, text=True, stdin=inp)
    if r.returncode != 0: raise RuntimeError('%s failed: %s' % (cmd, r.stderr[-2000:]))
    return [json.loads(l) for l in r.stdout.splitlines() if l.strip()]

def main():
    inp, outp = sys.argv[1], sys.argv[2]
    lines = [l.split() for l in open(inp) if l.strip()]
    open(outp + '.runs', 'w').close()
    if not lines: open(outp, 'w').close(); return
    samp = [p for p in lines if int(hashlib.md5(p[0].encode()).hexdigest(), 16) % 10 == 0]
    tmpd = os.environ.get('TMPDIR')
    with tempfile.NamedTemporaryFile('w', suffix='.in', delete=False, dir=tmpd) as fh:
        for p in lines: fh.write(' '.join(p[:3]) + '\n')
        fn = fh.name
    with tempfile.NamedTemporaryFile('w', suffix='.in', delete=False, dir=tmpd) as fh:
        for p in samp: fh.write(' '.join(p[:3]) + '\n')
        fs = fh.name
    try:
        P = run([os.path.join(ROOT, 'bin/picyc'), fn, '--full'])
        Fq = run([os.path.join(ROOT, 'bin/f66_w1'), fs, '--lockparity']) if samp else []
        with open(fn) as f: O = run([os.path.join(ROOT, 'bin/c33_eng'), '-M', '16000000', '-D', '20'], inp=f)
    finally: os.unlink(fn); os.unlink(fs)
    ph = {(r['name'], r['hole']): r for r in P if r['kind'] == 'hole'}
    fh_ = {(r['graph'], r['hole']): r for r in Fq if r['kind'] == 'hole'}
    oh = {}
    with open(outp + '.runs', 'w') as rf:
        for r in O:
            if 'run' in r: rf.write(json.dumps(r, separators=(',', ':')) + '\n')
            else: oh[(r['g'], r['h'])] = r
    sampnames = {p[0] for p in samp}
    with open(outp, 'w') as out:
        for p in lines:
            name, n = p[0], int(p[1]); rot = [list(map(int, x.split(','))) for x in p[2].split(';')]
            deg = [len(r) for r in rot]; holes = [v for v in range(n) if deg[v] == 5]
            rec = dict(name=name, n=n, deg5=len(holes), flags=' '.join(p[3:]), maxdeg=max(deg), sample=name in sampnames)
            H = {}; errs = []; lp = [0, 0, 0, 0]
            for h in holes:
                a = ph.get((name, h)); o = oh.get((name, h))
                if a is None or o is None: errs.append('missing hole %d' % h); continue
                if 'skip' in o: errs.append('c33 skip hole %d' % h); continue
                if a.get('cls_bad') or a.get('f5_bad') or a.get('cyc_split'): errs.append('picyc flags hole %d' % h)
                c = sorted((x[0], x[1]) for x in a['clsig'])
                if sum(x[0] for x in c) != a['states'] or sum(x[1] for x in c) != a['F']: errs.append('clsig sum hole %d' % h)
                if o['S'] != a['states'] or o['U'] != a['U']: errs.append('S/U mismatch picyc vs c33 hole %d' % h)
                e = dict(pc=all(F > 0 for s, F in c), mf=round(min(F / s for s, F in c), 6), q=min(4 * F - s for s, F in c),
                         ncls=len(c), S=a['states'], R=o['R'], Rcyc=o['Rcyc'], NR=o['NR'], NRcyc=o['NRcyc'], I=o['I'],
                         RmaxN=o['RmaxN'], runs=o['runs'], runsNR=o['runsNR'], dlc=o['dlc'], ndlc=o['ndlc'],
                         w=''.join(str(min(deg[u], 8)) if deg[u] < 8 else '8+' for u in rot[h]))
                if name in sampnames:
                    b = fh_.get((name, h))
                    if b is None: errs.append('f66 missing hole %d' % h)
                    else:
                        if a['U'] != b['nUnf']: errs.append('U mismatch picyc/f66 hole %d' % h)
                        if b['cap']: errs.append('f66 cap hole %d' % h)
                        if b['lp'][0] != b['nUnf']: errs.append('lp count hole %d' % h)
                        if b['allDL'] != o['ndlc']: errs.append('allDL mismatch f66 %d c33 %d hole %d' % (b['allDL'], o['ndlc'], h))
                        for k in range(4): lp[k] += b['lp'][k]
                        e['f66allDL'] = b['allDL']
                H[str(h)] = e
            rec.update(holes=H, lp=lp, errs=errs)
            out.write(json.dumps(rec, separators=(',', ':')) + '\n')

if __name__ == '__main__':
    main()
