"""Fans on the icosahedron: colourings of T* and the length to a 3-colour link.

T is the regular icosahedron from inquiry_slide.icosahedron. For one vertex v the
link is an induced 5-cycle, so each of the five non-crossing fans is absent.
T* is T - v plus that fan. Proper 4-colourings of T* are taken up to colour
permutation (first-occurrence form). Forgetting the two chords leaves a proper
4-colouring of T - v.

A move is one Kempe swap in the current deletion of T, or one singleton vacancy
slide. Length is the number of moves in a shortest sequence whose current link
uses at most three colours. The search cap is 20. This does not colour the
pentakis dodecahedron or the frequency-2 icosahedron.
"""

from __future__ import annotations

import json
import sys
from collections import Counter, deque
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from inquiry_slide import faces_of, icosahedron
from mass_core import (
    FIXTURES,
    RootState,
    deletion_colourings,
    rotation_from_fixture,
    validate_triangulation,
)

CAP = 20
HERE = Path(__file__).resolve().parent
COLOURS = (0, 1, 2, 3)


def validate_sphere(rot: list[list[int]], min_degree: int = 3) -> None:
    """Simple spherical triangulation, minimum degree relaxed below 5."""
    n = len(rot)
    for vertex, nbrs in enumerate(rot):
        if len(set(nbrs)) != len(nbrs) or vertex in nbrs or len(nbrs) < min_degree:
            raise AssertionError(vertex)
        if any(vertex not in rot[other] for other in nbrs):
            raise AssertionError(vertex)
    edges = sum(len(nbrs) for nbrs in rot) // 2
    if edges != 3 * n - 6:
        raise AssertionError(edges)
    seen: set[tuple[int, int]] = set()
    faces = 0
    for vertex, nbrs in enumerate(rot):
        for other in nbrs:
            if (vertex, other) in seen:
                continue
            dart = (vertex, other)
            length = 0
            while dart not in seen:
                seen.add(dart)
                length += 1
                if length > n:
                    raise AssertionError(dart)
                left, right = dart
                dart = (right, rot[right][(rot[right].index(left) + 1) % len(rot[right])])
            if length != 3 or dart != (vertex, other):
                raise AssertionError((vertex, other, length))
            faces += 1
    if n - edges + faces != 2 or len(seen) != 2 * edges:
        raise AssertionError((n, edges, faces, len(seen)))


def induced_cycle(rot: list[list[int]], link: list[int]) -> bool:
    members = set(link)
    cycle = {frozenset((link[i], link[(i + 1) % len(link)])) for i in range(len(link))}
    for vertex in link:
        inside = [other for other in rot[vertex] if other in members]
        if len(inside) != 2:
            return False
        if any(frozenset((vertex, other)) not in cycle for other in inside):
            return False
    return True


def compact(rot_map: dict[int, list[int]], vertices: list[int]) -> list[list[int]]:
    index = {vertex: i for i, vertex in enumerate(vertices)}
    return [[index[other] for other in rot_map[vertex]] for vertex in vertices]


def rotation_from_triangles(
    triangles: list[tuple[int, int, int]], vertices: list[int]
) -> dict[int, list[int]]:
    succ: dict[int, dict[int, int]] = {vertex: {} for vertex in vertices}
    for x, y, z in triangles:
        # Face (x, y, z) uses darts (x,y)->(y,z), (y,z)->(z,x), (z,x)->(x,y).
        for pred, mid, nxt in ((x, y, z), (y, z, x), (z, x, y)):
            previous = succ[mid].get(pred)
            if previous is not None and previous != nxt:
                raise RuntimeError(f"orientation conflict at {mid}: {pred} -> {previous} and {nxt}")
            succ[mid][pred] = nxt
    rot: dict[int, list[int]] = {}
    for vertex in vertices:
        if len(succ[vertex]) < 3:
            raise RuntimeError(f"degree {len(succ[vertex])} at {vertex}")
        start = min(succ[vertex])
        cycle = []
        cursor = start
        while True:
            cycle.append(cursor)
            cursor = succ[vertex][cursor]
            if cursor == start:
                break
            if len(cycle) > len(succ[vertex]):
                raise RuntimeError(f"rotation did not close at {vertex}")
        if len(cycle) != len(succ[vertex]):
            raise RuntimeError(f"rotation missed a neighbour at {vertex}")
        rot[vertex] = cycle
    return rot


