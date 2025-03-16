from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO
from werkzeug.security import generate_password_hash
from datetime import datetime, timezone
import pytz

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Secret key for session management

# Initialize SocketIO after the app
socketio = SocketIO(app)

# In-memory store for users and messages (in a real app, use a database)
users = {}
messages = []

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Validate login
        if users.get(username) == password:
            session['username'] = username
            return redirect(url_for('chat'))
        else:
            return 'Invalid credentials, please try again.'

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Simple check to see if username already exists
        if username in users:
            return 'Username already exists, please choose a different one.'
        else:
            users[username] = password  # Store user (In a real app, store in a database)
            return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if 'username' not in session:
        return redirect(url_for('login'))  # Redirect if not logged in

    username = session['username']
    if request.method == 'POST':
        message_content = request.form['message']
        tz = pytz.timezone('Asia/Kolkata')
        timestamp = datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')
        messages.append({'user': username, 'content': message_content, 'timestamp': timestamp})
        return redirect(url_for('chat'))  # Reload page after posting message

    return render_template('chat.html', messages=messages, current_user=username)

@app.route('/logout')
def logout():
    session.pop('username', None)  # Remove the session data
    return redirect(url_for('login'))

if __name__ == '__main__':
    socketio.run(app, debug=True)
