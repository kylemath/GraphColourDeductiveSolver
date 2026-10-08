"""Unequal-pole hybrid on the two-pole belt G_n minus one belt vertex.

G_n has poles a, b and belt u_i, v_i modulo n, with edges a-u_i, b-v_i,
u_i-u_{i+1}, v_i-v_{i+1}, u_i-v_i, u_i-v_{i-1}, and no a-b edge. The
deletion is h = u_0. Colourings are proper 4-colourings of G_n - h modulo
global colour permutation (first-occurrence form).

The hybrid, for c(a) != c(b), is any number of singleton vacancy slides, then
at most one whole-component Kempe swap in the current deletion graph, then
any number of further slides. A state is filled when the current boundary
uses at most three colours. This is an exhaustive finite check for n = 5 and
n = 8. It is not a proof for general n.
"""

from __future__ import annotations

import sys
from collections import deque
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from mass_core import deletion_colourings, validate_triangulation


def build_belt(n: int) -> tuple[list[list[int]], int, int]:
    """Return the rotation of G_n, the index of a, and the index of b.

    u_i = 2 + i and v_i = 2 + n + i.
    """
    if n < 3:
        raise ValueError(n)
    order = 2 + 2 * n
    a, b = 0, 1

    def u(i: int) -> int:
        return 2 + (i % n)

    def v(i: int) -> int:
        return 2 + n + (i % n)

    faces: list[tuple[int, int, int]] = []
    for i in range(n):
        faces.append((a, u(i), u(i + 1)))
        faces.append((b, v(i), v(i - 1)))
        faces.append((u(i + 1), u(i), v(i)))
        faces.append((v(i), u(i), v(i - 1)))

    succ: list[dict[int, int]] = [{} for _ in range(order)]
    for x, y, z in faces:
        succ[y][x] = z
        succ[z][y] = x
        succ[x][z] = y

    rot: list[list[int]] = []
    for vertex in range(order):
        start = next(iter(succ[vertex]))
        cycle = []
        seen = start
        while True:
            cycle.append(seen)
            seen = succ[vertex][seen]
            if seen == start:
                break
            if len(cycle) > order:
                raise RuntimeError("rotation did not close")
        if len(cycle) != len(succ[vertex]):
            raise RuntimeError("rotation missed a neighbour")
        rot.append(cycle)

    expected: set[tuple[int, int]] = set()

    def add(x: int, y: int) -> None:
        expected.add((x, y) if x < y else (y, x))

    for i in range(n):
        add(a, u(i))
        add(b, v(i))
        add(u(i), u(i + 1))
        add(v(i), v(i + 1))
        add(u(i), v(i))
        add(u(i), v(i - 1))
    got: set[tuple[int, int]] = set()
    for vertex, nbrs in enumerate(rot):
        for other in nbrs:
            got.add((vertex, other) if vertex < other else (other, vertex))
    if got != expected:
        raise RuntimeError("edge set disagrees with the belt description")
    if any(len(nbrs) != len(set(nbrs)) for nbrs in rot):
        raise RuntimeError("loop or repeated neighbour")
    validate_triangulation(rot)
    return rot, a, b


def hole_index(n: int) -> int:
    """u_0."""
    return 2


def vertex_name(n: int, vertex: int) -> str:
    if vertex == 0:
        return "a"
    if vertex == 1:
        return "b"
    if vertex < 2 + n:
        return f"u{vertex - 2}"
    return f"v{vertex - 2 - n}"


def colour_list(order: int, vertices: list[int], colours: tuple[int, ...], hole: int) -> list[int]:
    full = [-1] * order
    for index, vertex in enumerate(vertices):
        full[vertex] = colours[index]
    if full[hole] != -1:
        raise RuntimeError("hole is coloured")
    return full


def is_proper(rot: list[list[int]], col: list[int] | tuple[int, ...], hole: int | None = None) -> bool:
    for vertex, nbrs in enumerate(rot):
        if vertex == hole or col[vertex] < 0:
            continue
        for other in nbrs:
            if other == hole or col[other] < 0:
                continue
            if col[vertex] == col[other]:
                return False
    return True


