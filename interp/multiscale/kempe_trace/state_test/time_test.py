import sys, time, json, random; sys.path.insert(0, '/mnt/project-files/multiscale/kempe_trace/state_test')
from st import *
ce = json.load(open('/mnt/project-files/multiscale/opus_attack/bandfill/counterexamples.json'))
c = [c for c in ce if c['L'] == 13][0]
E = tube_setup(c, 'A'); w = c['w']; tris = tri_list(E['adj'], E['S'])
t0 = time.time(); print(unsat(E['adj'], E['S'], E['col'], E['bd'], w, 9), time.time()-t0)
t0 = time.time(); rows, H = state(E, E['col'], w, tris); print(time.time()-t0, H, parity_check(rows, E, E['col']))
t0 = time.time(); K = keys(rows, H, E['L'], w); print(time.time()-t0)
print(rows[0])
for side in 'AB':
    E = opus_setup(side); tris = tri_list(E['adj'], E['S'])
    t0 = time.time(); print(side, unsat(E['adj'], E['S'], E['col'], E['bd'], 4, 10 if side=='A' else 8), time.time()-t0)
    rows, H = state(E, E['col'], 4, tris); print(H, parity_check(rows, E, E['col']), [dt[g][2] for dt in rows for g in (1,2,3)])
    rng = random.Random(1); t0 = time.time()
    col2 = sat_colour(E['adj'], E['S'], {v: E['col'][v] for v in E['bd']}, rng); print('regen', time.time()-t0)
    t0 = time.time(); print(unsat(E['adj'], E['S'], col2, E['bd'], 4, 10 if side=='A' else 8), time.time()-t0)
