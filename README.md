# **Web Application Firewall (WAF) Project** 🛡️  

A **Web Application Firewall (WAF)** built using **Flask**, **SQLite**, and **React**, designed to detect and block common web threats like **SQL Injection, XSS, Command Injection, and LFI/RFI Attacks**.  

## **🚀 Features**  
👉 **SQL Injection Protection** – Detects and blocks malicious SQL queries.  
👉 **Cross-Site Scripting (XSS) Protection** – Identifies and prevents script injections.  
👉 **Command Injection Prevention** – Blocks dangerous system commands.  
👉 **Local/Remote File Inclusion (LFI/RFI) Defense** – Restricts unauthorized file access.  
👉 **IP Rate Limiting** – Limits repeated requests to prevent DoS attacks.  
👉 **Logging & Monitoring** – Logs all suspicious activity and user inputs.  
👉 **Interactive UI** – A modern **React frontend** with real-time logs and analytics.  
👉 **Docker & Render Deployment** – Easily deployable with Docker and Render.  

## **🛠️ Tech Stack**  
- **Frontend**: React, TailwindCSS, ShadCN  
- **Backend**: Python (Flask)  
- **Database**: SQLite  
- **Web Server**: Gunicorn  
- **Containerization**: Docker  
- **Deployment**: Render  

## **💂️ Security Checks Implemented**  
- **SQL Injection (SQLi)** detection and blocking.  
- **Cross-Site Scripting (XSS)** prevention.  
- **Command Injection** filtering.  
- **Path Traversal & Local File Inclusion (LFI/RFI)** blocking.  
- **Rate Limiting** to prevent abuse.  

## **🖥️ Setup & Installation**  
### **1️⃣ Clone the Repository**  
```sh
git clone https://github.com/yourusername/WAF_Project.git
cd WAF_Project
```

### **2️⃣ Install Backend Dependencies**  
```sh
pip install -r requirements.txt
```

### **3️⃣ Install Frontend Dependencies**  
```sh
cd client
npm install
```

### **4️⃣ Run the Backend**  
```sh
python app.py
```
The backend will run at **http://127.0.0.1:5000**.

### **5️⃣ Run the Frontend**  
```sh
cd client
npm start
```
The frontend will run at **http://localhost:3000**.

## **🐳 Deploy with Docker**  
### **1️⃣ Build the Docker Image**  
```sh
docker build -t waf_project .
```

### **2️⃣ Run the Container**  
```sh
docker run -p 5000:5000 waf_project
```

## **🌍 Deploy on Render**  
1. Push your changes to **GitHub**  
2. Connect the repository to **Render**  
3. Use `render.yaml` for automatic deployment  

## **🐝 Contributing**  
Feel free to fork this repository, create new features, and submit pull requests!  

## **📚 License**  
This project is **open-source** under the **MIT License**.  
