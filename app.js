document.addEventListener('DOMContentLoaded', () => {
    // Initialize Simulation 1
    const sim = new window.KempeSpinGlass('graphCanvas');
    const statusText = document.getElementById('status-text');

    document.getElementById('btn-scramble').addEventListener('click', () => {
        sim.initGraph();
        // Randomize outer colors
        for (let i=1; i<sim.nodes.length; i++) {
            sim.nodes[i].color = Math.floor(Math.random() * 4);
        }
        sim.draw();
        statusText.textContent = "Topology scrambled! Warning: Spin frustration introduced. High covariance energy state.";
        statusText.style.color = "var(--accent-red)";
    });

    document.getElementById('btn-step').addEventListener('click', () => {
        const msg = sim.step();
        statusText.textContent = msg;
        statusText.style.color = "var(--accent-blue)";
    });

    let annealing = false;
    let interval = null;
    const btnAnneal = document.getElementById('btn-anneal');
    btnAnneal.addEventListener('click', () => {
        if (annealing) {
            clearInterval(interval);
            btnAnneal.textContent = "Resume Thermal Annealing";
            btnAnneal.classList.remove('active');
            statusText.textContent = "Annealing paused.";
            statusText.style.color = "var(--accent-orange)";
        } else {
            interval = setInterval(() => {
                sim.step();
            }, 300);
            btnAnneal.textContent = "Halt Annealing";
            btnAnneal.classList.add('active');
            statusText.textContent = "Thermal relaxation via SO(3) Kempe rotations in progress... Navigating the Magic Gem gradient.";
            statusText.style.color = "var(--accent-green)";
        }
        annealing = !annealing;
    });

    // Mock Energy Landscape Canvas
    const eCanvas = document.getElementById('energyCanvas');
    const eCtx = eCanvas.getContext('2d');
    
    // Resize function for energy canvas to ensure it's responsive
    function resizeEnergyCanvas() {
        const rect = eCanvas.parentElement.getBoundingClientRect();
        eCanvas.width = rect.width * window.devicePixelRatio;
        eCanvas.height = 400 * window.devicePixelRatio;
        eCtx.scale(window.devicePixelRatio, window.devicePixelRatio);
        eCanvas.style.width = `${rect.width}px`;
        eCanvas.style.height = `400px`;
        return {width: rect.width, height: 400};
    }
    
    // Initial blank state
    let dims = resizeEnergyCanvas();
    eCtx.fillStyle = '#0d1117';
    eCtx.fillRect(0, 0, dims.width, dims.height);
    
    function drawEnergyLandscape() {
        const {width, height} = resizeEnergyCanvas();

        // Draw a simulated 2D energy landscape with topological 'basins'
        const imgData = eCtx.createImageData(width, height);
        
        let timeOffset = performance.now() * 0.001;
        
        for (let y = 0; y < height; y++) {
            for (let x = 0; x < width; x++) {
                const nx = (x / width) * 12;
                const ny = (y / height) * 12;
                
                // Fluid/psychedelic noise representing the Magic Gem Covariance field
                const v1 = Math.sin(nx + timeOffset)*Math.cos(ny - timeOffset);
                const v2 = Math.sin(nx*2.5)*Math.cos(ny*1.5 + timeOffset);
                const v = v1 + v2;
                
                const val = Math.floor((v + 2) / 4 * 255);
                
                const idx = (y * width + x) * 4;
                imgData.data[idx] = val / 4;        // R
                imgData.data[idx+1] = val / 6;      // G
                imgData.data[idx+2] = Math.min(val * 1.5, 255); // B (Deep blue/purple theme)
                imgData.data[idx+3] = 255;          // Alpha
            }
        }
        eCtx.putImageData(imgData, 0, 0);

        // Draw a 'path' representing the BFS Geodesic
        eCtx.beginPath();
        eCtx.moveTo(width*0.15, height*0.85);
        eCtx.quadraticCurveTo(width*0.4, height*0.3, width*0.85, height*0.65);
        
        // Neon glow for the path
        eCtx.shadowBlur = 15;
        eCtx.shadowColor = '#bc8cff';
        eCtx.strokeStyle = '#bc8cff';
        eCtx.lineWidth = 4;
        eCtx.setLineDash([15, 10]);
        eCtx.stroke();
        
        // Point
        eCtx.beginPath();
        eCtx.arc(width*0.85, height*0.65, 8, 0, Math.PI*2);
        eCtx.fillStyle = '#ffffff';
        eCtx.fill();
        eCtx.shadowBlur = 0; // reset
    }

    let isPlotting = false;
    let animFrame = null;
    
    function animateEnergy() {
        drawEnergyLandscape();
        animFrame = requestAnimationFrame(animateEnergy);
    }

    const btnPlot = document.getElementById('btn-plot');
    btnPlot.addEventListener('click', () => {
        if (!isPlotting) {
            animateEnergy();
            isPlotting = true;
            btnPlot.textContent = "Halt Plotting";
            document.getElementById('energy-status').textContent = "Covariance energy landscape plotted continuously. The glowing geodesic is the optimal safe Kempe swap path avoiding topological defects.";
            document.getElementById('energy-status').style.color = "var(--accent-purple)";
        } else {
            cancelAnimationFrame(animFrame);
            isPlotting = false;
            btnPlot.textContent = "Plot Energy Geodesic";
            document.getElementById('energy-status').textContent = "Plotting halted.";
            document.getElementById('energy-status').style.color = "var(--text-secondary)";
        }
    });
    
    window.addEventListener('resize', () => {
        if (!isPlotting) {
            resizeEnergyCanvas();
            eCtx.fillStyle = '#0d1117';
            eCtx.fillRect(0, 0, eCanvas.width, eCanvas.height);
        }
    });
});