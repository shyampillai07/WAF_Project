from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import time
import logging
import re

# Flask App Initialization
app = Flask(__name__, static_folder="client/build", static_url_path="/")
CORS(app, resources={r"/api/*": {"origins": "https://waf-project-1.onrender.com"}})

# MongoDB Atlas Connection
load_dotenv()
MONGO_URI = os.environ.get("MONGO_URI")
print(f"MongoDB URI: {MONGO_URI}")

if not MONGO_URI:
    raise ValueError("MongoDB URI is not set")

client = MongoClient(MONGO_URI)
db = client.waf_db  # Database name
logs_collection = db.logs  # Collection for storing logs
rules_collection = db.protection_rules  # Collection for storing rules

# Initialize Rate Limiter
limiter = Limiter(get_remote_address, app=app, default_limits=["5 per minute"])

# Security Rules
SECURITY_RULES = {
    "SQLi": [r"(\%27)|(\')|(\-\-)|(%23)|(#)", r"(?i)\b(SELECT|INSERT|DELETE|UPDATE|DROP|UNION|TRUNCATE|ALTER|EXEC|REPLACE|MERGE)\s"],
    "XSS": [r"(?i)<script.*?>.*?</script.*?>", r"(?i)javascript:.*"],
    "Command Injection": [r"(\||;|&&|\$|\`)", r"\b(rm|wget|curl|nc|netcat|bash|sh|python|perl|php|awk)\b"],
    "Path Traversal": [r"(\.\./|\.\.\\)", r"(/etc/passwd|/proc/self/cmdline)", r"https?:\/\/.*?\.[a-z]{2,6}\/.*"]
}

# Load Protection Rules from Database
def load_protection_rules():
    rules = list(rules_collection.find({}, {"_id": 0}))  # Exclude MongoDB's default `_id` field
    if not rules:
        # Insert default rules if not present
        default_rules = [
            {"id": 1, "name": "SQLi", "description": "Detects SQL injection", "enabled": True},
            {"id": 2, "name": "XSS", "description": "Detects cross-site scripting", "enabled": True},
            {"id": 3, "name": "Command Injection", "description": "Prevents OS command execution", "enabled": True},
            {"id": 4, "name": "Path Traversal", "description": "Blocks unauthorized file access", "enabled": True},
            {"id": 5, "name": "Rate Limiting", "description": "Limits excessive requests", "enabled": True}
        ]
        rules_collection.insert_many(default_rules)
        return default_rules
    return rules

protection_rules = load_protection_rules()

# API Endpoints
@app.route("/api/home", methods=["GET"])
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
            rules_collection.update_one({"id": rule_id}, {"$set": {"enabled": rule["enabled"]}})
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

# WAF Functions
def detect_attack(input_data):
    for rule in protection_rules:
        if rule["enabled"]:
            for pattern in SECURITY_RULES.get(rule["name"], []):
                try:
                    if re.search(pattern, input_data, re.IGNORECASE):
                        return rule["name"]
                except re.error as e:
                    print(f"Invalid regex pattern: {pattern} -> {e}")
                    continue
    return None

# Logging Function (MongoDB)
def log_attack(ip, input_data, threat_detected):
    log_entry = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "ip": ip,
        "input": input_data,
        "threat": threat_detected
    }
    logs_collection.insert_one(log_entry)

# Serve Frontend (React App)
@app.route("/")
@app.route("/<path:path>")
def serve_frontend(path="index.html"):
    try:
        return send_from_directory(app.static_folder, path)
    except Exception:
        return send_from_directory(app.static_folder, "index.html")

if __name__ == "__main__":
    app.run(debug=True)
    
    gunicorn_app = app