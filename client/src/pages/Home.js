import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import "../styles/home.scss";
import { FaShieldAlt, FaUser } from "react-icons/fa";
import API_BASE_URL  from "../config";

function Home() {
  const [message, setMessage] = useState("Loading...");

  useEffect(() => {
    console.log("✅ Home Component Loaded"); // Debugging

    fetch(`${API_BASE_URL}/api/home`)
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP error! Status: ${res.status}`);
        return res.json();
      })
      .then((data) => {
        console.log("🔹 API Response:", data); // Debugging
        setMessage(data.message || "Welcome to WAF Dashboard");
      })
      .catch((err) => {
        console.error("❌ Error fetching home data:", err);
        setMessage("Error: Unable to fetch home data");
      });
  }, []);

  return (
    <div className="home-container">
      <header className="home-header">
        <h1>{message}</h1>
        <p>Monitor and control web security threats in real time.</p>
      </header>

      <div className="home-dashboard">
        <div className="home-card">
          <FaShieldAlt className="home-icon" />
          <h3>Protection Rules</h3>
          <p>Manage and customize your firewall settings.</p>
          <Link to="/protectionrules" className="home-button">View Rules</Link>
        </div>

        <div className="home-card">
          <FaUser className="home-icon" />
          <h3>User Inputs</h3>
          <p>Analyze and filter user input for security threats.</p>
          <Link to="/userinputs" className="home-button">Check Inputs</Link>
        </div>
      </div>
    </div>
  );
}

export default Home;