# Web Application Firewall (WAF) Project

A Flask + React web application firewall demo that detects and blocks common web attacks before they reach backend business logic.

## Features

- SQL injection detection
- XSS detection
- Command injection detection
- Path traversal detection
- Request rate limiting on sensitive endpoints
- Attack logging to MongoDB
- Admin-gated protection rule toggling (server-side session auth)

## Tech Stack

- Backend: Flask, Flask-Limiter, PyMongo
- Frontend: React, React Router, SCSS
- Database: MongoDB Atlas
- Production server: Gunicorn
- Deployment: Render (Python Web Service)

## Current Security Model

- Pattern-based inspection for incoming user input against enabled rules
- Per-IP rate limiting for key API routes
- Protected rule updates via admin login session
- CSRF token validation on admin and rule-update state-changing endpoints
- Secure cookie defaults:
  - HttpOnly session cookie
  - Configurable SameSite and Secure flags
- Configurable CORS allowlist

## Environment Variables

Required for backend:

- MONGO_URI: MongoDB connection string
- ADMIN_PASSWORD: Password used by admin login endpoint
- FLASK_SECRET_KEY: Secret used to sign session cookies

Optional for backend:

- CORS_ORIGINS: Comma-separated list of allowed origins
- SESSION_COOKIE_SECURE: true or false
- SESSION_COOKIE_SAMESITE: Lax, Strict, or None

Optional for frontend:

- REACT_APP_API_BASE_URL: Backend base URL

## Local Development

1. Clone repository

```sh
git clone https://github.com/yourusername/WAF_Project.git
cd WAF_Project
```

1. Install backend dependencies

```sh
pip install -r requirements.txt
```

1. Create .env file in project root

```env
MONGO_URI=your_mongodb_connection_string
ADMIN_PASSWORD=your_admin_password
FLASK_SECRET_KEY=replace_with_long_random_secret
SESSION_COOKIE_SECURE=false
SESSION_COOKIE_SAMESITE=Lax
```

1. Run backend

```sh
python app.py
```

1. Install and run frontend

```sh
cd client
npm install
npm start
```

Frontend runs at <http://localhost:3000> and backend at <http://127.0.0.1:5000>.

## Deploy on Render

This repository includes [deployment/render.yaml](deployment/render.yaml) for backend deployment.

Set these environment variables in Render:

- MONGO_URI
- ADMIN_PASSWORD
- FLASK_SECRET_KEY
- CORS_ORIGINS (recommended)

## API Overview

- GET /api/home
- POST /api/user-input
- GET /api/protection-rules
- PATCH /api/protection-rules/:id (admin session required)
- GET /api/admin/status
- GET /api/admin/csrf-token
- POST /api/admin/login
- POST /api/admin/logout

For POST and PATCH admin-protected actions, send X-CSRF-Token with the value from GET /api/admin/csrf-token.

## Notes

This project provides practical baseline protection for common attack patterns. For stricter production security, add stronger account controls, endpoint audit trails, and centralized security monitoring.

## License

MIT
