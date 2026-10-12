/* ========================================================
   animations.js — Interactive demo controllers for each tab
   Agent 1012 — Four Colour Theorem Interactive Demo
   ======================================================== */

/* --------------------------------------------------
   Tab 1: Intro Map colouring demo
   -------------------------------------------------- */
const IntroDemo = {
  canvas: null, ctx: null,
  regions: [],
  selectedColour: 0,
  adjacency: [],

  init() {
    this.canvas = document.getElementById('intro-map-canvas');
    if (!this.canvas) return;
    this.ctx = this.canvas.getContext('2d');
    this.buildRegions();
    this.draw();

    this.canvas.addEventListener('click', e => this.onClick(e));
    document.getElementById('intro-reset').addEventListener('click', () => this.reset());
    document.getElementById('intro-auto').addEventListener('click', () => this.autoColour());

    document.querySelectorAll('#tab-intro .colour-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        document.querySelectorAll('#tab-intro .colour-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        this.selectedColour = parseInt(btn.dataset.colour);
      });
    });
    document.querySelector('#tab-intro .colour-btn').classList.add('active');
  },

  buildRegions() {
    const w = this.canvas.width, h = this.canvas.height;
    this.regions = [
      { id: 'A', path: [[0,0],[w*0.5,0],[w*0.35,h*0.35],[0,h*0.3]], colour: -1, label: 'A', cx: w*0.2, cy: h*0.15 },
      { id: 'B', path: [[w*0.5,0],[w,0],[w,h*0.3],[w*0.65,h*0.35]], colour: -1, label: 'B', cx: w*0.78, cy: h*0.15 },
      { id: 'C', path: [[w*0.35,h*0.35],[w*0.65,h*0.35],[w*0.5,h*0.5]], colour: -1, label: 'C', cx: w*0.5, cy: h*0.38 },
      { id: 'D', path: [[0,h*0.3],[w*0.35,h*0.35],[w*0.5,h*0.5],[w*0.3,h*0.7],[0,h*0.65]], colour: -1, label: 'D', cx: w*0.18, cy: h*0.5 },
      { id: 'E', path: [[w*0.65,h*0.35],[w,h*0.3],[w,h*0.65],[w*0.7,h*0.7],[w*0.5,h*0.5]], colour: -1, label: 'E', cx: w*0.82, cy: h*0.5 },
      { id: 'F', path: [[w*0.5,h*0.5],[w*0.3,h*0.7],[w*0.5,h],[w*0.7,h*0.7]], colour: -1, label: 'F', cx: w*0.5, cy: h*0.72 },
      { id: 'G', path: [[0,h*0.65],[w*0.3,h*0.7],[w*0.5,h],[0,h]], colour: -1, label: 'G', cx: w*0.15, cy: h*0.85 },
      { id: 'H', path: [[w*0.7,h*0.7],[w,h*0.65],[w,h],[w*0.5,h]], colour: -1, label: 'H', cx: w*0.85, cy: h*0.85 },
    ];
    this.adjacency = [
      ['A','B'],['A','C'],['A','D'],
      ['B','C'],['B','E'],
      ['C','D'],['C','E'],['C','F'],
      ['D','F'],['D','G'],
      ['E','F'],['E','H'],
      ['F','G'],['F','H'],
      ['G','H'],
    ];
  },

  draw() {
    DrawUtil.clear(this.ctx, this.canvas);
    DrawUtil.drawMapRegions(this.ctx, this.regions);
  },

  onClick(e) {
    const rect = this.canvas.getBoundingClientRect();
    const sx = this.canvas.width / rect.width;
    const sy = this.canvas.height / rect.height;
    const x = (e.clientX - rect.left) * sx;
    const y = (e.clientY - rect.top) * sy;

    for (const r of this.regions) {
      if (this.pointInRegion(x, y, r.path)) {
        r.colour = this.selectedColour;
        this.draw();
        this.checkStatus();
        return;
      }
    }
  },

  pointInRegion(px, py, path) {
    let inside = false;
    for (let i = 0, j = path.length - 1; i < path.length; j = i++) {
      const xi = path[i][0], yi = path[i][1];
      const xj = path[j][0], yj = path[j][1];
      if (((yi > py) !== (yj > py)) && (px < (xj - xi) * (py - yi) / (yj - yi) + xi))
        inside = !inside;
    }
    return inside;
  },

  checkStatus() {
    const status = document.getElementById('intro-status');
    const allColoured = this.regions.every(r => r.colour >= 0);
    let conflicts = 0;
    for (const [a, b] of this.adjacency) {
      const ra = this.regions.find(r => r.id === a);
      const rb = this.regions.find(r => r.id === b);
      if (ra.colour >= 0 && rb.colour >= 0 && ra.colour === rb.colour) conflicts++;
    }
    if (!allColoured) {
      status.textContent = `${this.regions.filter(r => r.colour >= 0).length}/${this.regions.length} regions coloured. ${conflicts} conflict(s).`;
      status.style.color = conflicts ? '#e74c3c' : '#8b90a8';
    } else if (conflicts === 0) {
      const used = new Set(this.regions.map(r => r.colour)).size;
      status.textContent = `All regions coloured with ${used} colour(s) and no conflicts!`;
      status.style.color = '#2ecc71';
    } else {
      status.textContent = `All coloured but ${conflicts} adjacent conflict(s) remain.`;
      status.style.color = '#e74c3c';
    }
  },

  autoColour() {
    const g = new Graph();
    for (const r of this.regions) g.addNode(r.id, 0, 0, r.id);
    for (const [a, b] of this.adjacency) g.addEdge(a, b);
    ColourAlgo.dsatur(g);
    for (const r of this.regions) r.colour = g.nodes[r.id].colour;
    this.draw();
    this.checkStatus();
  },

  reset() {
    for (const r of this.regions) r.colour = -1;
    this.draw();
    document.getElementById('intro-status').textContent = '';
  }
};

