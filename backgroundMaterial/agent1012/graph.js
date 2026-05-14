/* ========================================================
   graph.js — Graph data structures, algorithms & canvas drawing
   Agent 1012 — Four Colour Theorem Interactive Demo
   ======================================================== */

const COLOURS = ['#e74c3c', '#3498db', '#2ecc71', '#f1c40f'];
const COLOUR_NAMES = ['Red', 'Blue', 'Green', 'Yellow'];
const COLOUR_DIM = ['#a93226', '#2171a6', '#1f9c52', '#c9a30a'];
const HIGHLIGHT_STROKE = '#fff';
const NODE_RADIUS = 18;

/* --------------------------------------------------
   Graph Class
   -------------------------------------------------- */
class Graph {
  constructor() {
    this.nodes = {};   // id -> { x, y, colour, label, ... }
    this.edges = [];   // [{ from, to }]
    this.adj = {};     // id -> Set(ids)
  }

  addNode(id, x, y, label) {
    this.nodes[id] = { x, y, colour: -1, label: label || id, highlight: false };
    this.adj[id] = this.adj[id] || new Set();
  }

  addEdge(a, b) {
    if (!this.adj[a]) this.adj[a] = new Set();
    if (!this.adj[b]) this.adj[b] = new Set();
    if (this.adj[a].has(b)) return;
    this.adj[a].add(b);
    this.adj[b].add(a);
    this.edges.push({ from: a, to: b });
  }

  degree(id) {
    return this.adj[id] ? this.adj[id].size : 0;
  }

  neighbors(id) {
    return this.adj[id] ? [...this.adj[id]] : [];
  }

  nodeIds() {
    return Object.keys(this.nodes);
  }

  nodeCount() {
    return Object.keys(this.nodes).length;
  }

  edgeCount() {
    return this.edges.length;
  }

  clearColours() {
    for (const id of this.nodeIds()) this.nodes[id].colour = -1;
  }

  clearHighlights() {
    for (const id of this.nodeIds()) this.nodes[id].highlight = false;
  }

  isValidColouring() {
    for (const { from, to } of this.edges) {
      const c1 = this.nodes[from].colour;
      const c2 = this.nodes[to].colour;
      if (c1 >= 0 && c2 >= 0 && c1 === c2) return false;
    }
    return true;
  }

  isComplete() {
    return this.nodeIds().every(id => this.nodes[id].colour >= 0);
  }

  coloursUsed() {
    const s = new Set();
    for (const id of this.nodeIds()) {
      if (this.nodes[id].colour >= 0) s.add(this.nodes[id].colour);
    }
    return s.size;
  }

  clone() {
    const g = new Graph();
    for (const id of this.nodeIds()) {
      const n = this.nodes[id];
      g.addNode(id, n.x, n.y, n.label);
      g.nodes[id].colour = n.colour;
    }
    for (const e of this.edges) g.addEdge(e.from, e.to);
    return g;
  }

  nodeAt(x, y, radius) {
    radius = radius || NODE_RADIUS;
    for (const id of this.nodeIds()) {
      const n = this.nodes[id];
      const dx = n.x - x;
      const dy = n.y - y;
      if (dx * dx + dy * dy <= radius * radius) return id;
    }
    return null;
  }
}

/* --------------------------------------------------
   Graph factories
   -------------------------------------------------- */