def fan_triangles(link: list[int], apex_index: int) -> tuple[list[tuple[int, int, int]], tuple[int, int], tuple[int, int]]:
    """The fan τ_i = {i(i+2), i(i+3)} and its three triangles, oriented with the link."""
    apex = link[apex_index]
    nxt = link[(apex_index + 1) % 5]
    far = link[(apex_index + 2) % 5]
    near = link[(apex_index + 3) % 5]
    prev = link[(apex_index + 4) % 5]
    triangles = [(apex, nxt, far), (apex, far, near), (apex, near, prev)]
    return triangles, (apex, far), (apex, near)


def build_star(rot: list[list[int]], vertex: int, apex_index: int) -> dict:
    link = list(rot[vertex])
    added, chord_far, chord_near = fan_triangles(link, apex_index)
    if not induced_cycle(rot, link):
        raise AssertionError("link is not an induced 5-cycle")
    edges = {frozenset((a, b)) for a, nbrs in enumerate(rot) for b in nbrs}
    if frozenset(chord_far) in edges or frozenset(chord_near) in edges:
        raise AssertionError("fan chord already present")
    kept = [tuple(face) for face in faces_of(rot) if vertex not in face]
    vertices = [other for other in range(len(rot)) if other != vertex]
    try:
        rot_map = rotation_from_triangles(kept + added, vertices)
    except RuntimeError:
        flipped = [(c, b, a) for a, b, c in added]
        rot_map = rotation_from_triangles(kept + flipped, vertices)
    packed = compact(rot_map, vertices)
    validate_sphere(packed, min_degree=3)
    degrees = sorted(len(nbrs) for nbrs in packed)
    return {
        "link": link,
        "chords": [list(chord_far), list(chord_near)],
        "rot_map": rot_map,
        "vertices": vertices,
        "degrees": degrees,
        "edges": sum(degrees) // 2,
    }


def colourings_of(rot_map: dict[int, list[int]], vertices: list[int]) -> list[tuple[int, ...]]:
    """Proper 4-colourings up to colour permutation, vertices in increasing label order."""
    ordered = sorted(vertices)
    index = {vertex: i for i, vertex in enumerate(ordered)}
    earlier = [
        [index[other] for other in rot_map[vertex] if index[other] < i]
        for i, vertex in enumerate(ordered)
    ]
    found: list[tuple[int, ...]] = []
    current = [0] * len(ordered)

    def walk(position: int, top: int) -> None:
        if position == len(ordered):
            found.append(tuple(current))
            return
        blocked = {current[slot] for slot in earlier[position]}
        for colour in range(min(3, top + 1) + 1):
            if colour not in blocked:
                current[position] = colour
                walk(position + 1, max(top, colour))

    walk(0, -1)
    return found


def labelled_count(rot_map: dict[int, list[int]], vertices: list[int]) -> int:
    """Proper 4-colourings with colours drawn from {0,1,2,3}, no quotient."""
    ordered = sorted(vertices)
    index = {vertex: i for i, vertex in enumerate(ordered)}
    earlier = [
        [index[other] for other in rot_map[vertex] if index[other] < i]
        for i, vertex in enumerate(ordered)
    ]
    current = [0] * len(ordered)
    total = 0

    def walk(position: int) -> None:
        nonlocal total
        if position == len(ordered):
            total += 1
            return
        blocked = {current[slot] for slot in earlier[position]}
        for colour in COLOURS:
            if colour not in blocked:
                current[position] = colour
                walk(position + 1)

    walk(0)
    return total


