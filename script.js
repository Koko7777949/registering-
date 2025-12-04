// Canvas setup
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

// Set canvas size
canvas.width = 800;
canvas.height = 500;

// Game variables
const paddleWidth = 10;
const paddleHeight = 100;
const ballSize = 10;

let gameRunning = false;
let gamePaused = false;
let animationId = null;

// Paddle objects
const player1 = {
    x: 20,
    y: canvas.height / 2 - paddleHeight / 2,
    width: paddleWidth,
    height: paddleHeight,
    dy: 0,
    speed: 6,
    score: 0
};

const player2 = {
    x: canvas.width - 30,
    y: canvas.height / 2 - paddleHeight / 2,
    width: paddleWidth,
    height: paddleHeight,
    dy: 0,
    speed: 6,
    score: 0
};

// Ball object
const ball = {
    x: canvas.width / 2,
    y: canvas.height / 2,
    size: ballSize,
    dx: 4,
    dy: 4,
    speed: 4
};

// Keyboard state
const keys = {};

// Event listeners
document.getElementById('startBtn').addEventListener('click', startGame);
document.getElementById('restartBtn').addEventListener('click', restartGame);

window.addEventListener('keydown', (e) => {
    keys[e.key.toLowerCase()] = true;
    if (e.key === ' ') {
        e.preventDefault();
        if (gameRunning) {
            togglePause();
        }
    }
});

window.addEventListener('keyup', (e) => {
    keys[e.key.toLowerCase()] = false;
});

// Game functions
function startGame() {
    if (!gameRunning) {
        gameRunning = true;
        document.getElementById('startBtn').style.display = 'none';
        document.getElementById('restartBtn').style.display = 'inline-block';
        gameLoop();
    }
}

function restartGame() {
    // Reset scores
    player1.score = 0;
    player2.score = 0;
    updateScore();
    
    // Reset positions
    resetPositions();
    
    // Resume game if paused
    gamePaused = false;
    
    if (!gameRunning) {
        startGame();
    }
}

function togglePause() {
    gamePaused = !gamePaused;
    if (!gamePaused) {
        gameLoop();
    }
}

function resetPositions() {
    player1.y = canvas.height / 2 - paddleHeight / 2;
    player2.y = canvas.height / 2 - paddleHeight / 2;
    ball.x = canvas.width / 2;
    ball.y = canvas.height / 2;
    
    // Randomize initial ball direction
    ball.dx = (Math.random() > 0.5 ? 1 : -1) * ball.speed;
    ball.dy = (Math.random() > 0.5 ? 1 : -1) * ball.speed;
}

function updateScore() {
    document.getElementById('player1Score').textContent = player1.score;
    document.getElementById('player2Score').textContent = player2.score;
}

function movePaddles() {
    // Player 1 controls (W/S)
    if (keys['w'] && player1.y > 0) {
        player1.y -= player1.speed;
    }
    if (keys['s'] && player1.y < canvas.height - player1.height) {
        player1.y += player1.speed;
    }
    
    // Player 2 controls (Arrow Up/Down)
    if (keys['arrowup'] && player2.y > 0) {
        player2.y -= player2.speed;
    }
    if (keys['arrowdown'] && player2.y < canvas.height - player2.height) {
        player2.y += player2.speed;
    }
}

function moveBall() {
    ball.x += ball.dx;
    ball.y += ball.dy;
    
    // Wall collision (top and bottom)
    if (ball.y - ball.size <= 0 || ball.y + ball.size >= canvas.height) {
        ball.dy *= -1;
    }
    
    // Paddle collision
    // Player 1 paddle
    if (ball.x - ball.size <= player1.x + player1.width &&
        ball.x - ball.size >= player1.x &&
        ball.y >= player1.y &&
        ball.y <= player1.y + player1.height) {
        ball.dx = Math.abs(ball.dx);
        
        // Add spin based on where ball hits paddle
        const hitPos = (ball.y - player1.y) / player1.height;
        ball.dy = (hitPos - 0.5) * 8;
    }
    
    // Player 2 paddle
    if (ball.x + ball.size >= player2.x &&
        ball.x + ball.size <= player2.x + player2.width &&
        ball.y >= player2.y &&
        ball.y <= player2.y + player2.height) {
        ball.dx = -Math.abs(ball.dx);
        
        // Add spin based on where ball hits paddle
        const hitPos = (ball.y - player2.y) / player2.height;
        ball.dy = (hitPos - 0.5) * 8;
    }
    
    // Score points
    if (ball.x - ball.size <= 0) {
        player2.score++;
        updateScore();
        resetPositions();
    }
    
    if (ball.x + ball.size >= canvas.width) {
        player1.score++;
        updateScore();
        resetPositions();
    }
}

function draw() {
    // Clear canvas
    ctx.fillStyle = '#1a1a2e';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    // Draw center line
    ctx.strokeStyle = '#444';
    ctx.lineWidth = 2;
    ctx.setLineDash([10, 10]);
    ctx.beginPath();
    ctx.moveTo(canvas.width / 2, 0);
    ctx.lineTo(canvas.width / 2, canvas.height);
    ctx.stroke();
    ctx.setLineDash([]);
    
    // Draw paddles
    ctx.fillStyle = '#00ff00';
    ctx.fillRect(player1.x, player1.y, player1.width, player1.height);
    
    ctx.fillStyle = '#ff0000';
    ctx.fillRect(player2.x, player2.y, player2.width, player2.height);
    
    // Draw ball
    ctx.fillStyle = '#ffff00';
    ctx.beginPath();
    ctx.arc(ball.x, ball.y, ball.size, 0, Math.PI * 2);
    ctx.fill();
    
    // Draw pause text if paused
    if (gamePaused) {
        ctx.fillStyle = 'rgba(255, 255, 255, 0.8)';
        ctx.font = 'bold 48px Courier New';
        ctx.textAlign = 'center';
        ctx.fillText('PAUSED', canvas.width / 2, canvas.height / 2);
        ctx.font = '20px Courier New';
        ctx.fillText('Press SPACE to resume', canvas.width / 2, canvas.height / 2 + 40);
    }
}

function gameLoop() {
    if (!gameRunning) return;
    
    if (!gamePaused) {
        movePaddles();
        moveBall();
        draw();
        animationId = requestAnimationFrame(gameLoop);
    } else {
        draw(); // Still draw the paused state
    }
}

// Initial draw
draw();