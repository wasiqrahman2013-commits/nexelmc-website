from flask import Flask, render_template_string, jsonify
import os

app = Flask(__name__)

# Homepage HTML
HOME_PAGE = '''
<!DOCTYPE html>
<html>
<head>
    <title>NexelMC</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Inter', Arial, sans-serif; background: #0a0a0a; color: #fff; }
        .navbar { background: #1a1a1a; padding: 1rem 2rem; border-bottom: 1px solid #333; position: sticky; top: 0; }
        .nav-container { max-width: 1200px; margin: 0 auto; display: flex; justify-content: space-between; align-items: center; }
        .nav-logo { color: #ff6b00; font-size: 1.5rem; font-weight: bold; text-decoration: none; }
        .nav-links a { color: #fff; text-decoration: none; margin-left: 2rem; }
        .nav-links a:hover { color: #ff6b00; }
        .hero { text-align: center; padding: 100px 20px; background: linear-gradient(135deg, #1a1a2e, #0a0a0a); }
        .hero h1 { font-size: 3rem; color: #ff6b00; margin-bottom: 1rem; }
        .hero p { font-size: 1.2rem; color: #b0b0b0; margin-bottom: 2rem; }
        .ip { font-size: 1.3rem; background: #1a1a1a; display: inline-block; padding: 10px 20px; border-radius: 10px; margin: 20px 0; font-family: monospace; }
        button { background: #ff6b00; color: #fff; border: none; padding: 12px 24px; font-size: 1rem; border-radius: 8px; cursor: pointer; margin: 10px; }
        button:hover { background: #e55a00; }
        .features, .gamemodes { max-width: 1200px; margin: 0 auto; padding: 60px 20px; }
        h2 { text-align: center; font-size: 2rem; margin-bottom: 2rem; color: #ff6b00; }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 2rem; }
        .card { background: #1a1a1a; padding: 2rem; border-radius: 12px; text-align: center; border: 1px solid #333; }
        .card:hover { border-color: #ff6b00; transform: translateY(-5px); transition: all 0.3s; }
        .card h3 { margin-bottom: 1rem; }
        .card p { color: #b0b0b0; }
        .stats { background: #1a1a2e; padding: 60px 20px; }
        .stats-container { max-width: 1200px; margin: 0 auto; display: grid; grid-template-columns: repeat(4, 1fr); gap: 2rem; text-align: center; }
        .stat-number { font-size: 2.5rem; font-weight: bold; color: #ff6b00; }
        footer { background: #050505; padding: 40px 20px 20px; text-align: center; color: #666; }
        .footer-links a { color: #ff6b00; margin: 0 10px; text-decoration: none; }
        @media (max-width: 768px) { .stats-container { grid-template-columns: repeat(2, 1fr); } .nav-links { display: none; } }
    </style>
</head>
<body>
    <nav class="navbar">
        <div class="nav-container">
            <a href="/" class="nav-logo">⚡ NEXELMC</a>
            <div class="nav-links">
                <a href="/">Home</a>
                <a href="/about">About</a>
                <a href="/rules">Rules</a>
                <a href="/staff">Staff</a>
                <a href="/apply">Apply</a>
                <a href="/vote">Vote</a>
            </div>
        </div>
    </nav>

    <section class="hero">
        <h1>⚡ NEXELMC</h1>
        <p>Next Generation Minecraft Multiplayer</p>
        <div class="ip">play.nexelmc.com</div>
        <button onclick="copyIP()">📋 Copy Server IP</button>
        <br>
        <small>Zero pay-to-win • Active staff • Browser support</small>
    </section>

    <section class="features">
        <h2>Why NexelMC?</h2>
        <div class="grid">
            <div class="card"><h3>⚡ Low Latency</h3><p>Optimized for smooth gameplay worldwide</p></div>
            <div class="card"><h3>🛡️ Anti-Cheat</h3><p>Advanced protection against hackers</p></div>
            <div class="card"><h3>🌐 Browser Support</h3><p>Play from any browser via Eaglercraft</p></div>
            <div class="card"><h3>💬 Active Community</h3><p>Friendly players and dedicated staff</p></div>
        </div>
    </section>

    <section class="gamemodes">
        <h2>Game Modes (Coming Soon)</h2>
        <div class="grid">
            <div class="card"><h3>⚔️ Duels</h3><p>1v1 battles to prove your skill</p></div>
            <div class="card"><h3>🛏️ BedWars</h3><p>Defend your bed, destroy theirs</p></div>
            <div class="card"><h3>🏆 PvP Arena</h3><p>No rules, last man standing</p></div>
            <div class="card"><h3>🌍 Survival</h3><p>Build, explore, thrive with friends</p></div>
        </div>
    </section>

    <section class="stats">
        <div class="stats-container">
            <div><div class="stat-number">100+</div><div>Discord Members</div></div>
            <div><div class="stat-number">24/7</div><div>Uptime</div></div>
            <div><div class="stat-number">0</div><div>Pay-to-Win</div></div>
            <div><div class="stat-number">99.9%</div><div>Anti-Cheat</div></div>
        </div>
    </section>

    <footer>
        <div class="footer-links">
            <a href="/about">About</a> | <a href="/rules">Rules</a> | <a href="/staff">Staff</a> | <a href="/apply">Apply</a> | <a href="/vote">Vote</a>
        </div>
        <p style="margin-top: 20px;">💬 discord.gg/nexelmc | 🌐 play.nexelmc.com</p>
        <p>&copy; 2026 NexelMC. Not affiliated with Mojang.</p>
    </footer>

    <script>
        function copyIP() {
            navigator.clipboard.writeText("play.nexelmc.com");
            alert("✓ Server IP copied!");
        }
    </script>
</body>
</html>
'''

