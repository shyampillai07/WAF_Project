Web Application Firewall (WAF) Project 🛡️

A Web Application Firewall (WAF) built using Flask and SQLite, designed to detect and block common web threats like SQL Injection, XSS, Command Injection, and LFI/RFI Attacks.

🚀 Features

✅ SQL Injection Protection – Detects and blocks malicious SQL queries.
✅ Cross-Site Scripting (XSS) Protection – Identifies and prevents script injections.
✅ Command Injection Prevention – Blocks dangerous system commands.
✅ Local/Remote File Inclusion (LFI/RFI) Defense – Restricts unauthorized file access.
✅ IP Rate Limiting – Limits repeated requests to prevent DoS attacks.
✅ Logging & Monitoring – Logs all suspicious activity and user inputs.
✅ Docker & Render Deployment – Easily deployable with Docker and Render.

🛠️ Tech Stack

Backend: Python (Flask)

Database: SQLite

Web Server: Gunicorn

Containerization: Docker

Deployment: Render


📂 Project Structure

WAF_Project/
│── database/             # SQLite database for logging attacks
│── logs/                 # Stores application and access logs
│── static/               # Static assets (CSS, JS, images)
│── templates/            # HTML templates
│── app.py                # Main Flask application
│── gunicorn_config.py    # Gunicorn server configuration
│── Dockerfile            # Docker setup for containerization
│── render.yaml           # Render deployment configuration
│── requirements.txt      # Python dependencies
│── README.md             # Project documentation

🖥️ Setup & Installation

1️⃣ Clone the Repository

git clone https://github.com/yourusername/WAF_Project.git
cd WAF_Project

2️⃣ Install Dependencies

pip install -r requirements.txt

3️⃣ Run the Application

python app.py

The app will run at http://127.0.0.1:5000.

🐳 Deploy with Docker

1️⃣ Build the Docker Image

docker build -t waf_project .

2️⃣ Run the Container

docker run -p 5000:5000 waf_project

🌍 Deploy on Render

1. Push your changes to GitHub


2. Connect the repository to Render


3. Use render.yaml for automatic deployment



📜 License

This project is open-source under the MIT License.