def full_colouring(order: int, hole: int, vertices: list[int], colours: tuple[int, ...]) -> list[int]:
    full = [-1] * order
    ordered = sorted(vertices)
    for slot, vertex in enumerate(ordered):
        full[vertex] = colours[slot]
    if full[hole] != -1:
        raise RuntimeError("hole received a colour")
    return full


def canon_full(colours: list[int], hole: int) -> tuple[int, ...]:
    seen: dict[int, int] = {}
    out = []
    for vertex, colour in enumerate(colours):
        if vertex == hole:
            out.append(-1)
            continue
        out.append(seen.setdefault(colour, len(seen)))
    return tuple(out)


def deletion_tuple(full: tuple[int, ...] | list[int], hole: int) -> tuple[int, ...]:
    return tuple(colour for vertex, colour in enumerate(full) if vertex != hole)


def link_pattern(link: list[int], full: list[int], apex_index: int) -> tuple[int, ...]:
    """Colours from the fan apex, renamed by first occurrence along the link."""
    seen: dict[int, int] = {}
    out = []
    for step in range(5):
        colour = full[link[(apex_index + step) % 5]]
        out.append(seen.setdefault(colour, len(seen)))
    return tuple(out)


def is_proper(rot: list[list[int]], colours: list[int], hole: int) -> bool:
    for vertex, nbrs in enumerate(rot):
        if vertex == hole:
            continue
        for other in nbrs:
            if other == hole:
                continue
            if colours[vertex] == colours[other]:
                return False
    return True


def link_size(rot: list[list[int]], hole: int, colours: list[int] | tuple[int, ...]) -> int:
    return len({colours[other] for other in rot[hole]})


def kempe_images(
    rot: list[list[int]], hole: int, colours: list[int]
) -> list[tuple[tuple[int, int], tuple[int, ...], tuple[int, ...]]]:
    """One swap of one bichromatic component. Images are canonical at the same hole."""
    order = len(rot)
    images = []
    present = sorted({colours[vertex] for vertex in range(order) if vertex != hole})
    for first_index, first in enumerate(present):
        for second in present[first_index + 1 :]:
            remaining = {
                vertex
                for vertex in range(order)
                if vertex != hole and colours[vertex] in (first, second)
            }
            while remaining:
                seed = min(remaining)
                stack = [seed]
                component: set[int] = set()
                while stack:
                    vertex = stack.pop()
                    if vertex in component:
                        continue
                    component.add(vertex)
                    for other in rot[vertex]:
                        if other in remaining and other not in component:
                            stack.append(other)
                remaining -= component
                swapped = colours[:]
                for vertex in component:
                    swapped[vertex] = second if colours[vertex] == first else first
                canonical = canon_full(swapped, hole)
                images.append(((first, second), tuple(sorted(component)), canonical))
    return images


def slide_images(
    rot: list[list[int]], hole: int, colours: list[int]
) -> list[tuple[int, tuple[int, ...]]]:
    """Singleton slides. Each image is (new hole, canonical colouring)."""
    counts = Counter(colours[other] for other in rot[hole])
    images = []
    for other in rot[hole]:
        if counts[colours[other]] != 1:
            continue
        moved = colours[:]
        moved[hole] = colours[other]
        moved[other] = -1
        images.append((other, canon_full(moved, other)))
    return images


