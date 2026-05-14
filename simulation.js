class KempeSpinGlass {
    constructor(canvasId) {
        this.canvas = document.getElementById(canvasId);
        this.ctx = this.canvas.getContext('2d');
        this.resize();
        window.addEventListener('resize', () => this.resize());
        
        // Abstract neon colors mapping to the 4 states + Hot Potato (White)
        this.colors = ['#f85149', '#58a6ff', '#3fb950', '#d29922', '#ffffff']; 
        this.nodes = [];
        this.edges = [];
        
        this.initGraph();
    }

    resize() {
        const rect = this.canvas.parentElement.getBoundingClientRect();
        this.canvas.width = rect.width * window.devicePixelRatio;
        this.canvas.height = 400 * window.devicePixelRatio;
        this.ctx.scale(window.devicePixelRatio, window.devicePixelRatio);
        this.canvas.style.width = `${rect.width}px`;
        this.canvas.style.height = `400px`;
        if (this.nodes && this.nodes.length) this.draw();
    }

    initGraph() {
        // Create a central degree-5 node (the hot potato)
        const cx = this.canvas.width / (2 * window.devicePixelRatio);
        const cy = this.canvas.height / (2 * window.devicePixelRatio);
        
        this.nodes = [{ id: 0, x: cx, y: cy, color: 4, isCenter: true, charge: 1 }]; // Color 5 (index 4)
        
        // 5 neighbours forming a wheel
        const r = 90;
        for (let i = 0; i < 5; i++) {
            const angle = (i * 2 * Math.PI) / 5 - Math.PI/2;
            this.nodes.push({
                id: i+1,
                x: cx + r * Math.cos(angle),
                y: cy + r * Math.sin(angle),
                color: i % 4, // colors 1,2,3,4
                isCenter: false,
                charge: 0
            });
            // Connect to center
            this.edges.push([0, i+1]);
        }
        
        // Connect rim
        for(let i = 1; i <= 5; i++) {
            this.edges.push([i, i === 5 ? 1 : i+1]);
        }
        
        // Add an outer ring to allow chain swaps
        const r2 = 170;
        for (let i = 0; i < 5; i++) {
            const angle = (i * 2 * Math.PI) / 5 - Math.PI/2;
            this.nodes.push({
                id: i+6,
                x: cx + r2 * Math.cos(angle),
                y: cy + r2 * Math.sin(angle),
                color: (i+2) % 4, 
                isCenter: false,
                charge: 0
            });
            // Connect to inner rim
            this.edges.push([i+1, i+6]);
            // Connect outer rim
            this.edges.push([i+6, i === 4 ? 6 : i+7]);
        }

        this.draw();
    }

    draw() {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        
        // Draw edges
        this.ctx.lineWidth = 2;
        for (const [u, v] of this.edges) {
            const n1 = this.nodes[u];
            const n2 = this.nodes[v];
            
            // Highlight conflicting edges (same color, but color 5 is allowed temporarily as charge)
            if (n1.color === n2.color) {
                this.ctx.strokeStyle = '#f85149';
                this.ctx.setLineDash([5, 5]);
            } else {
                this.ctx.strokeStyle = '#30363d';
                this.ctx.setLineDash([]);
            }
            
            this.ctx.beginPath();
            this.ctx.moveTo(n1.x, n1.y);
            this.ctx.lineTo(n2.x, n2.y);
            this.ctx.stroke();
        }
        this.ctx.setLineDash([]);

        // Draw nodes
        for (const n of this.nodes) {
            this.ctx.beginPath();
            this.ctx.arc(n.x, n.y, n.isCenter ? 15 : 12, 0, 2 * Math.PI);
            this.ctx.fillStyle = this.colors[n.color];
            this.ctx.fill();
            this.ctx.strokeStyle = n.color === 4 ? '#ffffff' : '#000000';
            this.ctx.lineWidth = n.color === 4 ? 4 : 2;
            this.ctx.stroke();
            
            if (n.color === 4) {
                // Draw hot potato glow
                this.ctx.beginPath();
                this.ctx.arc(n.x, n.y, 25, 0, 2 * Math.PI);
                this.ctx.fillStyle = 'rgba(255, 255, 255, 0.2)';
                this.ctx.fill();
                this.ctx.beginPath();
                this.ctx.arc(n.x, n.y, 35, 0, 2 * Math.PI);
                this.ctx.fillStyle = 'rgba(255, 255, 255, 0.1)';
                this.ctx.fill();
            }
        }
    }
    
    // Physical analog: simulate finding a Kempe chain and flipping its "spin"
    step() {
        // Find a color pair, e.g. (color[0], color[1]) from outer ring to swap
        // A real simulation would trace the connected component
        // For visual sake, we'll pick a node, trace its (a,b) chain, and swap
        
        const candidateStart = Math.floor(Math.random() * 5) + 1; // Pick a neighbor of center
        const colorA = this.nodes[candidateStart].color;
        const colorB = (colorA + 1) % 4; // Arbitrary 2nd color
        
        // Find chain (dumb BFS)
        let chain = new Set([candidateStart]);
        let queue = [candidateStart];
        
        while (queue.length > 0) {
            let curr = queue.shift();
            for (let [u, v] of this.edges) {
                let neighbor = -1;
                if (u === curr) neighbor = v;
                if (v === curr) neighbor = u;
                
                if (neighbor !== -1 && !chain.has(neighbor)) {
                    if (this.nodes[neighbor].color === colorA || this.nodes[neighbor].color === colorB) {
                        chain.add(neighbor);
                        queue.push(neighbor);
                    }
                }
            }
        }
        
        // Flip colors in chain
        let flipped = 0;
        for (let idx of chain) {
            if (this.nodes[idx].color === colorA) {
                this.nodes[idx].color = colorB;
                flipped++;
            } else if (this.nodes[idx].color === colorB) {
                this.nodes[idx].color = colorA;
                flipped++;
            }
        }
        
        this.draw();
        return `Swapped (${colorA},${colorB}) chain of size ${flipped}. Hot potato stress redistributed.`;
    }
}

window.KempeSpinGlass = KempeSpinGlass;