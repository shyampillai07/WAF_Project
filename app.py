import re
import json
import time
from flask import Flask, request, jsonify

app = Flask(__name__)

# Security Rules for SQL Injection & XSS
BLOCKED_PATTERNS = [
    r"(\%27)|(\')|(\-\-)|(%23)|(#)",  # SQL Injection
    r"(<script>)|(<script>)"  # XSS
]

# IP Tracking for Blocking
BLOCKED_IPS = []
REQUEST_LOGS = {}

# Function to Check for Attacks
def is_malicious(input_data):
    for pattern in BLOCKED_PATTERNS:
        if re.search(pattern, input_data, re.IGNORECASE):
            return True
    return False

@app.route("/", methods=["GET", "POST"])
def waf():
    user_ip = request.remote_addr
    user_input = request.args.get("input", "")

    # Rate Limiting - Prevent Too Many Requests
    current_time = time.time()
    if user_ip in REQUEST_LOGS:
        if len(REQUEST_LOGS[user_ip]) >= 5:  # More than 5 requests in 10 seconds?
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

# Logging Function
def log_attack(ip, input_data):
    attack_data = {
        "ip": ip,
        "input": input_data,
        "time": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    with open("logs.json", "a") as log_file:
        json.dump(attack_data, log_file)
        log_file.write("\n")

if __name__ == "__main__":
    app.run(debug=True)
