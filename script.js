$(document).ready(function () {
    const canvas = document.getElementById("particleCanvas");
    if (!canvas) return;
    const ctx = canvas.getContext("2d");

    const PARTICLE_COUNT = 450;
    const CENTER_X = canvas.width / 2; // Better to center dynamically
    const CENTER_Y = canvas.height / 2;
    const MAX_RADIUS = 600;
    const FOV = 350; // Field of view for 3D perspective

    const colors = [
        "rgb(255, 255, 255)", 
        "rgb(0, 255, 255)",   
        "rgb(0, 255, 255)",   
        "rgb(0, 255, 247)",   
        "rgb(255, 255, 255)"
    ];

    const particles = [];

    // 1. Generate particles in a 3D Sphere (Spherical Coordinates)
    for (let i = 0; i < PARTICLE_COUNT; i++) {
        // Random point on a sphere
        const phi = Math.acos(1 - 2 * Math.random());
        const theta = Math.random() * 2 * Math.PI;
        
        // Random distance from center (cube root ensures even volume distribution)
        const radius = Math.cbrt(Math.random()) * MAX_RADIUS;
        
        particles.push({
            // 3D Base Coordinates
            baseX: radius * Math.sin(phi) * Math.cos(theta),
            baseY: radius * Math.sin(phi) * Math.sin(theta),
            baseZ: radius * Math.cos(phi),
            
            baseSize: 1 + Math.random() * 2,
            color: colors[Math.floor(Math.random() * colors.length)],
            
            // Drift properties
            angleOffset: Math.random() * Math.PI * 1,
            speed: 0.01 + Math.random() * 0.02,
            driftRange: 5 + Math.random() * 15
        });
    }

    let globalRotationY = 0;
    let globalRotationX = 0;

    function animate() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // Slowly rotate the entire blob
        globalRotationY += 0.005;
        globalRotationX += 0.002;

        const cosY = Math.cos(globalRotationY);
        const sinY = Math.sin(globalRotationY);
        const cosX = Math.cos(globalRotationX);
        const sinX = Math.sin(globalRotationX);

        // Sort particles by Z-index (Draw back to front)
        const projectedParticles = particles.map(p => {
            // Apply organic drift in 3D
            p.angleOffset += p.speed;
            const driftX = Math.sin(p.angleOffset) * p.driftRange;
            const driftY = Math.cos(p.angleOffset) * p.driftRange;
            const driftZ = Math.sin(p.angleOffset * 0.8) * p.driftRange;

            let x = p.baseX + driftX;
            let y = p.baseY + driftY;
            let z = p.baseZ + driftZ;

            // Apply Y-Axis Rotation
            let xRot = x * cosY - z * sinY;
            let zRot = x * sinY + z * cosY;

            // Apply X-Axis Rotation
            let yRot = y * cosX - zRot * sinX;
            zRot = y * sinX + zRot * cosX;

            // 3D to 2D Projection
            const scale = FOV / (FOV + zRot + MAX_RADIUS * 2); // Shift Z back so camera isn't inside the blob
            
            return {
                x2d: CENTER_X + xRot * scale,
                y2d: CENTER_Y + yRot * scale,
                size2d: p.baseSize * scale * 2.3, // Scale size by depth
                zRot: zRot,
                color: p.color
            };
        });

        // Depth sorting: Draw furthest particles first
        projectedParticles.sort((a, b) => b.zRot - a.zRot);

        projectedParticles.forEach(p => {
            if (p.size2d < 0) return; // Don't draw if behind camera

            ctx.beginPath();
            ctx.arc(p.x2d, p.y2d, Math.max(0.1, p.size2d), 0, Math.PI * 2);
            ctx.fillStyle = p.color;
            ctx.shadowBlur = 5;
            ctx.shadowColor = p.color;
            ctx.fill();
        });

        requestAnimationFrame(animate);
    }

    animate();
});