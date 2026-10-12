#!/usr/bin/env python3
"""planar_code -> 'name n rot' lines (rotation lists as given, 0-based)."""
import sys
data = open(sys.argv[1], 'rb').read(); assert data[:15] == b'>>planar_code<<'; i = 15; k = 0; tag = sys.argv[2]
while i < len(data):
    n = data[i]; i += 1; rot = []
    for v in range(n):
        nb = []
        while data[i] != 0: nb.append(data[i] - 1); i += 1
        i += 1; rot.append(nb)
    print(f"{tag}_{k} {n} " + ";".join(",".join(map(str, r)) for r in rot)); k += 1
