#!/usr/bin/env python3
"""Finalize beat_633 unavoidable set + weighted signed-cochain rules + standalone certificates.

Pipeline:
  1. Runs Exact Benders MILP (`solve_hitting_set.run_benders`) on `synth_rules.txt` across the full
     4,095-config pool U (applying any free deletions and k-for-1 super-killer substitutions on top of
     the synthesized 2-ball rules!).
  2. Prunes any unused synthesized parts (if a config backed by a rule was later replaced k-for-1 or
     subsumed), keeping the rule set minimal and mirror-closed.
  3. Runs two independent C/C++ reducibility engines (`kc` + `dfast18` for D; `kc -C2` + `cfast --fixed`
     for C) on EVERY selected external super-killer (`id >= 633`), saving full logs to `data/e2_super/`
     and verifying `lean_admissible_x` + `lean_fold_safe_x`.
  4. Exports `data/final_rules.json`, `data/final_registry.json`, and `data/final_pool_single.txt`,
     and runs `bin/fast_compress --mode cert` to emit full replayable certificates (`data/cert_karp_tail.json`
     and `data/certs/cert_d*.jsonl`).
"""
import collections
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, 'data')
BIN_COMP = os.path.join(HERE, 'bin', 'fast_compress')

sys.path.insert(0, '/Users/kylemathewson/GraphColouringNov/fullstack_t0')
import build_registry as br  # noqa: E402
import build_pool as bp  # noqa: E402
import solve_hitting_set as shs  # noqa: E402

WD = br.WD
KC_BIN = os.path.join(WD, 'loop/kc/kc')
DF_BIN = os.path.join(WD, 'out/job52/dfast18')
CF_BIN = os.path.join(WD, 'out/job52/cfast')


def parse_rules_txt(path):
    lines = [l.strip() for l in open(path) if l.strip()]
    assert lines[0].startswith('SCALE ')
    scale_M = int(lines[0].split()[1])
    assert lines[1].startswith('PARTS ')
    nparts = int(lines[1].split()[1])
    assert len(lines) == 2 + nparts
    parts = []
    for idx in range(nparts):
        toks = lines[2 + idx].split()
        tag = toks[0]
        n = int(toks[1])
        w = int(toks[2])
        pos = 3
        subs = []
        for _ in range(n):
            sp = [int(toks[pos]), int(toks[pos + 1])]
            hat = [int(toks[pos + 2]), int(toks[pos + 3])]
            nf = int(toks[pos + 4])
            pos += 5
            fans = []
            for _ in range(nf):
                fans.append([int(toks[pos]), int(toks[pos + 1])])
                pos += 2
            subs.append([sp, hat, fans])
        assert pos == len(toks)
        parts.append({'tag': tag, 'hub': n, 'target': 2, 'weight': w, 'subs': subs})
    return scale_M, parts


def verify_external_super(c):
    """Run two independent reducibility engines (kc + dfast18 / cfast) on external config c."""
    sup_dir = os.path.join(DATA, 'e2_super')
    os.makedirs(sup_dir, exist_ok=True)
    nm = c['name']
    kcl = c['kc_line']
    infn = os.path.join(sup_dir, f'{nm}.in')
    outfn = os.path.join(sup_dir, f'{nm}.out')
    with open(infn, 'w') as f:
        f.write(kcl + '\n')

    if c['kind'] == 'D':
        r1 = subprocess.run(['nice', '-n', '15', KC_BIN, infn, '-t', '300'], capture_output=True, text=True, check=True)
        r2 = subprocess.run(['nice', '-n', '15', DF_BIN, infn], capture_output=True, text=True, check=True)
        assert 'D=true' in r1.stdout, (nm, r1.stdout)
        assert 'D=true' in r2.stdout, (nm, r2.stdout)
        with open(outfn, 'w') as f:
            f.write('== kc\n' + r1.stdout + '== dfast18\n' + r2.stdout)
        c['tier'] = 'E2'
        c['subtier'] = 'E2'
        c['evidence'] = f'Two-engine D=true verified in {outfn} (kc + dfast18)'
    elif c['kind'] == 'C':
        xstr = c['X']
        eqR, eqI, lbl = br.parse_x_and_labels(c['m'], c['ring'], xstr)
        assert br.lean_admissible_x(c, eqR, eqI, lbl), nm
        assert br.lean_fold_safe_x(c, eqR, eqI, lbl), nm
        r1 = subprocess.run(['nice', '-n', '15', KC_BIN, infn, '-t', '600', '-C2'], capture_output=True, text=True, check=True)
        r2 = subprocess.run(['nice', '-n', '15', CF_BIN, '--fixed', xstr, infn], capture_output=True, text=True, check=True)
        assert ('D=true' in r1.stdout) or ('C-REDUCIBLE' in r1.stdout), (nm, r1.stdout)
        assert 'C-REDUCIBLE, leftover bad classes extending after contraction = 0' in r2.stdout, (nm, r2.stdout)
        with open(outfn, 'w') as f:
            f.write('== kc_C2\n' + r1.stdout + '== cfast_fixed\n' + r2.stdout)
        c['tier'] = 'E2'
        c['subtier'] = 'E2'
        c['evidence'] = f'Two-engine C2cons verified in {outfn} (kc -C2 + cfast --fixed X={{{xstr}}}) + admissibleX/foldSafeX'
    else:
        raise ValueError(f'Unexpected external super kind: {c["kind"]}')


