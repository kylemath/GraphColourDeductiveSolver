#!/usr/bin/env python3
"""Build candidate reducible configuration pool + base discharging rules for beat_633/.

Reads read-only upstream sources and beat_633/data/e2_rsst_cmerge/ logs:
  1. 71 RSST base parts (rsst_drules.v, cross-checked against Lean B2 lean_parts.txt) + 8 N2 parts.
  2. All 633 RSST configurations:
       - 582 D2 / C2cons configs (admissibleX + foldSafeX + Lean / ST-120R [E2] verified)
       - 1 Lean-proved general-C config 2.126 (CGlueM.lean, 0 sorry)
       - 50 [E2] general-C configs (verified by kc -C2 + cfast --fixed + admissibleXM + foldSafeX + coherB + NoClassChord)
  3. Candidate small-ring super-killers (for k-for-1 compression, k >= 2):
       - pats44_f.txt (r=6..12 D and foldSafeX C configs)
       - nl51_kc.txt (r=6..13 D configs with m <= 11, max interior deg <= 11)
       - vc_fw_windows.tsv (D and foldSafeX C 2-ball window configs)
"""
import collections
import glob
import hashlib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, 'data')
os.makedirs(DATA, exist_ok=True)

# Import read-only helper functions from fullstack_t0/build_registry.py without modifying fullstack_t0/
sys.path.insert(0, '/Users/kylemathewson/GraphColouringNov/fullstack_t0')
import build_registry as br  # noqa: E402

WT = br.WT
WD = br.WD


def check_no_class_chord(c, eqR, eqI, lbl):
    """Exact decidable certificate for CGlueM.lean NoClassChord under NoSep + NoShortSepCycle.

    Returns (ok, mode) where:
      mode == 0: passes 2.126's exact CGlueM starB + chordB checks verbatim.
      mode == 1: passes general CGlueM NoClassChord (every same-label touched ring pair (s, t) with s != t
                 is either at one star center passing chordB, or connected by an eqI interior path of length
                 2 or 3 whose exterior chord T.Adj(rho(s), rho(t)) would create a separating 4- or 5-cycle).
    """
    if not br.lean_admissible_x(c, eqR, eqI, lbl, check_ring_distinct=False):
        return False, -1
    if not br.lean_fold_safe_x(c, eqR, eqI, lbl):
        return False, -1
    m, r = c['m'], c['ring']
    ring_adj, int_adj = br.cfg_ring_int_adj(c)
    touched = sorted({t for t, _ in eqR})

    # coherB: touched s != t in different classes -> exclB or cycEx
    for s in touched:
        for t in touched:
            if lbl[m + s] != lbl[m + t] and s != t:
                if not (br._excl_b(m, r, ring_adj, int_adj, s, t) or br._cyc_ex(m, r, ring_adj, int_adj, s, t)):
                    return False, -1

    if br.lean_merge_checks_2o126(c, eqR, eqI, lbl):
        return True, 0

    eqR_by_r = collections.defaultdict(list)
    for t, a in eqR:
        eqR_by_r[t].append(a)
    eqI_adj = collections.defaultdict(list)
    for a, b in eqI:
        eqI_adj[a].append(b)
        eqI_adj[b].append(a)

    def chord_b_at(c_idx, s, t):
        rc = c['rot'][c_idx]
        g = len(rc)
        for j in range(g):
            if rc[j] == ['R', s]:
                if rc[(j - 1) % g] == ['R', t] or rc[(j + 1) % g] == ['R', t]:
                    return False
        return True

    def sep_cycle_4_or_5(s, t):
        # Ring-adjacent touched slots in the same class cannot be ruled out as non-adjacent!
        if t == (s + 1) % r or s == (t + 1) % r:
            return False
        # Find simple eqI path between an eqR neighbor of s and an eqR neighbor of t
        for a0 in eqR_by_r[s]:
            q = collections.deque([[a0]])
            while q:
                path = q.popleft()
                last = path[-1]
                if last in eqR_by_r[t]:
                    plen = len(path)
                    if plen == 1:
                        if chord_b_at(last, s, t):
                            return True
                    elif plen in (2, 3):
                        # Cycle (rho(s), iota(path[0]), ..., iota(path[-1]), rho(t)) has length plen + 2 in {4, 5}.
                        # Check existence of an interior edge (u, v) on path whose two facial apexes e1, e2 in I
                        # lie strictly on opposite sides off the cycle (matching CGlue.lean cycEx_sound).
                        for j in range(plen - 1):
                            u, v = path[j], path[j + 1]
                            if any(sr in ring_adj[v] for sr in ring_adj[u]):
                                continue
                            common_i = [e for e in int_adj[u] if e in int_adj[v]]
                            # Both facial triangles of interior edge (u, v) must have interior apexes off the path
                            # (since ring_adj[u] & ring_adj[v] == empty, neither facial apex can be a ring vertex!).
                            if len(common_i) < 2:
                                continue
                            ok_apex = True
                            for e in common_i:
                                if e in path:
                                    ok_apex = False
                                    break
                                if plen == 3 and not any(0 <= f < m and f not in path for f in int_adj[e]):
                                    ok_apex = False
                                    break
                            if ok_apex:
                                return True
                if len(path) < 3:
                    for nb in eqI_adj[last]:
                        if nb not in path:
                            q.append(path + [nb])
        return False

    by_lbl = collections.defaultdict(list)
    for t in touched:
        by_lbl[lbl[m + t]].append(t)
    for lv, ts in by_lbl.items():
        for i in range(len(ts)):
            for j in range(i + 1, len(ts)):
                if not sep_cycle_4_or_5(ts[i], ts[j]):
                    return False, -1
    return True, 1