/* --------------------------------------------------
   Tab 2: Dual graph transformation demo
   -------------------------------------------------- */
const DualDemo = {
  canvas1: null, ctx1: null,
  canvas2: null, ctx2: null,
  step: 0, maxSteps: 5,
  autoTimer: null,
  regions: [],
  dualGraph: null,

  init() {
    this.canvas1 = document.getElementById('dual-map-canvas');
    this.canvas2 = document.getElementById('dual-graph-canvas');
    if (!this.canvas1 || !this.canvas2) return;
    this.ctx1 = this.canvas1.getContext('2d');
    this.ctx2 = this.canvas2.getContext('2d');

    this.buildRegions();
    this.buildDualGraph();
    this.draw();

    document.getElementById('dual-step').addEventListener('click', () => this.nextStep());
    document.getElementById('dual-reset').addEventListener('click', () => this.resetDemo());
    document.getElementById('dual-auto').addEventListener('click', () => this.autoPlay());
  },

  buildRegions() {
    const w = 360, h = 320;
    this.regions = [
      { id: 'R1', path: [[0,0],[w*0.5,0],[w*0.4,h*0.4],[0,h*0.35]], colour: -1, label: 'R1', cx: w*0.2, cy: h*0.17 },
      { id: 'R2', path: [[w*0.5,0],[w,0],[w,h*0.35],[w*0.6,h*0.4]], colour: -1, label: 'R2', cx: w*0.78, cy: h*0.17 },
      { id: 'R3', path: [[w*0.4,h*0.4],[w*0.6,h*0.4],[w*0.5,h*0.65]], colour: -1, label: 'R3', cx: w*0.5, cy: h*0.46 },
      { id: 'R4', path: [[0,h*0.35],[w*0.4,h*0.4],[w*0.5,h*0.65],[0,h]], colour: -1, label: 'R4', cx: w*0.18, cy: h*0.65 },
      { id: 'R5', path: [[w*0.6,h*0.4],[w,h*0.35],[w,h],[w*0.5,h*0.65]], colour: -1, label: 'R5', cx: w*0.82, cy: h*0.65 },
    ];
  },

  buildDualGraph() {
    const w = 360, h = 320;
    this.dualGraph = new Graph();
    const positions = { R1: [w*0.25, h*0.22], R2: [w*0.75, h*0.22], R3: [w*0.5, h*0.48], R4: [w*0.2, h*0.75], R5: [w*0.8, h*0.75] };
    for (const [id, [x, y]] of Object.entries(positions)) this.dualGraph.addNode(id, x, y, id);
    this.dualGraph.addEdge('R1', 'R2');
    this.dualGraph.addEdge('R1', 'R3');
    this.dualGraph.addEdge('R1', 'R4');
    this.dualGraph.addEdge('R2', 'R3');
    this.dualGraph.addEdge('R2', 'R5');
    this.dualGraph.addEdge('R3', 'R4');
    this.dualGraph.addEdge('R3', 'R5');
    this.dualGraph.addEdge('R4', 'R5');
  },

  draw() {
    const status = document.getElementById('dual-status');
    DrawUtil.clear(this.ctx1, this.canvas1);
    DrawUtil.clear(this.ctx2, this.canvas2);

    if (this.step >= 1) {
      const regionColours = [0, 1, 2, 3, 0];
      this.regions.forEach((r, i) => { r.colour = regionColours[i]; });
    }
    DrawUtil.drawMapRegions(this.ctx1, this.regions);

    if (this.step >= 2) {
      for (const r of this.regions) {
        this.ctx1.beginPath();
        this.ctx1.arc(r.cx, r.cy, 6, 0, 2 * Math.PI);
        this.ctx1.fillStyle = '#fff';
        this.ctx1.fill();
        this.ctx1.strokeStyle = '#000';
        this.ctx1.lineWidth = 2;
        this.ctx1.stroke();
      }
    }

    if (this.step >= 3) {
      const nodesVisible = Math.min(this.step - 2, 5);
      const ids = this.dualGraph.nodeIds();
      for (let i = 0; i < nodesVisible && i < ids.length; i++) {
        const n = this.dualGraph.nodes[ids[i]];
        DrawUtil.drawNode(this.ctx2, n.x, n.y, 16, COLOURS[i % 4], '#fff', ids[i], '#fff');
      }
    }

    if (this.step >= 4) {
      for (const e of this.dualGraph.edges) {
        const a = this.dualGraph.nodes[e.from];
        const b = this.dualGraph.nodes[e.to];
        DrawUtil.drawEdge(this.ctx2, a.x, a.y, b.x, b.y, '#6c8cff', 2);
      }
      for (const id of this.dualGraph.nodeIds()) {
        const idx = this.dualGraph.nodeIds().indexOf(id);
        const n = this.dualGraph.nodes[id];
        DrawUtil.drawNode(this.ctx2, n.x, n.y, 16, COLOURS[idx % 4], '#fff', id, '#fff');
      }
    }

    if (this.step >= 5) {
      ColourAlgo.dsatur(this.dualGraph);
      DrawUtil.drawGraph(this.ctx2, this.canvas2, this.dualGraph, { nodeRadius: 16 });
    }

    const messages = [
      'Click "Step" to begin the transformation.',
      'Step 1: Colour the map regions.',
      'Step 2: Place a point (vertex) in each region.',
      'Step 3: Create corresponding vertices in the dual graph.',
      'Step 4: Connect vertices whose regions share a boundary.',
      'Step 5: Colour the dual graph — same problem, graph form!'
    ];
    status.textContent = messages[this.step] || messages[messages.length - 1];
  },

  nextStep() {
    if (this.step < this.maxSteps) this.step++;
    this.draw();
  },

  resetDemo() {
    this.step = 0;
    this.regions.forEach(r => { r.colour = -1; });
    this.dualGraph.clearColours();
    if (this.autoTimer) { clearInterval(this.autoTimer); this.autoTimer = null; }
    this.draw();
  },

  autoPlay() {
    if (this.autoTimer) { clearInterval(this.autoTimer); this.autoTimer = null; return; }
    this.resetDemo();
    this.autoTimer = setInterval(() => {
      this.nextStep();
      if (this.step >= this.maxSteps) { clearInterval(this.autoTimer); this.autoTimer = null; }
    }, 1200);
  }
};

