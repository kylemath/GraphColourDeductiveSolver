"""K3CHK6: occurrence of the K3CHK4 C alternative b8_u.56656.._...66... (X={I2-I3}) in three d8 rows (one picture up to symmetry):
rotation-preserving, Z-consistent frame of each row itself (K3CHK occurs())."""
src = open('out/job_K3CHK/rowcheck.py').read().split("out = open(K + 'per_row.tsv'")[0].replace("K = 'out/job_K3CHK/'", "K = 'out/job_K3CHK6/'")
exec(src)
rows = [('76566575', '66676565'), ('75765665', '65666765'), ('75756656', '56567666')]
with open(K + 'per_row.tsv', 'w') as f:
    f.write('# config\trow (d link apex)\tface-set embeddings\trotation-preserving\toccurs\n')
    for nm, line in CF.items():
        for L, S in rows:
            fs, rt = occurs(line, 8, L, S); f.write('%s\t8 %s %s\t%d\t%d\t%s\n' % (nm, L, S, fs, rt, 'YES' if rt else 'NO')); print(nm, L, S, fs, rt)
