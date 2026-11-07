"""K3CHK5: occurrence (rotation-preserving, Z-consistent frame of the row itself; K3CHK occurs()) in d8 row 76756556 / 56557667."""
src = open('out/job_K3CHK/rowcheck.py').read().split("out = open(K + 'per_row.tsv'")[0].replace("K = 'out/job_K3CHK/'", "K = 'out/job_K3CHK5/'")
exec(src)
with open(K + 'per_row.tsv', 'w') as f:
    f.write('# config\trow (d link apex)\tface-set embeddings\trotation-preserving\toccurs\n')
    for nm, line in CF.items():
        fs, rt = occurs(line, 8, '76756556', '56557667'); f.write('%s\t8 76756556 56557667\t%d\t%d\t%s\n' % (nm, fs, rt, 'YES' if rt else 'NO')); print(nm, fs, rt)
