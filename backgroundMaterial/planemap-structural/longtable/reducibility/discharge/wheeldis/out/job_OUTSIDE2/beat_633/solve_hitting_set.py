#!/usr/bin/env python3
"""Exact Benders / Lazy-Constraint MILP Minimum Hitting Set & Forced-Leaf Profiler.

Uses HiGHS (`scipy.optimize.milp`) + exact C++ full-world separation (`bin/fast_compress`)
to find the provably minimum-cardinality unavoidable set over the 4,095-config pool U for any
given discharging rule file, and outputs per-configuration forced-leaf profiles for surgical
2-ball cochain synthesis.
"""
import collections
import json
import os
import subprocess
import sys
import time
import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import csc_matrix

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, 'data')
BIN = os.path.join(HERE, 'bin', 'fast_compress')


def write_ids(path, ids):
    with open(path, 'w') as f:
        for x in sorted(ids):
            f.write(f'{x}\n')


def load_hyperedges(jsonl_path):
    edges = set()
    leaves = []
    if not os.path.exists(jsonl_path):
        return edges, leaves
    with open(jsonl_path) as f:
        for line in f:
            if not line.strip():
                continue
            obj = json.loads(line)
            ku = tuple(sorted(set(obj['kU'])))
            assert len(ku) > 0, f'Uncoverable leaf even in full 4095-pool U: {obj}'
            edges.add(ku)
            leaves.append(obj)
    return edges, leaves


def solve_milp_hitting_set(num_cfgs, pool_meta, hyperedges, allow_external=True):
    costs = np.ones(num_cfgs, dtype=float)
    ub_vec = np.ones(num_cfgs, dtype=float)
    for i, c in enumerate(pool_meta):
        if i < 633:
            # Prefer [L] -> [E2] D/C2cons -> [E2] C_merge among equal-cardinality solutions
            if c['tier'] == 'L':
                costs[i] = 1.00000
            elif c['kind'] != 'C_merge':
                costs[i] = 1.00002
            else:
                costs[i] = 1.00005
        else:
            # External super-killer: cost 1.002 so it is ONLY picked when replacing >= 2 RSST configs!
            costs[i] = 1.00200
            if not allow_external:
                ub_vec[i] = 0.0

    edge_list = sorted(hyperedges)
    if not edge_list:
        return set()
    rows, cols, vals = [], [], []
    for r_idx, ku in enumerate(edge_list):
        for cid in ku:
            rows.append(r_idx)
            cols.append(cid)
            vals.append(1.0)
    A = csc_matrix((vals, (rows, cols)), shape=(len(edge_list), num_cfgs))
    lb = np.ones(len(edge_list), dtype=float)
    ub = np.full(len(edge_list), np.inf, dtype=float)
    integrality = np.ones(num_cfgs, dtype=int)

    res = milp(
        c=costs,
        integrality=integrality,
        bounds=Bounds(np.zeros(num_cfgs), ub_vec),
        constraints=LinearConstraint(A, lb, ub),
        options={'mip_rel_gap': 0.0, 'presolve': True},
    )
    assert res.success, f'MILP failed: {res.message}'
    picked = {i for i, val in enumerate(res.x) if val > 0.5}
    return picked


def run_benders(rules_txt=None, init_active_ids=None, allow_external=True, k_thin=1, cap_per_cfg=400, tag='stage1'):
    pool_raw = json.load(open(os.path.join(DATA, 'pool_configs.json')))
    pool_meta = pool_raw['configs']
    num_cfgs = len(pool_meta)
    if init_active_ids is None:
        init_active_ids = set(range(633))

    act_fn = os.path.join(DATA, f'{tag}_active.txt')
    prof_fn = os.path.join(DATA, f'{tag}_profile.jsonl')
    write_ids(act_fn, init_active_ids)

    cmd = ['nice', '-n', '15', BIN, '--mode', 'profile', '--k-thin', str(k_thin),
           '--cap-per-cfg', str(cap_per_cfg),
           '--active', act_fn, '--out', prof_fn, '--threads', '3']
    if rules_txt:
        cmd.extend(['--rules', rules_txt])
    print(f'\n[{tag}] Running thin-leaf profile (k_thin={k_thin}, init_active={len(init_active_ids)})...')
    subprocess.run(cmd, check=False)

    hyperedges, init_leaves = load_hyperedges(prof_fn)
    print(f'[{tag}] Initial hyperedges: {len(hyperedges)} (from {len(init_leaves)} thin/violated leaves)')

    it = 0
    while True:
        it += 1
        t0 = time.time()
        cand = solve_milp_hitting_set(num_cfgs, pool_meta, hyperedges, allow_external=allow_external)
        n_rsst = sum(1 for i in cand if i < 633)
        n_ext = sum(1 for i in cand if i >= 633)
        print(f'[{tag}] MILP iter {it}: |S| = {len(cand)} (RSST={n_rsst}, EXT_SUPER={n_ext}) in {time.time()-t0:.2f}s')

        cand_fn = os.path.join(DATA, f'{tag}_cand.txt')
        sep_fn = os.path.join(DATA, f'{tag}_sep.jsonl')
        write_ids(cand_fn, cand)
        scmd = ['nice', '-n', '15', BIN, '--mode', 'sep', '--active', cand_fn, '--out', sep_fn, '--threads', '3']
        if rules_txt:
            scmd.extend(['--rules', rules_txt])
        rc = subprocess.run(scmd).returncode
        if rc == 0:
            print(f'[{tag}] CERTIFIED 0 VIOLATIONS across ALL degrees! Optimal |S*| = {len(cand)}!')
            out_opt = os.path.join(DATA, f'{tag}_opt_active.txt')
            write_ids(out_opt, cand)
            return cand, pool_meta

        new_edges, new_leaves = load_hyperedges(sep_fn)
        before = len(hyperedges)
        hyperedges.update(new_edges)
        print(f'[{tag}] Added {len(hyperedges) - before} new violated-leaf cuts (total={len(hyperedges)}) from {len(new_leaves)} leaves.')
        assert len(hyperedges) > before, 'No new hyperedges added despite violation!'


if __name__ == '__main__':
    allow_ext = '--no-ext' not in sys.argv
    rules_arg = None
    tag_arg = 'stage1_ext' if allow_ext else 'stage1_rsst_only'
    for i, a in enumerate(sys.argv[1:]):
        if a == '--rules':
            rules_arg = sys.argv[i + 2]
        elif a == '--tag':
            tag_arg = sys.argv[i + 2]
    run_benders(rules_txt=rules_arg, allow_external=allow_ext, k_thin=1, cap_per_cfg=400, tag=tag_arg)
