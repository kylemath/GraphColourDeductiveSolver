/* kempe-draw.js: a small SVG drawing module for coloured triangulations with a degree-five hole.
 *
 * DRAWING CONVENTION (project-wide; adopt it on any page that draws Kempe chains)
 *  1. Layout. A flat 2D drawing. The hole sits at the centre, its five neighbours form a ring around it, and the
 *     rest of the map spreads outward. Vertex positions are fixed for the whole page: every state is drawn on the
 *     same positions, so changes from one state to the next are easy to compare. No auto-rotation and no 3D.
 *     (Positions are computed offline by the page's build script; this module only draws them. The shared
 *     builder is docs/shared/hole_layout.py.) A page whose essential content is 3D may keep a 3D view, but any
 *     spin is opt-in (a button), off by default and unavailable under prefers-reduced-motion.
 *  2. Chains, metro-map style (like the game Mini Metro). A Kempe chain on colour pair {a,b} is a thick line made
 *     of two thin parallel strands, one in colour a and one in colour b, with rounded ends and joins. Each track has
 *     a thin casing in the background colour, so tracks that meet or run close stay visibly separate. Two chains
 *     never share an edge (an edge's two end colours fix its pair), so tracks only meet at nodes: there they fan
 *     in from different directions and the station disc sits on top.
 *  3. Shared nodes. A node on one highlighted chain gets a single ring; a node on two or three highlighted chains
 *     gets a ring split into one segment per chain. A segment's colour is the chain's other colour (the partner of
 *     the node's own colour), unless the chain sets `ring`. The node's fill always stays its own vertex colour.
 *
 * USAGE
 *   const kd = KempeDraw.create(svgElement, {
 *     pos: [[x, y], ...],          // one per vertex, roughly within [-1, 1]
 *     edges: [[u, w], ...],        // all edges of the triangulation (edges at the hole are drawn as dashed spokes)
 *     hole: 4, link: [..5 ids..],  // the hole vertex and its neighbours in cyclic order (both optional: a graph
 *                                  // with no hole is drawn the same way, without the hole marker)
 *     colours: ['#f85149', ...],   // colour index -> CSS colour
 *     bg: '#161b22',               // background colour (used for the casing)
 *     scale: 1,                    // multiplies every size (use > 1 for small graphs, < 1 for small multiples)
 *     // optional extras (all off by default)
 *     label: u => '7',             // text drawn on the vertex disc (null/'' for none); labelSize sets its size
 *     holeLabel: '?',              // text drawn in the hole marker
 *     vertexTitle: u => '...',     // tooltip for the vertex disc (default 'vertex u')
 *     onVertex: (u, event) => {},  // click handler on vertex discs (chain hit areas then let clicks through)
 *     blank: '#21262d'             // fill for an uncoloured vertex (colour null or < 0), drawn with a dashed outline
 *   });
 *   kd.setColouring(col);          // col[u] = colour index (the hole's entry is ignored)
 *   kd.setChains([{ v: [u, ...], pair: [a, b], ring: optionalCss, dash: false, title: 'tooltip', onClick, onEnter, onLeave }]);
 *                                  // dash: true draws the strands and ring segments dashed (e.g. "about to be swapped")
 *   kd.setDim(true|false);         // fade vertices and edges that are on no highlighted chain
 *   kd.layer('marks');             // an empty <g> above the rings, below the vertex text (page decorations)
 *   kd.layer('labels');            // an empty <g> on top, for page-specific labels
 *   kd.nodeR(u);                   // radius of the vertex disc at u (for placing labels)
 *   kd.disc(u);                    // the vertex disc element
 *
 * STANDALONE HELPERS (for tracks that are not graph edges, e.g. schematic chains drawn as curves)
 *   KempeDraw.track(parentG, pts, colA, colB, { strand, casing, bg, dash })   // polyline track, colour A on the left
 *   KempeDraw.quad(p0, c, p1, n)   // n+1 points on the quadratic Bezier p0 -> c -> p1 (feed to track for a curved edge)
 *   KempeDraw.legendIcon(colA, colB, { dash, bg })   // inline SVG markup of a short track, for legends
 */
