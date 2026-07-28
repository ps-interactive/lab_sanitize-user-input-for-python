
// Worng password
WrongPassword

// SQL injection snippets
"admin' --"
"anything' OR '1'='1"

// Malicious payload - XSS
<script>alert('XSS Vulnerability Executed! Cookie: ' + document.cookie);</script>

// Apply to: 
// 1. xss_attacker_form.html
// 2. LOGIN_TEMPLATE in app.py
<input type="hidden" name="csrf_token" value="{{ csrf_token() }}"></input>

// Add as the last element of this line (don't forget the leading comma), but only to allow inline styles:
// csp = {'default-src': '\'self\'', 'script-src': '\'self\''}
, 'style-src': '\'self\''


// URL for XSS testing
http://127.0.0.1:5000/update-form
