import sys, json, time, fill
for L in map(int, sys.argv[1].split(',')):
    t = time.time(); r = fill.run2(L); r['sec'] = round(time.time()-t, 1); print(json.dumps(r), flush=True)
