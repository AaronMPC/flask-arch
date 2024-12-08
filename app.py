from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Random secret key for session handling

@app.route('/')
def home():
    # Check if the user is logged in, otherwise redirect to login
    if 'logged_in' in session and session['logged_in']:
        return redirect(url_for('index'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Handle login form submission
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username == 'admin' and password == 'password':  # Simple validation
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            error = "Invalid credentials!"
            return render_template('login.html', error=error)
    
    return render_template('login.html')

@app.route('/index')
def index():
    # Serve the oven control page (after login)
    if 'logged_in' in session and session['logged_in']:
        return render_template('index.html')
    return redirect(url_for('login'))

@app.route('/start_timer/<int:duration>/<int:min_temp>/<int:max_temp>')
def start_timer(duration, min_temp, max_temp):
    # Handle start timer request (This can trigger real heater control in your system)
    return {'status': 'Timer started', 'duration': duration, 'min_temp': min_temp, 'max_temp': max_temp}

@app.route('/stop_timer')
def stop_timer():
    # Handle stop timer request (This can stop heater control in your system)
    return {'status': 'Timer stopped'}

if __name__ == '__main__':
    app.run(debug=True)