def build_move_graph(rot: list[list[int]]) -> dict:
    """Every deletion colouring at every vertex, with swap and slide successors."""
    order = len(rot)
    full_of: dict[tuple[int, tuple[int, ...]], tuple[int, ...]] = {}
    for hole in range(order):
        _vertices, orbits = deletion_colourings(rot, hole)
        for orbit in orbits:
            colours = [-1] * order
            slot = 0
            for vertex in range(order):
                if vertex == hole:
                    continue
                colours[vertex] = orbit[slot]
                slot += 1
            canonical = canon_full(colours, hole)
            if deletion_tuple(canonical, hole) != orbit:
                raise AssertionError("canonical form drifted from deletion_colourings")
            full_of[(hole, orbit)] = canonical
    swap_adj: dict[tuple[int, tuple[int, ...]], list[tuple[int, tuple[int, ...]]]] = {}
    slide_adj: dict[tuple[int, tuple[int, ...]], list[tuple[int, tuple[int, ...]]]] = {}
    for key, canonical in full_of.items():
        hole = key[0]
        colours = list(canonical)
        swaps = []
        for _pair, _component, image in kempe_images(rot, hole, colours):
            image_key = (hole, deletion_tuple(image, hole))
            if image_key not in full_of:
                raise AssertionError("swap left the deletion orbits")
            if image_key != key:
                swaps.append(image_key)
        slides = []
        for new_hole, image in slide_images(rot, hole, colours):
            image_key = (new_hole, deletion_tuple(image, new_hole))
            if image_key not in full_of:
                raise AssertionError("slide left the deletion orbits")
            slides.append(image_key)
        swap_adj[key] = swaps
        slide_adj[key] = slides
    return {"full": full_of, "swap": swap_adj, "slide": slide_adj}


def mixed_neighbors(graph: dict, state: tuple[int, tuple[int, ...]]) -> list[tuple[str, tuple[int, tuple[int, ...]]]]:
    moves = [("swap", item) for item in graph["swap"][state]]
    moves.extend(("slide", item) for item in graph["slide"][state])
    return moves


def reverse_distance(graph: dict, targets: set[tuple[int, tuple[int, ...]]], kind: str, cap: int) -> dict:
    """Shortest-path distance toward a target, following swap, slide, or both."""
    incoming: dict[tuple[int, tuple[int, ...]], list[tuple[int, tuple[int, ...]]]] = {key: [] for key in graph["full"]}
    for state in graph["full"]:
        if kind in ("swap", "both"):
            for nxt in graph["swap"][state]:
                incoming[nxt].append(state)
        if kind in ("slide", "both"):
            for nxt in graph["slide"][state]:
                incoming[nxt].append(state)
    dist = {state: 0 for state in targets}
    queue = deque(targets)
    while queue:
        state = queue.popleft()
        if dist[state] >= cap:
            continue
        for prev in incoming[state]:
            if prev not in dist:
                dist[prev] = dist[state] + 1
                queue.append(prev)
    return dist


def mixed_distance(
    graph: dict,
    start: tuple[int, tuple[int, ...]],
    targets: set[tuple[int, tuple[int, ...]]],
    cap: int,
) -> tuple[int | None, list[str]]:
    """Shortest swap/slide sequence, and the move kinds along one such sequence."""
    if start in targets:
        return 0, []
    parent: dict[tuple[int, tuple[int, ...]], tuple[tuple[int, tuple[int, ...]], str]] = {}
    queue = deque([(start, 0)])
    seen = {start}
    found = None
    while queue:
        state, depth = queue.popleft()
        if depth >= cap:
            continue
        for kind, nxt in mixed_neighbors(graph, state):
            if nxt in seen:
                continue
            parent[nxt] = (state, kind)
            seen.add(nxt)
            if nxt in targets:
                found = nxt
                queue.clear()
                break
            queue.append((nxt, depth + 1))
    if found is None:
        return None, []
    kinds = path_kinds(parent, found)
    return len(kinds), kinds


def path_kinds(
    parent: dict[tuple[int, tuple[int, ...]], tuple[tuple[int, tuple[int, ...]], str]],
    end: tuple[int, tuple[int, ...]],
) -> list[str]:
    kinds = []
    cursor = end
    while cursor in parent:
        cursor, kind = parent[cursor]
        kinds.append(kind)
    kinds.reverse()
    return kinds


