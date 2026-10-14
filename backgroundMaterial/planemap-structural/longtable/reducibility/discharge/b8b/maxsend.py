"""B8b (exploratory): structural upper bound on the number of K = 1 senders whose only big vertex is u (deg d).
Relaxation (ignores R except W12 words for d = 7; ignores everything beyond radius 2 of u):
  - link vertices and second-ring vertices of u have degree 5 or 6 (a big one only removes candidates: replacing
    it by 6 never lowers the count, see README 8.2);
  - a degree-5 link vertex w_i is a candidate (its word contains d; for d = 7 the word must not be a W12 wheel);
  - a degree-5 second-ring vertex is a candidate iff all its link and second-ring neighbours have degree 6
    (it must be 66666: a {5,6} word other than 66666 is a W12 wheel).
The neighbourhood is a cyclic sequence of blocks (deg w_i, [p_i if deg 6], s_i).  Exhaustive over all 6^d (d <= 9)
or by brute force over sequences; prints the maximum and the arrangements attaining it (up to rotation)."""
import sys, os, itertools
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
import ball, h0

BLOCKS = [(5, None, 5), (5, None, 6), (6, 5, 5), (6, 5, 6), (6, 6, 5), (6, 6, 6)]


def count(seq, d):
    n = len(seq); c = 0; who = []
    # ring-2 cycle: list of (deg, linknbrs)
    R2 = []
    for i, (dw, p, s) in enumerate(seq):
        if p is not None: R2.append((p, (i,)))
        R2.append((s, (i, (i + 1) % n)))
    L = len(R2)
    for i, (dw, p, s) in enumerate(seq):
        if dw != 5: continue
        if d == 7:
            word = ''.join(map(str, ball.wheel_canon([d, seq[(i + 1) % n][0], s, seq[i - 1][2], seq[i - 1][0]])))
            if word in h0.W12: continue
        c += 1; who.append('w%d' % i)
    for j, (dy, lk) in enumerate(R2):
        if dy != 5: continue
        if any(seq[k][0] != 6 for k in lk): continue
        if R2[j - 1][0] != 6 or R2[(j + 1) % L][0] != 6: continue
        c += 1; who.append(('p%d' if len(lk) == 1 else 's%d') % lk[0])
    return c, who


def canon(seq):
    n = len(seq); return min(tuple(seq[k:] + seq[:k]) for k in range(n))


if __name__ == '__main__':
    for d in map(int, sys.argv[1:]):
        best = -1; arr = set(); best66 = -1
        for seq in itertools.product(range(6), repeat=d):
            S = [BLOCKS[b] for b in seq]
            c, who = count(S, d)
            c66 = sum(1 for w in who if w[0] != 'w')
            best66 = max(best66, c66)
            if c > best: best = c; arr = {canon(seq)}
            elif c == best: arr.add(canon(seq))
        print('d=%d  max K=1 lone-u senders (relaxed): %d   max 66666 ones: %d   (d - 6 = %d)   attained by %d arrangements' % (
            d, best, best66, d - 6, len(arr)))
        for a in sorted(arr)[:6]:
            S = [BLOCKS[b] for b in a]; print('    ', S, count(S, d)[1])