def boundary_size(rot: list[list[int]], hole: int, col: tuple[int, ...] | list[int]) -> int:
    seen = 0
    mask = 0
    for other in rot[hole]:
        bit = 1 << col[other]
        if mask & bit == 0:
            mask |= bit
            seen += 1
    return seen


def is_target(rot: list[list[int]], hole: int, col: tuple[int, ...] | list[int]) -> bool:
    return boundary_size(rot, hole, col) <= 3


def canon_tuple(order: int, hole: int, col: list[int]) -> tuple[int, ...]:
    seen: dict[int, int] = {}
    out = []
    for vertex in range(order):
        if vertex == hole:
            out.append(-1)
            continue
        colour = col[vertex]
        mapped = seen.get(colour)
        if mapped is None:
            mapped = len(seen)
            seen[colour] = mapped
        out.append(mapped)
    return tuple(out)


def slide_moves(
    rot: list[list[int]], hole: int, col: tuple[int, ...]
) -> list[tuple[int, tuple[int, ...]]]:
    """Move the hole onto a boundary vertex whose colour appears once."""
    order = len(col)
    counts = [0, 0, 0, 0]
    for other in rot[hole]:
        counts[col[other]] += 1
    moves = []
    for other in rot[hole]:
        colour = col[other]
        if counts[colour] != 1:
            continue
        seen: dict[int, int] = {}
        out = [0] * order
        for vertex in range(order):
            if vertex == other:
                out[vertex] = -1
                continue
            source = colour if vertex == hole else col[vertex]
            mapped = seen.get(source)
            if mapped is None:
                mapped = len(seen)
                seen[source] = mapped
            out[vertex] = mapped
        moves.append((other, tuple(out)))
    return moves


def kempe_moves(
    rot: list[list[int]], hole: int, col: tuple[int, ...]
) -> list[tuple[int, tuple[int, int], tuple[int, ...], tuple[int, ...]]]:
    """Whole-component swaps in G - hole. Global relabelings are omitted."""
    order = len(col)
    found = []
    for first in range(4):
        for second in range(first + 1, 4):
            seen = [False] * order
            for seed in range(order):
                if seed == hole or seen[seed]:
                    continue
                if col[seed] != first and col[seed] != second:
                    continue
                stack = [seed]
                seen[seed] = True
                comp = []
                while stack:
                    vertex = stack.pop()
                    comp.append(vertex)
                    for other in rot[vertex]:
                        if other == hole or seen[other]:
                            continue
                        if col[other] == first or col[other] == second:
                            seen[other] = True
                            stack.append(other)
                member = [False] * order
                for vertex in comp:
                    member[vertex] = True
                mapped: dict[int, int] = {}
                out = [0] * order
                for vertex in range(order):
                    if vertex == hole:
                        out[vertex] = -1
                        continue
                    colour = col[vertex]
                    if member[vertex]:
                        colour = second if colour == first else first
                    image = mapped.get(colour)
                    if image is None:
                        image = len(mapped)
                        mapped[colour] = image
                    out[vertex] = image
                new_col = tuple(out)
                if new_col == col:
                    continue
                found.append((len(comp), (first, second), tuple(sorted(comp)), new_col))
    return found


def component_of(
    rot: list[list[int]], hole: int, col: list[int], first: int, second: int, seed: int
) -> set[int]:
    stack = [seed]
    seen = {seed}
    while stack:
        vertex = stack.pop()
        for other in rot[vertex]:
            if other == hole or other in seen:
                continue
            if col[other] == first or col[other] == second:
                seen.add(other)
                stack.append(other)
    return seen


