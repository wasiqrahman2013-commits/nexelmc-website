from flask import Flask, jsonify
import os

app = Flask(__name__)

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>NexelMC</title>
    <style>
        body { font-family: Arial; background: #0a0a0a; color: #fff; text-align: center; padding-top: 100px; }
        h1 { color: #ff6b00; }
        .ip { font-family: monospace; font-size: 1.2rem; margin: 20px 0; }
        button { background: #ff6b00; color: #fff; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; }
        .links { margin-top: 30px; }
        .links a { color: #ff6b00; margin: 0 10px; text-decoration: none; }
    </style>
</head>
<body>
    <h1>⚡ NEXELMC</h1>
    <p>Next Generation Minecraft Multiplayer</p>
    <div class="ip">play.nexelmc.com</div>
    <button onclick="copyIP()">Copy Server IP</button>
    <div class="links">
        <a href="/about">About</a> | <a href="/rules">Rules</a> | <a href="/staff">Staff</a> | <a href="/apply">Apply</a> | <a href="/vote">Vote</a>
    </div>
    <script>
        function copyIP() {
            navigator.clipboard.writeText("play.nexelmc.com");
            alert("IP copied!");
        }
    </script>
</body>
</html>
'''

ABOUT = '<h1>About NexelMC</h1><p>Coming soon!</p><a href="/">Back</a>'
RULES = '<h1>Server Rules</h1><p>Coming soon!</p><a href="/">Back</a>'
STAFF = '<h1>Staff Team</h1><p>Coming soon!</p><a href="/">Back</a>'
APPLY = '<h1>Apply for Staff</h1><p>Coming soon!</p><a href="/">Back</a>'
VOTE = '<h1>Vote for NexelMC</h1><p>Coming soon!</p><a href="/">Back</a>'

@app.route('/')
def home():
    return HTML

@app.route('/about')
def about():
    return ABOUT

@app.route('/rules')
def rules():
    return RULES

@app.route('/staff')
def staff():
    return STAFF

@app.route('/apply')
def apply():
    return APPLY

@app.route('/vote')
def vote():
    return VOTE

@app.route('/api/status')
def status():
    return {'online': True, 'players': 0}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