def main():
    rules_txt = os.path.join(DATA, 'synth_rules.txt')
    synth_act_fn = os.path.join(DATA, 'synth_active.txt')
    init_ids = {int(l.strip()) for l in open(synth_act_fn) if l.strip()}
    print(f'Loaded synth_active: {len(init_ids)} configs; running Exact Benders MILP over all 4,095 pool configs...')

    opt_ids, pool_meta = shs.run_benders(
        rules_txt=rules_txt,
        init_active_ids=init_ids,
        allow_external=True,
        k_thin=1,
        cap_per_cfg=500,
        tag='final_benders',
    )
    print(f'Benders MILP optimal set size: {len(opt_ids)} configs!')

    scale_M, parts = parse_rules_txt(rules_txt)

    # Prune any surgical mirror-pair batches (idx >= 71) that became redundant after Benders MILP swaps!
    if len(parts) > 71 and opt_ids != init_ids:
        opt_act_fn = os.path.join(DATA, 'final_benders_opt_active.txt')
        shs.write_ids(opt_act_fn, opt_ids)
        # Group surgical parts (idx >= 71) into minimal mirror pairs
        used = [False] * len(parts)
        groups = []
        for i in range(71, len(parts)):
            if used[i]:
                continue
            used[i] = True
            subs_i = tuple((tuple(s), tuple(h), tuple(tuple(x) for x in fs)) for s, h, fs in parts[i]['subs'])
            ms_i = tuple(br.mirror_part(list(subs_i)))
            if subs_i == ms_i:
                groups.append([i])
            else:
                partner = None
                for j in range(i + 1, len(parts)):
                    if not used[j] and parts[j]['weight'] == parts[i]['weight']:
                        subs_j = tuple((tuple(s), tuple(h), tuple(tuple(x) for x in fs)) for s, h, fs in parts[j]['subs'])
                        if subs_j == ms_i:
                            partner = j
                            break
                assert partner is not None, f'Missing mirror partner for {parts[i]["tag"]}'
                used[partner] = True
                groups.append([i, partner])

        drop_set = set()
        pruned_groups = 0
        # Test dropping from end to start
        for grp in reversed(groups):
            cand_drop = drop_set | set(grp)
            keep_parts = [p for idx_p, p in enumerate(parts) if idx_p not in cand_drop]
            tmp_rules = os.path.join(DATA, 'tmp_prune_rules.txt')
            tmp_sep = os.path.join(DATA, 'tmp_prune_sep.jsonl')
            with open(tmp_rules, 'w') as fr:
                fr.write(f'SCALE {scale_M}\nPARTS {len(keep_parts)}\n')
                for p in keep_parts:
                    toks = [p['tag'], str(p['hub']), str(p['weight'])]
                    for s, h, fs in p['subs']:
                        toks.extend([str(s[0]), str(s[1]), str(h[0]), str(h[1]), str(len(fs))])
                        for fr_r in fs:
                            toks.extend([str(fr_r[0]), str(fr_r[1])])
                    fr.write(' '.join(toks) + '\n')
            rc = subprocess.run(
                ['nice', '-n', '15', BIN_COMP, '--mode', 'sep', '--rules', tmp_rules,
                 '--active', opt_act_fn, '--out', tmp_sep, '--threads', '3'],
                capture_output=True, text=True
            ).returncode
            if rc == 0:
                drop_set = cand_drop
                pruned_groups += 1
        if drop_set:
            parts = [p for idx_p, p in enumerate(parts) if idx_p not in drop_set]
            print(f'  Pruned {len(drop_set)} redundant surgical parts ({pruned_groups} mirror groups) -> {len(parts)} parts remain!')

    # Verify mirror multiset closure on weighted parts
    orig_c = collections.Counter()
    mirr_c = collections.Counter()
    for p in parts:
        subs_t = tuple((tuple(s), tuple(h), tuple(tuple(x) for x in fs)) for s, h, fs in p['subs'])
        ms_t = tuple(br.mirror_part(list(subs_t)))
        orig_c[(subs_t, p['weight'])] += 1
        mirr_c[(ms_t, p['weight'])] += 1
    assert orig_c == mirr_c, 'Weighted mirror multiset closure failed!'

    # Assemble final compact registry (re-indexed 0 .. K-1)
    selected_orig_ids = sorted(opt_ids)
    final_cfgs = []
    for new_id, old_id in enumerate(selected_orig_ids):
        c = dict(pool_meta[old_id])
        if old_id >= 633:
            print(f'  Running two-engine [E2] verification on external super-killer {c["name"]} (old_id={old_id})...')
            verify_external_super(c)
        assert c['tier'] in ('L', 'E2'), c
        if c['kind'] == 'C':
            eqR, eqI, lbl = br.parse_x_and_labels(c['m'], c['ring'], c['X'])
            assert br.lean_admissible_x(c, eqR, eqI, lbl)
            assert br.lean_fold_safe_x(c, eqR, eqI, lbl)
        elif c['kind'] == 'C_merge':
            eqR, eqI, lbl = br.parse_x_and_labels(c['m'], c['ring'], c['X'])
            ok_nc, _ = bp.check_no_class_chord(c, eqR, eqI, lbl)
            assert ok_nc, c['name']
        c['pool_id'] = old_id
        c['id'] = new_id
        final_cfgs.append(c)

    with open(os.path.join(DATA, 'final_rules.json'), 'w') as f:
        json.dump({
            'scale_M': scale_M,
            'count': len(parts),
            'base_rsst_parts': 71,
            'surgical_cochain_parts': len(parts) - 71,
            'parts': [dict(idx=i, **p) for i, p in enumerate(parts)],
        }, f, indent=2)

    by_kind = collections.Counter(c['kind'] for c in final_cfgs)
    by_source = collections.Counter(c['source'] for c in final_cfgs)
    by_tier = collections.Counter(c['tier'] for c in final_cfgs)
    with open(os.path.join(DATA, 'final_registry.json'), 'w') as f:
        json.dump({
            'count': len(final_cfgs),
            'by_kind': dict(by_kind),
            'by_source': dict(by_source),
            'by_tier': dict(by_tier),
            'max_ring': max(c['ring'] for c in final_cfgs),
            'configs': final_cfgs,
        }, f, indent=2)

    # Write self-contained engine input containing ONLY the final K configurations and final rules,
    # then run `bin/fast_compress --mode cert` to emit final certificates!
    final_in = os.path.join(DATA, 'final_engine_input.txt')
    final_act = os.path.join(DATA, 'final_all_active.txt')
    with open(final_in, 'w') as f:
        f.write(f'SCALE {scale_M}\n')
        f.write(f'PARTS {len(parts)}\n')
        for p in parts:
            toks = [p['tag'], str(p['hub']), str(p['weight'])]
            for s, h, fs in p['subs']:
                toks.extend([str(s[0]), str(s[1]), str(h[0]), str(h[1]), str(len(fs))])
                for fr in fs:
                    toks.extend([str(fr[0]), str(fr[1])])
            f.write(' '.join(toks) + '\n')
        f.write(f'CONFIGS {len(final_cfgs)}\n')
        for c in final_cfgs:
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
    with open(final_act, 'w') as f:
        for i in range(len(final_cfgs)):
            f.write(f'{i}\n')

    certs_dir = os.path.join(DATA, 'certs')
    os.makedirs(certs_dir, exist_ok=True)
    for fn in os.listdir(certs_dir):
        if fn.startswith('cert_d') and fn.endswith('.jsonl'):
            os.remove(os.path.join(certs_dir, fn))
    subprocess.run([
        'nice', '-n', '15', BIN_COMP,
        '--pool', final_in,
        '--active', final_act,
        '--mode', 'cert',
        '--cert-dir', DATA,
        '--threads', '3',
    ], check=True)
    print(f'\n=== FINAL EXPORT COMPLETE: {len(final_cfgs)} CONFIGURATIONS, {len(parts)} PARTS (scale M={scale_M}) ===')
    print(f'  by_kind={dict(by_kind)}, by_source={dict(by_source)}, by_tier={dict(by_tier)}')


if __name__ == '__main__':
    main()
