let currentTemp = 0;
let remainingTime;
let timerInterval;
let fluctuationInterval;
let fluctuationRange = { min: 50, max: 70 };
let fanSpeed = 0;

function updateTemperature() {
    document.getElementById('temperature-value').innerText = `${currentTemp.toFixed(2)} °C`;
}

function updateFanSpeed() {
    document.getElementById('fan-speed-value').innerText = `${fanSpeed.toFixed(2)}%`;
    document.getElementById('fan-progress').value = fanSpeed;
}

function updateTimerProgress() {
    const progressValue = (1 - remainingTime / (2 * 60 * 60)) * 100;
    document.getElementById('timer-progress').value = progressValue;
}

function startFluctuation(min, max) {
    if (fluctuationInterval) clearInterval(fluctuationInterval);

    fluctuationInterval = setInterval(() => {
        if (remainingTime <= 0) {
            clearInterval(fluctuationInterval);
        } else {
            currentTemp = Math.random() * (max - min) + min;
            adjustFanSpeed(currentTemp, min, max);
            updateTemperature();
        }
    }, 2000);
}

function adjustFanSpeed(temp, min, max) {
    const fanSpeedPercentage = Math.max(0, Math.min(100, 100 - ((temp - min) / (max - min)) * 100));
    fanSpeed = fanSpeedPercentage;
    updateFanSpeed();
}

function startTimer(duration, min, max) {
    remainingTime = duration;
    if (timerInterval) clearInterval(timerInterval);

    timerInterval = setInterval(() => {
        let hours = Math.floor(remainingTime / 3600);
        let minutes = Math.floor((remainingTime % 3600) / 60);
        let seconds = remainingTime % 60;

        document.getElementById('timer-value').innerText =
            `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;

        updateTimerProgress();

        if (remainingTime <= 0) {
            clearInterval(timerInterval);
            alert('Timer finished!');
        } else {
            remainingTime--;
        }
    }, 1000);

    startFluctuation(min, max);
}

document.getElementById('start-2hr').onclick = () => startTimer(2 * 60 * 60, 50, 70);
document.getElementById('start-30min').onclick = () => startTimer(30 * 60, 50, 70);
document.getElementById('stop-timer').onclick = () => {
    clearInterval(timerInterval);
    clearInterval(fluctuationInterval);
    remainingTime = 0;
    document.getElementById('timer-value').innerText = '00:00:00';
    document.getElementById('timer-progress').value = 0;
};
