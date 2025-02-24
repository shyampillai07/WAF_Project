from flask import Flask, request, render_template, jsonify
import re
import sqlite3
import time

app = Flask(__name__,static_folder="static")

# Security Rules for SQL Injection & XSS
BLOCKED_PATTERNS = [
    r"(\%27)|(\')|(\-\-)|(%23)|(#)",  # SQL Injection
    r"(<script>)|(<script>)"  # XSS
]

BLOCKED_IPS = []
REQUEST_LOGS = {}

# Database setup (SQLite)
def init_db():
    conn = sqlite3.connect("waf_logs.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip TEXT,
            input TEXT,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

@app.route("/")
def home():
    return render_template("index.html")  # ✅ Only one home() function

@app.route("/check", methods=["GET"])
def waf():
    user_ip = request.remote_addr
    user_input = request.args.get("input", "")

    # Rate Limiting - Prevent Too Many Requests
    current_time = time.time()
    if user_ip in REQUEST_LOGS:
        if len(REQUEST_LOGS[user_ip]) >= 5:  # More than 5 requests in 10 sec?
            if current_time - REQUEST_LOGS[user_ip][0] < 10:
                BLOCKED_IPS.append(user_ip)
                return jsonify({"error": "Too many requests. IP temporarily blocked."}), 403
        REQUEST_LOGS[user_ip].append(current_time)
    else:
        REQUEST_LOGS[user_ip] = [current_time]

    # Check if IP is Blocked
    if user_ip in BLOCKED_IPS:
        return jsonify({"error": "Access Denied - IP Blocked"}), 403

    # Check for SQLi/XSS Attacks
    if is_malicious(user_input):
        log_attack(user_ip, user_input)
        return jsonify({"error": "Blocked by WAF"}), 403

    return jsonify({"message": "Safe Request"}), 200

def is_malicious(input_data):
    return any(re.search(pattern, input_data, re.IGNORECASE) for pattern in BLOCKED_PATTERNS)

def log_attack(ip, input_data):
    conn = sqlite3.connect("waf_logs.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO logs (ip, input, timestamp) VALUES (?, ?, ?)",
                   (ip, input_data, time.strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    app.run(debug=True)