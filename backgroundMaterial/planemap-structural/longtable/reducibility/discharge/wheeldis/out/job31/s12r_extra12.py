"""s12r50 add-on (Long Table 00:44Z): the 12 g2 columns loaded only from cons2 rows (Opus's list).
(a) every cons2 row (any non-R6 L, any apex word s over 5..9) in which one of them occurs gets it from a five whose own
    5-word (6, L_{i+1}, s_i, s_{i-1}, L_{i-1}) is in R5;  (b) no senderR2 row (any admissible assignment) uses them, and
receiverR2 rows carry no g terms at all (spec 12.5). Uses s12r_check.py's spec-side code up to the cons2 section.
Usage: WLP3X_DEF=1 WLP_SEPF=1 python3 out/job31/s12r_extra12.py SOL CERT ARGSFILE"""
import sys, os
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 's12r_check.py')).read()
src = src[:src.index('# ================= 12.4')].replace('os.path.abspath(__file__)', repr(os.path.join(os.path.dirname(os.path.abspath(__file__)), 's12r_check.py')))
exec(src)
K12 = [tuple(int(ch) for ch in k) for k in '5001655 5010655 5011655 5100655 5101655 5110655 5111655 6001655 6010655 6011655 6101655 6111655'.split()]
print('12 keys: in sender rows (deduped) %d; positive in the solution %d (%s)' % (
    sum(k in GSEND for k in K12), sum(G.get(k, 0) > 0 for k in K12), ' '.join(''.join(map(str, k)) for k in K12 if G.get(k, 0) <= 0)))
# (b) all admissible sender assignments, not only the deduped rows
used = set()
for w in SENDERS:
    sixes = [k for k in range(5) if w[k] == 6]; hats = sorted({m for k in sixes for m in (k, (k - 1) % 5)})
    for hb in itertools.product((0, 1), repeat=len(hats)):
        for fb in itertools.product((0, 1), repeat=len(sixes)):
            r = sender_row(w, dict(zip(hats, hb)), dict(zip(sixes, fb)))
            if r: used |= {k[1] for k in r if k[0] == 'g'} & set(K12)
print('(b) senderR2: %d of the 12 keys occur in any admissible assignment; receiverR2 rows have no g terms (spec 12.5)' % len(used))
# (a) every occurrence in a cons2 row over real letters
ALL6 = sorted({canon(L) for L in itertools.product(LET, repeat=6) if not isR6(L)})
occ = bad = 0; words = set()
for L in itertools.product(LET, repeat=6):          # every orientation, since a cons2 label need not be canonical
    if isR6(L) or 5 not in L: continue
    for i in range(6):
        if L[i] != 5: continue
        for si, sim in itertools.product(LET, repeat=2):   # only s_i and s_{i-1} enter this five's key
            k = g2_raw(L[(i + 1) % 6], c(L[(i + 2) % 6]), c(L[(i + 3) % 6]), c(L[(i + 4) % 6]), L[(i + 5) % 6], ap(si), ap(sim))
            if k in K12:
                occ += 1; fw = (6, L[(i + 1) % 6], si, sim, L[(i + 5) % 6]); words.add(canon(fw))
                if not isR5(fw): bad += 1; bad <= 5 and print('NOT R5: L %s i %d s_i %d s_i-1 %d five word %s' % (L, i, si, sim, fw))
print('(a) occurrences of the 12 keys in cons2 rows (non-R6 L in every orientation, s_i, s_{i-1} over 5..9): %d; five words not in R5: %d; distinct five words %s'
      % (occ, bad, sorted(''.join(map(str, w)) for w in words)))
print('EXTRA12: %s' % ('PASS' if bad == 0 and not used else 'FAIL'))
