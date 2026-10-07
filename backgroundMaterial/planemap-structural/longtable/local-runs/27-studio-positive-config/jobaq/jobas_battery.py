import json, sys
import jobaq
jobaq.GDIR = '../jobas/'; jobaq.ALLSTATES = True
res = []
for g, h in (('A7f1', 22), ('A7f2', 22), ('A7f3', 34), ('A7f4', 22)):
    for mirror in (False, True):
        for r in jobaq.run(g, h, mirror): res.append(r); print(json.dumps(r), flush=True)
json.dump(res, open('../jobas/jobas-battery.json', 'w'), indent=0)