ABOUT_PAGE = '<!DOCTYPE html><html><head><title>About</title><style>body{background:#0a0a0a;color:#fff;font-family:Arial;text-align:center;padding-top:100px;}a{color:#ff6b00;}</style></head><body><h1 style="color:#ff6b00">About NexelMC</h1><p>NexelMC is a next-generation Minecraft server built for fair gameplay, low latency, and an active community.</p><p>We support Eaglercraft (browser) and Java Edition players.</p><a href="/">← Back to Home</a></body></html>'
RULES_PAGE = '<!DOCTYPE html><html><head><title>Rules</title><style>body{background:#0a0a0a;color:#fff;font-family:Arial;padding:50px;}a{color:#ff6b00;}</style></head><body><h1 style="color:#ff6b00">Server Rules</h1><ul><li>Be respectful to all players</li><li>No hacking or cheating</li><li>No spamming or advertising</li><li>Respect staff decisions</li><li>Have fun!</li></ul><a href="/">← Back to Home</a></body></html>'
STAFF_PAGE = '<!DOCTYPE html><html><head><title>Staff</title><style>body{background:#0a0a0a;color:#fff;font-family:Arial;padding:50px;}a{color:#ff6b00;}</style></head><body><h1 style="color:#ff6b00">Staff Team</h1><p><strong>Owner:</strong> wasiq_rahman_yt</p><p><strong>Co-Owner:</strong> Coming Soon</p><p><strong>Admins:</strong> Coming Soon</p><p><strong>Moderators:</strong> Coming Soon</p><p><strong>Helpers:</strong> Coming Soon</p><p><strong>Builders:</strong> Coming Soon</p><a href="/">← Back to Home</a></body></html>'
APPLY_PAGE = '<!DOCTYPE html><html><head><title>Apply</title><style>body{background:#0a0a0a;color:#fff;font-family:Arial;padding:50px;}a{color:#ff6b00;}</style></head><body><h1 style="color:#ff6b00">Apply for Staff</h1><p>We are hiring Builders, Helpers, and Developers!</p><p>DM <strong>wasiq_rahman_yt</strong> on Discord with your application.</p><a href="/">← Back to Home</a></body></html>'
VOTE_PAGE = '<!DOCTYPE html><html><head><title>Vote</title><style>body{background:#0a0a0a;color:#fff;font-family:Arial;padding:50px;}a{color:#ff6b00;}</style></head><body><h1 style="color:#ff6b00">Vote for NexelMC</h1><p>Vote links coming soon! Check back later.</p><a href="/">← Back to Home</a></body></html>'

@app.route('/')
def home():
    return HOME_PAGE

@app.route('/about')
def about():
    return ABOUT_PAGE

@app.route('/rules')
def rules():
    return RULES_PAGE

@app.route('/staff')
def staff():
    return STAFF_PAGE

@app.route('/apply')
def apply():
    return APPLY_PAGE

@app.route('/vote')
def vote():
    return VOTE_PAGE

@app.route('/api/status')
def status():
    return {'online': True, 'players': 0, 'max': 100}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
