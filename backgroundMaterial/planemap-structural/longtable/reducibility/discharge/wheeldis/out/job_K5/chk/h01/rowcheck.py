"""ST-42 second check: occurrence (rotation-preserving; K3CHK occurs()) of the K-5 hit in its row."""
import sys
src = open('out/job_K3CHK/rowcheck.py').read().split("out = open(K + 'per_row.tsv'")[0].replace("K = 'out/job_K3CHK/'", "K = 'out/job_K5/chk/h01/'").replace("open(K + 'configs.kc')", "open(K + 'cfg.in')")
exec(src)
for nm, line in CF.items():
    fs, rt = occurs(line, 10, '6556656655', '7566556657'); print(nm, '10/6556656655/7566556657 face-set', fs, 'rotation-preserving', rt, 'OCCURS' if rt else 'NO')
