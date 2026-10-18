"""quick wheel checks for the self-pair hand checks (uses jcheck2's R5/R6 sets)."""
import sys, os, io, contextlib
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = sys.argv[1]
J = os.path.join(HERE, '..', 'J_lp_checker', 'jcheck2.py'); sys.argv = [J, 'help', 'root=' + ROOT]
g = {'__file__': J, '__name__': 'jc'}
with contextlib.redirect_stdout(io.StringIO()): exec(open(J).read(), g)
isR6, isR5 = g['isR6'], g['isR5']
# s0's 6-wheel at s1>=7, p1=5, o1=5: (w0 5, w1 6, p1 5, o1 5, o2, s6 5)
for o2 in (6, 7, 8, 9): print('s0 wheel 5 6 5 5 %d 5 R6?' % o2, isR6([5, 6, 5, 5, o2, 5]))
# p1 word rooted at s1 (s1, w1 6, s0 6, o1, n): lone 55667-type needs o1=n=5
for s1 in (7, 8, 9): print('p1 word', (s1, 6, 6, 5, 5), 'R5?', isR5((s1, 6, 6, 5, 5)))
# w1's wheel at s1>=7 p1=5: (u 7, w2 7, s1, p1 5, s0 6, w0 5)
for s1 in (7, 8, 9): print('w1 wheel 7 7 %d 5 6 5 R6?' % s1, isR6([7, 7, s1, 5, 6, 5]))
# w5's wheel at s4>=7 p5=5 (forced p5>=6 by round 42 anyway): (u 7, w6 5, s5 7, p5, s4, w4 7)
for s4 in (6, 7, 8, 9):
    print('w5 wheel p5=5..9 s4=%d R6?' % s4, [isR6([7, 5, 7, p, s4, 7]) for p in (5, 6, 7, 8, 9)])
print('w1 wheel at s1=6, p1=5..9:', [isR6([7, 7, 6, p, 6, 5]) for p in (5, 6, 7, 8, 9)])
