# The Four Color Theorem: A Comprehensive Study

## Table of Contents
1. [Statement of the Theorem](#statement-of-the-theorem)
2. [Graph-Theoretic Formulation](#graph-theoretic-formulation)
3. [Related Bounds and Corollaries](#related-bounds-and-corollaries)
4. [History of Proofs and Attempts](#history-of-proofs-and-attempts)
5. [The Appel-Haken Computer-Assisted Proof](#the-appel-haken-computer-assisted-proof)
6. [Modern Developments](#modern-developments)
7. [Implementation Examples](#implementation-examples)

---

## Statement of the Theorem

The **Four Color Theorem** states that any map drawn on a plane (or equivalently, on a sphere) can be colored using at most **four colors** such that no two adjacent regions (regions sharing a common boundary segment, not just a point) have the same color.

### Formal Statement

> **Theorem (Four Color Theorem):** Every planar graph $G$ is 4-colorable. That is:
> $$\chi(G) \leq 4$$
> where $\chi(G)$ denotes the chromatic number of $G$.

### Key Definitions

| Term | Definition |
|------|------------|
| **Planar Graph** | A graph that can be embedded in the plane without edge crossings |
| **Chromatic Number** | $\chi(G)$ = minimum number of colors needed to color vertices so no adjacent vertices share a color |
| **Proper Coloring** | An assignment of colors to vertices where no two adjacent vertices have the same color |
| **k-colorable** | A graph is k-colorable if it admits a proper coloring with at most k colors |

---

## Graph-Theoretic Formulation

### From Maps to Graphs

Every map can be converted to a **dual graph** where:
- Each region becomes a vertex
- Two vertices are connected by an edge if and only if their corresponding regions share a boundary

```python
import networkx as nx
import matplotlib.pyplot as plt

def map_to_dual_graph(regions_adjacency):
    """
    Convert a map's adjacency information to a dual graph.
    
    Parameters:
    -----------
    regions_adjacency : dict
        Dictionary where keys are region names and values are lists of adjacent regions
        
    Returns:
    --------
    G : networkx.Graph
        The dual graph representing the map
    
    Example:
    --------
    >>> adjacency = {
    ...     'A': ['B', 'C', 'D'],
    ...     'B': ['A', 'C', 'E'],
    ...     'C': ['A', 'B', 'D', 'E'],
    ...     'D': ['A', 'C', 'E'],
    ...     'E': ['B', 'C', 'D']
    ... }
    >>> G = map_to_dual_graph(adjacency)
    """
    G = nx.Graph()
    
    # Add all regions as vertices
    for region in regions_adjacency:
        G.add_node(region)
    
    # Add edges for adjacent regions
    for region, neighbors in regions_adjacency.items():
        for neighbor in neighbors:
            G.add_edge(region, neighbor)
    
    return G

# Example: Simple map with 5 regions
adjacency = {
    'Region_A': ['Region_B', 'Region_C', 'Region_D'],
    'Region_B': ['Region_A', 'Region_C', 'Region_E'],
    'Region_C': ['Region_A', 'Region_B', 'Region_D', 'Region_E'],
    'Region_D': ['Region_A', 'Region_C', 'Region_E'],
    'Region_E': ['Region_B', 'Region_C', 'Region_D']
}

G = map_to_dual_graph(adjacency)
print(f"Vertices: {G.number_of_nodes()}")
print(f"Edges: {G.number_of_edges()}")
print(f"Is planar: {nx.check_planarity(G)[0]}")
```

### Checking Planarity

A graph is planar if and only if it does not contain $K_5$ (complete graph on 5 vertices) or $K_{3,3}$ (complete bipartite graph) as a minor. This is the **Kuratowski-Wagner Theorem**.

```python
def check_planarity_detailed(G):
    """
    Check if a graph is planar and return detailed information.
    
    Uses the Boyer-Myrvold planarity algorithm (O(n) time complexity).
    """
    is_planar, embedding = nx.check_planarity(G)
    
    result = {
        'is_planar': is_planar,
        'num_vertices': G.number_of_nodes(),
        'num_edges': G.number_of_edges(),
    }
    
    if is_planar:
        # For planar graphs, verify Euler's formula
        # V - E + F = 2 (for connected graphs)
        # We can compute F from this
        V = G.number_of_nodes()
        E = G.number_of_edges()
        F = 2 - V + E  # Number of faces (including outer face)
        result['num_faces'] = F
        result['euler_characteristic'] = V - E + F
    
    return result

# Test with K4 (planar) and K5 (non-planar)
K4 = nx.complete_graph(4)
K5 = nx.complete_graph(5)

print("K4:", check_planarity_detailed(K4))
print("K5:", check_planarity_detailed(K5))
```

---

## Related Bounds and Corollaries

### Euler's Formula

For any connected planar graph embedded in the plane:

$$V - E + F = 2$$

where:
- $V$ = number of vertices
- $E$ = number of edges  
- $F$ = number of faces (including the unbounded outer face)

**Corollary:** For a simple planar graph with $V \geq 3$:

$$E \leq 3V - 6$$

This implies every planar graph has a vertex of degree at most 5.

```python
def verify_euler_formula(G):
    """
    Verify Euler's formula for a planar graph.
    
    For a connected planar graph: V - E + F = 2
    
    Since F = 2 - V + E for planar graphs, we verify the edge bound.
    """
    V = G.number_of_nodes()
    E = G.number_of_edges()
    
    is_planar = nx.check_planarity(G)[0]
    
    if not is_planar:
        return {'error': 'Graph is not planar'}
    
    # For planar graphs: E <= 3V - 6 (for V >= 3)
    edge_bound = 3 * V - 6
    satisfies_bound = E <= edge_bound
    
    # Minimum degree in a planar graph is at most 5
    min_degree = min(dict(G.degree()).values()) if G.number_of_nodes() > 0 else 0
    
    # Calculate number of faces using Euler's formula
    # Assuming connected graph
    F = 2 - V + E
    
    return {
        'V': V,
        'E': E,
        'F': F,
        'euler_characteristic': V - E + F,
        'edge_bound_3V_minus_6': edge_bound,
        'satisfies_edge_bound': satisfies_bound,
        'min_degree': min_degree,
        'has_vertex_degree_at_most_5': min_degree <= 5
    }

# Example with a planar graph
G = nx.petersen_graph()  # Not planar
H = nx.dodecahedral_graph()  # Planar

print("Petersen Graph (non-planar):", verify_euler_formula(G))
print("Dodecahedral Graph (planar):", verify_euler_formula(H))
```

### The Five Color Theorem

Before the Four Color Theorem was proven, **Heawood (1890)** proved:

> **Theorem (Five Color Theorem):** Every planar graph is 5-colorable.

The proof is elementary and uses induction:

1. Every planar graph has a vertex $v$ of degree $\leq 5$ (from Euler's formula)
2. Remove $v$, color the remaining graph by induction
3. If $\deg(v) \leq 4$, we have a spare color for $v$
4. If $\deg(v) = 5$, use a **Kempe chain argument** to free up a color

```python
def five_color_greedy(G):
    """
    Implement a greedy 5-coloring algorithm for planar graphs.
    
    This is guaranteed to work for planar graphs due to the
    Five Color Theorem.
    """
    if not nx.check_planarity(G)[0]:
        raise ValueError("Graph must be planar")
    
    # Order vertices by degree (smallest first - a simple heuristic)
    # Better: use smallest-last ordering
    vertices = sorted(G.nodes(), key=lambda v: G.degree(v))
    
    coloring = {}
    
    for v in vertices:
        # Find colors used by neighbors
        neighbor_colors = {coloring[n] for n in G.neighbors(v) if n in coloring}
        
        # Assign the smallest available color (0-indexed)
        for color in range(5):
            if color not in neighbor_colors:
                coloring[v] = color
                break
    
    return coloring

# Example
G = nx.dodecahedral_graph()
coloring = five_color_greedy(G)
num_colors = len(set(coloring.values()))
print(f"Colors used: {num_colors}")
print(f"Coloring valid: {all(coloring[u] != coloring[v] for u, v in G.edges())}")
```

### Heawood Conjecture for Higher Genus Surfaces

For a surface of genus $g > 0$, the maximum chromatic number is:

$$H(g) = \left\lfloor \frac{7 + \sqrt{1 + 48g}}{2} \right\rfloor$$

| Surface | Genus $g$ | $H(g)$ |
|---------|-----------|--------|
| Sphere | 0 | 4 (Four Color Theorem) |
| Torus | 1 | 7 |
| Double Torus | 2 | 8 |
| Triple Torus | 3 | 9 |

```python
import math

def heawood_number(genus):
    """
    Calculate the Heawood number for a surface of given genus.
    
    The Heawood number H(g) is the maximum chromatic number for
    graphs embeddable on a surface of genus g.
    
    H(g) = floor((7 + sqrt(1 + 48g)) / 2)
    
    Note: For g=0 (sphere), the formula gives 4, which is the
    Four Color Theorem.
    """
    if genus < 0:
        raise ValueError("Genus must be non-negative")
    
    return int((7 + math.sqrt(1 + 48 * genus)) // 2)

# Calculate for various surfaces
surfaces = [
    ("Sphere", 0),
    ("Torus", 1),
    ("Double Torus", 2),
    ("Triple Torus", 3),
    ("Genus 4", 4),
    ("Genus 5", 5),
]

print("Heawood Numbers for Various Surfaces:")
print("-" * 40)
for name, g in surfaces:
    print(f"{name} (g={g}): H(g) = {heawood_number(g)}")
```

---

## History of Proofs and Attempts

### Timeline

| Year | Event |
|------|-------|
| **1852** | Francis Guthrie conjectures four colors suffice |
| **1879** | Alfred Kempe publishes flawed "proof" |
| **1890** | Percy Heawood finds error; proves Five Color Theorem |
| **1913** | George Birkhoff introduces reducibility |
| **1922** | Franklin proves theorem for maps with ≤25 regions |
| **1969** | Heesch develops discharging method |
| **1976** | **Appel-Haken prove the theorem with computer assistance** |
| **1997** | Robertson et al. provide simplified proof |
| **2005** | Gonthier formally verifies proof in Coq |

### Kempe Chains

Despite his proof being wrong, Kempe introduced the crucial concept of **Kempe chains**:

> A **Kempe chain** is a maximal connected subgraph containing only vertices of two specific colors.

Swapping the colors in a Kempe chain preserves the validity of the coloring.

```python
def find_kempe_chain(G, coloring, start_vertex, color1, color2):
    """
    Find a Kempe chain starting from a vertex.
    
    A Kempe chain is a maximal connected component of vertices
    colored with exactly two colors.
    
    Parameters:
    -----------
    G : networkx.Graph
        The graph
    coloring : dict
        Current vertex coloring
    start_vertex : any
        Starting vertex (must be colored with color1 or color2)
    color1, color2 : int
        The two colors defining the Kempe chain
        
    Returns:
    --------
    chain : set
        Set of vertices in the Kempe chain
    """
    if coloring[start_vertex] not in (color1, color2):
        raise ValueError("Start vertex must be colored with color1 or color2")
    
    chain = set()
    to_visit = [start_vertex]
    
    while to_visit:
        v = to_visit.pop()
        if v in chain:
            continue
        
        if coloring[v] in (color1, color2):
            chain.add(v)
            for neighbor in G.neighbors(v):
                if neighbor not in chain and coloring[neighbor] in (color1, color2):
                    to_visit.append(neighbor)
    
    return chain


def swap_kempe_chain(coloring, chain, color1, color2):
    """
    Swap colors in a Kempe chain.
    
    This operation preserves the validity of the coloring.
    """
    new_coloring = coloring.copy()
    
    for v in chain:
        if new_coloring[v] == color1:
            new_coloring[v] = color2
        elif new_coloring[v] == color2:
            new_coloring[v] = color1
    
    return new_coloring


# Example: Demonstrate Kempe chain swap
def demonstrate_kempe_chain():
    """
    Demonstrate Kempe chain identification and swapping.
    """
    # Create a simple graph
    G = nx.cycle_graph(6)
    
    # Initial 3-coloring of cycle
    coloring = {0: 0, 1: 1, 2: 0, 3: 1, 4: 0, 5: 1}
    
    print("Initial coloring:", coloring)
    
    # Find Kempe chain with colors 0 and 1 starting from vertex 0
    chain = find_kempe_chain(G, coloring, 0, 0, 1)
    print(f"Kempe chain (colors 0,1) from vertex 0: {chain}")
    
    # Swap colors in the chain
    new_coloring = swap_kempe_chain(coloring, chain, 0, 1)
    print("After swap:", new_coloring)
    
    # Verify coloring is still valid
    valid = all(new_coloring[u] != new_coloring[v] for u, v in G.edges())
    print(f"Coloring still valid: {valid}")

demonstrate_kempe_chain()
```

---

## The Appel-Haken Computer-Assisted Proof

### Overview

In 1976, **Kenneth Appel** and **Wolfgang Haken** proved the Four Color Theorem using a combination of mathematical reasoning and computer verification. This was the **first major theorem to require computer assistance**.

### Proof Structure

The proof proceeds by **contradiction**:

1. **Assume** a minimal counterexample $G$ exists (smallest planar graph not 4-colorable)
2. **Discharging** shows $G$ must contain one of ~1,500 specific configurations
3. **Reducibility** shows each configuration cannot appear in a minimal counterexample
4. **Contradiction**: $G$ cannot exist

### Step 1: The Discharging Method

Assign initial "charges" to vertices and faces, then redistribute according to specific rules.

```python
def initial_charge(G):
    """
    Assign initial charges to vertices of a planar graph.
    
    Standard assignment: charge(v) = 6 - degree(v)
    
    By Euler's formula, for a planar graph:
    sum of charges = 6V - 2E = 6V - 2E
    
    Using E <= 3V - 6: sum >= 6V - 2(3V-6) = 12
    
    So total charge is always positive (= 12 for maximal planar graphs).
    """
    charges = {}
    for v in G.nodes():
        charges[v] = 6 - G.degree(v)
    return charges


def simple_discharging_rules(G, charges):
    """
    Apply simple discharging rules.
    
    Example rule: Vertices of degree >= 7 send charge to neighbors of degree <= 5.
    
    The key property: discharging preserves total charge.
    """
    new_charges = charges.copy()
    
    for v in G.nodes():
        if G.degree(v) >= 7:
            # This vertex has negative charge, send some to low-degree neighbors
            low_degree_neighbors = [n for n in G.neighbors(v) if G.degree(n) <= 5]
            
            if low_degree_neighbors:
                # Send charge equally to low-degree neighbors
                charge_to_send = min(1, -charges[v] / len(low_degree_neighbors))
                
                for n in low_degree_neighbors:
                    new_charges[n] += charge_to_send
                    new_charges[v] -= charge_to_send
    
    return new_charges


def demonstrate_discharging():
    """
    Demonstrate the discharging procedure on a planar graph.
    """
    # Create a planar graph
    G = nx.dodecahedral_graph()
    
    initial = initial_charge(G)
    total_initial = sum(initial.values())
    
    print(f"Total initial charge: {total_initial}")
    print(f"Positive charge vertices: {sum(1 for c in initial.values() if c > 0)}")
    print(f"Negative charge vertices: {sum(1 for c in initial.values() if c < 0)}")
    print(f"Zero charge vertices: {sum(1 for c in initial.values() if c == 0)}")
    
    # The dodecahedral graph is 3-regular, so all vertices have charge 6-3=3
    print(f"\nDegree distribution: {dict(G.degree())}")
    print(f"All charges: {set(initial.values())}")

demonstrate_discharging()
```

### Step 2: Unavoidable Sets

An **unavoidable set** is a collection of configurations such that every planar graph must contain at least one.

```python
def check_configuration(G, config_type):
    """
    Check if a graph contains specific configurations.
    
    Common reducible configurations include:
    - Vertices of degree <= 4
    - Certain arrangements of degree-5 vertices
    
    Parameters:
    -----------
    G : networkx.Graph
        The graph to check
    config_type : str
        Type of configuration to look for
        
    Returns:
    --------
    found : list
        List of vertices/subgraphs matching the configuration
    """
    found = []
    
    if config_type == "degree_4_or_less":
        # Vertices of degree 4 or less
        for v in G.nodes():
            if G.degree(v) <= 4:
                found.append(v)
                
    elif config_type == "degree_5_adjacent_to_degree_5":
        # Degree-5 vertices with a degree-5 neighbor
        for v in G.nodes():
            if G.degree(v) == 5:
                for n in G.neighbors(v):
                    if G.degree(n) == 5:
                        found.append((v, n))
                        
    elif config_type == "birkhoff_diamond":
        # The Birkhoff diamond: a specific reducible configuration
        # (simplified check - actual check is more complex)
        for v in G.nodes():
            if G.degree(v) == 4:
                neighbors = list(G.neighbors(v))
                # Check if exactly 2 pairs of neighbors are adjacent
                adj_count = sum(1 for i in range(4) for j in range(i+1, 4) 
                               if G.has_edge(neighbors[i], neighbors[j]))
                if adj_count == 2:
                    found.append(v)
    
    return found


def check_unavoidability():
    """
    Demonstrate that certain configurations are unavoidable in planar graphs.
    """
    # Every planar graph must have a vertex of degree <= 5
    test_graphs = [
        ("Complete K4", nx.complete_graph(4)),
        ("Dodecahedral", nx.dodecahedral_graph()),
        ("Icosahedral", nx.icosahedral_graph()),
        ("Octahedral", nx.octahedral_graph()),
    ]
    
    print("Checking for low-degree vertices (unavoidable in planar graphs):")
    print("-" * 60)
    
    for name, G in test_graphs:
        if nx.check_planarity(G)[0]:
            degrees = dict(G.degree())
            min_deg = min(degrees.values())
            low_deg_count = sum(1 for d in degrees.values() if d <= 5)
            print(f"{name}: min_degree={min_deg}, vertices with deg<=5: {low_deg_count}")

check_unavoidability()
```

### Step 3: Reducibility Testing

A configuration is **reducible** if any graph containing it cannot be a minimal counterexample.

```python
def test_reducibility_simple(G, v):
    """
    Test if removing a vertex makes the graph easier to color.
    
    A configuration around vertex v is reducible if:
    1. Remove v and its incident edges
    2. Any 4-coloring of the remaining graph can be extended to include v
    
    For vertices of degree <= 3, this is trivially true (at most 3 neighbors,
    so at least one color is available).
    
    Parameters:
    -----------
    G : networkx.Graph
        The graph
    v : vertex
        The vertex to test
        
    Returns:
    --------
    is_reducible : bool
        Whether the configuration is trivially reducible
    reason : str
        Explanation of the result
    """
    degree = G.degree(v)
    
    if degree <= 3:
        return True, f"Degree {degree} <= 3: at most 3 neighbors, always a free color"
    
    if degree == 4:
        # Degree 4 is reducible via Kempe chain argument
        return True, "Degree 4: reducible via Kempe chain argument"
    
    if degree == 5:
        # Degree 5 requires checking neighbor relationships
        neighbors = list(G.neighbors(v))
        
        # Check if any two non-adjacent neighbors exist
        non_adjacent_pairs = []
        for i in range(len(neighbors)):
            for j in range(i + 1, len(neighbors)):
                if not G.has_edge(neighbors[i], neighbors[j]):
                    non_adjacent_pairs.append((neighbors[i], neighbors[j]))
        
        if non_adjacent_pairs:
            return True, f"Degree 5 with non-adjacent neighbor pairs: {len(non_adjacent_pairs)} pairs"
        else:
            return False, "Degree 5 with all neighbors mutually adjacent: need deeper analysis"
    
    return False, f"Degree {degree} >= 6: requires case analysis"


def analyze_graph_reducibility(G):
    """
    Analyze reducibility of all vertices in a graph.
    """
    print("Reducibility Analysis")
    print("=" * 50)
    
    for v in sorted(G.nodes()):
        is_reducible, reason = test_reducibility_simple(G, v)
        status = "REDUCIBLE" if is_reducible else "COMPLEX"
        print(f"Vertex {v}: {status} - {reason}")

# Example
G = nx.petersen_graph()  # 3-regular graph
H = nx.dodecahedral_graph()  # Also 3-regular

print("Analyzing Dodecahedral Graph (first 5 vertices):")
for v in list(H.nodes())[:5]:
    is_red, reason = test_reducibility_simple(H, v)
    print(f"  Vertex {v}: {reason}")
```

### Computational Requirements

The original Appel-Haken proof required:

- **1,476 configurations** (later 1,936 in the 1989 revision)
- **487 discharging rules**
- **~1,200 hours** of computer time (1970s hardware)

```python
def estimate_verification_complexity():
    """
    Estimate the computational complexity of verifying reducibility.
    
    For each configuration:
    - Need to check all possible colorings of the boundary
    - For a ring of size k, there are roughly 4^k possible colorings
    - Must verify each can extend to the interior
    """
    
    # Appel-Haken parameters
    num_configurations = 1476  # original count
    avg_ring_size = 14  # average boundary ring size
    
    # Number of colorings to check per configuration
    colorings_per_config = 4 ** avg_ring_size
    
    # Total verifications (simplified estimate)
    total_checks = num_configurations * colorings_per_config
    
    print("Appel-Haken Proof Complexity Estimate")
    print("=" * 50)
    print(f"Number of configurations: {num_configurations}")
    print(f"Average ring size: {avg_ring_size}")
    print(f"Colorings per configuration: {colorings_per_config:,}")
    print(f"Total verification checks: {total_checks:,.0f}")
    print(f"")
    print("Note: Actual verification uses Kempe chain arguments")
    print("to reduce the effective search space significantly.")

estimate_verification_complexity()
```

---

## Modern Developments

### Robertson-Sanders-Seymour-Thomas (1997)

The RSST proof simplified the Appel-Haken proof significantly:

| Aspect | Appel-Haken (1976) | RSST (1997) |
|--------|-------------------|-------------|
| Configurations | 1,476 | **633** |
| Discharging rules | 487 | **32** |
| Computer time | ~1,200 hours | ~3 hours |

```python
def compare_proof_versions():
    """
    Compare the two main computer-assisted proofs.
    """
    proofs = {
        'Appel-Haken (1976)': {
            'configurations': 1476,
            'discharging_rules': 487,
            'max_ring_size': 14,
            'computer_hours': 1200,
        },
        'RSST (1997)': {
            'configurations': 633,
            'discharging_rules': 32,
            'max_ring_size': 14,
            'computer_hours': 3,
        }
    }
    
    print("Comparison of Four Color Theorem Proofs")
    print("=" * 60)
    
    for name, stats in proofs.items():
        print(f"\n{name}:")
        for key, value in stats.items():
            print(f"  {key.replace('_', ' ').title()}: {value:,}")
    
    # Calculate improvements
    ah = proofs['Appel-Haken (1976)']
    rsst = proofs['RSST (1997)']
    
    print("\n" + "=" * 60)
    print("Improvements (RSST vs Appel-Haken):")
    print(f"  Configurations reduced by: {(1 - rsst['configurations']/ah['configurations'])*100:.1f}%")
    print(f"  Discharging rules reduced by: {(1 - rsst['discharging_rules']/ah['discharging_rules'])*100:.1f}%")
    print(f"  Computer time reduced by: {(1 - rsst['computer_hours']/ah['computer_hours'])*100:.1f}%")

compare_proof_versions()
```

### Formal Verification (Gonthier, 2005)

**Georges Gonthier** used the **Coq proof assistant** to create a fully machine-verified proof:

- Every logical step is checked by the computer
- Eliminates concerns about bugs in the verification code
- The proof is a **certificate** that can be independently verified

```python
def formal_verification_overview():
    """
    Overview of the formal verification approach.
    """
    components = {
        'Coq Proof Assistant': 'Interactive theorem prover with dependent types',
        'SSReflect': 'Coq extension for small-scale reflection proofs',
        'Four Color Library': 'Formalization of graph theory and the proof',
        'Verification': 'Machine checks every logical inference',
    }
    
    print("Gonthier's Formal Verification (2005)")
    print("=" * 60)
    
    for component, description in components.items():
        print(f"\n{component}:")
        print(f"  {description}")
    
    print("\n" + "=" * 60)
    print("Key Achievement:")
    print("  The proof is now a mathematical OBJECT that can be")
    print("  mechanically verified, eliminating concerns about")
    print("  programming bugs or human error in case analysis.")

formal_verification_overview()
```

---

## Implementation Examples

### Complete Graph Coloring Algorithm

```python
def greedy_coloring(G):
    """
    Greedy graph coloring algorithm.
    
    Uses the Welsh-Powell algorithm:
    1. Order vertices by decreasing degree
    2. Assign colors greedily in that order
    
    This doesn't guarantee optimal coloring but is efficient.
    """
    # Sort vertices by degree (highest first)
    vertices = sorted(G.nodes(), key=lambda v: G.degree(v), reverse=True)
    
    coloring = {}
    
    for v in vertices:
        # Colors used by neighbors
        neighbor_colors = {coloring[n] for n in G.neighbors(v) if n in coloring}
        
        # Find smallest available color
        color = 0
        while color in neighbor_colors:
            color += 1
        
        coloring[v] = color
    
    return coloring


def dsatur_coloring(G):
    """
    DSATUR (Degree of Saturation) algorithm for graph coloring.
    
    Saturation degree = number of different colors in a vertex's neighborhood.
    
    Algorithm:
    1. Start with vertex of highest degree
    2. Always color the vertex with highest saturation degree
    3. Break ties by choosing highest degree vertex
    
    This often produces better results than greedy for planar graphs.
    """
    coloring = {}
    saturation = {v: 0 for v in G.nodes()}
    
    # Track which colors each vertex's neighbors use
    neighbor_colors = {v: set() for v in G.nodes()}
    
    while len(coloring) < G.number_of_nodes():
        # Find uncolored vertex with highest saturation
        uncolored = [v for v in G.nodes() if v not in coloring]
        
        # Sort by saturation (desc), then by degree (desc)
        next_vertex = max(uncolored, key=lambda v: (saturation[v], G.degree(v)))
        
        # Find smallest available color
        used_colors = neighbor_colors[next_vertex]
        color = 0
        while color in used_colors:
            color += 1
        
        # Assign color
        coloring[next_vertex] = color
        
        # Update saturation for neighbors
        for neighbor in G.neighbors(next_vertex):
            if neighbor not in coloring:
                if color not in neighbor_colors[neighbor]:
                    neighbor_colors[neighbor].add(color)
                    saturation[neighbor] += 1
    
    return coloring


def verify_four_coloring(G):
    """
    Verify that a planar graph can be 4-colored.
    
    Uses DSATUR which typically finds optimal or near-optimal colorings.
    """
    if not nx.check_planarity(G)[0]:
        return None, "Graph is not planar"
    
    coloring = dsatur_coloring(G)
    num_colors = len(set(coloring.values()))
    
    # Verify coloring is valid
    for u, v in G.edges():
        if coloring[u] == coloring[v]:
            return None, f"Invalid coloring: edge ({u}, {v}) has same color"
    
    return coloring, f"Successfully colored with {num_colors} colors"


# Test on various planar graphs
test_graphs = [
    ("Cycle C6", nx.cycle_graph(6)),
    ("Complete K4", nx.complete_graph(4)),
    ("Petersen (non-planar)", nx.petersen_graph()),
    ("Dodecahedral", nx.dodecahedral_graph()),
    ("Icosahedral", nx.icosahedral_graph()),
    ("Grid 4x4", nx.grid_2d_graph(4, 4)),
]

print("Four-Coloring Verification Results")
print("=" * 60)

for name, G in test_graphs:
    coloring, message = verify_four_coloring(G)
    is_planar = "planar" if nx.check_planarity(G)[0] else "non-planar"
    print(f"{name} ({is_planar}): {message}")
```

### Visualizing Graph Colorings

```python
def visualize_coloring(G, coloring, title="Graph Coloring"):
    """
    Visualize a graph with its coloring.
    
    Parameters:
    -----------
    G : networkx.Graph
        The graph
    coloring : dict
        Vertex coloring (vertex -> color_index)
    title : str
        Plot title
    """
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    
    # Color palette (colorblind-friendly)
    colors = ['#e41a1c', '#377eb8', '#4daf4a', '#984ea3', 
              '#ff7f00', '#ffff33', '#a65628', '#f781bf']
    
    # Map color indices to actual colors
    node_colors = [colors[coloring[v] % len(colors)] for v in G.nodes()]
    
    # Create layout
    if nx.check_planarity(G)[0]:
        # Use planar layout if possible
        pos = nx.planar_layout(G)
    else:
        pos = nx.spring_layout(G, seed=42)
    
    # Draw graph
    plt.figure(figsize=(10, 8))
    
    nx.draw(G, pos, 
            node_color=node_colors,
            node_size=500,
            with_labels=True,
            font_size=10,
            font_weight='bold',
            edge_color='gray',
            width=1.5)
    
    # Add legend
    unique_colors = sorted(set(coloring.values()))
    patches = [mpatches.Patch(color=colors[c], label=f'Color {c}') 
               for c in unique_colors]
    plt.legend(handles=patches, loc='upper left')
    
    plt.title(f"{title}\n(Using {len(unique_colors)} colors)")
    plt.axis('off')
    plt.tight_layout()
    plt.savefig('graph_coloring_example.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    return 'graph_coloring_example.png'

# Example usage (requires matplotlib)
# G = nx.dodecahedral_graph()
# coloring = dsatur_coloring(G)
# visualize_coloring(G, coloring, "Dodecahedral Graph")
```

### Complete Working Example

```python
"""
Complete example: Four Color Theorem demonstration

This script demonstrates the key concepts of the Four Color Theorem
including graph creation, planarity testing, and coloring algorithms.
"""

import networkx as nx
from collections import Counter

def main():
    print("=" * 70)
    print("FOUR COLOR THEOREM - DEMONSTRATION")
    print("=" * 70)
    
    # 1. Create a planar graph (map of regions)
    print("\n1. Creating a planar graph from map adjacencies...")
    
    # Example: Simplified map of some US states
    state_adjacencies = {
        'WA': ['OR', 'ID'],
        'OR': ['WA', 'ID', 'NV', 'CA'],
        'CA': ['OR', 'NV', 'AZ'],
        'ID': ['WA', 'OR', 'NV', 'UT', 'MT', 'WY'],
        'NV': ['OR', 'CA', 'AZ', 'UT', 'ID'],
        'AZ': ['CA', 'NV', 'UT', 'NM'],
        'UT': ['ID', 'NV', 'AZ', 'NM', 'CO', 'WY'],
        'MT': ['ID', 'WY', 'ND', 'SD'],
        'WY': ['MT', 'ID', 'UT', 'CO', 'NE', 'SD'],
        'CO': ['WY', 'UT', 'NM', 'OK', 'KS', 'NE'],
        'NM': ['AZ', 'UT', 'CO', 'OK', 'TX'],
        'ND': ['MT', 'SD', 'MN'],
        'SD': ['ND', 'MT', 'WY', 'NE', 'IA', 'MN'],
        'NE': ['SD', 'WY', 'CO', 'KS', 'MO', 'IA'],
        'KS': ['NE', 'CO', 'OK', 'MO'],
        'OK': ['KS', 'CO', 'NM', 'TX', 'AR', 'MO'],
        'TX': ['NM', 'OK', 'AR', 'LA'],
        'MN': ['ND', 'SD', 'IA', 'WI'],
        'IA': ['MN', 'SD', 'NE', 'MO', 'IL', 'WI'],
        'MO': ['IA', 'NE', 'KS', 'OK', 'AR', 'TN', 'KY', 'IL'],
        'AR': ['MO', 'OK', 'TX', 'LA', 'MS', 'TN'],
        'LA': ['TX', 'AR', 'MS'],
        'WI': ['MN', 'IA', 'IL', 'MI'],
        'IL': ['WI', 'IA', 'MO', 'KY', 'IN'],
        'MI': ['WI', 'IN', 'OH'],
        'IN': ['MI', 'IL', 'KY', 'OH'],
        'OH': ['MI', 'IN', 'KY', 'WV', 'PA'],
        'KY': ['OH', 'IN', 'IL', 'MO', 'TN', 'VA', 'WV'],
        'TN': ['KY', 'MO', 'AR', 'MS', 'AL', 'GA', 'NC', 'VA'],
        'MS': ['TN', 'AR', 'LA', 'AL'],
        'AL': ['MS', 'TN', 'GA', 'FL'],
        'GA': ['AL', 'TN', 'NC', 'SC', 'FL'],
        'FL': ['AL', 'GA'],
        'NC': ['TN', 'VA', 'SC', 'GA'],
        'SC': ['NC', 'GA'],
        'VA': ['KY', 'TN', 'NC', 'WV', 'MD', 'DC'],
        'WV': ['OH', 'KY', 'VA', 'MD', 'PA'],
        'PA': ['OH', 'WV', 'MD', 'DE', 'NJ', 'NY'],
        'MD': ['VA', 'WV', 'PA', 'DE', 'DC'],
        'DE': ['MD', 'PA', 'NJ'],
        'NJ': ['PA', 'DE', 'NY'],
        'NY': ['PA', 'NJ', 'CT', 'MA', 'VT'],
        'CT': ['NY', 'MA', 'RI'],
        'RI': ['CT', 'MA'],
        'MA': ['NY', 'CT', 'RI', 'VT', 'NH'],
        'VT': ['NY', 'MA', 'NH'],
        'NH': ['VT', 'MA', 'ME'],
        'ME': ['NH'],
        'DC': ['VA', 'MD'],
    }
    
    # Build graph
    G = nx.Graph()
    for state, neighbors in state_adjacencies.items():
        for neighbor in neighbors:
            G.add_edge(state, neighbor)
    
    print(f"   States (vertices): {G.number_of_nodes()}")
    print(f"   Borders (edges): {G.number_of_edges()}")
    
    # 2. Check planarity
    print("\n2. Checking planarity...")
    is_planar, _ = nx.check_planarity(G)
    print(f"   Graph is planar: {is_planar}")
    
    # 3. Verify Euler's formula bounds
    print("\n3. Verifying Euler's formula constraints...")
    V, E = G.number_of_nodes(), G.number_of_edges()
    edge_bound = 3 * V - 6
    print(f"   V = {V}, E = {E}")
    print(f"   Edge bound (3V - 6) = {edge_bound}")
    print(f"   E <= 3V - 6: {E <= edge_bound}")
    
    # 4. Find minimum degree vertex (guaranteed <= 5 for planar)
    print("\n4. Degree analysis...")
    degrees = dict(G.degree())
    min_deg = min(degrees.values())
    max_deg = max(degrees.values())
    min_deg_vertices = [v for v, d in degrees.items() if d == min_deg]
    print(f"   Minimum degree: {min_deg}")
    print(f"   Maximum degree: {max_deg}")
    print(f"   Vertices with min degree: {min_deg_vertices[:5]}...")
    
    # 5. Apply DSATUR coloring
    print("\n5. Applying DSATUR coloring algorithm...")
    
    coloring = {}
    saturation = {v: 0 for v in G.nodes()}
    neighbor_colors = {v: set() for v in G.nodes()}
    
    while len(coloring) < G.number_of_nodes():
        uncolored = [v for v in G.nodes() if v not in coloring]
        next_vertex = max(uncolored, key=lambda v: (saturation[v], G.degree(v)))
        
        used_colors = neighbor_colors[next_vertex]
        color = 0
        while color in used_colors:
            color += 1
        
        coloring[next_vertex] = color
        
        for neighbor in G.neighbors(next_vertex):
            if neighbor not in coloring:
                if color not in neighbor_colors[neighbor]:
                    neighbor_colors[neighbor].add(color)
                    saturation[neighbor] += 1
    
    # 6. Analyze results
    print("\n6. Coloring results...")
    num_colors = len(set(coloring.values()))
    color_counts = Counter(coloring.values())
    
    print(f"   Colors used: {num_colors}")
    print(f"   Color distribution: {dict(color_counts)}")
    
    # Verify coloring
    valid = all(coloring[u] != coloring[v] for u, v in G.edges())
    print(f"   Coloring is valid: {valid}")
    
    # 7. Show sample coloring
    print("\n7. Sample state colorings (Color names: Red=0, Blue=1, Green=2, Yellow=3):")
    color_names = {0: 'Red', 1: 'Blue', 2: 'Green', 3: 'Yellow'}
    sample_states = ['CA', 'TX', 'NY', 'FL', 'IL', 'PA', 'OH', 'MI']
    for state in sample_states:
        if state in coloring:
            c = coloring[state]
            print(f"   {state}: {color_names.get(c, f'Color {c}')}")
    
    print("\n" + "=" * 70)
    print("FOUR COLOR THEOREM VERIFIED FOR US STATE MAP")
    print(f"All {V} states colored with {num_colors} colors!")
    print("=" * 70)
    
    return coloring

if __name__ == "__main__":
    coloring = main()
```

---

## Summary and Key Takeaways

### The Theorem

$$\boxed{\text{Every planar graph } G \text{ satisfies } \chi(G) \leq 4}$$

### Key Concepts

| Concept | Description |
|---------|-------------|
| **Planar Graph** | Embeddable in plane without crossings |
| **Chromatic Number** | Minimum colors for proper vertex coloring |
| **Kempe Chain** | Maximal 2-colored connected subgraph |
| **Reducibility** | Configuration cannot be in minimal counterexample |
| **Unavoidability** | Every planar graph contains some configuration |
| **Discharging** | Charge redistribution proving unavoidability |

### Historical Significance

1. **First major computer-assisted proof** (1976)
2. **Sparked debate** about the nature of mathematical proof
3. **Fully formalized** in Coq (2005), providing machine verification
4. **Remains the only known proof method** - no human-checkable proof exists

### Practical Applications

- **Map coloring** (the original motivation)
- **Register allocation** in compilers
- **Frequency assignment** in wireless networks
- **Scheduling problems** with conflict constraints

---

*Document generated for Agent 1007 Problem Set*  
*Graph Colouring Project*
