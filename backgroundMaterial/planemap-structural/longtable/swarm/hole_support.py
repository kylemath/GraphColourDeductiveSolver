"""Support of the targetless singleton-slide component on order-18 graph 10.

Graph 10 is Florek's two-pole suspension G_8: two nonadjacent degree-8 poles
and sixteen degree-5 belt vertices. The start is discovery table 18-10-r0,
state 93, the published population-(2,5,5,5) colouring. A singleton slide
moves the hole to a neighbour whose colour appears once on the boundary.
Colours are canonicalized by first appearance in vertex order. The search
stops if the component exceeds the state cap before it closes.
"""

from __future__ import annotations

import gzip
import json
import sys
from collections import Counter, deque
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mass_core import validate_triangulation

TABLES = HERE.parent / "wp11-discovery" / "tables"
POPULATION = HERE.parent.parent / "independent-inquiry" / "vacancy-population-results.json"
OUT = HERE / "hole-support-data.json"
STATE_CAP = 4000
START_FIXTURE = "18-10-r0.json.gz"
START_INDEX = 93


def canon(colouring: list[int]) -> tuple[int, ...]:
    """First-appearance colour names. The hole stays -1."""
    names: dict[int, int] = {}
    out = []
    for colour in colouring:
        if colour == -1:
            out.append(-1)
        else:
            out.append(names.setdefault(colour, len(names)))
    return tuple(out)


def load_table(name: str) -> dict:
    path = TABLES / name
    return json.loads(gzip.decompress(path.read_bytes()))


def place(table: dict, index: int) -> list[int]:
    colouring = [-1] * len(table["graph"]["rotation"])
    for vertex, colour in zip(table["vertex_order"], table["states"][index]["coloring"]):
        colouring[vertex] = colour
    return colouring


def proper(rot: list[list[int]], colouring: list[int]) -> bool:
    for vertex, neighbours in enumerate(rot):
        for neighbour in neighbours:
            if colouring[vertex] == -1 or colouring[neighbour] == -1:
                continue
            if colouring[vertex] == colouring[neighbour]:
                return False
    return True


def slides_from(rot: list[list[int]], hole: int, colouring: tuple[int, ...]):
    boundary = rot[hole]
    counts = Counter(colouring[vertex] for vertex in boundary)
    moves = []
    for vertex in boundary:
        if counts[colouring[vertex]] != 1:
            continue
        moved = list(colouring)
        moved[hole] = moved[vertex]
        moved[vertex] = -1
        if not proper(rot, moved):
            raise AssertionError(f"slide {hole} -> {vertex} broke properness")
        moves.append((vertex, canon(moved)))
    return moves


def bfs(rot: list[list[int]], start: tuple[int, tuple[int, ...]], cap: int):
    queue = deque([start])
    parent: dict[tuple[int, tuple[int, ...]], tuple | None] = {start: None}
    edge: dict[tuple[int, tuple[int, ...]], int | None] = {start: None}
    capped = False
    while queue:
        if len(parent) > cap:
            capped = True
            break
        state = queue.popleft()
        hole, colouring = state
        for destination, moved in slides_from(rot, hole, colouring):
            nxt = (destination, moved)
            if nxt in parent:
                continue
            if len(parent) >= cap:
                capped = True
                queue.clear()
                break
            parent[nxt] = state
            edge[nxt] = hole
            queue.append(nxt)
    closed = not capped and not queue
    return parent, edge, closed, capped


def induced_edges(rot: list[list[int]], vertices: list[int]) -> list[list[int]]:
    chosen = set(vertices)
    edges = []
    for vertex in vertices:
        for neighbour in rot[vertex]:
            if neighbour in chosen and vertex < neighbour:
                edges.append([vertex, neighbour])
    return edges


def induced_has_cycle(rot: list[list[int]], vertices: list[int]) -> bool:
    """A back-edge to a non-parent in the undirected induced subgraph."""
    chosen = set(vertices)
    seen: set[int] = set()

    def walk(vertex: int, previous: int | None) -> bool:
        seen.add(vertex)
        for neighbour in rot[vertex]:
            if neighbour not in chosen or neighbour == previous:
                continue
            if neighbour in seen:
                return True
            if walk(neighbour, vertex):
                return True
        return False

    for vertex in vertices:
        if vertex not in seen and walk(vertex, None):
            return True
    return False


