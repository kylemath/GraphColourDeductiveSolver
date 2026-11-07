"""JCOV (Studio, 6 Nov): index every Conf literal in tracked .lean files on this checkout and the theorem that proves it.
Output: JSON list of {file, list, idx, def, name, r, m, ra, ia, kind, thm, how}. Our own files only (git ls-files)."""
import re, subprocess, json, sys, os, collections
ROOT = subprocess.check_output(['git', 'rev-parse', '--show-toplevel'], text=True).strip()
TR = set(subprocess.check_output(['git', 'ls-files', '*.lean'], cwd=ROOT, text=True).split())
files = sorted(TR | {os.path.relpath(os.path.join(dp, f), ROOT) for top in ('backgroundMaterial', 'out') for dp, dn, fn in os.walk(os.path.join(ROOT, top)) if '/.lake' not in dp for f in fn if f.endswith('.lean')})
files = [f for f in files if '/.lake/' not in f]
LIT = re.compile(r'name := "([^"]*)",?\s*r := (\d+),?\s*m := (\d+),?\s*ringAdj := (#\[\]|#\[.*?\]\]),?\s*intAdj := (#\[\]|#\[.*?\]\])', re.S)
arr = lambda s: [[int(x) for x in g.split(',') if x.strip()] for g in re.findall(r'#\[([^\[\]]*)\]', s[2:-1])] if s != '#[]' else []
ents = []; thms = []
for f in files:
    T = open(os.path.join(ROOT, f), errors='ignore').read()
    if 'ringAdj :=' in T:
        # enclosing defs: positions of 'def X' and list openings
        defs = [(m.start(), m.group(1)) for m in re.finditer(r'^def (\w+)', T, re.M)]
        cnt = collections.Counter()
        for m in LIT.finditer(T):
            d = [n for p, n in defs if p < m.start()]; d = d[-1] if d else None
            idx = cnt[d]; cnt[d] += 1
            ents.append(dict(file=f, defn=d, idx=idx, name=m[1], r=int(m[2]), m=int(m[3]), ra=arr(m[4]), ia=arr(m[5])))
    ns = None
    for line in T.split('\n'):
        mn = re.match(r'namespace (\S+)', line)
        if mn: ns = mn[1]
        mt = re.match(r'theorem (\w+) : (DCheck18\.dReducible|cReducible18) \((\w+)\.get ⟨(\d+)', line)
        if mt: thms.append(dict(tracked=f in TR, file=f, thm=(ns + '.' if ns else '') + mt[1], kind='D' if 'dRed' in mt[2] else 'C', defn=mt[3], idx=int(mt[4]), how='get')); continue
        mt = re.match(r'theorem (\w+) \(k : Fin (\d+)\) : (DCheck18\.dReducible|cReducible18) \((\w+)\.get', line)
        if mt:
            for k in range(int(mt[2])): thms.append(dict(tracked=f in TR, file=f, thm=(ns + '.' if ns else '') + mt[1], kind='D' if 'dRed' in mt[3] else 'C', defn=mt[4], idx=k, how='all'))
            continue
        mt = re.match(r'theorem (\w+) : run (cfg_\w+) = \{ classes := (\d+), ext := \d+, reached := (\d+)', line)
        if mt: thms.append(dict(tracked=f in TR, file=f, thm=(ns + '.' if ns else '') + mt[1], kind='D' if mt[3] == mt[4] else 'notD', defn=mt[2], idx=0, how='run')); continue
        mt = re.match(r'theorem (\w+) : dReducible (cfg_\w+) = true', line)
        if mt: thms.append(dict(tracked=f in TR, file=f, thm=(ns + '.' if ns else '') + mt[1], kind='D', defn=mt[2], idx=0, how='dred')); continue
        mt = re.match(r'theorem (\w+) : \(#\[([^\]]*)\] : Array Conf\)\.all agreesRSST = true', line)
        if mt:
            for c in re.findall(r'cfg_\d+', mt[2]): thms.append(dict(tracked=f in TR, file=f, thm=(ns + '.' if ns else '') + mt[1], kind='agree', defn=c, idx=0, how='agree'))
            continue
        mt = re.match(r'theorem (\w+) : \(rsst\.filter (.*)\)\.all agreesRSST = true', line)
        if mt: thms.append(dict(tracked=f in TR, file=f, thm=(ns + '.' if ns else '') + mt[1], kind='agree', defn='rsst', idx=0, how='agreeR:' + mt[2]))
json.dump(dict(ents=ents, thms=thms), open(sys.argv[1], 'w'))
print(len(files), 'files;', len(ents), 'conf literals;', len(thms), 'theorem refs', collections.Counter(t['how'].split(':')[0] for t in thms))
