from flask import Flask, render_template, request, send_file, abort, render_template_string, redirect, url_for, jsonify, session
import psutil, json, os
from functools import wraps
app = Flask(__name__)
app.secret_key = 'jTTg8Mj8fE9hCXEnLMzCqWaLrXhhXXqL'

users = {
    "LoadingQ": "LoadingQ1S0NT0P",
    "admin": "admin"
}

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        try:
          if users[request.form['username']] and request.form['password'] == users[request.form['username']]:
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        except Exception as e:
            error = f'Invalid Credentials. Please try again. {e}'
        else:
            error = 'Invalid Credentials. Please try again.'

    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))
@app.route('/reboot')
def reboot():
    os.system("sudo reboot")
    return render_template('reboot.html')


@app.route('/')
@login_required
def redi():
    return redirect("/dashboard", code=302)
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
          <style>
                  .sidebar {
            position: fixed;
            left: 0;
            top: 0;
            width: 200px;
            height: 100%;
            background-color: #333;
            padding: 20px;
            box-sizing: border-box;
        }
        .sidebar a {
            color: #fff;
            text-decoration: none;
            display: block;
            padding: 10px;
            transition: background 0.3s, color 0.3s;
        }
        .sidebar a:hover {
            background-color: #575757;
            color: white;
        }
        .main-content {
            margin-left: 220px;
            padding: 20px;
        }
          </style>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Status Dashboard</title>
            <script src="https://cdn.tailwindcss.com"></script>
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css"></link>
            <script>
                function updateSystemInfo() {
                    fetch('/info')
                        .then(response => response.json())
                        .then(data => {
                            document.getElementById('ram_usage').innerText = data.ram + '% RAM usage';
                            document.getElementById('cpu_usage').innerText = data.cpu + '% CPU usage';
                            document.getElementById('ram_bar').style.width = data.ram + '%';
                            document.getElementById('cpu_bar').style.width = data.cpu + '%';
                        });
                }

                // Call updateSystemInfo immediately, and then every 1000 milliseconds
                document.addEventListener('DOMContentLoaded', function() {
                    updateSystemInfo();
                    setInterval(updateSystemInfo, 1000);
                });
            </script>
        </head>
    <div class="sidebar">
    <div id="chat-links"></div>
      <a href="/logout">
    <button id="add-chat" style="color: #fff; text-decoration: none; display: block; padding: 10px; text-align: left; background-color: #333; border: none; width: 100%; cursor: pointer;">Logout</button>
      </a>
      <a href="/reboot">
    <button id="add-chat" style="color: #fff; text-decoration: none; display: block; padding: 10px; text-align: left; background-color: #333; border: none; width: 100%; cursor: pointer;">Reboot</button>
      </a>
    </div>
        <body class="bg-gray-100 font-sans leading-normal tracking-normal">
          <div class="main-content">
            <div class="container mx-auto p-4">
                <!-- Status Section -->
                <div class="bg-white shadow-md rounded p-4">
                    <div class="flex items-center mb-4">
                        <i class="fas fa-server text-blue-500 mr-2"></i>
                        <h3 class="font-medium text-lg">Service Status</h3>
                    </div>
                    <div class="mb-4">
                        <div class="flex justify-between items-center mb-2">
                            <h5 class="font-bold text-sm" id="ram_usage">Loading RAM usage...</h5>
                            <span class="text-sm text-green-500">Operational</span>
                        </div>
                        <div class="w-full bg-gray-200 rounded-full h-2 mb-4">
                            <div class="bg-green-500 h-2 rounded-full" id="ram_bar" style="width:0%"></div>
                        </div>
                    </div>
                    <div class="mb-4">
                        <div class="flex justify-between items-center mb-2">
                            <h5 class="font-bold text-sm" id="cpu_usage">Loading CPU usage...</h5>
                            <span class="text-sm text-green-500">Operational</span>
                        </div>
                        <div class="w-full bg-gray-200 rounded-full h-2 mb-4">
                            <div class="bg-green-500 h-2 rounded-full" id="cpu_bar" style="width:0%"></div>
                        </div>
                    </div>
                </div>
              </div>
            </div>
        </body>

        </html>
    ''')

# Route to get the current CPU and RAM usage
@app.route('/info')
def info():
    cpu_usage = psutil.cpu_percent()
    ram_usage = psutil.virtual_memory().percent
    return jsonify(cpu=cpu_usage, ram=ram_usage)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
