"""Frame consistency for explore's s5_ sender windows (loop/k51/sender_kills51.txt at 04a8b71c), from the file's spec
header only. For each line: (1) every interior vertex's kc degree (interior + ring adjacencies) equals the digit at its
frame slot in the name; (2) the kc interior adjacency equals the adjacency the spec implies between the framed slots;
(3) the name's lettered slots are exactly the frame's slots, and the F/N/x markers agree with the spec.
Spec adjacency among v (centre five), w_k, s_k (between w_k and w_{k+1}), f_k (private of a 6-spoke w_k, between
s_{k-1} and s_k): v-w_k; w_k-w_{k+1}; s_k-w_k, s_k-w_{k+1}; s_{k-1}-s_k iff w_k = 5; f_k-w_k, f_k-s_{k-1}, f_k-s_k."""
import sys, re
def spec_adj(a, b, W):
    """W: letters of w_0..w_4 as known (digit or None). Returns True / False / None (undecidable from W)."""
    ka, kb = a[0], b[0]
    def idx(x): return int(x[1:])
    if {ka, kb} == {'v', 'w'}: return True
    if ka == kb == 'w': return (idx(a) - idx(b)) % 5 in (1, 4)
    if {ka, kb} == {'s', 'w'}:
        s, w = (a, b) if ka == 's' else (b, a); return idx(w) in (idx(s), (idx(s) + 1) % 5)
    if ka == kb == 's':
        i, j = idx(a), idx(b)
        if (j - i) % 5 == 1: k = j
        elif (i - j) % 5 == 1: k = i
        else: return False
        return None if W[k] is None else W[k] == 5          # the edge s_{k-1}s_k iff w_k = 5
    if {ka, kb} == {'f', 'w'}:
        f, w = (a, b) if ka == 'f' else (b, a); return idx(f) == idx(w)
    if {ka, kb} == {'f', 's'}:
        f, s = (a, b) if ka == 'f' else (b, a); return idx(s) in ((idx(f) - 1) % 5, idx(f))
    if 'v' in (ka, kb): return False
    if ka == kb == 'f': return False
    return False
bad = 0; n = 0
for l in open(sys.argv[1]):
    if l.startswith('#') or not l.strip(): continue
    n += 1; parts = [p.strip() for p in l.split('|')]
    f = parts[0].split(); nm = f[0]; m = int(f[2]); rp = f[3].split(';'); ip = f[4].split(';')
    frame = parts[1].replace('frame', '').strip().split(',')
    assert len(frame) == m, (nm, len(frame), m)
    E = [set() if ip[u] == '-' else {int(x) for x in ip[u].split(',')} for u in range(m)]
    deg = [len(E[u]) + (0 if rp[u] == '-' else len(rp[u].split(','))) for u in range(m)]
    _, c_w, sw, fw = nm.split('_'); c, ww = c_w[0], c_w[1:]
    lett = {}
    if c == 'u': lett['v'] = 5
    for k, ch in enumerate(ww):
        if ch.isdigit(): lett['w%d' % k] = int(ch)
    for k, ch in enumerate(sw):
        if ch.isdigit(): lett['s%d' % k] = int(ch)
    for k, ch in enumerate(fw):
        if ch.isdigit(): lett['f%d' % k] = int(ch)
    W = [int(ch) if ch.isdigit() else (5 if ch == 'F' else 6 if ch == 'x' else None) for ch in ww]
    errs = []
    if set(frame) != set(lett): errs.append('frame slots %s != lettered slots %s' % (sorted(frame), sorted(lett)))
    for u, sl in enumerate(frame):
        if sl in lett and deg[u] != lett[sl]: errs.append('%s: kc degree %d != name digit %d' % (sl, deg[u], lett[sl]))
    for u in range(m):
        for v in range(u + 1, m):
            e = spec_adj(frame[u], frame[v], W)
            got = v in E[u]
            if e is None: errs.append('%s-%s undecidable from the name' % (frame[u], frame[v]))
            elif e != got: errs.append('%s-%s: spec %s, kc %s' % (frame[u], frame[v], e, got))
    for k, ch in enumerate(ww):   # markers
        if ch in 'FN':
            if not ('s%d' % ((k - 1) % 5) in lett and 's%d' % k in lett): errs.append('%s at w%d but s%d/s%d not both interior' % (ch, k, (k - 1) % 5, k))
        if ch == 'x' and 'f%d' % k not in lett: errs.append('x at w%d but f%d not interior' % (k, k))
    if errs: bad += 1; print('INCONSISTENT %s: %s' % (nm, '; '.join(errs)))
    else: print('ok %s (m=%d, frame %s)' % (nm, m, ','.join(frame)))
print('frames checked %d, inconsistent %d' % (n, bad))
