# W15: rough wall-time estimate for w15_upper.sh, from W15's measured runs on the shared 4-core container (5 Nov, load ~5-7).
# usage: python3 estimate15.py T DLIST NPROC
import sys
T = float(sys.argv[1]); DL = [int(x) for x in sys.argv[2].split(',')]; NP = int(sys.argv[3])
# wall-minutes per degree for ONE nice-10 process on the shared 4-core container (load ~9-10, so ~50% of a core), NECK=1, all parts
# summed. d = 7..9 measured at b77F in01 (t = 0.0315, 5 Nov): 9.4, 34.5, 49.6; d >= 10 from W10's runs (no NECK) divided by 4 [C].
BASE = {7: 9.4, 8: 34.5, 9: 49.6, 10: 6, 11: 3, 12: 2, 13: 1, 14: 0.3, 15: 0.1, 16: 0.1, 17: 0.1}
f = max(0.5, (0.0315 / max(T, 1e-3)) ** 1.5)
cpu = sum(BASE.get(d, 1) for d in DL) * f
print('runtime estimate: Python step ~2 min; separator ~%.0f process-min (one nice-10 process at load ~10) over %d process(es) -> ~%.0f min wall (+ re-check ~6 min if anything is reported); scale %.2f for t = %.4f' % (cpu, NP, cpu / NP * 1.1, f, T))