def ring_order(rot: list[list[int]], pole: int) -> list[int]:
    """Cyclic neighbour order of a pole. In a triangulation this is a cycle."""
    return list(rot[pole])


def identify_g8(rot: list[list[int]]) -> dict:
    poles = [vertex for vertex, neighbours in enumerate(rot) if len(neighbours) == 8]
    belt = [vertex for vertex, neighbours in enumerate(rot) if len(neighbours) == 5]
    if len(poles) != 2 or len(belt) != 16:
        raise AssertionError(f"degree pattern is not two 8s and sixteen 5s: {poles}")
    left, right = poles
    if right in rot[left]:
        raise AssertionError("the degree-8 vertices are adjacent")
    u_ring = ring_order(rot, left)
    v_ring = ring_order(rot, right)
    if set(u_ring) | set(v_ring) != set(belt) or set(u_ring) & set(v_ring):
        raise AssertionError("pole neighbourhoods do not partition the belt")
    u_index = {vertex: i for i, vertex in enumerate(u_ring)}
    v_index = {vertex: i for i, vertex in enumerate(v_ring)}
    n = len(u_ring)

    def consecutive_pair(index: dict[int, int], vertices: list[int]) -> tuple[int, int] | None:
        if len(vertices) != 2:
            return None
        i, j = index[vertices[0]], index[vertices[1]]
        gap = (j - i) % n
        if gap == 1:
            return i, j
        if gap == n - 1:
            return j, i
        return None

    # Orient the v-ring so that u_i meets v_i and v_{i-1}, matching TwoPoleStarEscape.
    aligned = None
    for start in range(n):
        for step in (1, -1):
            good = True
            for i, u_vertex in enumerate(u_ring):
                cross = [w for w in rot[u_vertex] if w in v_index]
                pair = consecutive_pair(v_index, cross)
                # u_i meets two consecutive vertices of the v-ring, shifted and possibly reflected.
                position = (start + step * i) % n
                expected = {position, (position - step) % n}
                if pair is None or set(pair) != expected:
                    good = False
                    break
            if good:
                aligned = {"start": start, "step": step}
                break
        if aligned:
            break
    if aligned is None:
        raise AssertionError("cross edges are not the antiprism suspension")
    return {
        "poles": poles,
        "belt": belt,
        "u_pole": left,
        "v_pole": right,
        "u_ring": u_ring,
        "v_ring": v_ring,
        "alignment": aligned,
    }


def kempe_component(rot, colouring, colours: set[int], start: int) -> set[int]:
    if colouring[start] not in colours:
        return set()
    found = {start}
    stack = [start]
    while stack:
        vertex = stack.pop()
        for neighbour in rot[vertex]:
            if neighbour in found or colouring[neighbour] not in colours:
                continue
            found.add(neighbour)
            stack.append(neighbour)
    return found


