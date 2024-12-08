from flask import Flask, render_template, jsonify
import random
import time

app = Flask(__name__)

# Variables to manage temperature, fan speed, and timer
current_temp = 0
remaining_time = 0
fan_speed = 0
timer_interval = None
fluctuation_interval = None

# Fluctuation range (min, max)
fluctuation_range = {"min": 50, "max": 70}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_timer/<int:duration>/<int:min_temp>/<int:max_temp>')
def start_timer(duration, min_temp, max_temp):
    global remaining_time, fluctuation_range
    remaining_time = duration
    fluctuation_range = {"min": min_temp, "max": max_temp}
    start_fluctuation(min_temp, max_temp)
    return jsonify({"status": "timer_started"})


@app.route('/stop_timer')
def stop_timer():
    global remaining_time, current_temp, fan_speed
    remaining_time = 0
    current_temp = 0
    fan_speed = 0
    return jsonify({"status": "timer_stopped"})

def start_fluctuation(min_temp, max_temp):
    global current_temp, fan_speed, fluctuation_interval

    if fluctuation_interval:
        fluctuation_interval.cancel()

    fluctuation_interval = time.time()  # This is a mock; use threading for actual timing

    # Random fluctuation for the temperature between min and max
    current_temp = random.uniform(min_temp, max_temp)
    adjust_fan_speed(current_temp, min_temp, max_temp)


def adjust_fan_speed(temp, min_temp, max_temp):
    global fan_speed
    # Inversely map the temperature to fan speed
    fan_speed = max(0, min(100, 100 - ((temp - min_temp) / (max_temp - min_temp)) * 100))


if __name__ == '__main__':
    app.run(debug=True, port=5000)
