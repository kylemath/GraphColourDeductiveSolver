import json
OPUS = {5:1,6:1,7:2,8:2,9:2,10:3,11:3,12:3,13:4,14:4,15:4}   # unfiltered mode 1 (opus REPORT)
R = {}
for l in open('/mnt/project-files/multiscale/bicolour/wstar.jsonl'):
    r = json.loads(l); R[(r['mode'], r['K0'], r['collar'], r['L'])] = r
def cell(m, k, c, L):
    r = R.get((m, k, c, L))
    if r is None:
        if m == 1 and c == 0 and k >= 3 and L % 3 != 2: return f"{OPUS[L]}="
        return '..'
    ws = r.get('wstar')
    if ws is None: return '>' + str(max(int(x) for x in r['w'])) if r['w'] else '..'
    return 'v' if ws == 'vacuous' else str(ws)
rows = [(1,k,0) for k in (2,3,4)] + [(3,2,0)] + [(1,k,1) for k in (2,3,4,5)] + [(3,2,1),(3,3,1)]
print('| filter | ' + ' | '.join(str(L) for L in range(5,16)) + ' |'); print('|---'*12 + '|')
print('| unfiltered mode 1 (Opus) | ' + ' | '.join(str(OPUS[L]) for L in range(5,16)) + ' |')
for m,k,c in rows:
    print(f"| {'old' if m==1 else 'pair'} k0={k} {'collar' if c else 'seam'} | " + ' | '.join(cell(m,k,c,L) for L in range(5,16)) + ' |')
