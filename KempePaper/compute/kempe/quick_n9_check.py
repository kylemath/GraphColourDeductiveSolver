"""Quick check: run original bfs_path_merge_check at n=9 to compare with new code."""
import sys, os, time
sys.path.insert(0, os.path.dirname(__file__))

from kempe_ops import enumerate_colourings, num_colours
from triangulation_db import generate_triangulations
from merge_analysis import bfs_path_merge_check

print("Running original bfs_path_merge_check at n=9...")
t0 = time.time()
db = generate_triangulations(9)
print(f"Generated triangulations in {time.time()-t0:.1f}s")

total_a5 = 0
total_mp = 0
total_merges = 0

for idx, T in enumerate(db[9]):
    name = T.graph.get('name', f'T_9_{idx}')
    for v in sorted(T.nodes()):
        if T.degree(v) > 5:
            continue
        result = bfs_path_merge_check(T, v)
        total_a5 += result['total_a5_swaps']
        total_mp += result['multi_chain_cases']
        total_merges += result['merges']

    if (idx + 1) % 10 == 0 or idx == 0:
        print(f"  [{idx+1}/50] a5={total_a5}, mp={total_mp}, merges={total_merges} "
              f"({time.time()-t0:.0f}s)")

print(f"\nOriginal code at n=9:")
print(f"  (a,5)-swaps: {total_a5}")
print(f"  Merge-prone: {total_mp}")
print(f"  BFS used unsafe (merges): {total_merges}")
print(f"  Time: {time.time()-t0:.1f}s")

if total_merges > 0:
    print("*** ORIGINAL CODE ALSO FINDS MERGES ***")
else:
    print("Original code: 0 merges (new code has a bug)")