(function (global) {
  'use strict';
  const NS = 'http://www.w3.org/2000/svg';

  function el(tag, attrs, parent) {
    const e = document.createElementNS(NS, tag);
    for (const k in attrs) e.setAttribute(k, attrs[k]);
    if (parent) parent.appendChild(e);
    return e;
  }

  function arcPath(cx, cy, r, a0, a1) {
    const x0 = cx + r * Math.cos(a0), y0 = cy + r * Math.sin(a0), x1 = cx + r * Math.cos(a1), y1 = cy + r * Math.sin(a1);
    const large = (a1 - a0) % (2 * Math.PI) > Math.PI ? 1 : 0;
    return 'M' + x0 + ' ' + y0 + ' A' + r + ' ' + r + ' 0 ' + large + ' 1 ' + x1 + ' ' + y1;
  }

  // offset a polyline by d along its left normal (mitred joins, clamped)
  function offsetLine(pts, d) {
    const n = pts.length, out = [];
    const nrm = (a, b) => { const dx = b[0] - a[0], dy = b[1] - a[1], l = Math.hypot(dx, dy) || 1; return [-dy / l, dx / l]; };
    for (let i = 0; i < n; i++) {
      let m;
      if (i === 0) m = nrm(pts[0], pts[1]);
      else if (i === n - 1) m = nrm(pts[n - 2], pts[n - 1]);
      else {
        const a = nrm(pts[i - 1], pts[i]), b = nrm(pts[i], pts[i + 1]);
        let x = a[0] + b[0], y = a[1] + b[1]; const l = Math.hypot(x, y) || 1; x /= l; y /= l;
        const c = Math.max(0.5, x * a[0] + y * a[1]); m = [x / c, y / c];
      }
      out.push([pts[i][0] + m[0] * d, pts[i][1] + m[1] * d]);
    }
    return out;
  }
  const ptsAttr = (p) => p.map((q) => q[0] + ',' + q[1]).join(' ');

  function track(parent, pts, colA, colB, o) {
    o = o || {};
    const s = o.strand || 0.0115, cs = o.casing === undefined ? 0.0075 : o.casing, bg = o.bg || '#0d1117';
    const g = el('g', {}, parent);
    const base = { fill: 'none', 'stroke-linecap': 'round', 'stroke-linejoin': 'round' };
    if (cs > 0) el('polyline', Object.assign({ points: ptsAttr(pts), stroke: bg, 'stroke-width': 2 * s + 2 * cs }, base), g);
    const dash = o.dash ? { 'stroke-dasharray': (2.2 * s) + ' ' + (1.6 * s) } : {};
    if (o.dash) el('polyline', Object.assign({ points: ptsAttr(pts), stroke: bg, 'stroke-width': 2 * s, opacity: 0.6 }, base), g);
    el('polyline', Object.assign({ points: ptsAttr(offsetLine(pts, s / 2)), stroke: colA, 'stroke-width': s }, base, dash), g);
    el('polyline', Object.assign({ points: ptsAttr(offsetLine(pts, -s / 2)), stroke: colB, 'stroke-width': s }, base, dash), g);
    return g;
  }

  function quad(p0, c, p1, n) {
    n = n || 24; const out = [];
    for (let i = 0; i <= n; i++) {
      const t = i / n, u = 1 - t;
      out.push([u * u * p0[0] + 2 * u * t * c[0] + t * t * p1[0], u * u * p0[1] + 2 * u * t * c[1] + t * t * p1[1]]);
    }
    return out;
  }

  function legendIcon(colA, colB, o) {
    o = o || {};
    const bg = o.bg || '#0d1117', dash = o.dash ? ' stroke-dasharray="4 3"' : '';
    return '<svg width="26" height="12" viewBox="0 0 26 12" aria-hidden="true" style="display:inline-block;width:26px;height:12px;vertical-align:-1px;margin-right:.3rem">' +
      '<line x1="3" y1="6" x2="23" y2="6" stroke="' + bg + '" stroke-width="10" stroke-linecap="round"/>' +
      '<line x1="3" y1="4" x2="23" y2="4" stroke="' + colA + '" stroke-width="3.4" stroke-linecap="round"' + dash + '/>' +
      '<line x1="3" y1="8" x2="23" y2="8" stroke="' + colB + '" stroke-width="3.4" stroke-linecap="round"' + dash + '/></svg>';
  }

  function create(svg, opt) {
    const P = opt.pos, hole = opt.hole, link = opt.link || [], C = opt.colours, sc = opt.scale || 1;
    const bg = opt.bg || '#0d1117', blank = opt.blank || '#21262d';
    const R = { v: 0.034 * sc, link: 0.044 * sc, strand: 0.0115 * sc, casing: 0.0075 * sc, ring: 0.011 * sc, edge: 0.007 * sc };
    const n = P.length, isLink = new Set(link);
    const hasHole = hole !== undefined && hole !== null;
    const adj = Array.from({ length: n }, () => new Set());
    opt.edges.forEach(([a, b]) => { adj[a].add(b); adj[b].add(a); });

    const root = el('g', { class: 'kd' }, svg);
    const L = {};
    ['hole', 'edges', 'casing', 'tracks', 'nodes', 'rings', 'marks', 'text', 'hits', 'labels'].forEach(k => { L[k] = el('g', { class: 'kd-' + k }, root); });
    L.hits.setAttribute('fill', 'none');
    L.rings.setAttribute('pointer-events', 'none');
    L.text.setAttribute('pointer-events', 'none');

    // hole: shaded pentagon, dashed spokes, dashed marker
    if (hasHole) {
      if (link.length) el('polygon', { points: link.map(x => P[x].join(',')).join(' '), fill: 'rgba(188,140,255,0.07)' }, L.hole);
      link.forEach(x => el('line', { x1: P[hole][0], y1: P[hole][1], x2: P[x][0], y2: P[x][1], stroke: '#7d8590',
        'stroke-width': R.edge * 0.9, 'stroke-dasharray': (0.022 * sc) + ' ' + (0.016 * sc) }, L.hole));
      el('circle', { cx: P[hole][0], cy: P[hole][1], r: R.link * 0.9, fill: bg, stroke: '#bc8cff', 'stroke-width': R.edge * 1.2,
        'stroke-dasharray': (0.016 * sc) + ' ' + (0.011 * sc) }, L.hole);
      if (opt.holeLabel) {
        const fs = R.link * 1.05;
        el('text', { x: P[hole][0], y: P[hole][1] + fs * 0.36, 'text-anchor': 'middle', 'font-size': fs, fill: '#e6edf3',
          'font-family': 'system-ui, sans-serif', 'pointer-events': 'none' }, L.hole).textContent = opt.holeLabel;
      }
    }
    const edgeEl = [];
    opt.edges.forEach(([a, b]) => {
      if (a === hole || b === hole) return;
      edgeEl.push({ a, b, e: el('line', { x1: P[a][0], y1: P[a][1], x2: P[b][0], y2: P[b][1], stroke: '#30363d', 'stroke-width': R.edge }, L.edges) });
    });
    const disc = [], txt = [];
    for (let u = 0; u < n; u++) {
      if (u === hole) { disc.push(null); txt.push(null); continue; }
      const d = el('circle', { cx: P[u][0], cy: P[u][1], r: isLink.has(u) ? R.link : R.v, stroke: bg, 'stroke-width': R.edge, class: 'kd-v' }, L.nodes);
      el('title', {}, d).textContent = 'vertex ' + u;
      if (opt.onVertex) { d.style.cursor = 'pointer'; d.addEventListener('click', ev => opt.onVertex(u, ev)); }
      disc.push(d);
      const lab = opt.label ? opt.label(u) : null;
      if (lab !== null && lab !== undefined && lab !== '') {
        const fs = opt.labelSize || R.v * 1.15;
        const t = el('text', { x: P[u][0], y: P[u][1] + fs * 0.36, 'text-anchor': 'middle', 'font-size': fs, 'font-weight': 600,
          fill: '#0d1117', 'font-family': 'system-ui, sans-serif' }, L.text);
        t.textContent = lab; txt.push(t);
      } else txt.push(null);
    }
    let col = new Array(n).fill(0), chains = [], dim = false;
    const coloured = u => col[u] !== null && col[u] !== undefined && col[u] >= 0;

    function clear(g) { while (g.firstChild) g.removeChild(g.firstChild); }
    function nodeR(u) { return isLink.has(u) ? R.link : R.v; }

    function setColouring(c) {
      col = c.slice();
      for (let u = 0; u < n; u++) {
        if (!disc[u]) continue;
        const ok = coloured(u);
        disc[u].setAttribute('fill', ok ? C[col[u]] : blank);
        disc[u].setAttribute('stroke', ok ? bg : '#7d8590');
        if (ok) disc[u].removeAttribute('stroke-dasharray'); else disc[u].setAttribute('stroke-dasharray', (0.012 * sc) + ' ' + (0.009 * sc));
        if (txt[u]) txt[u].setAttribute('fill', ok ? '#0d1117' : '#7d8590');
        if (opt.vertexTitle) disc[u].firstChild.textContent = opt.vertexTitle(u);
      }
      redraw();
    }

    function setChains(list) { chains = list || []; redraw(); }
    function setDim(x) { dim = !!x; redraw(); }

    function redraw() {
      ['casing', 'tracks', 'hits', 'rings'].forEach(k => clear(L[k]));
      const on = Array.from({ length: n }, () => []);      // chains through each node
      const s = R.strand, half = s / 2;
      chains.forEach((ch, ci) => {
        const S = new Set(ch.v);
        ch.v.forEach(u => on[u].push(ci));
        const grp = el('g', {}, L.tracks), hit = el('g', { style: ch.onClick ? 'cursor:pointer' : '' }, L.hits);
        if (ch.title) el('title', {}, hit).textContent = ch.title;
        const dash = ch.dash ? { 'stroke-dasharray': (2.2 * s) + ' ' + (1.6 * s) } : {};
        ch.v.forEach(u => {
          adj[u].forEach(w => {
            if (w <= u || !S.has(w) || w === hole) return;
            // orient from the colour-a end to the colour-b end; colour a runs on the left
            const [p, q] = col[u] === ch.pair[0] ? [u, w] : [w, u];
            const dx = P[q][0] - P[p][0], dy = P[q][1] - P[p][1], len = Math.hypot(dx, dy) || 1;
            const nx = -dy / len * half, ny = dx / len * half;
            el('line', { x1: P[p][0], y1: P[p][1], x2: P[q][0], y2: P[q][1], stroke: bg, 'stroke-width': 2 * s + 2 * R.casing, 'stroke-linecap': 'round' }, L.casing);
            el('line', Object.assign({ x1: P[p][0] + nx, y1: P[p][1] + ny, x2: P[q][0] + nx, y2: P[q][1] + ny, stroke: C[ch.pair[0]], 'stroke-width': s, 'stroke-linecap': 'round' }, dash), grp);
            el('line', Object.assign({ x1: P[p][0] - nx, y1: P[p][1] - ny, x2: P[q][0] - nx, y2: P[q][1] - ny, stroke: C[ch.pair[1]], 'stroke-width': s, 'stroke-linecap': 'round' }, dash), grp);
            el('line', { x1: P[p][0], y1: P[p][1], x2: P[q][0], y2: P[q][1], stroke: 'transparent', 'stroke-width': 6 * s, 'stroke-linecap': 'round', 'pointer-events': 'stroke' }, hit);
          });
          el('circle', { cx: P[u][0], cy: P[u][1], r: nodeR(u) + 3 * s, fill: 'transparent', 'pointer-events': opt.onVertex ? 'none' : 'all' }, hit);
        });
        if (ch.onClick) hit.addEventListener('click', ch.onClick);
        if (ch.onEnter) hit.addEventListener('mouseenter', ch.onEnter);
        if (ch.onLeave) hit.addEventListener('mouseleave', ch.onLeave);
        ch._hit = hit;
      });
      // rings: one segment per highlighted chain through the node
      for (let u = 0; u < n; u++) {
        if (!disc[u]) continue;
        const k = on[u].length, rr = nodeR(u) + R.ring * 0.5 + R.edge * 0.5;
        disc[u].style.opacity = dim && k === 0 ? 0.28 : 1;
        if (txt[u]) txt[u].style.opacity = dim && k === 0 ? 0.28 : 1;
        if (!k) continue;
        el('circle', { cx: P[u][0], cy: P[u][1], r: rr, fill: 'none', stroke: bg, 'stroke-width': R.ring + 2 * R.casing * 0.6 }, L.rings);
        const gap = k > 1 ? 0.5 : 0, start = -Math.PI / 2;
        on[u].forEach((ci, i) => {
          const ch = chains[ci], other = ch.pair[0] === col[u] ? ch.pair[1] : ch.pair[0];
          const stroke = ch.ring || C[other];
          const dash = ch.dash ? { 'stroke-dasharray': (1.6 * R.ring) + ' ' + (1.2 * R.ring) } : {};
          if (k === 1) el('circle', Object.assign({ cx: P[u][0], cy: P[u][1], r: rr, fill: 'none', stroke, 'stroke-width': R.ring }, dash), L.rings);
          else {
            const a0 = start + i * 2 * Math.PI / k + gap / 2, a1 = start + (i + 1) * 2 * Math.PI / k - gap / 2;
            el('path', Object.assign({ d: arcPath(P[u][0], P[u][1], rr, a0, a1), fill: 'none', stroke, 'stroke-width': R.ring, 'stroke-linecap': 'round' }, dash), L.rings);
          }
        });
      }
      edgeEl.forEach(({ a, b, e }) => { e.style.opacity = dim ? 0.35 : 1; });
    }

    return { setColouring, setChains, setDim, nodeR, disc: u => disc[u], layer: k => L[k], root, sizes: R };
  }

  global.KempeDraw = { create, track, quad, legendIcon };
})(window);
