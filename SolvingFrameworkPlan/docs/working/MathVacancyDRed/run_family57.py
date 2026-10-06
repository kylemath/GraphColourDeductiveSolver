"""Studio job 3 (Math, 6 Oct): vacancy-D-reducibility (joint game) for the 2-ball configurations
with link degrees in {5,6,7}, ring length 11..13 (ring length = sum(d) - 20). Not run on the MacBook.
Usage: python3 run_family57.py [max_ring]   (default 13). One line per sequence, flushed."""
import sys, time
import family, vdred_joint

max_ring = int(sys.argv[1]) if len(sys.argv) > 1 else 13
seqs = [s for s in family.bracelets((5, 6, 7)) if 7 in s and 11 <= sum(s) - 20 <= max_ring]
seqs.sort(key=lambda s: sum(s))
print(f"{len(seqs)} sequences, ring 11..{max_ring}", flush=True)
for s in seqs:
    t0 = time.process_time()
    try:
        r = vdred_joint.solve_joint(family.config_from_degrees(s), verbose=False, max_nodes=5_000_000)
    except Exception as e:
        r = f"ERROR {type(e).__name__}: {e}"
    print(s, "ring", sum(s) - 20, r, f"cpu {time.process_time()-t0:.1f}s", flush=True)
