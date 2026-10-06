#!/usr/bin/env python3
"""path3-local/test_math.py -- [exploratory] Local intel: test Math's path-3 builders and independent class checker.
(1) re-validate every builder instance with studiointel/graphs.py (orientation, Euler, min degree, separating triangles);
(2) gates G1 (icosahedron), G2 (FL(12) kT >= 2), G3 (RAK frozen -> kT >= 2 with a singleton class);
(3) checker vs engine: multiset of (class size, #filled) per hole must agree, on HoG 1152 (all 17 holes) and on builder instances.
Usage: python3 test_math.py BUILD_DIR OUT.jsonl"""
import sys, os, json, glob, importlib.util, time
from collections import Counter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *  # noqa

spec = importlib.util.spec_from_file_location('p3k', os.path.join(MATH, 'path3_kclasses.py')); p3k = importlib.util.module_from_spec(spec); spec.loader.exec_module(p3k)


def compare(F, info, holes, cap, out, tag):
    for v in holes:
        t = time.time(); e = kclasses(F, v)
        if 'classes' not in e: out.write(json.dumps({'tag': tag, 'v': v, 'engine': e}) + '\n'); continue
        try:
            c = p3k.analyse_hole(info, v, cap)
        except OverflowError:
            out.write(json.dumps({'tag': tag, 'v': v, 'checker': 'state cap'}) + '\n'); continue
        me = Counter((x[0], x[1]) for x in e['classes']); mc = Counter((x['size'], x['filled_states']) for x in c['classes'])
        row = {'tag': tag, 'v': v, 'agree': me == mc and e['n_states'] == c['H_states'], 'kH_engine': e['n_classes'], 'kH_checker': c['kH'],
               'H_states': [e['n_states'], c['H_states']], 'kT': c['kT'], 'T_states': c['T_states'], 'new_classes': c['new_classes'],
               'hit_iff_filled': c['consistency_hit_iff_filled'], 'classes_engine': sorted(me.items()),
               'O_vectors_per_class': [[x['size'], x['filled_states'], x['odd_parity_vectors']] for x in c['classes']], 'sec': round(time.time() - t, 2)}
        out.write(json.dumps(row) + '\n'); out.flush()
        print(tag, v, 'agree' if row['agree'] else 'DISAGREE', 'kH', e['n_classes'], c['kH'], 'kT', c['kT'], 'new', c['new_classes'], row['sec'], flush=True)


if __name__ == '__main__':
    bdir, outp = sys.argv[1], sys.argv[2]; out = open(outp, 'w')
    # (1) re-validation of builder output
    for jp in sorted(glob.glob(os.path.join(bdir, '*.json'))):
        info = json.load(open(jp)); F = [tuple(f) for f in info['faces_oriented']]
        ok, msg = graphs.check_triangulation(F); core, cmsg = core_ok(F)
        dg = graphs.degrees(F)
        agree = (min(dg.values()) == info['min_degree'] and graphs.n_separating_triangles(F) == info['separating_triangles']
                 and info['core_class_candidate'] == core) if ok else False
        out.write(json.dumps({'validate': info['name'], 'n': info['n'], 'triangulation': ok, 'core': core, 'why': cmsg, 'builder_agrees': agree}) + '\n')
        if not ok or not agree: print('VALIDATION', info['name'], ok, msg, agree)
    # (2)+(3) HoG 1152: every degree-5 hole
    hog = os.path.join(REPO, 'backgroundMaterial/planemap-structural/longtable/historical-traps/hog1152-heawood-four-color-graph.json')
    F = load_faces(hog); info = checker_json(F, 'HoG1152')
    compare(F, info, [x['v'] for x in info['deg5_orbit_reps']], 3000000, out, 'HoG1152')
    # gates and small builder instances (orbit reps; checker practical to ~10^6 states)
    names = ['FL_n5', 'CC_R1_tw0', 'RAK_a7_b1_s2', 'FL_n6', 'FL_n8', 'FL_n10', 'FL_n12', 'TU_n6_L3', 'TU_n7_L3', 'RAK_a11_b1_s2', 'RAK_a11_b1_s3',
             'RAK_a13_b1_s3', 'RAK_a13_b1_s2', 'TU_n6_L4', 'TU_n8_L3', 'CF_R2_E1', 'SL_rings8-9-9']
    for nm in names:
        p = os.path.join(bdir, nm + '.json')
        if not os.path.exists(p): continue
        info = json.load(open(p)); F = [tuple(f) for f in info['faces_oriented']]
        compare(F, info, [r['v'] for r in info['deg5_orbit_reps']], 3000000, out, nm)
