"""EXPLORE round 38 (09:52Z): kill w2's binding frames one by one.  Rows = round 36's w2 arrangements
(k36/rows_w2.txt: yload k m link s, frame coordinates L0 = u, L1 = w1, L2 = s1, ..., s'0 = w0).  Round 37's window
(link 7665575 + s'0 = 5) is applied first.  Each step: binding row = argmin (34/27 - yload)/k; its windows = centre +
link vertices around a nonempty subset of its link fives (or the whole link) + s-slots next to them, at its letters
(9 = degree >= 9 left open); kc -C in (ring, #fixed) order up to RMAX; D confirmed by dfast, C by cfast --search.
A kill removes every surviving row agreeing with the window in frame coordinates.
usage: python3 greedy.py RMAX MINUTES"""
import sys, os, itertools, subprocess, time
H = os.path.dirname(os.path.abspath(__file__)); W = os.path.normpath(os.path.join(H, '..', '..'))
src = open(os.path.join(W, 'gen28.py')).read(); src = src[:src.rindex('arrs = []')]
RMAX, MINS = int(sys.argv[1]), float(sys.argv[2])
sys.argv = ['gen28.py', '/dev/null', '24']; G = {'__file__': os.path.join(W, 'gen28.py'), '__name__': 'g28'}; exec(src, G)
BAR, d = 34 / 27, 7
KCC, DF, CF = os.path.join(H, '..', 'kc', 'kcc'), os.path.join(W, 'bin', 'dfast'), os.path.join(W, 'bin', 'cfast')
rows = []
for l in open(os.path.join(H, '..', 'k36', 'rows_w2.txt')):
    f = l.split(); rows.append((float(f[0]), int(f[1][2:]), [int(c) for c in f[4]], [int(c) for c in f[6]]))
LOG = open(os.path.join(H, 'greedy.log'), 'a')
def log(*a):
    s = ' '.join(str(x) for x in a); print(s, flush=True); LOG.write(s + '\n'); LOG.flush()
def covers(win, r):
    w, s = win
    return all(w[j] is None or w[j] == r[2][j] for j in range(d)) and all(s[j] is None or s[j] == r[3][j] for j in range(d))
def bound(r): return (BAR - r[0]) / r[1]
def windows(L, S):
    fives = [j for j in range(d) if L[j] == 5]; seen = {}; out = []
    subsets = [set(range(d))] + [{(i + e) % d for i in T for e in (-1, 0, 1)} for k in range(1, len(fives) + 1) for T in itertools.combinations(fives, k)]
    for wl in subsets:
        w = [L[j] if j in wl and L[j] != 9 else None for j in range(d)]
        slots = [j for j in range(d) if (j in wl or (j + 1) % d in wl) and S[j] != 9]
        for k in range(len(slots) + 1):
            for SS in itertools.combinations(slots, k):
                s = [S[j] if j in SS else None for j in range(d)]
                r = G['ringf'](d, w, s)
                if r > RMAX: continue
                Ls = ''.join(str(x) if x is not None else '.' for x in w); Ss = ''.join(str(x) if x is not None else '.' for x in s)
                key = G['canon_key'](d, Ls, Ss); nm = 'f%d_%s_%s' % (d, key[1], key[2])
                if (nm, Ls, Ss) in seen: continue
                line = G['make'](d, r, None, w, s, nm)
                if not line or line.startswith('RING'): continue
                seen[(nm, Ls, Ss)] = 1; out.append((r, sum(x is not None for x in s), nm, line, (w, s)))
    out.sort(key=lambda x: (x[0], x[1]))
    return out
def run(cmd, line):
    return subprocess.run(cmd, input=line + '\n', capture_output=True, text=True).stdout
cache = {}
def test(nm, r, line):
    if nm in cache: return cache[nm]
    o = run([KCC, '-C', '-s', '60', '-t', '600'], line); head = o.split('\n')[0]
    v = 'not', o.strip()
    if 'D=true' in head:
        o2 = run([DF, '/dev/stdin'], line) if r <= 16 else run([os.path.join(W, 'bin', 'dfast18'), '/dev/stdin'], line)
        v = ('D2' if 'D=true' in o2 else 'MISMATCH'), o.strip() + '\n  dfast: ' + o2.strip()
    elif 'C-REDUCIBLE' in o:
        o2 = subprocess.run([CF, '/dev/stdin', '--search', '--limit', '1'], input=line + '\n', capture_output=True, text=True).stdout
        v = ('C2' if 'C-REDUCIBLE' in o2 else 'CMISMATCH'), o.strip() + '\n  cfast: ' + o2.strip().replace('\n', '\n  cfast: ')
    cache[nm] = v; return v
k37 = ([7, 6, 6, 5, 5, 7, 5], [5, None, None, None, None, None, None])
alive = [r for r in rows if not covers(k37, r)]
log('# start %s: %d rows, %d after round 37 kill; RMAX %d' % (time.strftime('%H:%M:%SZ', time.gmtime()), len(rows), len(alive), RMAX))
t0 = time.time(); step = 0
while alive and time.time() - t0 < MINS * 60:
    b = min(alive, key=bound); step += 1
    L, S = b[2], b[3]
    log('step %d: cap %.4f at link %s s %s (yload %.4f k=%d)' % (step, bound(b), ''.join(map(str, L)), ''.join(map(str, S)), b[0], b[1]))
    killed = None
    for r, nf, nm, line, win in windows(L, S):
        if time.time() - t0 > MINS * 60: break
        v, out = test(nm, r, line)
        if v in ('MISMATCH', 'CMISMATCH'): log('  KILL LINE', v, nm); log(out); sys.exit(1)
        if v in ('D2', 'C2'): killed = (v, nm, r, win, out); break
    if not killed:
        log('  STOP: no window up to ring %d kills it (%d tested so far in total)' % (RMAX, len(cache))); break
    v, nm, r, win, out = killed
    n0 = len(alive); alive = [x for x in alive if not covers(win, x)]
    log('  %s %s ring %d (link %s s %s) removes %d rows' % (v, nm, r, ''.join(str(x) if x is not None else '.' for x in win[0]),
        ''.join(str(x) if x is not None else '.' for x in win[1]), n0 - len(alive)))
    for l in out.split('\n'): log('   ' + l[:200])
if alive:
    b = min(alive, key=bound)
    log('# end: cap %.4f (link %s s %s), R row first order t >= %.4f; %d windows tested; %.0f s' %
        (bound(b), ''.join(map(str, b[2])), ''.join(map(str, b[3])), (0.7 - 2 * bound(b)) / 2.7, len(cache), time.time() - t0))