def graph_isomorphic(left: list[list[int]], right: list[list[int]]) -> bool:
    """Exact graph isomorphism. Both arguments are 12-vertex degree-5 triangulations."""
    if len(left) != len(right):
        return False
    n = len(left)
    adj_l = [set(nbrs) for nbrs in left]
    adj_r = [set(nbrs) for nbrs in right]
    order = []
    seen = {0}
    stack = [0]
    while stack:
        vertex = stack.pop()
        order.append(vertex)
        for other in left[vertex]:
            if other not in seen:
                seen.add(other)
                stack.append(other)
    if len(order) != n:
        return False

    def search(image_of_zero: int) -> bool:
        mapping = [-1] * n
        used = [False] * n
        mapping[0] = image_of_zero
        used[image_of_zero] = True

        def place(position: int) -> bool:
            if position == n:
                return True
            vertex = order[position]
            if vertex == 0:
                return place(position + 1)
            for image in range(n):
                if used[image] or len(adj_r[image]) != len(adj_l[vertex]):
                    continue
                if any(
                    mapping[other] != -1 and mapping[other] not in adj_r[image]
                    for other in adj_l[vertex]
                ):
                    continue
                if any(
                    mapping[other] != -1 and (other in adj_l[vertex]) != (mapping[other] in adj_r[image])
                    for other in range(n)
                ):
                    continue
                mapping[vertex] = image
                used[image] = True
                if place(position + 1):
                    return True
                mapping[vertex] = -1
                used[image] = False
            return False

        return place(0)

    return any(search(image) for image in range(n))


def vertex_transitive(rot: list[list[int]]) -> bool:
    """The rotation graph admits an automorphism sending vertex 0 to every vertex."""
    n = len(rot)
    adj = [set(nbrs) for nbrs in rot]
    order = []
    seen = {0}
    stack = [0]
    while stack:
        vertex = stack.pop()
        order.append(vertex)
        for other in rot[vertex]:
            if other not in seen:
                seen.add(other)
                stack.append(other)

    def sends_zero_to(image_of_zero: int) -> bool:
        mapping = [-1] * n
        used = [False] * n
        mapping[0] = image_of_zero
        used[image_of_zero] = True

        def place(position: int) -> bool:
            if position == n:
                return True
            vertex = order[position]
            if vertex == 0:
                return place(position + 1)
            for image in range(n):
                if used[image]:
                    continue
                good = True
                for other in range(n):
                    mapped = mapping[other]
                    if mapped == -1:
                        continue
                    if (other in adj[vertex]) != (mapped in adj[image]):
                        good = False
                        break
                if not good:
                    continue
                mapping[vertex] = image
                used[image] = True
                if place(position + 1):
                    return True
                mapping[vertex] = -1
                used[image] = False
            return False

        return place(0)

    return all(sends_zero_to(image) for image in range(n))


