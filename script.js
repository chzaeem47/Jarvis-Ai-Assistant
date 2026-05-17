$(document).ready(function () {
    const container = document.getElementById("particleContainer");
    
    // Clear out any old lingering cached elements before rendering
    if(container) container.innerHTML = ''; 

    const PARTICLE_COUNT = 250; 

    const colors = [
        "rgba(255, 255, 255, 0.85)",  /* Electric Lime */
        "rgb(0, 253, 236)",   /* Bright Cyan */
        "rgb(2, 250, 246)",   /* Neon Mint */
        "rgb(2, 236, 248)",   /* Hot Pink */
        "rgb(255, 255, 255)", /* Purple Nebula */
        "rgba(255, 255, 255, 0.95)" /* White Highlights */
    ];

    // Centering calculations explicitly mapped for your 290px CSS container
    const CENTER_X = 140; 
    const CENTER_Y = 135; 
    const MAX_RADIUS = 130; /* Keeps particles safely inside the 290px bounds */

    for (let i = 0; i < PARTICLE_COUNT; i++) {
        const spark = document.createElement("div");
        spark.className = "spark";

        // Particle sizing variations
        const size = 1.5 + Math.random() * 2.6;
        spark.style.width = `${size}px`;
        spark.style.height = `${size}px`;

        // Circular Distribution Equation
        const angle = Math.random() * Math.PI *2;
        const distance = Math.sqrt(Math.random()) * MAX_RADIUS;

        // Calculate absolute top/left offset positions from the container's (0,0) corner
        const posX = CENTER_X + Math.cos(angle) * distance;
        const posY = CENTER_Y + Math.sin(angle) * distance;

        spark.style.left = `${posX}px`;
        spark.style.top = `${posY}px`;

        // Style and Color Mapping
        const randomColor = colors[Math.floor(Math.random() * colors.length)];
        spark.style.backgroundColor = randomColor;
        spark.style.boxShadow = `0 0 5px ${randomColor}`;

        // Organic Timing Variations
        const duration = 3.5 + Math.random() * 5.5;
        const delay = Math.random(); 
        
        spark.style.animation = `organicDrift ${duration}s ease-in-out ${delay}s infinite alternate`;

        container.appendChild(spark);
    }
});