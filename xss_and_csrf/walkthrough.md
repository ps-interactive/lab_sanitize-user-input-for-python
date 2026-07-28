## Lab Walkthrough & Explanations

### Part 1: Exploiting XSS (Cross-Site Scripting)
**The Vulnerability:** In the `VULNERABLE_TEMPLATE`, we used `{{ profile.bio | safe }}`. The `|safe` filter explicitly tells Jinja2 *not* to encode HTML entities. If an attacker inputs JavaScript into their bio, the browser will execute it natively.

**Why it matters:** If an attacker can execute arbitrary JavaScript in a victim's browser session, they can steal session cookies, capture keystrokes, or perform actions on behalf of the user.

**How to exploit:**
1. Run the app in vulnerable mode: `python app.py`
2. Open `http://127.0.0.1:5000/`
3. In the "Update Bio" input field, paste the following payload and click submit:
   ```html
   <script>alert('XSS Vulnerability Executed! Cookie: ' + document.cookie);</script>
   ```
