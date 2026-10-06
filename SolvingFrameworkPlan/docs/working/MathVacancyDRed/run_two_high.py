"""Studio job (Math, 6 Oct, explore mode): joint vacancy-D-reducibility game for the 2-balls of all link
sequences with three 5s and two entries in [6, dmax], adjacent (5,5,5,a,b) and non-adjacent (5,5,a,5,b),
up to rotation/reflection, ring length = sum - 20 <= max_ring. NOT run on the MacBook; untested.
Usage: python3 run_two_high.py [dmax=11] [max_ring=13] [max_nodes=5000000]"""
import sys, time
import family, vdred_joint

dmax = int(sys.argv[1]) if len(sys.argv) > 1 else 11
max_ring = int(sys.argv[2]) if len(sys.argv) > 2 else 13
max_nodes = int(sys.argv[3]) if len(sys.argv) > 3 else 5_000_000

def canon(s):
    reps = []
    for r in range(5):
        t = s[r:] + s[:r]
        reps += [t, t[::-1]]
    return min(reps)

seqs = set()
for a in range(6, dmax + 1):
    for b in range(6, dmax + 1):
        seqs.add(canon((5, 5, 5, a, b)))
        seqs.add(canon((5, 5, a, 5, b)))
seqs = sorted((s for s in seqs if sum(s) - 20 <= max_ring), key=lambda s: (sum(s), s))
print(f"{len(seqs)} sequences, dmax {dmax}, ring <= {max_ring}", flush=True)
for s in seqs:
    t0 = time.process_time()
    try:
        r = vdred_joint.solve_joint(family.config_from_degrees(s), verbose=False, max_nodes=max_nodes)
    except Exception as e:
        r = f"ERROR {type(e).__name__}: {e}"
    print(s, "ring", sum(s) - 20, r, f"cpu {time.process_time()-t0:.1f}s", flush=True)
