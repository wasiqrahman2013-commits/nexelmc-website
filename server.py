from flask import Flask, render_template_string, jsonify, request, redirect, session, url_for
from flask_session import Session
import requests
import os
from datetime import datetime
from config import DISCORD_CLIENT_ID, DISCORD_CLIENT_SECRET, DISCORD_REDIRECT_URI

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Discord OAuth2 endpoints
DISCORD_API_BASE = 'https://discordapp.com/api'
DISCORD_AUTHORIZE_URL = 'https://discord.com/api/oauth2/authorize'
DISCORD_TOKEN_URL = f'{DISCORD_API_BASE}/oauth2/token'
DISCORD_USER_URL = f'{DISCORD_API_BASE}/users/@me'

# Admin user IDs (add your Discord ID here)
ADMIN_IDS = set(os.environ.get('ADMIN_IDS', '').split(',')) if os.environ.get('ADMIN_IDS') else set()

# HTML Templates
TEMPLATES = {
    'base.html': '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}NexelMC | Next Generation Minecraft Multiplayer{% endblock %}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
</head>
<body>
    <nav class="navbar">
        <div class="nav-container">
            <a href="/" class="nav-logo">⚡ NEXELMC</a>
            <div class="nav-links" id="navLinks">
                <a href="/" class="nav-link">Home</a>
                <a href="/about" class="nav-link">About</a>
                <a href="/rules" class="nav-link">Rules</a>
                <a href="/staff" class="nav-link">Staff</a>
                <a href="/apply" class="nav-link">Apply</a>
                <a href="/vote" class="nav-link">Vote</a>
            </div>
            <button class="nav-toggle" id="navToggle">☰</button>
        </div>
    </nav>

    <main>
        {% block content %}{% endblock %}
    </main>

    <footer>
        <div class="footer-container">
            <div class="footer-section">
                <h4>⚡ NexelMC</h4>
                <p>The next generation Minecraft multiplayer experience. Play from your browser or Java Edition.</p>
            </div>
            <div class="footer-section">
                <h4>Quick Links</h4>
                <a href="/about">About</a>
                <a href="/rules">Rules</a>
                <a href="/staff">Staff</a>
                <a href="/apply">Apply</a>
            </div>
            <div class="footer-section">
                <h4>Connect</h4>
                <p>💬 <a href="https://discord.gg/xgbzTgUZuD" target="_blank">discord.gg/nexelmc</a></p>
                <p>🌐 play.nexelmc.com</p>
            </div>
        </div>
        <div class="footer-bottom">
            <p>&copy; 2026 NexelMC. Not affiliated with Mojang AB.</p>
        </div>
    </footer>

    <script>
        document.addEventListener('DOMContentLoaded', function() {
            const toggle = document.querySelector('.nav-toggle');
            const navLinks = document.querySelector('.nav-links');
            
            if (toggle && navLinks) {
                toggle.addEventListener('click', function() {
                    navLinks.classList.toggle('active');
                });
            }

            // Close menu when link is clicked
            document.querySelectorAll('.nav-link').forEach(link => {
                link.addEventListener('click', function() {
                    navLinks.classList.remove('active');
                });
            });
        });
    </script>
</body>
</html>''',

    'index.html': '''{% extends "base.html" %}

{% block content %}
<section class="hero">
    <div class="hero-content">
        <div class="hero-badge">🔥 COMING SOON</div>
        <h1 class="hero-title">Next Generation<br>Minecraft Multiplayer</h1>
        <p class="hero-subtitle">Zero pay-to-win. Active staff. Browser support. Join the revolution.</p>
        <div class="hero-buttons">
            <button class="btn-primary" onclick="copyIP()">📋 Copy Server IP</button>
            <button class="btn-secondary" onclick="window.open('https://discord.gg/xgbzTgUZuD', '_blank')">💬 Join Discord</button>
        </div>
        <div class="server-ip" id="serverIP">play.nexelmc.com</div>
        <div class="server-status">
            <span class="status-dot"></span> Server Status: <span id="serverStatus">Checking...</span>
        </div>
    </div>
</section>

<section class="features">
    <h2 class="section-title">Why NexelMC?</h2>
    <div class="features-grid">
        <div class="feature-card">
            <div class="feature-icon">⚡</div>
            <h3>Low Latency</h3>
            <p>Optimized server performance for smooth gameplay worldwide</p>
        </div>
        <div class="feature-card">
            <div class="feature-icon">🛡️</div>
            <h3>Anti-Cheat</h3>
            <p>Advanced protection against hackers and unfair advantages</p>
        </div>
        <div class="feature-card">
            <div class="feature-icon">🌐</div>
            <h3>Browser Support</h3>
            <p>Play directly from your browser via Eaglercraft</p>
        </div>
        <div class="feature-card">
            <div class="feature-icon">💬</div>
            <h3>Active Community</h3>
            <p>Friendly players and dedicated staff ready to help</p>
        </div>
    </div>
</section>

<section class="gamemodes">
    <h2 class="section-title">Game Modes</h2>
    <div class="gamemodes-grid">
        <div class="gamemode-card">
            <div class="gamemode-icon">⚔️</div>
            <h3>Duels</h3>
            <p>1v1 battles to prove your skill</p>
            <span class="gamemode-status">Coming Soon</span>
        </div>
        <div class="gamemode-card">
            <div class="gamemode-icon">🛏️</div>
            <h3>BedWars</h3>
            <p>Defend your bed, destroy theirs</p>
            <span class="gamemode-status">Coming Soon</span>
        </div>
        <div class="gamemode-card">
            <div class="gamemode-icon">🏆</div>
            <h3>PvP Arena</h3>
            <p>No rules, last man standing</p>
            <span class="gamemode-status">Coming Soon</span>
        </div>
        <div class="gamemode-card">
            <div class="gamemode-icon">🌍</div>
            <h3>Survival</h3>
            <p>Build, explore, thrive with friends</p>
            <span class="gamemode-status">Coming Soon</span>
        </div>
    </div>
</section>

<section class="stats">
    <div class="stats-container">
        <div class="stat">
            <div class="stat-number">100+</div>
            <div class="stat-label">Discord Members</div>
        </div>
        <div class="stat">
            <div class="stat-number">24/7</div>
            <div class="stat-label">Uptime</div>
        </div>
        <div class="stat">
            <div class="stat-number">0</div>
            <div class="stat-label">Pay-to-Win</div>
        </div>
        <div class="stat">
            <div class="stat-number">99.9%</div>
            <div class="stat-label">Anti-Cheat</div>
        </div>
    </div>
</section>

<script>
    function copyIP() {
        navigator.clipboard.writeText("play.nexelmc.com");
        alert("✓ Server IP copied to clipboard!");
    }

    async function checkServerStatus() {
        const statusElement = document.getElementById('serverStatus');
        const dotElement = document.querySelector('.status-dot');
        
        try {
            const response = await fetch('/api/status');
            const data = await response.json();
            
            if (data.online) {
                statusElement.textContent = '🟢 Online';
                if (dotElement) dotElement.style.background = '#00ff00';
            } else {
                statusElement.textContent = '🔴 Offline';
                if (dotElement) dotElement.style.background = '#ff0000';
            }
        } catch (error) {
            statusElement.textContent = '🔴 Offline';
            if (dotElement) dotElement.style.background = '#ff0000';
        }
    }

    checkServerStatus();
    setInterval(checkServerStatus, 30000);
</script>
{% endblock %}''',

    'about.html': '''{% extends "base.html" %}
{% block title %}About | NexelMC{% endblock %}

{% block content %}
<section class="page-header">
    <h1>About NexelMC</h1>
    <p>Learn about our vision and mission</p>
</section>

<section class="about-content">
    <div class="about-section">
        <h2>Our Vision</h2>
        <p>NexelMC is building the next generation of Minecraft multiplayer. We believe in creating a server that prioritizes player experience, fairness, and community. No pay-to-win mechanics, no unfair advantages—just pure, competitive Minecraft gameplay.</p>
    </div>

    <div class="about-section">
        <h2>Our Mission</h2>
        <p>We're on a mission to:</p>
        <ul>
            <li>Provide a lag-free, optimized Minecraft experience</li>
            <li>Maintain a zero pay-to-win policy</li>
            <li>Build an active, welcoming community</li>
            <li>Offer browser-based gameplay via Eaglercraft</li>
            <li>Implement advanced anti-cheat systems</li>
            <li>Support players 24/7 with dedicated staff</li>
        </ul>
    </div>

    <div class="about-section">
        <h2>What Makes Us Different</h2>
        <div class="features-grid">
            <div class="feature-card">
                <div class="feature-icon">🎮</div>
                <h3>Fair Gameplay</h3>
                <p>No pay-to-win. Everyone starts equal.</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">🌐</div>
                <h3>Browser Access</h3>
                <p>Play from any device without Java Edition.</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">👥</div>
                <h3>Community First</h3>
                <p>Active staff and friendly players.</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">⚡</div>
                <h3>Performance</h3>
                <p>Optimized for low latency worldwide.</p>
            </div>
        </div>
    </div>

    <div class="about-section contact-section">
        <h2>Get in Touch</h2>
        <p>Have questions? Join our Discord community!</p>
        <a href="https://discord.gg/xgbzTgUZuD" class="btn-primary" target="_blank">💬 Join Discord</a>
    </div>
</section>
{% endblock %}''',

    'rules.html': '''{% extends "base.html" %}
{% block title %}Rules | NexelMC{% endblock %}

{% block content %}
<section class="page-header">
    <h1>Server Rules</h1>
    <p>Please read and follow these rules to maintain a positive community</p>
</section>

<section class="rules-content">
    <div class="rules-list">
        <div class="rule-card">
            <div class="rule-number">1</div>
            <h3>Be Respectful</h3>
            <p>Treat all players and staff with respect. No harassment, bullying, or discrimination of any kind.</p>
        </div>

        <div class="rule-card">
            <div class="rule-number">2</div>
            <h3>No Hacking or Cheating</h3>
            <p>Using hacks, mods, or exploits is strictly prohibited. Violators will be permanently banned.</p>
        </div>

        <div class="rule-card">
            <div class="rule-number">3</div>
            <h3>No Spam or Flooding</h3>
            <p>Don't spam chat with repeated messages, excessive caps, or flooding.</p>
        </div>

        <div class="rule-card">
            <div class="rule-number">4</div>
            <h3>No Advertising</h3>
            <p>Don't advertise other servers, Discord servers, or external links without permission.</p>
        </div>

        <div class="rule-card">
            <div class="rule-number">5</div>
            <h3>Respect Staff Decisions</h3>
            <p>Staff decisions are final. If you disagree, appeal through our Discord.</p>
        </div>

        <div class="rule-card">
            <div class="rule-number">6</div>
            <h3>Have Fun!</h3>
            <p>This is a game. Enjoy yourself, make friends, and be part of our community.</p>
        </div>

        <div class="rule-card">
            <div class="rule-number">7</div>
            <h3>No Griefing or Stealing</h3>
            <p>Respect other players' builds and belongings. Griefing and stealing will result in punishment.</p>
        </div>

        <div class="rule-card">
            <div class="rule-number">8</div>
            <h3>No Inappropriate Content</h3>
            <p>Keep chat family-friendly. No NSFW content, hate speech, or offensive language.</p>
        </div>

        <div class="rule-card">
            <div class="rule-number">9</div>
            <h3>Report Issues</h3>
            <p>If you see rule violations or bugs, report them to staff immediately.</p>
        </div>
    </div>

    <div class="rules-footer">
        <h3>Punishment Policy</h3>
        <p><strong>First Offense:</strong> Warning</p>
        <p><strong>Second Offense:</strong> Temporary Mute/Ban (24 hours)</p>
        <p><strong>Third Offense:</strong> Extended Ban (7 days)</p>
        <p><strong>Severe Violations:</strong> Permanent Ban</p>
    </div>
</section>
{% endblock %}''',

    'staff.html': '''{% extends "base.html" %}
{% block title %}Staff | NexelMC{% endblock %}

{% block content %}
<section class="page-header">
    <h1>Our Staff Team</h1>
    <p>Meet the people keeping NexelMC running smoothly</p>
</section>

<section class="staff-content">
    <div class="staff-roles">
        <div class="staff-role">
            <h3>👑 Owner</h3>
            <div class="staff-members">
                <div class="staff-member">
                    <div class="staff-avatar">👑</div>
                    <p class="staff-name">wasiq_rahman_yt</p>
                    <p class="staff-title">Founder & Lead</p>
                </div>
            </div>
        </div>

        <div class="staff-role">
            <h3>🔱 Co-Owner</h3>
            <div class="staff-members">
                <div class="staff-member">
                    <div class="staff-avatar">🔱</div>
                    <p class="staff-name">Coming Soon</p>
                    <p class="staff-title">Co-Owner</p>
                </div>
            </div>
        </div>

        <div class="staff-role">
            <h3>⚙️ Admins</h3>
            <div class="staff-members">
                <div class="staff-member">
                    <div class="staff-avatar">⚙️</div>
                    <p class="staff-name">Coming Soon</p>
                    <p class="staff-title">Administrator</p>
                </div>
            </div>
        </div>

        <div class="staff-role">
            <h3>📋 Managers</h3>
            <div class="staff-members">
                <div class="staff-member">
                    <div class="staff-avatar">📋</div>
                    <p class="staff-name">Coming Soon</p>
                    <p class="staff-title">Manager</p>
                </div>
            </div>
        </div>

        <div class="staff-role">
            <h3>💻 Developers</h3>
            <div class="staff-members">
                <div class="staff-member">
                    <div class="staff-avatar">💻</div>
                    <p class="staff-name">Coming Soon</p>
                    <p class="staff-title">Lead Developer</p>
                </div>
            </div>
        </div>

        <div class="staff-role">
            <h3>🛡️ Moderators</h3>
            <div class="staff-members">
                <div class="staff-member">
                    <div class="staff-avatar">🛡️</div>
                    <p class="staff-name">Coming Soon</p>
                    <p class="staff-title">Moderator</p>
                </div>
            </div>
        </div>

        <div class="staff-role">
            <h3>🤝 Helpers</h3>
            <div class="staff-members">
                <div class="staff-member">
                    <div class="staff-avatar">🤝</div>
                    <p class="staff-name">Coming Soon</p>
                    <p class="staff-title">Helper</p>
                </div>
            </div>
        </div>

        <div class="staff-role">
            <h3>🏗️ Builders</h3>
            <div class="staff-members">
                <div class="staff-member">
                    <div class="staff-avatar">🏗️</div>
                    <p class="staff-name">Coming Soon</p>
                    <p class="staff-title">Builder</p>
                </div>
            </div>
        </div>
    </div>

    <div class="staff-footer">
        <h3>Interested in Joining Staff?</h3>
        <p>We're always looking for dedicated community members to join our team!</p>
        <a href="/apply" class="btn-primary">Apply Now</a>
    </div>
</section>
{% endblock %}''',

    'apply.html': '''{% extends "base.html" %}
{% block title %}Apply | NexelMC{% endblock %}

{% block content %}
<section class="page-header">
    <h1>Join Our Team</h1>
    <p>Help us build the best Minecraft community</p>
</section>

<section class="apply-content">
    <div class="apply-intro">
        <h2>We're Hiring!</h2>
        <p>NexelMC is looking for passionate community members to join our staff team.</p>
    </div>

    <div class="apply-positions">
        <div class="position-card">
            <div class="position-icon">🏗️</div>
            <h3>Builder</h3>
            <p>Help us create amazing worlds and structures.</p>
            <ul>
                <li>Design and build server worlds</li>
                <li>Create custom structures</li>
                <li>Maintain server aesthetics</li>
            </ul>
            <a href="https://forms.gle/builder-form" class="btn-primary" target="_blank">Apply as Builder</a>
        </div>

        <div class="position-card">
            <div class="position-icon">🤝</div>
            <h3>Helper</h3>
            <p>Assist players and help maintain a positive community.</p>
            <ul>
                <li>Help new players</li>
                <li>Answer questions</li>
                <li>Report issues to staff</li>
            </ul>
            <a href="https://forms.gle/helper-form" class="btn-primary" target="_blank">Apply as Helper</a>
        </div>

        <div class="position-card">
            <div class="position-icon">💻</div>
            <h3>Developer</h3>
            <p>Build the future of NexelMC.</p>
            <ul>
                <li>Develop server plugins</li>
                <li>Fix bugs and optimize code</li>
                <li>Implement new features</li>
            </ul>
            <a href="https://forms.gle/developer-form" class="btn-primary" target="_blank">Apply as Developer</a>
        </div>
    </div>

    <div class="apply-requirements">
        <h2>General Requirements</h2>
        <ul>
            <li>Must be 13+ years old</li>
            <li>Active Discord member</li>
            <li>Respectful and mature behavior</li>
            <li>Commitment to the community</li>
        </ul>
    </div>

    <div class="apply-footer">
        <h3>Questions?</h3>
        <p>Join our Discord and ask staff members directly!</p>
        <a href="https://discord.gg/xgbzTgUZuD" class="btn-secondary" target="_blank">💬 Join Discord</a>
    </div>
</section>
{% endblock %}''',

    'vote.html': '''{% extends "base.html" %}
{% block title %}Vote | NexelMC{% endblock %}

{% block content %}
<section class="page-header">
    <h1>Vote for NexelMC</h1>
    <p>Help us grow by voting on server lists</p>
</section>

<section class="vote-content">
    <div class="vote-intro">
        <h2>Support NexelMC</h2>
        <p>Voting helps us grow and reach more players. Every vote counts!</p>
    </div>

    <div class="vote-sites">
        <div class="vote-card">
            <div class="vote-icon">🎮</div>
            <h3>Minecraft Server List</h3>
            <p>Vote on the official Minecraft server list</p>
            <a href="#" class="btn-primary" target="_blank">Vote Here</a>
        </div>

        <div class="vote-card">
            <div class="vote-icon">⭐</div>
            <h3>Server.pro</h3>
            <p>Rate and vote for NexelMC on Server.pro</p>
            <a href="#" class="btn-primary" target="_blank">Vote Here</a>
        </div>

        <div class="vote-card">
            <div class="vote-icon">🏆</div>
            <h3>TopG</h3>
            <p>Support us on TopG server list</p>
            <a href="#" class="btn-primary" target="_blank">Vote Here</a>
        </div>
    </div>

    <div class="vote-rewards">
        <h2>Vote Rewards</h2>
        <ul>
            <li>💰 In-game currency</li>
            <li>🎁 Exclusive cosmetics</li>
            <li>⭐ Voting streaks</li>
            <li>🏅 Special badges</li>
        </ul>
    </div>

    <div class="vote-footer">
        <h3>Thank You!</h3>
        <p>Your support means everything to us. Thank you for voting!</p>
    </div>
</section>
{% endblock %}'''
}

# Routes
@app.route('/')
def index():
    return render_template_string(TEMPLATES['base.html'] + TEMPLATES['index.html'])

@app.route('/about')
def about():
    return render_template_string(TEMPLATES['base.html'] + TEMPLATES['about.html'])

@app.route('/rules')
def rules():
    return render_template_string(TEMPLATES['base.html'] + TEMPLATES['rules.html'])

@app.route('/staff')
def staff():
    return render_template_string(TEMPLATES['base.html'] + TEMPLATES['staff.html'])

@app.route('/apply')
def apply():
    return render_template_string(TEMPLATES['base.html'] + TEMPLATES['apply.html'])

@app.route('/vote')
def vote():
    return render_template_string(TEMPLATES['base.html'] + TEMPLATES['vote.html'])

# API Endpoint
@app.route('/api/status')
def api_status():
    return jsonify({
        'online': True,
        'players': 0,
        'max': 100,
        'timestamp': datetime.now().isoformat()
    })

# Discord OAuth2 Routes
@app.route('/login')
def login():
    return redirect(f'{DISCORD_AUTHORIZE_URL}?client_id={DISCORD_CLIENT_ID}&redirect_uri={DISCORD_REDIRECT_URI}&response_type=code&scope=identify%20email')

@app.route('/callback')
def callback():
    code = request.args.get('code')
    if not code:
        return redirect('/')
    
    data = {
        'client_id': DISCORD_CLIENT_ID,
        'client_secret': DISCORD_CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': DISCORD_REDIRECT_URI,
        'scope': 'identify email'
    }
    
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = requests.post(DISCORD_TOKEN_URL, data=data, headers=headers)
    
    if response.status_code != 200:
        return redirect('/')
    
    token_data = response.json()
    access_token = token_data.get('access_token')
    
    user_response = requests.get(DISCORD_USER_URL, headers={'Authorization': f'Bearer {access_token}'})
    user_data = user_response.json()
    
    session['user_id'] = user_data.get('id')
    session['username'] = user_data.get('username')
    session['access_token'] = access_token
    
    return redirect('/admin')

@app.route('/admin')
def admin():
    if 'user_id' not in session:
        return redirect('/login')
    
    user_id = session.get('user_id')
    if user_id not in ADMIN_IDS:
        return 'Unauthorized', 403
    
    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Admin Panel | NexelMC</title>
        <link rel="stylesheet" href="{url_for('static', filename='style.css')}">
    </head>
    <body>
        <div style="padding: 2rem; max-width: 800px; margin: 0 auto;">
            <h1>Admin Panel</h1>
            <p>Welcome, {session.get('username')}!</p>
            <p>User ID: {user_id}</p>
            <a href="/logout" class="btn-primary">Logout</a>
        </div>
    </body>
    </html>
    '''

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
