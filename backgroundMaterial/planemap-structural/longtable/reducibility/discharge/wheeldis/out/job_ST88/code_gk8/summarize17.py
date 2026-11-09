# W17 copy of W15's summarize15.py (+ drive17 lines, + W17 self-test / KS table / exname / pattern-count lines).
# code_gk (round 4): + the W17 GK lines (keys, amounts, window tables, self-tests).
# W15: summary of one w15_upper.sh run.  usage: python3 summarize15.py LOGDIR[,LOGDIR2..] DLIST [DMAXP]
# reads LOGDIR/p0.log (Python checks, query dump, tail), LOGDIR/sep.log (drive15 lines, one per (d, part)), LOGDIR/replay.jsonl
# (Python exact re-check of every reported arrangement, when any). Prints per-d lines and the verdict.
import sys, re, json, collections, os
LS = sys.argv[1].split(','); DL = [int(x) for x in sys.argv[2].split(',')]; DMAXP = int(sys.argv[3]) if len(sys.argv) > 3 else 17   # LOGDIR may be a comma list (one run split by degree)
p0 = [l.rstrip('\n') for L in LS if os.path.exists(os.path.join(L, 'p0.log')) for l in open(os.path.join(L, 'p0.log'))]
_seen = set()
for l in p0:
    if l in _seen: continue
    _seen.add(l)
    if re.search(r'^kill table U|^section 14 prime|^solution t =|^W10 families|^senderR2 rows \d|^  (five|nofive) |^bounds:|^mrowL|^V = 8 mrowL|^f2b tables|^MONO|^NOCLAMP|^f2b positive|^W10 self-test|^cons2|^CONS2 STEP|^W17 self-test \(|^W17 KS separator|^W17 GK|^sep: W17 GK|^exname:|^patterns distinct|^f2b self-test|^separator binary|^DP |^Karp tail', l): print(l[:400])
fails = sorted(set(l for l in p0 if l.startswith('FAIL:'))); verd = [l for l in p0 if l.startswith('VERDICT')]
T = None
for l in p0:
    m = re.match(r'^solution t = ([0-9.e+-]+)', l)
    if m: T = float(m.group(1))
jobs = collections.defaultdict(list)
for l in [l for L in LS if os.path.exists(os.path.join(L, 'sep.log')) for l in open(os.path.join(L, 'sep.log'))]:
    m = re.match(r'^drive1[57] d=(\d+) part=(\S+) neck=(\S+) bugfix=(\S+) thr=(\S+) reported (\d+) end=\[(.*?)\] rc=(-?\d+) (\d+)s(.*)$', l.strip())
    if m: jobs[int(m.group(1))].append(m.groups())
rep = collections.defaultdict(list)
for L in LS:
  if os.path.exists(os.path.join(L, 'replay.jsonl')):
    for l in open(os.path.join(L, 'replay.jsonl')):
        d, lk, sv, adm, v, _ = json.loads(l); rep[d].append((adm, v, lk, sv))
EPS = 1e-9; ok = True; per = {}; nviol = {}   # W17: nviol = exact violators found, also when the search hit its cap
for d in DL:
    J = jobs.get(d, [])
    parts = sorted({j[1] for j in J}); n_need = int(parts[0].split('/')[1]) if parts else 0
    complete = bool(J) and len(parts) == n_need and all(j[6].startswith('END') and j[6].split()[3:4] == ['0'] and j[7] == '0' and 'CAPHIT' not in j[9] for j in J)
    nrep = sum(int(j[5]) for j in J); secs = sum(int(j[8]) for j in J)
    viol = [r for r in rep.get(d, []) if r[0] and T is not None and r[1] > d - 6 + T + EPS]
    if nrep and len(rep.get(d, [])) < nrep: complete = False   # reported arrangements not all re-checked
    per[d] = len(viol) if complete else None; nviol[d] = len(viol)
    _pos = [0, 0, 0]; _sl = set(); _adm = [0, 0]; _admn = 0
    for j in J:
        _e = j[6].split()
        if 'POS' in _e: _i = _e.index('POS'); _pos = [a + int(b) for a, b in zip(_pos, _e[_i + 1:_i + 4])]
        if 'SLACK' in _e: _sl.add(_e[_e.index('SLACK') + 1])
        if 'POSADM' in _e: _i = _e.index('POSADM'); _adm = [a + int(b) for a, b in zip(_adm, _e[_i + 1:_i + 3])]; _admn += 1
    print('d=%d: %s (separator reported %d, Python exact re-check: %d violated%s; %d part(s), %ds CPU-wall%s)' % (
        d, ('exact violated %d' % len(viol)) if complete else 'NOT ESTABLISHED', nrep, len(viol), (', max excess %.3g' % max(r[1] - (d - 6 + T) for r in viol)) if viol else '',
        len(J), secs, '' if complete else ' -- missing / aborted / cap hit / not re-checked'))
    if J: print('  d=%d NOCLAMP counters: pruning slack %s; leaves reached with a positive f2b correction %d, of them above the threshold before the admissibility filters %d, crossing it only by the correction %d%s' % (d, ','.join(sorted(_sl)) or '?', _pos[0], _pos[1], _pos[2],
          ('; admissible (would be reported) %d, crossing only by the correction %d (from %d of %d part(s))' % (_adm[0], _adm[1], _admn, len(J))) if _admn else ''))
    for r in sorted(viol, key=lambda r: -r[1])[:5]: print('  VIOLATED receiverR2 d=%d exact load %.12f link %s s %s' % (d, r[1], r[2], r[3]))
for f in fails: print(f[:400])
for v in verd: print(v[:400])
pyok = bool(verd) and all('PASS' in v for v in verd) and not fails
allrun = all(per.get(d) is not None for d in DL); anyv = any(nviol.get(d) for d in DL)   # W17: an exact violator is a witness even if a part hit its cap
print('violators by d: %s' % {d: per[d] for d in DL})
full = set(DL) >= set(range(7, DMAXP + 1))
if anyv: print('RESULT: INFEASIBLE (exact receiver violators above)%s%s' % ('' if pyok else '; Python checks also FAIL', '' if allrun else '; some degree not finished (cap hit), so the violator counts are lower bounds'))
elif not pyok:
    _und = [int(m.group(1)) for l in p0 for m in [re.match(r'^DP d=(\d+) relaxed closed-walk bound', l)] if m]
    _kc = [float(m.group(1)) for l in p0 for m in [re.search(r'covered for d >= ([0-9.]+)', l)] if m]
    _need = max(_und + [0])   # DP covers DMAXP+1..30, Karp d >= X (X <= 31 needed): exhaust every undecided DP degree
    print('RESULT: NOT ESTABLISHED (a Python check FAILED: see FAIL lines)%s' % (('; the DP tail is undecided up to d = %d: rerun with DMAXP=%d' % (_need, _need)) if _need > DMAXP else '; Karp needs d >= %.3f <= 31' % _kc[0] if _kc and _kc[0] > 31 else ''))
elif not allrun: print('RESULT: NOT ESTABLISHED (some degree not finished)')
elif not full: print('RESULT: PARTIAL PASS: senders, cons2, mrowL, self-tests, DP %d..30 and Karp pass; receivers d = %s exhaustive 0 violated; d = %s NOT run' % (DMAXP + 1, ','.join(map(str, DL)), ','.join(str(d) for d in range(7, DMAXP + 1) if d not in DL)))
else: print('RESULT: FEASIBLE (every sender row, cons2, mrowL, d = 7..%d exhaustive, DP %d..30 and Karp pass)' % (DMAXP, DMAXP + 1))
