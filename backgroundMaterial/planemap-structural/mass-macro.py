"""Exact finite mass-macro checks. Standard library only; not a uniform proof."""
import argparse, collections, hashlib, itertools, json, sys, time
from pathlib import Path

PAIRS = tuple(itertools.combinations(range(4), 2))
FORMULA = 'boundary-surplus/component-mass-v1'

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def canon(colouring):
    names = {}
    return tuple(names.setdefault(a, len(names)) for a in colouring)

def parse_rotation(line):
    n_text, code = line.split(' ', 1)
    n = int(n_text)
    rotation = [[ord(c) - 97 for c in row] for row in code.split(',')]
    assert len(rotation) == n
    for v, ns in enumerate(rotation):
        assert len(ns) >= 5 and len(set(ns)) == len(ns) and v not in ns
        assert all(0 <= w < n and v in rotation[w] for w in ns)
    assert sum(map(len, rotation)) == 6*n - 12
    reached = {0}; queue = [0]
    for v in queue:
        for w in rotation[v]:
            if w not in reached:
                reached.add(w); queue.append(w)
    assert len(reached) == n
    seen = set(); faces = 0
    for v, ns in enumerate(rotation):
        for w in ns:
            if (v, w) in seen:
                continue
            start = (v, w); dart = start; length = 0
            while dart not in seen:
                seen.add(dart); length += 1
                a, b = dart
                dart = (b, rotation[b][(rotation[b].index(a)+1) % len(rotation[b])])
            assert dart == start and length == 3
            faces += 1
    assert faces == 2*n - 4
    return rotation

def colourings(adjacency):
    """DSATUR ordering; new colour names introduced once, without losing orbits."""
    c = [-1]*len(adjacency); found = set()
    def go(max_colour, left):
        if left == 0:
            found.add(canon(c)); return
        v = max((v for v, a in enumerate(c) if a < 0), key=lambda v:
                (len({c[w] for w in adjacency[v] if c[w] >= 0}), len(adjacency[v]), -v))
        forbidden = {c[w] for w in adjacency[v]}
        for a in range(min(3, max_colour+1)+1):
            if a not in forbidden:
                c[v] = a; go(max(max_colour, a), left-1); c[v] = -1
    go(-1, len(adjacency))
    return sorted(found)

def state_data(c, adjacency, boundary, n):
    p = max(0, len({c[v] for v in boundary})-3)
    q = 0; moves = []
    for a, b in PAIRS:
        pending = {v for v, k in enumerate(c) if k in (a, b)}
        while pending:
            seed = min(pending); component = {seed}; queue = [seed]; pending.remove(seed)
            for v in queue:
                ns = adjacency[v] & pending
                pending -= ns; component |= ns; queue.extend(ns)
            if component & boundary:
                q += len(component - boundary)**2
            swapped = canon(b if k == a and v in component else
                            a if k == b and v in component else k for v, k in enumerate(c))
            moves.append(((a, b), tuple(sorted(component)), swapped))
    assert p in (0, 1) and 0 <= q <= 6*n*n
    return (p, q, (6*n*n+1)*p+q), moves