def star_swap(rot, structure: dict, hole: int, colouring: tuple[int, ...]) -> dict | None:
    """The TwoPoleStarEscape swap, or None when its hypotheses fail."""
    u_pole = structure["u_pole"]
    v_pole = structure["v_pole"]
    u_set = set(structure["u_ring"])
    v_set = set(structure["v_ring"])
    if hole not in u_set and hole not in v_set:
        return None
    if colouring[u_pole] != colouring[v_pole] or colouring[u_pole] == -1:
        return None
    if hole in u_set:
        own_pole, other_pole = u_pole, v_pole
        own_set, other_ring = u_set, structure["v_ring"]
    else:
        own_pole, other_pole = v_pole, u_pole
        own_set, other_ring = v_set, structure["u_ring"]
    boundary = list(rot[hole])
    boundary_colours = [colouring[vertex] for vertex in boundary]
    counts = Counter(boundary_colours)
    pole_colour = colouring[own_pole]
    other_boundary = [vertex for vertex in boundary if vertex in set(other_ring)]
    own_boundary = [vertex for vertex in boundary if vertex in own_set]
    belt_has_pole_colour = any(
        colouring[vertex] == pole_colour for vertex in range(len(rot)) if vertex != hole and vertex not in (u_pole, v_pole)
    )
    singletons = [
        vertex for vertex in other_boundary if counts[colouring[vertex]] == 1
    ]
    record = {
        "hole": hole,
        "pole_colour": pole_colour,
        "poles_equal": True,
        "boundary": boundary,
        "boundary_colours": boundary_colours,
        "boundary_colour_count": len(counts),
        "other_boundary": other_boundary,
        "other_boundary_adjacent": other_boundary[1] in rot[other_boundary[0]] if len(other_boundary) == 2 else False,
        "own_boundary": own_boundary,
        "belt_vertex_has_pole_colour": belt_has_pole_colour,
        "singleton_other_ring": singletons,
        "available": False,
    }
    if len(counts) <= 3:
        record["already_target"] = True
        return record
    record["already_target"] = False
    if belt_has_pole_colour or len(other_boundary) != 2 or not record["other_boundary_adjacent"]:
        return record
    if not singletons:
        return record
    # The note uses any singleton colour on the other ring. Take the least vertex.
    anchor = min(singletons)
    rare = colouring[anchor]
    predicted = {other_pole} | {vertex for vertex in other_ring if colouring[vertex] == rare}
    actual = kempe_component(rot, colouring, {pole_colour, rare}, other_pole)
    swapped = list(colouring)
    for vertex in actual:
        swapped[vertex] = rare if colouring[vertex] == pole_colour else pole_colour
    if not proper(rot, swapped):
        raise AssertionError("star swap broke properness")
    new_boundary = [swapped[vertex] for vertex in boundary]
    record.update({
        "anchor": anchor,
        "rare_colour": rare,
        "predicted_star": sorted(predicted),
        "actual_component": sorted(actual),
        "component_is_the_star": actual == predicted,
        "boundary_colours_after": new_boundary,
        "boundary_colour_count_after": len(set(new_boundary)),
        "available": actual == predicted and len(set(new_boundary)) <= 3 and len(actual) == len(predicted),
        "single_component": True,
    })
    return record


def path_to(parent, state) -> list[tuple[int, tuple[int, ...]]]:
    steps = []
    while state is not None:
        steps.append(state)
        state = parent[state]
    steps.reverse()
    return steps


def population(colouring) -> list[int]:
    counts = Counter(colour for colour in colouring if colour != -1)
    return sorted(counts.values())


