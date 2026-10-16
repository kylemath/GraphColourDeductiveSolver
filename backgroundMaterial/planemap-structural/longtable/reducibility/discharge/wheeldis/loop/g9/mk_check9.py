"""G9 probe 2 (exploratory): writes loop/g9/defect_check2_9.py from loop/g9/defect_check2_8.py: receivers of every degree
>= 7 (a centre of degree 9..12 included; its own wheel has no registry -> not reducible, no test requested); letters
>= 9 read as 9 (= B in keys); B-fixed configurations also looked up by their gen28 name f<d>_<link>_<s> (when the
ring is simple without pinching and no letter >= 9 is in the configuration) in out/job28/*.out|cfast, loop/lp/*.out|cfast
and loop/g9/g9_*.dfast.out; e/p receiver-centred verdicts also read from loop/lp/*.out and loop/g9/g9_*.dfast.out."""
import os
G9 = os.path.dirname(os.path.abspath(__file__))
s = open(os.path.join(G9, 'defect_check2_8.py')).read()
def rep(a, b, cnt=1):
    global s
    assert s.count(a) == cnt, (a, s.count(a)); s = s.replace(a, b)
rep('"""[G9 copy, see loop/g9/mk_check8.py', '"""[G9 probe-2 copy (mk_check9.py): receivers of degree >= 7, f-name lookup for B-fixed]\n[G9 copy, see loop/g9/mk_check8.py')
rep("T8 = {}\n", """T8 = {}
DVF, CVF = {}, {}
for fn in glob.glob(os.path.join(HERE, 'out', 'job28', '*.out')) + glob.glob(os.path.join(HERE, 'loop', 'lp', '*.out')) + glob.glob(os.path.join(G9, 'g9_*.dfast.out')):
    for line in open(fn):
        f = line.split()
        if not f or ('D=true' not in line and 'D=false' not in line): continue
        if re.match(r'^f\\d+_', f[0]): DVF[f[0]] = 'D' if 'D=true' in line else 'notD'
        elif re.match(r'^[ep]\\d+_', f[0]) and 'loop' in fn: TESTED[key_of_name(f[0])] = 'D' if 'D=true' in line else 'notD'
for fn in glob.glob(os.path.join(HERE, 'out', 'job28', '*.cfast')) + glob.glob(os.path.join(HERE, 'loop', 'lp', '*.cfast')):
    cur = None
    for line in open(fn):
        if ' r=' in line and not line.startswith(' '): cur = line.split()[0]
        elif 'C-REDUCIBLE' in line and cur: CVF[cur] = 'C'
        elif 'search |X|' in line and cur: CVF.setdefault(cur, 'neither')
""")
rep("        if deg.get(u) not in (7, 8): continue", "        if deg.get(u) is None or deg[u] < 7: continue")
rep("w7 = (T7 if d == 7 else T8).get(cw)", "w7 = (T7 if d == 7 else T8 if d == 8 else {}).get(cw)")
rep("        if w7 == 'D': st['D'] += 1; st['W%dD' % d] += 1\n", "        if d >= 9: st['bigcentre_wheel_untested'] += 1\n        elif w7 == 'D': st['D'] += 1; st['W%dD' % d] += 1\n")
rep("        L_ = ''.join(str(deg[x]) for x in lk); S_ = ''", "        L_ = ''.join(str(min(deg[x], 9)) for x in lk); S_ = ''")
rep("S_ += str(deg[com[0]])", "S_ += str(min(deg[com[0]], 9))")
rep("                    cb = extract_cfg(adj, deg, Ib)\n",
    """                    cb = extract_cfg(adj, deg, Ib); fnm = None
                    if cb is not None:
                        wl_ = {(i + e) % d for i in S for e in (-1, 0, 1)}; sl_ = {(i + e) % d for i in S for e in (-1, 0)}
                        if all(L_[j] != '9' for j in wl_) and all(S_[j] != '9' for j in sl_):
                            kf = canon_key(d, ''.join(L_[j] if j in wl_ else '.' for j in range(d)), ''.join(S_[j] if j in sl_ else '.' for j in range(d)))
                            fnm = 'f%d_%s_%s' % (d, kf[1], kf[2])
""")
rep("kb = 'b' + hashlib.sha1(cb.encode()).hexdigest()[:16]; db = DRES.get(kb); cbv = CRES.get(kb)",
    """kb = 'b' + hashlib.sha1(cb.encode()).hexdigest()[:16]; db = DRES.get(kb); cbv = CRES.get(kb)
                        if fnm and DVF.get(fnm) == 'D': db = 'D'
                        elif fnm and db is None and fnm in DVF: db = DVF[fnm]
                        if fnm and CVF.get(fnm) == 'C': cbv = 'C'
                        elif fnm and cbv is None and fnm in CVF: cbv = CVF[fnm]""")
open(os.path.join(G9, 'defect_check2_9.py'), 'w').write(s)
print('ok')