const GraphFactory = {
  cycle(n, cx, cy, r) {
    const g = new Graph();
    for (let i = 0; i < n; i++) {
      const angle = (2 * Math.PI * i) / n - Math.PI / 2;
      g.addNode(String(i), cx + r * Math.cos(angle), cy + r * Math.sin(angle), String(i));
    }
    for (let i = 0; i < n; i++) g.addEdge(String(i), String((i + 1) % n));
    return g;
  },

  complete(n, cx, cy, r) {
    const g = new Graph();
    for (let i = 0; i < n; i++) {
      const angle = (2 * Math.PI * i) / n - Math.PI / 2;
      g.addNode(String(i), cx + r * Math.cos(angle), cy + r * Math.sin(angle), String(i));
    }
    for (let i = 0; i < n; i++)
      for (let j = i + 1; j < n; j++)
        g.addEdge(String(i), String(j));
    return g;
  },

  bipartite(m, n, cx, cy, w, h) {
    const g = new Graph();
    for (let i = 0; i < m; i++) {
      const x = cx - w / 2 + (w / (m + 1)) * (i + 1);
      g.addNode('a' + i, x, cy - h / 2, 'a' + i);
    }
    for (let j = 0; j < n; j++) {
      const x = cx - w / 2 + (w / (n + 1)) * (j + 1);
      g.addNode('b' + j, x, cy + h / 2, 'b' + j);
    }
    for (let i = 0; i < m; i++)
      for (let j = 0; j < n; j++)
        g.addEdge('a' + i, 'b' + j);
    return g;
  },

  grid(rows, cols, cx, cy, spacing) {
    const g = new Graph();
    const ox = cx - ((cols - 1) * spacing) / 2;
    const oy = cy - ((rows - 1) * spacing) / 2;
    for (let r = 0; r < rows; r++) {
      for (let c = 0; c < cols; c++) {
        const id = `${r}_${c}`;
        g.addNode(id, ox + c * spacing, oy + r * spacing, `(${r},${c})`);
      }
    }
    for (let r = 0; r < rows; r++) {
      for (let c = 0; c < cols; c++) {
        if (c + 1 < cols) g.addEdge(`${r}_${c}`, `${r}_${c + 1}`);
        if (r + 1 < rows) g.addEdge(`${r}_${c}`, `${r + 1}_${c}`);
      }
    }
    return g;
  },

  petersen(cx, cy, ro, ri) {
    const g = new Graph();
    for (let i = 0; i < 5; i++) {
      const a = (2 * Math.PI * i) / 5 - Math.PI / 2;
      g.addNode('o' + i, cx + ro * Math.cos(a), cy + ro * Math.sin(a), String(i));
      g.addNode('i' + i, cx + ri * Math.cos(a), cy + ri * Math.sin(a), String(i + 5));
    }
    for (let i = 0; i < 5; i++) {
      g.addEdge('o' + i, 'o' + ((i + 1) % 5));
      g.addEdge('o' + i, 'i' + i);
      g.addEdge('i' + i, 'i' + ((i + 2) % 5));
    }
    return g;
  },

  dodecahedron(cx, cy, r) {
    const g = new Graph();
    const rings = [
      { count: 5, radius: r * 0.35, offset: -Math.PI / 2 },
      { count: 5, radius: r * 0.7, offset: -Math.PI / 2 + Math.PI / 5 },
      { count: 5, radius: r * 0.9, offset: -Math.PI / 2 + 2 * Math.PI / 5 },
      { count: 5, radius: r, offset: -Math.PI / 2 + 3 * Math.PI / 5 },
    ];
    let id = 0;
    const ids = [];
    for (const ring of rings) {
      const ringIds = [];
      for (let i = 0; i < ring.count; i++) {
        const a = ring.offset + (2 * Math.PI * i) / ring.count;
        const nid = String(id);
        g.addNode(nid, cx + ring.radius * Math.cos(a), cy + ring.radius * Math.sin(a), nid);
        ringIds.push(nid);
        id++;
      }
      ids.push(ringIds);
    }
    for (let i = 0; i < 5; i++) {
      g.addEdge(ids[0][i], ids[0][(i + 1) % 5]);
      g.addEdge(ids[0][i], ids[1][i]);
      g.addEdge(ids[1][i], ids[2][i]);
      g.addEdge(ids[1][i], ids[2][(i + 4) % 5]);
      g.addEdge(ids[2][i], ids[3][i]);
      g.addEdge(ids[3][i], ids[3][(i + 1) % 5]);
    }
    return g;
  },

  usaWestern(cx, cy, scale) {
    const g = new Graph();
    const states = {
      WA: [0.15, 0.05], OR: [0.15, 0.25], CA: [0.08, 0.55],
      ID: [0.32, 0.15], NV: [0.22, 0.45], AZ: [0.32, 0.7],
      UT: [0.42, 0.45], MT: [0.52, 0.08], WY: [0.52, 0.28],
      CO: [0.55, 0.50], NM: [0.50, 0.72], ND: [0.72, 0.05],
      SD: [0.72, 0.22], NE: [0.72, 0.40], KS: [0.72, 0.55],
      OK: [0.72, 0.72], TX: [0.65, 0.88],
    };
    for (const [s, [x, y]] of Object.entries(states)) {
      g.addNode(s, cx - scale / 2 + x * scale, cy - scale / 2 + y * scale, s);
    }
    const borders = [
      ['WA', 'OR'], ['WA', 'ID'], ['OR', 'ID'], ['OR', 'NV'], ['OR', 'CA'],
      ['CA', 'NV'], ['CA', 'AZ'], ['ID', 'NV'], ['ID', 'UT'], ['ID', 'MT'],
      ['ID', 'WY'], ['NV', 'AZ'], ['NV', 'UT'], ['AZ', 'UT'], ['AZ', 'NM'],
      ['UT', 'NM'], ['UT', 'CO'], ['UT', 'WY'], ['MT', 'WY'], ['MT', 'ND'],
      ['MT', 'SD'], ['WY', 'CO'], ['WY', 'NE'], ['WY', 'SD'], ['CO', 'NM'],
      ['CO', 'OK'], ['CO', 'KS'], ['CO', 'NE'], ['NM', 'OK'], ['NM', 'TX'],
      ['ND', 'SD'], ['SD', 'NE'], ['NE', 'KS'], ['KS', 'OK'], ['OK', 'TX'],
    ];
    for (const [a, b] of borders) g.addEdge(a, b);
    return g;
  },

  simpleMap(cx, cy, r) {
    const g = new Graph();
    const positions = {
      A: [cx, cy - r * 0.7],
      B: [cx - r * 0.8, cy - r * 0.1],
      C: [cx + r * 0.8, cy - r * 0.1],
      D: [cx - r * 0.5, cy + r * 0.6],
      E: [cx + r * 0.5, cy + r * 0.6],
      F: [cx, cy + r * 0.15],
    };
    for (const [id, [x, y]] of Object.entries(positions)) {
      g.addNode(id, x, y, id);
    }
    g.addEdge('A', 'B'); g.addEdge('A', 'C'); g.addEdge('A', 'F');
    g.addEdge('B', 'D'); g.addEdge('B', 'F');
    g.addEdge('C', 'E'); g.addEdge('C', 'F');
    g.addEdge('D', 'E'); g.addEdge('D', 'F');
    g.addEdge('E', 'F');
    return g;
  },

  platonic(type, cx, cy, r) {
    if (type === 'tetrahedron') return GraphFactory.complete(4, cx, cy, r);
    if (type === 'cube') {
      const g = new Graph();
      const s = r * 0.55;
      const offsets = [
        [-s, -s], [s, -s], [s, s], [-s, s],
        [-s * 0.5, -s * 0.5], [s * 0.5, -s * 0.5], [s * 0.5, s * 0.5], [-s * 0.5, s * 0.5]
      ];
      for (let i = 0; i < 8; i++) {
        g.addNode(String(i), cx + offsets[i][0], cy + offsets[i][1], String(i));
      }
      [['0','1'],['1','2'],['2','3'],['3','0'],
       ['4','5'],['5','6'],['6','7'],['7','4'],
       ['0','4'],['1','5'],['2','6'],['3','7']].forEach(([a, b]) => g.addEdge(a, b));
      return g;
    }
    if (type === 'octahedron') {
      const g = new Graph();
      const pts = [[0, -r], [-r * 0.8, 0], [r * 0.8, 0], [0, r], [-r * 0.4, -r * 0.1], [r * 0.4, -r * 0.1]];
      for (let i = 0; i < 6; i++) g.addNode(String(i), cx + pts[i][0], cy + pts[i][1], String(i));
      [[0,1],[0,2],[0,4],[0,5],[1,3],[1,4],[1,5],[2,3],[2,4],[2,5],[3,4],[3,5]].forEach(([a,b])=> g.addEdge(String(a),String(b)));
      return g;
    }
    if (type === 'dodecahedron') return GraphFactory.dodecahedron(cx, cy, r);
    if (type === 'icosahedron') {
      const g = new Graph();
      for (let i = 0; i < 12; i++) {
        const a = (2 * Math.PI * i) / 12 - Math.PI / 2;
        const rad = (i < 6) ? r * 0.5 : r;
        g.addNode(String(i), cx + rad * Math.cos(a), cy + rad * Math.sin(a), String(i));
      }
      const edges = [[0,1],[1,2],[2,3],[3,4],[4,5],[5,0],
        [0,6],[0,7],[1,7],[1,8],[2,8],[2,9],[3,9],[3,10],[4,10],[4,11],[5,11],[5,6],
        [6,7],[7,8],[8,9],[9,10],[10,11],[11,6]];
      edges.forEach(([a,b]) => g.addEdge(String(a), String(b)));
      return g;
    }
    return GraphFactory.complete(4, cx, cy, r);
  }
};

