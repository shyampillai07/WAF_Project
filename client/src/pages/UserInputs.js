import React, { useState } from "react";
import "../styles/userinputs.scss";
import API_BASE_URL from "../config";

const UserInput = () => {
  const [input, setInput] = useState("");
  const [error, setError] = useState("");
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!input.trim()) {
      setError("❌ Input cannot be empty.");
      return;
    }

    setError("");
    setLoading(true);

    try {
      const res = await fetch(`${API_BASE_URL}/api/user-input`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ input }),
      });

      const data = await res.json();

      if (res.ok) {
        setResponse(`✅ ${data.message}`);
      } else {
        setResponse(`❌ Error ${res.status}: ${data.error || "Blocked by WAF"}`);
      }
    } catch (err) {
      console.error("❌ Error:", err);
      setError("❌ Error connecting to the server.");
    } finally {
      setLoading(false);
      setInput("");
    }
  };

  return (
    <div className="userinputs-container">
      <div className="user-input-box">
        <h1>Enter Your Input</h1>
        <form className="user-input-form" onSubmit={handleSubmit}>
          <label htmlFor="userInput">Type Your Input:</label>
          <input
            type="text"
            id="userInput"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Enter your input..."
            disabled={loading}
          />
          {error && <p className="error-message">{error}</p>}
          <button type="submit" className="submit-btn" disabled={loading}>
            {loading ? "Submitting..." : "Submit"}
          </button>
        </form>
        {response && (
          <p className={`api-response ${response.includes("❌") ? "error-message" : "success-message"}`}>
            {response}
          </p>
        )}
      </div>
    </div>
  );
};

export default UserInput;