def analyse_fan(
    rot: list[list[int]],
    vertex: int,
    apex_index: int,
    state: RootState,
    graph: dict,
    targets: set[tuple[int, tuple[int, ...]]],
    mixed_dist: dict,
    slide_dist: dict,
    with_paths: bool,
) -> dict:
    star = build_star(rot, vertex, apex_index)
    orbits = colourings_of(star["rot_map"], star["vertices"])
    labelled = labelled_count(star["rot_map"], star["vertices"])
    if labelled != 24 * len(orbits):
        raise AssertionError((labelled, len(orbits)))
    rows = []
    for orbit in orbits:
        full = full_colouring(len(rot), vertex, star["vertices"], orbit)
        if not is_proper(rot, full, vertex):
            raise AssertionError("restriction is not proper on T - v")
        canonical = canon_full(full, vertex)
        key = (vertex, deletion_tuple(canonical, vertex))
        if key not in graph["full"]:
            raise AssertionError("restriction is not a deletion orbit")
        if state.index[key[1]] != state.C.index(key[1]):
            raise AssertionError("orbit missing from RootState")
        info = state.info[state.index[key[1]]]
        pattern = link_pattern(star["link"], list(canonical), apex_index)
        link_colours = [canonical[other] for other in star["link"]]
        one_swap = info["p"] == 0 or any(state.info[target]["p"] == 0 for _pair, _comp, target in info["moves"])
        one_slide = key in targets or any(nxt in targets for nxt in graph["slide"][key])
        if key in targets:
            swap_slide = 0
        else:
            reached = [
                1 + slide_dist[nxt]
                for nxt in graph["swap"][key]
                if nxt in slide_dist and 1 + slide_dist[nxt] <= CAP
            ]
            swap_slide = min(reached) if reached else None
        mixed = 0 if key in targets else mixed_dist.get(key)
        if mixed is not None and mixed > CAP:
            mixed = None
        slide_chain = 0 if key in targets else slide_dist.get(key)
        if slide_chain is not None and slide_chain > CAP:
            slide_chain = None
        kinds: list[str] = []
        if with_paths and mixed not in (None, 0):
            mixed_again, kinds = mixed_distance(graph, key, targets, CAP)
            if mixed_again != mixed:
                raise AssertionError((mixed_again, mixed, pattern))
        if info["p"] == 0 and mixed != 0:
            raise AssertionError(pattern)
        if info["p"] == 1 and one_swap and mixed not in (0, 1):
            raise AssertionError((mixed, pattern))
        rows.append(
            {
                "orbit": list(key[1]),
                "pattern": list(pattern),
                "link_colours": link_colours,
                "colours_on_link": len(set(link_colours)),
                "colours_used": len(set(key[1])),
                "p": info["p"],
                "one_swap": one_swap,
                "one_slide": one_slide,
                "swap_then_slides": swap_slide,
                "slide_chain": slide_chain,
                "mixed": mixed,
                "mixed_kinds": kinds,
            }
        )
    by_pattern: dict[str, dict] = {}
    for row in rows:
        name = "".join(str(value) for value in row["pattern"])
        bucket = by_pattern.setdefault(
            name,
            {
                "pattern": row["pattern"],
                "orbits": 0,
                "mixed": [],
                "one_slide": 0,
                "slide_chain": [],
                "swap_then_slides": [],
            },
        )
        bucket["orbits"] += 1
        bucket["mixed"].append(row["mixed"])
        bucket["one_slide"] += int(row["one_slide"])
        bucket["slide_chain"].append(row["slide_chain"])
        bucket["swap_then_slides"].append(row["swap_then_slides"])
    distances = [row["mixed"] for row in rows]
    worst = None if any(item is None for item in distances) else max(distances)
    return {
        "apex_index": apex_index,
        "apex": star["link"][apex_index],
        "chords": star["chords"],
        "degrees": star["degrees"],
        "edges": star["edges"],
        "orbits": len(orbits),
        "labelled": labelled,
        "link3": sum(1 for row in rows if row["colours_on_link"] <= 3),
        "link4": sum(1 for row in rows if row["colours_on_link"] == 4),
        "worst": worst,
        "unreachable": sum(1 for item in distances if item is None),
        "patterns": by_pattern,
        "rows": rows,
    }


def witness_swap(rot: list[list[int]], state: RootState, orbit: tuple[int, ...]) -> dict:
    """Smallest bichromatic component whose swap makes the link use at most three colours.

    Link colours after the swap are written in the original colour names, before
    the first-occurrence renaming of the image orbit.
    """
    index = state.index[orbit]
    link = list(rot[state.r])
    full = list(graph_full(state, index))
    hits = []
    for pair, component, target in state.info[index]["moves"]:
        if state.info[target]["p"] != 0:
            continue
        raw = full[:]
        first, second = pair
        for vertex in component:
            if full[vertex] == first:
                raw[vertex] = second
            elif full[vertex] == second:
                raw[vertex] = first
        after = [raw[vertex] for vertex in link]
        if len(set(after)) > 3:
            raise AssertionError((pair, component, after))
        hits.append((len(component), pair, component, after))
    hits.sort()
    _size, pair, component, after = hits[0]
    missing = sorted(set(range(4)) - set(after))
    return {
        "pair": list(pair),
        "component": list(component),
        "link_before": [full[vertex] for vertex in link],
        "link_after": after,
        "missing_colour": missing,
    }


