SageMath `graphs.KittellGraph` (develop `smallgraphs.py`) supplies the adjacency; its doctest states order $23$ and size $63$. `compute/kempe/a1720_k6_kittell.py` https://github.com/sagemath/sage/blob/develop/src/sage/graphs/generators/smallgraphs.py
MathWorld calls the Kittell graph planar on $23$ nodes and $63$ edges. `groups/K6_kittell.json` https://mathworld.wolfram.com/KittellGraph.html
That edge list is simple, connected, and planar, with $42$ faces, every face a triangle, and Euler characteristic $2$. `groups/K6_kittell.json`
Degrees: fifteen $5$s, five $6$s, three $7$s. Degree-$5$ vertices: $2,3,4,5,8,9,12,13,14,16,17,18,20,21,22$. `groups/K6_kittell.json`
KC5 at each of those $15$ vertices returns $0$ bad classes and one mixed Kempe class. `groups/K6_kittell.json`
Maximum Kempe distance to $|c(N(v))|\le 3$ is $4$, at vertices $9$ and $17$. `groups/K6_kittell.json`
Normalised $4$-colouring counts of $G-v$ run from $398$ to $508$. `groups/K6_kittell.json`
Structural check plus all $15$ vertices took $0.31$ s. `groups/K6_kittell.json`