def main() -> None:
    table = load_table(START_FIXTURE)
    rot = table["graph"]["rotation"]
    validate_triangulation(rot)
    structure = identify_g8(rot)
    raw = place(table, START_INDEX)
    if not proper(rot, raw):
        raise AssertionError("published start is not proper")
    start = (table["root"], canon(raw))
    if population(start[1]) != [2, 5, 5, 5]:
        raise AssertionError(f"unexpected population {population(start[1])}")
    parent, _edge, closed, capped = bfs(rot, start, STATE_CAP)
    holes = sorted({hole for hole, _colouring in parent})
    degrees = {vertex: len(rot[vertex]) for vertex in holes}
    poles = structure["poles"]
    pole_states = [state for state in parent if state[0] in poles]
    belt_states = [state for state in parent if state[0] not in poles]
    reaching = next((state for state in pole_states), None)
    explicit = None
    if reaching is not None:
        route = path_to(parent, reaching)
        before = route[-2]
        explicit = {
            "from_hole": before[0],
            "to_hole": reaching[0],
            "from_colouring": list(before[1]),
            "to_colouring": list(reaching[1]),
            "hole_path": [state[0] for state in route],
        }
    equal_rows = []
    for state in belt_states:
        hole, colouring = state
        if colouring[poles[0]] != colouring[poles[1]]:
            continue
        checked = star_swap(rot, structure, hole, colouring)
        if checked is not None:
            checked["colouring"] = list(colouring)
        equal_rows.append(checked)
    published = json.loads(POPULATION.read_text())["failed_starts"]
    siblings = []
    for row in published:
        other = load_table(row["fixture"])
        if other["graph"]["ascii"] != table["graph"]["ascii"]:
            raise AssertionError(f"{row['fixture']} is a different graph")
        placed = canon(place(other, row["state_index"]))
        state = (other["root"], placed)
        siblings.append({
            "fixture": row["fixture"],
            "state_index": row["state_index"],
            "root": other["root"],
            "in_component": state in parent,
            "population": population(placed),
        })
    unequal = sum(
        1 for hole, colouring in belt_states if colouring[poles[0]] != colouring[poles[1]]
    )
    edges = induced_edges(rot, holes)
    per_hole = Counter(hole for hole, _colouring in parent)
    boundary_sizes = Counter(
        len({colouring[vertex] for vertex in rot[hole]}) for hole, colouring in parent
    )
    into_pole = {pole: [] for pole in poles}
    for hole, colouring in parent:
        for destination, _moved in slides_from(rot, hole, colouring):
            if destination in into_pole:
                into_pole[destination].append(hole)
    fill_populations = set()
    star_sizes = set()
    for row in equal_rows:
        if not row or not row.get("available"):
            continue
        hole = row["hole"]
        colouring = row["colouring"]
        swapped = list(colouring)
        pole_colour, rare = row["pole_colour"], row["rare_colour"]
        for vertex in row["actual_component"]:
            swapped[vertex] = rare if colouring[vertex] == pole_colour else pole_colour
        missing = list(set(range(4)) - set(row["boundary_colours_after"]))
        if len(missing) != 1 or not proper(rot, swapped):
            raise AssertionError("star swap did not leave a 3-coloured boundary")
        swapped[hole] = missing[0]
        if not proper(rot, swapped):
            raise AssertionError("filling the hole after the star swap is improper")
        fill_populations.add(tuple(population(swapped)))
        star_sizes.add(len(row["actual_component"]))
    data = {
        "fixture": START_FIXTURE,
        "state_index": START_INDEX,
        "order": table["graph"]["order"],
        "graph_index": table["graph"]["graph_index"],
        "ascii": table["graph"]["ascii"],
        "ascii_sha256": table["graph"]["ascii_sha256"],
        "state_cap": STATE_CAP,
        "states_seen": len(parent),
        "closed": closed,
        "capped": capped,
        "population": population(start[1]),
        "poles": poles,
        "pole_nonadjacent": structure["v_pole"] not in rot[structure["u_pole"]],
        "u_pole": structure["u_pole"],
        "v_pole": structure["v_pole"],
        "u_ring": structure["u_ring"],
        "v_ring": structure["v_ring"],
        "belt": structure["belt"],
        "S": holes,
        "degrees": {str(vertex): degree for vertex, degree in degrees.items()},
        "both_poles_in_S": all(pole in holes for pole in poles),
        "induced_edges": edges,
        "induced_edge_count": len(edges),
        "induced_cycle": induced_has_cycle(rot, holes),
        "states_per_hole": {str(vertex): per_hole[vertex] for vertex in holes},
        "boundary_colour_counts": {str(size): count for size, count in sorted(boundary_sizes.items())},
        "slides_into_pole": {str(pole): sorted(set(sources)) for pole, sources in into_pole.items()},
        "star_component_sizes": sorted(star_sizes),
        "fill_populations": sorted(fill_populations),
        "explicit_slide": explicit,
        "belt_states": len(belt_states),
        "pole_states": len(pole_states),
        "unequal_pole_belt_states": unequal,
        "equal_pole_belt_states": len(equal_rows),
        "star_available_count": sum(bool(row and row.get("available")) for row in equal_rows),
        "star_example": next((row for row in equal_rows if row and row.get("available")), equal_rows[0] if equal_rows else None),
        "start_colouring": list(start[1]),
        "siblings": siblings,
    }
    OUT.write_text(json.dumps(data, indent=2) + "\n")
    summary = {k: data[k] for k in (
        "states_seen", "closed", "capped", "S", "degrees", "both_poles_in_S",
        "induced_edge_count", "induced_cycle", "belt_states", "pole_states",
        "unequal_pole_belt_states", "equal_pole_belt_states", "star_available_count", "poles",
    )}
    summary["siblings_inside"] = sum(row["in_component"] for row in siblings)
    summary["sibling_roots"] = [row["root"] for row in siblings]
    print(json.dumps(summary, indent=2))
    if explicit:
        print("slide", explicit["from_hole"], "->", explicit["to_hole"], "path", explicit["hole_path"])
    if data["star_example"]:
        example = data["star_example"]
        print("star", json.dumps({k: example[k] for k in example if k not in ("boundary",)}, indent=2))


if __name__ == "__main__":
    main()
