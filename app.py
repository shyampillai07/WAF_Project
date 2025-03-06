from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_sqlalchemy import SQLAlchemy
import re
import os
import time
import logging

# Flask App Initialization
app = Flask(__name__, static_folder="client/build", static_url_path="/")
CORS(app, resources={r"/api/*": {"origins": "https://waf-project-1.onrender.com"}})

# Initialize Rate Limiter
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["5 per minute"]
)

# Create Directories
os.makedirs("logs", exist_ok=True)

# PostgreSQL Database Connection
DATABASE_URL = os.getenv("DATABASE_URL")  

if DATABASE_URL:
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db = SQLAlchemy(app)
else:
    db = None

# Database Model
class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(50), nullable=False)
    input = db.Column(db.Text, nullable=False)
    threat = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.String(50), nullable=False)

# Initialize Database
def init_db():
    if db is None:
        print("No database URL found. Skipping DB initialization.")
        return

    with app.app_context():
        db.create_all()
        print("Database initialized successfully.")

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
@limiter.limit("5 per minute")
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
@limiter.limit("5 per minute")
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
    try:
        return send_from_directory(app.static_folder, path)
    except Exception:
        return send_from_directory(app.static_folder, "index.html")

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

# Logging Function (Updated for SQLAlchemy)
def log_attack(ip, input_data, threat_detected):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

    if db is None:
        return

    try:
        new_log = Log(ip=ip, input=input_data, threat=threat_detected, timestamp=timestamp)
        db.session.add(new_log)
        db.session.commit()
    except Exception as e:
        error_logger.error(f"Database Logging Error: {e}")
        db.session.rollback()

    access_logger.info(f"INPUT: {input_data} - IP: {ip} - THREAT: {threat_detected}")

# Ensure DB is initialized when the app starts
if __name__ != "__main__":
    init_db()
    gunicorn_app = app