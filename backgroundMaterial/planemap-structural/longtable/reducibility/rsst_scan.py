#!/usr/bin/env python3
"""Scan RSST unavoidable.conf (studiointel/routeb/rsst): ring-size histogram, D vs C counts, and
(for rings <= RMAX) rerun dred.py's extendability + closure, comparing the extendable-class count
with RSST's third header field.  Usage: rsst_scan.py CONF RMAX"""
import sys, time, collections
import dred

def parse(path):
    L = open(path).read().split("\n"); i = 0; out = []
    while i < len(L):
        if not L[i].strip() or L[i].strip().replace('.', '').isdigit() and '.' in L[i]:
            name = L[i].strip()
            if not name: i += 1; continue
        name = L[i].strip(); hdr = L[i+1].split()
        n, r, next_, contr = map(int, hdr[:4])
        adj = {}
        for j in range(n):
            f = L[i+3+j].split(); v = int(f[0]); adj[v] = [int(x) for x in f[2:]]
        out.append(dict(name=name, n=n, r=r, next=next_, contr=contr, adj=adj))
        i += 3 + n
        while i < len(L) and L[i].strip() and not ('.' in L[i] and len(L[i].split()) == 1): i += 1
        while i < len(L) and not L[i].strip(): i += 1
    return out

cf = parse(sys.argv[1]); RMAX = int(sys.argv[2])
print(len(cf), "configurations")
print("ring sizes:", sorted(collections.Counter(c["r"] for c in cf).items()))
print("D (contract 0):", sum(c["contr"] == 0 for c in cf), " C:", sum(c["contr"] != 0 for c in cf))
for c in cf:
    if c["r"] > RMAX: continue
    r, n = c["r"], c["n"]; m = n - r
    ra = [[t-1 for t in c["adj"][r+1+a] if t <= r] for a in range(m)]
    ia = [[t-r-1 for t in c["adj"][r+1+a] if t > r] for a in range(m)]
    t = time.time()
    allk, good, lev = dred.closure(r, ra, ia, m, verbose=False)
    print(f"{c['name']:>8} r={r} n={n} classes={len(allk)} ext={len(lev[0])} (RSST {c['next']}) "
          f"contract={c['contr']} Dred={good == set(allk)} depth={len(lev)-1} {time.time()-t:.1f}s", flush=True)
