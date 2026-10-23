"""Minimal obstructing collars vs their one-vertex deletions (passing by minimality) and vs the regenerated population."""
import sys, json, os
sys.path.insert(0, '/mnt/project-files/multiscale/kempe_trace/state_test')
from st import *
MB = '/mnt/project-files/multiscale/kempe_trace/minimal_bad/'; OUT = '/mnt/project-files/multiscale/kempe_trace/state_test/'
ce = json.load(open('/mnt/project-files/multiscale/opus_attack/bandfill/counterexamples.json'))
res = []
for fn in sorted(os.listdir(MB)):
    if fn == 'index.json': continue
    m = json.load(open(MB + fn)); L, w, k0 = m['L'], m['w'], m['k0']
    if fn.startswith('opus'):
        side = fn[5]; E = opus_setup(side); exp = 'opus_' + side
    else:
        side = fn.split('_')[2]; E = tube_setup([c for c in ce if c['L'] == L][0], side); exp = f'L{L}_{side}'
    inv = {E['coord'][v]: v for v in E['S']}
    Smin = set()
    for r, cc, col in m['cells']:
        v = inv[(r, cc)]; assert E['col'][v] == col; Smin.add(v)
    adj, col, bd = E['adj'], E['col'], E['bd']
    assert unsat(adj, Smin, col, bd, w, k0)
    def pstate(S):
        out = []
        for r in range(w + 1):
            R = E['region'](r) & S; rv = E['rowv'](r)
            out.append((tuple(int(v in S) for v in rv), tuple(sorted(traces(adj, R, col, rv).items()))))
        return out
    st0 = pstate(Smin)
    dels = []
    for v in sorted(Smin):
        if E['depth'][v] == 0: continue
        S2 = Smin - {v}; ob = unsat(adj, S2, col, bd, w, k0)
        st2 = pstate(S2); r_v = E['depth'][v]; pos = E['rowv'](r_v).index(v) if r_v <= w else None
        diff_rows = [r for r in range(w + 1) if st0[r] != st2[r]]
        # traces with v's own position removed: does connectivity of the OTHER boundary vertices change?
        conn_rows = []
        for r in range(w + 1):
            t0 = dict(st0[r][1]); t2 = dict(st2[r][1])
            for p in t0:
                b0 = sorted(tuple(x for x in b if not (r == r_v and x == pos)) for b in t0[p]); b0 = sorted(b for b in b0 if b)
                if b0 != sorted(t2[p]): conn_rows.append(r); break
        dels.append(dict(v_row=r_v, v_col=E['coord'][v][1], obstructing=ob, state_rows_differ=diff_rows, connectivity_rows_differ=conn_rows))
    res.append(dict(name=fn[:-5], exp=exp, L=L, w=w, k0=k0, size=len(Smin), rows_used=m['rows_used'], cells=m['cells'], deletions=dels))
    nd = len(dels); npass = sum(not d['obstructing'] for d in dels)
    nconn0 = sum(1 for d in dels if not d['connectivity_rows_differ'])
    print(fn, 'size', len(Smin), 'deletions', nd, 'passing', npass, 'deletions with no connectivity change on any row', nconn0,
          'first row where state differs', sorted(set(min(d['state_rows_differ']) for d in dels if d['state_rows_differ'])), flush=True)
json.dump(res, open(OUT + 'minimal_vs_deletions.json', 'w'), indent=1)
