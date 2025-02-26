from flask import Flask, request, render_template, jsonify
import re
import sqlite3
import time
import logging
import os

app = Flask(__name__, static_folder="static")

# Ensure logs directory exists
os.makedirs("logs", exist_ok=True)

# Setup Access Logging
access_logger = logging.getLogger("access")
access_handler = logging.FileHandler("logs/access.log")
access_formatter = logging.Formatter("%(asctime)s - INPUT: %(message)s - IP: %(ip)s - THREAT: %(threat)s")
access_handler.setFormatter(access_formatter)
access_logger.addHandler(access_handler)
access_logger.setLevel(logging.INFO)

# Setup Error Logging
error_logger = logging.getLogger("error")
error_handler = logging.FileHandler("logs/error.log")
error_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
error_logger.addHandler(error_handler)
error_logger.setLevel(logging.ERROR)

# 🚨 SECURITY PATTERNS 🚨
SQLI_PATTERNS = [
    r"(\%27)|(\')|(\-\-)|(%23)|(#)",  # Basic SQL Injection
    r"\b(SELECT|INSERT|DELETE|UPDATE|DROP|UNION|TRUNCATE|ALTER|EXEC|REPLACE|MERGE)\b",  # SQL Keywords
    r"(\bOR\b|\bAND\b).*(=|LIKE|IN).*(['\"0-9])",  # OR/AND-based SQLi
    r"(\/\*.*?\*\/)"  # SQL Comment Injection
]

XSS_PATTERNS = [
    r"(?i)<script.*?>.*?</script.*?>",  # Basic XSS
    r"(?i)javascript:.*",  # Inline JavaScript
    r"(?i)on\w+=.*",  # Event Handlers (onerror, onclick, etc.)
    r"(?i)(alert|confirm|prompt|eval).*?"  # JavaScript Functions
]

CMD_INJECTION_PATTERNS = [
    r"(\||;|&&|\$|\`)",  # Command Separators
    r"\b(rm|wget|curl|nc|netcat|bash|sh|python|perl|php|awk)\b"  # Dangerous Commands
]

LFI_RFI_PATTERNS = [
    r"(\.\./|\.\.\\)",  # Directory Traversal
    r"(\/etc\/passwd|\/proc\/self\/cmdline)",  # Accessing System Files
    r"https?:\/\/.*?\.[a-z]{2,6}\/.*"  # Remote File Inclusion (RFI)
]

BLOCKED_IPS = []
REQUEST_LOGS = {}

# 📌 Initialize Database
def init_db():
    conn = sqlite3.connect("database/waf_logs.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip TEXT,
            input TEXT,
            threat TEXT,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

# 🏠 Home Route
@app.route("/")
def home():
    return render_template("index.html") 

#log Html Route
@app.route("/logs")
def logs():
    conn = sqlite3.connect("database/waf_logs.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM logs ORDER BY id DESC")
    logs = cursor.fetchall()
    conn.close()
    return render_template("logs.html", logs=logs)

#Error Html Route
@app.route("/error")
def error():
    with open("logs/error.log", "r") as f:
        error_logs = f.read()
    return render_template("error.html", error_logs=error_logs)

# 🔍 WAF Security Check
@app.route("/check", methods=["GET"])
def waf():
    user_ip = request.remote_addr
    user_input = request.args.get("input", "")

    app.logger.info(f"Received Input: {user_input}")

    # 🚦 Rate Limiting - Prevent Too Many Requests
    if is_rate_limited(user_ip):
        return jsonify({"error": "Too many requests. IP temporarily blocked."}), 403

    # 🚫 Blocked IP Check
    if user_ip in BLOCKED_IPS:
        return jsonify({"error": "Access Denied - IP Blocked"}), 403

    # 🔍 Check for security threats
    threat_type = detect_attack(user_input)
    if threat_type:
        log_attack(user_ip, user_input, threat_type)
        return jsonify({"error": f"Blocked by WAF: {threat_type}"}), 403

    return jsonify({"message": "Safe Request"}), 200

# 🚦 Rate Limiting Check
def is_rate_limited(user_ip):
    current_time = time.time()
    if user_ip in REQUEST_LOGS:
        if len(REQUEST_LOGS[user_ip]) >= 5:  # More than 5 requests in 10 sec?
            if current_time - REQUEST_LOGS[user_ip][0] < 10:
                BLOCKED_IPS.append(user_ip)
                return True
        REQUEST_LOGS[user_ip].append(current_time)
    else:
        REQUEST_LOGS[user_ip] = [current_time]
    return False

# 🔎 Detect Attack Type (SQLi / XSS / RCE / LFI-RFI)
def detect_attack(input_data):
    for pattern in SQLI_PATTERNS:
        if re.search(pattern, input_data, re.IGNORECASE):
            return "SQL Injection"

    for pattern in XSS_PATTERNS:
        if re.search(pattern, input_data, re.IGNORECASE):
            return "XSS Attack"

    for pattern in CMD_INJECTION_PATTERNS:
        if re.search(pattern, input_data, re.IGNORECASE):
            return "Command Injection"

    for pattern in LFI_RFI_PATTERNS:
        if re.search(pattern, input_data, re.IGNORECASE):
            return "Path Traversal / LFI-RFI Attack"

    return None  # No threat detected

# 📌 Log Attacks in Database & Access Log
def log_attack(ip, input_data, threat_detected):
    conn = sqlite3.connect("database/waf_logs.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO logs (ip, input, threat, timestamp) VALUES (?, ?, ?, ?)",
                   (ip, input_data, threat_detected, time.strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

    log_message = f"INPUT: {input_data}"
    access_logger.info(log_message, extra={"ip": ip, "threat": threat_detected})

# 📌 Log Errors
def log_error(error_message):
    error_logger.error(error_message)

# 🚀 Run the Application
if __name__ == "__main__":
    init_db()
    app.run(debug=True)