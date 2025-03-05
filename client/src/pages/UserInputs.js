import React, { useState, useEffect } from "react";
import "../styles/userinputs.scss";

const UserInput = () => {
  const [input, setInput] = useState("");
  const [error, setError] = useState("");
  const [response, setResponse] = useState(null);

  useEffect(() => {
    console.log("✅ UserInput Component Loaded");
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();

    console.log("🔹 Submitting:", input);

    if (!input.trim()) {
      setError("❌ Input cannot be empty.");
      console.log("❌ Error: Input is empty");
      return;
    }
    setError("");

    try {
      console.log("🔹 Sending request to API...");
      const res = await fetch('${API_BASE_URL}/api/user-input', {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ input }),
      });

      console.log("🔹 Response received:", res);
      const data = await res.json();
      console.log("🔹 Response Data:", data);

      if (res.ok) {
        setResponse(`✅ ${data.message}`);
      } else {
        setResponse(`❌ Error ${res.status}: ${data.error || "Blocked by WAF"}`);
      }
    } catch (err) {
      console.error("❌ Error:", err);
      setError("❌ Error connecting to the server.");
    }

    setInput("");
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
          />
          {error && <p className="error-message">{error}</p>}
          <button type="submit" className="submit-btn">
            Submit
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