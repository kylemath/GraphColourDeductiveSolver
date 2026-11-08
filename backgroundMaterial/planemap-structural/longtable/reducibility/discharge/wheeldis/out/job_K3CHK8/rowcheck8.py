"""K3CHK8: occurrence (rotation-preserving, Z-consistent frame of the row itself; K3CHK occurs()) of b7_u.666666_.5...5. in GL5 row B 7/7666666/6567656."""
src = open('out/job_K3CHK/rowcheck.py').read().split("out = open(K + 'per_row.tsv'")[0].replace("K = 'out/job_K3CHK/'", "K = 'out/job_K3CHK8/'").replace("open(K + 'configs.kc')", "open(K + 'eng/cfg.in')")
exec(src)
with open(K + 'per_row.tsv', 'w') as f:
    f.write('# config\trow (d link apex)\tface-set embeddings\trotation-preserving\toccurs\n')
    for nm, line in CF.items():
        for L, S in [('7666666', '6567656')]:
            fs, rt = occurs(line, 7, L, S); f.write('%s\t7 %s %s\t%d\t%d\t%s\n' % (nm, L, S, fs, rt, 'YES' if rt else 'NO')); print(nm, L, S, fs, rt)
