<div align="center">

# Web Application Firewall (WAF)

Enterprise-grade Web Application Firewall built with Flask, React, and MongoDB.

<p align="center">

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)
![MongoDB](https://img.shields.io/badge/MongoDB-47A248?style=for-the-badge&logo=mongodb&logoColor=white)
![SCSS](https://img.shields.io/badge/SCSS-CC6699?style=for-the-badge&logo=sass&logoColor=white)
![Render](https://img.shields.io/badge/Render-430098?style=for-the-badge&logo=render&logoColor=white)

</p>

</div>



## Overview

This project demonstrates a Web Application Firewall (WAF) that inspects incoming HTTP requests, detects common web attacks, blocks malicious payloads, and logs security events before requests reach backend application logic.



## Features

- SQL Injection Detection
- Cross-Site Scripting (XSS) Detection
- Command Injection Detection
- Path Traversal Detection
- Request Rate Limiting
- MongoDB Attack Logging
- CSRF Protection
- Secure Session Authentication
- Configurable CORS Allowlist
- Runtime Protection Rule Management



## Technology Stack

<table>
<tr>

<td align="center" width="170">
<img src="https://skillicons.dev/icons?i=python" width="60"><br>
<b>Python</b>
</td>

<td align="center" width="170">
<img src="https://skillicons.dev/icons?i=flask" width="60"><br>
<b>Flask</b>
</td>

<td align="center" width="170">
<img src="https://skillicons.dev/icons?i=react" width="60"><br>
<b>React</b>
</td>

<td align="center" width="170">
<img src="https://skillicons.dev/icons?i=mongodb" width="60"><br>
<b>MongoDB Atlas</b>
</td>

</tr>

<tr>

<td align="center">
<img src="https://skillicons.dev/icons?i=sass" width="60"><br>
<b>SCSS</b>
</td>

<td align="center">
<img src="https://skillicons.dev/icons?i=git" width="60"><br>
<b>Git</b>
</td>

<td align="center">
<img src="https://skillicons.dev/icons?i=github" width="60"><br>
<b>GitHub</b>
</td>

<td align="center">
<img src="https://skillicons.dev/icons?i=postman" width="60"><br>
<b>Postman</b>
</td>

</tr>
</table>



## Architecture

```text
Client
   │
   ▼
React Frontend
   │
   ▼
Flask WAF Engine
   │
   ├── SQL Injection Detection
   ├── XSS Detection
   ├── Command Injection Detection
   ├── Path Traversal Detection
   ├── Rate Limiting
   ▼
Backend APIs
   │
   ▼
MongoDB
```



## Security Features

| Feature | Description |
|----------|-------------|
| SQL Injection Protection | Detects SQL injection payloads |
| XSS Protection | Blocks cross-site scripting attacks |
| Command Injection Protection | Prevents command execution attempts |
| Path Traversal Protection | Detects directory traversal payloads |
| Rate Limiting | Limits repeated requests from the same IP |
| CSRF Protection | Secures state-changing admin operations |
| Secure Sessions | Uses HttpOnly cookies with configurable SameSite and Secure flags |
| Attack Logging | Stores blocked requests in MongoDB |



## Project Structure

```text
WAF_Project/
│
├── client/
├── deployment/
├── app.py
├── requirements.txt
├── .env
└── README.md
```



## Installation

### Clone Repository

```bash
git clone https://github.com/yourusername/WAF_Project.git
cd WAF_Project
```

### Backend

```bash
pip install -r requirements.txt
python app.py
```

### Frontend

```bash
cd client
npm install
npm start
```



## Environment Variables

```env
MONGO_URI=
ADMIN_PASSWORD=
FLASK_SECRET_KEY=
SESSION_COOKIE_SECURE=false
SESSION_COOKIE_SAMESITE=Lax
CORS_ORIGINS=
REACT_APP_API_BASE_URL=
```



## API Endpoints

| Method | Endpoint |
|---------|----------|
| GET | `/api/home` |
| POST | `/api/user-input` |
| GET | `/api/protection-rules` |
| PATCH | `/api/protection-rules/:id` |
| GET | `/api/admin/status` |
| GET | `/api/admin/csrf-token` |
| POST | `/api/admin/login` |
| POST | `/api/admin/logout` |



## Deployment

Backend deployment is configured using:

```
deployment/render.yaml
```



## Contributors

- Shyam Pillai
- Suchit Naik
- Aishwaraya Raikar



## License

This project is licensed under the MIT License.


## Contact

<p align="left">
  <a href="mailto:shyam.m.pillai71@gmail.com">
    <img src="https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white" alt="Email"/>
  </a>

  <a href="https://linkedin.com/in/shyampillai07">
    <img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn"/>
  </a>

  For questions, feedback, or collaboration opportunities, feel free to reach out.
