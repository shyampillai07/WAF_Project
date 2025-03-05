from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import re
import sqlite3
import time
import logging
import os

# Flask App Initialization
app = Flask(__name__, static_folder="client/build", static_url_path="/")
CORS(app, resources={r"/api/*": {"origins": "https://waf-project-1.onrender.com"}})  # CORS for local & deployed frontend

# Create Directories
os.makedirs("logs", exist_ok=True)
os.makedirs("/opt/render/database", exist_ok=True)

# Database Path (Ensure persistence in Render)
DB_PATH = os.environ.get("DATABASE_URL", "sqlite:////opt/render/database/waf_logs.db")

# Initialize Database
def init_db():
    conn = sqlite3.connect(DB_PATH.replace("sqlite:///", ""))
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

# Logging Configuration
log_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

def setup_logger(name, log_file):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        handler = logging.FileHandler(log_file)
        handler.setFormatter(log_formatter)
        logger.addHandler(handler)

    return logger

access_logger = setup_logger("access", "logs/access.log")
error_logger = setup_logger("error", "logs/error.log")

# Security Rules
SECURITY_RULES = {
    "SQLi": [r"(\%27)|(\')|(\-\-)|(%23)|(#)", r"(?i)\b(SELECT|INSERT|DELETE|UPDATE|DROP|UNION|TRUNCATE|ALTER|EXEC|REPLACE|MERGE)\s"],
    "XSS": [r"(?i)<script.*?>.*?</script.*?>", r"(?i)javascript:.*"],
    "Command Injection": [r"(\||;|&&|\$|\`)", r"\b(rm|wget|curl|nc|netcat|bash|sh|python|perl|php|awk)\b"],
    "Path Traversal": [r"(\.\./|\.\.\\)", r"(/etc/passwd|/proc/self/cmdline)", r"https?:\/\/.*?\.[a-z]{2,6}\/.*"]
}

protection_rules = [
    {"id": 1, "name": "SQLi", "description": "Detects SQL injection", "enabled": True},
    {"id": 2, "name": "XSS", "description": "Detects cross-site scripting", "enabled": True},
    {"id": 3, "name": "Command Injection", "description": "Prevents OS command execution", "enabled": True},
    {"id": 4, "name": "Path Traversal", "description": "Blocks unauthorized file access", "enabled": True},
    {"id": 5, "name": "Rate Limiting", "description": "Limits excessive requests", "enabled": True}
]

# API Endpoints
@app.route('/api/home', methods=['GET'])
def home():
    return jsonify({"message": "Welcome to the Web Application Firewall!"})

@app.route("/api/protection-rules", methods=["GET"])
def get_protection_rules():
    return jsonify({"rules": protection_rules})

@app.route("/api/protection-rules/<int:rule_id>", methods=["PATCH"])
def update_protection_rule(rule_id):
    data = request.get_json()
    for rule in protection_rules:
        if rule["id"] == rule_id:
            rule["enabled"] = data.get("enabled", rule["enabled"])
            return jsonify({"message": "Rule updated successfully.", "rule": rule}), 200
    return jsonify({"error": "Rule not found"}), 404

@app.route("/api/user-input", methods=["POST"])
def user_input():
    data = request.json
    user_input = data.get("input", "")

    if not user_input.strip():
        return jsonify({"error": "Empty input received"}), 400

    threat_type = detect_attack(user_input)
    if threat_type:
        log_attack(request.remote_addr, user_input, threat_type)
        return jsonify({"error": f"Blocked by WAF: {threat_type}"}), 403

    return jsonify({"message": "Safe Request"}), 200

# Serve Frontend (React App)
@app.route("/")
@app.route("/<path:path>")
def serve_frontend(path="index.html"):
    return send_from_directory(app.static_folder, path)

# WAF Functions
def detect_attack(input_data):
    for rule in protection_rules:
        if rule["enabled"]:
            for pattern in SECURITY_RULES.get(rule["name"], []):
                try:
                    if re.search(pattern, input_data, re.IGNORECASE):
                        return rule["name"]
                except re.error as e:
                    error_logger.error(f"Invalid regex pattern: {pattern} -> {e}")
                    continue
    return None

def log_attack(ip, input_data, threat_detected):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    conn = sqlite3.connect(DB_PATH.replace("sqlite:///", ""))
    cursor = conn.cursor()
    cursor.execute("INSERT INTO logs (ip, input, threat, timestamp) VALUES (?, ?, ?, ?)",
                   (ip, input_data, threat_detected, timestamp))
    conn.commit()
    conn.close()
    access_logger.info(f"INPUT: {input_data} - IP: {ip} - THREAT: {threat_detected}")

if __name__ != "__main__":
    init_db()
    gunicorn_app = app