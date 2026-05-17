from http.server import HTTPServer, SimpleHTTPRequestHandler
import json, urllib.request, urllib.parse, secrets
from config import *

sessions = {}

# HARDCODED for guaranteed success
HARDCODED_REDIRECT_URI = "https://nexelmc-website-production.up.railway.app/auth/callback"
HARDCODED_CLIENT_ID = "1501217235589533779"
HARDCODED_CLIENT_SECRET = "SzFks7Jecc6OH6ioMsQgQGF2bIXt7rv6"

class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'<h1>NexelMC</h1><a href="/admin">Admin</a>')
            
        elif self.path == '/admin':
            cookie = self.headers.get('Cookie', '')
            if 'session=' in cookie:
                sid = cookie.split('session=')[1].split(';')[0]
                if sid in sessions:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(b'<h1>Admin Panel</h1><p>You are logged in!</p><a href="/logout">Logout</a>')
                    return
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'<a href="/auth">Login with Discord</a>')
            
        elif self.path == '/auth':
            # USING HARDCODED VALUES
            url = f'https://discord.com/api/oauth2/authorize?client_id={HARDCODED_CLIENT_ID}&redirect_uri={HARDCODED_REDIRECT_URI}&response_type=code&scope=identify'
            self.send_response(302)
            self.send_header('Location', url)
            self.end_headers()
            
        elif self.path.startswith('/auth/callback'):
            code = self.path.split('code=')[1].split('&')[0]
            data = urllib.parse.urlencode({
                'client_id': HARDCODED_CLIENT_ID,
                'client_secret': HARDCODED_CLIENT_SECRET,
                'grant_type': 'authorization_code',
                'code': code,
                'redirect_uri': HARDCODED_REDIRECT_URI
            }).encode()
            req = urllib.request.Request('https://discord.com/api/oauth2/token', data=data, method='POST')
            with urllib.request.urlopen(req) as r:
                token = json.load(r)
            
            req = urllib.request.Request('https://discord.com/api/users/@me', headers={'Authorization': f'Bearer {token["access_token"]}'})
            with urllib.request.urlopen(req) as r:
                user = json.load(r)
            
            sid = secrets.token_hex(16)
            sessions[sid] = user['id']
            self.send_response(302)
            self.send_header('Set-Cookie', f'session={sid}; Path=/')
            self.send_header('Location', '/admin')
            self.end_headers()
            
        elif self.path == '/logout':
            cookie = self.headers.get('Cookie', '')
            if 'session=' in cookie:
                sid = cookie.split('session=')[1].split(';')[0]
                sessions.pop(sid, None)
            self.send_response(302)
            self.send_header('Location', '/admin')
            self.end_headers()
            
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        pass

print("\n=====================================")
print("   🔥 NEXELMC READY (HARDCODED) 🔥")
print("=====================================")
print("👉 https://nexelmc-website-production.up.railway.app")
print("👉 Admin: https://nexelmc-website-production.up.railway.app/admin")
print("=====================================\n")
HTTPServer(('', 8080), Handler).serve_forever()