def search(
    rot: list[list[int]],
    hole: int,
    col: list[int],
    cap: int,
) -> dict[str, object]:
    """Slides, then at most one Kempe swap, then slides. Exhaustive up to cap."""
    order = len(rot)
    start = canon_tuple(order, hole, col)
    phase: dict[tuple[int, tuple[int, ...]], None] = {(hole, start): None}
    queue: deque[tuple[int, tuple[int, ...]]] = deque([(hole, start)])
    slides_hit = is_target(rot, hole, start)
    while queue and not slides_hit:
        if len(phase) > cap:
            return {"status": "capped", "states": len(phase), "size": None}
        here, colours = queue.popleft()
        for nxt, new_col in slide_moves(rot, here, colours):
            key = (nxt, new_col)
            if key in phase:
                continue
            if len(phase) >= cap:
                return {"status": "capped", "states": len(phase), "size": None}
            phase[key] = None
            if is_target(rot, nxt, new_col):
                slides_hit = True
                break
            queue.append(key)
        if slides_hit:
            break
    if slides_hit:
        return {"status": "slides", "states": len(phase), "size": 0}

    buckets: list[deque[tuple[int, tuple[int, ...]]]] = [deque() for _ in range(order)]
    best: dict[tuple[int, tuple[int, ...]], int] = {}

    def consider(size: int, here: int, colours: tuple[int, ...]) -> None:
        key = (here, colours)
        if key in phase:
            return
        previous = best.get(key)
        if previous is not None and previous <= size:
            return
        best[key] = size
        buckets[size].append(key)

    states = len(phase)
    for here, colours in phase:
        for size, _pair, _comp, new_col in kempe_moves(rot, here, colours):
            before = len(best)
            consider(size, here, new_col)
            if len(best) > before:
                states += 1
                if states > cap:
                    return {"status": "capped", "states": states, "size": None}

    for size in range(1, order):
        live = buckets[size]
        while live:
            here, colours = live.popleft()
            if best[(here, colours)] != size:
                continue
            if is_target(rot, here, colours):
                return {"status": "kempe", "states": states, "size": size}
            for nxt, new_col in slide_moves(rot, here, colours):
                before = len(best)
                consider(size, nxt, new_col)
                if len(best) > before:
                    states += 1
                    if states > cap:
                        return {"status": "capped", "states": states, "size": None}
    return {"status": "unfilled", "states": states, "size": None}


def trace_kempe(
    rot: list[list[int]], hole: int, col: list[int], want: int
) -> dict[str, object]:
    """Replay the minimum-size success and return the swap that realises it."""
    order = len(rot)
    start = canon_tuple(order, hole, col)
    phase: dict[tuple[int, tuple[int, ...]], tuple[int, tuple[int, ...]] | None] = {
        (hole, start): None
    }
    queue: deque[tuple[int, tuple[int, ...]]] = deque([(hole, start)])
    while queue:
        here, colours = queue.popleft()
        for nxt, new_col in slide_moves(rot, here, colours):
            key = (nxt, new_col)
            if key in phase:
                continue
            phase[key] = (here, colours)
            queue.append(key)

    origin: dict[tuple[int, tuple[int, ...]], tuple[object, ...]] = {}
    buckets: list[deque[tuple[int, tuple[int, ...]]]] = [deque() for _ in range(order)]
    best: dict[tuple[int, tuple[int, ...]], int] = {}

    def consider(size: int, here: int, colours: tuple[int, ...], how: tuple[object, ...]) -> None:
        key = (here, colours)
        if key in phase:
            return
        previous = best.get(key)
        if previous is not None and previous <= size:
            return
        best[key] = size
        origin[key] = how
        buckets[size].append(key)

    for here, colours in phase:
        for size, pair, comp, new_col in kempe_moves(rot, here, colours):
            if size != want:
                continue
            consider(size, here, new_col, ("kempe", here, colours, pair, comp))

    live = buckets[want]
    while live:
        here, colours = live.popleft()
        if best[(here, colours)] != want:
            continue
        if is_target(rot, here, colours):
            cursor = (here, colours)
            slides_after = 0
            while origin[cursor][0] != "kempe":
                slides_after += 1
                _tag, prev_h, prev_c, _via = origin[cursor]
                cursor = (prev_h, prev_c)
            _tag, kempe_hole, _before, pair, comp = origin[cursor]
            slides_before = 0
            walk = (kempe_hole, _before)
            while phase[walk] is not None:
                slides_before += 1
                walk = phase[walk]
            return {
                "hole": kempe_hole,
                "pair": pair,
                "component": comp,
                "slides_before": slides_before,
                "slides_after": slides_after,
                "target_hole": here,
                "target_colours": colours,
            }
        for nxt, new_col in slide_moves(rot, here, colours):
            consider(want, nxt, new_col, ("slide", here, colours, nxt))
    raise RuntimeError("traced search missed the recorded success")