def graph_full(state: RootState, index: int) -> tuple[int, ...]:
    colours = [-1] * state.n
    for slot, vertex in enumerate(state.V):
        colours[vertex] = state.C[index][slot]
    return tuple(colours)


def slide_landings(rot: list[list[int]], hole: int, colours: list[int]) -> list[dict]:
    counts = Counter(colours[other] for other in rot[hole])
    landings = []
    for other in rot[hole]:
        if counts[colours[other]] != 1:
            continue
        moved = colours[:]
        moved[hole] = colours[other]
        moved[other] = -1
        landings.append(
            {
                "to": other,
                "colour": colours[other],
                "link_colours": [moved[vertex] for vertex in rot[other]],
                "colours_on_link": link_size(rot, other, moved),
            }
        )
    return landings


def pick_witness(fan: dict, distance: int) -> dict:
    rows = [row for row in fan["rows"] if row["mixed"] == distance]
    rows.sort(key=lambda row: (row["pattern"], row["orbit"]))
    return rows[0]


def summarise_vertex(
    rot: list[list[int]],
    vertex: int,
    graph: dict,
    targets: set[tuple[int, tuple[int, ...]]],
    mixed_dist: dict,
    slide_dist: dict,
    with_paths: bool,
) -> dict:
    state = RootState(rot, vertex)
    state.check_closure()
    if len(state.C) != 20:
        raise AssertionError(len(state.C))
    kempe_distance = state.target_distance_max()
    fans = [
        analyse_fan(
            rot, vertex, apex, state, graph, targets, mixed_dist, slide_dist, with_paths
        )
        for apex in range(5)
    ]
    orbit_counts = [fan["orbits"] for fan in fans]
    worsts = [fan["worst"] for fan in fans]
    if len(set(orbit_counts)) != 1 or len(set(map(tuple, (tuple(sorted(fan["patterns"])) for fan in fans)))) != 1:
        raise AssertionError("fans of one vertex disagreed")
    if len(set(worsts)) != 1:
        raise AssertionError(worsts)
    # Pattern multisets, not just names.
    signatures = []
    for fan in fans:
        signatures.append(
            tuple(sorted((name, bucket["orbits"]) for name, bucket in fan["patterns"].items()))
        )
    if len(set(signatures)) != 1:
        raise AssertionError(signatures)
    return {
        "vertex": vertex,
        "link": list(rot[vertex]),
        "deletion_orbits": len(state.C),
        "kempe_distance_all_orbits": kempe_distance,
        "non_target": sum(1 for info in state.info if info["p"] == 1),
        "fans": fans,
        "state": state,
    }


def json_ready(summary: dict) -> dict:
    """Drop RootState and per-orbit rows; keep one witness of each length."""
    vertex = summary["vertex"]
    fans_out = []
    for fan in summary["fans"]:
        patterns = []
        for name in sorted(fan["patterns"]):
            bucket = fan["patterns"][name]
            patterns.append(
                {
                    "pattern": bucket["pattern"],
                    "orbits": bucket["orbits"],
                    "mixed_min": min(item for item in bucket["mixed"] if item is not None),
                    "mixed_max": max(item for item in bucket["mixed"] if item is not None),
                    "one_slide": bucket["one_slide"],
                    "slide_chain_max": max(
                        (-1 if item is None else item) for item in bucket["slide_chain"]
                    ),
                    "swap_then_slides_max": (
                        None
                        if all(item is None for item in bucket["swap_then_slides"])
                        else max(item for item in bucket["swap_then_slides"] if item is not None)
                    ),
                }
            )
        fans_out.append(
            {
                "apex_index": fan["apex_index"],
                "apex": fan["apex"],
                "chords": fan["chords"],
                "degrees": fan["degrees"],
                "edges": fan["edges"],
                "orbits": fan["orbits"],
                "labelled": fan["labelled"],
                "link3": fan["link3"],
                "link4": fan["link4"],
                "worst": fan["worst"],
                "unreachable": fan["unreachable"],
                "patterns": patterns,
            }
        )
    return {
        "vertex": vertex,
        "link": summary["link"],
        "deletion_orbits": summary["deletion_orbits"],
        "kempe_distance_all_orbits": summary["kempe_distance_all_orbits"],
        "non_target": summary["non_target"],
        "fans": fans_out,
    }


