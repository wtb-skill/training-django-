
// Timer logic
let timer = document.getElementById('timer');
let startTime = new Date();

function updateTimer() {
    let currentTime = new Date();
    let elapsedTime = currentTime - startTime;
    let seconds = Math.floor(elapsedTime / 1000 % 60);
    let minutes = Math.floor(elapsedTime / (1000 * 60) % 60);
    let hours = Math.floor(elapsedTime / (1000 * 60 * 60));

    timer.innerHTML = `${hours}h ${minutes}m ${seconds}s`;
}

setInterval(updateTimer, 1000);
