"""K3CHK4: occurrence (rotation-preserving, Z-consistent frame of the row itself; K3CHK occurs()) of the D kill and the C alternative
in the two d8 binder rows of the 0.040940 point (ST-19)."""
src = open('out/job_K3CHK/rowcheck.py').read().split("out = open(K + 'per_row.tsv'")[0].replace("K = 'out/job_K3CHK/'", "K = 'out/job_K3CHK4/'")
exec(src)
rows = [('56656757', '66665576'), ('56657576', '66667556')]
with open(K + 'per_row.tsv', 'w') as f:
    f.write('# config\trow (d link apex)\tface-set embeddings\trotation-preserving\toccurs\n')
    for nm, line in CF.items():
        for L, S in rows:
            fs, rt = occurs(line, 8, L, S); f.write('%s\t8 %s %s\t%d\t%d\t%s\n' % (nm, L, S, fs, rt, 'YES' if rt else 'NO')); print(nm, L, S, fs, rt)