def main() -> None:
    _verts, rot = icosahedron()
    validate_triangulation(rot)
    if len(rot) != 12 or any(len(nbrs) != 5 for nbrs in rot):
        raise AssertionError("not the 5-regular triangulation on 12 vertices")
    fixture = rotation_from_fixture(FIXTURES / "icosahedron-fixture.json")
    same_graph = graph_isomorphic(rot, fixture)
    transitive = vertex_transitive(rot)
    graph = build_move_graph(rot)
    targets = {
        key for key, canonical in graph["full"].items() if link_size(rot, key[0], canonical) <= 3
    }
    mixed_dist = reverse_distance(graph, targets, "both", CAP)
    slide_dist = reverse_distance(graph, targets, "slide", CAP)
    # One vertex is the census. The other eleven are the symmetry check.
    primary = summarise_vertex(rot, 0, graph, targets, mixed_dist, slide_dist, True)
    others = []
    for vertex in range(1, 12):
        summary = summarise_vertex(rot, vertex, graph, targets, mixed_dist, slide_dist, False)
        others.append(
            {
                "vertex": vertex,
                "orbits": summary["fans"][0]["orbits"],
                "link3": summary["fans"][0]["link3"],
                "link4": summary["fans"][0]["link4"],
                "worst": summary["fans"][0]["worst"],
                "patterns": sorted(summary["fans"][0]["patterns"]),
            }
        )
        del summary
    fan0 = primary["fans"][0]
    if any(row["unreachable"] for fan in primary["fans"] for row in [fan] if fan["unreachable"]):
        verdict = "KILL"
    elif any(fan["worst"] is None for fan in primary["fans"]):
        verdict = "KILL"
    else:
        verdict = "FILL"
    worst = max(fan["worst"] for fan in primary["fans"])
    state = primary["state"]
    witnesses = {}
    for distance in sorted({fan["worst"] for fan in primary["fans"]} | {0, worst}):
        if not any(row["mixed"] == distance for row in fan0["rows"]):
            continue
        row = pick_witness(fan0, distance)
        orbit = tuple(row["orbit"])
        record = {
            "pattern": row["pattern"],
            "orbit": row["orbit"],
            "link_colours": row["link_colours"],
            "mixed_kinds": row["mixed_kinds"],
            "one_slide": row["one_slide"],
            "slide_chain": row["slide_chain"],
            "swap_then_slides": row["swap_then_slides"],
            "slides": slide_landings(rot, 0, list(graph["full"][(0, orbit)])),
        }
        if distance >= 1:
            record["swap"] = witness_swap(rot, state, orbit)
        witnesses[str(distance)] = record
    payload = {
        "verdict": verdict,
        "worst_length": worst,
        "cap": CAP,
        "vertex": 0,
        "one_vertex_enough": transitive,
        "isomorphic_to_fixture": same_graph,
        "fans_agree": True,
        "other_vertices": others,
        "primary": json_ready(primary),
        "witnesses": witnesses,
    }
    # Retain a failing colouring explicitly when the cap is hit.
    failing = [
        row
        for fan in primary["fans"]
        for row in fan["rows"]
        if row["mixed"] is None or row["mixed"] > CAP
    ]
    payload["failing"] = [
        {"pattern": row["pattern"], "orbit": row["orbit"], "link_colours": row["link_colours"]}
        for row in failing
    ]
    out = HERE / "icosahedron-fan-data.json"
    out.write_text(json.dumps(payload, indent=1) + "\n")
    print(json.dumps({"verdict": verdict, "worst_length": worst, "fans": payload["primary"]["fans"][0], "witnesses": witnesses, "others_worst": [row["worst"] for row in others], "transitive": transitive, "fixture": same_graph}, indent=1))


if __name__ == "__main__":
    main()
