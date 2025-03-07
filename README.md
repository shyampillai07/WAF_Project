# **Web Application Firewall (WAF) Project** 🛡️  

A **Web Application Firewall (WAF)** built using **Flask, MongoDB, and React**, designed to detect and block common web threats such as **SQL Injection, XSS, Command Injection, and LFI/RFI Attacks**.  

## **🚀 Features**  

✔ **SQL Injection Protection** – Detects and blocks malicious SQL queries.  
✔ **Cross-Site Scripting (XSS) Protection** – Prevents client-side script injections.  
✔ **Command Injection Prevention** – Blocks unauthorized system command execution.  
✔ **Local/Remote File Inclusion (LFI/RFI) Defense** – Restricts unauthorized file access.  
✔ **IP Rate Limiting** – Prevents abuse by limiting repeated requests.  
✔ **Logging & Monitoring** – Logs all suspicious activity in **MongoDB Atlas**.  
✔ **Interactive UI** – A **React-based frontend** with real-time logs & analytics.  
✔ **Docker & Render Deployment** – Easily deployable using **Docker & Render**.  

## **🛠️ Tech Stack**  

| **Category**    | **Technology**         |
|----------------|-----------------------|
| **Frontend**   | React, TailwindCSS, ShadCN |
| **Backend**    | Python (Flask)         |
| **Database**   | MongoDB (Atlas)        |
| **Web Server** | Gunicorn               |
| **Deployment** | Docker, Render         |

## **💂 Security Checks Implemented**  

✅ **SQL Injection (SQLi)** detection and blocking.  
✅ **Cross-Site Scripting (XSS)** prevention.  
✅ **Command Injection** filtering.  
✅ **Path Traversal & Local File Inclusion (LFI/RFI)** blocking.  
✅ **Rate Limiting** to prevent abuse and DoS attacks.  

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

### **3️⃣ Set Up MongoDB Atlas**  
1. **Create a MongoDB Atlas Account** at [MongoDB Atlas](https://www.mongodb.com/atlas).  
2. **Set up a cluster** and create a database.  
3. **Get your MongoDB URI** and update the `.env` file:  
   ```sh
   MONGO_URI="your_mongodb_connection_string"
   ```

### **4️⃣ Install Frontend Dependencies**  
```sh
cd client
npm install
```

### **5️⃣ Run the Backend**  
```sh
python app.py
```
The backend will run at **http://127.0.0.1:5000**.  

### **6️⃣ Run the Frontend**  
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
docker run -p 5000:5000 --env-file .env waf_project
```

## **🌍 Deploy on Render**  

### **1️⃣ Backend Deployment**  
1. **Push your changes to GitHub**.  
2. **Connect the repository to Render**.  
3. **Set up a Web Service** for Flask using `render.yaml`.  

### **2️⃣ Frontend Deployment**  
1. Inside the `client/` folder, run:  
   ```sh
   npm run build
   ```
2. Upload the `build/` folder to **Render** as a **Static Site**.  

## **🐝 Contributing**  
Contributions are welcome! Feel free to **fork** this repository, create new features, and submit **pull requests**.  

## **📚 License**  
This project is open-source under the **MIT License**.  