def population(col: list[int]) -> tuple[int, ...]:
    counts = [0, 0, 0, 0]
    for colour in col:
        if colour >= 0:
            counts[colour] += 1
    return tuple(sorted(counts, reverse=True))


def star_swap(n: int, rot: list[list[int]], col: list[int]) -> dict[str, object]:
    """Apply the equal-pole star described in TwoPoleStarEscape.md."""
    hole = hole_index(n)
    a, b = 0, 1
    if col[a] != col[b]:
        raise RuntimeError("star swap is for equal poles")
    pole = col[a]
    boundary = list(rot[hole])
    expected = {a, 2 + ((n - 1) % n), 2 + 1, 2 + n + ((n - 1) % n), 2 + n}
    if set(boundary) != expected:
        raise RuntimeError(f"link of u_0 is {boundary}, expected {sorted(expected)}")
    counts: dict[int, int] = {}
    for vertex in boundary:
        counts[col[vertex]] = counts.get(col[vertex], 0) + 1
    other_ring = (2 + n + ((n - 1) % n), 2 + n)  # v_{n-1}, v_0
    chosen = None
    for vertex in other_ring:
        if counts[col[vertex]] == 1:
            chosen = vertex
            break
    if chosen is None:
        raise RuntimeError("no singleton colour on the other ring")
    belt_colour = col[chosen]
    predicted = {b}
    for i in range(n):
        vertex = 2 + n + i
        if col[vertex] == belt_colour:
            predicted.add(vertex)
    actual = component_of(rot, hole, col, pole, belt_colour, b)
    if actual != predicted:
        raise RuntimeError("star component disagrees with the deletion graph")
    swapped = col[:]
    for vertex in actual:
        swapped[vertex] = belt_colour if col[vertex] == pole else pole
    after = [swapped[vertex] for vertex in boundary]
    if len(set(after)) > 3:
        raise RuntimeError("star swap left four colours on the boundary")
    if belt_colour in after:
        raise RuntimeError("the singleton belt colour survived on the boundary")
    missing = [colour for colour in range(4) if colour not in after][0]
    filled = swapped[:]
    filled[hole] = missing
    if not is_proper(rot, filled, None):
        raise RuntimeError("filling after the star swap is improper")
    return {
        "singleton": chosen,
        "belt_colour": belt_colour,
        "pole_colour": pole,
        "component_size": len(actual),
        "component": tuple(sorted(actual)),
        "boundary_before": tuple(col[vertex] for vertex in boundary),
        "boundary_after": tuple(after),
        "filled_hole_colour": missing,
    }


