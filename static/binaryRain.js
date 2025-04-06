const canvas = document.getElementById("binaryCanvas");
const ctx = canvas.getContext("2d");

// Set canvas to full screen
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

// Characters for the binary rain
const binaryChars = "01";
const fontSize = 16;
const columns = canvas.width / fontSize;

// Array to store the y-coordinate of each column
const drops = Array(Math.floor(columns)).fill(0);

// Colors for the binary rain
const colors = ["#0f0", "#0a0", "#0ff"]; // Green, dark green, and cyan

// Draw the binary rain
function draw() {
    // Set the background to a translucent black to create the fading effect
    ctx.fillStyle = "rgba(0, 0, 0, 0.05)";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Set the text font
    ctx.font = `${fontSize}px monospace`;

    // Loop through each column
    for (let i = 0; i < drops.length; i++) {
        // Get a random binary character
        const text = binaryChars[Math.floor(Math.random() * binaryChars.length)];

        // Randomly select a color for the character
        const color = colors[Math.floor(Math.random() * colors.length)];
        ctx.fillStyle = color;

        // Draw the character at the current position
        ctx.fillText(text, i * fontSize, drops[i] * fontSize);

        // Randomly reset the drop to the top of the screen
        if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) {
            drops[i] = 0;
        }

        // Increment the y-coordinate for the drop
        drops[i]++;
    }
}

// Update the canvas every 50 milliseconds
setInterval(draw, 50);

// Adjust canvas size on window resize
window.addEventListener("resize", () => {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
});