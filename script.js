$(document).ready(function () {
    const canvas = document.getElementById("particleCanvas");
    if (!canvas) return;
    const ctx = canvas.getContext("2d");

    const PARTICLE_COUNT = 400;
    const CENTER_X = 141;
    const CENTER_Y = 138;
    const MAX_RADIUS = 150;

    const colors = [
        "rgb(255, 255, 255)", 
        "rgb(0, 251, 255)",   
        "rgb(0, 234, 255)",   
        "rgb(0, 255, 247)",   
        "rgb(255, 255, 255)", 
        "rgb(255, 255, 255)"
    ];

    // Generate and store particle properties
    const particles = [];
    for (let i = 0; i < PARTICLE_COUNT; i++) {
        const angle = Math.random() * Math.PI * 5;
        const distance = Math.sqrt(Math.random()) * MAX_RADIUS;
        
        particles.push({
            // Base positions
            baseX: CENTER_X + Math.cos(angle) * distance,
            baseY: CENTER_Y + Math.sin(angle) * distance,
            // Current positions
            x: 0,
            y: 0,
            size: 2 + Math.random() * 3,
            color: colors[Math.floor(Math.random() * colors.length)],
            // Unique speeds/offsets for the "organic drift"
            angleOffset: Math.random() * 1,
            speed: 0.01 + Math.random() * 0.02,
            driftRange: 5 + Math.random() * 10
        });
    }

    // Animation Loop
    function animate() {
        // Clear canvas every frame
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        particles.forEach(p => {
            // Replicate the CSS 'organicDrift' using Math.sin
            p.angleOffset += p.speed;
            const driftX = Math.sin(p.angleOffset) * p.driftRange;
            const driftY = Math.cos(p.angleOffset) * p.driftRange;

            p.x = p.baseX + driftX;
            p.y = p.baseY + driftY;

            // Draw particle
            ctx.beginPath();
            ctx.arc(p.x, p.y, p.size / 2, 0, Math.PI * 2);
            ctx.fillStyle = p.color;
            
            // Optional: Glow effect (Can be taxing, remove if mobile lags)
            ctx.shadowBlur = 5;
            ctx.shadowColor = p.color;

            ctx.fill();
        });

        // Tells browser to animate efficiently
        requestAnimationFrame(animate);
    }

    // Start loop
    animate();
});