def check_root(rotation, root, expected=None):
    n = len(rotation); vertices = [v for v in range(n) if v != root]
    position = {v: i for i, v in enumerate(vertices)}
    adjacency = [{position[w] for w in rotation[v] if w != root} for v in vertices]
    boundary = {position[w] for w in rotation[root]}
    colours = colourings(adjacency)
    index = {c: i for i, c in enumerate(colours)}
    if expected is not None:
        assert len(colours) == expected['coloring_orbits']
    scores = []; successors = []
    for c in colours:
        assert all(c[v] != c[w] for v, ns in enumerate(adjacency) for w in ns)
        score, moves = state_data(c, adjacency, boundary, n)
        scores.append(score)
        successors.append({index[t] for _, _, t in moves})
    assert all(i in successors[j] for i, ns in enumerate(successors) for j in ns)
    best = [min(ns, key=lambda j: (scores[j][2], j)) for ns in successors]
    non_targets = [i for i, s in enumerate(scores) if s[0] == 1]
    one_bad = [i for i in non_targets if scores[best[i]][2] >= scores[i][2]]
    two_bad = [i for i in one_bad if not any(scores[best[j]][2] < scores[i][2]
                                           for j in successors[i])]
    result = dict(root=root, vertex_order=vertices, boundary_cyclic_order=rotation[root],
                  coloring_orbits=len(colours), non_target_orbits=len(non_targets),
                  one_swap_stuck_orbits=len(one_bad), two_swap_stuck_orbits=len(two_bad),
                  outcome='no_start_colorings' if not colours else
                  'fails' if two_bad else 'passes',
                  first_one_swap_stuck=None if not one_bad else
                  dict(coloring=colours[one_bad[0]], lex_rank=scores[one_bad[0]][:2],
                       rank=scores[one_bad[0]][2]))
    if two_bad:
        i = two_bad[0]; c = colours[i]
        score, first = state_data(c, adjacency, boundary, n)
        def encode(move):
            pair, component, t = move
            return dict(pair=pair, component=[vertices[v] for v in component],
                        successor_coloring=t, successor_rank=scores[index[t]][2],
                        successor_lex_rank=scores[index[t]][:2])
        layers = []
        for j in sorted(successors[i]):
            s, second = state_data(colours[j], adjacency, boundary, n)
            layers.append(dict(intermediate_coloring=colours[j], rank=s[2],
                               moves=[encode(move) for move in second]))
        result['failure_witness'] = dict(coloring=c, lex_rank=score[:2], rank=score[2],
            one_step_moves=[encode(move) for move in first], two_step_layers=layers,
            completeness='Every nonempty bichromatic component for each of six pairs is listed at the source and each distinct one-step successor. Global renaming is canonicalized; all pairs and component exchanges are preserved by renaming.')
        assert all(m['successor_rank'] >= score[2] for m in result['failure_witness']['one_step_moves'])
        assert all(m['successor_rank'] >= score[2] for layer in layers for m in layer['moves'])
    return result

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input-dir', type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument('--output', type=Path, default=Path(__file__).with_name('mass-macro-results.json'))
    parser.add_argument('--regression-only', action='store_true')
    args = parser.parse_args(); started = time.monotonic()
    baseline = json.loads((args.input_dir/'search-results.json').read_text())
    scope = ('Exact finite orbit enumeration of the specified one-/two-swap rank formula; '
             'not a uniform descent proof, efficient Select, Four Colour proof, or solver complexity theorem.')
    out = dict(scope=scope, status='running', formula_version=FORMULA, macro_bound=2,
               formula='R=(6n^2+1)*max(0,|colors(B)|-3)+sum_{six pairs,K intersect B nonempty}|K minus B|^2',
               checker_sha256=digest(Path(__file__)), python_version=sys.version,
               graph_index_convention='zero-based', ascii_hash_convention='UTF-8 exact graph line, excluding newline',
               input_hashes={'search-results.json': digest(args.input_dir/'search-results.json')},
               orders=[], existential_kill_witness=None)
    inputs = {}
    for order in baseline['orders']:
        n = order['order']; path = args.input_dir/f'triangulations-min5-{n}.txt'
        file_hash = digest(path); assert file_hash == order['input_sha256']
        out['input_hashes'][path.name] = file_hash
        lines = path.read_text().splitlines(); assert len(lines) == order['graphs']
        by = {g['graph_index']: g for g in order['graphs_checked']}
        assert set(by) == set(range(len(lines)))
        for i, line in enumerate(lines):
            assert by[i]['ascii'] == line
        inputs[n] = (lines, by)
    regressions = []
    for n, gi, roots in [(12, 0, None), (20, 36, [8])]:
        lines, by = inputs[n]; rotation = parse_rotation(lines[gi])
        roots = roots or [v for v, ns in enumerate(rotation) if len(ns) == 5]
        old = {r['root']: r for r in by[gi]['roots']}
        for r in roots:
            result = check_root(rotation, r, old[r])
            if n == 12:
                assert result['coloring_orbits'] == 20 and result['one_swap_stuck_orbits'] == 0
            else:
                assert result['coloring_orbits'] == 198 and result['non_target_orbits'] == 131
                assert result['one_swap_stuck_orbits'] == 3 and result['two_swap_stuck_orbits'] == 0
                assert result['first_one_swap_stuck']['lex_rank'] == (1, 190)
            regressions.append(dict(order=n, graph_index=gi, result=result))
    out['regressions'] = regressions
    print('Regression fixtures passed: all 12 icosahedron roots and graph36/root8.', flush=True)
    if args.regression_only:
        out['status'] = 'regressions_passed'
        args.output.write_text(json.dumps(out, indent=2)+'\n'); return
    for n, (lines, by) in inputs.items():
        rec = dict(order=n, graphs_available=len(lines), graphs_checked=[]); out['orders'].append(rec)
        for gi, line in enumerate(lines):
            rotation = parse_rotation(line); old = {r['root']: r for r in by[gi]['roots']}
            roots = [v for v, ns in enumerate(rotation) if len(ns) == 5]
            assert roots and set(roots) == set(old)
            results = [check_root(rotation, r, old[r]) for r in roots]
            passing = [r['root'] for r in results if r['outcome'] == 'passes']
            failing = [r['root'] for r in results if r['outcome'] == 'fails']
            graph = dict(graph_index=gi, ascii=line, ascii_sha256=hashlib.sha256(line.encode()).hexdigest(),
                         degree_five_roots=roots, passing_roots=passing, failing_roots=failing,
                         no_start_coloring_roots=[r['root'] for r in results if r['outcome']=='no_start_colorings'],
                         roots=results)
            rec['graphs_checked'].append(graph)
            if len(failing) == len(roots):
                out['existential_kill_witness'] = dict(order=n, graph_index=gi,
                    ascii_sha256=graph['ascii_sha256'], roots=failing)
                out['status'] = 'existential_counterexample_found'
            out['elapsed_seconds'] = time.monotonic()-started
            args.output.write_text(json.dumps(out, indent=2)+'\n')
            print(f'order {n}, graph {gi}/{len(lines)-1}: {len(passing)}/{len(roots)} roots pass; '
                  f'{sum(r["two_swap_stuck_orbits"] for r in results)} stuck orbits; '
                  f'{out["elapsed_seconds"]:.1f}s', flush=True)
            if out['existential_kill_witness']:
                return
    out['status'] = 'finite_corpus_completed'; out['completed_through_order'] = 20
    out['totals'] = dict(graphs=sum(len(o['graphs_checked']) for o in out['orders']),
        roots=sum(len(g['roots']) for o in out['orders'] for g in o['graphs_checked']),
        coloring_orbits=sum(r['coloring_orbits'] for o in out['orders'] for g in o['graphs_checked'] for r in g['roots']),
        failing_roots=sum(len(g['failing_roots']) for o in out['orders'] for g in o['graphs_checked']))
    assert out['totals']['graphs'] == 118 and out['totals']['roots'] == 1586 and out['totals']['coloring_orbits'] == 244051
    out['elapsed_seconds'] = time.monotonic()-started
    args.output.write_text(json.dumps(out, indent=2)+'\n')
    print(json.dumps(out['totals']), flush=True)

if __name__ == '__main__':
    main()
