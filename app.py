from flask import Flask, request, jsonify, send_from_directory, session
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import time
import re
import hmac
import secrets
from datetime import timedelta

load_dotenv()
app = Flask(__name__, static_folder="client/build", static_url_path="/")

def env_bool(name, default=False):
    value = os.environ.get(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}

app.config["SECRET_KEY"] = os.environ.get("FLASK_SECRET_KEY", "dev-insecure-secret-change-me")
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = os.environ.get("SESSION_COOKIE_SAMESITE", "Lax")
app.config["SESSION_COOKIE_SECURE"] = env_bool("SESSION_COOKIE_SECURE", os.environ.get("RENDER") == "true")
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(hours=8)

DEFAULT_CORS_ORIGINS = [
    "http://localhost:3000",
    "https://waf-project.onrender.com",
    "https://waf-project-1.onrender.com",
]
cors_origins = os.environ.get("CORS_ORIGINS")
allowed_origins = [o.strip() for o in cors_origins.split(",") if o.strip()] if cors_origins else DEFAULT_CORS_ORIGINS
CORS(app, resources={r"/api/*": {"origins": allowed_origins}}, supports_credentials=True)

MONGO_URI = os.environ.get("MONGO_URI")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD")

if not MONGO_URI:
    raise ValueError("MongoDB URI is not set")

client = MongoClient(MONGO_URI)
db = client.waf_db
logs_collection = db.logs
rules_collection = db.protection_rules

limiter = Limiter(get_remote_address, app=app, default_limits=["5 per minute"])

SECURITY_RULES = {
    "SQLi": [r"(\%27)|(\')|(\-\-)|(%23)|(#)", r"(?i)\b(SELECT|INSERT|DELETE|UPDATE|DROP|UNION|TRUNCATE|ALTER|EXEC|REPLACE|MERGE)\s"],
    "XSS": [r"(?i)<script.*?>.*?</script.*?>", r"(?i)javascript:.*"],
    "Command Injection": [r"(\||;|&&|\$|\`)", r"\b(rm|wget|curl|nc|netcat|bash|sh|python|perl|php|awk)\b"],
    "Path Traversal": [r"(\.\./|\.\.\\)", r"(/etc/passwd|/proc/self/cmdline)", r"https?:\/\/.*?\.[a-z]{2,6}\/.*"]
}

def load_protection_rules():
    rules = list(rules_collection.find({}, {"_id": 0}))
    if not rules:
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
 
def get_protection_rules_from_db():
    return load_protection_rules()

def get_or_create_csrf_token():
    token = session.get("csrf_token")
    if not token:
        token = secrets.token_urlsafe(32)
        session["csrf_token"] = token
    return token

def validate_csrf_token():
    session_token = session.get("csrf_token")
    request_token = request.headers.get("X-CSRF-Token", "")
    return bool(session_token) and hmac.compare_digest(session_token, request_token)
@app.route("/api/home", methods=["GET"])
@limiter.limit("5 per minute")
def home():
    return jsonify({"message": "Welcome to the Web Application Firewall!"})

@app.route("/api/protection-rules", methods=["GET"])
def get_protection_rules():
    return jsonify({"rules": get_protection_rules_from_db()})

@app.route("/api/admin/status", methods=["GET"])
def admin_status():
    return jsonify({"isAdmin": bool(session.get("is_admin"))})

@app.route("/api/admin/csrf-token", methods=["GET"])
def admin_csrf_token():
    token = get_or_create_csrf_token()
    return jsonify({"csrfToken": token})

@app.route("/api/admin/login", methods=["POST"])
@limiter.limit("10 per minute")
def admin_login():
    if not ADMIN_PASSWORD:
        return jsonify({"error": "Admin login is disabled: ADMIN_PASSWORD is not configured."}), 503

    if not validate_csrf_token():
        return jsonify({"error": "Invalid CSRF token."}), 403

    data = request.get_json(silent=True) or {}
    password = data.get("password", "")
    if not isinstance(password, str) or not password.strip():
        return jsonify({"error": "Password is required."}), 400

    if not hmac.compare_digest(password, ADMIN_PASSWORD):
        return jsonify({"error": "Invalid credentials."}), 403

    session.permanent = True
    session["is_admin"] = True
    return jsonify({"message": "Admin login successful."}), 200

@app.route("/api/admin/logout", methods=["POST"])
def admin_logout():
    if not validate_csrf_token():
        return jsonify({"error": "Invalid CSRF token."}), 403

    session.pop("is_admin", None)
    return jsonify({"message": "Logged out."}), 200

@app.route("/api/protection-rules/<int:rule_id>", methods=["PATCH"])
def update_protection_rule(rule_id):
    if not session.get("is_admin"):
        return jsonify({"error": "Unauthorized"}), 403

    if not validate_csrf_token():
        return jsonify({"error": "Invalid CSRF token."}), 403

    data = request.get_json(silent=True) or {}
    for rule in get_protection_rules_from_db():
        if rule["id"] == rule_id:
            rule["enabled"] = data.get("enabled", rule["enabled"])
            rules_collection.update_one({"id": rule_id}, {"$set": {"enabled": rule["enabled"]}})
            return jsonify({"message": "Rule updated successfully.", "rule": rule}), 200
    return jsonify({"error": "Rule not found"}), 404

@app.route("/api/user-input", methods=["POST"])
@limiter.limit("5 per minute")
def user_input():
    data = request.get_json(silent=True) or {}
    user_input = data.get("input", "")

    if not user_input.strip():
        return jsonify({"error": "Empty input received"}), 400

    threat_type = detect_attack(user_input)
    if threat_type:
        log_attack(request.remote_addr, user_input, threat_type)
        return jsonify({"error": f"Blocked by WAF: {threat_type}"}), 403

    return jsonify({"message": "Safe Request"}), 200

def detect_attack(input_data):
    for rule in get_protection_rules_from_db():
        if rule["enabled"]:
            for pattern in SECURITY_RULES.get(rule["name"], []):
                try:
                    if re.search(pattern, input_data, re.IGNORECASE):
                        return rule["name"]
                except re.error as e:
                    print(f"Invalid regex pattern: {pattern} -> {e}")
                    continue
    return None

def log_attack(ip, input_data, threat_detected):
    log_entry = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "ip": ip,
        "input": input_data,
        "threat": threat_detected
    }
    logs_collection.insert_one(log_entry)

@app.route("/")
@app.route("/<path:path>")
def serve_frontend(path="index.html"):
    try:
        return send_from_directory(app.static_folder, path)
    except Exception:
        return send_from_directory(app.static_folder, "index.html")

if __name__ == "__main__":
    app.run(debug=False)