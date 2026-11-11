#!/usr/bin/env python3
"""ST-127 (a): the B5 kill list from our local kc lines, diffed against W6r's proofset185 (data).
Local sources (W = .../wheeldis/out): 582 proved from loop/k44/rsst.txt + rsst_verdicts.txt; 2.126 (rsst003);
SUB = job_ST111/in/d9plus/d9_greedy.tsv (37) + nl2837_r11 + nl3352_r13 (kc: loop/studio/opus_check/s39o/nl51_kc.txt)
      + P20 fix_63c8a193fe (job_ST111/hits_st111.tsv; P21 fix_404d45e819 proved but not required: excluded);
SUB2 = job_ST119/in/results/fw_greedy.tsv (143 nl) + job_ST119/windows13.tsv (13 windows); job_ST123/in/nl2208_r13.kc.
Writes st127/local_sub_kc.txt (the substitutes, sorted by name), st127/diff.txt and st127/k767_kc.txt
(582 + 2.126 + substitutes, the kill-list order used by the exporter and Lean)."""
import os, sys, hashlib
H = os.path.dirname(os.path.abspath(__file__)); B5 = os.path.normpath(os.path.join(H, '..'))
OUT = os.path.normpath(os.path.join(B5, '..', '..')); WD = os.path.normpath(os.path.join(OUT, '..'))
S = os.path.join(B5, 'st127')
def lines(p): return [l.rstrip('\n') for l in open(p) if l.strip()]
nl = {l.split()[0]: l for l in lines(os.path.join(WD, 'loop/studio/opus_check/s39o/nl51_kc.txt'))}
src = {}
def add(name, kc, where):
    if name in src and src[name][0] != kc: print('CONFLICT', name, where, src[name][1])
    src.setdefault(name, (kc, where))
g = [l.split('\t') for l in lines(os.path.join(OUT, 'job_ST111/in/d9plus/d9_greedy.tsv'))][1:]
for f in g: add(f[1], nl[f[1]], 'SUB d9_greedy')
for n in ('nl2837_r11', 'nl3352_r13'): add(n, nl[n], 'SUB extra')
hits = {l.split('\t')[0]: l.split('\t')[-1] for l in lines(os.path.join(OUT, 'job_ST111/hits_st111.tsv'))}
add('fix_63c8a193fe', hits['fix_63c8a193fe'], 'SUB P20 hits_st111')
fw = [l.split('\t') for l in lines(os.path.join(OUT, 'job_ST119/in/results/fw_greedy.tsv'))][1:]
for f in fw: add(f[2], nl[f[2]], 'SUB2 fw_greedy')
for l in lines(os.path.join(OUT, 'job_ST119/windows13.tsv')):
    f = l.split('\t'); add(f[0], f[3], 'SUB2 windows13')
add('nl2208_r13', lines(os.path.join(OUT, 'job_ST123/in/nl2208_r13.kc'))[0], 'ST123')
nsub_greedy = len(g); nfw = len(fw)
loc = sorted(src)
open(os.path.join(S, 'local_sub_kc.txt'), 'w').write('\n'.join(src[n][0] for n in loc) + '\n')
w = {l.split()[0]: l for l in lines(os.path.join(S, 'w6r/proofset185_kc.txt'))}
out = ['local substitutes: %d (d9_greedy %d + 2 extra + P20; fw_greedy %d nl + 13 windows; nl2208_r13), W6r proofset185: %d'
       % (len(loc), nsub_greedy, nfw, len(w))]
out.append('names only local: %s' % sorted(set(loc) - set(w)))
out.append('names only W6r: %s' % sorted(set(w) - set(loc)))
diffl = [n for n in sorted(set(loc) & set(w)) if src[n][0] != w[n]]
out.append('common names with differing kc lines: %d %s' % (len(diffl), diffl))
for n in diffl: out += ['  local: ' + src[n][0], '  W6r:   ' + w[n]]
out.append('md5 local_sub_kc.txt %s; md5 of W6r proofset185 sorted %s' % (
    hashlib.md5(('\n'.join(src[n][0] for n in loc) + '\n').encode()).hexdigest()[:8],
    hashlib.md5(('\n'.join(w[n] for n in sorted(w)) + '\n').encode()).hexdigest()[:8]))
open(os.path.join(S, 'diff.txt'), 'w').write('\n'.join(out) + '\n'); print('\n'.join(out))
# kill list: 582 proved + 2.126 (rsst.txt order) + substitutes (sorted by name)
rs = lines(os.path.join(WD, 'loop/k44/rsst.txt'))
ver = {}
for l in lines(os.path.join(WD, 'loop/k44/rsst_verdicts.txt')):
    f = l.split()
    if f and f[0].startswith('rsst'): ver[f[0]] = [z for z in f if z.startswith('verdict=')][0].split('=')[1]
k = [l for l in rs if ver[l.split()[0]] in ('D2', 'C2cons') or l.split()[0] == 'rsst003_2o126']
assert len(k) == 583, len(k)
open(os.path.join(S, 'k767_kc.txt'), 'w').write('\n'.join(k + [src[n][0] for n in loc]) + '\n')
print('kill list', len(k) + len(loc))