/* --------------------------------------------------
   Colouring algorithms
   -------------------------------------------------- */
const ColourAlgo = {
  greedy(graph) {
    const order = graph.nodeIds().sort((a, b) => graph.degree(b) - graph.degree(a));
    const steps = [];
    for (const v of order) {
      const used = new Set();
      for (const n of graph.neighbors(v)) {
        if (graph.nodes[n].colour >= 0) used.add(graph.nodes[n].colour);
      }
      let c = 0;
      while (used.has(c)) c++;
      graph.nodes[v].colour = c;
      steps.push({ vertex: v, colour: c, reason: `deg=${graph.degree(v)}, used=[${[...used]}]` });
    }
    return steps;
  },

  dsatur(graph) {
    const sat = {};
    const nCols = {};
    for (const id of graph.nodeIds()) {
      sat[id] = 0;
      nCols[id] = new Set();
    }
    const steps = [];
    const coloured = new Set();

    while (coloured.size < graph.nodeCount()) {
      let best = null;
      let bestSat = -1;
      let bestDeg = -1;
      for (const id of graph.nodeIds()) {
        if (coloured.has(id)) continue;
        const s = sat[id];
        const d = graph.degree(id);
        if (s > bestSat || (s === bestSat && d > bestDeg)) {
          best = id;
          bestSat = s;
          bestDeg = d;
        }
      }
      const used = nCols[best];
      let c = 0;
      while (used.has(c)) c++;
      graph.nodes[best].colour = c;
      coloured.add(best);
      steps.push({
        vertex: best,
        colour: c,
        saturation: bestSat,
        reason: `sat=${bestSat}, deg=${graph.degree(best)}, used=[${[...used]}]`
      });

      for (const n of graph.neighbors(best)) {
        if (!coloured.has(n) && !nCols[n].has(c)) {
          nCols[n].add(c);
          sat[n]++;
        }
      }
    }
    return steps;
  },

  findKempeChain(graph, startId, c1, c2) {
    if (graph.nodes[startId].colour !== c1 && graph.nodes[startId].colour !== c2) return [];
    const chain = new Set();
    const stack = [startId];
    while (stack.length) {
      const v = stack.pop();
      if (chain.has(v)) continue;
      const vc = graph.nodes[v].colour;
      if (vc !== c1 && vc !== c2) continue;
      chain.add(v);
      for (const n of graph.neighbors(v)) {
        if (!chain.has(n)) {
          const nc = graph.nodes[n].colour;
          if (nc === c1 || nc === c2) stack.push(n);
        }
      }
    }
    return [...chain];
  },

  swapKempeChain(graph, chain, c1, c2) {
    for (const v of chain) {
      if (graph.nodes[v].colour === c1) graph.nodes[v].colour = c2;
      else if (graph.nodes[v].colour === c2) graph.nodes[v].colour = c1;
    }
  },

  initialCharges(graph) {
    const charges = {};
    for (const id of graph.nodeIds()) {
      charges[id] = 6 - graph.degree(id);
    }
    return charges;
  },

  discharge(graph, charges) {
    const newCharges = { ...charges };
    for (const v of graph.nodeIds()) {
      if (graph.degree(v) >= 7) {
        const lowNeighbors = graph.neighbors(v).filter(n => graph.degree(n) <= 5);
        if (lowNeighbors.length > 0) {
          const send = Math.min(1, Math.abs(charges[v]) / lowNeighbors.length);
          for (const n of lowNeighbors) {
            newCharges[n] += send;
            newCharges[v] -= send;
          }
        }
      }
    }
    return newCharges;
  }
};