/* --------------------------------------------------
   Tab 2: K5, K33, K4 mini diagrams
   -------------------------------------------------- */
const MiniFigures = {
  init() {
    this.drawK5();
    this.drawK33();
    this.drawK4();
  },

  drawK5() {
    const canvas = document.getElementById('k5-canvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const g = GraphFactory.complete(5, 90, 90, 65);
    DrawUtil.drawGraph(ctx, canvas, g, { nodeRadius: 12, showLabels: true });
  },

  drawK33() {
    const canvas = document.getElementById('k33-canvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const g = GraphFactory.bipartite(3, 3, 90, 90, 140, 120);
    DrawUtil.drawGraph(ctx, canvas, g, { nodeRadius: 12, showLabels: false });
  },

  drawK4() {
    const canvas = document.getElementById('k4-canvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const g = GraphFactory.complete(4, 90, 90, 65);
    ColourAlgo.dsatur(g);
    DrawUtil.drawGraph(ctx, canvas, g, { nodeRadius: 12, showLabels: true });
  }
};

/* --------------------------------------------------
   Tab 3: Euler formula demo
   -------------------------------------------------- */
const EulerDemo = {
  canvas: null, ctx: null,
  currentType: 'tetrahedron',

  init() {
    this.canvas = document.getElementById('euler-canvas');
    if (!this.canvas) return;
    this.ctx = this.canvas.getContext('2d');

    const select = document.getElementById('euler-graph-select');
    select.addEventListener('change', () => {
      this.currentType = select.value;
      this.draw();
    });
    this.draw();
  },

  draw() {
    const g = GraphFactory.platonic(this.currentType, 200, 175, 130);
    ColourAlgo.dsatur(g);
    DrawUtil.drawGraph(this.ctx, this.canvas, g, { nodeRadius: 14 });

    const V = g.nodeCount();
    const E = g.edgeCount();
    const F = 2 - V + E;
    const euler = V - E + F;
    const edgeBound = 3 * V - 6;
    const minDeg = Math.min(...g.nodeIds().map(id => g.degree(id)));

    const statsEl = document.getElementById('euler-stats');
    statsEl.innerHTML = `
      <div class="stat-box"><div class="stat-val">${V}</div><div class="stat-label">Vertices (V)</div></div>
      <div class="stat-box"><div class="stat-val">${E}</div><div class="stat-label">Edges (E)</div></div>
      <div class="stat-box"><div class="stat-val">${F}</div><div class="stat-label">Faces (F)</div></div>
      <div class="stat-box"><div class="stat-val">${euler}</div><div class="stat-label">V − E + F</div></div>
      <div class="stat-box"><div class="stat-val">${edgeBound}</div><div class="stat-label">3V − 6</div></div>
      <div class="stat-box"><div class="stat-val">${E <= edgeBound ? '✓' : '✗'}</div><div class="stat-label">E ≤ 3V−6</div></div>
      <div class="stat-box"><div class="stat-val">${minDeg}</div><div class="stat-label">Min Degree</div></div>
      <div class="stat-box"><div class="stat-val">${g.coloursUsed()}</div><div class="stat-label">Colours Used</div></div>
    `;
  }
};

/* --------------------------------------------------
   Tab 5: Kempe chain demo
   -------------------------------------------------- */
const KempeDemo = {
  canvas: null, ctx: null,
  graph: null,
  chain: [],
  selectedVertex: null,

  init() {
    this.canvas = document.getElementById('kempe-canvas');
    if (!this.canvas) return;
    this.ctx = this.canvas.getContext('2d');

    this.buildGraph();
    this.draw();

    this.canvas.addEventListener('click', e => this.onClick(e));
    document.getElementById('kempe-find').addEventListener('click', () => this.findChain());
    document.getElementById('kempe-swap').addEventListener('click', () => this.swapChain());
    document.getElementById('kempe-reset').addEventListener('click', () => this.resetDemo());
  },

  buildGraph() {
    this.graph = GraphFactory.dodecahedron(300, 210, 170);
    ColourAlgo.dsatur(this.graph);
    this.chain = [];
    this.selectedVertex = null;
  },

  draw() {
    // Chains follow the site drawing convention (docs/shared/kempe-draw.js), on canvas: a metro-style track of two thin
    // parallel strands in the chain's two colours, rounded, with a background casing; chain vertices keep their own
    // fill and get a ring in the partner colour.
    this.graph.clearHighlights();
    DrawUtil.drawGraph(this.ctx, this.canvas, this.graph, { nodeRadius: 16 });
    const ctx = this.ctx, g = this.graph;
    if (this.chain.length > 0 && this.pair) {
      const bg = getComputedStyle(document.documentElement).getPropertyValue('--surface2').trim() || '#1e2230';
      const [a, b] = this.pair, S = new Set(this.chain), s = 5, casing = 3;
      const edges = g.edges.filter(e => S.has(e.from) && S.has(e.to));
      ctx.save(); ctx.lineCap = 'round'; ctx.lineJoin = 'round';
      for (const e of edges) {                       // casing
        const p = g.nodes[e.from], q = g.nodes[e.to];
        ctx.beginPath(); ctx.moveTo(p.x, p.y); ctx.lineTo(q.x, q.y);
        ctx.strokeStyle = bg; ctx.lineWidth = 2 * s + 2 * casing; ctx.stroke();
      }
      for (const e of edges) {                       // strands: colour a on the left, from the a-end to the b-end
        let p = g.nodes[e.from], q = g.nodes[e.to];
        if (p.colour !== a) [p, q] = [q, p];
        const dx = q.x - p.x, dy = q.y - p.y, l = Math.hypot(dx, dy) || 1, nx = -dy / l * s / 2, ny = dx / l * s / 2;
        [[a, 1], [b, -1]].forEach(([c, sg]) => {
          ctx.beginPath(); ctx.moveTo(p.x + sg * nx, p.y + sg * ny); ctx.lineTo(q.x + sg * nx, q.y + sg * ny);
          ctx.strokeStyle = COLOURS[c]; ctx.lineWidth = s; ctx.stroke();
        });
      }
      ctx.restore();
      for (const v of this.chain) {                  // stations on top: own fill, ring in the partner colour
        const n = g.nodes[v];
        DrawUtil.drawNode(ctx, n.x, n.y, 16, COLOURS[n.colour % COLOURS.length], null, n.label);
        const other = n.colour === a ? b : a;
        ctx.beginPath(); ctx.arc(n.x, n.y, 16 + 4.5, 0, 2 * Math.PI);
        ctx.strokeStyle = bg; ctx.lineWidth = 7; ctx.stroke();
        ctx.beginPath(); ctx.arc(n.x, n.y, 16 + 4.5, 0, 2 * Math.PI);
        ctx.strokeStyle = COLOURS[other]; ctx.lineWidth = 4; ctx.stroke();
      }
    }

    if (this.selectedVertex) {
      const n = this.graph.nodes[this.selectedVertex];
      this.ctx.beginPath();
      this.ctx.arc(n.x, n.y, 26, 0, 2 * Math.PI);
      this.ctx.strokeStyle = '#fff';
      this.ctx.lineWidth = 2;
      this.ctx.setLineDash([4, 3]);
      this.ctx.stroke();
      this.ctx.setLineDash([]);
    }
  },

  onClick(e) {
    const rect = this.canvas.getBoundingClientRect();
    const sx = this.canvas.width / rect.width;
    const sy = this.canvas.height / rect.height;
    const x = (e.clientX - rect.left) * sx;
    const y = (e.clientY - rect.top) * sy;
    const id = this.graph.nodeAt(x, y, 20);
    if (id) {
      this.selectedVertex = id;
      this.draw();
      const c = this.graph.nodes[id].colour;
      document.getElementById('kempe-status').textContent =
        `Selected vertex ${id} (${COLOUR_NAMES[c]}). Click "Highlight Chain" to find the Kempe chain.`;
    }
  },

  findChain() {
    if (!this.selectedVertex) {
      document.getElementById('kempe-status').textContent = 'Click a vertex first!';
      return;
    }
    const c1 = parseInt(document.getElementById('kempe-c1').value);
    const c2 = parseInt(document.getElementById('kempe-c2').value);
    if (c1 === c2) {
      document.getElementById('kempe-status').textContent = 'Please choose two different colours.';
      return;
    }
    const vc = this.graph.nodes[this.selectedVertex].colour;
    if (vc !== c1 && vc !== c2) {
      document.getElementById('kempe-status').textContent =
        `Vertex ${this.selectedVertex} is ${COLOUR_NAMES[vc]}, not one of the selected colours. Pick a matching vertex.`;
      return;
    }
    this.chain = ColourAlgo.findKempeChain(this.graph, this.selectedVertex, c1, c2);
    this.pair = [c1, c2];
    this.draw();
    document.getElementById('kempe-status').textContent =
      `Kempe chain (${COLOUR_NAMES[c1]}/${COLOUR_NAMES[c2]}) from ${this.selectedVertex}: ${this.chain.length} vertices highlighted.`;
  },

  swapChain() {
    if (this.chain.length === 0) {
      document.getElementById('kempe-status').textContent = 'Find a chain first!';
      return;
    }
    const c1 = parseInt(document.getElementById('kempe-c1').value);
    const c2 = parseInt(document.getElementById('kempe-c2').value);
    ColourAlgo.swapKempeChain(this.graph, this.chain, c1, c2);
    this.draw();
    const valid = this.graph.isValidColouring();
    document.getElementById('kempe-status').textContent =
      `Swapped ${this.chain.length} vertices. Colouring still valid: ${valid ? 'Yes' : 'No'}`;
  },

  resetDemo() {
    this.buildGraph();
    this.draw();
    document.getElementById('kempe-status').textContent =
      'Select two colours then click a vertex to find a Kempe chain.';
  }
};

/* --------------------------------------------------
   Tab 6: Discharging demo
   -------------------------------------------------- */
const DischargeDemo = {
  canvas: null, ctx: null,
  graph: null,
  charges: null,
  phase: 0,

  init() {
    this.canvas = document.getElementById('discharge-canvas');
    if (!this.canvas) return;
    this.ctx = this.canvas.getContext('2d');
    this.buildGraph();
    this.draw();

    document.getElementById('discharge-init').addEventListener('click', () => this.assignCharges());
    document.getElementById('discharge-run').addEventListener('click', () => this.runDischarge());
    document.getElementById('discharge-reset').addEventListener('click', () => this.resetDemo());
  },

  buildGraph() {
    const g = new Graph();
    const cx = 300, cy = 200;
    const positions = [
      [0, -160], [-140, -60], [140, -60], [-90, 80], [90, 80], [0, 160],
      [-50, -30], [50, -30], [0, 50]
    ];
    for (let i = 0; i < positions.length; i++) {
      g.addNode(String(i), cx + positions[i][0], cy + positions[i][1], String(i));
    }
    const edges = [
      [0,1],[0,2],[1,3],[2,4],[3,5],[4,5],
      [0,6],[0,7],[1,6],[2,7],[3,6],[4,7],
      [5,8],[3,8],[4,8],[6,7],[6,8],[7,8]
    ];
    edges.forEach(([a, b]) => g.addEdge(String(a), String(b)));
    this.graph = g;
    this.charges = null;
    this.phase = 0;
  },

  draw() {
    DrawUtil.drawGraph(this.ctx, this.canvas, this.graph, {
      nodeRadius: 20,
      charges: this.charges
    });
  },

  assignCharges() {
    this.charges = ColourAlgo.initialCharges(this.graph);
    this.phase = 1;
    this.draw();
    const total = Object.values(this.charges).reduce((a, b) => a + b, 0);
    const pos = Object.values(this.charges).filter(c => c > 0).length;
    const neg = Object.values(this.charges).filter(c => c < 0).length;
    document.getElementById('discharge-status').textContent =
      `Charges assigned: charge(v) = 6 − deg(v). Total = ${total}. ${pos} positive, ${neg} negative.`;
  },

  runDischarge() {
    if (!this.charges) {
      document.getElementById('discharge-status').textContent = 'Assign charges first!';
      return;
    }
    this.charges = ColourAlgo.discharge(this.graph, this.charges);
    this.phase = 2;
    this.draw();
    const total = Object.values(this.charges).reduce((a, b) => a + b, 0).toFixed(1);
    const pos = Object.values(this.charges).filter(c => c > 0.01).length;
    document.getElementById('discharge-status').textContent =
      `After discharging: total charge = ${total} (preserved). ${pos} vertices with positive charge must contain a reducible configuration.`;
  },

  resetDemo() {
    this.buildGraph();
    this.draw();
    document.getElementById('discharge-status').textContent = 'Click "Assign Charges" to begin.';
  }
};

/* --------------------------------------------------
   Tab 8: Playground
   -------------------------------------------------- */
const Playground = {
  canvas: null, ctx: null,
  graph: null,
  selectedColour: 0,
  dsaturSteps: [],
  stepIndex: 0,

  init() {
    this.canvas = document.getElementById('playground-canvas');
    if (!this.canvas) return;
    this.ctx = this.canvas.getContext('2d');

    document.getElementById('playground-graph').addEventListener('change', () => this.loadGraph());
    document.getElementById('playground-solve').addEventListener('click', () => this.solve());
    document.getElementById('playground-step').addEventListener('click', () => this.stepSolve());
    document.getElementById('playground-clear').addEventListener('click', () => this.clearColours());

    this.canvas.addEventListener('click', e => this.onClick(e));

    document.querySelectorAll('#tab-interactive .colour-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        document.querySelectorAll('#tab-interactive .colour-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        this.selectedColour = parseInt(btn.dataset.colour);
      });
    });

    this.loadGraph();
  },

  loadGraph() {
    const type = document.getElementById('playground-graph').value;
    const cx = 350, cy = 250;
    switch (type) {
      case 'petersen':  this.graph = GraphFactory.petersen(cx, cy, 180, 85); break;
      case 'cycle6':    this.graph = GraphFactory.cycle(6, cx, cy, 170); break;
      case 'k4':        this.graph = GraphFactory.complete(4, cx, cy, 150); break;
      case 'dodecahedron': this.graph = GraphFactory.dodecahedron(cx, cy, 200); break;
      case 'grid':      this.graph = GraphFactory.grid(4, 4, cx, cy, 80); break;
      case 'usa':       this.graph = GraphFactory.usaWestern(cx, cy, 480); break;
    }
    this.dsaturSteps = [];
    this.stepIndex = 0;
    this.draw();
    this.updateStats();
    this.clearLog();
  },

  draw() {
    DrawUtil.drawGraph(this.ctx, this.canvas, this.graph, { nodeRadius: NODE_RADIUS });
  },

  onClick(e) {
    const rect = this.canvas.getBoundingClientRect();
    const sx = this.canvas.width / rect.width;
    const sy = this.canvas.height / rect.height;
    const x = (e.clientX - rect.left) * sx;
    const y = (e.clientY - rect.top) * sy;
    const id = this.graph.nodeAt(x, y, NODE_RADIUS + 4);
    if (id) {
      this.graph.nodes[id].colour = this.selectedColour;
      this.draw();
      this.updateStatus();
    }
  },

  solve() {
    this.graph.clearColours();
    const g2 = this.graph.clone();
    const steps = ColourAlgo.dsatur(g2);
    for (const s of steps) this.graph.nodes[s.vertex].colour = s.colour;
    this.draw();
    this.logSteps(steps);
    this.updateStatus();
  },

  stepSolve() {
    if (this.dsaturSteps.length === 0) {
      this.graph.clearColours();
      const g2 = this.graph.clone();
      this.dsaturSteps = ColourAlgo.dsatur(g2);
      this.stepIndex = 0;
      this.graph.clearColours();
      this.clearLog();
    }
    if (this.stepIndex < this.dsaturSteps.length) {
      const s = this.dsaturSteps[this.stepIndex];
      this.graph.nodes[s.vertex].colour = s.colour;
      this.stepIndex++;
      this.draw();
      this.addLogEntry(s);
      this.updateStatus();
    }
    if (this.stepIndex >= this.dsaturSteps.length) {
      document.getElementById('playground-status').textContent += ' (DSATUR complete)';
    }
  },

  clearColours() {
    this.graph.clearColours();
    this.dsaturSteps = [];
    this.stepIndex = 0;
    this.draw();
    this.clearLog();
    this.updateStatus();
  },

  updateStats() {
    const el = document.getElementById('playground-stats');
    const V = this.graph.nodeCount();
    const E = this.graph.edgeCount();
    const minDeg = V > 0 ? Math.min(...this.graph.nodeIds().map(id => this.graph.degree(id))) : 0;
    const maxDeg = V > 0 ? Math.max(...this.graph.nodeIds().map(id => this.graph.degree(id))) : 0;
    el.innerHTML = `V=${V}, E=${E}<br>Degree range: [${minDeg}, ${maxDeg}]`;
  },

  updateStatus() {
    const status = document.getElementById('playground-status');
    const valid = this.graph.isValidColouring();
    const complete = this.graph.isComplete();
    const used = this.graph.coloursUsed();
    if (complete && valid) {
      status.textContent = `Properly coloured with ${used} colour(s)!`;
      status.style.color = '#2ecc71';
    } else if (!valid) {
      status.textContent = `Conflict detected! Adjacent vertices share a colour.`;
      status.style.color = '#e74c3c';
    } else {
      const done = this.graph.nodeIds().filter(id => this.graph.nodes[id].colour >= 0).length;
      status.textContent = `${done}/${this.graph.nodeCount()} vertices coloured.`;
      status.style.color = '#8b90a8';
    }
  },

  clearLog() {
    document.getElementById('playground-log').innerHTML = '';
  },

  logSteps(steps) {
    this.clearLog();
    for (const s of steps) this.addLogEntry(s);
  },

  addLogEntry(s) {
    const el = document.getElementById('playground-log');
    const div = document.createElement('div');
    div.className = 'log-entry';
    div.innerHTML = `<span class="log-highlight">${s.vertex}</span> → ${COLOUR_NAMES[s.colour]} (${s.reason})`;
    el.appendChild(div);
    el.scrollTop = el.scrollHeight;
  }
};
