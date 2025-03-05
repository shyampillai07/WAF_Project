import React, { useState, useEffect } from "react";
import { FaDatabase, FaCode, FaTerminal, FaFolderOpen, FaTachometerAlt, FaShieldAlt } from "react-icons/fa";
import "../styles/protectionrules.scss";
import { API_BASE_URL } from "../config";

const iconMap = {
  SQLi: <FaDatabase />,
  XSS: <FaCode />,
  "Command Injection": <FaTerminal />,
  "Path Traversal": <FaFolderOpen />,
  "Rate Limiting": <FaTachometerAlt />,
};

const ProtectionRules = () => {
  const [rules, setRules] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [updatingRuleId, setUpdatingRuleId] = useState(null);

  console.log("🔹 ProtectionRules Component Loaded");

  // Fetch Protection Rules
  useEffect(() => {
    const fetchRules = async () => {
      try {
        console.log("🔹 Fetching protection rules...");
        const response = await fetch(`${API_BASE_URL}/api/protection-rules`);

        if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);

        const data = await response.json();
        console.log("✅ Raw API Response:", data);

        // Validate that `data.rules` is an array
        if (!data || typeof data !== "object" || !Array.isArray(data.rules)) {
          throw new Error("Invalid API response format: 'rules' should be an array.");
        }

        setRules(
          data.rules.map((rule) => ({
            ...rule,
            icon: iconMap[rule.name] || <FaShieldAlt />,
          }))
        );
      } catch (err) {
        console.error("❌ Error fetching protection rules:", err.message);
        setError("Failed to load protection rules.");
      } finally {
        setLoading(false);
      }
    };

    fetchRules();
  }, []);

  // Toggle Rule
  const toggleRule = async (id, currentStatus) => {
    if (updatingRuleId) return; // Prevent multiple rapid clicks
    setUpdatingRuleId(id);
    console.log(`🔹 Toggling rule ${id}:`, !currentStatus);

    try {
      const response = await fetch(`http://127.0.0.1:5000/api/protection-rules/${id}`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ enabled: !currentStatus }),
      });

      if (!response.ok) throw new Error(`Failed to update rule (Status: ${response.status})`);

      // Update rule state optimistically
      setRules((prevRules) =>
        prevRules.map((rule) => (rule.id === id ? { ...rule, enabled: !currentStatus } : rule))
      );

      console.log(`✅ Rule ${id} updated successfully!`);
    } catch (err) {
      console.error(`❌ Error updating rule ${id}:`, err.message);
      setError("Failed to update rule. Please try again.");
    } finally {
      setUpdatingRuleId(null);
    }
  };

  return (
    <div className="protectionrules-container">
      <h1>Protection Rules</h1>
      {loading ? (
        <p>Loading rules...</p>
      ) : error ? (
        <p className="error-message">{error}</p>
      ) : (
        <div className="rules-grid">
          {rules.map((rule) => (
            <div key={rule.id} className={`rule-card ${rule.enabled ? "enabled" : "disabled"}`}>
              <div className="icon-wrapper">{rule.icon}</div>
              <div className="text-content">
                <h3>{rule.name}</h3>
                <p>{rule.description}</p>
              </div>
              <label className={`switch ${updatingRuleId === rule.id ? "disabled" : ""}`}>
                <input
                  type="checkbox"
                  checked={rule.enabled}
                  onChange={() => toggleRule(rule.id, rule.enabled)}
                  disabled={updatingRuleId === rule.id}
                />
                <span className="slider round"></span>
              </label>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default ProtectionRules;