def classify_n(n: int, cap: int) -> dict[str, object]:
    rot, a, b = build_belt(n)
    order = len(rot)
    hole = hole_index(n)
    if n == 8 and (order != 18 or len(rot[a]) != 8 or len(rot[b]) != 8):
        raise RuntimeError("G_8 does not match the Florek degree description")
    if any(len(rot[2 + i]) != 5 or len(rot[2 + n + i]) != 5 for i in range(n)):
        raise RuntimeError("a belt vertex is not degree 5")
    vertices, colourings = deletion_colourings(rot, hole)
    equal = []
    unequal = []
    for colours in colourings:
        full = colour_list(order, vertices, colours, hole)
        if not is_proper(rot, full, hole):
            raise RuntimeError("enumerated colouring is improper")
        if full[a] == full[b]:
            equal.append(full)
        else:
            unequal.append(full)

    k = (n - 2) // 3
    if n != 3 * k + 2:
        raise RuntimeError("this check expects n ≡ 2 mod 3")
    expected_pop = tuple(sorted((2, 2 * k + 1, 2 * k + 1, 2 * k + 1), reverse=True))
    star_rows = []
    for full in equal:
        if population(full) != expected_pop:
            raise RuntimeError(f"equal-pole population {population(full)} != {expected_pop}")
        if is_target(rot, hole, full):
            raise RuntimeError("equal-pole boundary was already a target")
        star_rows.append(star_swap(n, rot, full))

    example = equal[0]
    example_star = star_rows[0]
    example_search = search(rot, hole, example, cap)
    if example_search["status"] not in ("slides", "kempe"):
        raise RuntimeError("enumerator did not fill the equal-pole example")
    star_state = None
    for size, pair, comp, new_col in kempe_moves(rot, hole, canon_tuple(order, hole, example)):
        if size == example_star["component_size"] and is_target(rot, hole, new_col):
            star_state = (size, pair, comp)
            break
    if star_state is None:
        raise RuntimeError("enumerator does not see the explicit star as a filling Kempe move")

    counts = {"slides": 0, "kempe": 0, "unfilled": 0, "capped": 0}
    already = sum(1 for full in unequal if is_target(rot, hole, full))
    worst = -1
    worst_index = None
    max_states = 0
    unfilled_index = None
    for index, full in enumerate(unequal):
        result = search(rot, hole, full, cap)
        status = str(result["status"])
        counts[status] += 1
        max_states = max(max_states, int(result["states"]))
        if status == "kempe":
            size = int(result["size"])
            if size > worst:
                worst = size
                worst_index = index
        elif status == "unfilled" and unfilled_index is None:
            unfilled_index = index
        if (index + 1) % 50 == 0:
            print(f"n={n} {index + 1}/{len(unequal)} {counts} max_states={max_states}", flush=True)

    if worst < 0 and counts["kempe"] == 0 and counts["unfilled"] == 0 and counts["capped"] == 0:
        worst = 0
    witness: dict[str, object] | None = None
    if unfilled_index is not None:
        full = unequal[unfilled_index]
        witness = {
            "kind": "unfilled",
            "colours": named_colours(n, full),
            "boundary": named_boundary(n, rot, hole, full),
        }
    elif worst_index is not None:
        full = unequal[worst_index]
        traced = trace_kempe(rot, hole, full, worst)
        witness = {
            "kind": "kempe",
            "size": worst,
            "colours": named_colours(n, full),
            "boundary": named_boundary(n, rot, hole, full),
            "swap_hole": vertex_name(n, int(traced["hole"])),
            "pair": traced["pair"],
            "component": [vertex_name(n, vertex) for vertex in traced["component"]],
            "slides_before": traced["slides_before"],
            "slides_after": traced["slides_after"],
            "target_hole": vertex_name(n, int(traced["target_hole"])),
        }
    return {
        "n": n,
        "order": order,
        "orbits": len(colourings),
        "equal": len(equal),
        "unequal": len(unequal),
        "counts": counts,
        "already": already,
        "worst": worst,
        "max_states": max_states,
        "star_sizes": sorted({int(row["component_size"]) for row in star_rows}),
        "equal_example": {
            "colours": named_colours(n, example),
            "boundary_before": [
                (vertex_name(n, vertex), example[vertex]) for vertex in rot[hole]
            ],
            "star": {
                "singleton": vertex_name(n, int(example_star["singleton"])),
                "component_size": example_star["component_size"],
                "component": [vertex_name(n, vertex) for vertex in example_star["component"]],
                "boundary_after": [
                    (vertex_name(n, vertex), colour)
                    for vertex, colour in zip(rot[hole], example_star["boundary_after"])
                ],
                "filled_hole_colour": example_star["filled_hole_colour"],
            },
            "search": example_search["status"],
        },
        "witness": witness,
    }


def named_colours(n: int, col: list[int]) -> list[tuple[str, int]]:
    hole = hole_index(n)
    return [(vertex_name(n, vertex), col[vertex]) for vertex in range(len(col)) if vertex != hole]


def named_boundary(
    n: int, rot: list[list[int]], hole: int, col: list[int]
) -> list[tuple[str, int]]:
    return [(vertex_name(n, vertex), col[vertex]) for vertex in rot[hole]]


def main() -> None:
    cap = 20000
    reports = [classify_n(5, cap), classify_n(8, cap)]
    for report in reports:
        print(report["n"], report["orbits"], report["equal"], report["unequal"], report["counts"],
              "already", report["already"], "worst", report["worst"], "states", report["max_states"])
        print("star", report["star_sizes"], "equal_search", report["equal_example"]["search"])
        print("witness", report["witness"])


if __name__ == "__main__":
    main()
