"""cost-aware removal: groups = rules (in current set) whose only justifier is config n and n justifies no table item alone; try removing a whole group.
usage: cfgdd.py START.json OUT.json"""
import sys, json, pickle, re, collections, time, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from client import *
start, outp = sys.argv[1:3]; cur = set(json.load(open(start)))
S71 = B + 's71_ruleset/'
d = pickle.load(open(S71 + 'cover.pkl', 'rb')); items = [it for it in pickle.load(open(S71 + 'items.pkl', 'rb')) if it[2]]; cls = d['cls']
Nn = lambda r: json.dumps(r, sort_keys=True, separators=(',', ':'))
def key(g, r): return ('R_' + g + '_0' if g.endswith('w6') else 'R_' + g, Nn(r))
ws = {(it[0], it[1]): it[2] for it in items if it[0].startswith('R_')}
RW = {i: ws[key(*L[i])] for i in range(len(L))}
tabforced = {next(iter(it[2])) for it in items if not it[0].startswith('R_') and len(it[2]) == 1}
rsr = {}
for l in open('/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/sp/rsst.txt'):
    f = l.split(); rsr[f[0].split('_')[0]] = int(f[1])
def ring(n):
    if n.startswith('rsst'): return rsr[n.split('_')[0]]
    m = re.search(r'_r(\d+)$', n)
    if m: return int(m.group(1))
    m = re.match(r'[a-z]+(\d+)_', n); return int(m.group(1)) if m else -1
isD = lambda n: cls[n].endswith('D') or cls[n] == 'nl51'
W = {13: .1, 14: 25 / 60, 15: 1.25, 16: 4, 17: 13}
def cost(n):
    if not isD(n): return .25
    r = ring(n); return 2. if r == -1 else 2 / 60 if r <= 12 else W[r]
LOG = open(S73 + 'run/cfgdd.log', 'a')
def log(m): LOG.write('%s %s\n' % (time.strftime('%H:%M:%S'), m)); LOG.flush()
for rnd in range(3):
    grp = collections.defaultdict(list)
    for i in cur:
        if len(RW[i]) == 1:
            n = next(iter(RW[i]))
            if n not in tabforced: grp[n].append(i)
    order = sorted(grp, key=lambda n: -cost(n) / len(grp[n]))
    log('round %d: %d rules, %d groups, top: %s' % (rnd, len(cur), len(order), [(n, cost(n), len(grp[n])) for n in order[:5]]))
    acc = 0; saved = 0.0; q = [n for n in order if cost(n) > 0.05]
    while q:
        batch = [q.pop(0)]
        if q: batch.append(q.pop(0))
        res = check_many([cur - set(grp[n]) for n in batch]); done = False
        for n, (ok, m) in zip(batch, res):
            if ok and not done: cur -= set(grp[n]); acc += 1; saved += cost(n); done = True
            elif ok: q.insert(0, n)
        json.dump(sorted(cur), open(outp, 'w'))
        log('rules %d accepted %d saved~%.1fh queue %d' % (len(cur), acc, saved, len(q)))
    if not acc: break
log('FINAL %d' % len(cur))