def canon_rot_key(c):
    """Canonical signature up to interior relabeling? Fast exact signature for deduplicating identical entries."""
    return (c['ring'], c['m'], tuple(c['deg']), json.dumps(c['rot']))


def main():
    p71, pn2, p79 = br.build_parts79()
    print(f'Verified 71 RSST parts + 8 N2 parts (79 total).')

    # 1. Load all 633 RSST configurations
    rsst_confs = br.parse_unavoidable_conf()
    rsst_kc_lines = [l.strip() for l in open(br.RSST_KC) if l.strip()]
    verds = []
    for line in open(br.VERD):
        f = line.split()
        if f and f[0].startswith('rsst') and len(f) > 2:
            vd = [z for z in f if z.startswith('verdict=')][0].split('=')[1]
            xtok = [z for z in f if z.startswith('X=')][0].split('=', 1)[1].strip('{}')
            verds.append((f[0], vd, xtok))
    assert len(rsst_confs) == len(rsst_kc_lines) == len(verds) == 633

    # Load cmerge51 verification records from task-673
    cmerge_raw = json.load(open(os.path.join(DATA, 'rsst51_verified_cmerge.json')))
    cmerge_map = {row[0]: (row[1], row[2], row[3], row[4]) for row in cmerge_raw}
    assert len(cmerge_map) == 51

    st120r = {}
    for line in open(os.path.join(WD, 'out/job_ST120R/verdicts.tsv')):
        f = line.rstrip('\n').split('\t')
        assert f[3] == 'PASS', f
        st120r[f[0]] = f

    st122 = {}
    for line in open(os.path.join(WD, 'out/job_ST122/results.tsv')):
        if line.startswith('#') or line.startswith('idx\t') or not line.strip():
            continue
        f = line.rstrip('\n').split('\t')
        assert f[14] == 'CONFIRMED', f
        st122[f[1]] = f

    in_lean179 = {}
    for line in open(os.path.join(WD, 'out/job_ST113/rsst582_lean_coverage.tsv')):
        if line.startswith('#') or not line.strip():
            continue
        f = line.rstrip('\n').split('\t')
        if f[5] == 'covered':
            in_lean179[f[0]] = f[6]

    pool = []
    mode_counts = collections.Counter()
    for idx, (c, kcl, (rid, vd, xtok)) in enumerate(zip(rsst_confs, rsst_kc_lines, verds)):
        assert rid.startswith('rsst%03d_' % idx)
        c['rsst_id'] = rid
        c['kc_line'] = kcl
        if vd in ('D2', 'C2cons'):
            if rid in in_lean179:
                tier = 'L'
                subtier = 'L_full' if vd == 'D2' else 'L_eval'
                ev = f'ST-113 Lean ({in_lean179[rid]}) + {vd}'
            elif rid in st122:
                tier = 'L'
                subtier = 'L_full' if st122[rid][9] == 'yes' else 'L_eval'
                ev = f'ST-122 Lean ({st122[rid][15]}) + {vd}'
            else:
                assert rid in st120r, rid
                tier = 'E2'
                subtier = 'E2'
                ev = f'ST-120R PASS ({st120r[rid][4]}) + {vd}'
            c['source'] = 'RSST_582'
            c['kind'] = 'D' if vd == 'D2' else 'C'
            c['X'] = '-' if vd == 'D2' else xtok
            c['rim_pinned'] = ('R' in xtok) if vd == 'C2cons' else False
            if vd == 'C2cons':
                eqR, eqI, lbl = br.parse_x_and_labels(c['m'], c['ring'], xtok)
                assert br.lean_admissible_x(c, eqR, eqI, lbl)
                assert br.lean_fold_safe_x(c, eqR, eqI, lbl)
                c['eqR'], c['eqI'], c['lbl'] = eqR, eqI, lbl
                c['cmerge_mode'] = -1
            c['tier'] = tier
            c['subtier'] = subtier
            c['evidence'] = ev
        else:
            assert rid in cmerge_map, rid
            _, _, xcm, _ = cmerge_map[rid]
            eqR, eqI, lbl = br.parse_x_and_labels(c['m'], c['ring'], xcm)
            ok_nc, mode_nc = check_no_class_chord(c, eqR, eqI, lbl)
            assert ok_nc, f'NoClassChord failed on {rid} ({c["name"]}) X={xcm}'
            mode_counts[mode_nc] += 1
            # Also verify two-engine log exists and passed in beat_633/data/e2_rsst_cmerge/
            out_fn = os.path.join(DATA, 'e2_rsst_cmerge', f'{rid}.out')
            out_txt = open(out_fn).read()
            assert 'C-REDUCIBLE' in out_txt and 'leftover bad classes extending after contraction = 0' in out_txt, rid
            c['eqR'], c['eqI'], c['lbl'] = eqR, eqI, lbl
            c['cmerge_mode'] = mode_nc
            c['X'] = xcm
            c['rim_pinned'] = ('R' in xcm)
            c['kind'] = 'C_merge'
            if c['name'] == '2.126':
                c['source'] = 'RSST_2o126_LEAN'
                c['tier'] = 'L'
                c['subtier'] = 'L_full'
                c['evidence'] = f'Lean 4 0-sorry CGlueM.lean + E2 ({out_fn})'
            else:
                c['source'] = 'RSST_CMERGE'
                c['tier'] = 'E2'
                c['subtier'] = 'E2'
                c['evidence'] = f'E2 kc -C2 + cfast --fixed ({out_fn}) + CGlueM mode={mode_nc}'
        pool.append(c)

    assert len(pool) == 633
    print(f'Verified all 633 RSST configs! (582 D2/C2cons + 51 C_merge: mode0_star={mode_counts[0]}, mode1_sep45={mode_counts[1]})')

    # 2. Add candidate small-ring super-killers from pats44_f.txt, nl51_kc.txt (r <= 13), and vc_fw_windows.tsv
    seen_rot = {canon_rot_key(c) for c in pool}
    seen_names = {c['name'] for c in pool}

    # 2a. pats44_f.txt
    pats_df = set()
    for line in open(os.path.join(WD, 'loop/k44/A_df.out')):
        if 'D=true' in line:
            pats_df.add(line.split()[0])
    pats_cf = {}
    cur_nm = None
    for line in open(os.path.join(WD, 'loop/k44/A_cf.out')):
        if not line.startswith(' ') and 'r=' in line:
            cur_nm = line.split()[0]
        elif cur_nm and 'C-REDUCIBLE, leftover bad classes extending after contraction = 0' in line:
            m = re.search(r'fixed X=\{([^}]+)\}', line)
            if m:
                pats_cf[cur_nm] = m.group(1)

    n_pats = 0
    for line in open(os.path.join(WD, 'loop/k44/pats44_f.txt')):
        if not line.strip():
            continue
        nm = line.split()[0]
        if nm in seen_names:
            continue
        if nm not in pats_df and nm not in pats_cf:
            continue
        try:
            e = br.kc_to_entry(line)
        except AssertionError:
            continue
        if e['m'] > 12 or max(e['deg']) > 11:
            continue
        rk = canon_rot_key(e)
        if rk in seen_rot:
            continue
        if nm in pats_df:
            e['source'] = 'SUPER_PATS44'
            e['kind'] = 'D'
            e['X'] = '-'
            e['rim_pinned'] = False
            e['tier'] = 'E2_CAND'
            e['subtier'] = 'E2_CAND'
            e['evidence'] = 'k44 A_df.out D=true (will re-verify with kc + dfast18 if selected)'
        else:
            xtok = pats_cf[nm]
            eqR, eqI, lbl = br.parse_x_and_labels(e['m'], e['ring'], xtok)
            if not (br.lean_admissible_x(e, eqR, eqI, lbl) and br.lean_fold_safe_x(e, eqR, eqI, lbl)):
                continue
            e['source'] = 'SUPER_PATS44'
            e['kind'] = 'C'
            e['X'] = xtok
            e['rim_pinned'] = ('R' in xtok)
            e['eqR'], e['eqI'], e['lbl'] = eqR, eqI, lbl
            e['tier'] = 'E2_CAND'
            e['subtier'] = 'E2_CAND'
            e['evidence'] = f'k44 A_cf.out C2cons X={{{xtok}}} + admissibleX/foldSafeX'
        seen_rot.add(rk)
        seen_names.add(nm)
        pool.append(e)
        n_pats += 1

    # 2b. ST-119 s*.tsv + vc_fw_windows.tsv (D and foldSafeX C windows)
    n_win = 0
    vc_ok = set()
    for i, line in enumerate(open(os.path.join(WD, 'out/job_ST119/in/results/vc_fw_windows.tsv'))):
        if i == 0 or not line.strip():
            continue
        f = line.rstrip('\n').split('\t')
        if f[23] == 'True' and f[24] == 'True':
            vc_ok.add(f[0])

    for fn_s in sorted(glob.glob(os.path.join(WD, 'out/job_ST119/in/results/s*.tsv'))):
        if fn_s.endswith('.log'):
            continue
        for line in open(fn_s):
            f = line.rstrip('\n').split('\t')
            if len(f) < 12:
                continue
            nm, vd, xstr, v2_s, kcl = f[0], f[4], f[6], f[10], f[11]
            if nm in seen_names:
                continue
            if vd == 'D' and 'dfast18:D' in v2_s:
                pass
            elif vd == 'C' and 'cfast:C-REDUCIBLE' in v2_s and nm in vc_ok:
                pass
            else:
                continue
            try:
                e = br.kc_to_entry(kcl)
            except AssertionError:
                continue
            rk = canon_rot_key(e)
            if rk in seen_rot:
                continue
            if vd == 'D':
                e['source'] = 'SUPER_WIN'
                e['kind'] = 'D'
                e['X'] = '-'
                e['rim_pinned'] = False
            else:
                eqR, eqI, lbl = br.parse_x_and_labels(e['m'], e['ring'], xstr)
                if not (br.lean_admissible_x(e, eqR, eqI, lbl) and br.lean_fold_safe_x(e, eqR, eqI, lbl)):
                    continue
                e['source'] = 'SUPER_WIN'
                e['kind'] = 'C'
                e['X'] = xstr
                e['rim_pinned'] = ('R' in xstr)
                e['eqR'], e['eqI'], e['lbl'] = eqR, eqI, lbl
            e['tier'] = 'E2_CAND'
            e['subtier'] = 'E2_CAND'
            e['evidence'] = f'ST-119 window ({vd})'
            seen_rot.add(rk)
            seen_names.add(nm)
            pool.append(e)
            n_win += 1

    # 2c. nl51_kc.txt with ring <= 13, m <= 11, max_deg <= 11
    n_nl = 0
    for line in open(br.NL51_KC):
        if not line.strip():
            continue
        f = line.split()
        nm, r, m = f[0], int(f[1]), int(f[2])
        if r > 13 or m > 11 or nm in seen_names:
            continue
        e = br.kc_to_entry(line)
        if max(e['deg']) > 11:
            continue
        rk = canon_rot_key(e)
        if rk in seen_rot:
            continue
        e['source'] = 'SUPER_NL51'
        e['kind'] = 'D'
        e['X'] = '-'
        e['rim_pinned'] = False
        e['tier'] = 'E2_CAND'
        e['subtier'] = 'E2_CAND'
        e['evidence'] = 'nl51_kc.txt D-config (will re-verify with kc + dfast18 if selected)'
        seen_rot.add(rk)
        seen_names.add(nm)
        pool.append(e)
        n_nl += 1

    for idx, c in enumerate(pool):
        c['id'] = idx

    print(f'Added external super-killer candidates: pats44={n_pats}, win={n_win}, nl51_r<=13={n_nl} -> total pool={len(pool)}')

    # Write parts71.json, parts79.json, pool_configs.json, and flat C++ input file pool_input.txt
    for fn_out, plist, desc in [
        ('parts71.json', p71, 'RSST 71 base parts (scale M=10, unit weight 1)'),
        ('parts79.json', p79, 'RSST 71 base parts + 8 N2 parts (scale M=10, unit weight 1)'),
    ]:
        with open(os.path.join(DATA, fn_out), 'w') as f:
            json.dump({
                'description': desc,
                'scale_M': 10,
                'parts': [
                    {
                        'idx': i,
                        'tag': tag,
                        'hub': len(p),
                        'target': 2,
                        'weight': 1,
                        'subs': [[list(s), list(h), [list(x) for x in fs]] for s, h, fs in p],
                    }
                    for i, (tag, p) in enumerate(plist)
                ],
            }, f, indent=2)

    with open(os.path.join(DATA, 'pool_configs.json'), 'w') as f:
        json.dump({'count': len(pool), 'rsst_count': 633, 'configs': pool}, f, indent=2)

    with open(os.path.join(DATA, 'pool_input.txt'), 'w') as f:
        f.write(f'SCALE 10\n')
        f.write(f'PARTS {len(p71)}\n')
        for tag, p in p71:
            toks = [tag, str(len(p)), '1']
            for s, h, fs in p:
                toks.extend([str(s[0]), str(s[1]), str(h[0]), str(h[1]), str(len(fs))])
                for fr in fs:
                    toks.extend([str(fr[0]), str(fr[1])])
            f.write(' '.join(toks) + '\n')
        f.write(f'CONFIGS {len(pool)}\n')
        for c in pool:
            hdr = [
                str(c['id']), c['name'], c['source'], c['kind'], c['tier'],
                '1' if c['rim_pinned'] else '0', str(c['ring']), str(c['m']),
            ]
            f.write(' '.join(hdr) + '\n')
            for u in range(c['m']):
                rt = c['rot'][u]
                row = [str(len(rt))]
                for kind, val in rt:
                    row.extend(['0' if kind == 'I' else '1', str(val)])
                f.write(' '.join(row) + '\n')
    print(f'Wrote {DATA}/pool_configs.json and {DATA}/pool_input.txt.')


if __name__ == '__main__':
    main()