/* --------------------------------------------------
   Canvas drawing utilities
   -------------------------------------------------- */
const DrawUtil = {
  clear(ctx, canvas) {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
  },

  drawEdge(ctx, x1, y1, x2, y2, colour, width) {
    ctx.beginPath();
    ctx.moveTo(x1, y1);
    ctx.lineTo(x2, y2);
    ctx.strokeStyle = colour || '#3a3f55';
    ctx.lineWidth = width || 1.5;
    ctx.stroke();
  },

  drawNode(ctx, x, y, radius, fillColour, strokeColour, label, labelColour) {
    ctx.beginPath();
    ctx.arc(x, y, radius, 0, 2 * Math.PI);
    ctx.fillStyle = fillColour || '#2e3347';
    ctx.fill();
    if (strokeColour) {
      ctx.strokeStyle = strokeColour;
      ctx.lineWidth = 2.5;
      ctx.stroke();
    }
    if (label !== undefined && label !== null) {
      ctx.fillStyle = labelColour || '#fff';
      ctx.font = `bold ${Math.max(10, radius * 0.65)}px sans-serif`;
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText(String(label), x, y + 1);
    }
  },

  drawGraph(ctx, canvas, graph, opts) {
    opts = opts || {};
    const nodeRadius = opts.nodeRadius || NODE_RADIUS;
    const showLabels = opts.showLabels !== false;
    const edgeColour = opts.edgeColour || '#3a3f55';
    const highlightEdges = opts.highlightEdges || [];
    const chargeMap = opts.charges || null;

    DrawUtil.clear(ctx, canvas);

    for (const e of graph.edges) {
      const a = graph.nodes[e.from];
      const b = graph.nodes[e.to];
      const isHL = highlightEdges.some(h =>
        (h[0] === e.from && h[1] === e.to) || (h[0] === e.to && h[1] === e.from)
      );
      DrawUtil.drawEdge(ctx, a.x, a.y, b.x, b.y,
        isHL ? '#f1c40f' : edgeColour,
        isHL ? 3 : 1.5
      );
    }

    for (const id of graph.nodeIds()) {
      const n = graph.nodes[id];
      let fill = n.colour >= 0 ? COLOURS[n.colour % COLOURS.length] : '#2e3347';
      let stroke = n.highlight ? HIGHLIGHT_STROKE : (n.colour >= 0 ? null : '#555');
      const lbl = showLabels ? n.label : null;
      DrawUtil.drawNode(ctx, n.x, n.y, nodeRadius, fill, stroke, lbl);

      if (chargeMap && chargeMap[id] !== undefined) {
        const ch = chargeMap[id];
        const cStr = ch >= 0 ? `+${ch.toFixed(1)}` : ch.toFixed(1);
        ctx.fillStyle = ch > 0 ? '#2ecc71' : (ch < 0 ? '#e74c3c' : '#888');
        ctx.font = 'bold 11px sans-serif';
        ctx.textAlign = 'center';
        ctx.fillText(cStr, n.x, n.y - nodeRadius - 6);
      }
    }
  },

  drawMapRegions(ctx, regions) {
    for (const r of regions) {
      ctx.beginPath();
      ctx.moveTo(r.path[0][0], r.path[0][1]);
      for (let i = 1; i < r.path.length; i++) ctx.lineTo(r.path[i][0], r.path[i][1]);
      ctx.closePath();
      ctx.fillStyle = r.colour >= 0 ? COLOURS[r.colour] : '#2e3347';
      ctx.fill();
      ctx.strokeStyle = '#555';
      ctx.lineWidth = 2;
      ctx.stroke();

      if (r.label) {
        ctx.fillStyle = '#fff';
        ctx.font = 'bold 14px sans-serif';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(r.label, r.cx, r.cy);
      }
    }
  }
};
