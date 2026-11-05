# B3: route.tsv (my D/C windows) -> configs files by LP route, with q-names and the slots each window reads beyond the
# current table window.  usage: python3 mkconfigs.py route.tsv OUTDIR
import sys, os
from lprime import lp
from aprime import ap
RT, OD = sys.argv[1], sys.argv[2]
G = {'Lp': [], 'L': [], 'Ap': [], 'A': [], 'F': [], 'X': [], 'C': []}
for l in open(RT):
    if l.startswith('#'): continue
    g = l.rstrip('\n').split('\t'); c, r, m, nm, fam, conf, rt, ent, rows, kl = g
    isC = conf.startswith('kcc:C')
    rows_t = ' '.join(x for x in rows.split() if '[v1' in x); nrows = len(rows.split())
    rec = None
    if rt in ('L', 'X7') and nm.startswith('b7_') and nm.count('_p') == 1:
        sg, key, extra, ex, q = lp(nm)
        rec = ('L' if not extra else 'Lp', '%s | l3q side %s | read outside the l3q payee window: %s | %s | rows %d: %s' % (kl, key, ex or '(none)', q, nrows, rows_t))
    elif rt in ('A', "A'"):
        k, ex, q = ap(nm)
        rec = ('A' if ex.startswith('(none') else 'Ap', '%s | kill6 %s | read outside the kill6 key: %s | %s | rows %d: %s' % (kl, k, ex, q, nrows, rows_t))
    elif rt == 'F':
        rec = ('F', '%s | %s | rows %d: %s' % (kl, ent, nrows, rows_t))
    else:
        rec = ('X', '%s | %s | rows %d: %s' % (kl, ent, nrows, rows_t))
    G[rec[0]].append(('[%s] ' % conf.split('cfast')[0][4:].strip() if isC else '') + rec[1] + '  # r%s m%s %s' % (r, m, fam))
    if isC: G['C'].append(rec[1] + '  # r%s m%s %s %s' % (r, m, fam, conf[:40]))
HDR = {
 'Lp': "# Route L' (row-level l3q mask). Two-engine D (kcc+dfast+dfast18) unless marked [C]. Kills letter a2 of the l3q payee side\n# (private of the link 7 next to apex a, c,a <= 6). The window reads link/apex slots outside the RELAY_SPEC 21.4 payee window;\n# the payee's receiver row reads them exactly, so it may credit Q[(c,a,m minus the letter)] there. No new LP column.\n",
 'L': "# Route L (plain l3q table entry, PRIVCELL_SPEC 2.4): window inside the payee window; kill the letter in every L3T key consistent with it.\n",
 'Ap': "# Route A' (wider kill6 mask, PRIVCELL_SPEC 2.1 (A')). Two-engine D unless [C]. Kills a private letter of a link 6; the window reads\n# slots outside the kill6 key (u, w_{j-2..j+2}, s_{j-2..j+1}); M is keyed by (sig2, mask), so no new column, but the mask lookup must read them.\n",
 'A': "# Route A (plain kill6 entry, inside the key): k6patch-style table bits.\n",
 'F': "# Route F (u-centred receiver pattern): the whole context is reducible; add as an f-name / q-name with empty PRIV.\n",
 'X': "# Route X (cell kill: two privates, a ring-3 vertex, or a private of a 7 not next to a small apex): needs a new key / cluster row.\n",
 'C': "# C-reducible windows (kcc -C and cfast --fixed X both C-REDUCIBLE; |X| <= 4). Need ring-merge / Lean hC checks before use.\n"}
FN = {'Lp': 'configs_D_l3qrow.txt', 'L': 'configs_D_l3q.txt', 'Ap': 'configs_D_kill6wide.txt', 'A': 'configs_D_kill6.txt', 'F': 'configs_D_rows.txt', 'X': 'configs_D_cells.txt', 'C': 'configs_C_all.txt'}
for k, L in G.items():
    if not L: continue
    with open(os.path.join(OD, FN[k]), 'w') as f:
        f.write(HDR[k] + '# columns: kc line | route entry | extra slots | q-name (PRIVCELL grammar, not canonicalised) | rows touched (count: target rows)\n')
        for x in L: f.write(x + '\n')
    print(FN[k], len(L))
