from flask import Flask, request, render_template_string, redirect, url_for, make_response, render_template
from flask_wtf.csrf import CSRFProtect
from flask_talisman import Talisman

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret-dev-key-12345'

# Global toggle to switch between Vulnerable and Secure modes for the lab
SECURITY_ENABLED = False

# Simulated Multi-User Database
users_db = {
    "alice": {"username": "Alice", "bio": "Welcome to my profile!", "password": "Password123"},
    "attacker": {"username": "Attacker", "bio": "Harmless bio...", "password": "EvilPassword"}
}

csrf = CSRFProtect()

# -------------------------------------------------------------------------
# LOGIN ROUTE (Simulates issuing session credentials)
# -------------------------------------------------------------------------

LOGIN_TEMPLATE = """
<!DOCTYPE html>
<html>
<head><title>SecureBank Login</title></head>
<body>
    <h2>Lab Login Page</h2>
    <form method="POST" action="/login">
        <label>Username:</label><br>
        <input type="text" name="username" value="alice"><br><br>
        <label>Password:</label><br>
        <input type="password" name="password" value="Password123"><br><br>
        <button type="submit">Log In</button>
    </form>
</body>
</html>
"""

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = users_db.get(username)
        if user and user['password'] == password:
            resp = make_response(redirect(url_for('view_profile', username=username)))
            
            if not SECURITY_ENABLED:
                # VULNERABLE MODE: Cookie is accessible to JavaScript (httponly=False)
                resp.set_cookie('session_id', 'SESS_TOKEN_987654321_ALICE', httponly=False)
            else:
                # SECURE MODE: Cookie is protected from JavaScript execution (httponly=True)
                resp.set_cookie('session_id', 'SESS_TOKEN_987654321_ALICE', httponly=True)
                
            return resp
        return "Invalid credentials", 401

    return render_template_string(LOGIN_TEMPLATE)


# -------------------------------------------------------------------------
# 1 & 2. VULNERABLE SCENARIO (XSS & CSRF Enabled)
# -------------------------------------------------------------------------

VULNERABLE_TEMPLATE = """
<!DOCTYPE html>
<html>
<head><title>SecureBank Profile (Vulnerable)</title></head>
<body>
    <h1>Welcome, {{ profile.username }}</h1>
    
    <div>
        <h3>User Bio:</h3>
        <p>{{ profile.bio | safe }}</p> 
    </div>

    <hr>
    <h3>Update Bio</h3>
    <form method="POST" action="/update-bio">
        <input type="text" name="bio" value="{{ profile.bio }}">
        <button type="submit">Update Bio</button>
    </form>
    <hr>
    <p>
        <a href="{{ url_for('view_profile', username='attacker') }}">Nice Profile - Just click!</a>
    </p>
</body>
</html>
"""

@app.route('/profile/<username>', methods=['GET'])
def view_profile(username):
    user = users_db.get(username)
    if not user:
        return "User not found", 404
    return render_template_string(VULNERABLE_TEMPLATE, profile=user)

@app.route('/update-form', methods=['GET'])
def serve_update_form():
    return render_template('xss_attacker_form.html', profile=users_db['attacker'])

@app.route('/profile/<username>/update-bio', methods=['POST'])
def update_profile_bio(username):
    if username in users_db:
        users_db[username]['bio'] = request.form.get('bio', '')
        return f"Bio updated for dynamic user '{username}'!"
    return "User not found", 404

@app.route('/update-bio', methods=['POST'])
def update_bio():
    users_db['attacker']['bio'] = request.form.get('bio', '')
    return "Attacker bio updated successfully! Navigate to /profile/attacker to trigger."

@app.route('/')
def index():
    return redirect(url_for('login'))

# @app.route('/change-password', methods=['POST'])
# def change_password():
#     # State-changing request without any CSRF validation
#     user_profile['new_password'] = request.form.get('new_password', '')
#     print(f"[!] Password successfully changed to: {user_profile['new_password']}")
#     return "Password changed successfully! (Vulnerable Route)"

@app.route('/change-password', methods=['POST'])
def change_password():
    # State-changing request without any CSRF validation
    users_db['alice']['password'] = request.form.get('new_password', '')
    print(f"[!] Password successfully changed to: {users_db['alice']['password']}")
    return "Password changed successfully! (Vulnerable Route)"
# -------------------------------------------------------------------------
# SECURE SCENARIO & CONFIGURATION
# -------------------------------------------------------------------------

# SECURE_TEMPLATE = """
# <!DOCTYPE html>
# <html>
# <head><title>SecureBank Profile (Protected)</title></head>
# <body>
#     <h1>Welcome, {{ profile.username }}</h1>
#     <div>
#         <h3>User Bio:</h3>
#         <p>{{ profile.bio }}</p> 
#     </div>
# </body>
# </html>
# """

SECURE_TEMPLATE = """
<!DOCTYPE html>
<html>
<head><title>SecureBank Profile (Protected)</title></head>
<body>
    <h1>Welcome, {{ profile.username }}</h1>
    
    <div>
        <h3>User Bio:</h3>
        <p>{{ profile.bio }}</p> 
    </div>

    <hr>
    <h3>Update Bio</h3>
    <form method="POST" action="/secure/update-bio">
        <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
        <input type="text" name="bio" value="{{ profile.bio }}">
        <button type="submit">Update Bio</button>
    </form>

    <hr>
    <h3>Change Password</h3>
    <form method="POST" action="/secure/change-password">
        <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
        <input type="password" name="new_password" placeholder="New Password">
        <button type="submit">Change Password</button>
    </form>
</body>
</html>
"""

@app.route('/secure')
def secure_index():
    return render_template_string(SECURE_TEMPLATE, profile=users_db['alice'])

@app.route('/secure/update-bio', methods=['POST'])
def secure_update_bio():
    users_db['alice']['bio'] = request.form.get('bio', '')
    return redirect(url_for('secure_index'))

@app.route('/secure/change-password', methods=['POST'])
def secure_change_password():
    users_db['alice']['password'] = request.form.get('new_password', '')
    return "Password changed successfully! (Secure Route)"

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == '--secure':
        SECURITY_ENABLED = True
        print("[+] Starting server in SECURE mode...")
        csrf.init_app(app)
        app.config['WTF_CSRF_ENABLED'] = True
        csp = {'default-src': '\'self\'', 'script-src': '\'self\''}
        Talisman(app, content_security_policy=csp, force_https=False)
    else:
        print("[!] Starting server in VULNERABLE mode...")
        
    app.run(debug=True, port=5000)
